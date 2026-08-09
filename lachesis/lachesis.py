# python lachesis/lachesis.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))
devotionPoints = 28
# What is stated below is what the save gets wrong. Everything a model leaves
# out is filled in at load from the character's own save file - every worn item,
# its components, the set tiers and every point spent - so a stat written here
# is an override, and the comment beside it is what was derived. Anything the
# two agreed on to within 5% was deleted rather than annotated: it was a
# transcription of a number the code already had.
#
# A stated stat has the constellations already taken subtracted from it at load,
# because the sheet is read in town with them on and the optimiser is choosing
# them - so a value here can sit above the derived figure beside it by exactly
# what a devotion grants, and that is not a discrepancy.
#
#     python savefile.py Lachesis stats     what the save derives
#
stats =	{
		# Character level. Enemy defence follows from it and from the difficulty,
		# and crit chance follows from that against your offensive ability - so
		# without it every crit-triggered proc scores zero. It also decides which
		# gear evalItemMods will show you.
		# Which column of the difficulty table to read. It moves enemy
		# defence, and every enemy resistance by up to twelve points, so
		# it is not a detail. Taken from the level band; correct it if he
		# is grinding a difficulty he has out-levelled.
		"difficulty":"normal",
		"attacks/s":3.5,
		# Bare rates: nothing here is named, so no main attack is read. Name the
		# skills and their ranks and the cooldowns come from the game.
		"rotation":[
			3.5, # sigil
			2.5, # lightning totem
			2.5, # grasping roots
			1,   # pets/locust
			1,   # pets/locust
			1,   # pets/locust
		],
		"hits/s":.5,
		"blocks/s":0,
		"kills/s":1.5,
		# crit chance was pinned here. It is derived now, from offensive
		# ability against the enemy defence that level and difficulty give -
		# so it tracks the sheet instead of going stale against it.
		"low healths/s":1.0/30, # total guesswork.

		"cunning":400,  # derived 360 -10%

		# offense 1500 and defense 1250 were here and are gone: they are stale.
		# Both implied a per-level ability gain of 11.7 and 10.0 against a
		# 12.3-18.0 spread across every other character, which is a sheet that
		# has not been read in a while rather than a different rule. She is out
		# of the fit that LEVEL_ABILITY comes from for the same reason.
		#
		# What is left below is off the same stale sheet, so treat the derived
		# figures in these comments as the better number until she is re-read.

		"health":6500,  # derived 8603 +39%
		"armor":800,  # derived 873.54 +9%
		"energy":3500,  # derived 4963 +42%

		"vitality %":1050,  # derived 678 -15%
		"chaos %":500,  # derived 259 -32%

		"pet all damage %":250+100,  # derived 383 +32%

		"fight length":15,

		"playStyle":"shortranged",
		"weapons":["offhand"],
		"blacklist":[
			# sage, 			#seems cool but there's nothing but the ability
			# wolf,			#relatively low value for the requirements
			# soldier,			#relatively low value for the requirements
			# tree, spear,
			# falcon, hammer, owl, harpy, throne, wolverine, blade # don't need these. crook will supply all I need.
		]
	}

	
weights = {
		"offense":20, 
		"cast speed":25,
		"defense":7.5,
		"armor":3.5, 
		# armor absorb is good vs lots of little hits. This char regens fast with lots of little enemies so there's not much value
		"armor absorb":10,
		"health":.75,
		"health/s":5, #downgraded because I lifesteal so much. i really just want a big pool not regen.
		"energy":.66,
		"energy/s %":10,
		"avoid melee":10, "avoid ranged":15,

		"resist":7.5,

		"fire resist":0,
		"cold resist":0,
		"lightning resist":0,
		"vitality resist":0,

		"pet attack speed":5,
		"pet total speed":15,
		"pet offense":5,
		"pet offense %":50,
		"pet lifesteal %":10,
		"pet all damage %":10,
		"pet damage":5,
		"pet defense %":2.5,
		"pet resist":2.5,
		"pet health %":10,
		"pet health/s":10,
		"pet retaliation":1, "pet retaliaion %":3,

		"vitality %":25,
		"chaos %":7.5,

		"triggered vitality":35, "triggered vitality decay":15,
		"triggered chaos":10,
		"triggered life leech":5,
		"triggered damage":1,
		
		"attack opportunity cost":0, # I don't auto attack.
		"slow move":2.5,
		"stun %":20,

		"Raise the Dead":.5,
	}