stats =	{
		"attacks/s":3.5,
		"allAttacks/s":[
			3.5, # sigil
			2.5, # lightning totem
			2.5, # grasping roots
			1,   # pets/locust
			1,   # pets/locust
			1,   # pets/locust
		],
		"hits/s":.5,
		"blocks/s":0,
		"kills/s":1.5,
		"crit chance":.1,
		"low healths/s":1.0/30, # total guesswork.

		"physique":650,
		"cunning":400,
		"spirit":600,

		"offense":1500,
		"defense":1250,

		"health":6500,
		"armor":800,
		"energy":3500,

		"vitality %":1050, "vitality decay %":450,
		"chaos %":500,

		"pet all damage %":250+100,

		"fight length":15,

		"playStyle":"shortranged",
		"weapons":["offhand"],
		"blacklist":[
			# sage, 			#seems cool but there's nothing but the ability
			# wolf,			#relatively low value for the requirements
			# soldier,			#relatively low value for the requirements
			# tree, spear,
			# falcon, hammer, owl, harpy, throne, wolverine, blade # don't need these. crook will supply all I need.
		]
	}

	
weights = {
		"offense":20, 
		"cast speed":25,
		"defense":7.5,
		"armor":3.5, 
		# armor absorb is good vs lots of little hits. This char regens fast with lots of little enemies so there's not much value
		"armor absorb":10,
		"health":.75,
		"health/s":5, #downgraded because I lifesteal so much. i really just want a big pool not regen.
		"energy":.66,
		"energy/s %":10,
		"avoid melee":10, "avoid ranged":15,

		"resist":7.5,

		"fire resist":0,
		"cold resist":0,
		"lightning resist":0,
		"vitality resist":0,

		"pet attack speed":5,
		"pet total speed":15,
		"pet offense":5,
		"pet offense %":50,
		"pet lifesteal %":10,
		"pet all damage %":10,
		"pet damage":5,
		"pet defense %":2.5,
		"pet resist":2.5,
		"pet health %":10,
		"pet health/s":10,
		"pet retaliation":1, "pet retaliaion %":3,

		"vitality %":25,
		"chaos %":7.5,

		"triggered vitality":35, "triggered vitality decay":15,
		"triggered chaos":10,
		"triggered life leech":5,
		"triggered damage":1,
		
		"weapon damage %":1,
		"attack opportunity cost":0, # I don't auto attack.
		"slow move":2.5,
		"stun %":20,

		"Raise the Dead":.5,
	}