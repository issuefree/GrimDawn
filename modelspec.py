"""Model file defaults, validation and scaffolding.

A model file declares three things: devotionPoints, a `stats` dict (your character
sheet) and a `weights` dict (how much you value each stat). Historically five
stats keys were required with no documentation, and omitting one produced
KeyError: 'attacks/s' or TypeError: 'int' object is not iterable. Misspelling a
weight was worse - it was silently ignored, so the optimiser quietly scored
against a stat you thought you had asked for.

This module gives the required keys sensible defaults, and checks both dicts
against the vocabulary the optimiser can actually score, suggesting a correction
when a key looks like a near miss.
"""
import collections
import difflib
import os

from dataModel import Constellation
from constants import (damages, DOT_SECONDS, resists, primaryDamages,
                       conversions)

# Must be supplied; there is no defensible default for these.
# The one key in a damagePriority block that is not a damage type: what
# every type you did not name is worth. Spelled the way the weight it
# replaces was spelled, so a model moving one line keeps the same word.
CATCH_ALL = "damage"

# The other reserved key in a damagePriority block: derive every damage weight
# from what the rotation deals, instead of stating a preference per type. Its
# value is what the largest weight should come out at.
ROTATION = "rotation"

# Three things about the incoming side that no record states, used only by
# applyDefensePriority and named every run it uses them.
#
# A character absorbs 70% of physical damage up to their armor value with
# nothing on their gear saying otherwise; "armor absorb" on the sheet wins.
ARMOR_ABSORB_DEFAULT = 70.0
def hitsTaken(stats):
	"""How often you are hit. Stated if you say so, otherwise derived.

	Not "hits/s", which is hits you land - a hit-triggered proc fires off yours,
	not theirs.

	Derived, it is the same circle Ability.effectiveTargets measures for a
	point-blank area effect, read from the other end: the enemies your own pbaoe
	would cover are the enemies close enough to swing at you. Same density, same
	playStyle adjustment, same ceiling. So a tank standing in a room takes four
	hits a second where a kiting archer takes half of one, and against a single
	boss both take one - which is the shape a retribution build actually has.
	"""
	stated = float(stats.get("hits taken/s") or 0)
	if stated:
		return stated
	import devotionderive
	return devotionderive.hitsTakenFor(stats.get("playStyle"),
									   stats.get("enemy density") or None,
									   stats.get("enemies"))
# And how much of what hits you is physical, which is the only thing armor
# reduces. A guess, and the one number here with nothing behind it: monster
# damage lives on their skills rather than their records, so it is not a mean
# over anything the way ENEMY_RESIST_BASE is.
PHYSICAL_SHARE = 0.5

REQUIRED_POINTS = "devotionPoints"
REQUIRED_STATS = {
	"attacks/s": "your Attack Speed off the sheet - how fast you swing. Not a "
				 "sum of everything you press; that is what 'rotation' lists",
	"playStyle": "one of: melee, shortranged, ranged, tank",
}

# Keys a model used to write that resolveRotation now derives. Both said things
# the one rotation list already says, and saying them twice let them disagree:
# every model wrote its held attack in both, and three wrote it only in
# allAttacks/s and so were priced against a bare swing they never made.
RETIRED_STATS = {
	"allAttacks/s": "renamed to 'rotation' - it lists skills, not rates, and "
					"'allAttacks/s' beside 'attacks/s' read as a total of it",
	"main attack": "derived from 'rotation' now. The first entry is the attack "
				   "you hold the button on, and a passive, a toggle or a "
				   "SkillSecondary_ anywhere in the list is a modifier on it - "
				   "so put the modifiers in the rotation and delete this",
}
PLAY_STYLES = ("melee", "shortranged", "ranged", "tank")

# Control keys that are not character-sheet numbers.
CONTROL_STATS = {
	"attacks/s", "allAttacks/s", "hits/s", "blocks/s", "kills/s", "criticals/s",
	"low healths/s", "crit chance", "fight length", "playStyle", "weapons",
	"blacklist", "difficulty", "level",
	# what you fight, rather than what you are. "enemy density" (enemies per
	# square metre) sizes every area proc in devotionderive; "enemy defense" is
	# the defensive ability crit chance is worked out against. Both were read
	# by the code already and neither was listed here, so a model that set one
	# was told it was an unknown stat and never read.
	"enemy density", "enemy defense",
	# how many are actually in front of you, which caps what any one cast can
	# reach. Density cannot say it: a chain jumps to a fixed number of separate
	# targets however sparse the room, and against a boss it jumps to one.
	"enemies",
	# how often you are hit, which is not "hits/s" - that is hits you land, and
	# it is what a hit-triggered proc fires off. Only applyDefensePriority reads
	# this, to say what armor stops over a fight.
	"hits taken/s",
	# the skill bar. Stated as skills and ranks; resolveRotation replaces it with
	# (skill, ability, rate) triples, because the names are the interesting part
	# and rotationDamage cannot work out what a build deals from bare rates.
	"rotation",
	# both derived from it, and both listed here because they end up in stats:
	# the bare rates a proc's trigger is scored against, and the attack you hold
	# the button on together with the modifiers that hang off it.
	"allAttacks/s", "main attack",
}


def weaponTypes():
	"""Every weapon tag any constellation restricts on, so the default restricts nothing."""
	tags = set()
	for c in Constellation.constellations:
		tags.update(c.restricts)
	return sorted(tags)


def applyDefaults(stats):
	"""Fill in the keys that used to be mandatory boilerplate. Returns notes applied."""
	notes = []
	if "allAttacks/s" not in stats and "attacks/s" in stats:
		stats["allAttacks/s"] = [stats["attacks/s"]]
		notes.append("%s, so every proc is scored against attacks/s alone - list "
					 "the skills on your bar and their ranks for a better estimate"
					 % ("no 'rotation'" if "rotation" not in stats
						else "nothing in 'rotation' resolved to a rate"))
	if "weapons" not in stats:
		stats["weapons"] = weaponTypes()
		notes.append("weapons defaulted to all types (no constellation excluded)")
	if "blacklist" not in stats:
		stats["blacklist"] = []
	return notes


def itemAbilities():
	"""Every skill an item grants, by the name the game gives it.

	115 components, augments and pieces of gear carry one, and a good part of
	any bar is made of them - Sacred Strike off Blessed Steel, Shield Slam off
	a Battered Shell. They are not in skillData, which holds mastery skills
	only, so a rotation naming one used to have to fall back to a bare number
	with the skill's name in a comment.

	Returns {name: (ability, item name)}. First one wins where two items grant
	the same skill, and the item is kept only so the note can say where it came
	from.
	"""
	import itemData
	out = {}
	equipment = getattr(itemData, "equipment", {})
	pools = (itemData.components, itemData.augments,
			 list(equipment.values()) if isinstance(equipment, dict) else list(equipment))
	for pool in pools:
		for item in pool:
			if item.ability and item.ability.name not in out:
				out[item.ability.name] = (item.ability, item.name)
	return out


_ITEM_ABILITIES = {}


def items():
	"""itemAbilities(), built once - it walks every component and augment."""
	if not _ITEM_ABILITIES:
		_ITEM_ABILITIES.update(itemAbilities())
	return _ITEM_ABILITIES


def plainDamage(bonus):
	"""The damage type a bonus key names, or None if it does not name one.

	skillgen writes an attack's own damage as "triggered X" and a buff's as
	plain "X". It is the same damage - Feral Claws' 117 pierce reads as nothing
	if the prefix is left on - so the prefix comes off and the three places that
	were each stripping it with their own comment ask here instead.
	"""
	plain = bonus[len("triggered "):] if bonus.startswith("triggered ") else bonus
	return plain if plain in damages else None


def isModifier(ability):
	"""True for a skill that is never pressed but changes the one you hold down.

	Two ways to tell, both off the record rather than off which key the model
	filed it under. A SkillSecondary_ goes off as part of its parent - Explosive
	Strike fires with Fire Strike, and carries 30% weapon damage of its own. A
	passive or a toggle is not a press at all: Open Wounds bleeds for Onslaught,
	Werewolf is the form Feral Claws comes from, Disintegration is a rank on a
	beam. None of them is a button, and all of them modify what you swing.
	"""
	return (str(ability.gc("skillClass") or "").startswith("SkillSecondary_")
			or ability.gc("trigger") in ("passive", "toggle"))


def recordedParent(name):
	"""What the records say `name` modifies, or None.

	skillgen reads it out of the tree's record names, so Open Wounds knows it is
	Onslaught's and Fault Line knows it is Leap's. The rotation says where a
	modifier goes; this is what checks it, and what tells you where to put one
	you have written in the wrong place.
	"""
	from models import Skill
	skill = Skill.skills.get(name)
	parent = skill.parent() if skill else None
	return parent.name if parent else None


def splitEntry(entry):
	"""(name, rank, press, modifiers) out of one rotation entry.

	The elements after the name are read by type rather than by position, since
	a press interval is optional and a skill with modifiers and no interval
	would otherwise leave a hole to count past. A list is the modifiers; the
	numbers are the rank and then the press.
	"""
	rest = list(entry[1:])
	modifiers = next((r for r in rest if isinstance(r, list)), [])
	numbers = [r for r in rest if not isinstance(r, list)]
	rank = numbers[0] if numbers else 0
	press = float(numbers[1] or 0) if len(numbers) > 1 else 0.0
	return entry[0], rank, press, modifiers


def resolveRotation(stats):
	"""Turn the skill bar into the rate each skill actually fires at.

	One list says what you play. An entry is a mastery skill and its rank, an
	item skill and how often you press it, or a bare rate for anything the data
	cannot name:

	    ("Mortar Trap", 12)          fires on its own cooldown
	    ("Flashbang", 12, 3.0)       ...unless you press it slower than that
	    ("Sacred Strike", 1.5)       an item skill has no rank, so that is the press
	    0.5

	A skill that is never pressed but changes one that is - see isModifier - goes
	inside the entry for the skill it modifies, because that is the only thing it
	can modify:

	    ("Leap", 8, 1.5, [("Fault Line", 8)])
	    ("Onslaught", 1, [("Open Wounds", 3), ("Endless Rage", 1)])

	The nesting is the link, so there is nothing to spell and nothing to keep in
	step with a name written elsewhere. The elements after the name are read by
	type rather than by position - see splitEntry - so a skill with modifiers and
	no press interval does not leave a hole to count past.

	The records say what each modifier really modifies, and that is used to check
	the nesting rather than to decide it: one nested under the wrong skill says
	so, and one left at the top level is told which entry to move inside.

	A skill fires no faster than its cooldown and no faster than you press it,
	so the rate is one over whichever is longer. Which one wins is not obvious
	and differs per line - gwyr presses Rune of Hagarrad every 3.7 seconds
	against a 4 second cooldown, and Mortar Trap every 15 against 2.5, the
	second because a short cooldown is not always worth spamming.

	Written out as numbers this was a column of magic constants with the
	arithmetic in a comment beside it, going stale the moment a rank changed or
	the game was patched. Named, the cooldown comes from the records and the
	press interval stays what it is: a fact about how you play.

	Three sorts of entry are not presses, and the records say which is which
	rather than the model sorting them into keys of their own:

	  a weapon pool skill  fires instead of an ordinary swing, so its rate is
	                       attacks/s times its chance and the held attack keeps
	                       whatever is left. The pool is competitive, so chances
	                       that sum past one are normalised the way the game does
	  a modifier           never pressed. It rides the rate of the entry it is
	                       nested in, and where that entry is the held attack it
	                       is priced into a swing instead
	  the held attack      the first entry that is neither, which runs at
	                       attacks/s: that is what holding a button down means,
	                       and a stated cooldown does not describe it

	So "main attack" is read out of the same list rather than written down a
	second time. Every model used to state its held attack in both places, and
	three stated it only here - which left armitage, pakse and lochlan pricing
	every granted skill against a bare 100% swing none of them makes.

	"% Reduced Skill Cooldown" off the sheet is taken off first, the same
	reduction and the same 90% cap Ability.resolveTiming applies to a proc.

	Fills in, for everything downstream: "allAttacks/s", the bare rates a proc's
	trigger is scored against; "main attack", the held attack and its modifiers;
	and "rotation" itself, resolved to (name, ability, rate).
	"""
	notes = []
	for retired, why in RETIRED_STATS.items():
		if retired in stats:
			raise ValueError("stats[%r] is no longer read - %s" % (retired, why))
	entries = stats.get("rotation")
	if not entries:
		return notes
	if not any(isinstance(e, (tuple, list)) for e in entries):
		# A rotation of bare rates names nothing, so there is no cooldown to look
		# up and no held attack to find - but the rates themselves are still what
		# a proc's trigger is scored against, and dropping them here left
		# applyDefaults to replace the whole bar with a single attacks/s.
		stats["allAttacks/s"] = [float(e) for e in entries]
		return notes
	import skillData                       # noqa: F401 - registers the skills
	from models import Skill
	reduction = min(90.0, float(stats.get("reduce cooldown") or 0)) / 100.0
	swing = float(stats.get("attacks/s") or 0)

	# Look every named entry up first, so what kind of thing it is comes from its
	# record and not from where it sits in the list. Each becomes
	# (name, ability, rank, press, source, modifiers); source is None for a
	# mastery skill, and modifiers are the ones nested inside this entry, each
	# already looked up the same way.
	def look(entry, nested=False):
		if not entry or not isinstance(entry[0], str):
			notes.append("rotation: %r does not start with a skill name, so there is "
						 "nothing to look up. A modifier goes inside the entry for the "
						 "skill it modifies, not in a list of its own" % (entry,))
			return (None, None, 0, 0.0, None, [])
		name, rank, press, inner = splitEntry(entry)
		if nested and inner:
			notes.append("rotation: %r carries modifiers of its own, which is a level "
						 "deeper than the bar goes - nest them beside it instead" % name)
			inner = []
		skill = Skill.skills.get(name)
		if skill is not None:
			return (name, skill.getAbility(rank), rank, press, None,
					[look(m, True) for m in inner])
		# Not a mastery skill, so try what the items grant. There is no rank on
		# an item skill, so its first number is the press interval - and it is a
		# button of its own, which nothing in a mastery tree modifies.
		granted = items().get(name)
		if granted is None:
			notes.append("rotation: nothing called %r in the mastery skills or the "
						 "item skills, so it contributes no rate at all" % name)
			return (name, None, 0, 0.0, None, [])
		if inner:
			notes.append("rotation: %r comes off an item, and nothing in a mastery tree "
						 "modifies an item skill, so %s nested inside it is not scored"
						 % (name, ", ".join(repr(splitEntry(m)[0]) for m in inner)))
		ability, source = granted
		return (name, ability, None, float(rank or 0), source, [])

	looked = [look(e) if isinstance(e, (tuple, list)) else (None, None, 0, 0.0, None, [])
			  for e in entries]

	# A modifier is not a button, so one at the top level is in the wrong place.
	# The records know which entry it belongs inside, so say which.
	for name, ability, rank, _, source, _ in looked:
		if ability is None or source is not None or not isModifier(ability):
			continue
		parent = recordedParent(name)
		notes.append("rotation: %r modifies a skill rather than being pressed, so it "
					 "belongs inside that skill's entry - %s. It is not scored where "
					 "it is"
					 % (name, ("nest it in the %r line" % parent) if parent else
						"the records do not say which, so nest it in whichever you play"))

	# The weapon pool comes first because it changes what the held attack does.
	pool = {}
	for name, ability, _, _, source, _ in looked:
		if ability is not None and source is None and not isModifier(ability) \
		   and str(ability.gc("skillClass") or "").startswith("Skill_WPAttack_"):
			pool[name] = float(ability.gc("chance") or 0)
	claimed = sum(pool.values())
	if claimed > 1.0:
		pool = {k: v / claimed for k, v in pool.items()}
		notes.append("weapon pool chances sum to %.0f%%, so they are normalised "
					 "down the way the game does" % (100 * claimed))
		claimed = 1.0

	# The held attack: the first entry that is neither a modifier nor a pool
	# skill. Taking it by position rather than by class is what lets a beam,
	# a shapeshifted claw and a weapon pool basic attack all be one thing.
	held, heldRank = next(((name, rank) for name, ability, rank, _, source, _ in looked
						   if ability is not None and source is None
						   and not isModifier(ability) and name not in pool), (None, 0))

	rates, rows, resolved = [], [], []
	onHeld, elsewhere = [], []

	def attach(host, rate, nested):
		"""Put an entry's modifiers on it, once its own rate is known.

		A modifier on the attack you hold down is priced into a swing, which is
		what "main attack" carries. One on a skill you press has no swing to be
		part of, so it rides that skill's rate instead - which is the whole
		difference between Open Wounds and Fault Line.
		"""
		siblings = {m[0] for m in nested}
		for name, ability, rank, _, source, _ in nested:
			if ability is None or source is not None:
				continue                   # already complained about by name
			if not isModifier(ability):
				notes.append("rotation: %r is a %s, which the records call a button of "
							 "its own - nested here it is read as a modifier on %r "
							 "instead" % (name, ability.gc("skillClass"), host))
			recorded = recordedParent(name)
			if recorded and recorded != host and recorded not in siblings:
				notes.append("rotation: %r is nested in %r, but the records say it "
							 "modifies %r" % (name, host, recorded))
			if host == held:
				onHeld.append((name, rank))
			else:
				resolved.append((name, ability, rate))
				elsewhere.append("%s at %g on %s" % (name, rank, host))

	def orphaned(host, nested):
		if nested:
			notes.append("rotation: %s %s %r, which fires at no rate, so %s not scored "
						 "either" % (", ".join(repr(m[0]) for m in nested),
									 "modifies" if len(nested) == 1 else "modify", host,
									 "it is" if len(nested) == 1 else "they are"))

	def cooldownOf(ability, nested):
		"""A skill's cooldown, less what the modifiers nested in it take off.

		Some modifiers exist to change the recharge and nothing else: Frenzied
		Cry is four seconds off Rallying Cry and states no other number in its
		whole record. A few go the other way - Focused Gaze makes Dreeg's Evil
		Eye a charged shot and adds four seconds - so it is a sum, not a
		discount. The flat change lands before the sheet's "% Reduced Skill
		Cooldown", which is the order the game applies them in.

		Returns (cooldown, what the modifiers changed).
		"""
		base = float(ability.gc("recharge") or 0)
		change = sum(float(m[1].gc("recharge change") or 0)
					 for m in nested if m[1] is not None)
		return max(0.0, base + change) * (1.0 - reduction), change

	for entry, (name, ability, rank, press, source, nested) in zip(entries, looked):
		if name is None:
			# A bare rate, or an entry look could not read - which it has already
			# complained about, and which is not a number to fall back on.
			if not isinstance(entry, (tuple, list)):
				rates.append(float(entry))
			continue
		if ability is None:
			continue                       # already complained about by name
		if source is not None:
			if ability.gc("trigger") != "manual":
				notes.append("rotation: %r off %s fires on %r rather than being "
							 "pressed, so it belongs to its own trigger rather "
							 "than in a rotation" % (name, source, ability.gc("trigger")))
				continue
			cooldown = float(ability.gc("recharge") or 0) * (1.0 - reduction)
			interval = max(cooldown, press)
			if not interval:
				notes.append("rotation: %r off %s has no cooldown, so say how "
							 "often you press it" % (name, source))
				continue
			rates.append(1.0 / interval)
			resolved.append((name, ability, 1.0 / interval))
			rows.append("%s off %s: %.3g/s (%s)"
						% (name, source, 1.0 / interval,
						   "cooldown %gs" % cooldown if cooldown >= press
						   else "pressed every %gs" % press))
			continue
		if isModifier(ability):
			continue                       # already complained about, by name
		if name in pool:
			rate = swing * pool[name]
			rates.append(rate)
			resolved.append((name, ability, rate))
			rows.append("%s at %g: %.3g/s (weapon pool, %.0f%% of swings)"
						% (name, rank, rate, 100 * pool[name]))
			attach(name, rate, nested)
			continue
		if name == held:
			# Held down, so it runs at your swing rate - less whatever share of
			# those swings the weapon pool takes over, since a pool skill fires
			# instead of the ordinary attack.
			rate = swing * (1.0 - claimed)
			# Attached either way: what a swing is worth is a fact about the
			# skill even where the weapon pool leaves it no swings to make.
			attach(name, rate, nested)
			if not rate:
				# A pool that claims every swing means the attack it replaces
				# never happens - a real thing to build, but it should be said
				# rather than the entry quietly disappearing.
				notes.append("rotation: the weapon pool claims every swing, so %r "
							 "never fires on its own and contributes nothing. "
							 "Check the ranks: chances that sum past 100%% are "
							 "usually a sign one of them is guessed too high" % name)
				continue
			rates.append(rate)
			resolved.append((name, ability, rate))
			rows.append("%s at %g: %.3g/s (%s)"
						% (name, rank, rate,
						   "held, so attacks/s" if not claimed else
						   "held, less the %.0f%% of swings the weapon pool takes"
						   % (100 * claimed)))
			continue
		cooldown, change = cooldownOf(ability, nested)
		interval = max(cooldown, press)
		if not interval:
			# Not held, not a modifier, and nothing says how often it happens.
			notes.append("rotation: %r states no cooldown and is not the attack you "
						 "hold down, so nothing says how often it fires - say how "
						 "often you press it" % name)
			orphaned(name, nested)
			continue
		rates.append(1.0 / interval)
		resolved.append((name, ability, 1.0 / interval))
		rows.append("%s at %g: %.3g/s (%s)"
					% (name, rank, 1.0 / interval,
					   ("cooldown %gs%s" % (cooldown, ", %+gs from what modifies it" % change
											if change else ""))
					   if cooldown >= press else "pressed every %gs" % press))
		attach(name, 1.0 / interval, nested)

	stats["allAttacks/s"] = rates
	# Kept because the names are the interesting part and converting to bare
	# rates throws them away. rotationDamage reads this to work out what the
	# build actually deals, and it cannot do that from a column of numbers.
	stats["rotation"] = resolved
	if held:
		# The held attack first: models.py reads this to work out what one swing
		# is worth, and the modifiers only mean anything against it.
		stats["main attack"] = [(held, heldRank)] + onHeld

	if rows:
		notes.append("rotation from the skill data - " + "; ".join(rows))
	if elsewhere:
		notes.append("modifiers on skills you press, at that skill's rate - "
					 + "; ".join(elsewhere))
	if held:
		notes.append("main attack: %s at %g%s"
					 % (held, heldRank,
						", modified by " + ", ".join("%s at %g" % m for m in onHeld)
						if onHeld else " - nothing in the rotation modifies it"))
	return notes


def rotationDamage(stats):
	"""What the rotation deals per second, per damage type, and per point of what.

	The rotation says which skills fire and how often; the skill data says what
	each one delivers; the sheet says what it delivers it with. Between them
	there is no need to guess how much a build cares about fire - it deals what
	it deals.

	    D(X) = sum over skills of rate * (sheetFlat(X) * weaponPct/100 + own(X))
	                                   * (1 + X%/100)

	and the two derivatives that matter are what a weight is supposed to be:

	    d D(X) / d(flat X) = (1 + X%/100) * sum(rate * weaponPct/100)
	    d D(X) / d(X %)    = sum(rate * (sheetFlat(X) * weaponPct/100 + own(X))) / 100

	The first is the same for every type but for its percentage, because a point
	of flat damage rides on whatever share of your rotation swings a weapon. The
	second is where builds differ: it is what a percentage has to multiply, and
	a type you deal none of has nothing.

	Returns {damage: (perSecond, dFlat, dPerc)}. Empty if the rotation is bare
	numbers, since then there is nothing to read the skills off.
	"""
	rotation = stats.get("rotation")
	if not rotation:
		return {}
	import skillData                       # noqa: F401 - registers the skills
	from models import Skill, Model
	bonus = Model.attributeBonus(stats)
	# The modifiers hanging off the attack you hold the button on. They are not
	# separate presses so they carry no rate of their own, but their damage
	# lands every time it does - Open Wounds bleeds for Onslaught and nothing
	# else, and without this morena's bleed is only what her sheet carries.
	#
	# So they fire at the held attack's rate, which is looked up rather than
	# taken as the first line of the rotation. Those differ when the held attack
	# is not in the rotation at all: pakse's weapon pool claims every swing, so
	# Righteous Fervor never fires, and reading the first line instead gave its
	# modifiers the rate of Aegis of Menhir.
	firing = [(ability, rate) for _, ability, rate in rotation]
	stated = stats.get("main attack")
	if stated:
		if isinstance(stated[0], str):
			stated = [stated]
		rates = {name: rate for name, _, rate in rotation}
		heldRate = rates.get(stated[0][0], 0.0)
		for name, level in stated[1:]:
			skill = Skill.skills.get(name)
			if skill is not None and name not in rates:
				firing.append((skill.getAbility(level), heldRate))

	# swings per second, weighted by how much weapon damage each skill carries
	swings = 0.0
	own = {}
	for ability, rate in firing:
		swings += rate * ability.gb("weapon damage %") / 100.0
		for key, amount in ability.bonuses.items():
			plain = plainDamage(key)
			if plain is None:
				continue
			amount = amount[0] * amount[1] if isinstance(amount, list) else amount
			own[plain] = own.get(plain, 0.0) + rate * amount

	out = {}
	for damage in damages:
		if damage in ("elemental", "all damage"):
			continue
		flat = float(stats.get(damage, 0) or 0)
		perc = float(stats.get(damage + " %", 0) or 0) + bonus.get(damage, 0)
		multiplier = 1.0 + perc / 100.0
		base = flat * swings + own.get(damage, 0.0)
		out[damage] = (base * multiplier, multiplier * swings, base / 100.0)
	return out


def retaliationDamage(stats):
	"""What you deal per second by being hit, and per point of what.

	The other half of a retribution build, and the half no rotation can see:
	retaliation does not come off anything you press, it comes off being hit.
	So its rate is "hits taken/s" - the same figure armor is counted against -
	and everything else follows the way the attack side does.

	    R(X) = flat(X) * (1 + retaliation%/100) * hitsTaken

	    d R(X) / d(flat X)        = (1 + retaliation%/100) * hitsTaken
	    d R    / d(retaliation %) = sum(flat) * hitsTaken / 100

	Retaliation has its own multiplier rather than sharing the damage one: the
	game's tooltip says in as many words that "% All Damage does not affect
	Retaliation damage". Nor do the attribute bonuses, which is why nothing is
	added from cunning or spirit here.

	Returns ({damage: (perSecond, dFlat)}, dPercent).
	"""
	taken = hitsTaken(stats)
	percent = float(stats.get("all retaliation %", 0)
					or stats.get("retaliation %", 0) or 0)
	multiplier = 1.0 + percent / 100.0
	out, pool = {}, 0.0
	for damage in damages:
		if damage in ("elemental", "all damage"):
			continue
		flat = float(stats.get(damage + " retaliation", 0) or 0)
		if not flat:
			continue
		pool += flat
		out[damage] = (flat * multiplier * taken, multiplier * taken)
	return out, pool * taken / 100.0


def dotFactor(damage, stats):
	"""What a point of flat damage of this type delivers, against a point of physical.

	One for anything that lands on the swing. Less for a damage over time,
	because reapplying one refreshes it rather than stacking it: a point of
	bleed is three seconds' worth of bleed, and if you swing again in a third of
	a second you collected a ninth of it before overwriting the rest.

	So it is min(duration, attack interval) / duration - which is the same rule
	calculateBonus already applies to a proc's [dps, seconds] pair, now applied
	to the flat damage on the sheet as well. Both durations come from the game:
	DOT_SECONDS is read off the item records, where it is all but unanimous per
	type.

	This replaced a flat half, applied to a type reached through the catch-all
	and not to one named outright - which was the same number meaning two
	things again, and neither of them measured. A half is right at two attacks
	a second against a three second bleed and generous at anything faster;
	morena swings three times a second, where the answer is a ninth.

	A duration bonus deliberately does not lengthen the duration here. Grim
	Dawn's "+% Duration" raises the total damage by as much as it raises the
	time, so the damage per second is unchanged and so is what you collect
	before refreshing. What a longer duration buys is what the separate
	"X duration" weight is for.
	"""
	if damage not in DOT_SECONDS:
		return 1.0
	rate = float(stats.get("attacks/s") or 0)
	if not rate:
		return 1.0
	seconds = DOT_SECONDS[damage]
	return min(seconds, 1.0 / rate) / seconds


# One cast of your own attack, read out of the skills that make it up.
# percent    "% Weapon Damage" summed over the attack and its modifiers
# flat       damage of its own, per type, in calculateBonus's units
# boost      percentages it adds for itself, which the sheet does not carry
# longer     duration bonuses of its own, ditto
# abilities  the skills themselves, for asking how wide the swing is
# named      "<skill> at <rank>" per skill, for the note the load prints
# missing    names nothing in the skill data answers to
# mixed      (skill, damage) where a type arrived as both a number and a pair
MainAttack = collections.namedtuple(
	"MainAttack", "percent flat boost longer abilities named missing mixed")


def addFlat(store, damage, value):
	"""Add one skill's flat damage of a type to what the others already give.

	Two abilities of one attack can both carry a type - gwyr's Fire Strike has
	55 fire and Brimstone adds 60 more - and the game adds them. The value is
	either a number, meaning damage on the hit, or a [dps, seconds] pair,
	meaning a duration effect; calculateBonus prices the two differently, so
	they are summed in their own units and never converted into each other.

	Returns False without storing anything if the type arrives as both at once,
	which no record in the game does and which there is no honest sum for.
	"""
	if damage not in store:
		store[damage] = list(value) if isinstance(value, list) else value
		return True
	old = store[damage]
	if isinstance(old, list) != isinstance(value, list):
		return False
	if isinstance(old, list):
		# the same duration effect twice: the damage adds and the longer of the
		# two windows is the one it runs over
		store[damage] = [old[0] + value[0], max(old[1], value[1])]
	else:
		store[damage] = old + value
	return True


def mainAttack(stats):
	"""Read stats["main attack"] into what one cast of it is built from.

	The held attack and the modifiers hanging off it, which resolveRotation
	picks out of the rotation. Nothing any of them carries reaches the character
	sheet: the sheet is what applies to every attack you make, and a skill and
	its modifiers apply to that skill. Open Wounds bleeds for Onslaught and
	nothing else, and Endless Rage's 12% bleed lifts Onslaught's bleed on top of
	the sheet's own rather than being part of the 450% that applies to
	everything. So a cast is worked out from all three: the weapon damage it
	scales, the flat damage it adds, and the percentages it adds for itself.

	Returns a MainAttack, empty where nothing is named. This is read twice per
	load - once to price a swing against a granted skill, once to price the
	damage weights - and it used to be walked separately for each, which is how
	the two came to disagree about whether two skills carrying the same damage
	type add up.
	"""
	percent, flat, boost, longer = 0.0, {}, {}, {}
	abilities, named, missing, mixed = [], [], [], []
	stated = stats.get("main attack")
	if stated:
		if isinstance(stated[0], str):
			stated = [stated]
		import skillData                   # noqa: F401 - registers the skills
		from models import Skill
		for name, level in stated:
			skill = Skill.skills.get(name)
			if skill is None:
				missing.append(name)
				continue
			ability = skill.getAbility(level)
			# Kept so mainAttackTargets can ask them how wide they are. Not
			# scored here: how many enemies a swing covers depends on how many
			# there are, and that changes between the boss column and the pack.
			abilities.append(ability)
			percent += ability.gb("weapon damage %")
			for bonus, value in ability.bonuses.items():
				# fenris carries 200% pierce with no flat pierce on his sheet
				# precisely because Feral Claws' own 117 is where his pierce
				# comes from, which is what plainDamage is here to not lose.
				damage = plainDamage(bonus)
				if damage:
					if not addFlat(flat, damage, value):
						mixed.append((name, damage))
				elif bonus.endswith(" %") and bonus[:-2] in damages:
					boost[bonus[:-2]] = boost.get(bonus[:-2], 0) + value
				elif bonus.endswith(" duration") and bonus[:-9] in damages:
					longer[bonus[:-9]] = longer.get(bonus[:-9], 0) + value
			named.append("%s at %d" % (name, level))
	return MainAttack(percent, flat, boost, longer, abilities, named, missing, mixed)


def mainAttackDamage(stats):
	"""What one cast of your own attack is built from: (weapon share, its own flat).

	The weapon share is the attack's "% Weapon Damage" over a hundred, and it is
	how much of the sheet's flat damage the attack actually delivers. A Cadence
	at 150% delivers one and a half times it; Albrecht's Aether Ray delivers
	none of it, because it carries no weapon component at all - its 294 aether
	is its own, and the 1700 on the sheet is what an auto-attack she never makes
	would do.

	That distinction is the whole of what a "pure caster" needs and none of it
	was read. swingPercent already prices a swing this way, as
	sheetFlat * weaponPct/100 + the skill's own flat, so this is the same rule
	applied to the weights rather than a new claim about the game.

	Returns (1.0, {}) when no main attack is named, which is the old behaviour:
	assume everything you deal goes through your weapon.
	"""
	read = mainAttack(stats)
	if not read.named:
		return 1.0, {}
	# a [dps, seconds] pair is a duration effect; its total is what one cast
	# lays down, and dotFactor is not this function's job
	own = {damage: (value[0] * value[1] if isinstance(value, list) else value)
		   for damage, value in read.flat.items()}
	return read.percent / 100.0, own


def applyDefensePriority(stats, weights, priority):
	"""Turn one "how much do I care about surviving" number into every defensive weight.

	Seven or eight hand-written numbers used to say this, and their ratios to
	each other were guesses - what a point of armor is worth against a point of
	health is not a preference, it follows from what you already have, exactly
	the way the flat-versus-percent damage split does. Only the overall scale is
	yours, and that is what `priority` is.

	Everything is priced in effective health: how much more damage you can take
	before dying, per point of the stat. A point of health is one point of that
	by definition, so it is the unit the rest are quoted in.

	    health          1, being the unit
	    armor           what it stops per hit, times the hits you take, times
	                    the share of them that is physical
	    armor absorb    ditto, the percentage half of the same pair
	    resist          health / (100 - your resist), the mirror of
	                    resistReductionValue: the same curve read on your own
	                    resistance instead of the enemy's
	    defense         how much of the enemy's hit chance a point buys off,
	                    against the offensive ability its level and difficulty
	                    give it
	    avoid melee     a straight percentage of hits that never land
	    avoid ranged

	The two that are a pair rather than a single number are armor and armor
	absorb, and they work the way flat and percent damage do. The game says
	damage taken is (protection * (1 - absorption)) + (damage - protection)
	whenever the hit is bigger than your armor, which is damage - armor*absorb:
	a point of armor stops `absorb` of a point, and a point of absorb stops
	`armor/100`. Neither needs to know how hard the enemy hits, which is the
	one thing about the incoming side that is not in the records.
	"""
	notes = []
	if not priority:
		return notes
	health = float(stats.get("health") or 0)
	fight = float(stats.get("fight length") or 30)
	if not health:
		notes.append("defensePriority ignored: no health on the sheet, and every "
					 "defensive weight is quoted per point of effective health")
		return notes

	derived, missing, assumed = {}, [], []
	derived["health"] = 1.0

	# Armor and armor absorb, the flat-and-percent pair, and the only two that
	# need to know anything about the incoming side. "hits/s" is no use here -
	# that is hits you land, which is what drives a hit-triggered proc - so how
	# often you are hit is its own number and defaults to once a second.
	armor = float(stats.get("armor") or 0)
	absorb = float(stats.get("armor absorb") or ARMOR_ABSORB_DEFAULT)
	taken = hitsTaken(stats)
	if not stats.get("hits taken/s"):
		assumed.append("hits taken/s %.2f, from %s standing in a room at the "
					   "default density" % (taken, stats.get("playStyle") or "?"))
	if stats.get("armor absorb") is None:
		assumed.append("armor absorb %g%%" % absorb)
	if armor:
		# Armor stops absorb% of a point per hit, per the game's own
		# physicalDamageDefenseEquationDGP, and it stops it on physical damage
		# only - so what it is worth depends on how much of what hits you is
		# physical, which no record states and PHYSICAL_SHARE is a guess at.
		blows = taken * fight * PHYSICAL_SHARE
		derived["armor"] = absorb / 100.0 * blows
		derived["armor absorb"] = armor / 100.0 * blows
		assumed.append("physical share of incoming %g" % PHYSICAL_SHARE)

	# Resistance, read off your own the way resistReductionValue reads it off
	# the enemy's. Damage taken is (1 - R/100), so a point takes it to
	# (99 - R)/(100 - R) and buys health/(100 - R) of effective health.
	held = [float(stats.get(r) or 0) for r in resists if stats.get(r) is not None]
	if held:
		mean = sum(held) / len(held)
		derived["resist"] = health / (100.0 - mean) if mean < 100 else 0.0
	else:
		missing.append("your resistances, without which 'resist' cannot be priced "
					   "- state them as 'fire resist' and so on")

	# Defensive ability, against what the enemy swings with. A point buys off
	# some of its chance to hit, and the derivative is taken numerically because
	# the game's PTH equation is a blend of two terms and not worth inverting.
	from models import enemyOffense, hitChance, difficultyOf
	level = float(stats.get("level") or 0)
	defense = float(stats.get("defense") or 0)
	if level and defense:
		oa = enemyOffense(level, difficultyOf(_Stats(stats)))
		before, after = hitChance(oa, defense), hitChance(oa, defense + 1.0)
		if before > 0:
			derived["defense"] = health * (before - after) / before
	elif defense:
		missing.append("'level', without which the enemy's offensive ability is unknown")

	# Avoidance is a flat share of hits that never land at all.
	for key in ("avoid melee", "avoid ranged"):
		have = float(stats.get(key) or 0)
		derived[key] = health / (100.0 - have) if have < 100 else 0.0

	for key, perPoint in sorted(derived.items()):
		if key in weights:
			continue        # explicit weight wins, as everywhere else
		weights[key] = priority * perPoint
	notes.append("defensePriority %g -> %s"
				 % (priority, ", ".join("%s %.3g" % (k, weights.get(k, 0))
										for k, _ in sorted(derived.items()))))
	for gap in missing:
		notes.append("defensePriority: nothing derived for %s" % gap)
	if assumed:
		notes.append("defensePriority assumed %s - none of it is on the sheet"
					 % ", ".join(assumed))
	return notes


class _Stats(object):
	"""Just enough of a Model for difficultyOf, which takes one."""

	def __init__(self, stats):
		self.stats = stats

	def getStat(self, key):
		return self.stats.get(key, 0)


def fromRotation(stats, weights, priority):
	"""Every damage weight from what the rotation actually deals.

	    damagePriority = {"rotation": 30}
	    damagePriority = {"rotation": 30, "fire": 1.5}

	The number beside "rotation" is what the largest damage weight should come
	out at, so it lands in the same range as the hand-written ones it replaces
	and nothing else in the model has to be rescaled. A damage type named
	alongside it is a lean - a multiplier on what the rotation says, for when
	you want to push a build somewhere it is not already.

	This is the last of the guessing to go. A priority was a preference, and
	the honest answer to "how much do I care about fire" is "as much fire as I
	deal", which the rotation and the skill records know between them. gwyr had
	physical at 5 and pierce at 5 while dealing 0.9% physical and 8.1% pierce.

	What it cannot see is a type you deal none of yet and want to build into.
	That is what the lean is for, and it is a real preference rather than a
	number standing in for arithmetic nobody did.
	"""
	notes = []
	rows = rotationDamage(stats)
	if not rows:
		notes.append("damagePriority asked for %r, but the rotation is bare numbers - "
					 "name the skills and their ranks and it can read them" % ROTATION)
		return notes
	scale = float(priority.get(ROTATION) or 0) or 1.0
	lean = {k: float(v) for k, v in priority.items() if k != ROTATION}

	# Retaliation is another source of damage per second, so it is priced on
	# the same scale rather than by hand beside it. That balance - what he
	# deals by swinging against what he deals by being hit - was the thing
	# nobody could set honestly, because the two halves were in different
	# units. They are in the same one now: damage a second, per point.
	retal, retalPercent = retaliationDamage(stats)

	# Everything is quoted against the biggest, so "rotation": 30 means "my
	# largest weight should be about 30" rather than asking anyone to guess at
	# units of damage per second.
	peak = max([max(dFlat, dPerc) * lean.get(d, 1.0)
				for d, (_, dFlat, dPerc) in rows.items()]
			   + [dFlat * lean.get(d, 1.0) for d, (_, dFlat) in retal.items()]
			   + [retalPercent]) or 1.0
	rate = float(stats.get("attacks/s") or 0)
	total = sum(perSecond for perSecond, _, _ in rows.values()) or 1.0
	swing, shares = 0.0, []
	for damage, (perSecond, dFlat, dPerc) in rows.items():
		factor = dotFactor(damage, stats) * lean.get(damage, 1.0) * scale / peak
		landed = dFlat * lean.get(damage, 1.0) * scale / peak
		for key, amount in ((damage, dFlat * factor),
							(damage + " %", dPerc * factor),
							# a proc's damage is not refreshed by your swinging,
							# so it keeps the undiscounted value, over attacks/s
							# because it lands once where a point on the sheet
							# lands on every swing
							("triggered " + damage, landed / (rate or 1.0))):
			if key not in weights:
				weights[key] = amount
		swing += float(stats.get(damage, 0) or 0) * dFlat * factor
		if perSecond > total * 0.005:
			shares.append("%s %.0f%%" % (damage, 100 * perSecond / total))
	if swing and "weapon damage %" not in weights:
		weights["weapon damage %"] = swing / 100.0 / (rate or 1.0)

	retalTotal = sum(perSecond for perSecond, _ in retal.values())
	for damage, (_, dFlat) in retal.items():
		key = damage + " retaliation"
		if key not in weights:
			weights[key] = dFlat * lean.get(damage, 1.0) * scale / peak
	if retalPercent and "retaliation %" not in weights:
		weights["retaliation %"] = retalPercent * scale / peak

	notes.append("damage weights from the rotation, which deals: " + ", ".join(shares))
	if retalTotal:
		notes.append("retaliation is %.0f%% of what he deals - %.0f a second against "
					 "%.0f from the rotation, at %.2f hits taken a second"
					 % (100 * retalTotal / (total + retalTotal), retalTotal, total,
						hitsTaken(stats)))
	if lean:
		notes.append("leaning on " + ", ".join("%s x%g" % (k, v) for k, v in sorted(lean.items())))
	return notes


def applyDamagePriority(stats, weights, priority, attributeBonus=None):
	"""Split one priority per damage type into flat and % weights using the sheet.

	How much a point of a damage type is worth is not a preference - it follows
	from what you already have. Roughly, damage of type X is
	(flat + weaponBase) * (1 + X%/100), so:

	    +1 flat X  is worth  (1 + X%/100)
	    +1% X      is worth  (flat / 100)

	With 69 flat lightning and 850% lightning, a point of flat is ~14x the value
	of a point of %. With no flat physical at all, physical % multiplies nothing
	and is worth zero. Hand-written weights tend to set the two equal, which
	quietly misprices exactly the types you invest in least.

	The priority you supply stays a pure preference ("pierce matters more than
	cold"). Anything already named explicitly in `weights` wins, so you can
	always pin a value you disagree with.

	One key is not a damage type: "damage" is the priority for every type you
	did not name, and it is the only place a catch-all belongs. It used to be a
	weight of its own, evaluated somewhere else entirely and against a different
	divisor, which meant the same number meant two things depending on which
	half of the model you wrote it in - lochlan's read as 60.8 next to
	priorities of 8.25 to 27.5. Here it is a priority like any other and is
	compared with the ones above it by reading them.

	Duration damage is discounted by dotFactor, the same for a type you named
	and a type the catch-all reached. It used to be halved for one and left
	alone for the other, which made "bleed 5" mean two different things
	depending on whether bleed was written down.

	The scaling factor is one number for the whole block, not one per type, and
	that is the difference between a weight meaning something and not. Per type
	it was (vFlat + vPerc) / 2 for that type, which held weight(X) + weight(X %)
	to exactly twice the priority - tidy, and wrong across types, because a type
	you hold a lot of flat damage in has a large vPerc and so a large divisor.
	lochlan puts lightning at 27.5 against physical's 8.25 and a point of flat
	lightning delivers 12.38 damage against physical's 9.00, and it came out
	lightning 10.92, physical 14.14: lower on the type he cares about more and
	that hits harder, because his 5000 flat lightning drove that divisor to
	31.19 against physical's 5.25.

	Shared, the divisor cancels out of every comparison and what is left is
	priority * value-per-point, which is what a weight is for. Totals are no
	longer held per type - a type carrying most of its value in the percentage
	draws more of the block than one that does not, which is the honest answer
	and the reason the tidy property had to go.

	attributeBonus is the percentage cunning and spirit add, which the sheet
	does not show and checkModel folds in later - later than this, which is the
	point of passing it. Reading morena's pierce as the 275 on her sheet rather
	than the 551 she actually has valued a point of flat pierce at 3.75 times
	its damage instead of 6.51, and correspondingly overvalued a point of
	percentage. Both halves of the split were wrong and in opposite directions.
	"""
	attributeBonus = attributeBonus or {}
	notes = []
	priority = dict(priority)
	if ROTATION in priority:
		return fromRotation(stats, weights, priority)
	catchAll = priority.pop(CATCH_ALL, None)
	if catchAll is None and priority:
		# Standard rather than opt-in, because leaving it out never meant what
		# it looked like. It looked like "I have not thought about poison"; it
		# scored as "poison is worth exactly nothing", and a devotion offering
		# a type you did not name read as offering nothing at all. Nobody
		# builds a character who would rather have no acid damage than some.
		#
		# Half the least thing you did name: below all of them, because not
		# naming a type says at least that much, and not zero, because a bit of
		# damage is a bit of damage. It is the one number here that is a
		# judgement rather than a reading, so it is stated in the notes every
		# run and overridden by writing "damage" in the block yourself.
		catchAll = min(priority.values()) / 2.0
		notes.append("%s not set, so it defaults to %g - half the lowest priority "
					 "named. Without it every type you did not name is worth "
					 "nothing at all; set it in the block to say otherwise"
					 % (CATCH_ALL, catchAll))

	# How much of the sheet's flat damage your own attack actually delivers, and
	# what it brings of its own. A weapon build is 1.0 and nothing, which is
	# what every model assumed before anything could say otherwise.
	share, own = mainAttackDamage(stats)

	def value(damage):
		"""(flat, perc, what a point of flat is worth when it lands, ditto a percent).

		"When it lands" is the distinction the share makes. A point of flat X on
		your gear is worth 1 + X%/100 to anything that delivers it - a proc's
		weapon damage, an auto-attack - but your own attack delivers only its
		weapon share of it, which for a spell carrying no weapon component is
		none. So the landed value is what a proc is priced against and the
		shared one is what gear flat is worth to you, and they are not the same
		number for a caster.

		A percent multiplies everything of that type one cast lands: the share
		of the sheet it delivers, plus whatever the cast brings of its own.
		"""
		flat = stats.get(damage, 0)
		perc = stats.get(damage + " %", 0) + attributeBonus.get(damage, 0)
		return (flat, perc, 1.0 + perc / 100.0,
				(share * flat + own.get(damage, 0)) / 100.0)

	# The mean of what the per-type divisors used to be, over the types named
	# outright, so a block whose types agree on their split lands where it
	# always did and only one that disagrees moves. A block that names nothing
	# but the catch-all has no split to reconcile and divides by one, which is
	# exactly what a bare "damage" weight used to do.
	#
	# A type contributing nothing at all is left out rather than averaged in as
	# a zero: hela carries 250% vitality and no vitality damage from any source,
	# and counting that as a divisor of nothing would scale the whole block by
	# how many such types happened to be listed.
	named = [d for d in priority
			 if (stats.get(d) or stats.get(d + " %") or attributeBonus.get(d))
			 and (value(d)[2] or value(d)[3])]
	norm = (sum((value(d)[2] + value(d)[3]) / 2.0 for d in named) / len(named)
			if named else 1.0)

	swing = 0.0     # what one full weapon swing is worth, for weapon damage %
	for damage in damages:
		# aggregates rather than types you can be dealt, priced from their parts
		if damage in ("elemental", "all damage"):
			continue
		if damage in priority:
			p = priority[damage]
		elif catchAll is not None:
			p = catchAll
		else:
			continue
		factor = dotFactor(damage, stats)
		flat, perc, landed, vPerc = value(damage)
		# what a point of gear flat is worth to you, as opposed to when it lands
		vFlat = share * landed
		# "triggered X" is priced per point of damage actually delivered, and
		# calculateBonus has already taken a proc's [dps, seconds] down to what
		# one application lands - min(duration, interval), the very thing
		# dotFactor measures. So the triggered weight is the undiscounted one,
		# or a proc's bleed would be discounted for refreshing twice. What it
		# does carry is the division by attacks/s, because a proc lands once
		# where a point on the sheet lands on every swing.
		#
		# And it is priced off the landed value rather than the shared one. A
		# proc's damage is the proc's, not your weapon's - hela's beam carries
		# no weapon component, so her gear's flat aether is worth nothing to
		# her, but a devotion that deals aether still deals it.
		rate = float(stats.get("attacks/s") or 0)
		triggered = p * landed / norm / (rate or 1.0)
		swing += stats.get(damage, 0) * p * landed * factor / norm
		for key, amount in ((damage, p * vFlat * factor / norm),
							(damage + " %", p * vPerc * factor / norm),
							("triggered " + damage, triggered)):
			if key in weights:
				continue # explicit weight wins
			# unrounded: the notes below round for reading, but a weight that
			# has been rounded to three places is a weight that has been
			# changed, and these feed bareSwing and every damage comparison
			weights[key] = amount
		if damage not in priority:
			continue        # reported in one line below, not thirty
		bonus = attributeBonus.get(damage, 0)
		notes.append("%s priority %g -> %s %g, %s %% %g  (%g flat, %g%%%s)"
					 % (damage, p, damage, weights.get(damage, 0),
						damage, weights.get(damage + " %", 0), flat, perc,
						" incl %g from attributes" % round(bonus) if bonus else ""))

	# A proc's "% Weapon Damage" swings your weapon, whatever your own attack
	# does, so it is priced off the landed value too - the same sum checkModel
	# used to build out of the weights above, but before the share is applied.
	# Those are zero for a caster, which would have said a weapon-damage proc
	# is worth nothing to her when it is the one thing that does put her gear's
	# flat damage to work.
	rate = float(stats.get("attacks/s") or 0)
	if swing and "weapon damage %" not in weights:
		weights["weapon damage %"] = swing / 100.0 / (rate or 1.0)

	unnamed = [d for d in damages if d not in priority
			   and d not in ("elemental", "all damage")]
	if catchAll is not None and unnamed:
		bands = {}
		for d in unnamed:
			bands.setdefault(round(weights.get(d, 0), 3), []).append(d)
		notes.append("%s priority %g -> everything not named above, at what a point "
					 "of each delivers: %s"
					 % (CATCH_ALL, catchAll,
						"; ".join("%g for %s" % (w, ", ".join(sorted(names)))
								  for w, names in sorted(bands.items(), reverse=True))))
	for damage in priority:
		if damage not in named:
			notes.append("%s has nothing on the sheet, so its priority buys flat %s only "
						 "- there is no percentage of nothing to be worth anything"
						 % (damage, damage))
	return notes


def bonusVocabulary():
	"""Every weight name the optimiser can score against."""
	vocab = set()
	for c in Constellation.constellations:
		for s in c.stars:
			vocab.update(s.bonuses)
			if s.ability:
				vocab.update(s.ability.bonuses)
				vocab.add(s.ability.name)
				for v in s.ability.bonuses.values():
					if isinstance(v, dict):
						vocab.update(v)
	# names checkModel derives, or expands from shorthand
	vocab.update({"resist", "pet resist", "damage", "pet damage", "triggered damage",
				  "retaliation", "pet retaliation", "attack opportunity cost",
				  "all damage %", "pet all damage %", "crit damage", "total speed",
				  "elemental", "triggered elemental", "elemental %", "elemental resist",
				  "reduce resist", "reduce elemental resist"})
	for d in damages:
		vocab.update({d, d + " %", "pet " + d, "pet " + d + " %", "triggered " + d,
					  d + " retaliation", "pet " + d + " retaliation",
					  "reduce " + d + " resist", "reduce " + d + " resist %",
					  d + " duration"})
	vocab.update({"reduce resist %", "reduce elemental resist %"})
	# 34 items carry one of these and nothing scored them, so a conversion read
	# as a free bonus - and it is not free, it is a trade. checkModel derives a
	# weight for each from the sheet, which is why they belong here rather than
	# being a preference anyone has to state.
	vocab.update(conversions())
	for r in resists:
		vocab.update({r, "pet " + r, "max " + r, "pet max " + r, "reduce " + r})
	return vocab


def statVocabulary():
	"""Character-sheet names a stats dict may legitimately carry."""
	vocab = set(CONTROL_STATS)
	vocab.update({"physique", "cunning", "spirit", "offense", "defense", "health",
				  "health/s", "energy", "energy/s", "armor", "armor absorb",
				  "armor piercing", "attack speed", "cast speed", "move speed",
				  "block %", "blocked damage %", "damage absorb %", "lifesteal %",
				  "weapon damage %", "crit damage", "retaliation %", "pet damage %",
				  # What you deal by being hit. The flat figures are per type,
				  # the percentage is one number for all of them - the game's
				  # own tooltip says "% All Damage does not affect Retaliation
				  # damage", so retaliation has its own multiplier and this is
				  # it. Both spellings, since the sheet says one and the weight
				  # vocabulary has long said the other.
				  "all retaliation %",
				  "avoid melee", "avoid ranged", "elemental %", "elemental resist",
				  "all damage %", "physical resist",
				  # % Reduced Skill Cooldown off the sheet. Ability.resolveTiming
				  # takes it off every cooldown - item skills and devotion procs
				  # alike - and it was not readable before.
				  "reduce cooldown",
				  # weapon damage of the attack you actually swing with, which is
				  # what a granted skill interrupts and has to beat, and how many
				  # enemies that swing reaches, since giving it up costs all of
				  # them. Both derive from the held attack resolveRotation picks
				  # out; state one only for an attack the skill data cannot
				  # describe. "main attack" itself is derived and lives here
				  # because it ends up in stats, not because a model may write it.
				  "main attack %", "main attack", "main attack targets",
				  # energy a second a granted skill may spend, when regeneration
				  # is not the story - a leech build sustains on something the
				  # sheet's regen figure does not show
				  "energy for skills/s"})
	for d in damages:
		vocab.update({d, d + " %", d + " duration", d + " retaliation"})
	for r in resists:
		vocab.update({r, "max " + r})
	for d in primaryDamages:
		vocab.add("reduce " + d + " resist")
		vocab.add("enemy " + d + " resist")   # what the enemy resists, not what you reduce
	vocab.add("enemy resist")
	# checkModel reads a "<stat> %" form for anything with a percentage modifier
	# (via bonusToPercent / processMetaStats), so those are legitimate sheet values
	for stat in ("physique", "cunning", "spirit", "health", "health/s", "energy",
				 "energy/s", "armor", "offense", "defense", "blocked damage"):
		vocab.add(stat + " %")
	return vocab


# A proc's trigger names the rate it fires at, and Ability.calculateTriggerTime
# reads that rate straight off the sheet. A rate of zero is not a small number,
# it is an early return that scores the whole proc at nothing - so a sheet that
# omits one silently deletes every proc hanging off it. trigger -> the ways the
# sheet can supply its rate, and how to say it in the warning. Each way is a
# group of keys that all have to be present, and any one group is enough.
TRIGGER_RATES = {
	"attack": ((("attacks/s",),), "set 'attacks/s'"),
	"hit": ((("hits/s",),), "set 'hits/s'"),
	# checkModel derives criticals/s from crit chance, and crit chance itself
	# from offensive ability against a stated enemy defense - which needs both,
	# so naming the enemy without an offense to swing at it is not enough
	"critical": ((("crit chance",), ("offense", "enemy defense"), ("offense", "level")),
				 "set 'level' (or 'enemy defense' outright) alongside 'offense' "
				 "to derive it, or pin 'crit chance'"),
	"block": ((("blocks/s",),), "set 'blocks/s'"),
	"kill": ((("kills/s",),), "set 'kills/s'"),
	"low health": ((("low healths/s",),), "set 'low healths/s'"),
}


def unratedTriggers(stats):
	"""Triggers this sheet gives no rate for, as warnings naming what each costs.

	Call this after filterConstellations, so it only counts procs the character
	could actually have taken - a two-hander should not be told what its missing
	block rate costs it in shield constellations it was never offered.

	Not fatal. A build with no crit and no block genuinely fires none of those,
	and saying so is the point: morena weights crit damage at 10 while carrying
	no crit chance, which reads as a crit build but scores all nine
	crit-triggered procs at zero.
	"""
	# by identity: buildAbilityFragments registers a part-way prefix as its own
	# constellation sharing the same Ability object, so walking constellations
	# alone reports one proc twice
	counts, seen = {}, set()
	for c in Constellation.constellations:
		for star in c.stars:
			trigger = star.ability.gc("trigger") if star.ability else None
			if trigger in TRIGGER_RATES and id(star.ability) not in seen:
				seen.add(id(star.ability))
				counts[trigger] = counts.get(trigger, 0) + 1
	out = []
	for trigger, procs in sorted(counts.items()):
		groups, hint = TRIGGER_RATES[trigger]
		# A stated zero is an answer, not a gap. fenris does not block, and
		# saying "blocks/s": 0 used to be indistinguishable from not having
		# thought about it - the test was truthiness, so the model got told to
		# set a key it had already set. The procs still score zero either way;
		# what changes is whether that is news.
		if any(all(key in stats for key in group) for group in groups):
			continue
		if not any(all(stats.get(key) for key in group) for group in groups):
			out.append("nothing gives %s-triggered procs a rate, so all %d of them "
					   "score 0 - %s" % (trigger, procs, hint))
	return out


# Names that are real things in Grim Dawn but that no weight can ever be paid
# for, with the reason. Without this they read as typos: the validator said
# "unknown weight 'damage reflect %'" in the same breath it says it for
# 'aether reist', and offered 'burn duration' for 'stun duration', which is a
# confident wrong answer to a question with a real one.
#
# Every entry here has been checked against the database rather than assumed.
UNSCORED = {
	"damage reflect %":
		"real, and gddata reads it from defensiveReflect - but of 25867 item "
		"records only two carry that field and both are loot affixes, no "
		"devotion carries it at all, and skillgen does not emit it for Blade "
		"Barrier. Nothing you can pick grants it, so a weight cannot be spent",
	"stun duration":
		"the game has no separate field for it - offensiveStunModifier is the "
		"stun duration modifier and is already the weight called 'stun %'",
}


def _suggest(key, vocab):
	# 0.80 catches real typos ('peirce', 'aether reist', 'physiacl resist'). Keys
	# that are unsupported rather than misspelt are answered by UNSCORED above
	# and never reach here, which is what stops a confident wrong suggestion.
	close = difflib.get_close_matches(key, sorted(vocab), n=1, cutoff=0.80)
	return "  (did you mean %r?)" % close[0] if close else ""


def validate(name, points, stats, weights, priority=None):
	"""Raise on anything unrecoverable; warn about anything suspicious."""
	problems = []
	if not isinstance(points, (int, float)) or points <= 0:
		problems.append("%s must be a positive number (got %r)" % (REQUIRED_POINTS, points))
	for key, why in REQUIRED_STATS.items():
		if key not in stats:
			problems.append("stats is missing %r - %s" % (key, why))
	if stats.get("playStyle") not in PLAY_STYLES and "playStyle" in stats:
		problems.append("stats['playStyle'] is %r; expected one of %s"
						% (stats["playStyle"], ", ".join(PLAY_STYLES)))
	if "difficulty" in stats:
		# A name nobody recognises used to fall through to the default, which
		# reads a different column of the game's scaling table - wrong enemy
		# defence and wrong resistances, silently. Loud is better.
		from models import DIFFICULTIES, DIFFICULTY_ALIAS
		known = set(DIFFICULTIES) | set(DIFFICULTY_ALIAS)
		if str(stats["difficulty"]).lower() not in known:
			problems.append("stats['difficulty'] is %r; expected one of %s%s"
							% (stats["difficulty"], ", ".join(sorted(known)),
							   _suggest(str(stats["difficulty"]).lower(), known)))
	if not weights and not priority:
		problems.append("weights is empty, so every constellation scores 0")
	for key in (priority or {}):
		if key in (CATCH_ALL, ROTATION):
			continue        # the two keys that are not damage types
		if key not in damages:
			problems.append("damagePriority key %r is not a damage type%s"
							% (key, _suggest(key, damages)))
	if problems:
		raise ValueError("%s model is not usable:\n    %s"
						 % (name, "\n    ".join(problems)))

	warnings = []
	bonusVocab, statVocab = bonusVocabulary(), statVocabulary()
	for key in weights:
		if key in UNSCORED:
			warnings.append("weight %r cannot score: %s" % (key, UNSCORED[key]))
		elif key not in bonusVocab:
			warnings.append("unknown weight %r - nothing scores against it%s"
							% (key, _suggest(key, bonusVocab)))
	for key in stats:
		if key not in statVocab:
			warnings.append("unknown stat %r - it is never read%s"
							% (key, _suggest(key, statVocab)))
	return warnings


TEMPLATE = '''\
# %(name)s - devotion model.
#
# stats   = your character sheet, as the game reports it.
# weights = how much a point of each stat is worth to you. Relative values are
#           all that matter; scale is arbitrary. Start rough and refine.
#
# Only attacks/s and playStyle are required. Everything else is optional -
# add sheet numbers as you care about them. Unknown keys are reported on load.

# python %(folder)s/%(folder)s.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))

devotionPoints = %(points)d

stats = {
	"attacks/s": 2.0,            # Attack Speed off the sheet: how fast you swing
	"playStyle": "%(style)s",%(styles)s

	# Your skill bar, in the order you would describe it. Name the skill and its
	# rank and the rate comes from the game's own cooldown; add a third number
	# where you press it slower than it recharges, because a short cooldown is
	# not always worth spamming. An item skill has no rank, so its second number
	# is the press interval. Plain rates still work for anything unnameable.
	#
	# The first entry is the attack you hold the button down on, and it runs at
	# attacks/s above. Passives, toggles and secondary attacks are not presses -
	# the records say so - and each goes inside the entry for the skill it
	# modifies, which is the only thing it can modify.
	# "rotation": [("Fire Strike", 12, [("Explosive Strike", 12)]),  # held, + a
	#                                            # modifier on it, not a button
	#              ("Mortar Trap", 12, 15.0),    # pressed every 15s
	#              ("Leap", 12, [("Fault Line", 8)]),  # cooldown, + a modifier
	#              ("Sacred Strike", 1.5),       # off an item, pressed every 1.5s
	#              0.5],

	# Pressing a skill an item grants costs you one swing of the above, and a
	# skill only earns its place by beating it. Derived from the rotation; set
	# this only for an attack the skill data does not describe.
	# "main attack %%": 100,

	# Your level, and what you fight. Crit chance is derived from your offensive
	# ability against the enemy's defensive one using the game's own hit
	# formula, and enemy defence is derived from level - so stating "level" is
	# usually enough, and without it every crit-triggered proc scores zero.
	# Override "enemy defense" directly if you grind a difficulty whose scaling
	# the game's records do not carry. "enemy density" is enemies per square
	# metre and sizes every area proc.
	# "level": 100,
	# "difficulty": "ultimate",     # normal | elite | ultimate
	# "enemy defense": 1400,        # overrides what level+difficulty derive
	# "enemy resist": 25,           # ditto, for every damage type at once
	# "enemy density": 0.03,

	# "weapons": ["sword", "shield"],   # omit to allow every constellation
	# "physique": 0, "cunning": 0, "spirit": 0,
	# "offense": 0, "defense": 0,
	# "health": 0, "health/s": 0, "armor": 0,
	# "fight length": 30,

	# Flat and %% damage for the types you care about. damagePriority below
	# uses these to work out what a point of each is actually worth.
	# "pierce": 350, "pierce %%": 200,
}

# One number per damage type saying how much you care about it. The flat vs %%
# split is derived from the sheet above: with 69 flat lightning and 850%%
# lightning, a flat point is worth ~14x a percentage point, and with no flat
# physical at all, "physical %%" multiplies nothing. You should not have to work
# that out by hand, and hand-written weights usually get it wrong.
damagePriority = {
%(priority)s}

# Everything else - defence, speed, utility. Anything named here also overrides
# whatever damagePriority would have derived.
weights = {
%(weights)s}
'''

# Rough starting points. These are opinions, not truths - tune them.
# archetype: (damagePriority lines, weights lines)
ARCHETYPES = {
	"physical": (['\t"physical": 10,', '\t"pierce": 5,'],
				 ['\t"offense": 5, "attack speed": 10,',
				  '\t"weapon damage %%": 7.5,']),
	"bleed":    (['\t"bleed": 15,', '\t"physical": 5,'],
				 ['\t"bleed duration": 5,',
				  '\t"offense": 5, "attack speed": 10,']),
	"fire":     (['\t"fire": 15,', '\t"burn": 7.5,'],
				 ['\t"burn duration": 5,', '\t"cast speed": 10,']),
	"tank":     (['\t"physical": 5,'],
				 ['\t"armor": 5, "armor absorb": 20,',
				  '\t"health": 0.66, "defense": 7.5,',
				  '\t"resist": 15, "physical resist": 35,',
				  '\t"block %%": 100, "blocked damage %%": 40,']),
	"pet":      ([],
				 ['\t"pet all damage %%": 10,', '\t"pet resist": 10,',
				  '\t"health": 0.5, "defense": 5,']),
}


def scaffold(name, archetype="physical", points=55, style="melee", force=False):
	"""Write <name>/<name>.py from the template. Returns the path written."""
	folder = name.lower()
	path = os.path.join(folder, folder + ".py")
	if os.path.exists(path) and not force:
		raise ValueError("%s already exists; pass force=True to overwrite" % path)
	if archetype not in ARCHETYPES:
		raise ValueError("unknown archetype %r; try one of: %s"
						 % (archetype, ", ".join(sorted(ARCHETYPES))))
	os.makedirs(folder, exist_ok=True)
	priorityLines, weightLines = ARCHETYPES[archetype]
	text = TEMPLATE % {
		"name": name,
		"folder": folder,
		"points": points,
		"style": style,
		"styles": "        # melee | shortranged | ranged | tank",
		"priority": ("\n".join(priorityLines) % () + "\n") if priorityLines else "",
		"weights": "\n".join(weightLines) % () + "\n",
	}
	with open(path, "w") as handle:
		handle.write(text)
	return path
