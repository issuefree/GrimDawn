devotionPoints = 20

stats = {
		"level":32,
		"difficulty":"elite",

		"attacks/s":3,
		"allAttacks/s":[
			1.5, # main attack (taking it down a notch due to using other abilities etc)
			1,   # slam
			.75,  # ring
			.75,  # blades
			.75,  # shadow
		],

		"hits/s":2,
		"low healths/s":1.0/30, # total guesswork.

		"physique":375,
		"cunning":600,
		"spirit":200,

		# Sheet value. crit chance is derived from this and comes out at the
		# 17.7% the training dummy reports, so it is not pinned here - pinning
		# it would go stale the moment this number changes.
		"offense":1250,
		"defense":810,

		"health":5000,
		"health/s":110,

		"armor":318,

		"energy":1300,
		"energy/s":8,

		"physical %":125, "physical":0,
		"pierce %":300, "pierce":500,
		"bleed %":450, "bleed":350,
		"cold %":100, "cold":50,

		"fight length":30,

		"playStyle":"melee",
		# Kept deliberately: this excludes shield and ranged constellations.
		# Omitting it defaults to every weapon type, which is not the same thing.
		"weapons":["sword", "axe", "dagger", "mace", "scepter", "spear", "twohand"],
		# blacklist omitted - defaults to empty
	}

damagePriority = {
		"pierce": 12.5,
		"physical": 10,
		"bleed": 5,
		"cold": 5,
	}

weights = {
		"attack speed":50,
		"cast speed":25,

		"offense": 5, # "offense %": ,

		"damage":1,

		"bleed duration":5,

		# "weapon damage %":7.5,

		"crit damage": 10,

		# "lifesteal %":33,
		"move speed": 50,
	}
