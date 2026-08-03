# python fenris/fenris.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))

devotionPoints = 20

stats = {
		# Character level. Enemy defence follows from it and from the difficulty,
		# and crit chance follows from that against your offensive ability - so
		# without it every crit-triggered proc scores zero. It also decides which
		# gear evalItemMods will show you.
		"level":43,
		# Which column of the difficulty table to read. It moves enemy
		# defence, and every enemy resistance by up to twelve points, so
		# it is not a detail. Taken from the level band; correct it if he
		# is grinding a difficulty he has out-levelled.
		"difficulty":"normal",
		"attacks/s":3,
		"allAttacks/s":[
			1.5, # main attack (taking it down a notch due to using other abilities etc)
			1,   # slam
			.5,  # rip
			.33, # leap
		],

		# What he actually swings, which is what every damage weight is priced
		# against. Werewolf is the form; Feral Claws is the attack it gives him,
		# and it carries 110% weapon damage at rank 8 - so the flat damage on
		# the sheet below is not decoration, he delivers 110% of it every swing.
		# It also brings 117 pierce of its own, which is where the 200% pierce
		# below has something to multiply: none of it is on the sheet.
		"main attack": [("Feral Claws", 8), ("Werewolf", 8),
						("Voracity", 4), ("Recklessness", 9)],

		"hits/s":4,
		"blocks/s":0,   # no shield, so the block-triggered procs really are worth nothing
		"low healths/s":1.0/30, # total guesswork.

		"physique":600,
		"cunning":600,
		"spirit":300,

		"offense":1250,
		"defense":1100,

		"health":6000,
		"health/s":50,

		"armor":500,

		"energy":1500,
		"energy/s":14,

		"physical %":350, "physical":750,
		"pierce %":200, "pierce":0,
		"bleed %":650, "bleed":1500,
		"chaos %":350, "chaos":400,

		"fight length":30,

		"playStyle":"melee",
		# "weapons":["sword", "axe", "dagger", "mace", "scepter", "spear", "twohand"],
		"blacklist":[
			# manticore, manticoreAcidSpray# I'm not sure it makes sense in this build. Not many attacks to bind it to and the stats on the constellation aren't that good.
		]
	}

# What every damage type is worth, in one place. One number each, and the
# flat-versus-percent split comes off the sheet - which is the part that cannot
# be done by hand and the part the four pairs below were getting wrong.
#
# These four are the halves of the pairs they replaced, so the preference is
# unchanged and only the split moves. Against the current sheet:
#
#     physical    5    ->   5.10 / 5.51
#     pierce     10    ->   8.00 / 1.56
#     bleed      15    ->   2.52 / 3.90
#     chaos      15    ->  12.99 / 8.81
#
# pierce % has something to multiply only because Feral Claws brings 117
# pierce of its own - the sheet says 0 flat pierce, and 200% of what is on the
# sheet would be 200% of nothing. That is what naming the main attack buys.
#
# bleed is the low one at 2.49 despite 1500 flat and a priority of 15, because
# it is a damage over time: he swings three times a second against a three
# second bleed, so eight ninths of each application is overwritten before it
# lands. His triggered bleed is untouched by that and comes out far higher,
# because a devotion's bleed is not reapplied by his swinging - which is why
# his solution buys 3295 of it.
damagePriority = {
		"physical":5,
		"pierce":10,
		"bleed":15,
		"chaos":15,
		"damage":1,
	}

weights = {
		# "attack opportunity cost" was -100 and is derived now, at -30.71 -
		# one swing, which is what pressing a granted skill costs. The -100 is
		# in armitage and lochlan too and looks like a number that was copied
		# rather than chosen; state it here if he really does value a swing at
		# three times what it is worth.
		#
		# "weapon damage %" was 7.5 and derives at 42.19: one percent of the
		# flat damage on the sheet, over attacks/s.
		"attack speed":10,

		# not a split of anything, so not a priority
		"bleed duration":5,

		"crit damage": 1,

		"lifesteal %":33,
		"move speed": 10,

		# Staying alive. Nothing here was weighted at all until now, so the
		# optimiser had been told a squishy level 43 melee character wants
		# nothing but damage.
		#
		# These are starting values, not derived ones - what a point of health
		# is worth against a point of pierce is a preference, and there is
		# nothing in the game to read it off. They are scaled so defence comes
		# out at 38% of what the solution buys, which is a guess at "squishy
		# and would like not to be" rather than a measurement.
		#
		# It is not a smooth dial. Scaling all seven together by 0.4 rather
		# than 0.6 drops defence from 38% to 7%: Fox and Behemoth fall out of
		# the solution whole rather than shrinking, because twenty points buys
		# five constellations and each is in or out. Expect the same if you
		# push them up - the next thing that happens is another constellation
		# swaps in, not a gradual tilt.
		#
		# health carries the most of this. A point of it is worth 0.3 here, but
		# checkModel turns that into 9 per point of health/s - health times
		# fight length - and health/s is 2908 of the 3582 defence buys.
		#
		# No block: he carries no shield, so "block %", "blocked damage %" and
		# "shield recovery" are deliberately absent rather than forgotten.
		"health":0.3,
		"armor":0.9, "armor absorb":6,
		"defense":2.4,
		"resist":3.6, "physical resist":12,
		"avoid melee":4.8,
	}
