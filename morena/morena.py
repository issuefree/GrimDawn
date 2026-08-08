# python morena/morena.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))

devotionPoints = 20

# What is stated below is what the save gets wrong. Everything a model leaves
# out is filled in at load from the character's own save file - every worn item,
# its components, the set tiers and every point spent - so a stat written here
# is an override, and the comment beside it is what was derived. Anything the
# two agreed on to within 5% was deleted rather than annotated: it was a
# transcription of a number the code already had.
#
#     python savefile.py Morena stats     what the save derives
#
stats = {
		"level":39,
		"difficulty":"normal",

		"cunning":750,  # derived 682 -9%
		"spirit":300,  # derived 277 -8%

		"offense":1200,  # derived 533 -56%
		"defense":900,  # derived 286 -68%
		"armor":425,  # derived 216.86 -49%

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

		"health/s":60,  # derived 44.68 -26%

		"energy":1600,  # derived 1806 +13%
		"energy/s":9,

		"physical %":150, "physical":375,  # derived physical % 86 -43%, physical 114.5 -24%
		"pierce %":400, "pierce":550,  # derived pierce % 194 -52%, pierce 37 -66%
		"bleed %":400, "bleed":150,  # derived bleed % 251 -37%
		"cold %":150, "cold":50,  # derived cold % 69 -54%, cold 5.5 -72%
		"frostburn %":250, "frostburn":0,  # derived frostburn % 90 -64%

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
