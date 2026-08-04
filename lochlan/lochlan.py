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

devotionPoints = 27

stats = {
		# The character, not the plan. This was 85 with the sheet below written
		# as estimates for that level - see the block marked "still level 85"
		# further down, which is what now has to come off the real sheet.
		"level":59,
		"difficulty":"veteran",
		# estimate how frequent combat events are for calculating dynamic stats and abilities
		"attacks/s":2,
		# His rotation, from bots/lochlan.ahk against the cooldowns the records
		# state. A skill fires no faster than its cooldown and no faster than
		# it is pressed, so the rate is one over whichever is longer; the load
		# prints which one won for each. The first entry is what he holds the
		# button down on, and it is his main attack. RANKS ARE STUBS.
		"rotation":[
			("Savagery", 10),                  # held on left button
			("Primal Strike", 10, 1.0),
			("Storm Totem", 10, 4.3),
			("Wendigo Totem", 10, 5.0),
			("War Cry", 10, 5.0),
					# "oleronsMight" was a rate here. It is Oleron's Might off
					# Oleron's Blood, and it fires on attack rather than being
					# pressed - so it is not a separate attack source at all,
					# it rides the ones below. Counting it doubled a share of
					# his rotation.
			1,      # Wind Devil. Really is missing from skillData: its record
					# yields no bonuses skillgen can read, so there is nothing
					# to name. See NOTES.md
		],
		"hits/s":2,
		"blocks/s":0,
		"kills/s":1.5,
		# crit chance was pinned here. It is derived now, from offensive
		# ability against the enemy defence that level and difficulty give -
		# so it tracks the sheet instead of going stale against it.
		"low healths/s":1.0/20, # total guesswork.

		"fight length":20, # average length of a fight... this is for weighting abilities and over time effects. If you rely on wearing down opponents this should be long. If you are a glass cannon this should be small.

		"physique":752,
		"cunning":392,
		"spirit":448,

		"offense":1946,
		"defense":1608,

		"health":10000,
		"health/s":145,

		"armor":1353,

		"energy":2265,
		"energy/s":34,
		
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

weights = {
		"armor":2.5, "armor absorb":30,
		"avoid melee":30, "avoid ranged":25,
		"defense":15,

		"attack speed":75,
		"cast speed":25,

		"offense":20,
		
		"health":1.5,
		"energy":1,
		"lifesteal %":100,

		# lightning, electrocute and physical are split out of damagePriority
		# above. Duration is not a split of anything, so it stays here.
		"electrocute duration":2.5,

		# "physical to lightning" and "physical to elemental" were 5 and 1 here.
		# Both are derived from the sheet now that it carries flat damage,
		# because what a conversion is worth is not a preference: it moves a
		# hundredth of your 150 flat physical onto lightning's weight instead
		# of physical's, and the sheet says what that trade is.

		# "weapon damage %" was 100 by hand and is derived now - your flat
		# damage pool priced at the weights above, over attacks/s.
		#
		# "attack opportunity cost" was -300 against that hand-set 100: three
		# swings for one cast, for the savagery stacks a cast drops. It now
		# derives at one swing, like every other model. If the three was right,
		# state the whole figure here as a weight - but note it is three times
		# whatever weapon damage % currently derives to, not three times 100,
		# and it will need revisiting whenever the sheet moves.

		"resist":5,
		"physical resist":125,

		# 0-25 = 50
		# 25-50 = 33
		# 50-60 = 25
		# 60-75 = 20
		# 75-85 = 10		
		"pierce resist":25,
		"fire resist":0, 
		"cold resist":0, 
		"lightning resist":0, 
		"bleed resist":20,
		"acid resist":20,
		"aether resist":0,
		"chaos resist":25,
		"vitality resist":0,

		# "stun %" is the stun duration modifier - the game has no second field
		# for it, so the "stun duration":5 that used to sit under here could
		# never be paid.
		"stun %":25,

		"move speed":20,

		# scales with pet damage and we're not using that
		"Bysmiel's Command":0,
		"Shepherd's Call":0,
	}

skills = [
	{"Markovian's Advantage":6},
	{"Fighting Spirit":4},
	{"Menhir's Will":4},
	{"Military Conditioning":5},
	{"Zolhan's Technique":7},
	{"Blitz":1},
	{"Veterancy":1},
	{"War Cry":3},
	{"Field Command":9},
	{"Terrify":3},
	{"Decorated Soldier":1},
	{"Blindside":2},
	{"Squad Tactics":4},
	{"Break Morale":1},
	{"Counter Strike":1},
	{"Scars of Battle":3},

	{"Brute Force":1},
	{"Savagery":9},
	{"Primal Strike":6},
	{"Might of the Bear":3},
	{"Mogdrogen's Pact":3},
	{"Feral Hunger":5},
	{"Wind Devil":1},
	{"Summon Briarthorn":1},
	{"Torrent":4},
	{"Tenacity of the Boar":5},
	{"Heart of the Wild":5},
	{"Wendigo Totem":2},
	{"Raging Tempest":8},
	{"Storm Surge":4},
	{"Oak Skin":1},
	{"Storm Totem":6},
	{"Storm Touched":5},
	{"Blood Pact":1},
	{"Maelstrom":2},
	{"Emboldening Presence":2},
	{"Stormcaller's Pact":8},
	{"Conjure Primal Spirit":1},
]

# skills = {}

constellations = [xC, fiend, viper, tsunami, wraith, quill, kraken, tempest, hawk, eel, ultosHandofUltos, spearoftheHeavens]
# constellations = [ultos]