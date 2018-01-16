devotionPoints = 57

stats = {
		"attacks/s":2.75,
		"allAttacks/s":[
			2, # main attack (fire strike) (taking it down a notch due to using other abilities etc)
			1, # stormfire - seal of destruction
			.75, # mortar
			.75, # thermite mine
			2*.25, # zolhan's 
			2*.25, # markovian's advantage
			.5, # brutal shield slam: 3s recharge, 3 target max. Call it 2 targets and 4 seconds between = .5 aps
			.4, #war cry: 7.5 s recharge, big radius, call it 3 hits = 3/7.5 = .4
		],
		"hits/s":4,
		"blocks/s":1.5,
		"kills/s":1,
		"crit chance":.10,
		"low healths/s":1.0/30, # total guesswork.

		"physique":1000,
		"cunning":475,
		"spirit":400,

		"offense":2000,
		"defense":2400,

		"health":10000,
		"health/s":275,

		"armor":2650,

		"energy":2000,
		"energy/s":18,

		"physical %":400, "physical":900,
		"internal %":400, "internal":1,
		"fire %":1300, "fire":1600,
		"burn %":1000, "burn":500,
		"lightning %":850, "lightning":69,
		"electrocute %":650, "electrocute":1,
		"chaos %":450, "chaos":1,

		"retaliation %":350+100,

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
		
		"energy":.75,
		"energy absorb": 15,

		"health": .66,

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
		"move speed": 10,

		"Acid Spray":.75,
	}


  # Solution([xA, xO, lion, xC, fiend, viper, hound, quill, phoenix, messenger, behemoth, hawk, torchMeteorShower, ultosHandofUltos, targoShieldWall], self),  # 58044 (57)
  # Solution([xA, xO, lion, xC, fiend, viper, raven, hound, phoenix, messenger, behemoth, hawk, torchMeteorShower, ultosHandofUltos, targoShieldWall], self),  # 57868 (57)
  # Solution([xA, xO, lion, xC, fiend, viper, hound, light, phoenix, messenger, behemoth, hawk, torchMeteorShower, ultos, targoShieldWall], self),  # 57830 (57)
  # Solution([xA, xO, lion, xC, fiend, viper, raven, hound, phoenix, messenger, behemoth, light, torchMeteorShower, ultosHandofUltos, targoShieldWall], self),  # 57656 (57)
  # Solution([xA, xO, lion, xC, fiend, viper, raven, light, lizard, phoenix, messenger, behemoth, torchMeteorShower, ultosHandofUltos, targoShieldWall], self),  # 57145 (57)
  # Solution([xE, hawk, xO, lion, xC, fiend, viper, hound, phoenix, behemoth, toad, messenger, torchMeteorShower, ultosHandofUltos, targoShieldWall], self),  # 57095 (57)
  # Solution([xO, lion, xC, fiend, viper, hound, quill, phoenix, behemoth, toad, messenger, torchMeteorShower, ultosHandofUltos, targoShieldWall], self),  # 56990 (57)
  # Solution([xO, lion, xC, fiend, viper, raven, hound, phoenix, behemoth, toad, messenger, torchMeteorShower, ultosHandofUltos, targoShieldWall], self),  # 56814 (57)
  # Solution([xE, hawk, xO, lion, xC, viper, wraith, shieldmaiden, messenger, behemoth, phoenix, crown, targo, ultosHandofUltos], self),  # 55767 (57)
  # Solution([xE, xO, lion, xP, imp, xC, fiend, behemoth, viper, phoenix, toad, messenger, torchMeteorShower, ultosHandofUltos, targoShieldWall], self),  # 55607 (57)
  # Solution([xE, quill, xO, lion, xC, viper, wraith, shieldmaiden, messenger, behemoth, phoenix, ultosHandofUltos, chariotWaywardSoul, targoShieldWall], self),  # 55497 (57)
  # Solution([xO, lion, xC, fiend, viper, quill, wraith, phoenix, shieldmaiden, messenger, crown, ultosHandofUltos, behemothGiantsBlood, targoShieldWall], self),  # 55452 (57)
  # Solution([xO, panther, wraith, lion, shieldmaiden, messenger, fiend, viper, raven, phoenix, ultosHandofUltos, obeliskStoneForm, targoShieldWall], self),  # 55450 (57)
  # Solution([xE, xO, lion, xC, fiend, viper, wraith, shieldmaiden, messenger, behemoth, phoenix, crown, ultosHandofUltos, targoShieldWall], self),  # 55317 (57)
  # Solution([xE, xO, lion, xC, viper, imp, shieldmaiden, behemoth, phoenix, owl, messenger, crown, ultosHandofUltos, targoShieldWall], self),  # 54990 (57)
  # Solution([xE, raven, xO, lion, xC, fiend, viper, hound, phoenix, shieldmaiden, wolverine, messenger, behemothGiantsBlood, ultosHandofUltos, targoShieldWall], self),  # 54938 (57)
  # Solution([xO, dryad, xC, fiend, viper, raven, hound, phoenix, wolverine, messenger, crown, ultosHandofUltos, behemothGiantsBlood, targoShieldWall], self),  # 53228 (57)
  # Solution([xO, panther, imp, lion, shieldmaiden, xC, fiend, phoenix, behemoth, wolverine, messenger, ultosHandofUltos, targoShieldWall], self),  # 52758 (57)
	