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

devotionPoints = 53

stats = {
		# The character, not the plan. This was 85 with the sheet below written
		# as estimates for that level - see the block marked "still level 85"
		# further down, which is what now has to come off the real sheet.
		"level":59,
		"difficulty":"elite",
		# estimate how frequent combat events are for calculating dynamic stats and abilities
		"attacks/s":2,
		"allAttacks/s":[
			2,	#savagery
			2,	#storm totem
			1,	#wind devil
			.33,#primal strike
		],
		"hits/s":2,
		"blocks/s":0,
		"kills/s":1.5,	
		# crit chance was pinned here. It is derived now, from offensive
		# ability against the enemy defence that level and difficulty give -
		# so it tracks the sheet instead of going stale against it.
		"low healths/s":1.0/20, # total guesswork.

		"fight length":20, # average length of a fight... this is for weighting abilities and over time effects. If you rely on wearing down opponents this should be long. If you are a glass cannon this should be small.

		# Worth checking against the sheet. This file began as a copy of
		# armitage's and the level and devotion points came along with it - 85
		# and 53 against his 86 and 57 - so the header that used to sit here
		# calling these "estimated sheet stats for target level" was inherited
		# too and proves nothing either way about the numbers below it. They are
		# a lightning build's and armitage's are a fire tank's, so they have
		# been reworked; whether they were reworked from the game or from
		# memory is the open question.
		#
		# One thing the level change does make wrong on its own: devotionPoints
		# above is still 53, which is armitage's and not reachable at 59.
		#
		# And the flat damage lines are missing outright, which is its own
		# problem: with no flat physical or lightning there is nothing for
		# weapon damage to scale, nothing to split a damage priority against,
		# and no pool for a conversion to trade - which is why "weapon damage %"
		# and "attack opportunity cost" below are hand-set numbers with nothing
		# underneath them.
		"physique":842,
		"cunning":388,
		"spirit":488,

		"offense":2128,
		"defense":1722,

		"health":10331,
		"health/s":249,
		"health/s %":9+18+18+8+6+6+6+11+10+40,

		"armor":1507,
		# "armor absorb":76,

		"energy":2265,
		"energy/s":19.08,
		"energy/s %":154.9,
		
		"physical %":420+159,
		"lightning %":1523+229,
		"electrocute %":1280+244,

		"playStyle":"melee", # playstyle for weighting constellation abilities. [ranged/shortranged/melee/tank]
		"weapons":[
			"twohand", "2h-axe"
		],
		"blacklist":[
			# list of constellations that I want to manually exclude for some reason.
		]	
	}

weights = {
		"armor":2.5, "armor absorb":30,
		"avoid melee":30, "avoid ranged":25,
		"defense":15,

		"attack speed":75,
		"cast speed":25,

		"offense":20,
		# "crit damage":20,
		
		"health":1.5,
		"energy":1,
		"lifesteal %":100,

		"electrocute":20, "electrocute %":10, "electrocute duration":2.5,
		"physical":9, "physical %":7.5,
		"lightning":25, "lightning %":30,
		"bleed":7, "bleed %":3,
		"cold":10, "cold %":2,
		"frostburn":10,
		"internal":7.5,
		"burn":7.5,
		"aether":7.5,
		"fire":9,

		"physical to lightning":5,
		"physical to elemental":1,

		"weapon damage %":100, 
		"attack opportunity cost":-150-100-50, # I like basic attacks since they stack my savagery plus the auto attack replacements

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

		"stun %":25,
		"stun duration":5,

		"move speed":20,

		# scales with pet damage and we're not using that
		"Bysmiel's Command":0,
		"Shepherd's Call":0,
	}

# The gear list that used to sit here is gone - some 170 lines of Item()
# literals that nothing read: models.py's `model.items = locals()["items"]`
# has been commented out for as long as git remembers. 26 of the 30 pieces
# are in the extracted data now and can be asked for by name:
#
#     compareGear("ultos' stormseeker", "mythical glyph of kelphat'zoth")
#     evalItems("ultos' hood")
#
# The four that are not are the Ultos' Storm set bonuses at 2/3/4/5 pieces,
# including the Ultos' Wrath proc on the fifth. itemgen does not read set
# records, so those are the one thing deleting this cost - see git history
# for what they said.

# items = [	Item( "Ultos' Stormseeker",
# 		{"physical":(270+386)/2, "attacks/s":1.45, "lightning":(5+53)/2, "lightning %":203, "electrocute %":203, "physical to lightning":45, "offense":18, "attack speed":16, "cast speed":16, "reduce cooldown":16, "Stormcaller's Pact":3},
# 		"twohand",
# 	),
# 	Item( "Mythical Touch of the Everliving Grove",
# 		{"armor":1014, "health":452, "health %":4, "health/s":26, "health/s %":40, "elemental resist":18, "Hearth of the Wild":2, "Oak Skin":2,
# 		"pet health %":10, "pet defense %":12, "pet vitality resist":39},
# 		"arms",
# 		Ability( "Healing Winds",
# 			{"type":"heal", "trigger":"attack", "chance":.1, "recharge":6},
# 			{"health %":3, "health":1650}
# 		)
# 	),

# ]

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