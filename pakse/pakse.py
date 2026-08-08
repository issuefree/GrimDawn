# python pakse/pakse.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))

devotionPoints = 28

# What is stated below is what the save gets wrong. Everything a model leaves
# out is filled in at load from the character's own save file - every worn item,
# its components, the set tiers and every point spent - so a stat written here
# is an override, and the comment beside it is what was derived. Anything the
# two agreed on to within 5% was deleted rather than annotated: it was a
# transcription of a number the code already had.
#
#     python savefile.py Pakse stats     what the save derives
#
stats = {
		# Character level. Enemy defence follows from it and from the difficulty,
		# and crit chance follows from that against your offensive ability - so
		# without it every crit-triggered proc scores zero. It also decides which
		# gear evalItemMods will show you.
		"level":65,
		# Which column of the difficulty table to read. It moves enemy
		# defence, and every enemy resistance by up to twelve points, so
		# it is not a detail. Taken from the level band; correct it if he
		# is grinding a difficulty he has out-levelled.
		"difficulty":"elite",
		"attacks/s":2,
		# His rotation, from bots/pakse.ahk against the cooldowns the records
		# state. A skill fires no faster than its cooldown and no faster than
		# it is pressed, so the rate is one over whichever is longer; the load
		# prints which one won for each. The first entry is what he holds the
		# button down on, and it is his main attack. RANKS ARE STUBS.
		"rotation":[
			# What is on the bar and the order he plays it. Every line here was
			# a flat 12, which was a placeholder: he has one point in most of
			# them, off the save, and ten in Retribution - which is a modifier
			# on what he holds and now arrives as one, along with the eight
			# others that were written out here.
			"Righteous Fervor",            # held on left button
			("Aegis of Menhir", 0.5),
			("Judgment", 4.8),
			("Overguard", 5.0),
			("Ascension", 5.0),
			("War Cry", 7.5),
			"Smite",
			"Shattering Smash",
			"Zolhan's Technique",
			"Markovian's Advantage",
			("Shield Slam", 3.0),          # off Battered Shell
			("Blade Ward", 3.0),           # off Reinforced Shell; 12s cooldown
										   # wins, so the press does not matter
			# "stomp" and "dreegsGaze" on key 9 were a rate here. Both are
			# devotion procs: they fire on their own triggers and the devotion
			# system already scores them, so a rate here counted them twice.
		],
		"blocks/s":1,
		"hits/s":1.5, # assuming a non-trivial fight
		"kills/s":.5,
		# crit chance was pinned here. It is derived now, from offensive
		# ability against the enemy defence that level and difficulty give -
		# so it tracks the sheet instead of going stale against it.
		"low healths/s":1.0/30, # total guesswork.

		"physique":1000,  # derived 936 -6%

		"offense":1100,  # derived 1680.86 +53%
		"defense":1300,  # derived 1603.2 +23%

		"health":10000,  # derived 9074 -9%
		"health/s":133,  # derived 58.44 -56%

		"armor":1000,  # derived 698.25 -30%

		"energy":2000,  # derived 2246 +12%
		"energy/s":15,  # derived 0.8 -95%

		# "internal %":400, "internal":1,
		# "fire %":1300, "fire":1600,
		# "burn %":1000, "burn":500,
		# "lightning %":850, "lightning":69,
		# "electrocute %":650, "electrocute":1,
		# "chaos %":450, "chaos":1,
		"acid":500,  # derived 38 -92%

		"retaliation %":500,  # derived 393 -21%

		"fight length":15,

		"playStyle":"tank",
		"weapons":["sword", "axe", "mace", "dagger", "shield"],
		"blacklist":[
			"bonds"  # for pet builds
		]
	}

# What every damage type is worth, in one place. This one names none of
# them individually: "damage" is the priority for everything not named,
# and it was the weight of the same name until damage numbers were
# gathered here. A block that names nothing else divides by one, so it
# means exactly what it meant as a weight.
damagePriority = {
		# Derived from the rotation rather than stated. He deals 66% acid, 17%
		# physical, 15% internal, 2% fire - which is worth reading twice, since
		# nothing in this file suggested acid was two thirds of him. It comes
		# off the sheet's 500 flat acid at 500%, delivered by a weapon pool that
		# claims every one of his swings.
		#
		# 25 is what his largest damage weight was before this, so the rest of
		# the model keeps its scale. Name a type beside it to lean.
		"rotation": 25,
	}

weights = {
		# select the important bonuses from above and give them a value.
		# Note some bonuses will be automatically calculated if left blank (and should be unless you want to override):
		#	health/s <- health, health/s %, fight length
		#	energy/s <- energy, energy/s %, energy length

		#   physique <- health/s, health, defense
		#   cunning <- appropriate damage %, offense
		#   spirit <- appropriate damage %, energy, energy/s

		#	perc stats ["physique", "cunning", "spirit", "offense", "defense", "health", "energy", "armor"]
		#		will be calculated from your stats settings and base (non perc) values

		#   resist reductions <- appropriate damage % stat and bonus
		#	crit damage <- uses damage % stats and weights and crit chance stat

		#   elemental damage and resist <- fire/cold/lightning damage and resist  (includes pets)
		#   all damage % -< all individual damage % (includes pets)
		
		#Note there are a few shorthand notations. An individual setting will override the shorthand setting:
		#	resist <- sets a value for all resist types
		#	pet resist <- sets a value for all pet resist types
		#	reduce resist <- sets a value for all resist reductions
		#	damage <- sets a value for all on hit damage types
		#	triggered damage <- sets a value for all ability triggered damage types
		#		note that if you don't set triggered damage it gets valued at on hit damage of the same type since triggered damage is (roughly) normalized in value to on hit damage
		#   retaliation <- sets a value for all retaliation damage types
		#   pet retaliation <- sets a value for all pet retaliation damage types

		"attack speed":5,
		"cast speed":5,
		
		"energy":.25,
		"energy absorb": 15,

		"health": .66,

		"armor": 3, 
		"armor absorb": 20,
		
		"damage absorb %":100,

		"defense": 5, # "defense %": ,
		
		"resist": 15,
		
		"physical resist":35,
		"aether resist":25,


		"block %": 100,
		"blocked damage %":50,
		"shield recovery":75,

		"offense": 12.5, # "offense %": ,

		# Nine damage weights were here - physical, acid and poison with their
		# triggered and percentage forms - and every one beat the derivation
		# above, because a stated weight wins. "rotation": 25 reads his bar and
		# works out that he deals 72% acid and 16% physical; the hand-set
		# numbers had physical at 10 against acid's 15, which is nothing like
		# that split.
		#
		# "poison duration" stays: it is not a split of anything the rotation
		# deals, so nothing derives it and it really is a preference.
		"poison duration":2,

		"damage reflect %": 35,
		# Kept, unlike armitage's, and the difference is the sheet. retaliation
		# is derived off flat retaliation per type times the percentage that
		# multiplies it - armitage states 6000 physical, 15000 fire and 8000
		# lightning, so his derives. This sheet states "retaliation %":500 and
		# no flat retaliation at all, so there is nothing for the 500% to
		# multiply and the derivation produces nothing. Dropping these two on
		# the assumption they were derived cost him 18181 of 47244, which is
		# what a retribution build looks like with its retaliation priced at
		# zero.
		#
		# Transcribe his flat retaliation per type and these can go the way
		# armitage's did.
		"retaliation": 15,
		"retaliation %": 25,

		"lifesteal %": 20,
		"move speed": 10,
	}

