# Lethe - devotion model.
#
# stats   = your character sheet, as the game reports it.
# weights = how much a point of each stat is worth to you. Relative values are
#           all that matter; scale is arbitrary. Start rough and refine.
#
# Only attacks/s and playStyle are required. Everything else is optional -
# add sheet numbers as you care about them. Unknown keys are reported on load.

# python lethe/lethe.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))

devotionPoints = 55

stats = {
	"attacks/s": 2.0,            # attacks per second, as swung in practice
	"playStyle": "melee",        # melee | shortranged | ranged | tank

	# Your skill bar. Name the skill and its rank and the rate comes from the
	# game's own cooldown; add a third number where you press it slower than it
	# recharges. The first entry is what you hold the button down on, and
	# passives and toggles anywhere in the list are read as modifiers on it.
	# "rotation": [("Cadence", 12), ("Blitz", 12, 4.0), 0.5],

	# What that swings for. Pressing a skill an item grants costs you one of
	# these, and a skill only earns its place by beating it - without a rotation
	# every component skill is measured against a bare 100% swing. Derived from
	# the rotation; set this only for an attack the skill data cannot describe.
	# "main attack %": 100,

	# Your level, and what you fight. Crit chance is derived from your offensive
	# ability against the enemy's defensive one using the game's own hit
	# formula, and enemy defence is derived from level - so stating "level" is
	# usually enough, and without it every crit-triggered proc scores zero.
	# Override "enemy defense" directly if you grind a difficulty whose scaling
	# the game's records do not carry. "enemy density" is enemies per square
	# metre and sizes every area proc.
	"level": 44,                  # the one number we have
	"difficulty": "normal",        # normal | elite | ultimate
	# "enemy defense": 1400,        # overrides what level+difficulty derive
	# "enemy resist": 25,           # ditto, for every damage type at once
	# "enemy density": 0.03,

	# "weapons": ["sword", "shield"],   # omit to allow every constellation
	# "physique": 0, "cunning": 0, "spirit": 0,
	# "offense": 0, "defense": 0,
	# "health": 0, "health/s": 0, "armor": 0,
	# "fight length": 30,

	# Flat and % damage for the types you care about. damagePriority below
	# uses these to work out what a point of each is actually worth.
	# "pierce": 350, "pierce %": 200,
}

# One number per damage type saying how much you care about it. The flat vs %
# split is derived from the sheet above: with 69 flat lightning and 850%
# lightning, a flat point is worth ~14x a percentage point, and with no flat
# physical at all, "physical %" multiplies nothing. You should not have to work
# that out by hand, and hand-written weights usually get it wrong.
damagePriority = {
	"physical": 10,
	"pierce": 5,
}

# Everything else - defence, speed, utility. Anything named here also overrides
# whatever damagePriority would have derived.
weights = {
	"offense": 5, "attack speed": 10,
}
