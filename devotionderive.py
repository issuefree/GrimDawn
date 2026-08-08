"""Turn raw devotion proc geometry into the modelling numbers the optimiser needs.

The data files should be raw game values. Everything judgemental lives here, in
one place, applied by rule rather than per-ability opinion.

These used to be hand-assigned per ability:

  shape   - which is really just a restatement of the skill's class. Measured
            against the old hand-written values, class predicts shape on 20 of
            22 procs; both disagreements are the same class labelled 'ground'
            in one place and 'circle' in another, which was inconsistency
            rather than a real distinction.

  targets - how many enemies a proc hits. This never followed from anything:
            Elemental Storm and Whirlpool share a 3.5m radius but were given
            2.5 and 2, and Tainted Eruption at 10m got the same 3 as Light of
            Empyrion at 5m. It is now computed from the area the skill covers
            and one per-character density figure, so two skills with the same
            geometry always get the same answer.

  summons - how much damage a summoned creature adds up to. The old file wrote
            out a total per summon from a guessed number of attacks: 3.3 for the
            skeleton, 5 for the shadow clone, 2 for the arcane current. The data
            files now carry the pet's damage for one hit, and summonHits works
            the count out from the lifespan and the creature's own attack speed.

  ticks   - whether a proc's stated damage lands once or once per second of its
            duration. See durationScale.
"""
import math

# skill class -> shape. The optimiser's playStyle logic in ability.py already
# knows what to do with each of these.
SHAPE_BY_CLASS = {
	"Skill_AttackRadius": "pbaoe",
	"Skill_AttackProjectileRing": "pbaoe",
	"Skill_AttackProjectileOrbiting": "pbaoe",
	"Skill_BuffAttackRadiusDuration": "pbaoe",
	"Skill_BuffAttackRadiusLightning": "pbaoe",
	"Skill_AttackProjectileAreaEffect": "ground",
	"Skill_AttackProjectileDrop": "ground",
	"Skill_BuffAttackRadiusDrop": "ground",
	"Skill_TargetedSpawnPet": "ground",
	"Skill_AttackProjectileBurst": "cone",
	"Skill_AttackProjectileFan": "cone",
	"Skill_AttackWave": "line",
	"Skill_AttackProjectile": "line",
	"Skill_AttackChain": "circle",
	"Skill_AttackBuffRadius": "circle",
	"Skill_AttackBuff": "melee",
	"Skill_AttackWeapon": "melee",
	# A basic attack, or something that replaces one: it hits whatever your
	# weapon hits, one target, at whatever range you were already fighting at.
	# Its own shape, because neither of the existing single-target answers
	# fits. The default of "circle" handed a melee character 1.25 enemies for
	# Onslaught, and "melee" would have charged a gunslinger's Fire Strike the
	# .05 that is meant for an ability which drags a kiter into arm's reach.
	# Nothing adjusts a shape that no playStyle has an opinion about, which is
	# the right answer here: how you position does not change how many enemies
	# one swing lands on.
	"Skill_WeaponPool_BasicAttack": "single",     # Fire Strike, Onslaught
	"Skill_WeaponPool_ChargedFinale": "single",   # Cadence
	"Skill_WPAttack_BasicAttack": "single",       # 13 weapon pool procs
}

# Enemies per square metre assumed when a character has not said otherwise.
# Fitted against the old hand-written targets: at 0.03 the derived value lands
# within one target on 22 of 27 procs, and is consistent by construction where
# the hand values were not. Override per character with stats["enemy density"].
DEFAULT_DENSITY = 0.03
MAX_TARGETS = 4.0

# How many enemies end up inside a circle centred on you, relative to what the
# geometry alone would give - which is a statement about how you fight rather
# than about the skill. A kiting archer barely gets anything into arm's reach; a
# tank is standing in the middle of them on purpose.
#
# These are the pbaoe numbers out of Ability.effectiveTargets, which reads them
# from here so there is one copy. They answer two questions at once: how many
# enemies a pbaoe of yours covers, and how many are close enough to be hitting
# you - which is the same circle seen from either end.
PBAOE_BY_STYLE = {"ranged": 0.125, "shortranged": 0.75, "melee": 1.0, "tank": 1.5}

# Monsters swing about once a second: the median of characterAttackSpeed over
# the 3052 Monster records that state one is exactly 1.000, the mean 1.016.
# So the rate you are hit at is very nearly the number of them in reach.
MONSTER_SWINGS = 1.0
# What share of incoming damage is each type, measured off the game rather than
# guessed. Monster records carry no damage of their own - it is all on the
# skills they name - so this walks 2964 Monster records under
# records/creatures/enemies to the 2934 whose skills deal anything, sums each
# one's offensive damage by type, and takes the mean of their shares. Each
# monster counts once, so a boss with six skills does not outvote a trash mob.
#
# It is the number that says what a point of fire resist is worth against a
# point of aether resist, and before this there was none: every resistance was
# priced identically, as if you took an equal beating from all ten.
#
# Regenerate with devotionderive.measureIncoming(); it takes about a minute and
# is a literal here for the same reason ENEMY_RESIST_BASE is - it changes only
# when the game does.
INCOMING_SHARE = {
	"physical": 0.407, "acid": 0.089, "cold": 0.084, "fire": 0.069,
	"chaos": 0.068, "vitality": 0.068, "lightning": 0.065, "pierce": 0.057,
	"aether": 0.051, "bleed": 0.040,
}


def measureIncoming(root=None):
	r"""Re-measure INCOMING_SHARE from the game. Slow, and only run by hand."""
	import collections, re
	from gddata import Database, lastValue
	db = Database(root) if root else Database()
	direct = {"Physical": "physical", "Pierce": "pierce", "Fire": "fire",
			  "Cold": "cold", "Lightning": "lightning", "Poison": "acid",
			  "Life": "vitality", "Aether": "aether", "Chaos": "chaos",
			  "Bleeding": "bleed"}
	# a duration effect states only its rate here; the type is what matters
	duration = {"SlowBleeding": "bleed", "SlowPoison": "acid", "SlowBurn": "fire",
				"SlowFrostburn": "cold", "SlowElectrical": "lightning",
				"SlowLifeLeach": "vitality"}
	total, counted = collections.Counter(), 0
	for path in db.under("records/creatures/enemies"):
		record = db.read(path)
		if not record or record.get("Class") != "Monster":
			continue
		got = collections.Counter()
		for field, value in record.items():
			if not re.fullmatch(r"skillName\d+", field) or not isinstance(value, str):
				continue
			skill = db.read(value)
			if not skill:
				continue
			for name, damage in direct.items():
				low = lastValue(skill.get("offensive%sMin" % name, 0)) or 0
				high = lastValue(skill.get("offensive%sMax" % name, 0)) or low
				if low or high:
					got[damage] += (float(low) + float(high)) / 2.0
			for name, damage in duration.items():
				low = lastValue(skill.get("offensive%sMin" % name, 0)) or 0
				if low:
					got[damage] += float(low)
		if not got:
			continue
		counted += 1
		spread = sum(got.values())
		for damage, amount in got.items():
			total[damage] += amount / spread
	return {d: round(v / counted, 3) for d, v in total.most_common()}

# Metres around you that enemies attack from. The one figure here with nothing
# measured behind it - monster attack ranges live on their skills rather than
# their records, the same reason PHYSICAL_SHARE is a guess. Three metres is
# arm's reach and a step.
ENGAGEMENT_RADIUS = 3.0


def hitsTakenFor(playStyle, density=None, enemies=None):
	"""How often you are hit, from how many enemies get within reach of you.

	The same circle Ability.effectiveTargets measures for a pbaoe, read from the
	other end: the enemies your own point-blank area effect would cover are the
	enemies close enough to be swinging at you. So it is the same density, the
	same playStyle adjustment and the same ceiling, times what a monster swings
	at - which the records say is once a second.

	Which makes a retribution build's rate fall out of the fight rather than
	being stated: one enemy is one hit a second, a room of them is four, and a
	kiting character is barely touched whatever the room holds.
	"""
	targets = targetsFor("Skill_AttackRadius", radius=ENGAGEMENT_RADIUS, density=density)
	targets *= PBAOE_BY_STYLE.get(playStyle, 1.0)
	limit = enemies if enemies else MAX_TARGETS
	return min(targets, MAX_TARGETS, limit) * MONSTER_SWINGS


def shapeFor(skillClass):
	"""The shape a class implies, or "single" where the table has no entry.

	The default used to be "circle", which is an opinion: it tells the
	playStyle adjustment to treat the skill as an area effect and multiply its
	targets. 53 classes fall through this - Skill_Modifier alone is 85 skills -
	and a melee character was collecting 1.25 enemies for every one of them,
	including for modifiers like Open Wounds that have no geometry at all and
	only exist to hang off another skill.

	"single" is the absence of an opinion rather than a different one: no
	playStyle has a branch for it, so nothing is scaled. What area a class
	genuinely covers still comes from its own radius, which areaFor reads
	whatever the shape says.
	"""
	return SHAPE_BY_CLASS.get(skillClass, "single")


def areaFor(skillClass, geometry):
	"""Square metres a proc covers, from whichever geometry its class uses.

	Radius classes carry projectileExplosionRadius/skillTargetRadius, waves
	carry waveDistance and a start/end width, and chains carry sparkMaxNumber
	instead of any area at all.
	"""
	radius = float(geometry.get("radius") or 0)
	shape = shapeFor(skillClass)
	if shape == "line" and geometry.get("waveDistance"):
		width = (float(geometry.get("waveStartWidth") or 0)
				 + float(geometry.get("waveEndWidth") or 0)) / 2.0 or 1.0
		return float(geometry["waveDistance"]) * width
	if radius > 0.5:
		area = math.pi * radius * radius
		if shape == "cone":
			area /= 3.0    # a cone sweeps roughly a third of the circle
		elif shape == "line":
			area /= 4.0
		return area
	return 0.0


def targetsFor(skillClass, radius=0.0, projectiles=0, density=None, geometry=None):
	"""Estimate how many enemies a proc realistically hits.

	Area-based where the skill has a radius, projectile-count-based where it
	does not, and a floor of one because a proc that triggers hits something.
	density is enemies per square metre and belongs to the character, not the
	skill - a build that fights packs should see bigger numbers everywhere.
	"""
	if density is None:
		density = DEFAULT_DENSITY
	geometry = dict(geometry or {})
	geometry.setdefault("radius", radius)
	sparks = float(geometry.get("sparkMaxNumber") or 0)

	area = areaFor(skillClass, geometry)
	if area > 0:
		hit = 1.0 + area * density
	elif sparks:
		# a chain jumps between separate targets, so it is far more reliable
		# at hitting several than an area effect of the same nominal size
		hit = 1.0 + math.sqrt(sparks)
	elif projectiles:
		# many small projectiles rarely all land on separate targets
		hit = 1.0 + math.sqrt(float(projectiles)) * 0.5
	else:
		hit = 1.0

	return round(min(MAX_TARGETS, hit), 2)


# Seconds a summoned creature spends walking to its next target between swings.
# The old hand-written Revenant put this at 4 ("2 seconds per attack, 4 seconds
# spent chasing on average") and every other summon was guessed a whole number of
# attacks with no stated reasoning at all. 4 is kept, but it is now added to the
# pet's real attack speed instead of to a guessed one.
CHASE_SECONDS = 4.0
# What characterAttackSpeed multiplies. Creature records cluster hard at 1.0,
# which is the game's "average" attack rate of one swing a second.
BASE_ATTACK_RATE = 1.0


def summonHits(lifespan, attackSpeed=0.0, mode="attack", melee=False):
	"""How many times one summon lands its payload before it expires.

	Three ways a summon delivers damage, and the game's own records say which:

	  aura    a pool or a swarm - a standing field that damages once a second
			  for as long as it is there, and never has to chase anything
	  attack  a creature that swings at its own attack speed, plus the walk to
			  the next target if it fights in melee
	  once    a trap: it detonates and dies, so it is not scored here at all -
			  devotiongen emits those as ordinary attacks

	The hand-written data guessed this per summon and disagreed with itself:
	the skeleton got 3.3 attacks over 20s, the shadow clone 5 over 24s and the
	arcane current 2 over 4.5s, which are three different rates for three
	creatures whose records differ by less than that.
	"""
	life = float(lifespan or 0)
	if life <= 0:
		return 1.0
	if mode == "aura":
		return life
	seconds = 1.0 / (float(attackSpeed or 0) or BASE_ATTACK_RATE)
	if melee:
		seconds += CHASE_SECONDS
	return max(1.0, life / seconds)


def summonDebuffUpTime(hits, lifespan):
	"""Fraction of a summon's life its timed debuffs are actually up.

	A pet reapplies its debuff every time it connects, so the debuff is up for
	about as much of the fight as the pet is landing hits. An aura reaches 1 and
	stays there, which is right: stand in Yugol's pool and the slow never lapses.
	"""
	life = float(lifespan or 0)
	if life <= 0:
		return 1.0
	return min(1.0, float(hits) / life)


# Damaging ticks one enemy takes from a ground effect it is caught in. A field
# persists for its stated duration, but that is how long it is on the floor, not
# how long anything stands in it, and the two were being conflated: a six second
# Whirlpool was charging six full ticks.
#
# One is what the hand-written data said. Of the eight procs that state a
# duration, seven carried a single tick, and the author's note on Whirlpool spells
# out why - "big radius but I'm taking a damage tick away because it's long
# lasting ground target". Aetherfire, carrying 190 x 3, is the lone exception and
# is the one this scaling was originally generalised from.
GROUND_TICKS = 1.0


# Metres between you and what you are hitting, per playStyle. The play styles in
# ability.py already state these in words - ranged is "optimal range 10+ yards",
# shortranged "5-10 yards", melee "melee but not surrounded", tank "all enemies
# up close and personal" - so this is those sentences as numbers, in one place.
ENGAGEMENT_RANGE = {"tank": 1.0, "melee": 1.5, "shortranged": 7.0, "ranged": 12.0}
DEFAULT_RANGE = 2.5


def damageScale(bands, playStyle):
	"""What share of its damage a proc lands, given how far out you fight.

	A projectile can be worth less up close than at distance - Blade Burst
	throws a ring of blades from your feet and only reaches full damage three
	metres out, so a tank standing in the middle of a pack collects the 70%
	band. It is the only devotion proc in the game with a falloff, but the rule
	is the game's rather than a special case, so it is applied by rule.

	Returns 1.0 when a proc has no falloff, which is every other proc.
	"""
	if not bands:
		return 1.0
	distance = ENGAGEMENT_RANGE.get(playStyle, DEFAULT_RANGE)
	for low, high, percent in bands:
		if low <= distance < high:
			return percent / 100.0
	# past the last band the projectile has expired; the furthest one is the
	# best available answer for a character who fights further out than the
	# skill was built for
	return bands[-1][2] / 100.0 if bands else 1.0


def durationScale(duration, shape=None):
	"""How many times a proc's stated damage lands on one enemy.

	A duration means different things by shape. On a ground field it is how long
	the field lasts; on a mark or a maul it is how long the debuff sits on one
	enemy, and scaling by it multiplied Mark of the Wendigo's damage tenfold.
	Neither is a count of hits, so neither is scaled beyond GROUND_TICKS.
	"""
	if shape is not None and shape != "ground":
		return 1.0
	return GROUND_TICKS if float(duration or 0) > 1 else 1.0
