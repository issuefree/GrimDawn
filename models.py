import os

import devotionderive
from dataModel import *
from constellationData import *
from utils import *
from solution import *

# What one point of cunning is worth, from the game's own numbers rather than
# rounded by hand - and used on both sides, so what a point is worth to score
# and what it has already given the sheet cannot drift apart.
CUNNING_DAMAGE = 1 / 245.0 * 100      # physical and pierce %
CUNNING_DURATION = 1 / 215.0 * 100    # bleed and internal trauma %
CUNNING_OFFENSE = 0.5                 # offensive ability
CUNNING_HEALTH = 1.0                  # health
# Physique: health, health regen beyond the base 50, defensive ability.
PHYSIQUE_HEALTH = 2.5
PHYSIQUE_REGEN = 1 / 25.0
PHYSIQUE_DEFENSE = 0.5
# Spirit: health, energy, energy regen flat and percentage, and the magical
# damage types - 1/215 for direct, 1/200 for the durations.
SPIRIT_HEALTH = 1.0
SPIRIT_ENERGY = 2.0
SPIRIT_REGEN = 0.01
SPIRIT_REGEN_PERCENT = 0.25
SPIRIT_DAMAGE = 1 / 215.0 * 100
SPIRIT_DURATION = 1 / 200.0 * 100

# All six constants above are the game's, and records/game/combatformulas.dbr
# says so in as many words: physicalDamageEquation divides dexterity by 245,
# physicalDurationDamageEquation by 215, magicalDamageEquation by 215,
# magicalDurationDamageEquation by 200, and both offensiveAbilityEquation and
# defensiveAbilityEquation take half of the attribute. Nothing here is fitted.

# Hitting is the record's. normalPTHEquation is probabilityToHit/70, so PTH
# under 70 is your chance to land the blow at all and 70 is certainty.
PTH_HIT_THRESHOLD = 70.0

# Critting is measured, because the record does not say it. Two readings off a
# level 34 training dummy on Elite, same character, gear swapped between them:
#
#     offensive ability 846   PTH 105.6   5.3% critical
#     offensive ability 1250  PTH 118.5  17.7% critical
#
# Fitting crit = (PTH - T)/W to those two, with nothing assumed, returns
# T = 100.1 and W = 103.8. So PTH reads as a percentage where 100 is an
# ordinary hit and every point above it is a point of critical chance.
#
# The pthThreshold ladder in the record - 70/90/105/120/130/135 paying
# 1.0/1.1/1.2/1.3/1.4/1.5 - is not this. It sizes the damage bonus once a
# critical happens, and two earlier guesses that it also gated the chance
# (at 70, then at 90) predicted 40.8% and 24.0% where the game said 17.7%.
# 100 appears nowhere in the record; it is here because it was measured twice.
PTH_CRIT_BASE = 100.0
PTH_CRIT_WINDOW = 100.0

# Difficulty scaling, which is not per-enemy at all: gameengine.dbr names
# records/game/balancingadjustment_mp+difficulty_enemies01.dbr as the
# monsterAttributePak, and every field in it is twelve numbers - three
# difficulties by four player counts. Index 0/4/8 is Normal/Elite/Ultimate for
# a solo character, and characterLifeModifier reading +50/+320/+580% across
# those three is what confirms the layout.
DIFFICULTIES = ("normal", "elite", "ultimate")
DEFAULT_DIFFICULTY = "ultimate"
# Veteran is not a fourth band, it is a switch on the first one - the game says
# so itself: "Veteran Mode enhances Normal Difficulty ... Can be toggled on/off
# in the main menu at any time", and Elite is "for characters that have
# completed Normal / Veteran". The pak has three columns and Veteran reads the
# Normal one. What it raises is monster level and density, and level is a stat
# of its own here.
DIFFICULTY_ALIAS = {"veteran": "normal"}

# characterDefensiveAbility and characterDefensiveAbilityModifier from the pak,
# which apply on top of whatever the enemy's own record says.
DIFFICULTY_DEFENSE = {"normal": (35.0, -15.0), "elite": (60.0, -8.0),
					  "ultimate": (75.0, -8.0)}
DEFENSE_PER_LEVEL = 12.0     # defensiveAbilityEquation: characterLevel * 12
DEFENSE_BASE = 53.0          # and its trailing + 53

# Resistance the enemy is assumed to have, per damage type, as a percentage.
# Nothing in the database states a resistance equation - the shield line in
# combatformulas.dbr, damage * ((100 - absorption) / 100), is the convention the
# engine uses everywhere, and resistance is the same plain multiplier with no
# floor at zero. So what a point of resist reduction buys depends only on what
# the enemy already resists, and both halves of that are measured.
#
# What the enemy's own record carries: the mean over the 2570
# Common/Champion/Hero/Boss records with a charLevel.
ENEMY_RESIST_BASE = {
	"vitality": 19.2, "cold": 16.7, "pierce": 16.5, "fire": 15.3,
	"lightning": 14.6, "acid": 14.2, "physical": 14.1, "aether": 13.1,
	"chaos": 11.9, "bleed": 0.0, "life leech": 0.0,
}
# What the difficulty adds on top, from the same monsterAttributePak. Nothing
# is resisted any better on Normal than the record says; Elite and Ultimate are
# where it comes from, and it is not uniform - lightning and acid gain three
# times what physical does.
DIFFICULTY_RESIST = {
	"physical":   {"normal": 0.0, "elite": 0.0, "ultimate": 2.0},
	"pierce":     {"normal": 0.0, "elite": 2.0, "ultimate": 5.0},
	"fire":       {"normal": 0.0, "elite": 4.0, "ultimate": 8.0},
	"cold":       {"normal": 0.0, "elite": 2.0, "ultimate": 5.0},
	"lightning":  {"normal": 0.0, "elite": 6.0, "ultimate": 10.0},
	"acid":       {"normal": 0.0, "elite": 6.0, "ultimate": 10.0},
	"vitality":   {"normal": 0.0, "elite": 6.0, "ultimate": 12.0},
	"aether":     {"normal": 0.0, "elite": 2.0, "ultimate": 5.0},
	"chaos":      {"normal": 0.0, "elite": 2.0, "ultimate": 5.0},
	"bleed":      {"normal": 0.0, "elite": 5.0, "ultimate": 9.0},
	"life leech": {"normal": 35.0, "elite": 45.0, "ultimate": 65.0},
}
# Duration damage has no resistance of its own - the pak carries no
# defensiveSlowFire, defensiveSlowPoison or the like, because the game resists
# each by its parent element. Bleeding is the exception and has its own field,
# which is why it appears above rather than here.
RESISTED_AS = {
	"burn": "fire", "frostburn": "cold", "electrocute": "lightning",
	"poison": "acid", "vitality decay": "vitality", "internal": "physical",
	"elemental": "fire",
}
DEFAULT_ENEMY_RESIST = 0.0


def difficultyOf(model):
	"""Which column of the pak to read. Unrecognised names are caught by
	modelspec.validate rather than quietly becoming the default here - reading
	the wrong column moves both enemy defence and every resistance."""
	stated = str(model.getStat("difficulty") or DEFAULT_DIFFICULTY).lower()
	stated = DIFFICULTY_ALIAS.get(stated, stated)
	return stated if stated in DIFFICULTIES else DEFAULT_DIFFICULTY


def enemyResist(model, damage):
	"""What the enemy resists this damage type by, in percent.

	An explicit "enemy <type> resist" wins, then a blanket "enemy resist", then
	the record base plus whatever the difficulty adds.
	"""
	stated = model.getStat("enemy %s resist" % damage)
	if stated:
		return float(stated)
	stated = model.getStat("enemy resist")
	if stated:
		return float(stated)
	parent = RESISTED_AS.get(damage, damage)
	return (ENEMY_RESIST_BASE.get(parent, DEFAULT_ENEMY_RESIST)
			+ DIFFICULTY_RESIST.get(parent, {}).get(difficultyOf(model), 0.0))


def enemyDefense(level, difficulty):
	"""Defensive ability of a level-appropriate enemy, from the game's equation.

	defensiveAbilityEquation is (base + level*12 + strength*0.5) * (1 + mod/100)
	+ 53. Almost every enemy record leaves its own base and strength at zero, so
	what is left is the level term and the difficulty's contribution to both the
	flat part and the modifier.
	"""
	flat, modifier = DIFFICULTY_DEFENSE.get(difficulty, DIFFICULTY_DEFENSE[DEFAULT_DIFFICULTY])
	return (flat + float(level) * DEFENSE_PER_LEVEL) * (1 + modifier / 100.0) + DEFENSE_BASE


def resistReductionValue(enemyResistPercent):
	"""Extra damage one flat point of resist reduction buys, as a fraction.

	Damage is base * (1 - R/100) and R goes negative freely, so dropping R by
	one point multiplies damage by (101 - R)/(100 - R) - a gain of 1/(100 - R).
	Against an unresisting enemy that is exactly 1% per point, and it climbs
	from there: 1.18% at the 15% an average enemy carries, 2% at 50%.

	The .0075 this replaces was measured off a training dummy and came out
	below the value at zero resistance, which the formula cannot produce for
	any enemy that resists anything at all. The likely cause is that resist
	reduction of the same kind does not stack - only the largest source counts
	- so a second source added to one already running measures as worth much
	less than the first.
	"""
	return 1.0 / (100.0 - float(enemyResistPercent))


def percentReductionValue(enemyResistPercent):
	"""Same, for one point of the '% reduced target's resistance' kind.

	A different mechanic wearing a similar name. Viper's 20 does not subtract
	20 points, it takes a fifth off whatever the enemy has - so it is worth
	R/100 of a flat point, and nothing whatsoever against an enemy at zero.
	At the 15% an average enemy carries, a point of it is worth about a
	seventh of a flat point.

	Unaffected by the crit threshold correction; this reads resistance, not PTH.
	"""
	return resistReductionValue(enemyResistPercent) * float(enemyResistPercent) / 100.0


def probabilityToHit(offense, enemyDefense):
	"""Grim Dawn's PTH, off your offensive ability against an enemy's defensive.

	Copied from probabilityToHitEquation in records/game/combatformulas.dbr
	rather than fitted. Two terms, a ratio and a difference, blended 30/70.
	"""
	oa, da = float(offense), float(enemyDefense)
	if oa <= 0:
		return 0.0
	return ((((oa / ((da / 3.5) + oa)) * 300) * 0.3)
			+ (((((oa * 3.25) + 10000) - (da * 3.25)) / 100) * 0.7)) - 50


def critChance(offense, enemyDefense):
	"""Share of your hits that critical, as a fraction.

	    hit  = min(1, PTH/70)          crit = (PTH - 100)/100

	so PTH 70 to 100 always lands and never criticals, and 200 would critical
	every time. See PTH_CRIT_BASE for the two readings this comes off.

	The residual is small and points the same way both times: against the 484
	defensive ability the equation gives a level 34 dummy, this reads 0.3 and
	0.8 of a point high. Solving instead for the defensive ability that would
	make each reading exact gives 490 and 503 - agreeing with each other and
	with the equation to within 3%, which is where the residual lives. Nothing
	is fitted per character.

	It is very sensitive to the gap between the two abilities. morena criticals
	17.7% of the time at 1250 offensive ability, 5.3% at 846, and not at all
	below about 700.
	"""
	pth = probabilityToHit(offense, enemyDefense)
	return min(1.0, max(0.0, (pth - PTH_CRIT_BASE) / PTH_CRIT_WINDOW))


def hitChance(offense, enemyDefense):
	"""Share of your attacks that land at all. Certain once PTH reaches 70."""
	return min(1.0, max(0.0, probabilityToHit(offense, enemyDefense)) / PTH_HIT_THRESHOLD)


class Model:
	# ALL_DAMAGE_PERC="all damage %"				#increases all non-retaliation damage

	# flat damage (e.g. "acid") only affects weapon attacks and skills that have a weapon component
	# perc damage increases all damage of the type by: base*(sum(all perc damage increases))
	# duration damages stack from different sources but not from the same source.
		# i.e. if you have burn damage on your weapon that does 500 damage over 5 seconds but you hit every second
		# the actual damage delivered per hit will be 100 not 500

	# ACID="acid"	
	# ACID_PERCENT="acid %"
	# POISON="poison"								
	# POISON_PERC="poison %"
	# POISON_DURATION="poison duration"

	# ELEMENTAL="elemental"							#elemental damage is delivered as 1/3 cold, 1/3 fire, 1/3 lightning
	# ELEMENTAL_PERC="elemental %"					#increases all cold,fire,lightning damage by the perc

	# COLD="cold"
	# COLD_PERC="cold %"
	# FROSTBURN="frostburn"
	# FROSTBURN_PERC="frostburn %"
	# FROSTBURN_DURATION="frostburn duration"

	# FIRE="fire"
	# FIRE_PERC="fire %"
	# BURN="burn"
	# BURN_PERC="burn %"
	# BURN_DURATION="burn duration"

	# LIGHTNING="lightning"
	# LIGHTNING_PERC="lightning %"
	# ELECTROCUTE="electrocute"
	# ELECTROCUTE_PERC="electrocute %"
	# ELECTROCUTE_DURATION="electrocute duration"

	# PHYSICAL="physical"
	# PHYSICAL_PERC="physical %"
	# INTERNAL="internal"
	# INTERNAL_PERC="internal %"
	# INTERNAL_DURATION="internal duration"

	# PIERCE="pierce"
	# PIERCE_PERC="pierce %"

	# BLEED="bleed"
	# BLEED_PERC="bleed %"
	# BLEED_DURATION="bleed duration"

	# AETHER="aether"
	# AETHER_PERC= "aether %"

	# CHAOS="chaos"
	# CHAOS_PERC="chaos %"

	# VITALITY="vitality"
	# VITALITY_PERC="vitality %"
	# VITALITY_DECAY="vitality decay"
	# VITALITY_DECAY_PERC="vitality decay %"

	# LIFE_LEECH="life leech"
	# LIFE_LEECH_PERC="life leech %"

	# TRIGGERED_ACID="triggered acid"
	# TRIGGERED_AETHER="triggered aether"
	# TRIGGERED_BLEED="triggered bleed"
	# TRIGGERED_BURN="triggered burn"
	# TRIGGERED_CHAOS="triggered chaos"
	# TRIGGERED_COLD="triggered cold"
	# TRIGGERED_ELECTROCUTE="triggered electrocute"
	# TRIGGERED_ELEMENTAL="triggered elemental"
	# TRIGGERED_FIRE="triggered fire"
	# TRIGGERED_FROSTBURN="triggered frostburn"
	# TRIGGERED_INTERNAL="triggered internal"
	# TRIGGERED_LIGHTNING="triggered lightning"
	# TRIGGERED_PHYSICAL="triggered physical"
	# TRIGGERED_PIERCE="triggered pierce"
	# TRIGGERED_POISON="triggered poison"
	# TRIGGERED_VITALITY="triggered vitality"

	# ACID_RESIST="acid resist"
	# AETHER_RESIST="aether resist"
	# BLEED_RESIST="bleed resist"

	# ARMOR="armor"
	# ARMOR_PERC="armor %"
	# ARMOR_ABSORB="armor absorb"
	# ARMOR_PHYSIQUE_REQUIREMENTS="armor physique requirements"
	# ATTACK_AS_HEALTH_PERC="attack as health %"
	# ATTACK_SPEED="attack speed"
	# ATTACK_SPEED_RETALIATION="attack speed retaliation"
	# AVOID_MELEE="avoid melee"
	# AVOID_RANGED="avoid ranged"
	# BLEED_RETALIATION="bleed retaliation"
	# BLOCK_PERC="block %"
	# BLOCKED_DAMAGE_PERC="blocked damage %"
	# CAST_SPEED="cast speed"
	# CHAOS_RESIST="chaos resist"
	# CHAOS_RETALIATION="chaos retaliation"
	# COLD_RESIST="cold resist"
	# CONSTITUTION_PERC="constitution %"
	# CRIT_DAMAGE="crit damage"
	# CUNNING="cunning"
	# CUNNING_PERC="cunning %"
	# CUNNING_RANGED_REQUIREMENTS="cunning ranged requirements"
	# DAMAGE_ABSORB="damage absorb"
	# DAMAGE_ABSORB_PERC="damage absorb %"
	# DAMAGE_BEAST_PERC="damage beast %"
	# DAMAGE_CHTHONICS_PERC="damage chthonics %"
	# DAMAGE_FROM_ARACHNIDS="damage from arachnids"
	# DAMAGE_FROM_BEASTS="damage from beasts"
	# DAMAGE_FROM_INSECTOIDS="damage from insectoids"
	# DAMAGE_FROM_UNDEAD="damage from undead"
	# DAMAGE_HUMAN_PERC="damage human %"
	# DAMAGE_REFLECT_PERC="damage reflect %"
	# DAMAGE_TO_CTHONICS="damage to cthonics"
	# DAMAGE_TO_UNDEAD="damage to undead"
	# DAMAGE_UNDEAD_PERC="damage undead %"
	# DEFENSE="defense"
	# DEFENSE_PERC="defense %"
	# DURATION="duration"
	# ELEMENTAL_RESIST="elemental resist"
	# ELEMENTAL_SHIELD="elemental shield"
	# ENERGY="energy"
	# ENERGY_PERC="energy %"
	# ENERGY_ABSORB="energy absorb"
	# ENERGY_BURN_PERC="energy burn %"
	# ENERGY_LEECH="energy leech"
	# ENERGY_LEECH_RESIST="energy leech resist"
	# ENERGY_REGENERATION="energy/s %"
	# ENERGY_PER_SEC="energy/s"
	# FIRE_RESIST="fire resist"
	# HEALTH="health"
	# HEALTH_PERC="health %"
	# HEALTH_REGENERATION="health/s %"
	# HEALTH_PER_SEC="health/s"
	# JEWELRY_SPIRIT_REQUIREMENTS="jewelry spirit requirements"
	# LIFE_LEECH_RESIST="life leech resist"
	# LIFE_LEECH_RETALIATION="life leech retaliation"
	# LIFESTEAL_PERC="lifesteal %"
	# LIGHTNING_RESIST="lightning resist"
	# MAX_ACID_RESIST="max acid resist"
	# MAX_AETHER_RESIST="max aether resist"
	# MAX_BLEED_RESIST="max bleed resist"
	# MAX_CHAOS_RESIST="max chaos resist"
	# MAX_FIRE_RESIST="max fire resist"
	# MAX_LIGHTNING_RESIST="max lightning resist"
	# MAX_PIERCE_RESIST="max pierce resist"
	# MAX_VITALITY_RESIST="max vitality resist"
	# MELEE_WEAPON_CUNNING_REQUIREMENTS="melee weapon cunning requirements"
	# MELEE_WEAPON_PHYSIQUE_REQUIREMENTS="melee weapon physique requirements"
	# MOVE_SPEED="move speed"
	# MOVE_SPEED_RETALIATION="move speed retaliation"
	# OFFENSE="offense"
	# OFFENSE_PERC="offense %"
	# PET_ACID="pet acid"
	# PET_ACID_RESIST="pet acid resist"
	# PET_AETHER_RESIST="pet aether resist"
	# PET_ALL_DAMAGE_PERC="pet all damage %"
	# PET_ATTACK_SPEED="pet attack speed"
	# PET_BLEED_RESIST="pet bleed resist"
	# PET_CHAOS_RESIST="pet chaos resist"
	# PET_CRIT_DAMAGE="pet crit damage"
	# PET_DEFENSE_PERC="pet defense %"
	# PET_ELEMENTAL_PERC="pet elemental %"
	# PET_ELEMENTAL_RESIST="pet elemental resist"
	# PET_FIRE_DAMAGE_PERC="pet fire damage %"
	# PET_HEALTH_PERC="pet health %"
	# PET_HEALTH_REGENERATION="pet health/s %"
	# PET_HEALTH_PER_SEC="pet health/s"
	# PET_LIFESTEAL_PERC="pet lifesteal %"
	# PET_LIGHTNING_DAMAGE_PERC="pet lightning damage %"
	# PET_MAX_ALL_RESIST="pet max all resist"
	# PET_OFFENSE_PERC="pet offense %"
	# PET_PHYSICAL="pet physical"
	# PET_PIERCE_RESIST="pet pierce resist"
	# PET_PIERCE_RETALIATION="pet pierce retaliation"
	# PET_POISON="pet poison"
	# PET_RETALIATION_PERC="pet retaliation %"
	# PET_TOTAL_SPEED="pet total speed"
	# PET_VITALITY_RESIST="pet vitality resist"
	# PHYSICAL_RESIST="physical resist"
	# PHYSICAL_RETALIATION="physical retaliation"
	# PHYSICAL_TO_CHAOS="physical to chaos"
	# PHYSIQUE="physique"
	# PHYSIQUE_PERC="physique %"
	# PIERCE_RESIST="pierce resist"
	# PIERCE_RETALIATION="pierce retaliation"
	# REDUCE_AETHER_RESIST="reduce aether resist"
	# REDUCE_ELEMENTAL_RESIST="reduce elemental resist"
	# REDUCE_LIGHTNING_RESIST="reduce lightning resist"
	# REDUCE_PHYSICAL_RESIST="reduce physical resist"
	# REDUCE_PIERCE_RESIST="reduce pierce resist"
	# REDUCE_DAMAGE_PERC="reduce damage %"
	# REDUCE_DEFENSE="reduce defense"
	# REDUCED_BLEED_DURATION="reduced bleed duration"
	# REDUCED_BURN_DURATION="reduced burn duration"
	# REDUCED_ELECTROCUTE_DURATION="reduced electrocute duration"
	# REDUCED_ENTRAPMENT_DURATION="reduced entrapment duration"
	# REDUCED_FREEZE="reduced freeze"
	# REDUCED_FREEZE_DURATION="reduced freeze duration"
	# REDUCED_FROSTBURN_DURATION="reduced frostburn duration"
	# REDUCED_POISON_DURATION="reduced poison duration"
	# REDUCED_STUN_DURATION="reduced stun duration"
	# REFLECTED_DAMAGE_REDUCTION="reflected damage reduction"
	# RETALIATION_PERC="retaliation %"
	# SHIELD_PHYSIQUE_REQUIREMENTS="shield physique requirements"
	# SHIELD_RECOVERY="shield recovery"
	# SKILL_COST_PERC="skill cost %"
	# SKILL_DISRUPTION_PROTECTION="skill disruption protection"
	# SLOW_MOVE="slow move"
	# SLOW_RESIST="slow resist"
	# SPIRIT="spirit"
	# SPIRIT_PERC="spirit %"
	# STUN_PERC="stun %"
	# STUN_DURATION="stun duration"
	# STUN_RETALIATION="stun retaliation"
	# TERRIFY_RETALIATION="terrify retaliation"
	# TOTAL_SPEED="total speed"
	# VITALITY_DECAY_RETALIATION="vitality decay retaliation"
	# VITALITY_RESIST="vitality resist"
	# WEAPON_DAMAGE_PERC="weapon damage %"
	# WEAPON_SPIRIT_REQUIREMENTS="weapon spirit requirements"

	def __init__(self, name, stats, bonuses, points):
		self.name = name
		self.stats = stats
		self.bonuses = bonuses
		self.points = points
		self.initialized = False

	@staticmethod
	def loadModel(name):
		import modelspec

		path = name.lower() + "/" + name.lower() + ".py"
		if not os.path.exists(path):
			raise FileNotFoundError(
				"No model at %s. Create one with:  python devotion.py --new %s" % (path, name))

		# Run the file against a copy of this module's globals so a blacklist can
		# name constellations. exec(src, locals()) only worked by accident of how
		# CPython caches the locals proxy, and left those names unresolvable.
		namespace = dict(globals())
		with open(path, "r") as handle:
			exec(handle.read(), namespace)

		missing = [k for k in ("devotionPoints", "stats", "weights") if k not in namespace]
		if missing:
			raise ValueError("%s does not define: %s" % (path, ", ".join(missing)))

		stats, weights = namespace["stats"], namespace["weights"]
		notes = modelspec.applyDefaults(stats)
		if namespace.get("damagePriority"):
			notes += modelspec.applyDamagePriority(stats, weights, namespace["damagePriority"])
		warnings = modelspec.validate(name, namespace["devotionPoints"], stats, weights,
									  namespace.get("damagePriority"))
		for note in notes:
			print("  note: " + note)
		for warning in warnings:
			print("  WARNING: %s: %s" % (path, warning))

		model = Model(name, stats, weights, namespace["devotionPoints"])
		# model.items = locals()["items"]
		# model.skills = locals()["skills"]
		# model.constellations = locals()["constellations"]
		model.initialize()
		# after initialize, so this only counts procs on constellations this
		# character was actually offered
		for warning in modelspec.unratedTriggers(stats):
			print("  WARNING: %s: %s" % (path, warning))
		return model

	# checkModel is NOT idempotent: it folds attribute-derived bonuses straight into
	# self.stats (physical %, pierce %, bleed %, internal %, the elemental/duration
	# damage types), so running it twice adds cunning/spirit scaling twice and
	# inflates every damage stat. loadModel() already initializes, so a second call
	# from startSearch() used to silently corrupt the model it was optimizing.
	def initialize(self, force=False):
		if self.initialized and not force:
			return
		self.initialized = True

		self.checkModel()
		self.filterConstellations()

		self.seedSolutions = []
		self.readSeedSolutions()

	def __str__(self):
		out = ""
		for key in sorted(self.bonuses.keys()):
			if self.get(key) > 0:
				out += key + " " + str(self.bonuses[key]) + "\n"
		return out

	def addSolution(self, solution):
		self.seedSolutions += [solution]
		self.seedSolutions = list(set(self.seedSolutions))
		self.seedSolutions.sort(key=lambda s: s.score, reverse=True)

	def saveSeedSolutions(self):
		os.makedirs(self.name.lower(), exist_ok=True)

		out = "self.seedSolutions = [\n"
		for s in sorted(self.seedSolutions, key=lambda s: s.score, reverse=True):
			out += "  Solution("+solutionPath(s.constellations)+ " self),  # " + str(int(s.score)) + " (" + str(s.cost) + ")\n"
		out += "]"
		with open(self.name.lower()+"/solutions.py", 'w') as file:
			file.write(out)

	def readSeedSolutions(self):
		path = self.name.lower()+"/solutions.py"
		try:
			with open(path, "r") as file:
				lines = file.read()
		except FileNotFoundError:
			self.saveSeedSolutions() # start a fresh seed file
			return

		# a malformed seed file used to be swallowed silently and look like "no seeds",
		# and was then overwritten with an empty list. Warn and leave the file alone.
		try:
			exec(lines)
			# dict.fromkeys dedupes like set() but keeps file order, so equal-scoring
			# seeds no longer land in a hash-dependent order on every run
			self.seedSolutions = sorted(dict.fromkeys(self.seedSolutions), key=lambda s:s.score, reverse=True)
		except Exception as e:
			print("  WARNING: could not read seed solutions from %s: %s: %s"%(path, type(e).__name__, e))
			print("  Leaving the file untouched; fix or delete it to continue seeding.")
			self.seedSolutions = []
			return

		# Seeds outlive the model that produced them. When gear changes,
		# filterConstellations() drops constellations this character can no longer
		# use, but the saved file still names them - so an unusable solution would
		# be re-scored as if valid, and its score would seed bestScore and prune
		# away legitimate ones. filterConstellations() has already run by now.
		usable = set(id(c) for c in Constellation.constellations)
		kept = []
		for s in self.seedSolutions:
			stale = [c for c in getattr(s, "constellations", []) if id(c) not in usable]
			if stale:
				print("  DISCARDING stale seed (no longer available: %s): %s"
					  % (", ".join(c.name for c in stale), solutionPath(s.constellations)))
			else:
				kept.append(s)
		self.seedSolutions = kept

		print("Reading seed solutions:")
		for s in self.seedSolutions:
			print("  " + str(s))

		self.saveSeedSolutions()


	def bonusToPercent(self, bonus):
		return (1+self.getStat(bonus)/100.0)

	def checkModel(self):
		print("Checking model...")
		print("  "+self.name)

		if not "allAttacks/s" in self.stats:
			self.stats["allAttacks/s"] = [self.stats["attacks/s"]]

		self.stats["allAttacks/s"].sort(reverse=True)

		# What your main attack swings for is a fact about your skill bar, not a
		# preference, and the generated skill data already knows it - name the
		# skill and the level and it is looked up. skillData is imported here
		# rather than at the top because it is six thousand lines and only a
		# model that names an attack needs it.
		if not self.getStat("main attack %") and self.getStat("main attack"):
			# One (skill, level) pair, or a list of them where the modifiers
			# that hang off the attack also carry weapon damage. Most do not -
			# Onslaught's Open Wounds and Endless Rage add bleed and a bleed
			# duration, not a bigger swing - but Blood Burst adds 85%, so the
			# list is worth accepting rather than assuming the base is all of it.
			stated = self.getStat("main attack")
			if stated and isinstance(stated[0], str):
				stated = [stated]
			import skillData                       # noqa: F401 - registers the skills
			total, named = 0, []
			for name, level in stated:
				skill = Skill.skills.get(name)
				if skill is None:
					print("  WARNING: no skill called %r - it adds nothing to 'main attack'" % name)
					continue
				part = skill.getAbility(level).gb("weapon damage %")
				total += part
				named.append("%s at %d%s" % (name, level, "" if part else " (+0)"))
			if named:
				self.stats["main attack %"] = total
				print("  main attack %%: %g  (%s)" % (total, ", ".join(named)))

		if not "fight length" in self.stats:
			self.stats["fight length"] = 30

		# What you fight is a question of what level you fight at and on which
		# difficulty; both come from the game's own equation and scaling table.
		if not self.getStat("enemy defense") and self.getStat("level"):
			difficulty = difficultyOf(self)
			self.stats["enemy defense"] = enemyDefense(self.getStat("level"), difficulty)
			print("  enemy defense: %.0f  (level %g on %s)"
				  % (self.stats["enemy defense"], self.getStat("level"), difficulty))

		# Crit chance follows from offensive ability against what you fight, so
		# derive it rather than making it a number to guess at. An explicit
		# "crit chance" still wins, the way an explicit weight beats a derived one.
		if "crit chance" not in self.stats and self.getStat("offense") and self.getStat("enemy defense"):
			oa, da = self.getStat("offense"), self.getStat("enemy defense")
			self.stats["crit chance"] = critChance(oa, da)
			print("  crit chance: %.3f  (offense %g vs enemy defense %g, PTH %.1f, hits %.0f%%)"
				  % (self.stats["crit chance"], oa, da, probabilityToHit(oa, da),
					 100 * hitChance(oa, da)))

		self.stats["criticals/s"] = getTriggerChance(self.getStat("crit chance"), self.getStat("attacks/s"))

		# /s stats can be calculated based on fight length and the value of the stat

		#1 health/s for a 30s fight is equal to... 30 health, consider the character's % regen stat
		#I'd like to perhaps give a boost to energy since it doesn't fast regen out of combat
		energyBonus = 2

		parts = ["health", "energy"]
		#calculate value of health/s and energy/s
		for part in parts:
			hps = self.get(part) * self.getStat("fight length") * self.bonusToPercent(part + "/s %")
			if part == "energy":
				hps = hps * energyBonus
			self.setCalculated(part+"/s", hps)
		
		#calculate value of health/s % and energy/s %
		#% health/s % affects ALL flat health regen EXCEPT for that gained from Physique.
		# regen from physique = (P-50)*.04

		# figure how much health/s 1 health/s % gives
		# the problem is that health/s is on the sheet as a total i.e. your health/s % is already factored in.
		# so I need to get the base value first			
		hpsP = (self.getStat("physique")-50)*.04
		hpsS = self.getStat("health/s")
		baseHps = (hpsS - hpsP)/self.bonusToPercent("health/s %")
		self.setCalculated("health/s %", baseHps*.01*self.get("health/s"))

		# physique grants health/s, health and defense so this should be accounted for
		val = 0
		val += self.get("health/s") * PHYSIQUE_REGEN
		val += self.get("health") * PHYSIQUE_HEALTH
		val += self.get("defense") * PHYSIQUE_DEFENSE   # the game gives .5, not .4

		self.setCalculated("physique", val)

		# One point of cunning is +1 health, +0.5 offensive ability, 1/245 of a
		# percent physical and pierce damage, and 1/215 of a percent bleed and
		# internal trauma. Pierce read .40 against physical's .41 where the game
		# gives both the same, offensive ability read .4 where the game gives
		# .5, and the health was missing.
		val = 0
		val += self.get("physical %") * CUNNING_DAMAGE
		val += self.get("pierce %") * CUNNING_DAMAGE
		val += self.get("bleed %") * CUNNING_DURATION
		val += self.get("internal %") * CUNNING_DURATION
		val += self.get("offense") * CUNNING_OFFENSE
		val += self.get("health") * CUNNING_HEALTH

		self.setCalculated("cunning", val)

		# spirit grants fire %, burn %, cold %, frostburn %, lightning %, electrocute %, acid %, poison %, vitality %, vitality decay%, aether %, chaos %, energy and energy regen
		val = 0
		# magicalDamage and magicalDurationDamage are the game's own groupings;
		# spelling them out here had quietly left life leech off the first list.
		val += sum([self.get(d + " %") for d in magicalDamage]) * SPIRIT_DAMAGE
		val += sum([self.get(d + " %") for d in magicalDurationDamage]) * SPIRIT_DURATION
		val += self.get("energy") * SPIRIT_ENERGY
		val += self.get("energy/s") * SPIRIT_REGEN
		val += self.get("energy/s %") * SPIRIT_REGEN_PERCENT
		val += self.get("health") * SPIRIT_HEALTH

		self.setCalculated("spirit", val)

		# update damage % stats
		self.stats["physical %"] = self.getStat("physical %") + self.getStat("cunning")*CUNNING_DAMAGE
		self.stats["pierce %"] = self.getStat("pierce %") + self.getStat("cunning")*CUNNING_DAMAGE
		self.stats["bleed %"] = self.getStat("bleed %") + self.getStat("cunning")*CUNNING_DURATION
		self.stats["internal %"] = self.getStat("internal %") + self.getStat("cunning")*CUNNING_DURATION

		# Spirit's share, on the same footing as cunning's above: unconditional.
		# It used to be skipped for any type the sheet left at zero, which meant a
		# damage type picked up from a devotion rather than from gear was scored
		# with no attribute scaling at all - morena has 200 spirit, which doubles
		# frostburn, and Tsunami's frostburn was counted as if she had none. The
		# cunning lines above never had that guard, so this is also the two
		# halves agreeing. 0.47 was a hand-rounded SPIRIT_DAMAGE; the constant
		# comes from the game's own magicalDamageEquation.
		for dam in magicalDamage:
			self.stats[dam + " %"] = self.getStat(dam + " %") + self.getStat("spirit")*SPIRIT_DAMAGE

		for dam in magicalDurationDamage:
			self.stats[dam + " %"] = self.getStat(dam + " %") + self.getStat("spirit")*SPIRIT_DURATION

		#check stats vs % stats
		percStats = ["physique", "cunning", "spirit", "offense", "defense", "health", "energy", "armor"]
		for stat in percStats:
			self.setCalculated(stat+" %", self.getStat(stat) * self.get(stat) / 100)

		# Resist reduction, from the game's multiplier rather than a fitted
		# constant. A point of it buys 1/(100 - enemyResist) more damage, which
		# is then worth that fraction of your whole damage multiplier - so it
		# converts into the same units as a point of "<damage> %".
		#
		# The /3 stays: resist reduction lands on one enemy where a damage
		# percentage applies to everything you hit, and most of it is a debuff
		# with a duration rather than something always on. That part is
		# judgement, not the game's arithmetic.
		SINGLE_TARGET_DISCOUNT = 3.0
		for damage in primaryDamages:
			if self.get(damage+" %") > 0:
				resist = enemyResist(self, damage)
				# pet sheet damage only counts "all damage %" so specific types are lost here
				totalDamagePerc = (self.getStat(damage+" %")+100) + (self.getStat("pet damage %")+100)
				worth = (totalDamagePerc * resistReductionValue(resist)
						 * self.get(damage+" %") / SINGLE_TARGET_DISCOUNT)
				self.setCalculated("reduce "+damage+" resist", worth)
				# "X% reduced target's resistance" takes a share of what the
				# enemy has instead of subtracting points, so it is worth
				# nothing against an enemy that resists nothing
				self.setCalculated("reduce "+damage+" resist %",
								   worth * resist / 100.0)

		self.setCalculated("reduce resist", sum([self.get("reduce "+b) for b in resists]))
		self.setCalculated("reduce resist %", sum([self.get("reduce "+b+" %") for b in resists]))

		elementals = ["fire", "cold", "lightning"]
		self.setCalculated("reduce elemental resist", sum([self.get("reduce "+b+" resist") for b in elementals]))
		self.setCalculated("reduce elemental resist %",
						   sum([self.get("reduce "+b+" resist %") for b in elementals]))

		# handle shorthand sets: resist	
		#resist types
		for b in resists:
			self.setIfNull(b, self.get("resist"))
			self.setIfNull("pet "+b, self.get("pet resist"))

		# elemental damage % and resist should be the sum of the individual components
		self.setCalculated("elemental %", sum([self.get(b) for b in ["cold %", "lightning %", "fire %"]]))

		# elemental resists are weird. e.g. fire resist protects against burn and elemental resist protects against fire but elemental resist does not protect against burn
		self.setCalculated("elemental resist", sum([self.get(b) for b in ["cold resist", "lightning resist", "fire resist"]]))

		# all damage should be >= all other damage bonuses (sans retaliation)
		# don't count cold, lightning, or fire as they're already aggregated under elemental
		parts = ["acid %", "aether %", "bleed %", "burn %", "chaos %", "electrocute %", "elemental %", "frostburn %", "internal %", "physical %", "pierce %", "poison %", "vitality %", "vitality decay %"]
		self.setCalculated("all damage %", sum([self.get(b) for b in parts]))

		self.setCalculated("pet all damage %", sum([self.get("pet " + b) for b in parts]))

		total = 0
		for damage in damages:
			total += (self.getStat(damage+" %")+100)*self.get(damage+" %")/100
		
		self.setCalculated("crit damage", total*self.getStat("crit chance"))

		for damage in damages:
			if damage in self.bonuses:
				self.setCalculated("triggered "+damage, self.bonuses[damage]/self.getStat("attacks/s"))

		#calculate elemental damage and triggered elemental damage if not set
		self.setCalculated("elemental", sum([self.get(elemental) for elemental in elementals])/3.0)
		self.setCalculated("triggered elemental", sum([self.get("triggered " + elemental) for elemental in elementals])/3.0)

		# Catch-all for a damage type the model never named. A point of flat X
		# is worth (1 + X%/100), because that is what it multiplies out to -
		# which is exactly how applyDamagePriority prices a type you did name,
		# so a named and an unnamed type are now on the same footing instead of
		# the unnamed one getting a flat number that ignored the sheet.
		#
		# It matters most for a damage type you only get from a devotion. It is
		# never on your gear, so it is never on the sheet, so there was nothing
		# to derive a priority from and it fell through to "damage" - and
		# frostburn on a build with 200 spirit is a x2 multiplier being scored
		# as x1.
		#
		# Retaliation is deliberately left flat: the game's own tooltip for it
		# says "% All Damage does not affect Retaliation damage", and a pet
		# scales off its own bonuses rather than yours.
		derived = []
		for damage in damages:
			# duration damage is counted for half if not specified manually
			factor = 1
			if damage in durationDamages:
				factor = .5
			multiplier = 1 + (self.getStat(damage + " %")
							  + self.getStat("all damage %")) / 100.0

			# "elemental" and "all damage" are aggregates rather than types you
			# can be dealt, and are reported by their components instead
			if (damage not in self.bonuses and self.get("damage")
					and damage not in ("elemental", "all damage")):
				derived.append((damage, self.get("damage")*factor*multiplier, multiplier))
			self.setIfNull(damage, self.get("damage")*factor*multiplier)
			self.setIfNull("pet "+damage, self.get("pet damage")*factor)

			self.setIfNull("triggered "+damage,
						   max([self.get(damage), self.get("triggered damage")*factor*multiplier]))

			self.setIfNull(damage+" retaliation", self.get("retaliation")*factor)
			self.setIfNull("pet "+damage+" retaliation", self.get("pet retaliation")*factor)

		if derived:
			# grouped, because they come out in a handful of bands - one per
			# attribute and duration combination - and a line each is noise
			bands = {}
			for damage, weight, multiplier in derived:
				bands.setdefault((round(weight, 3), round(multiplier, 2)), []).append(damage)
			print("  damage types the model did not name, priced off their multiplier:")
			for (weight, multiplier), names in sorted(bands.items(), reverse=True):
				print("    %7.3f  (x%.2f)  %s" % (weight, multiplier, ", ".join(sorted(names))))

		# What one swing is worth, and therefore what a point of weapon damage %
		# is worth: a skill's "% Weapon Damage" scales the whole flat damage of
		# the attack, so one point of it is one percent of your flat damage
		# pool, priced at the weights those types already carry. Same reasoning
		# as applyDamagePriority - it follows from the sheet and is not a
		# preference, so it does not need to be one. morena had it at 25 by hand
		# where the sheet says 71.
		self.setIfNull("weapon damage %", sum(
			self.getStat(d) * self.get(d) for d in damages
			if d not in ("elemental", "all damage")) / 100.0)

		# Pressing a granted skill costs you the attack you would have made.
		# Priced in the same currency, because it is the same thing: a swing.
		# At a main attack of 100% the two agree by construction - giving up one
		# swing costs exactly one swing's worth of flat damage.
		if self.get("attack opportunity cost") == 0:
			self.bonuses["attack opportunity cost"] = -self.get("weapon damage %")
		print("  weapon damage %%: %.2f  -> attack opportunity cost %.2f"
			  % (self.get("weapon damage %"), self.get("attack opportunity cost")))

		if not self.get("weapon damage %"):
			print("  WARNING: nothing on the sheet for weapon damage to scale, so pressing "
				  "a granted skill costs nothing and every component skill scores as pure "
				  "upside. Give the model some flat damage.")
		elif not self.getStat("main attack %"):
			print("  note: no 'main attack %' - a component skill is priced against a bare "
				  "100% swing, so one that beats that reads as an upgrade. Name your attack "
				  "as \"main attack\":(\"Cadence\", 12) and it is read from the skill data.")

		total = 0
		for speed in ["attack speed", "cast speed", "move speed"]:
			total += self.get(speed)
		self.setCalculated("total speed", total)

	def filterConstellations(self):
		print("\n  Checking for weapon restricted constellations...")
		for c in self.getStat("blacklist"):
			if c in Constellation.constellations:
				Constellation.constellations.remove(c)
				print("    -", c.name, "blacklisted ")
		for c in Constellation.constellations[:]:
			if c.restricts:
				satisfied = False
				for weapon in self.getStat("weapons"):
					if weapon in c.restricts:
						satisfied = True
				if not satisfied:
					Constellation.constellations.remove(c)
					print("    -", c.name, "removed <-",str(c.restricts))

	def calculateBonus(self, bonus, value):
		#handle flat duration damages being overwritten.
		# the value of flat damage is based on how much damage you'll deliver with it.
		# so 10 fire damage, 1 attack per second, 30 second fight you'll do 300 damage
		# assuming you keep hitting the same target until it dies
		# 10 burn damage over 2 seconds will do 5 damage on the first tick then you'll hit again and overwrite it.
		# so you'll only do 150 damage to that target with your burn damage so we would modify the burn damage to 5.
		# i.e. the slower your weapon the more valuable dot damage is.
		# this doesn't apply to triggered dot damage.
		# if your character play style is more like hit each enemy once so your dots will do the most damage then
		# this would be handled in the value of the stat.
		# skills with a weapon component will tend to mess this calculation up.
		# so if your build is based on skills with a weapon component with a significant cooldown that would be handled in the value of the stat
		# One rule for both, differing only in how long the gap between hits is.
		# A refreshed damage-over-time delivers dps * min(duration, interval) per
		# application, and the weight is per point delivered per hit, so that
		# product is what a point is worth. For you the interval is one attack;
		# for a pet it is the pet's own swing.
		#
		# The pet half used to sit behind an `if type(value) == list` that the
		# branch above had already returned on, so it never ran once - pet
		# duration damage was being divided by *your* attack speed, which the
		# comment beside it said was wrong.
		if type(value) == type([]):
			dotDps, seconds = value
			if bonus.startswith("pet "):
				# A summon swings about once a second and spends a while walking
				# to its next target; devotionderive measured both off the
				# creature records. Five seconds is longer than any duration
				# damage in the game lasts, so a pet's does run to completion -
				# which is what the note here always claimed, now for a reason.
				interval = 1.0 / devotionderive.BASE_ATTACK_RATE + devotionderive.CHASE_SECONDS
			else:
				interval = 1.0 / float(self.getStat("attacks/s"))
			return self.get(bonus) * dotDps * min(seconds, interval)
		return self.get(bonus)*value

	def get(self, key):
		if key in self.bonuses:
			return self.bonuses[key]
		else:
			return 0
	def set(self, key, value):
		self.bonuses[key] = value

	def setCalculated(self, key, value):
		out = key + ": " 
		if not key in self.bonuses:
			self.set(key, value)
			print("  " + out + str(self.get(key)))
		else:
			print("* " + out + str(self.get(key)) + " (" + str(value) + ")")

	def setIfNull(self, key, value):
		if not key in self.bonuses:
			self.set(key, value)

	def getStat(self, key):
		if key in self.stats:
			return self.stats[key]
		else:
			return 0


	#bonuses
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
	#stats
		# estimate how frequent combat events are for calculating dynamic stats and abilities
		# "attacks/s":1.75,		
		# "allAttacks/s":[
		# 	# list of attack skills that can be linked to abilities. remember to include your main attack.
		# 	1.75, #main attack (fire strike)
		# 	.5, # brutal shield slam: 3s recharge, 3 target max. Call it 2 targets and 4 seconds between = .5 aps
		# 	.4, #war cry: 7.5 s recharge, big radius, call it 3 hits = 3/7.5 = .4
		# 	.385, # markovian's advantage: 22% chance = 1.75*.22 = 
		# ],		
		# "hits/s":4,
		# "blocks/s":1.5,
		# "kills/s":1,		
		# "crit chance":.05,
		# "low healths/s":1.0/45, # total guesswork.

		# "fight length":30, # average length of a fight... this is for weighting abilities and over time effects. If you rely on wearing down opponents this should be long. If you are a glass cannon this should be small.

		# # estimated sheet stats for target level
		# "physique":900,
		# "cunning":400,
		# "spirit":450,

		# "offense":1200,
		# "defense":1400,

		# "health":7500,
		# "health/s %":25,

		# "armor":1000,
		# "energy":2500,
		
		# # estimated damage % for target level. add whatever damages are important to your build
		# "physical %":200, # sheet % damage for important damage types.
		# "fire %":400,
		# "lightning %":200,
		# "acid %":150,

		# "retaliation %":250+100,


		# "playStyle":"tank", # playstyle for weighting constellation abilities. [ranged/shortranged/melee/tank]
		# "weapons":[
		# 	# list of weapons used for constellations that have a weapon requirement. E.g. "shield", "sword"
		# ],
		# "blacklist":[
		# 	# list of constellations that I want to manually exclude for some reason.
		# ]	
