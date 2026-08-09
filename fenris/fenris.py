# python fenris/fenris.py [--budget 30] [--seeds 10] [--exhaustive]
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
# A stated stat has the constellations already taken subtracted from it at load,
# because the sheet is read in town with them on and the optimiser is choosing
# them - so a value here can sit above the derived figure beside it by exactly
# what a devotion grants, and that is not a discrepancy.
#
#     python savefile.py Fenris stats     what the save derives
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
		"difficulty":"normal",
		# Attack Speed off the sheet. It is what the held attack runs at, what a
		# damage over time is refreshed at, and the rate every attack-triggered
		# proc fires off.
		"attacks/s":1.64,
		# His rotation, from bots/fenris.ahk against the cooldowns the records
		# state. A skill fires no faster than its cooldown and no faster than
		# he presses it, so the rate is one over whichever is longer, and the
		# load prints which one won for each.
		#
		# Feral Claws is first, which is what the left button holds down: it
		# runs at attacks/s and it is his main attack. The rest are buttons on
		# the bar, including the two buffs, since a devotion can be bound to a
		# buff as readily as to an attack.
		#
		# The three nested inside Feral Claws are not buttons and never fire on
		# their own - they change what it swings for. Between them they carry
		# its 110% weapon damage, which is why the flat damage on the sheet
		# below is not decoration, and 117 pierce, which is what the 200% pierce
		# below has to multiply: none of it is on the sheet.
		#
		# RANKS ARE STUBS at 8 except Werewolf, Voracity and Recklessness, and
		# Feral Claws, which are real.
		"rotation":[
			# Held; the Werewolf form's attack. Werewolf is named because it is
			# the one link the records do not carry - nothing in the naming ties
			# a form to the attack it grants, so it has to be said. Voracity and
			# Recklessness then arrive on their own, by modifying Werewolf.
			#
			# Everything else here is just what is on the bar: the ranks are the
			# points he has spent, off the save.
			("Feral Claws", ["Werewolf"]),
			("Brutal Slam", 1.0),          # off Severed Claw. Chipped Claw's
										   # plain "Slam" is the weaker version
										   # and has the same 2s cooldown, so
										   # only its damage would differ
			("Curse of Frailty", 2.5),
			"Leap",
			("Bonechilling Cry", 3.0),
			("Blood of Dreeg", 3.0),
			"Rip and Tear",
			("Rallying Cry", 4.0),
		],

		"hits/s":4,
		"blocks/s":0,   # no shield, so the block-triggered procs really are worth nothing
		"low healths/s":1.0/30, # total guesswork.



		"health":6000,  # derived 5173 -13%

		"armor":500,  # derived 316.29 -37%

		"energy":1500,  # derived 1836 +22%
		"energy/s":14,  # derived 2.5 -82%

		"physical %":350,  # derived 219 -30%
		"pierce %":200, "pierce":0,  # derived pierce % 100 -50%
		"bleed %":650, "bleed":1500,  # derived bleed % 340 -31%
		"chaos %":350, "chaos":400,  # derived chaos % 114 -67%, chaos 12 -86%

		"fight length":30,

		"playStyle":"melee",
		# "weapons":["sword", "axe", "dagger", "mace", "scepter", "spear", "twohand"],
		"blacklist":[
			# manticore, manticoreAcidSpray# I'm not sure it makes sense in this build. Not many attacks to bind it to and the stats on the constellation aren't that good.
		]
	}

# Derived from the rotation rather than stated. He deals 66% bleed, 23%
# physical, 9% chaos, 2% pierce - against hand-written priorities of 15, 5, 15
# and 10, which had chaos level with bleed while dealing a seventh of it, and
# pierce second-highest while dealing a fiftieth.
#
# The bleed is that large because Voracity puts a bleed on the Werewolf form
# and his sheet carries 1500 flat of it. It is still discounted for refreshing
# - he swings three times a second against a three second bleed - which is why
# his flat bleed weight stays modest while his bleed % does not.
#
# 13 is what his largest damage weight was before this, so the rest of the
# model keeps its scale. Name a type beside it to lean.
damagePriority = {
		"rotation":13,
	}

# How much of what the solution buys should be keeping him alive. One number,
# because what a point of armor is worth against a point of health is not a
# preference - it follows from the sheet, the same way the flat-versus-percent
# damage split does. Only the scale is a choice.
#
# Everything is priced in effective health: how much more damage he can take
# before dying, per point of the stat, so health is 1 by definition and the
# rest are quoted against it. At 0.28 that comes out as
#
#     health          0.28      armor absorb   21
#     armor            2.9      avoid melee    17
#     defense          1.1      avoid ranged   17
#
# 0.28 buys 40% of the solution defensive - sweepDefense() in the sandbox is
# how that was found, and it shows why it cannot just be asked for:
#
#     0.22 -> 8%     0.28 -> 40%     0.6 -> 78%
#     0.25 -> 9%     0.30 -> 42%     1.0 -> 95%
#
# Nothing between 9% and 40% is reachable. Twenty points buys five
# constellations and each is in or out, so the share steps rather than slides.
defensePriority = 0.28

weights = {
		# "attack opportunity cost" was -100 and is derived now, at -30.71 -
		# one swing, which is what pressing a granted skill costs. The -100 is
		# in armitage and lochlan too and looks like a number that was copied
		# rather than chosen; state it here if he really does value a swing at
		# three times what it is worth.
		#
		# "weapon damage %" was 7.5 and derives at 22.71: one percent of the
		# flat damage on the sheet, over the 3.8 weapon deliveries a second
		# his rotation makes - not over his 1.64 attacks, which counted a
		# percentage point at more than twice what it delivers.
		"attack speed":10,

		# not a split of anything, so not a priority
		"bleed duration":5,


		"lifesteal %":33,
		"move speed": 10,

	}
