# python lochlan/lochlan.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
# Above the imports below, which need the repo root on the path.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))

from dataModel import *
from itemData import *
from constellationData import *

devotionPoints = 28

stats = {
		# The character, not the plan. This was 85 with the sheet below written
		# as estimates for that level - see the block marked "still level 85"
		# further down, which is what now has to come off the real sheet.
		"level":60,
		"difficulty":"normal",
		# estimate how frequent combat events are for calculating dynamic stats and abilities
		"attacks/s":1.76,
		"crit damage": 70,
		# His rotation, from bots/lochlan.ahk against the cooldowns the records
		# state. A skill fires no faster than its cooldown and no faster than
		# it is pressed, so the rate is one over whichever is longer; the load
		# prints which one won for each. The first entry is what he holds the
		# button down on, and it is his main attack. RANKS ARE STUBS.
		"rotation":[
			("Savagery", 13, [("Might of the Bear", 3), ("Tenacity of the Boar", 2), ("Storm Touched", 4)]),                  # held on left button
			("Primal Strike", 11, [("Torrent", 10), ("Storm Surge", 3)]),
			("Storm Totem", 10),
			("Wendigo Totem", 2, [("Blood Pact", 2)]),
			("Wind Devil", 2, [("Raging Tempest", 3), ("Maelstrom", 4)]),
			# WPS
			("Feral Hunger", 8), ("Markovian's Advantage", 3), ("Zolhan's Technique", 3)
		],
		"hits/s":1,
		"blocks/s":0,
		"kills/s":1.5,
		# crit chance was pinned here. It is derived now, from offensive
		# ability against the enemy defence that level and difficulty give -
		# so it tracks the sheet instead of going stale against it.
		"low healths/s":1.0/20, # total guesswork.

		"fight length":15, # average length of a fight... this is for weighting abilities and over time effects. If you rely on wearing down opponents this should be long. If you are a glass cannon this should be small.

		"physique":752,
		"cunning":392,
		"spirit":448,

		"offense":1946,
		"defense":1608,

		"health":1070, #base
		"health/s":145,

		"armor":1353,
		"armor absorb":84,

		"energy":490, #base
		"energy/s":34,
		
		"pierce resist":80,
		"fire resist":80, 
		"cold resist":80, 
		"lightning resist":80, 
		"bleed resist":73,
		"acid resist":40,
		"aether resist":6,
		"chaos resist":14,
		"vitality resist":51,

		"physical %":640, "physical":150,
		"lightning %":930, "lightning":5000,
		"electrocute %":1000, "electrocute":500,

		"playStyle":"melee", # playstyle for weighting constellation abilities. [ranged/shortranged/melee/tank]
		"weapons":[
			"twohand", "2h-axe"
		],
		"blacklist":[
			# list of constellations that I want to manually exclude for some reason.
		]	
	}

# One number per damage type saying how much you care about it. The flat and %
# weights are split out of it against the sheet, which is the part nobody can
# do by hand: with 5000 flat lightning and 1138% of it, a point of lightning %
# multiplies fifty flat points and a point of flat multiplies nothing but
# itself, so the percentage is worth four times as much. The hand-written pair
# had them at 25 and 30 - all but equal.
#
#     lightning     25 / 30    ->  22.42 / 90.54
#     electrocute   20 / 10    ->  13.08 /  4.94
#     physical       9 / 7.5   ->   4.89 /  0.82
#
# These three numbers were picked as the halves of the pairs they replaced,
# back when the split was normalised per type and so preserved each pair's
# total. It is normalised across the block now, which is what makes the three
# comparable with each other, and the totals move: lightning draws more of the
# block because most of its value is in the percentage. Re-tune them against
# each other rather than against what the old pairs summed to.
#
# Only these three are here because only these three are on the sheet. A type
# with neither a flat nor a percentage figure has nothing to infer a split
# from, so bleed, cold, frostburn, internal, burn, aether and fire stay as
# stated weights below - add them to the sheet and they can move up here.
damagePriority = {
		# Derived from the rotation rather than stated. He deals 88% lightning,
		# 9% electrocute, 2% physical - against hand-written priorities of 27.5,
		# 15 and 8.25, which had electrocute at over half of lightning while
		# dealing a ninth of it, and physical at a third while dealing a
		# fortieth.
		#
		# 90 is what his largest damage weight was before this, so the rest of
		# the model keeps its scale. Name a type beside it to lean.
		"rotation": 90,
	}

# How much of what the solution buys should be keeping him alive. Six weights
# were hand-set here - armor, armor absorb, avoid melee, avoid ranged, defense
# and health - and every one is derivable in effective health, so this replaces
# the lot.
#
# They were not consistent with each other, which is the argument for deriving
# them. Read back as a defensePriority each implied a different one, and the
# spread was more than tenfold: armor absorb was the cheapest reading and
# defensive ability the dearest, so a point of survival bought one way counted
# for far more than the same point bought the other. That is not a preference
# anybody held - it is what six numbers set one at a time look like.
#
# 2.5 lands closest to the 19% defensive share the hand-set numbers were
# actually buying, so this is a re-derivation rather than a rebalancing.
# Measured through the real runner with seeds cleared between runs:
#
#     0.5 ->  2%    1.5 -> 11%    2.5 -> 17%    4.0 -> 38%
#     1.0 ->  2%    2.0 -> 14%    3.0 -> 31%
#
# The totals beside those are not comparable with the 84019 the hand-set
# weights scored, and neither is 2.5's 82162: the derived weights are on a
# different scale - armor absorb goes from 30 to 469 - so what moved is the
# balance, not the build's worth. The share is what is comparable.
defensePriority = 2.5

weights = {
		"attack speed":75,
		"cast speed":25,

		"offense":20,

		"energy":1,
		"lifesteal %":100,

		# "resist" and the nine per-type weights under it are derived now, off
		# the resistances on the sheet: a point is worth health/(100 - what you
		# have), so it is worth four times as much at 20 as at 79 and nothing at
		# all at 80. The band table that used to sit here - 0-25 = 50, 25-50 =
		# 33, and so on - was that curve worked out by hand, and this is the
		# same shape read off the sheet instead of estimated in five steps.
		#
		# "physical resist" stays only because the sheet does not state his.
		# Put it up there with the other nine and this can go too.
		"physical resist":125,

		# "stun %" is the stun duration modifier - the game has no second field
		# for it, so the "stun duration":5 that used to sit under here could
		# never be paid.
		"stun %":25,

		"move speed":25,

		# scales with pet damage and we're not using that
		"Bysmiel's Command":0,
		"Shepherd's Call":0,
	}
