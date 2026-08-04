"""Generate skillData.py from the Grim Dawn database.

A mastery's skills hang off records/ui/skills/class<NN>/skill<MM>.dbr, each of
which names one skill record, and every number on that record is an array
running from the first point spent upwards. The optimiser wants one Ability per
level, so each level is read as its own record through gddata.atLevel and put
through the same bonus extraction the devotion procs use.

What kind of thing a skill is comes from its class, and that also settles how it
is triggered:

  Skill_Passive, Skill_Modifier, Skill_Transmuter   always on
  ...Toggled                                        a stance you leave running
  Skill_PassiveOn<something>BuffSelf                fires on that something
  Skill_WeaponPool_*, Skill_WPAttack_*              a weapon-pool attack, which
                                                    replaces an ordinary swing
  everything else                                   a button you press

    python devotion.py --regenerate
"""
import re

from gddata import Database, atLevel, firstOf, lastValue, procRecords
from devotiongen import dictLiteral, procBonuses

MASTERY = re.compile(r"/_classtraining_class(\d+)\.dbr$")

# Which skill a modifier modifies, from the name of its record. Nothing on the
# record says it - see parentOf - so these take the naming convention apart.
# A pet modifier and Nightblade's "_mod<N>" hang the suffix off the base name.
PARENT_SUFFIX = re.compile(r"(_petmodifier|_petmod|_mod\d*)$")
# <base><number><letter>, any part of which may be absent.
NUMBERED = re.compile(r"^(.*?)(\d+)([a-z]?)$")
# A skill is a candidate for a parent only if it is one of these.
MODIFIER_CLASSES = ("Modifier", "Transmuter", "SkillSecondary_")

# class fragment -> (type, trigger). First match wins, so the specific
# PassiveOn... forms have to come before plain Passive.
KINDS = (
	("PassiveOnLife", ("buff", "low health")),
	("PassiveOnCrit", ("buff", "critical")),
	("PassiveOnHit", ("buff", "hit")),
	("PassiveOnKill", ("buff", "kill")),
	("PassiveOnBlock", ("buff", "block")),
	("Toggled", ("buff", "toggle")),
	("Passive", ("buff", "passive")),
	("Modifier", ("buff", "passive")),
	("Transmuter", ("buff", "passive")),
	("Shapeshift", ("buff", "toggle")),
	# Two kinds of weapon attack and the difference matters. A WPAttack is one of
	# the pool that sometimes replaces a swing, so the optimiser charges it
	# -100% weapon damage: the swing it replaced was already counted. A
	# WeaponPool skill - Savagery, Cadence - is the swing, and is not.
	("WPAttack", ("wps", "attack")),
	("WeaponPool", ("aar", "attack")),
	("SpellBeam", ("aar", "attack")),
	("SpellDrain", ("aar", "attack")),
	("SpawnPet", ("summon", "manual")),
	("Attack", ("attack", "manual")),
	("Buff", ("buff", "manual")),
)
# A skill states its own chance under one of these, and they mean different
# things: a weapon pool skill's weight is its percentage chance to replace a
# swing, and an on-hit passive states its activation chance outright.
CHANCE_FIELDS = ("skillChanceWeight", "onHitActivationChance")


def kindOf(skillClass):
	for fragment, kind in KINDS:
		if fragment.lower() in skillClass.lower():
			return kind
	return "buff", "passive"


def masteries(db):
	"""class number -> mastery name, e.g. 1 -> Soldier."""
	out = {}
	for path in db.under("records/skills/playerclass"):
		match = MASTERY.search(path)
		if match:
			name = db.name(db.read(path))
			if name:
				out[int(match.group(1))] = name
	return out


def skillsOf(db, classNumber):
	"""Every named skill in one mastery's tree, in the order the tree lists it.

	An aura keeps its name on the buff record it delegates to rather than on the
	skill the tree points at, so the name is taken from the first record that has
	one - without that, Field Command and Mogdrogen's Pact have no name at all.

	Two sources, because the buttons are not the whole mastery. A skill a
	transformation grants has no button of its own - it appears on the bar the
	form gives you - so walking the UI alone missed the four skills the Berserker
	gets in Werewolf form, Feral Claws among them. That is not a corner: Feral
	Claws is the primary attack of every Werewolf build there is, and a model
	naming it as its main attack could not look it up.

	The class tree record lists everything the mastery grants, so it is read as
	well. Across the other nine masteries it adds exactly one entry each, the
	mastery bar itself, which is a real node and is kept.

	Yields (name, record, stem), where the stem is the record's file name without
	its extension. That is the only thing that says which skill a modifier
	modifies - see parentStems - and it is taken from the path the tree points
	at rather than from the record resolve() may swap in, since a pet modifier's
	payload lives on the pet's skill while its place in the tree does not.
	"""
	out = []
	seen = set()

	def add(path):
		skill = db.read(path) if path else None
		if not skill:
			return
		stem = path.split("/")[-1].rsplit(".", 1)[0]
		skill = resolve(skill, db)
		name = next((db.name(r) for r in procRecords(skill, db) if db.name(r)), "")
		if name and name not in seen:
			seen.add(name)
			out.append((name, skill, stem))

	for index in range(1, 40):
		button = db.read("records/ui/skills/class%02d/skill%02d.dbr" % (classNumber, index))
		add(button.get("skillName") if button else None)

	tree = db.read("records/skills/playerclass%02d/_classtree_class%02d.dbr"
				   % (classNumber, classNumber))
	for field, path in sorted((tree or {}).items()):
		if re.fullmatch(r"skillName\d+", field) and isinstance(path, str):
			add(path)
	return out


def resolve(skill, db):
	"""The record a tree node's numbers actually live on.

	A pet modifier node holds nothing but a pointer to one of the pet's own
	skills, and that is where both its name and its payload are. Some of those
	are auras the pet radiates over you - Emboldening Presence is the Briarthorn
	buffing its owner - and some are the pet's own attacks.
	"""
	target = skill.get("petSkillName") if "PetModifier" in (skill.get("Class") or "") else None
	nested = db.read(target) if target else None
	return nested or skill


def parentStems(stem):
	"""Record names the skill at `stem` could be a modifier of, best first.

	Nothing on a modifier's record names its parent - `onslaught2.dbr` is Open
	Wounds and says only that it is a Skill_Modifier - so the tree's naming is
	all there is, and it is consistent enough to take apart:

	    onslaught2, onslaught3   -> onslaught1     a numbered modifier
	    onslaught1b              -> onslaught1     a letter is a transmuter
	    arcanemissile2           -> arcanemissile  where the base takes no 1
	    ringofsteel_mod1         -> ringofsteel    Nightblade spells it this way
	    mortartrap2_petmod       -> mortartrap1    a modifier on a summon
	    stormtotem01b_petmod...  -> stormtotem01   both at once

	A zero-padded number is deliberately not treated as a family. `passive01`
	through `passive04` are four separate skills a mastery grants, not three
	modifiers on the first, and Form of the Beast is `passive04` - so reading
	that as a child of `passive01` would attach a mastery passive to an
	unrelated one. Only a trailing letter makes a padded name a child.

	Returns () where the name says nothing, which is the honest answer for the
	four skills in the game that this cannot place.
	"""
	suffixed = PARENT_SUFFIX.sub("", stem)
	match = NUMBERED.match(suffixed)
	if not match:
		# "ringofsteel_mod1" leaves "ringofsteel", which is the base itself
		return (suffixed + "1", suffixed) if suffixed != stem else ()
	base, digits, letter = match.groups()
	if letter:
		return (base + digits,)
	if digits.startswith("0"):
		return ()
	return (base + "1", base)


def parentOf(stem, records):
	"""The record name `stem` modifies, or None. `records` is one mastery's tree."""
	return next((p for p in parentStems(stem) if p in records and p != stem), None)


def topLevel(skill, db):
	"""How many points the skill takes, ultimate ranks included.

	A buff skill keeps its ladder where it keeps its name: on the buff record it
	delegates to, not on the node the tree points at. curse1.dbr states no
	skillMaxLevel at all - curse1_buff.dbr states 10 and 20 - so reading the node
	alone gave a top of 1 for fifty of the three hundred skills, Curse of
	Frailty, Blood of Dreeg and Word of Pain among them. They came out one level
	long, and since Skill.getAbility clamps to maxLevel, every rank a model
	stated for one of them was silently pinned to the first point spent.

	So the ladder is taken from the first record in the chain that states one,
	the same way skillsOf takes the name.
	"""
	records = procRecords(skill, db)
	top = firstOf(records, "skillUltimateLevel") or firstOf(records, "skillMaxLevel")
	return int(top or 1)


def levelAbility(skill, db, level):
	"""What one skill looks like at one level."""
	view = atLevel(skill, level)
	skillClass = skill.get("Class", "")
	kind, trigger = kindOf(skillClass)
	conditions = {"type": kind, "trigger": trigger, "skillClass": skillClass}

	chance = 0
	for field in CHANCE_FIELDS:
		chance = lastValue(view.get(field, 0)) or 0
		if chance:
			break
	conditions["chance"] = round(float(chance) / 100.0, 3) if chance else 1
	for field, name in (("skillCooldownTime", "recharge"), ("skillActiveDuration", "duration")):
		value = lastValue(view.get(field, 0)) or 0
		if value:
			conditions[name] = round(float(value), 2)

	# A buff hands you damage to put on your own attacks; an attack deals it
	# itself. Same distinction the devotion procs make. A weapon attack sits with
	# the buffs: its flat damage is damage your swing does, which is what the
	# models weight when they weight "physical" rather than "triggered physical".
	# Every record in the chain is levelled, not just the top one: a toggled
	# aura keeps its numbers on the buff it delegates to, and reading that at
	# full rank gave every point in Emboldening Presence its level 22 value.
	records = [atLevel(nested, level) for nested in procRecords(skill, db)]
	bonuses = procBonuses(records, db, triggered=kind in ("attack", "summon"))
	return conditions, bonuses


def generate(path="skillData.py", root=None):
	db = Database(root) if root else Database()
	lines = ['"""Generated from the Grim Dawn database - do not edit.',
			 "",
			 "Regenerate after a game patch with:  python devotion.py --regenerate",
			 "",
			 "One Ability per point spent, indexed by level, so levels[3] is the skill",
			 "with three points in it. Level 0 is the empty string: no points, no skill.",
			 '"""',
			 "from dataModel import Skill",
			 "from ability import Ability",
			 ""]
	skillCount, orphans = 0, []
	for classNumber, mastery in sorted(masteries(db).items()):
		lines.append("# === %s ===" % mastery)
		# Read the whole mastery before writing any of it. A parent has to be
		# named as a string, so it has to have been emitted - and a skill whose
		# every level yields no bonuses is dropped, which is not knowable until
		# its levels have been read.
		written = []
		for name, skill, stem in skillsOf(db, classNumber):
			top = topLevel(skill, db)
			levels = []
			for level in range(1, top + 1):
				conditions, bonuses = levelAbility(skill, db, level)
				if not bonuses:
					continue
				levels.append("\t\tAbility(%r, %s, %s),"
							  % (str(level), dictLiteral(conditions), dictLiteral(bonuses)))
			if not levels:
				continue
			written.append((name, stem, levels, skill.get("Class") or ""))

		byStem = {stem: name for name, stem, _, _ in written}
		parents = {}
		for name, stem, _, skillClass in written:
			if not any(kind in skillClass for kind in MODIFIER_CLASSES):
				continue
			parent = parentOf(stem, byStem)
			if parent:
				parents[name] = byStem[parent]
			else:
				orphans.append((mastery, name, stem))

		# Parents first, so the Skill constructor can link a child to one that
		# already exists. One pass is enough - a modifier never has modifiers -
		# but it is written as a loop so that a deeper tree would not silently
		# emit a forward reference.
		order, pending = [], list(written)
		while pending:
			ready = [s for s in pending if parents.get(s[0]) in (None,)
					 or parents[s[0]] in {n for n, _, _, _ in order}]
			if not ready:
				ready = pending          # a cycle, which the data does not have
			order += ready
			pending = [s for s in pending if s not in ready]

		for name, stem, levels, _ in order:
			parent = parents.get(name)
			lines.append("Skill(%r, %r, [" % (name, mastery))
			lines.append('\t\t"",')
			lines.extend(levels)
			lines.append("\t]%s)" % (", %r" % parent if parent else ""))
			skillCount += 1
		lines.append("")

	with open(path, "w", encoding="utf-8") as handle:
		handle.write("\n".join(lines) + "\n")
	return len(masteries(db)), skillCount, orphans
