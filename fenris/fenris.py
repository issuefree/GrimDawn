# python fenris/fenris.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))

devotionPoints = 20

stats = {
		# Character level. Enemy defence follows from it and from the difficulty,
		# and crit chance follows from that against your offensive ability - so
		# without it every crit-triggered proc scores zero. It also decides which
		# gear evalItemMods will show you.
		"level":43,
		# Which column of the difficulty table to read. It moves enemy
		# defence, and every enemy resistance by up to twelve points, so
		# it is not a detail. Taken from the level band; correct it if he
		# is grinding a difficulty he has out-levelled.
		"difficulty":"normal",
		"attacks/s":3,
		"allAttacks/s":[
			1.5, # main attack (taking it down a notch due to using other abilities etc)
			1,   # slam
			.5,  # rip
			.33, # leap
		],

		"hits/s":4,
		"low healths/s":1.0/30, # total guesswork.

		"physique":500,
		"cunning":500,
		"spirit":300,

		"offense":1000,
		"defense":1000,

		"health":6000,
		"health/s":35,

		"armor":392,

		"energy":2000,
		"energy/s":18,

		"physical %":75, "physical":0,
		"pierce %":150, "pierce":100,
		"bleed %":500, "bleed":500,
		"chaos %":300, "chaos":300,

		"fight length":30,

		"playStyle":"tank",
		"weapons":["sword", "axe", "dagger", "mace", "scepter", "spear", "twohand"],
		"blacklist":[
			# manticore, manticoreAcidSpray# I'm not sure it makes sense in this build. Not many attacks to bind it to and the stats on the constellation aren't that good.
		]
	}

# What every damage type is worth, in one place. This one names none of
# them individually: "damage" is the priority for everything not named,
# and it was the weight of the same name until damage numbers were
# gathered here. A block that names nothing else divides by one, so it
# means exactly what it meant as a weight.
damagePriority = {
		"damage":1,
	}

weights = {
		"attack opportunity cost":-100,
		"attack speed":10,
		"cast speed":7.5,
		
		"offense": 20, # "offense %": ,

		"physical": 5, "triggered physical":2.5, "physical %": 5,
		"pierce": 10, "pierce %": 10,
		"bleed":15, "bleed %": 15, "bleed duration":5,
		"chaos":15, "chaos %": 15, 

		"weapon damage %":7.5,

		"crit damage": 1,
		
		"lifesteal %":33,
		"move speed": 10,
	}
