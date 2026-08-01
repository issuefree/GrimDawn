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
		# Kept deliberately: this excludes shield and ranged constellations.
		# Omitting it defaults to every weapon type, which is not the same thing.
		"weapons":["sword", "axe", "dagger", "mace", "scepter", "spear", "twohand"],
		# blacklist omitted - defaults to empty
	}

# One number per damage type saying how much you care about it. The flat vs %
# split is derived from the sheet above, which prices them very differently to
# the old 1:1 weights:
#   pierce  350 flat / 200%  ->  a % point is worth a little more than a flat one
#   bleed   275 flat / 300%  ->  a flat point is worth ~1.45x a % point
#   cold     20 flat /  50%  ->  a flat point is worth 7.5x a % point,
#                                there being almost no cold damage to scale up
damagePriority = {
		"pierce": 15,
		"bleed": 10,
		"cold": 7.5,
	}

weights = {
		"attack opportunity cost":-100,
		"attack speed":10,
		"cast speed":7.5,

		"offense": 5, # "offense %": ,

		"damage":1,

		# No physical on the sheet, so the flat/% split cannot be derived and
		# these stay explicit. If this character does carry physical damage, add
		# it to stats above and move this into damagePriority.
		"physical": 10, "physical %": 10,

		"bleed duration":5,

		"weapon damage %":7.5,

		"crit damage": 1,

		# "lifesteal %":33,
		"move speed": 10,
	}
