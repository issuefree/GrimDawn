devotionPoints = 52

stats = {
		"attacks/s":2.75,
		"allAttacks/s":[
			2.75, #main attack (fire strike)
			.75, # thermite mine / mortar
			2.75*.25, # markovian's advantage
			.5, # brutal shield slam: 3s recharge, 3 target max. Call it 2 targets and 4 seconds between = .5 aps
			.4, #war cry: 7.5 s recharge, big radius, call it 3 hits = 3/7.5 = .4
		],
		"hits/s":4,
		"blocks/s":1.5,
		"kills/s":1,
		"crit chance":.15,
		"low healths/s":1.0/120, # total guesswork.

		"physique":1000,
		"cunning":400,
		"spirit":500,

		"offense":2000,
		"defense":2000,

		"health":10000,
		"health regeneration":250,

		"armor":2250,
		"energy":2250,

		"physical %":250, "physical":600,
		"internal %":275, "internal":1,
		"fire %":1800, "fire":4250,
		"burn %":1000, "burn":1500,
		"lightning %":850, "lightning":1100,

		"retaliation %":500+100,

		"fight length":30,

		"playStyle":"tank",
		"weapons":["sword", "shield"],
		"blacklist":[
			# manticore, manticoreAcidSpray# I'm not sure it makes sense in this build. Not many attacks to bind it to and the stats on the constellation aren't that good.
		]
	}

weights = {
		"attack opportunity cost":-100,
		"attack speed":10,
		"cast speed":7.5,
		
		"energy":.5, # "energy %": ,
		"energy absorb": 15,
		# "energy regeneration": ,
		# "energy/s": ,

		"health": .66, # "health %": ,
		# "health regeneration": 5,
		# "health/s": 5,

		"armor": 5-1.5, 
		"armor absorb": 20,
		
		"damage absorb %":100,

		"defense": 7.5, # "defense %": ,
		
		"resist": 15,
		
		"physical resist":35,
		"pierce resist":0,
		
		"fire resist":0, 
		"lightning resist":0,
		"cold resist":0,
		"acid resist":5,
		"chaos resist":0,
		"vitality resist":0,
		"aether reist":25,


		"block %": 100,
		"blocked damage %":50-10,
		"shield recovery":75,

		"offense": 12.5, # "offense %": ,

		"damage":1,
		"physical": 5, "triggered physical":2.5, "physical %": 5,
		"fire":15, "triggered fire":7.5, "fire %": 15,
		"burn":7.5, "triggered burn":5, "burn %": 5, "burn duration":5,
		"lightning": 7.5, "triggered lightning":3.25, "lightning %":5,
		#"elemental": 6, "triggered elemental":5, # "elemental %": 20,


		"weapon damage %":7.5,

		# "crit damage": ,
		"damage reflect %": 35,
		"retaliation":7, 
		"retaliation %":15,
		
		"stun %":-5,

		"lifesteal %":20,
		"move %": 10,

		"Acid Spray":.75,
	}