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
	"attacks/s": 2.0,            # attacks per second, as swung in practice
	"playStyle": "ranged",        # melee | shortranged | ranged | tank

	# Read off bots/gwyr.ahk, which is the rotation he actually plays, against
	# the cooldowns the skill records state. A skill fires no faster than its
	# cooldown and no faster than he presses it, so the rate is one over
	# whichever of the two is longer - and which one wins is different for
	# almost every line below.
	#
	#                     presses   cooldown   limited by
	#   Flashbang            3.0s       1s     the button
	#   Rune of Hagarrad     3.7s       4s     the cooldown
	#   Rune of Kalastor     3.7s       4s     the cooldown
	#   Inquisitor Seal      5.0s       5s     both, near enough
	#   Thermite Mine        5.0s       -      the button; the record states no
	#                                          cooldown at all, which is worth
	#                                          a look
	#   Mortar Trap         15.0s     2.5s     the button, by six times over
	#
	# The ones where the button wins are deliberate: a skill on a short cooldown
	# is not always worth spamming, which is what the script says about
	# Flashbang in as many words and what the 15s on Mortar Trap means too.
	#
	# Flashbang is the check on all of it: the script says "really 1 second"
	# beside it and the record agrees.
	"allAttacks/s": [
		2.0,      # Fire Strike, held on left button, so it runs continuously
		0.333,    # Flashbang         1/3.0
		0.25,     # Rune of Hagarrad  1/4
		0.25,     # Rune of Kalastor  1/4
		0.20,     # Inquisitor Seal   1/5
		0.20,     # Thermite Mine     1/5
		0.167,    # "gaze", key 9     1/6, cooldown unknown - which skill is it?
		0.067,    # Mortar Trap       1/15
	],

	# STUB - the ranks are placeholders and every damage weight is priced
	# against them. Left button held is the attack, and for a Demolitionist
	# holding down fire that is Fire Strike: 100% weapon damage, so his sheet's
	# 3000 flat fire is delivered in full every shot. The modifiers are the ones
	# that carry his fire and burn. Correct the numbers from the skill screen.
	"main attack": [("Fire Strike", 12), ("Explosive Strike", 12),
					("Brimstone", 12), ("Static Strike", 1)],

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
	"fire":10,
	"burn":10,
	"physical": 5,
	# STUB - both were falling through to the catch-all at 1, and both are
	# large on the sheet: 675 flat pierce at 625%, which for a gun is most of
	# what it fires, and the Inquisitor half of him is where the lightning
	# comes from. Priced at 1 they were worth 0.65 and 0.64 a point against
	# fire's 11.71. These two numbers are guesses at how much he cares; the
	# split between flat and percent is not.
	"pierce": 5,
	"lightning": 2,
	"damage":1,
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
