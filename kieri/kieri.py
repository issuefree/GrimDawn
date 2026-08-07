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
		"physique":450,
		"cunning":450,
		"spirit":450,

		"offense":1200,
		"defense":900,

		"health":4000,
		"health/s %":10,

		"armor":250,
		"energy":2000,
		
		# estimated damage % for target level. add whatever damages are important to your build
		"physical": 200, "physical %":150,
		"fire": 650, "fire %":450, 
		"burn":50, "burn %":300,
		"lightning %":300, 
		"electrocute %":300,

		"playStyle":"ranged", # playstyle for weighting constellation abilities. [ranged/shortranged/melee/tank]
		"rotation": [
			("Fire Strike", 8, [("Explosive Strike", 6), ("Static Strike", 2), ("Brimstone", 5)]),
		],
		"weapons":[
			"ranged"
		],
		"blacklist":[
			kraken, # 1hand ranged
			# list of constellations that I want to manually exclude for some reason.
		]	
	}