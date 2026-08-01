devotionPoints = 20

stats = {
		"attacks/s":3,
		"allAttacks/s":[
			1.5, # main attack (taking it down a notch due to using other abilities etc)
			1,   # slam
			.75,  # ring
			.75,  # blades
			.75,  # shadow
		],

		"hits/s":4,
		"low healths/s":1.0/30, # total guesswork.

		"physique":375,
		"cunning":500,
		"spirit":200,

		"offense":1150,
		"defense":750,

		"health":4000,
		"health/s":50,

		"armor":318,

		"energy":1200,
		"energy/s":8,

		# "physical %":0, "physical":0,
		"pierce %":200, "pierce":350,
		"bleed %":300, "bleed":275,
		"cold %":50, "cold":20,

		"fight length":30,

		"playStyle":"tank",
		"weapons":["sword", "axe", "dagger", "mace", "scepter", "spear", "twohand"],
		"blacklist":[
			# manticore, manticoreAcidSpray# I'm not sure it makes sense in this build. Not many attacks to bind it to and the stats on the constellation aren't that good.
		]
	}

weights = {
		"attack opportunity cost":-100,
		"attack speed":10,
		"cast speed":7.5,
		
		"offense": 10, # "offense %": ,

		"damage":1,
		"physical": 10, "physical %": 10,
		"pierce": 15, "pierce %": 15,
		"bleed":15, "bleed %": 15, "bleed duration":5,
		"cold":10, "cold %": 10, 

		"weapon damage %":7.5,

		"crit damage": 1,
		
		# "lifesteal %":33,
		"move speed": 10,
	}
