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
}

# Enemies per square metre assumed when a character has not said otherwise.
# Fitted against the old hand-written targets: at 0.03 the derived value lands
# within one target on 22 of 27 procs, and is consistent by construction where
# the hand values were not. Override per character with stats["enemy density"].
DEFAULT_DENSITY = 0.03
MAX_TARGETS = 4.0


def shapeFor(skillClass):
	return SHAPE_BY_CLASS.get(skillClass, "circle")


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
