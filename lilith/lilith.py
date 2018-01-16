devotionPoints = 45

stats = {
		# estimate how frequent combat events are for calculating dynamic stats and abilities
		"attacks/s":2,
		"allAttacks/s":[
			# list of attack skills that can be linked to abilities. remember to include your main attack.
			# 5, # skeletons (1 per skeleton)
			# 1, # zombie
			# 1, # raven
			2, #curse
			.2, #reap
			1, #bone harvest
		],
		"hits/s":.2,
		"blocks/s":0,
		"kills/s":.25,
		"crit chance":.15,
		"low healths/s":.075, # total guesswork.

		"fight length":20, # average length of a fight... this is for weighting abilities and over time effects. If you rely on wearing down opponents this should be long. If you are a glass cannon this should be small.

		# estimated sheet stats for target level
		"physique":617,
		"cunning":442,
		"spirit":813,

		"offense":1890,
		"defense":1706,

		"health":9834,
		"health/s":88.38,
		"health regeneration":0,

		"energy":6019/2,
		"energy/s":52.12,
		"energy regeneration":0,

		"armor":1199,
		
		# estimated damage % for target level. add whatever damages are important to your build
		"aether %":300, # sheet % damage for important damage types.
		"physical %":230,
		"vitality %":400,
		"vitality decay %":200,
		"chaos %":400,

		"pet damage %":1241,

		"playStyle":"shortranged", # playstyle for weighting constellation abilities. [ranged/shortranged/melee/tank]
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
		"move speed":7.5, 

		"armor":.2,
		"health":.2,
		
		"resist":1,
		"vitality resist":0,
		"fire resist":0,
		"cold resist":0,
		"lightning resist":0,
		"acid resist":0,
		"pierce resist":2.5,
		"chaos resist":2.5,
		"bleed resist":0,
		"aether resist":0.5,
		"physiacl resist":25,

		"defense":.5,

		"avoid melee":15,
		"avoid ranged":25,

		"offense":1,

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
		"pet health %":15, 
		"pet health regeneration":2.5, 
		"pet health/s":7.5, 
		
		"pet resist":1.5,
		"pet fire resist":0,
		"pet cold resist":0,
		"pet lightning resist":0,
		"pet poison resist":2,
		"pet pierce resist":2,
		"pet bleed resist":2,		

		"pet lifesteal %":15, 
		"pet offense":5,
		"pet offense %":50, 
		"pet crit damage":10,

		"pet retaliation":2.5,
		"pet retaliation %":5, 
		
		"pet move speed":10,		
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

		"reduce defense":2,
		"slow move":5,

		"total speed":15,

		"Bysmiel's Command":2.5, #hard skills to keep active 100%, bonus due to it being a summon
		"Raise the Dead":.5 #summons scale with player damage not pet damage so they won't be very good
	}

