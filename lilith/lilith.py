# python lilith/lilith.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))

devotionPoints = 45

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
#     python savefile.py Lilith stats     what the save derives
#
stats = {
		# Character level. Enemy defence follows from it and from the difficulty,
		# and crit chance follows from that against your offensive ability - so
		# without it every crit-triggered proc scores zero. It also decides which
		# gear evalItemMods will show you.
		# Which column of the difficulty table to read. It moves enemy
		# defence, and every enemy resistance by up to twelve points, so
		# it is not a detail. Taken from the level band; correct it if he
		# is grinding a difficulty he has out-levelled.
		"difficulty":"elite",
		# estimate how frequent combat events are for calculating dynamic stats and abilities
		"attacks/s":2,
		"rotation":[
			# Bare rates: nothing here is named, so no main attack is read and
			# every granted skill is priced against a bare 100% swing. Name the
			# skills and their ranks and both come out of the skill data.
			# 9, # skeletons (1 per skeleton)
			# 1, # zombie
			# 1, # raven
			2, #curse can spam
			1/5.8, #reap 1 target
			2/2.9, #bone harvest ~2 targets
			2*.15, # reaping strike
			2*.15, # necrotic edge
		],
		"hits/s":.33,
		"blocks/s":0,
		"kills/s":.25,
		# crit chance was pinned here. It is derived now, from offensive
		# ability against the enemy defence that level and difficulty give -
		# so it tracks the sheet instead of going stale against it.
		"low healths/s":.075, # total guesswork.

		"fight length":20, # average length of a fight... this is for weighting abilities and over time effects. If you rely on wearing down opponents this should be long. If you are a glass cannon this should be small.

		# estimated sheet stats for target level


		"health":9834,  # derived 7984 -16%
		"health/s":88.38,  # derived 77.48 -12%
		"health/s %":0,

		"energy":6019/2,  # derived 4376 +45%
		"energy/s":52.12,  # derived 4.8 -91%
		"energy/s %":0,

		"armor":1199,  # derived 909.18 -24%
		
		# estimated damage % for target level. add whatever damages are important to your build
		"aether %":300, # sheet % damage for important damage types.  derived 73 -76%
		"physical %":230,
		"vitality %":400,  # derived 204 -49%
		"vitality decay %":200,  # derived 79 -60%
		"chaos %":400,  # derived 170 -58%

		"pet damage %":1241,

		"playStyle":"shortranged", # playstyle for weighting constellation abilities. [ranged/shortranged/melee/tank]
		"weapons":[
			"rifle"
		],
		"blacklist":[
			# list of constellations that I want to manually exclude for some reason.
		]	
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

		"cast speed":2.5, 
		"move speed":7.5, 

		"armor":.2,
		"health":.2,
		
		"resist":1,
		"vitality resist":0,
		"fire resist":0,
		"cold resist":0,
		"lightning resist":0,
		"acid resist":0,
		"pierce resist":2.5,
		"chaos resist":2.5,
		"bleed resist":0,
		"aether resist":0.5,
		"physical resist":25,

		"defense":.5,

		"avoid melee":15,
		"avoid ranged":25,

		"offense":1,

		"energy":.1,

		"stun %":3,
		"slow move":3,

		"pet damage":15,

		# "pet all damage %":25, 
		"pet vitality %":7.5,
		"pet physical %":10,
		"pet fire %":5,
		"pet lightning %":5,
		"pet chaos %":2.5,
		"pet acid %":5,
		"pet poison %":1,
		"pet burn %":1,

		"pet attack speed":25,
		"pet defense":4,
		"pet defense %":7.5,
		"pet health %":15, 
		"pet health/s %":2.5, 
		"pet health/s":7.5, 
		
		"pet resist":1.5,
		"pet fire resist":0,
		"pet cold resist":0,
		"pet lightning resist":0,
		"pet poison resist":2,
		"pet pierce resist":2,
		"pet bleed resist":2,		

		"pet lifesteal %":15, 
		"pet offense":5,
		"pet offense %":50, 
		"pet crit damage":10,

		"pet retaliation":2.5,
		"pet retaliation %":5, 
		
		"pet move speed":10,		
		"pet total speed":30, 

		"physical %":.5,
		"aether %":.75,
		"vitality %":.75,
		"chaos %":.75,
		"vitality decay %":.75,

		"triggered damage":1,
		"triggered vitality":1.5,
		"triggered vitality decay":1.5,
		"triggered aether":1.5,
		"triggered chaos":1.5,

		"reduce defense":2,
		"slow move":5,

		"total speed":15,

		"Bysmiel's Command":2.5, #hard skills to keep active 100%, bonus due to it being a summon
		"Raise the Dead":0, #summons scale with player damage not pet damage so they won't be very good
		"Living Shadow":0,

		"Aetherfire":4.5, #this can be tied to skeletons and has no recharge. This number is based on calculated effective since I can't put the pet attacks in allAttacks/s since it will over value things that can't be tied to pets.
		"Flame Torrent":4.5,
		"Eldritch Fire":4.5,
		"Wendigo's Mark":4.5,
		"Guardian's Gaze":3,
		"Twin Fangs":2.5,
		"Rattosh":4.5,



	}

