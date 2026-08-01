"""Turn raw devotion proc geometry into the modelling numbers the optimiser needs.

The data files should be raw game values. Everything judgemental lives here, in
one place, applied by rule rather than per-ability opinion.

Two things used to be hand-assigned per ability:

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


def durationScale(activeDuration):
	"""Ground effects list damage per tick; they apply for their whole duration.

	The old data files baked this in by hand for some abilities and not others
	(Aetherfire carried 190 x 3, its neighbours did not), which is precisely
	the sort of inconsistency this module exists to remove.
	"""
	active = float(activeDuration or 0)
	return active if active > 1 else 1.0
