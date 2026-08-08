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

devotionPoints = 25

stats = {
	"attacks/s": 5.0,            # casts per second, as channelled in practice
	"playStyle": "ranged",        # melee | shortranged | ranged | tank

	# Rates the procs are scored against. attacks/s above covers 14 attack
	# triggers; these three are unset, so the 3 block-triggered, 14
	# hit-triggered and 2 low-health-triggered procs in the game all score
	# zero - a third of everything the optimiser could offer her.
	# "hits/s": 2, "blocks/s": 0, "low healths/s": 1.0/30,

	# Her whole bar is one channelled beam and a rank on it, so the rotation is
	# two lines. Albrecht's Aether Ray is first, which makes it the thing she
	# holds the button down on and the thing every damage weight is priced
	# against; Disintegration is a passive, so the load reads it as a modifier
	# rather than as a second attack.
	#
	# The beam carries no weapon component at all, so none of the flat damage on
	# the sheet below reaches it - the 1700 aether is what an auto-attack she
	# never makes would do, and her aether % is multiplying the 294 the beam
	# brings of its own. The rest of her bar is still missing; adding it would
	# stop every proc being scored against attacks/s alone.
	"rotation": [
		# Ranks are points spent, off the save with
		#     python savefile.py Hela
		# not the rank the skill screen shows. The Ray read 26 here because that
		# is what her skill screen says, and 14 of those are gear - which is now
		# stated once, off the same save, instead of being inside this number.
		("Albrecht's Aether Ray", 10, [("Disintegration", 2)]),
		("Reap Spirit", 8),
		("Siphon Souls", 2, [("Sear Souls", 1), ("Blood Boil", 1)]),
	],

	"level": 58,
	"difficulty": "normal",       # from the level band, not from the save

	"physique": 600, "cunning": 380, "spirit": 1053,
	"offense": 1635, "defense": 1300,
	"health": 9000, "health/s": 50, 
	"energy": 4500, "energy/s": 165,
	"armor": 479,

	# Flat and % damage for the types you care about. damagePriority below
	# uses these to work out what a point of each is actually worth.
	# vitality is 0 flat, so its percentage multiplies nothing and is priced at
	# nothing - that is not a mistake in the sheet, it is what 250% of no
	# vitality damage is worth.
	"aether": 1700, "aether %": 1200,
	"lightning": 500, "lightning %": 750,
	"vitality": 0, "vitality %": 250,
	"fire": 250, "fire %": 450,
	"cold": 250, "cold %": 450,
	"weapons":["sceptre", "offhand"],
	"blacklist":[
		tsunami # Hela's range for ray and reap are outside the range of the proc so it doesn't hit much.
	]
}

# One number per damage type saying how much you care about it. The flat vs %
# split is derived from the sheet above, and so is every damage weight in the
# model - this is the only place a damage number belongs.
#
# "damage" is the priority for every type not named, and it defaults to half
# the lowest one that is - 1.25 here. Write it in if that is wrong; leaving it
# out no longer means acid and chaos are worth nothing.
#
# These four now read very differently from a weapon build's, and that is the
# point. Every flat weight is zero - a point of aether on her gear does
# nothing for a beam that carries no weapon component - and the percentages
# are priced against what one cast actually lands, which is the beam's own 294
# aether and 262 fire, not the 1700 and 250 on the sheet. Her fire % went from
# 0.66 to 0.92 and her aether % from 17.99 to 4.11 on that alone.
#
# Which means these four numbers now buy a good deal less against "offense"
# and "attack speed" below than they did when they were priced off the sheet.
# They are relative to each other and were never calibrated against the
# utility weights; that is the next thing to look at.
damagePriority = {
	"aether": 10,
	"lightning": 10,
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
