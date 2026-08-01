"""Pull devotion constellation data out of the Grim Dawn .arz databases.

Expansions override the base database, so records are layered
base -> GDX1 -> GDX2 -> GDX3 and the last definition wins.
"""
import os

from constants import damages, durationDamages
from gdarz import Arz

# Override with the GRIM_DAWN_DIR environment variable if installed elsewhere.
GD = os.environ.get("GRIM_DAWN_DIR",
                    r"C:/Program Files (x86)/Steam/steamapps/common/Grim Dawn")
LAYERS = ["database/database.arz", "gdx1/database/GDX1.arz",
          "gdx2/database/GDX2.arz", "gdx3/database/GDX3.arz"]

# Grim Dawn's internal field names -> the optimiser's bonus vocabulary.
# The naming is treacherous: offensiveLife is vitality, offensivePoison is acid,
# offensiveSlowPoison is poison-over-time, offensiveSlowPhysical is internal trauma.
FLAT = {
    "offensivePhysical": "physical", "offensivePierce": "pierce",
    "offensiveFire": "fire", "offensiveCold": "cold", "offensiveLightning": "lightning",
    "offensivePoison": "acid", "offensiveLife": "vitality", "offensiveAether": "aether",
    "offensiveChaos": "chaos", "offensiveElemental": "elemental",
    # offensiveLifeLeechMin is how the game expresses "% of attack damage
    # converted to health", which this codebase calls lifesteal %.
    "offensiveLifeLeech": "lifesteal %",
    "offensiveSlowBleeding": "bleed", "offensiveSlowPhysical": "internal",
    # GD names these after the parent element, not the effect: SlowFire is burn,
    # SlowCold is frostburn, SlowLightning is electrocute, SlowLife is vitality decay.
    "offensiveSlowFire": "burn", "offensiveSlowCold": "frostburn",
    "offensiveSlowLightning": "electrocute", "offensiveSlowPoison": "poison",
    "offensiveSlowLife": "vitality decay",
    # resist reduction carries a Min suffix in the data, both forms
    "offensiveTotalResistanceReductionAbsolute": "reduce resist",
    "offensiveElementalResistanceReductionAbsolute": "reduce elemental resist",
    "offensivePhysicalResistanceReductionAbsolute": "reduce physical resist",
    # percent-based resist reduction is expressed as a Min/Max pair
    "offensiveElementalResistanceReductionPercent": "reduce elemental resist",
    "offensivePhysicalResistanceReductionPercent": "reduce physical resist",
    "offensiveTotalResistanceReductionPercent": "reduce resist",
    "retaliationPhysical": "physical retaliation", "retaliationPierce": "pierce retaliation",
    "retaliationFire": "fire retaliation", "retaliationCold": "cold retaliation",
    "retaliationLightning": "lightning retaliation", "retaliationPoison": "acid retaliation",
    "retaliationLife": "vitality retaliation", "retaliationChaos": "chaos retaliation",
    "retaliationAether": "aether retaliation", "retaliationBleeding": "bleed retaliation",
    "retaliationStun": "stun retaliation",
    "retaliationSlowLife": "vitality decay retaliation",
    "retaliationSlowLifeLeach": "life leech retaliation",
    # These name what is done to the target rather than a damage type. The
    # optimiser has no stat for "the enemy misses more", so slowing an enemy's
    # offensive ability is scored as defence and its defensive ability as
    # offence, which is how the hand-written data always scored them.
    # SlowRunSpeed slows the legs, SlowTotalSpeed slows everything the target
    # does; the optimiser has one stat for being slowed and both land on it.
    "offensiveSlowRunSpeed": "slow move",
    "offensiveSlowTotalSpeed": "slow move",
    "offensiveSlowOffensiveAbility": "defense",
    "offensiveSlowDefensiveAbility": "offense",
}
# The subset of FLAT that lands on the enemy rather than on you. A summon's
# payload keeps these and its damage; everything else in a pet's records
# describes the pet itself and is none of the player's business.
ENEMY_FLAT = frozenset(["slow move", "defense", "offense"])
DIRECT = {
    "characterOffensiveAbility": "offense", "characterOffensiveAbilityModifier": "offense %",
    "characterDefensiveAbility": "defense", "characterDefensiveAbilityModifier": "defense %",
    "characterStrength": "physique", "characterStrengthModifier": "physique %",
    "characterDexterity": "cunning", "characterDexterityModifier": "cunning %",
    "characterIntelligence": "spirit", "characterIntelligenceModifier": "spirit %",
    "characterLife": "health", "characterLifeModifier": "health %",
    "characterMana": "energy", "characterManaModifier": "energy %",
    "characterLifeRegen": "health/s", "characterLifeRegenModifier": "health/s %",
    "characterManaRegen": "energy/s", "characterManaRegenModifier": "energy/s %",
    "characterAttackSpeedModifier": "attack speed",
    "characterSpellCastSpeedModifier": "cast speed",
    "characterRunSpeedModifier": "move speed",
    "characterTotalSpeedModifier": "total speed",
    "characterDodgePercent": "avoid melee", "characterDeflectProjectile": "avoid ranged",
    "defensiveProtection": "armor", "defensiveProtectionModifier": "armor %",
    "defensiveAbsorptionModifier": "armor absorb",
    "defensivePhysical": "physical resist", "defensivePierce": "pierce resist",
    "defensiveFire": "fire resist", "defensiveCold": "cold resist",
    "defensiveLightning": "lightning resist", "defensivePoison": "acid resist",
    "defensiveLife": "vitality resist", "defensiveAether": "aether resist",
    "defensiveChaos": "chaos resist", "defensiveBleeding": "bleed resist",
    "defensiveElementalResistance": "elemental resist",
    "defensiveStun": "stun resist", "defensiveFreeze": "freeze resist",
    "defensiveSlowLifeLeach": "life leech resist",
    "defensivePetrify": "petrify resist", "defensiveTrap": "trap resist",
    "defensiveDisruption": "skill disruption protection",
    "defensiveBlockModifier": "block %", "defensiveBlockAmountModifier": "blocked damage %",
    "blockRecoveryTime": "shield recovery",
    "offensiveTotalDamageModifier": "all damage %",
    "offensiveCritDamageModifier": "crit damage",
    "weaponDamagePct": "weapon damage %",
    "offensivePhysicalModifier": "physical %", "offensivePierceModifier": "pierce %",
    "offensiveFireModifier": "fire %", "offensiveColdModifier": "cold %",
    "offensiveLightningModifier": "lightning %", "offensivePoisonModifier": "acid %",
    "offensiveLifeModifier": "vitality %", "offensiveAetherModifier": "aether %",
    "offensiveChaosModifier": "chaos %", "offensiveElementalModifier": "elemental %",
    "offensiveSlowBleedingModifier": "bleed %", "offensiveSlowPhysicalModifier": "internal %",
    "offensiveSlowFireModifier": "burn %", "offensiveSlowColdModifier": "frostburn %",
    "offensiveSlowLightningModifier": "electrocute %", "offensiveSlowPoisonModifier": "poison %",
    "offensiveSlowLifeModifier": "vitality decay %",
    "offensiveLifeLeechModifier": "life leech %",
    "offensivePercentCurrentLifeModifier": "lifesteal %",
    "offensiveLifeLeechChanceModifier": "lifesteal %",
    "retaliationTotalDamageModifier": "retaliation %",
    "offensiveStunModifier": "stun %",
    "offensiveSlowBleedingDurationModifier": "bleed duration",
    "offensiveSlowFireDurationModifier": "burn duration",
    "offensiveSlowColdDurationModifier": "frostburn duration",
    "offensiveSlowLightningDurationModifier": "electrocute duration",
    "offensiveSlowPoisonDurationModifier": "poison duration",
    "offensiveSlowPhysicalDurationModifier": "internal duration",
    "offensiveSlowLifeDurationModifier": "vitality decay duration",
    "defensiveTotalSpeedResistance": "slow resist",
    "defensivePercentReflectionResistance": "reflected damage reduction",
    "defensiveReflect": "damage reflect %",
    "characterHealIncreasePercent": "healing %",
    "characterConstitutionModifier": "constitution %",
    "characterEnergyAbsorptionPercent": "energy absorb",
    "characterDefensiveBlockRecoveryReduction": "shield recovery",
    "characterAttackSpeedModifier": "attack speed",
    "defensiveBleeding": "bleed resist",
    "skillCooldownReduction": "skill recharge",
    "offensiveFumbleModifier": "fumble", "offensiveTotalResistanceReductionAbsolute": "reduce resist",
    # A shield absorbs a flat amount or a percentage; the game keeps the two in
    # separate fields and so does the optimiser.
    "damageAbsorption": "damage absorb", "damageAbsorptionPercent": "damage absorb %",
    # Heals that restore a lump plus a fraction of your maximum.
    "skillLifeBonus": "health", "skillLifePercent": "health %",
}
# Life the skill costs you every second it is running. Same units as a
# regeneration bonus, opposite sign.
COSTS = {"skillActiveLifeCost": "health/s", "skillActiveManaCost": "energy/s"}
# Crowd control the data states as a duration in seconds. The hand-written file
# scored these out of 100 and picked the number by feel - Magi's 1.5s stun was
# worth 25 and Spear of the Heavens' 1.0s was worth 100. One second is taken as
# 100 here so that two procs that stun for the same time are worth the same.
STUNS = ("offensiveStun", "offensiveKnockdown")
STUN_SCALE = 100.0
# A record with debufSkill set describes what is done to the enemy, using the
# very same field names as a buff on yourself. A negative resistance there is
# resistance reduction; the optimiser has no stat for "enemy hits less
# accurately", so reduced enemy offensive ability is scored the way the
# hand-written data always scored it, as defence.
DEBUFF = {
    "defensivePhysical": "reduce physical resist", "defensivePierce": "reduce pierce resist",
    "defensiveFire": "reduce fire resist", "defensiveCold": "reduce cold resist",
    "defensiveLightning": "reduce lightning resist", "defensivePoison": "reduce acid resist",
    "defensiveLife": "reduce vitality resist", "defensiveAether": "reduce aether resist",
    "defensiveChaos": "reduce chaos resist", "defensiveBleeding": "reduce bleed resist",
    "defensiveElementalResistance": "reduce elemental resist",
    "characterOffensiveAbility": "defense",
    "characterDefensiveAbility": "offense",
    "defensiveProtection": "reduce armor",
}
WEAPON_FLAGS = {"Sword": "sword", "Sword2h": "2h-sword", "Axe": "axe", "Axe2h": "2h-axe",
                "Mace": "mace", "Mace2h": "2h-mace", "Spear": "spear", "Staff": "staff",
                "Dagger": "dagger", "Scepter": "scepter", "Shield": "shield",
                "Offhand": "offhand", "Ranged1h": "ranged", "Ranged2h": "ranged"}
AFFINITY = {"Ascendant": "a", "Chaos": "c", "Eldritch": "e", "Order": "o", "Primordial": "p"}


class Database:
    """Layered view of the four .arz files."""

    def __init__(self, root=GD):
        self.layers = []
        for rel in LAYERS:
            path = os.path.join(root, rel)
            if os.path.exists(path):
                self.layers.append(Arz(path))
        self.cache = {}

    def read(self, name):
        if name in self.cache:
            return self.cache[name]
        merged = None
        for layer in self.layers:          # later layers override earlier ones
            if name in layer.records:
                merged = layer.read(name)
        self.cache[name] = merged
        return merged

    def constellations(self):
        names = set()
        for layer in self.layers:
            names.update(n for n in layer.records
                         if "/devotion/constellations/constellation" in n
                         and "background" not in n)
        return sorted(names)


def lastValue(value):
    """Devotion stats are per-level arrays; the final entry is the maxed value."""
    if isinstance(value, list):
        return value[-1] if value else 0
    return value


RACES = {"Undead": "damage undead %", "Beast": "damage beast %", "Human": "damage human %",
         "Chthonic": "damage cthonics %", "Aetherial": "damage aetherials %",
         "Insectoid": "damage insectoid %", "Magical": "damage magical %",
         "Eldritch": "damage eldritch %"}


def starBonuses(skill, db=None):
    """Map one star's passive stat fields into optimiser bonus names.

    A star may also carry petBonusName, pointing at a record that uses the very
    same field names but applies them to your pets. Those are folded in here
    with a "pet " prefix, which is how the optimiser names them.
    """
    out = {}
    petRecord = skill.get("petBonusName")
    if petRecord and db is not None:
        bonus = db.read(petRecord)
        if bonus:
            for key, value in starBonuses(bonus).items():
                key = key if key.startswith("pet ") else "pet " + key
                out[key] = out.get(key, 0) + value
    for field, name in DIRECT.items():
        v = lastValue(skill.get(field, 0))
        if v:
            out[name] = out.get(name, 0) + round(float(v), 3)
    races = skill.get("racialBonusRace")
    racial = lastValue(skill.get("racialBonusPercentDamage", 0)) or 0
    if racial and races:
        for race in (races if isinstance(races, list) else [races]):
            name = RACES.get(race)
            if name:
                out[name] = out.get(name, 0) + round(float(racial), 3)
    for prefix, name in FLAT.items():
        lo = lastValue(skill.get(prefix + "Min", 0)) or 0
        hi = lastValue(skill.get(prefix + "Max", 0)) or 0
        if not (lo or hi):
            continue
        value = round((float(lo) + float(hi or lo)) / 2.0, 3)
        seconds = lastValue(skill.get(prefix + "DurationMin", 0)) or 0
        if seconds and name in durationDamages:
            # damage over time is [damage per second, seconds]; calculateBonus
            # and Ability both expect that pair rather than a flat total
            out[name] = [value, round(float(seconds), 2)]
        elif not isinstance(out.get(name), list):
            out[name] = out.get(name, 0) + value
    return out


def weaponRestricts(skill):
    """Weapon types a star demands, as the tags the optimiser filters on."""
    return sorted({tag for field, tag in WEAPON_FLAGS.items() if skill.get(field)})


def isDebuff(record):
    return bool(record.get("debufSkill"))


def procRecords(skill, db, depth=0):
    """A proc skill and the buff record it delegates to.

    Several classes - Skill_AttackBuff, Skill_AttackBuffRadius, Skill_BuffRadius -
    hold nothing but a pointer to a buffSkillName record, and that record is where
    the trigger, the display name and the whole payload actually live. Dire Bear's
    star skill is literally one field (pointBlank); "Maul", its 305 physical and
    its 4.5m radius are all on the buff. The two records never define the same
    stat, so reading them as one record is safe.
    """
    out = [skill]
    target = skill.get("buffSkillName") if depth < 2 else None
    if target and db is not None:
        nested = db.read(target)
        if nested:
            out.extend(procRecords(nested, db, depth + 1))
    return out


def firstOf(records, field, default=None):
    """First non-empty value of a field across a proc's records."""
    for record in records:
        value = lastValue(record.get(field, 0)) or 0
        if value:
            return value
    return default


def hasFlatDamage(record):
    """True if a record carries flat damage of its own, as opposed to modifiers."""
    return any(lastValue(record.get(prefix + "Min", 0)) or lastValue(record.get(prefix + "Max", 0))
               for prefix, name in FLAT.items() if name in damages)


def summonFor(skill, db):
    """What a spawn proc actually puts on the field.

    A summon's damage is nowhere in the skill record: the skill only names a
    creature, and the creature's own attack skills carry the numbers. This walks
    spawnObjects -> pet -> pet skills and reports raw game values only. How many
    times a summon gets to use that attack is judgement, and lives in
    devotionderive.

    Returns None if the skill spawns nothing that fights (some spawn purely
    cosmetic objects), otherwise a dict of:

        lifespan       seconds the summon lasts
        limit, burst   how many may stand at once, how many arrive per cast
        attackSpeed    the pet's characterAttackSpeed multiplier (0 = stationary)
        mode           "attack" repeated attacks, "aura" a damaging field that
                       ticks once a second, "once" a trap that detonates and dies
        melee          whether the pet has to reach its target before it can hit
        records        the records whose bonuses make up one hit
    """
    spawns = skill.get("spawnObjects")
    petPath = lastValue(spawns) if spawns else None
    pet = db.read(petPath) if petPath else None
    if not pet:
        return None

    paths = [pet.get("skillName%d" % i) for i in range(1, 13)]
    paths += [pet.get("attackSkillName"), pet.get("specialAttackSkillName")]
    skills = [db.read(path) for path in paths if path]
    skills = [s for s in skills if s]

    mode, records = None, []
    # A pool or a swarm is modelled in the data as a pet holding a toggled
    # radius buff; that buff record is the thing that does the damage.
    for petSkill in skills:
        if "BuffRadiusToggled" in (petSkill.get("Class") or ""):
            nested = [r for r in procRecords(petSkill, db) if hasFlatDamage(r)]
            if nested:
                mode, records = "aura", nested
                break

    if not records:
        attack = db.read(pet["attackSkillName"]) if pet.get("attackSkillName") else None
        if attack:
            # a passive with flat damage is the damage the creature adds to every
            # swing, so it belongs to each hit as much as the attack does
            records = [attack] + [s for s in skills
                                  if s.get("Class") == "Skill_Passive" and hasFlatDamage(s)]
            mode = "attack"
        else:
            # No named attack. A creature still hits for whatever its innate
            # passive carries (Bysmiel's hound); anything else is a trap whose
            # single skill goes off once and takes the pet with it.
            innate = [s for s in skills
                      if s.get("Class") == "Skill_Passive" and hasFlatDamage(s)]
            if innate:
                mode, records = "attack", innate
            else:
                for petSkill in skills:
                    if "Suicide" in (petSkill.get("Class") or ""):
                        continue
                    nested = [r for r in procRecords(petSkill, db) if hasFlatDamage(r)]
                    if nested:
                        mode, records = "once", nested
                        break
    if not records:
        return None

    # a pet that has to walk to its target spends much of its life doing that.
    # Read it from every skill the creature owns, not just the damaging one:
    # Bysmiel's hound carries its damage on a passive and its melee reach on the
    # attacks that passive feeds.
    melee = any((s.get("distanceProfile") or "") == "Melee" for s in skills)
    return {"lifespan": float(lastValue(skill.get("spawnObjectsTimeToLive", 0)) or 0),
            "limit": float(lastValue(skill.get("petLimit", 0)) or 1),
            "burst": float(lastValue(skill.get("petBurstSpawn", 0)) or 1),
            "attackSpeed": float(pet.get("characterAttackSpeed") or 0),
            "mode": mode, "melee": melee, "records": records,
            "attackClass": records[0].get("Class") or ""}


GEOMETRY_FIELDS = ("projectileExplosionRadius", "skillTargetRadius", "skillRadius",
                   "waveDistance", "waveStartWidth", "waveEndWidth", "sparkMaxNumber",
                   "projectileLaunchNumber", "skillProjectileMaximumNumber",
                   "skillActiveDuration", "skillCooldownTime")


def geometryFor(records):
    """Raw geometry for a proc, read across every record it is made of.

    Skill_AttackBuffRadius and friends keep their radius on the buff record
    rather than on the star's own skill, which is the same indirection
    procRecords already resolves - so this just reads the list it is given,
    first record to state a field wins.
    """
    out = {}
    for record in records:
        for field in GEOMETRY_FIELDS:
            value = lastValue(record.get(field, 0)) or 0
            if value and field not in out:
                out[field] = float(value)
    out["radius"] = max(out.get("projectileExplosionRadius", 0),
                        out.get("skillTargetRadius", 0),
                        out.get("skillRadius", 0))
    out["projectiles"] = (out.get("projectileLaunchNumber", 0)
                          or out.get("skillProjectileMaximumNumber", 0))
    return out
