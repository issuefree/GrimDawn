# python kieri/kieri.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))


devotionPoints = 15

# What every damage type is worth, in one place. This one names none of
# them individually: "damage" is the priority for everything not named,
# and it was the weight of the same name until damage numbers were
# gathered here. A block that names nothing else divides by one, so it
# means exactly what it meant as a weight.
damagePriority = {
		"damage":1,
	}

weights = {
		"armor":.25,
		"attack speed":40, 
		"cast speed":10, 
		
		"offense":20, 

		"avoid melee":5, "avoid ranged":7.5, 
		"defense":5, 

		"resist":3,
		"physical resist":5, 

		"health":.66, 
		"energy":.5, 

		"physical":10, "physical %":15, 
		#"pierce":0, "pierce %":0, 
		"burn":5, "burn %":5, "burn duration":2.5, "triggered burn":7.5,
		"fire":15, "fire %":20, 
		"lightning":3, "lightning %":5, 
		"chaos %":1, 
		"pierce %":1.5,
		"elemental":5, 

		"lifesteal %":15, 

		"move speed":20, 

		"slow move":10, 
		"stun %":50, "stun duration":10, 

	}
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
#     python savefile.py Kieri stats     what the save derives
#
stats =	{
		# Character level. Enemy defence follows from it and from the difficulty,
		# and crit chance follows from that against your offensive ability - so
		# without it every crit-triggered proc scores zero. It also decides which
		# gear evalItemMods will show you.
		"level":33,
		# Which column of the difficulty table to read. It moves enemy
		# defence, and every enemy resistance by up to twelve points, so
		# it is not a detail. Taken from the level band; correct it if he
		# is grinding a difficulty he has out-levelled.
		"difficulty":"normal",
		# estimate how frequent combat events are for calculating dynamic stats and abilities
		"attacks/s":1.75,
		"hits/s":.25,
		"blocks/s":0,
		"kills/s":1.5,
		# crit chance was pinned here. It is derived now, from offensive
		# ability against the enemy defence that level and difficulty give -
		# so it tracks the sheet instead of going stale against it.
		"low healths/s":1.0/45, # total guesswork.

		"fight length":20, # average length of a fight... this is for weighting abilities and over time effects. If you rely on wearing down opponents this should be long. If you are a glass cannon this should be small.

		# estimated sheet stats for target level
		"cunning":450,  # derived 410 -9%


		"health":4000,  # derived 3609 -10%

		"armor":250,  # derived 145.43 -42%
		"energy":2000,  # derived 2182 +9%
		
		# estimated damage % for target level. add whatever damages are important to your build
		"physical": 200, "physical %":150,  # derived physical 47 -41%, physical % 49 -67%
		"fire": 650, "fire %":450,  # derived fire 46 -61%, fire % 186 -59%
		"burn":50, "burn %":300,  # derived burn % 82 -73%
		"lightning %":300,  # derived 58 -78%
		"electrocute %":300,  # derived 58 -77%

		"playStyle":"ranged", # playstyle for weighting constellation abilities. [ranged/shortranged/melee/tank]
		"rotation": [
			# The whole bar. His rank is the points he has spent, off the save -
			# it read 8 here, where he has spent 4 and his gear grants the other
			# 4 - and Explosive Strike, Static Strike and Brimstone come off the
			# records as modifiers of it.
			"Fire Strike",             # held on left button
		],
		"weapons":[
			"ranged"
		],
		"blacklist":[
			kraken, # 1hand ranged
			# list of constellations that I want to manually exclude for some reason.
		]	
	}