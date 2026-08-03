# Gwyr - devotion model.
#
# stats   = your character sheet, as the game reports it.
# weights = how much a point of each stat is worth to you. Relative values are
#           all that matter; scale is arbitrary. Start rough and refine.
#
# Only attacks/s and playStyle are required. Everything else is optional -
# add sheet numbers as you care about them. Unknown keys are reported on load.

# python gwyr/gwyr.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))

devotionPoints = 41

stats = {
	"attacks/s": 2.0,            # attacks per second, as swung in practice
	"playStyle": "ranged",        # melee | shortranged | ranged | tank

	# Break out each trigger source for a better estimate of stacked procs.
	# "allAttacks/s": [2.0, 1.0, 0.5],

	# What the first of those swings for. Pressing a skill an item grants costs
	# you one of these, and a skill only earns its place by beating it - leave
	# it out and every component skill is measured against a bare 100% swing.
	# "main attack %": 100,

	# Your level, and what you fight. Crit chance is derived from your offensive
	# ability against the enemy's defensive one using the game's own hit
	# formula, and enemy defence is derived from level - so stating "level" is
	# usually enough, and without it every crit-triggered proc scores zero.
	# Override "enemy defense" directly if you grind a difficulty whose scaling
	# the game's records do not carry. "enemy density" is enemies per square
	# metre and sizes every area proc.
	"level": 72,                  # the one number we have
	"difficulty": "elite",        # normal | elite | ultimate
	# "enemy defense": 1400,        # overrides what level+difficulty derive
	# "enemy resist": 25,           # ditto, for every damage type at once
	# "enemy density": 0.03,

	"weapons": ["2h ranged"],   # omit to allow every constellation
	"physique": 950, "cunning": 550, "spirit": 450,
	"offense": 2082, "defense": 1900,
	"health": 8000, "health/s": 320, 
	"energy": 2500, "energy/s": 28,
	"armor": 900,
	# "fight length": 30,

	# Flat and % damage for the types you care about. damagePriority below
	# uses these to work out what a point of each is actually worth.
	"physical": 100, "physical %": 300,
	"pierce": 675, "pierce %": 625,
	"fire": 3000, "fire %": 1400,
	"lightning": 25, "lightning %": 625,
	"burn": 2000, "burn %": 1000, "burn duration": 200,
	"electrocute": 0, "electrocute %": 400, "electrocute duration": 50,
}

# One number per damage type saying how much you care about it. The flat vs %
# split is derived from the sheet above: with 69 flat lightning and 850%
# lightning, a flat point is worth ~14x a percentage point, and with no flat
# physical at all, "physical %" multiplies nothing. You should not have to work
# that out by hand, and hand-written weights usually get it wrong.
damagePriority = {
	"fire":10,
	"burn":10,
	"physical": 5,
	"damage":1,
}

# Everything else - defence, speed, utility. Anything named here also overrides
# whatever damagePriority would have derived.
weights = {
	# "offense": 5, "attack speed": 10,
	# "weapon damage %": 7.5,
}
