# python fenris/fenris.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))

devotionPoints = 20

stats = {
		# Character level. Enemy defence follows from it and from the difficulty,
		# and crit chance follows from that against your offensive ability - so
		# without it every crit-triggered proc scores zero. It also decides which
		# gear evalItemMods will show you.
		"level":43,
		# Which column of the difficulty table to read. It moves enemy
		# defence, and every enemy resistance by up to twelve points, so
		# it is not a detail. Taken from the level band; correct it if he
		# is grinding a difficulty he has out-levelled.
		"difficulty":"normal",
		# Off the sheet - his Attack Speed, which is what one weapon swing
		# takes. Not a sum of everything he presses: that is what the rotation
		# below is for, and adding the two together counted his bar twice.
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
			# Held; the Werewolf form's attack, with the form itself and its two
			# passives nested inside, since all three modify what he swings.
			("Feral Claws", 8, [("Werewolf", 8), ("Voracity", 4),
								("Recklessness", 9)]),
			("Brutal Slam", 1.0),          # off Severed Claw. Chipped Claw's
										   # plain "Slam" is the weaker version
										   # and has the same 2s cooldown, so
										   # only its damage would differ
			("Curse of Frailty", 8, 2.5),
			("Leap", 8),
			("Bonechilling Cry", 8, 3.0),
			("Blood of Dreeg", 8, 3.0),
			("Rip and Tear", 8),
			("Rallying Cry", 8, 4.0),
		],

		"hits/s":4,
		"blocks/s":0,   # no shield, so the block-triggered procs really are worth nothing
		"low healths/s":1.0/30, # total guesswork.

		"physique":600,
		"cunning":600,
		"spirit":300,

		"offense":1250,
		"defense":1100,

		"health":6000,
		"health/s":50,

		"armor":500,

		"energy":1500,
		"energy/s":14,

		"physical %":350, "physical":750,
		"pierce %":200, "pierce":0,
		"bleed %":650, "bleed":1500,
		"chaos %":350, "chaos":400,

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
