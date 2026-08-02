"""Generate constellationData.py from the Grim Dawn database.

The output is meant to be raw game values. Anything judgemental - how many
enemies a proc hits, what shape it covers, whether a ground effect's damage
should be multiplied by its duration, how many times a summon gets to swing -
is left to devotionderive.py, which the analysis code applies at scoring time.
That is why abilities are emitted with their skill class and geometry rather
than with a hand-picked targets number, and why a summon is emitted with its
pet's per-hit damage, lifespan and attack speed rather than a total.

Two things about the records make this less direct than it sounds. A proc often
keeps nothing but a pointer to a buff record, and its trigger, its name and its
whole payload live there (gddata.procRecords). And a summon's damage is not in
the skill at all - the skill names a creature and the creature's own attack
skills carry the numbers (gddata.summonFor).

    python devotion.py --regenerate
"""
import re

from constants import damages, durationDamages
from gddata import (Database, starBonuses, geometryFor, lastValue, firstOf,
					procRecords, summonFor, weaponRestricts, damageBandsFor, AFFINITY)

# skill class -> the ability "type" the optimiser reasons about
TYPE_BY_CLASS = (
	("SpawnPet", "summon"),
	("BuffSelfShield", "shield"),
	("Heal", "heal"),
	("Attack", "attack"),
	("Buff", "buff"),
)

# templateAutoCast filename -> trigger. Order matters: onattackcrit contains
# onattack, and the health thresholds are spelled at45%health rather than
# onlowhealth, so they have to be recognised before anything else runs.
TRIGGERS = (
	("%health", "low health"),
	("onlowhealth", "low health"),
	("onattackcrit", "critical"),
	("oncrit", "critical"),
	("onattack", "attack"),
	("onmeleehit", "hit"),
	("onanyhit", "hit"),
	("onblock", "block"),
	("onkill", "kill"),
)


def identifier(name):
	"""Short stable id, the name models refer to a constellation by.

	Crossroads all share one FileDescription and are told apart by the affinity
	they grant, which the caller knows and this does not, so they return None.
	"""
	if name.lower().startswith("crossroads"):
		return None
	ident = re.sub(r"[^0-9a-zA-Z]+", "", name)
	return ident[0].lower() + ident[1:] if ident else None


def abilityType(skillClass):
	"""What kind of thing a proc is.

	The hand-written data called Behemoth, Dryad, Chariot of the Dead and Tree of
	Life heals because each hands back a lump of health. They are timed buffs
	that happen to include one, and nearly everything they give - the armour, the
	regeneration, the resistances - lasts only as long as the buff does, so they
	are scored on up-time like any other buff. Scoring them as heals charged the
	whole payload once per trigger and made Tree of Life worth twice a Blind Sage.
	"""
	for fragment, kind in TYPE_BY_CLASS:
		if fragment.lower() in skillClass.lower():
			return kind
	return "buff"


def triggerAndChance(records):
	"""The trigger a proc fires on, from whichever of its records declares it.

	Skills that delegate to a buff record (Huntress, Dire Bear, Dying God) carry
	templateAutoCast on the buff, not on the star's own skill.
	"""
	cast = ""
	for record in records:
		cast = (record.get("templateAutoCast") or "").lower()
		if cast:
			break
	if not cast:
		return None, None
	trigger = None
	for fragment, name in TRIGGERS:
		if fragment in cast:
			trigger = name
			break
	match = re.search(r"_(\d+)%", cast)
	chance = int(match.group(1)) / 100.0 if match else 1.0
	return trigger, chance


def procBonuses(records, db, summon=False, triggered=True):
	"""Proc output as raw game numbers, summed over every record that makes it up.

	A proc is rarely one record: the star's skill may delegate its whole payload
	to a buff record, and may separately carry a petBonusName whose identical
	field names apply to your pets instead of you. None of them define the same
	field twice, so they add rather than override.

	Two shapes matter beyond plain scalars:

	* Damage over time is stored as damage-per-second plus a duration, and is
	  emitted as [dps, seconds]. ability.py then charges dps * min(duration,
	  retrigger interval), because a DoT reapplied by the same source refreshes
	  rather than stacking. The hand-written data put the *total* in the dps
	  slot - Elemental Storm carried [196, 2] where the game says 98 over 2s -
	  so it counted those twice.

	* Anything with a matching <field>DurationMin is a timed debuff (resist
	  reduction, slows) and goes in the nested "duration" dict, which
	  setDebuffValue scales by how often the proc lands.

	summon=True reads a pet's records, where only what reaches the enemy counts.
	A skeleton's own lifesteal or a spectral current's own crit damage are the
	creature's business; folding them into the player's sheet would credit you
	with stats you never get.

	triggered=False is for a buff, where flat damage is damage the buff adds to
	your own attacks rather than damage the proc deals - Mogdrogen's Howl gives
	you bleed damage, it does not bleed anything itself.
	"""
	from gddata import FLAT, DIRECT, DEBUFF, ENEMY_FLAT, COSTS, STUNS, STUN_SCALE, isDebuff
	# (record, "" | "pet ") - a petBonusName record repeats the same field names
	# but aims them at your pets, which the optimiser names with a "pet " prefix
	pieces = []
	for record in records:
		pieces.append((record, ""))
		bonus = db.read(record["petBonusName"]) if record.get("petBonusName") else None
		if bonus:
			pieces.append((bonus, "pet "))

	out, timed = {}, {}
	for record, prefix in pieces:
		debuff = isDebuff(record)
		for field, name in FLAT.items():
			lo = lastValue(record.get(field + "Min", 0)) or 0
			hi = lastValue(record.get(field + "Max", 0)) or 0
			if not (lo or hi):
				continue
			if summon and not (name in damages or name in ENEMY_FLAT
							   or name.startswith("reduce ")):
				continue
			value = round((float(lo) + float(hi or lo)) / 2.0, 2)
			# only actual damage is scored as "triggered"; resist reduction and the
			# like keep their own name, and pet damage is named "pet bleed" rather
			# than "pet triggered bleed"
			key = prefix + (("triggered " + name)
							if name in damages and triggered and not prefix else name)
			seconds = lastValue(record.get(field + "DurationMin", 0)) or 0
			if seconds and name in durationDamages:
				# The duration on the field is the one that counts. A debuff aura
				# also states how long it sits on the enemy, and stretching the
				# damage over that instead charged Huntress's Rend five times its
				# bleed: 325 a second for one second, reapplied while you keep
				# hitting, is not 325 a second for five.
				out[key] = [value, round(float(seconds), 2)]
			elif seconds:
				timed[key] = timed.get(key, 0) + value
			elif not isinstance(out.get(key), list):
				out[key] = out.get(key, 0) + value
		for field, name in DIRECT.items():
			value = lastValue(record.get(field, 0)) or 0
			if not value:
				continue
			# On a debuff record these same fields say what is done to the enemy,
			# so a negative resistance is resistance reduction, and reducing the
			# enemy's offensive ability is worth what defence is worth. Anything
			# with no such counterpart - the enemy's own armour, its regeneration -
			# is dropped rather than credited to the player with the sign flipped.
			if debuff:
				if field not in DEBUFF or value >= 0:
					continue
				name, value = DEBUFF[field], -value
			elif summon:
				continue
			seconds = lastValue(record.get(field + "DurationMin", 0)) or 0
			target = timed if seconds else out
			key = prefix + name
			target[key] = target.get(key, 0) + round(float(value), 2)
		for field, name in COSTS.items():
			value = lastValue(record.get(field, 0)) or 0
			if value and not summon:
				out[prefix + name] = out.get(prefix + name, 0) - round(float(value), 2)
		for field in STUNS:
			seconds = lastValue(record.get(field + "Min", 0)) or 0
			if seconds and not prefix:
				out["stun %"] = out.get("stun %", 0) + round(float(seconds) * STUN_SCALE, 2)
	if timed:
		out["duration"] = timed
	return out


def summonConditions(summon):
	"""Raw spawn numbers as ability conditions.

	How many times a summon gets to swing is not decided here - devotionderive
	works that out from the lifespan and the pet's own attack speed. The one
	judgement this function does make is structural: a trap that detonates once
	and dies is scored as an attack rather than as a standing pet, because "what
	fraction of the fight is it up for" means nothing for a single detonation.
	That is how the hand-written data scored Widow's Arcane Bomb too.
	"""
	if summon["mode"] == "once":
		return {"type": "attack"}
	out = {"petMode": summon["mode"], "petMelee": bool(summon["melee"])}
	for key, name in (("lifespan", "lifespan"), ("limit", "limit"),
					  ("burst", "burst"), ("attackSpeed", "petAttackSpeed")):
		if summon[key]:
			out[name] = round(float(summon[key]), 2)
	return out


def literal(value):
	if isinstance(value, float) and value == int(value):
		return str(int(value))
	return repr(value)


def listLiteral(values):
	# nested, because a distance falloff is a list of (from, to, percent) bands
	return "[%s]" % ", ".join(listLiteral(v) if isinstance(v, list) else literal(v)
							  for v in values)


def dictLiteral(mapping):
	parts = []
	for key, value in sorted(mapping.items()):
		if isinstance(value, dict):
			parts.append('"%s":%s' % (key, dictLiteral(value)))
		elif isinstance(value, list):
			parts.append('"%s":%s' % (key, listLiteral(value)))
		else:
			parts.append('"%s":%s' % (key, literal(value)))
	return "{" + ", ".join(parts) + "}"


def generate(path="constellationData.py", root=None):
	db = Database(root) if root else Database()
	lines = ['"""Generated from the Grim Dawn database - do not edit.',
			 "",
			 "Regenerate after a game patch with:  python devotion.py --regenerate",
			 "",
			 "Values are raw game numbers. Proc shape, target count, how many ticks",
			 "an enemy takes and how often a summon swings are all derived at scoring",
			 "time by devotionderive.py, which is where that judgement belongs.",
			 '"""',
			 "from dataModel import Constellation, Star",
			 "from ability import Ability",
			 ""]
	used, count, procs = set(), 0, 0

	for path_ in db.constellations():
		record = db.read(path_)
		name = record.get("FileDescription", "")
		if not name or name.lower().endswith("bitmap"):
			continue
		requires = " ".join(
			"%d%s" % (record["affinityRequired%d" % i], AFFINITY[record["affinityRequiredName%d" % i]])
			for i in (1, 2, 3)
			if record.get("affinityRequired%d" % i) and record.get("affinityRequiredName%d" % i) in AFFINITY)
		provides = " ".join(
			"%d%s" % (record["affinityGiven%d" % i], AFFINITY[record["affinityGivenName%d" % i]])
			for i in (1, 2, 3)
			if record.get("affinityGiven%d" % i) and record.get("affinityGivenName%d" % i) in AFFINITY)

		if name.lower().startswith("crossroads"):
			letter = provides.strip()[-1:] if provides else ""
			ident = "x" + letter.upper()
			name = "Crossroads " + {"a": "Ascendant", "c": "Chaos", "e": "Eldritch",
									"o": "Order", "p": "Primordial"}.get(letter, letter)
		else:
			ident = identifier(name)
		if not ident or ident in used:
			continue
		used.add(ident)
		count += 1

		# devotionLinks<n> names the star that has to be taken before star n, so
		# a constellation is a tree rather than a chain - 58 of the 109 branch.
		# Flattening it into a chain made every star a prerequisite of the next
		# and left no proc reachable part-way along.
		stars = []
		for index in range(1, 9):
			button = record.get("devotionButton%d" % index)
			if not button:
				continue
			skillPath = db.read(button).get("skillName")
			stars.append((index, record.get("devotionLinks%d" % index),
						  db.read(skillPath) if skillPath else None))
		if not stars:
			continue

		restricts = sorted({tag for _, _, skill in stars if skill
							for tag in weaponRestricts(skill)})

		lines.append("%s = Constellation(%r, %r, %r)" % (ident, name, requires, provides))
		lines.append("%s.id = %r" % (ident, ident))
		if restricts:
			lines.append("%s.restricts = %r" % (ident, restricts))

		varFor = {}
		for position, (index, parent, skill) in enumerate(stars):
			var = "%s_%d" % (ident, position)
			varFor[index] = var
			records = procRecords(skill, db) if skill else []
			isProc = any(r.get("templateAutoCast") for r in records)
			bonuses = {} if (skill is None or isProc) else starBonuses(skill, db)
			lines.append("%s = Star(%s, %s, %s)"
						 % (var, ident, varFor.get(parent, "[]"), dictLiteral(bonuses)))
			if not isProc:
				continue
			trigger, chance = triggerAndChance(records)
			if not trigger:
				continue
			geometry = geometryFor(records)
			conditions = {"type": abilityType(skill.get("Class", "")),
						  "trigger": trigger, "chance": chance,
						  "skillClass": skill.get("Class", "")}
			for key in ("radius", "projectiles", "sparkMaxNumber", "waveDistance",
						"waveStartWidth", "waveEndWidth"):
				if geometry.get(key):
					conditions[key] = round(float(geometry[key]), 2)
			bands = damageBandsFor(records)
			if bands:
				conditions["damageBands"] = [list(band) for band in bands]
			recharge = firstOf(records, "skillCooldownTime", 0)
			if recharge:
				conditions["recharge"] = round(float(recharge), 2)
			# "duration" is the name Ability reads for how long a proc's effect
			# lasts - getUpTime and durationScale both key off it. Emitting it as
			# activeDuration left every generated buff with nothing to be up for.
			active = firstOf(records, "skillActiveDuration", 0)
			if active:
				conditions["duration"] = round(float(active), 2)
			payload, isSummon = records, conditions["type"] == "summon"
			if isSummon:
				summon = summonFor(skill, db)
				if not summon:
					continue
				conditions.update(summonConditions(summon))
				payload = summon["records"]
				geometry = geometryFor(payload)
				for key in ("radius", "waveDistance", "waveStartWidth", "waveEndWidth"):
					if geometry.get(key):
						conditions[key] = round(float(geometry[key]), 2)
			label = firstOf(records, "FileDescription", None) or name
			label = label.split(" - ", 1)[1].strip() if " - " in label else label
			lines.append("%s.addAbility(Ability(%r, %s, %s))"
						 % (var, label, dictLiteral(conditions),
							dictLiteral(procBonuses(payload, db, summon=isSummon,
													triggered=conditions["type"] in ("attack", "summon")))))
			procs += 1
		lines.append("")

	lines += ["# A proc part-way along a constellation can be bought on its own, so each",
			  "# such prefix is registered as a constellation in its own right.",
			  "Constellation.buildAbilityFragments(globals())"]

	with open(path, "w", encoding="utf-8") as handle:
		handle.write("\n".join(lines) + "\n")
	return count, procs
