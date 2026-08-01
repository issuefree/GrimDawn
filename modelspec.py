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
from constants import damages, resists, primaryDamages

# Must be supplied; there is no defensible default for these.
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


def applyDamagePriority(stats, weights, priority):
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
	cold"), and is preserved in total: weight(X) + weight(X %) == 2 * priority.
	Anything already named explicitly in `weights` wins, so you can always pin a
	value you disagree with.
	"""
	notes = []
	for damage, value in sorted(priority.items()):
		flat, perc = stats.get(damage, 0), stats.get(damage + " %", 0)
		if not flat and not perc:
			# Nothing on the sheet to reason from. Splitting here would just
			# invent a ratio, so leave it to an explicit weight.
			notes.append("%s priority ignored: no %s on the sheet, so flat vs %% "
						 "cannot be inferred - set both weights explicitly" % (damage, damage))
			continue
		vFlat = 1.0 + perc / 100.0   # value of +1 flat point
		vPerc = flat / 100.0         # value of +1 percentage point
		norm = (vFlat + vPerc) / 2.0
		derived = {damage: value * vFlat / norm, damage + " %": value * vPerc / norm}
		for key, amount in derived.items():
			if key in weights:
				continue # explicit weight wins
			weights[key] = round(amount, 3)
		notes.append("%s priority %g -> %s %g, %s %% %g  (sheet: %g flat, %g%%)"
					 % (damage, value, damage, weights.get(damage, 0),
						damage, weights.get(damage + " %", 0), flat, perc))
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
					  "reduce " + d + " resist", d + " duration"})
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
				  "all damage %", "physical resist"})
	for d in damages:
		vocab.update({d, d + " %", d + " duration"})
	for r in resists:
		vocab.update({r, "max " + r})
	for d in primaryDamages:
		vocab.add("reduce " + d + " resist")
	# checkModel reads a "<stat> %" form for anything with a percentage modifier
	# (via bonusToPercent / processMetaStats), so those are legitimate sheet values
	for stat in ("physique", "cunning", "spirit", "health", "health/s", "energy",
				 "energy/s", "armor", "offense", "defense", "blocked damage"):
		vocab.add(stat + " %")
	return vocab


def _suggest(key, vocab):
	# 0.80 catches real typos ('peirce', 'aether reist', 'physiacl resist') while
	# staying quiet on keys that are simply unsupported ('damage reflect %'),
	# where a confident-looking wrong suggestion would be worse than none.
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
	if not weights and not priority:
		problems.append("weights is empty, so every constellation scores 0")
	for key in (priority or {}):
		if key not in damages:
			problems.append("damagePriority key %r is not a damage type%s"
							% (key, _suggest(key, damages)))
	if problems:
		raise ValueError("%s model is not usable:\n    %s"
						 % (name, "\n    ".join(problems)))

	warnings = []
	bonusVocab, statVocab = bonusVocabulary(), statVocabulary()
	for key in weights:
		if key not in bonusVocab:
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

devotionPoints = %(points)d

stats = {
	"attacks/s": 2.0,            # attacks per second, as swung in practice
	"playStyle": "%(style)s",%(styles)s

	# Break out each trigger source for a better estimate of stacked procs.
	# "allAttacks/s": [2.0, 1.0, 0.5],

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
		"points": points,
		"style": style,
		"styles": "        # melee | shortranged | ranged | tank",
		"priority": ("\n".join(priorityLines) % () + "\n") if priorityLines else "",
		"weights": "\n".join(weightLines) % () + "\n",
	}
	with open(path, "w") as handle:
		handle.write(text)
	return path
