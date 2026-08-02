# python morena/morena.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))

devotionPoints = 20

stats = {
		"level":33,
		"difficulty":"normal",

		"attacks/s":3,
		"allAttacks/s":[
			1.5, # main attack (taking it down a notch due to using other abilities etc)
			1,   # slam
			.75,  # ring
			.75,  # blades
			.75,  # shadow
		],
		# The first of those, with the modifiers that only apply to it. Read for
		# what a swing is worth, which is what pressing a skill an item grants
		# costs you - update it as these get levelled, because a component skill
		# that beats Onslaught at 1 will not beat it at 10.
		"main attack":[("Onslaught", 1), ("Open Wounds", 3), ("Endless Rage", 1)],

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
		"frostburn %":158, "frostburn":67,

		"fight length":30,

		"playStyle":"melee",
		# Kept deliberately: this excludes shield and ranged constellations.
		# Omitting it defaults to every weapon type, which is not the same thing.
		"weapons":["sword", "axe", "dagger", "mace", "scepter", "spear", "twohand"],
		# blacklist omitted - defaults to empty
	}

damagePriority = {
		"pierce": 10,
		"physical": 7.5,
		"bleed": 5,
		"cold": 5,
	}

weights = {
		"attack speed":50,
		"cast speed":25,

		"offense": 5, # "offense %": ,

		"damage":1,
		"health":.1,
		"energy":.1,

		"bleed duration":5,

		# "weapon damage %" left out on purpose: it is one percent of the flat
		# damage on the sheet above, so it is derived rather than guessed. It
		# came out at 71 where this said 25.

		# "lifesteal %":33,
		"move speed": 50,
	}
