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

		"hits/s":4,
		"low healths/s":1.0/30, # total guesswork.

		"physique":500,
		"cunning":500,
		"spirit":300,

		"offense":1000,
		"defense":1000,

		"health":6000,
		"health/s":35,

		"armor":392,

		"energy":2000,
		"energy/s":18,

		"physical %":75, "physical":0,
		"pierce %":150, "pierce":100,
		"bleed %":500, "bleed":500,
		"chaos %":300, "chaos":300,

		"fight length":30,

		"playStyle":"tank",
		"weapons":["sword", "axe", "dagger", "mace", "scepter", "spear", "twohand"],
		"blacklist":[
			# manticore, manticoreAcidSpray# I'm not sure it makes sense in this build. Not many attacks to bind it to and the stats on the constellation aren't that good.
		]
	}

# What every damage type is worth, in one place. One number each, and the
# flat-versus-percent split comes off the sheet - which is the part that cannot
# be done by hand and the part the four pairs below were getting wrong.
#
# These four are the halves of the pairs they replace, so the preference is
# unchanged and only the split moves:
#
#     physical    5 / 5     ->   4.88 / 0.00
#     pierce     10 / 10    ->  11.70 / 2.58
#     bleed      15 / 15    ->   3.57 / 2.15
#     chaos      15 / 15    ->  20.85 / 11.59
#
# physical % goes to nothing because the sheet says 0 flat physical, and 75%
# of nothing is nothing. bleed drops fourfold because it is a damage over time
# and he swings three times a second against a three second bleed, so he
# overwrites eight ninths of it before it lands - his triggered bleed is
# untouched by that and goes up, to 10.72, because a devotion's bleed is not
# reapplied by his swinging.
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
		# "weapon damage %" was 7.5 and derives at 30.71: one percent of the
		# flat damage on the sheet, over attacks/s.
		"attack speed":10,
		"cast speed":7.5,

		"offense": 20, # "offense %": ,

		# not a split of anything, so not a priority
		"bleed duration":5,

		"crit damage": 1,

		"lifesteal %":33,
		"move speed": 10,

		# Nothing defensive is weighted, and playStyle says tank. With no
		# weight on health, armor, defense, resist or block, the optimiser has
		# been told a level 43 character wants nothing but damage and picks
		# accordingly - armitage, who is the same archetype, weights all five.
	}
