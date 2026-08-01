"""Pull devotion constellation data out of the Grim Dawn .arz databases.

Expansions override the base database, so records are layered
base -> GDX1 -> GDX2 -> GDX3 and the last definition wins.
"""
import os

from constants import durationDamages
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
}
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


def affinityString(record, kind):
    """kind is 'Required' or 'Given' -> e.g. '3a 2e'."""
    parts = []
    for i in (1, 2, 3):
        amount = record.get("affinity%s%d" % (kind, i), 0) or 0
        label = record.get("affinity%sName%d" % (kind, i), "")
        if amount and label in AFFINITY:
            parts.append("%d%s" % (amount, AFFINITY[label]))
    return " ".join(parts)


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
    return sorted({tag for field, tag in WEAPON_FLAGS.items() if skill.get(field)})


def compareToHandMaintained():
    """Report where constellationData.py has drifted from the game files.

    Returns a list of human-readable lines. Star bonuses are compared as
    multisets of (name, value) so a difference in star ordering between the two
    sources is not mistaken for a change in the data.
    """
    from dataModel import Constellation
    import constellationData
    assert constellationData  # imported for its side effect: registers every constellation

    db = Database()
    hand = {c.name: c for c in Constellation.constellations}
    lines, absent, changed = [], [], []

    for path in db.constellations():
        record = db.read(path)
        name = record.get("FileDescription", "")
        if not name:
            continue
        if name not in hand:
            absent.append(name)
            continue
        current = hand[name]
        gameStars = [i for i in range(1, 9) if record.get("devotionButton%d" % i)]
        if len(gameStars) != len(current.stars):
            changed.append("%s: %d stars in game, %d here"
                           % (name, len(gameStars), len(current.stars)))
            continue
        gameTotals, handTotals = {}, {}
        for index in gameStars:
            skillPath = db.read(record["devotionButton%d" % index]).get("skillName")
            if not skillPath:
                continue
            skill = db.read(skillPath)
            if skill.get("templateAutoCast"):
                continue # a triggered proc, not a passive star bonus
            for key, value in starBonuses(skill, db).items():
                gameTotals[key] = gameTotals.get(key, 0) + value
        for star in current.stars:
            for key, value in star.bonuses.items():
                if isinstance(value, list):
                    continue
                handTotals[key] = handTotals.get(key, 0) + value
        for key in sorted(set(gameTotals) & set(handTotals)):
            if abs(gameTotals[key] - handTotals[key]) > 0.51:
                changed.append("%s: %s is %g in game, %g here"
                               % (name, key, gameTotals[key], handTotals[key]))

    if absent:
        lines.append("%d constellation(s) in the game files but not in constellationData.py:"
                     % len(absent))
        lines.extend("    " + n for n in sorted(absent))
    if changed:
        lines.append("%d value(s) differ from the game files:" % len(changed))
        lines.extend("    " + c for c in sorted(changed))
    if not lines:
        lines.append("constellationData.py matches the game files.")
    return lines


GEOMETRY_FIELDS = ("projectileExplosionRadius", "skillTargetRadius", "skillRadius",
                   "waveDistance", "waveStartWidth", "waveEndWidth", "sparkMaxNumber",
                   "projectileLaunchNumber", "skillProjectileMaximumNumber",
                   "skillActiveDuration", "skillCooldownTime")


def geometryFor(skill, db=None, depth=0):
    """Raw geometry for a proc, following the sub-record some classes delegate to."""
    out = {}
    for field in GEOMETRY_FIELDS:
        value = lastValue(skill.get(field, 0)) or 0
        if value:
            out[field] = float(value)
    out["radius"] = max(out.get("projectileExplosionRadius", 0),
                        out.get("skillTargetRadius", 0),
                        out.get("skillRadius", 0))
    out["projectiles"] = (out.get("projectileLaunchNumber", 0)
                          or out.get("skillProjectileMaximumNumber", 0))
    # Skill_AttackBuffRadius and friends hold their numbers one record along
    if depth < 2 and not out["radius"] and not out["projectiles"]:
        for link in ("buffSkillName", "petSkillName", "skillSecondaryName"):
            target = skill.get(link)
            if target and db is not None:
                nested = db.read(target)
                if nested:
                    merged = geometryFor(nested, db, depth + 1)
                    for key, value in merged.items():
                        out.setdefault(key, value)
                        if key in ("radius", "projectiles") and value:
                            out[key] = out[key] or value
                    break
    return out
