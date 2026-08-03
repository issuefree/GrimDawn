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

REQUIRED_POINTS = "devotionPoints"
REQUIRED_STATS = {
	"attacks/s": "attacks per second, used to scale everything trigger-based",
	"playStyle": "one of: melee, shortranged, ranged, tank",
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
		notes.append("allAttacks/s defaulted to [attacks/s]; list your individual "
					 "attack sources for a better estimate")
	if "weapons" not in stats:
		stats["weapons"] = weaponTypes()
		notes.append("weapons defaulted to all types (no constellation excluded)")
	if "blacklist" not in stats:
		stats["blacklist"] = []
	return notes


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
	stated = stats.get("main attack")
	if not stated:
		return 1.0, {}
	if isinstance(stated[0], str):
		stated = [stated]
	import skillData                       # noqa: F401 - registers the skills
	from models import Skill
	share, own = 0.0, {}
	for name, level in stated:
		skill = Skill.skills.get(name)
		if skill is None:
			continue                        # checkModel warns about this by name
		ability = skill.getAbility(level)
		share += ability.gb("weapon damage %") / 100.0
		for bonus, amount in ability.bonuses.items():
			# skillgen names an attack's own damage "triggered X" and a buff's
			# plain "X" - the same damage either way, so the prefix comes off.
			# Feral Claws states its 117 pierce as "triggered pierce", and
			# fenris carries 200% pierce with no flat pierce on his sheet
			# precisely because that 117 is where his pierce comes from.
			name = bonus[len("triggered "):] if bonus.startswith("triggered ") else bonus
			if name in damages:
				# a [dps, seconds] pair is a duration effect; its total is what
				# one cast lays down, and dotFactor is not this function's job
				amount = amount[0] * amount[1] if isinstance(amount, list) else amount
				own[name] = own.get(name, 0) + amount
	return share, own


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
				  "avoid melee", "avoid ranged", "elemental %", "elemental resist",
				  "all damage %", "physical resist",
				  # % Reduced Skill Cooldown off the sheet. Ability.resolveTiming
				  # takes it off every cooldown - item skills and devotion procs
				  # alike - and it was not readable before.
				  "reduce cooldown",
				  # weapon damage of the attack you actually swing with, which is
				  # what a granted skill interrupts and has to beat. Name the
				  # skill as ("Cadence", 12) and the percentage is looked up.
				  # and how many enemies that swing reaches, since giving it up
				  # costs all of them. Derived from the named skill's geometry;
				  # set this only for an attack the skill data does not describe.
				  "main attack %", "main attack", "main attack targets",
				  # energy a second a granted skill may spend, when regeneration
				  # is not the story - a leech build sustains on something the
				  # sheet's regen figure does not show
				  "energy for skills/s"})
	for d in damages:
		vocab.update({d, d + " %", d + " duration"})
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
		if key == CATCH_ALL:
			continue        # the one key that names every type rather than one
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
	"attacks/s": 2.0,            # attacks per second, as swung in practice
	"playStyle": "%(style)s",%(styles)s

	# Break out each trigger source for a better estimate of stacked procs.
	# "allAttacks/s": [2.0, 1.0, 0.5],

	# What the first of those swings for. Pressing a skill an item grants costs
	# you one of these, and a skill only earns its place by beating it - leave
	# it out and every component skill is measured against a bare 100%% swing.
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
