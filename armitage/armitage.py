# python armitage/armitage.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))

devotionPoints = 57

# What is stated below is what the save gets wrong. Everything a model leaves
# out is filled in at load from the character's own save file - every worn item,
# its components, the set tiers and every point spent - so a stat written here
# is an override, and the comment beside it is what was derived. Anything the
# two agreed on to within 5% was deleted rather than annotated: it was a
# transcription of a number the code already had.
#
# A stated stat has the constellations already taken subtracted from it at load,
# because the sheet is read in town with them on and the optimiser is choosing
# them - so a value here can sit above the derived figure beside it by exactly
# what a devotion grants, and that is not a discrepancy.
#
#     python savefile.py Armitage stats     what the save derives
#
stats = {
		# Character level. Enemy defence follows from it and from the difficulty,
		# and crit chance follows from that against your offensive ability - so
		# without it every crit-triggered proc scores zero. It also decides which
		# gear evalItemMods will show you.
		"level":86,
		# Which column of the difficulty table to read. It moves enemy
		# defence, and every enemy resistance by up to twelve points, so
		# it is not a detail. Taken from the level band; correct it if he
		# is grinding a difficulty he has out-levelled.
		"difficulty":"ultimate",
		# Attack Speed off the sheet. It is what the held attack runs at, what a
		# damage over time is refreshed at, and the rate every attack-triggered
		# proc fires off.
		"attacks/s":2.41,
		# His rotation, from bots/armitage.ahk against the cooldowns the records
		# state. A skill fires no faster than its cooldown and no faster than
		# it is pressed, so the rate is one over whichever is longer; the load
		# prints which one won for each. The first entry is what he holds the
		# button down on, and it is his main attack. RANKS ARE STUBS.
		"rotation":[
			# What is on the bar and the order he plays it. The rank is the
			# points he has spent, off the save, and the modifiers come off the
			# records - Explosive Strike, Searing Strike, Static Strike and
			# Break Morale were all written out here and all come back on their
			# own. Searing Might is the case that shows why they are derived
			# rather than listed: it modifies Explosive Strike, which modifies
			# Fire Strike, and only Fire Strike is a button.
			"Fire Strike",                 # held on left button
			("Thermite Mine", 5.0),
			("War Cry", 7.5),
			("Mortar Trap", 15.0),
			"Zolhan's Technique",
			"Markovian's Advantage",
			("Brutal Shield Slam", 3.0),   # off Serrated Shell: 300% weapon
										   # damage where the plain Shield Slam off a
										   # Battered Shell is 230%. Same 3s cooldown,
										   # so only the damage differs
			("Stormfire", 1.0),            # off Seal of Destruction, no cooldown
										   # of its own so the press is the rate
		],
		"hits/s":4,
		"blocks/s":1.5,
		# STUB, and for a retribution build it is the most consequential number
		# in the file: retaliation fires off being hit, so this is its rate the
		# way attacks/s is the rotation's. It defaults to 1 and at 1 retaliation
		# is 54% of what he deals; at 2 it is 70%, at 3 it is 78%. A shield tank
		# standing in a pack is being hit rather more than once a second.
		# "hits taken/s":2,
		"kills/s":1,
		# crit chance was pinned here. It is derived now, from offensive
		# ability against the enemy defence that level and difficulty give -
		# so it tracks the sheet instead of going stale against it.
		"low healths/s":1.0/30, # total guesswork.

		"physique":1000,  # derived 1061 +14%
		"cunning":475,  # derived 409 -11%
		"spirit":400,  # derived 436 +23%

		"offense":2000,  # derived 1991.9 +12%
		"defense":2400,  # derived 2106.9 -11%


		"armor":2650,  # derived 949.57 -62%

		"energy":2000,  # derived 2422 +21%
		"energy/s":18,  # derived 7.7 -45%

		"physical %":400, "physical":900,  # derived physical % 8 -98%, physical 71.5 -60%
		"internal %":400, "internal":1,  # derived internal % 8 -98%
		"fire %":1300, "fire":1600,  # derived fire % 598 -44%, fire 40 -71%
		"burn %":1000, "burn":500,  # derived burn % 518 -31%
		"lightning %":850, "lightning":69,  # derived lightning % 362 -46%, lightning 52 +717%
		"electrocute %":650, "electrocute":1,  # derived electrocute % 362 -32%
		"chaos %":450, "chaos":1,  # derived chaos % 75 -83%

		"physical retaliation": 6000,  # derived 813 -86%
		"fire retaliation": 15000,  # derived 644.5 -96%
		"lightning retaliation": 8000,  # derived 1056 -87%

		"all retaliation %":831,

		"fight length":30,

		"playStyle":"tank",
		"weapons":["sword", "shield"],
		"blacklist":[
			# manticore, manticoreAcidSpray# I'm not sure it makes sense in this build. Not many attacks to bind it to and the stats on the constellation aren't that good.
		]
	}

# What every damage type is worth, in one place. This one names none of
# them individually: "damage" is the priority for everything not named,
# and it was the weight of the same name until damage numbers were
# gathered here. A block that names nothing else divides by one, so it
# means exactly what it meant as a weight.
damagePriority = {
		# Derived from the rotation rather than stated. He deals 62% fire, 18%
		# physical, 16% burn, 2% internal, 2% lightning - which nothing in this
		# file said before: every damage weight came from a bare "damage": 1
		# catch-all, so fire and internal were priced the same way.
		#
		# 15 is what his largest damage weight was before this, so the rest of
		# the model keeps its scale. Name a type beside it to lean.
		"rotation": 15,
	}

weights = {
		# "attack opportunity cost" was -100 and "weapon damage %" 7.5, both
		# hand-set and both now derived - the second is his flat damage pool
		# over what actually delivers it, and the first is one delivery of it.
		# The -100 is in fenris and lochlan too and reads as copied rather than
		# chosen.
		"attack speed":10,
		"cast speed":7.5,
		
		"energy":.75,
		"energy absorb": 15,

		"health": .66,

		"armor": 5-1.5, 
		"armor absorb": 20,
		
		"damage absorb %":100,

		"defense": 7.5, # "defense %": ,
		
		"resist": 15,
		
		"physical resist":35,
		"pierce resist":0,
		
		"fire resist":0, 
		"lightning resist":0,
		"cold resist":0,
		"acid resist":5,
		"chaos resist":0,
		"vitality resist":0,
		"aether resist":25,


		"block %": 100,
		"blocked damage %":50-10,
		"shield recovery":75,

		"offense": 12.5, # "offense %": ,

		# Twelve damage weights were here - physical, fire, burn and lightning
		# with their triggered and percentage forms - and every one of them beat
		# the derivation above, because a stated weight wins. So "rotation": 15
		# was reading his bar, working out that he deals 62% fire and 3%
		# lightning, and then being ignored for exactly the types he deals.
		# The hand-set numbers had lightning level with burn at a sixth of its
		# damage, which is the sort of thing deriving them is for.
		#
		# "burn duration" stays: it is not a split of anything the rotation
		# deals, so nothing derives it and it really is a preference.
		"burn duration":5,

		# "crit damage": ,
		"damage reflect %": 35,
		# "retaliation" 7 and "retaliation %" 15 were here. Both are derived
		# now, off the flat retaliation on the sheet and the 831% that
		# multiplies it, at the rate he is hit - which is what makes them
		# comparable with the attack weights rather than a separate guess
		# beside them.
		
		"stun %":-5,

		"lifesteal %":20,
		"move speed": 10,

		"Acid Spray":.75,
	}


  # Solution([xA, xO, lion, xC, fiend, viper, hound, quill, phoenix, messenger, behemoth, hawk, torchMeteorShower, ultosHandofUltos, targoShieldWall], self),  # 58044 (57)
  # Solution([xA, xO, lion, xC, fiend, viper, raven, hound, phoenix, messenger, behemoth, hawk, torchMeteorShower, ultosHandofUltos, targoShieldWall], self),  # 57868 (57)
  # Solution([xA, xO, lion, xC, fiend, viper, hound, light, phoenix, messenger, behemoth, hawk, torchMeteorShower, ultos, targoShieldWall], self),  # 57830 (57)
  # Solution([xA, xO, lion, xC, fiend, viper, raven, hound, phoenix, messenger, behemoth, light, torchMeteorShower, ultosHandofUltos, targoShieldWall], self),  # 57656 (57)
  # Solution([xA, xO, lion, xC, fiend, viper, raven, light, lizard, phoenix, messenger, behemoth, torchMeteorShower, ultosHandofUltos, targoShieldWall], self),  # 57145 (57)
  # Solution([xE, hawk, xO, lion, xC, fiend, viper, hound, phoenix, behemoth, toad, messenger, torchMeteorShower, ultosHandofUltos, targoShieldWall], self),  # 57095 (57)
  # Solution([xO, lion, xC, fiend, viper, hound, quill, phoenix, behemoth, toad, messenger, torchMeteorShower, ultosHandofUltos, targoShieldWall], self),  # 56990 (57)
  # Solution([xO, lion, xC, fiend, viper, raven, hound, phoenix, behemoth, toad, messenger, torchMeteorShower, ultosHandofUltos, targoShieldWall], self),  # 56814 (57)
  # Solution([xE, hawk, xO, lion, xC, viper, wraith, shieldmaiden, messenger, behemoth, phoenix, crown, targo, ultosHandofUltos], self),  # 55767 (57)
  # Solution([xE, xO, lion, xP, imp, xC, fiend, behemoth, viper, phoenix, toad, messenger, torchMeteorShower, ultosHandofUltos, targoShieldWall], self),  # 55607 (57)
  # Solution([xE, quill, xO, lion, xC, viper, wraith, shieldmaiden, messenger, behemoth, phoenix, ultosHandofUltos, chariotWaywardSoul, targoShieldWall], self),  # 55497 (57)
  # Solution([xO, lion, xC, fiend, viper, quill, wraith, phoenix, shieldmaiden, messenger, crown, ultosHandofUltos, behemothGiantsBlood, targoShieldWall], self),  # 55452 (57)
  # Solution([xO, panther, wraith, lion, shieldmaiden, messenger, fiend, viper, raven, phoenix, ultosHandofUltos, obeliskStoneForm, targoShieldWall], self),  # 55450 (57)
  # Solution([xE, xO, lion, xC, fiend, viper, wraith, shieldmaiden, messenger, behemoth, phoenix, crown, ultosHandofUltos, targoShieldWall], self),  # 55317 (57)
  # Solution([xE, xO, lion, xC, viper, imp, shieldmaiden, behemoth, phoenix, owl, messenger, crown, ultosHandofUltos, targoShieldWall], self),  # 54990 (57)
  # Solution([xE, raven, xO, lion, xC, fiend, viper, hound, phoenix, shieldmaiden, wolverine, messenger, behemothGiantsBlood, ultosHandofUltos, targoShieldWall], self),  # 54938 (57)
  # Solution([xO, dryad, xC, fiend, viper, raven, hound, phoenix, wolverine, messenger, crown, ultosHandofUltos, behemothGiantsBlood, targoShieldWall], self),  # 53228 (57)
  # Solution([xO, panther, imp, lion, shieldmaiden, xC, fiend, phoenix, behemoth, wolverine, messenger, ultosHandofUltos, targoShieldWall], self),  # 52758 (57)
	