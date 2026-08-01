"""Generate constellationData_generated.py from the Grim Dawn database.

The output is meant to be raw game values. Anything judgemental - how many
enemies a proc hits, what shape it covers, whether a ground effect's damage
should be multiplied by its duration - is left to devotionderive.py, which the
analysis code applies at scoring time. That is why abilities are emitted with
their skill class and geometry rather than with a hand-picked targets number.

    python devotion.py --regenerate
"""
import re

from gddata import Database, starBonuses, geometryFor, lastValue, AFFINITY

# skill class -> the ability "type" the optimiser reasons about
TYPE_BY_CLASS = (
	("SpawnPet", "summon"),
	("BuffSelfShield", "shield"),
	("Heal", "heal"),
	("Attack", "attack"),
	("Buff", "buff"),
)

# templateAutoCast filename -> trigger
TRIGGERS = (
	("onattackcrit", "critical"),
	("oncrit", "critical"),
	("onattack", "attack"),
	("onanyhit", "hit"),
	("onblock", "block"),
	("onlowhealth", "low health"),
	("onkill", "kill"),
)

FLAT_TO_TRIGGERED = True # proc damage is scored as "triggered <type>"


def identifier(name, provides):
	"""Short stable id. Crossroads all share a FileDescription, so split them
	by the affinity they grant, matching the xA/xC/xE/xO/xP the models use."""
	if name.lower().startswith("crossroads"):
		for label, letter in AFFINITY.items():
			if provides.startswith(label[0]) or label.lower() in name.lower():
				pass
		return None # resolved by the caller, which knows the affinity granted
	ident = re.sub(r"[^0-9a-zA-Z]+", "", name)
	return ident[0].lower() + ident[1:] if ident else None


def abilityType(skillClass):
	for fragment, kind in TYPE_BY_CLASS:
		if fragment.lower() in skillClass.lower():
			return kind
	return "buff"


def triggerAndChance(skill):
	cast = (skill.get("templateAutoCast") or "").lower()
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


def procBonuses(skill, db):
	"""Proc output, as raw game numbers. Min/Max stay separate - averaging is a
	modelling choice and belongs with the rest of them in the analysis code."""
	from gddata import FLAT, DIRECT
	out = {}
	for prefix, name in FLAT.items():
		lo = lastValue(skill.get(prefix + "Min", 0)) or 0
		hi = lastValue(skill.get(prefix + "Max", 0)) or 0
		if not (lo or hi):
			continue
		key = name if name in ("lifesteal %",) else "triggered " + name
		out[key] = round((float(lo) + float(hi or lo)) / 2.0, 2)
	for field, name in DIRECT.items():
		value = lastValue(skill.get(field, 0)) or 0
		if value:
			out[name] = out.get(name, 0) + round(float(value), 2)
	return out


def literal(value):
	if isinstance(value, float) and value == int(value):
		return str(int(value))
	return repr(value)


def dictLiteral(mapping):
	return "{" + ", ".join('"%s":%s' % (k, literal(v)) for k, v in sorted(mapping.items())) + "}"


def generate(path="constellationData_generated.py", root=None):
	db = Database(root) if root else Database()
	lines = ['"""Generated from the Grim Dawn database - do not edit.',
			 "",
			 "Regenerate with:  python devotion.py --regenerate",
			 "",
			 "Values are raw game numbers. Proc shape, target count and duration",
			 "scaling are derived at scoring time by devotionderive.py.",
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
			ident = identifier(name, provides)
		if not ident or ident in used:
			continue
		used.add(ident)
		count += 1

		stars = []
		for index in range(1, 9):
			button = record.get("devotionButton%d" % index)
			if not button:
				continue
			skillPath = db.read(button).get("skillName")
			stars.append(db.read(skillPath) if skillPath else None)
		if not stars:
			continue

		restricts = sorted({tag for skill in stars if skill
							for field, tag in _WEAPONS.items() if skill.get(field)})

		lines.append("%s = Constellation(%r, %r, %r)" % (ident, name, requires, provides))
		lines.append("%s.id = %r" % (ident, ident))
		if restricts:
			lines.append("%s.restricts = %r" % (ident, restricts))

		previous = "[]"
		for position, skill in enumerate(stars):
			var = "%s_%d" % (ident, position)
			bonuses = {} if (skill is None or skill.get("templateAutoCast")) else starBonuses(skill, db)
			lines.append("%s = Star(%s, %s, %s)" % (var, ident, previous, dictLiteral(bonuses)))
			previous = var
			if skill is None or not skill.get("templateAutoCast"):
				continue
			trigger, chance = triggerAndChance(skill)
			if not trigger:
				continue
			geometry = geometryFor(skill, db)
			conditions = {"type": abilityType(skill.get("Class", "")),
						  "trigger": trigger, "chance": chance,
						  "skillClass": skill.get("Class", "")}
			for key in ("radius", "projectiles", "sparkMaxNumber", "waveDistance",
						"waveStartWidth", "waveEndWidth"):
				if geometry.get(key):
					conditions[key] = round(float(geometry[key]), 2)
			recharge = lastValue(skill.get("skillCooldownTime", 0)) or 0
			if recharge:
				conditions["recharge"] = round(float(recharge), 2)
			active = lastValue(skill.get("skillActiveDuration", 0)) or 0
			if active:
				conditions["activeDuration"] = round(float(active), 2)
			label = skill.get("FileDescription", name)
			label = label.split(" - ", 1)[1].strip() if " - " in label else label
			lines.append("%s.addAbility(Ability(%r, %s, %s))"
						 % (var, label, dictLiteral(conditions), dictLiteral(procBonuses(skill, db))))
			procs += 1
		lines.append("")

	with open(path, "w", encoding="utf-8") as handle:
		handle.write("\n".join(lines) + "\n")
	return count, procs


_WEAPONS = {"Sword": "sword", "Sword2h": "2h-sword", "Axe": "axe", "Axe2h": "2h-axe",
			"Mace": "mace", "Mace2h": "2h-mace", "Spear": "spear", "Staff": "staff",
			"Dagger": "dagger", "Scepter": "scepter", "Shield": "shield",
			"Offhand": "offhand", "Ranged1h": "ranged", "Ranged2h": "ranged"}
