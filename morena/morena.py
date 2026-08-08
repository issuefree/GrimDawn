# python morena/morena.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))

devotionPoints = 20

stats = {
		"level":39,
		"difficulty":"normal",

		"physique":500,
		"cunning":750,
		"spirit":300,

		"offense":1200,
		"defense":900,
		"armor":425,

		"attacks/s":1.88,
		"rotation":[
			# Held on the left button, with the two passives that modify it
			# nested inside - they are not buttons, and Onslaught is the only
			# thing they can apply to.
			# Ranks are points spent, off the save with
			#     python savefile.py Morena
			# not the rank the skill screen shows. She has exactly one point in
			# every skill on this bar; the numbers above 1 here were her skill
			# screen, and that difference is her gear, stated once off the same
			# save instead of being folded in nine times.
			("Onslaught", 1, [("Open Wounds", 1), ("Endless Rage", 1)]),
			("Shadow Strike", 1),
			("Ring of Steel", 1, [("Circle of Slaughter", 1)]),
			("Leap", 1, [("Fault Line", 1)]),
			("Bonechilling Cry", 1, 12),
			("Rallying Cry", 1, [("Frenzied Cry", 1), ("Impulse", 1)]),
			("Pneumatic Burst", 1, [("Breath of Belgothian", 1), ("Shadow Dance", 1), ("Elemental Awakening", 1)]),
			# WPS skills
			("Bloodfangs", 1), ("Avalanche", 1), ("Belgothian's Shears", 1),
			("Amarasta's Quick Cut", 1), ("Whirling Death", 1),
			("Battle Surge", 1),
			("Untamed Rage", 1),
		],

		"hits/s":2,
		"low healths/s":1.0/30, # total guesswork.

		"health":5500,
		"health/s":60,

		"energy":1600,
		"energy/s":9,

		"physical %":150, "physical":375,
		"pierce %":400, "pierce":550,
		"bleed %":400, "bleed":150,
		"cold %":150, "cold":50,
		"frostburn %":250, "frostburn":0,

		"fight length":30,

		"playStyle":"melee",
		"weapons":["sword", "axe", "dagger", "mace", "scepter", "spear"],
	}

damagePriority = {
		# Derived from the rotation rather than stated. She deals 50% pierce,
		# 25% bleed, 22% physical, 3% cold - against hand-written priorities of
		# 10, 5, 7.5 and 5, which had cold level with bleed while dealing an
		# eighth of it. The bleed is a quarter of her output only because Open
		# Wounds is counted: it hangs off Onslaught rather than being pressed,
		# so it is in "main attack" above and not in the rotation, and folding
		# it in took her bleed from 17% to 25%.
		#
		# 16 is what her largest damage weight was before this, so the rest of
		# the model keeps its scale. Name a type beside it to lean.
		"rotation": 16,
	}

weights = {
		"attack speed":50,
		"cast speed":25,

		"offense": 5, # "offense %": ,

		"health":.1,
		"energy":.1,

		"bleed duration":5,

		# "lifesteal %":33,
		"move speed": 50,
	}
