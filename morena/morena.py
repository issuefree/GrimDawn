# python morena/morena.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))

devotionPoints = 20

stats = {
		"level":38,
		"difficulty":"normal",

		"physique":449,
		"cunning":677,
		"spirit":273,

		"offense":1159,
		"defense":835,
		"armor":366,

		# Off the sheet - her Attack Speed, which is what one weapon swing
		# takes. Not a sum of everything she presses: that is allAttacks/s
		# below, and counting the bar in both places counted it twice.
		"attacks/s":1.91,
		# His rotation, from bots/morena.ahk against the cooldowns the records
		# state. A skill fires no faster than its cooldown and no faster than
		# it is pressed, so the rate is one over whichever is longer; the load
		# prints which one won for each. RANKS ARE STUBS.
		"allAttacks/s":[
			("Onslaught", 1),                  # held on left button
			("Shadow Strike", 8, 1.75),
			("Ring of Steel", 8, 1.5),
			("Leap", 8, 1.5),
			("Bonechilling Cry", 8, 4.5),
			("Rallying Cry", 8, 8.0),
			("Amarasta's Blade Burst", 8, 10.0),
			("Sacred Strike", 1.5),        # off Blessed Steel
		],
		# The first of those, with the modifiers that only apply to it. Read for
		# what a swing is worth, which is what pressing a skill an item grants
		# costs you - update it as these get levelled, because a component skill
		# that beats Onslaught at 1 will not beat it at 10.
		"main attack":[("Onslaught", 1), ("Open Wounds", 3), ("Endless Rage", 1)],

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
