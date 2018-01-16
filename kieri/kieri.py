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

		"damage":1,
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

		"weapon damage %":25, 
	}
stats =	{
		# estimate how frequent combat events are for calculating dynamic stats and abilities
		"attacks/s":3,		
		"hits/s":.25,
		"blocks/s":0,
		"kills/s":1.5,		
		"crit chance":.15,
		"low healths/s":1.0/45, # total guesswork.

		"fight length":20, # average length of a fight... this is for weighting abilities and over time effects. If you rely on wearing down opponents this should be long. If you are a glass cannon this should be small.

		# estimated sheet stats for target level
		"physique":450,
		"cunning":450,
		"spirit":450,

		"offense":1200,
		"defense":900,

		"health":3500,
		"health regeneration":10,

		"armor":250,
		"energy":2000,
		
		# estimated damage % for target level. add whatever damages are important to your build
		"physical %":150,
		"fire %":400, "burn %":200,
		"lightning %":250, "electrocute %":100,
		"pierce":100,
		"chaos":100,

		"playStyle":"ranged", # playstyle for weighting constellation abilities. [ranged/shortranged/melee/tank]
		"weapons":[
			"ranged"
		],
		"blacklist":[
			# list of constellations that I want to manually exclude for some reason.
		]	
	}