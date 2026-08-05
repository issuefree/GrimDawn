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

		# Off the sheet - her Attack Speed, which is what one weapon swing
		# takes. Not a sum of everything she presses: that is the rotation
		# below, and counting the bar in both places counted it twice.
		"attacks/s":1.88,
		# Her rotation, from bots/morena.ahk against the cooldowns the records
		# state. A skill fires no faster than its cooldown and no faster than
		# it is pressed, so the rate is one over whichever is longer; the load
		# prints which one won for each.
		#
		# Onslaught is first, so it is what she holds the button down on and it
		# is her main attack. What it swings for is what pressing a skill an
		# item grants costs her, and it moves as these get levelled: a component
		# skill that beats Onslaught at 1 will not beat it at 10.
		# RANKS ARE STUBS.
		"rotation":[
			# Held on the left button, with the two passives that modify it
			# nested inside - they are not buttons, and Onslaught is the only
			# thing they can apply to.
			("Onslaught", 1, [("Open Wounds", 3), ("Endless Rage", 1)]),
			("Shadow Strike", 1),
			("Ring of Steel", 3, [("Circle of Slaughter", 6)]),
			("Leap", 1, [("Fault Line", 4)]),
			("Bonechilling Cry", 1, 12),
			("Rallying Cry", 1, [("Frenzied Cry", 1), ("Impulse", 1)]),
			("Pneumatic Burst", 1, [("Breath of Belgothian", 1), ("Shadow Dance", 1), ("Elemental Awakening", 1)]),			
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
		# Kept deliberately: this excludes shield and ranged constellations.
		# Omitting it defaults to every weapon type, which is not the same thing.
		"weapons":["sword", "axe", "dagger", "mace", "scepter", "spear", "twohand"],
		# blacklist omitted - defaults to empty
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

		# "weapon damage %" left out on purpose: it is one percent of the flat
		# damage on the sheet above, so it is derived rather than guessed. It
		# came out at 71 where this said 25.

		# "lifesteal %":33,
		"move speed": 50,
	}
