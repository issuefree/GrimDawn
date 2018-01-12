stats = {
		# estimate how frequent combat events are for calculating dynamic stats and abilities
		"attacks/s":1,
		"allAttacks/s":[
			# list of attack skills that can be linked to abilities. remember to include your main attack.
			# 5, # skeletons (1 per skeleton)
			# 1, # zombie
			# 1, # raven
			# 1, #curse
			.2, #reap
			.2, #doombolt
		],
		"hits/s":.2,
		"blocks/s":0,
		"kills/s":1,		
		"crit chance":.05,
		"low healths/s":.05, # total guesswork.

		"fight length":30, # average length of a fight... this is for weighting abilities and over time effects. If you rely on wearing down opponents this should be long. If you are a glass cannon this should be small.

		# estimated sheet stats for target level
		"physique":650,
		"cunning":400,
		"spirit":1000,

		"offense":1500,
		"defense":1500,

		"health":6000,
		"health regeneration":100,
		"energy":4000,
		"energy regeneration":50,

		"armor":1000,
		
		# estimated damage % for target level. add whatever damages are important to your build
		"aether %":300, # sheet % damage for important damage types.
		"physical %":175,
		"vitality %":400,
		"vitality decay %":200,
		"chaos %":400,

		"playStyle":"ranged", # playstyle for weighting constellation abilities. [ranged/shortranged/melee/tank]
		"weapons":[
			"offhand"
		],
		"blacklist":[
			# list of constellations that I want to manually exclude for some reason.
		]	
	}

weights = {
		# select the important bonuses from above and give them a value.
		# Note some bonuses will be automatically calculated if left blank (and should be unless you want to override):
		#	health/s <- health, health regeneration, fight length
		#	energy/s <- energy, energy regeneration, energy length

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

		"cast speed":2.5, 
		"move %":7.5, 

		"armor":.15,
		"health":.2,
		"resist":.5,
		"defense":.25,

		"avoid melee":15,
		"avoid ranged":30,

		"offense":1.5,

		"energy":.1,

		"pet damage":15,

		# "pet all damage %":25, 
		"pet vitality %":7.5,
		"pet physical %":10,
		"pet fire %":5,
		"pet lightning %":5,
		"pet chaos %":2.5,
		"pet acid %":5,
		"pet poison %":1,
		"pet burn %":1,

		"pet attack speed":20, 
		"pet defense":4,
		"pet defense %":7.5, 
		"pet health %":7.5, 
		"pet health regeneration":2.5, 
		"pet health/s":7.5, 
		"pet resist":2,
		"pet lifesteal %":15, 
		"pet offense":5,
		"pet offense %":50, 
		"pet crit damage":10,

		"pet retaliation":2.5,
		"pet retaliation %":5, 
		
		"pet move %":10,		
		"pet total speed":30, 

		"physical %":.5,
		"aether %":.75,
		"vitality %":.75,
		"chaos %":.75,
		"vitality decay %":.75,

		"triggered damage":1,
		"triggered vitality":1.5,
		"triggered vitality decay":1.5,
		"triggered aether":1.5,
		"triggered chaos":1.5,

		"reduce resist":1.25,
		"reduce physical resist":2.5, 
		"reduce vitality resist":2,
		"reduce defense":2,
		"slow move":5,

		"total speed":15,

		"Shepherd's Call":.66, #the skills this can bind to make it difficult to keep up 100%
		"Bysmiel's Command":2.5, #hard skills to keep active 100%, bonus due to it being a summon
		"Raise the Dead":.5 #summons scale with player damage not pet damage so they won't be very good
	}

