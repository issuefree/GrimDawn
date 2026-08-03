# python pakse/pakse.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))

devotionPoints = 28

stats = {
		# Character level. Enemy defence follows from it and from the difficulty,
		# and crit chance follows from that against your offensive ability - so
		# without it every crit-triggered proc scores zero. It also decides which
		# gear evalItemMods will show you.
		"level":65,
		# Which column of the difficulty table to read. It moves enemy
		# defence, and every enemy resistance by up to twelve points, so
		# it is not a detail. Taken from the level band; correct it if he
		# is grinding a difficulty he has out-levelled.
		"difficulty":"elite",
		"attacks/s":2,
		"allAttacks/s":[
			1, # main attack, half value due to spamming abilities
			1*.19, # smite 
			1*.18, # smash
			1*.15, # zolhan's 
			1*.15, # markovian's advantage
			.5, # aegis
			.5, # brutal shield slam: 3s recharge, 3 target max. Call it 2 targets and 4 seconds between = .5 aps
			.4, # war cry: 7.5 s recharge, big radius, call it 3 hits = 3/7.5 = .4
		],
		"blocks/s":1,
		"hits/s":1.5, # assuming a non-trivial fight
		"kills/s":.5,
		# crit chance was pinned here. It is derived now, from offensive
		# ability against the enemy defence that level and difficulty give -
		# so it tracks the sheet instead of going stale against it.
		"low healths/s":1.0/30, # total guesswork.

		"physique":1000,
		"cunning":400,
		"spirit":350,

		"offense":1100,
		"defense":1300,

		"health":10000,
		"health/s":133,

		"armor":1000,

		"energy":2000,
		"energy/s":15,

		"physical %":200, "physical":125,
		# "internal %":400, "internal":1,
		# "fire %":1300, "fire":1600,
		# "burn %":1000, "burn":500,
		# "lightning %":850, "lightning":69,
		# "electrocute %":650, "electrocute":1,
		# "chaos %":450, "chaos":1,
		"acid %":500, "acid":500,

		"retaliation %":500,

		"fight length":15,

		"playStyle":"tank",
		"weapons":["sword", "axe", "mace", "dagger", "shield"],
		"blacklist":[
			"bonds"  # for pet builds
		]
	}

weights = {
		# select the important bonuses from above and give them a value.
		# Note some bonuses will be automatically calculated if left blank (and should be unless you want to override):
		#	health/s <- health, health/s %, fight length
		#	energy/s <- energy, energy/s %, energy length

		#   physique <- health/s, health, defense
		#   cunning <- appropriate damage %, offense
		#   spirit <- appropriate damage %, energy, energy/s

		#	perc stats ["physique", "cunning", "spirit", "offense", "defense", "health", "energy", "armor"]
		#		will be calculated from your stats settings and base (non perc) values

		#   resist reductions <- appropriate damage % stat and bonus
		#	crit damage <- uses damage % stats and weights and crit chance stat

		#   elemental damage and resist <- fire/cold/lightning damage and resist  (includes pets)
		#   all damage % -< all individual damage % (includes pets)
		
		#Note there are a few shorthand notations. An individual setting will override the shorthand setting:
		#	resist <- sets a value for all resist types
		#	pet resist <- sets a value for all pet resist types
		#	reduce resist <- sets a value for all resist reductions
		#	damage <- sets a value for all on hit damage types
		#	triggered damage <- sets a value for all ability triggered damage types
		#		note that if you don't set triggered damage it gets valued at on hit damage of the same type since triggered damage is (roughly) normalized in value to on hit damage
		#   retaliation <- sets a value for all retaliation damage types
		#   pet retaliation <- sets a value for all pet retaliation damage types

		"attack speed":5,
		"cast speed":5,
		
		"energy":.25,
		"energy absorb": 15,

		"health": .66,

		"armor": 3, 
		"armor absorb": 20,
		
		"damage absorb %":100,

		"defense": 5, # "defense %": ,
		
		"resist": 15,
		
		"physical resist":35,
		"aether resist":25,


		"block %": 100,
		"blocked damage %":50,
		"shield recovery":75,

		"offense": 12.5, # "offense %": ,

		"damage":3,
		"physical": 10, "triggered physical":5, "physical %": 5,
		# "fire":15, "triggered fire":7.5, "fire %": 15,
		# "burn":7.5, "triggered burn":5, "burn %": 5, "burn duration":5,
		# "lightning": 7.5, "triggered lightning":3.25, "lightning %":5,
		#"elemental": 6, "triggered elemental":5, # "elemental %": 20,
		"acid":15, "triggered acid":2.5, "acid %":25,
		"poison":7.5, "triggered poison":1, "poison %":15, "poison duration":2,


		"weapon damage %": 7.5,

		"crit damage": 10,
		"damage reflect %": 35,
		"retaliation": 15, 
		"retaliation %": 25,
		
		"lifesteal %": 20,
		"move speed": 10,
	}

