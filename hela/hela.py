# Hela - devotion model.
#
# stats   = your character sheet, as the game reports it.
# weights = how much a point of each stat is worth to you. Relative values are
#           all that matter; scale is arbitrary. Start rough and refine.
#
# Only attacks/s and playStyle are required. Everything else is optional -
# add sheet numbers as you care about them. Unknown keys are reported on load.

# python hela/hela.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))

devotionPoints = 22

stats = {
	"attacks/s": 2.0,            # attacks per second, as swung in practice
	"playStyle": "ranged",        # melee | shortranged | ranged | tank

	# Rates the procs are scored against. attacks/s above covers 14 attack
	# triggers; these three are unset, so the 3 block-triggered, 14
	# hit-triggered and 2 low-health-triggered procs in the game all score
	# zero - a third of everything the optimiser could offer her.
	# "hits/s": 2, "blocks/s": 0, "low healths/s": 1.0/30,

	# Break out each trigger source for a better estimate of stacked procs;
	# without it this is just [attacks/s] and stacked procs read optimistic.
	# "allAttacks/s": [2.0, 1.0, 0.5],

	# What the first of those swings for. Pressing a skill an item grants costs
	# you one of these, and a skill only earns its place by beating it - leave
	# it out and every component skill is measured against a bare 100% swing.
	# "main attack %": 100,

	"level": 58,
	"difficulty": "normal",       # from the level band, not from the save

	# omitted, and each has a live default: "weapons" allows every
	# constellation, "enemy density" sizes area procs at 0.03 enemies a square
	# metre, "fight length" is 30 seconds, and "enemy defense" comes from level
	# and difficulty above - 674 here, which puts crit at 17.1%.

	"physique": 582, "cunning": 380, "spirit": 1053,
	"offense": 1450, "defense": 1295,
	"health": 9500, "health/s": 50, 
	"energy": 5200, "energy/s": 165,
	"armor": 512,

	# Flat and % damage for the types you care about. damagePriority below
	# uses these to work out what a point of each is actually worth.
	# vitality is 0 flat, so its percentage multiplies nothing and is priced at
	# nothing - that is not a mistake in the sheet, it is what 250% of no
	# vitality damage is worth.
	"aether": 1700, "aether %": 1200,
	"lightning": 500, "lightning %": 750,
	"vitality": 0, "vitality %": 250,
	"fire": 250, "fire %": 550,

}

# One number per damage type saying how much you care about it. The flat vs %
# split is derived from the sheet above, and so is every damage weight in the
# model - this is the only place a damage number belongs.
#
# There is no "damage" key here, and that is a decision rather than an
# omission: it is the priority for every type not named, and without it acid,
# chaos, bleed, pierce, physical, cold and the rest are worth exactly nothing,
# so a devotion offering them reads as offering nothing at all. Add
# "damage": 1 or so if a bit of off-type damage is still worth a bit.
damagePriority = {
	"aether": 10,
	"lightning": 5,
	"vitality": 2.5,
	"fire": 2.5,
}

# Everything that is not damage - defence, speed, utility. Anything named here
# also overrides whatever damagePriority would have derived, so an entry is a
# statement that you disagree with the sheet.
#
# "weapon damage %" was here at the template's 7.5 and is gone: it is one
# percent of the flat damage on the sheet over attacks/s, which is 182.50, so
# the template was understating a swing twenty-four fold. "attack opportunity
# cost" follows it and is now -182.50 as well.
#
# The two below are still the template's numbers and are the only ones in the
# file that nothing checks - offense and attack speed are preferences, not
# facts about the sheet. They are worth 500 and 310 in the current solution,
# so they are not idle.
#
# Nothing defensive is named at all, which is worth knowing before trusting a
# solution: with no weight on health, armor, defense or resist, the optimiser
# has been told a level 58 character wants nothing but damage, and it picks
# accordingly.
weights = {
	"offense": 5, "attack speed": 10,
}
