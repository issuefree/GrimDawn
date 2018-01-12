stats = {
		# estimate how frequent combat events are for calculating dynamic stats and abilities
		"attacks/s":2.16,
		"allAttacks/s":[
			2,	#savagery
			2,	#storm totem
			1,	#wind devil
			.33,#primal strike
		],
		"hits/s":1.5,
		"blocks/s":0,
		"kills/s":1.5,	
		"crit chance":.15,
		"low healths/s":1.0/15, # total guesswork.

		"fight length":20, # average length of a fight... this is for weighting abilities and over time effects. If you rely on wearing down opponents this should be long. If you are a glass cannon this should be small.

		# estimated sheet stats for target level
		"physique":800,
		"cunning":400,
		"spirit":550,

		"offense":1500,
		"defense":1500,

		"health":8000,
		"health regeneration":90,

		"armor":1300,
		"energy":2500,
		
		# estimated damage % for target level. add whatever damages are important to your build
		"physical %":700,
		"lightning %":900,
		"electrocute %":650,

		"playStyle":"melee", # playstyle for weighting constellation abilities. [ranged/shortranged/melee/tank]
		"weapons":[
			"twohand", "2h-axe"
		],
		"blacklist":[
			# list of constellations that I want to manually exclude for some reason.
		]	
	}

weights = {
		"armor":2, "armor absorb":10,
		"avoid melee":20, "avoid ranged":15,
		"defense":10,

		"attack speed":50,
		"cast speed":25,

		"offense":25,
		# "crit damage":20,
		
		"health":1,
		"energy":.75,
		"lifesteal %":20,

		"electrocute":15, "electrocute %":10, "electrocute duration":2.5,
		"physical":15, "physical %":15,
		"lightning":20, "lightning %":25,
		"bleed %":5,

		"weapon damage %":50, 
		"attack opportunity cost":-50,

		"resist":5,
		"physical resist":20,

		"pierce resist":.5, "fire resist":0, "cold resist":0, "lightning resist":0, "bleed resist":2.5,
		"poison resist":10,
		"aether resist":10,
		"chaos resist":10,
		"vitality resist":7.5,

		"stun %":10,
		"stun duration":5,

		"move %":20,

		# scales with pet damage and we're not using that
		"Bysmiel's Command":0,
	}