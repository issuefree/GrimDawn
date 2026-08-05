# Gwyr - devotion model.
#
# stats   = your character sheet, as the game reports it.
# weights = how much a point of each stat is worth to you. Relative values are
#           all that matter; scale is arbitrary. Start rough and refine.
#
# Only attacks/s and playStyle are required. Everything else is optional -
# add sheet numbers as you care about them. Unknown keys are reported on load.

# python gwyr/gwyr.py [--budget 30] [--seeds 10] [--exhaustive]
# Exits here rather than falling through; see devotion.runModelFile for why.
if __name__ == "__main__":
	import os, sys
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	import devotion
	sys.exit(devotion.runModelFile(__file__))

devotionPoints = 41

stats = {
	# Attack Speed off the sheet. It is what the held attack runs at, what a
	# damage over time is refreshed at, and the rate every attack-triggered
	# proc fires off.
	"attacks/s": 2.43,
	"playStyle": "ranged",        # melee | shortranged | ranged | tank

	# His rotation, read off bots/gwyr.ahk, which is a machine-readable
	# statement of how he actually plays. Each entry is the skill and its rank,
	# and where he presses a button slower than the skill recharges, the
	# interval he presses at - because a skill fires no faster than its
	# cooldown and no faster than you press it.
	#
	# The cooldowns come from the game rather than from here, so the rates are
	# printed on load instead of being written down. Which constraint wins
	# differs almost every line, and where it is the button that wins it is
	# deliberate: a short cooldown is not always worth spamming. Flashbang is
	# the check on the lot - the script says "really 1 second" beside it and
	# the record says 1.
	#
	# Fire Strike is first because it is what he holds the left button down on,
	# which makes it his main attack and runs it at attacks/s above. The three
	# nested inside it are not buttons - they are the ones that carry his fire
	# and burn, and none of it is on the sheet.
	#
	# STUB - the ranks are placeholders and every damage weight is priced
	# against them. Correct the numbers from the skill screen.
	"rotation": [
		# Held, with the three that modify it nested inside: Explosive Strike
		# fires with it rather than on its own, and the other two are passives.
		("Fire Strike", 12, [("Explosive Strike", 12), ("Brimstone", 12),
							 ("Static Strike", 1)]),
		("Flashbang", 12, 3.0),
		("Rune of Hagarrad", 12),
		("Rune of Kalastor", 12),
		("Inquisitor Seal", 12),
		("Thermite Mine", 12, 5.0),     # the record states no cooldown at all
		("Mortar Trap", 12, 15.0),
		# "gaze" on key 9 was a rate here. It is a devotion proc: it fires on
		# its own trigger and the devotion system already scores it, so a rate
		# in the rotation was counting it a second time as an attack source.
	],

	# STUB - nothing on the sheet says these and they are guesses in the shape
	# of a ranged character who kites. hits/s is hits he lands, which drives
	# every hit-triggered proc; hits taken/s is how often he is hit, which is
	# what armor is counted against.
	"hits/s": 4,
	"hits taken/s": 0.5,
	"low healths/s": 1.0/30,
	"blocks/s": 0,          # two-handed ranged, so this one is not a guess

	# Your level, and what you fight. Crit chance is derived from your offensive
	# ability against the enemy's defensive one using the game's own hit
	# formula, and enemy defence is derived from level - so stating "level" is
	# usually enough, and without it every crit-triggered proc scores zero.
	# Override "enemy defense" directly if you grind a difficulty whose scaling
	# the game's records do not carry. "enemy density" is enemies per square
	# metre and sizes every area proc.
	"level": 73,                  # from the save file, not transcribed
	"difficulty": "elite",        # normal | elite | ultimate
	# "enemy defense": 1400,        # overrides what level+difficulty derive
	# "enemy resist": 25,           # ditto, for every damage type at once
	# "enemy density": 0.03,

	"weapons": ["2h ranged"],   # omit to allow every constellation
	"physique": 950, "cunning": 550, "spirit": 450,
	"offense": 2082, "defense": 1900,
	"health": 8000, "health/s": 320, 
	"energy": 2500, "energy/s": 28,
	"armor": 900,
	# "fight length": 30,

	# Flat and % damage for the types you care about. damagePriority below
	# uses these to work out what a point of each is actually worth.
	"physical": 100, "physical %": 300,
	"pierce": 675, "pierce %": 625,
	"fire": 3000, "fire %": 1400,
	"lightning": 25, "lightning %": 625,
	"burn": 2000, "burn %": 1000, "burn duration": 200,
	"electrocute": 0, "electrocute %": 400, "electrocute duration": 50,
}

# One number per damage type saying how much you care about it. The flat vs %
# split is derived from the sheet above: with 69 flat lightning and 850%
# lightning, a flat point is worth ~14x a percentage point, and with no flat
# physical at all, "physical %" multiplies nothing. You should not have to work
# that out by hand, and hand-written weights usually get it wrong.
damagePriority = {
	# Derived from the rotation above rather than stated. What a build cares
	# about is what it deals, and the skills and their cooldowns say what that
	# is: 59% fire, 32% burn, 8% pierce, 1% physical, 0.3% lightning.
	#
	# The hand-written priorities this replaces had physical and pierce both at
	# 5 while physical is a ninth of pierce's damage, and fire and burn equal
	# while fire is nearly twice burn.
	#
	# 30 is what the largest weight comes out at, so the rest of the model does
	# not have to be rescaled. Name a type beside it to lean - "fire": 1.5 - for
	# something you want to build toward rather than already deal.
	"rotation": 30,
}

# How much of the solution should be keeping him alive, priced in effective
# health - see fenris for what the number means. sweepDefense() says:
#
#     0.1 -> 1%    0.3 -> 9%     0.6 -> 37%
#     0.2 -> 3%    0.4 -> 10%
#
# 0.4 for now, which is 10%. He kites at range and is not the one dying, so
# this is deliberately lower than fenris's 40% - and it is a stub like the rest
# of him. The step up to 37% is one constellation swapping in, not a slope.
defensePriority = 0.4

# Everything that is not damage or defence. Both of these are preferences with
# nothing to derive them from, and both are STUBS at the values every other
# model happens to use.
weights = {
	"offense": 5,
	"attack speed": 10,
	"move speed": 10,
}
