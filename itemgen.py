"""Generate itemData.py from the Grim Dawn database.

Three things come out of it and they are found three different ways:

  components  every ItemRelic record. What slots one fits is a set of boolean
              flags on the record itself.
  augments    every ItemEnchantment record, the same way.
  equipment   named pieces only. There are some eight thousand gear records and
              no way to tell from the data which of them a character cares
              about, so the names stay hand-picked in equipmentWanted.py and
              this looks each one up. Set bonuses come from the set record the
              pieces point at, one entry per piece count, which is the shape the
              hand-written file used.

Item names are not in the .arz at all - a record says it is called
tagCompB018Name - so this reads them out of the text archives through
gddata.Database.name.

    python devotion.py --regenerate
"""
from gddata import (Database, firstOf, geometryFor, itemExtras, lastValue,
                    procRecords, starBonuses)
from devotiongen import dictLiteral, procBonuses, triggerAndChance

# record flag -> the location name the optimiser filters on. The game says
# hands where the models say arms, and names each two-hander separately where
# the models have one "twohand".
SLOTS = {
    "head": "head", "chest": "chest", "shoulders": "shoulders", "hands": "arms",
    "legs": "legs", "feet": "feet", "waist": "waist",
    "amulet": "amulet", "medal": "medal", "ring": "ring",
    "shield": "shield", "offhand": "offhand",
    "sword": "sword", "axe": "axe", "mace": "mace", "dagger": "dagger",
    "scepter": "scepter", "ranged1h": "ranged", "ranged2h": "ranged",
    "sword2h": "twohand", "axe2h": "twohand", "mace2h": "twohand",
    "spear2h": "twohand", "staff": "twohand",
}
# gear record class -> location, for the named equipment
CLASS_SLOTS = {
    "ArmorProtective_Head": "head", "ArmorProtective_Chest": "chest",
    "ArmorProtective_Shoulders": "shoulders", "ArmorProtective_Hands": "arms",
    "ArmorProtective_Legs": "legs", "ArmorProtective_Feet": "feet",
    "ArmorProtective_Waist": "waist",
    "ArmorJewelry_Amulet": "amulet", "ArmorJewelry_Medal": "medal",
    "ArmorJewelry_Ring": "ring",
    "WeaponArmor_Shield": "shield", "WeaponArmor_Offhand": "offhand",
    "WeaponMelee_Sword": "sword", "WeaponMelee_Axe": "axe",
    "WeaponMelee_Mace": "mace", "WeaponMelee_Dagger": "dagger",
    "WeaponMelee_Scepter": "scepter",
    "WeaponHunting_Ranged1h": "ranged", "WeaponHunting_Ranged2h": "ranged",
    "WeaponMelee_Sword2h": "twohand", "WeaponMelee_Axe2h": "twohand",
    "WeaponMelee_Mace2h": "twohand", "WeaponMelee_Spear2h": "twohand",
    "WeaponMelee_Staff": "twohand", "ItemArtifact": "relic",
}
GEAR_CLASSES = tuple(CLASS_SLOTS)

# A weapon pool skill does not cost you a turn, it replaces your swing: the game
# rolls skillChanceWeight on each attack and substitutes this for the default
# one. That is a different thing from a skill you press, and the optimiser
# already has a type for it - a wps is charged -100 weapon damage % for the
# attack it displaces rather than an attack opportunity cost, because you were
# going to swing anyway.
#
# Told apart by class alone. Every one of the 39 on items is a Skill_WPAttack_*,
# none of them has a cooldown, and skillChanceWeight appears on nothing else.
WPS_CLASS = "WPAttack"

# An item's granted skill has no templateAutoCast: what fires it is its class.
# Most are abilities you press, which the optimiser calls a manual trigger.
SKILL_TRIGGERS = (
    ("PassiveOnLife", "low health"),
    ("PassiveOnHit", "hit"),
    ("Toggled", "toggle"),
    ("Passive", "passive"),
)


def triggerFor(skillClass):
    for fragment, trigger in SKILL_TRIGGERS:
        if fragment.lower() in skillClass.lower():
            return trigger
    return "manual"


def itemBonuses(record, db):
    """Everything one item record gives you, in the optimiser's vocabulary."""
    out = starBonuses(record, db)
    for name, value in itemExtras(record, db).items():
        out[name] = out.get(name, 0) + value
    return out


def locationsFor(record):
    return sorted({name for flag, name in SLOTS.items() if record.get(flag)})


def grantedAbility(record, db):
    """The Ability an item's granted skill amounts to, or None.

    An item skill usually has no templateAutoCast - it is a button you press,
    which the optimiser calls a manual trigger, and its class says so. Where the
    item does name a controller it is the same kind of record the devotion procs
    use, so the trigger and the chance are read the same way.
    """
    path = record.get("itemSkillName")
    skill = db.read(path) if path else None
    if not skill:
        return None
    records = procRecords(skill, db)
    bonuses = procBonuses(records, db, triggered=True)
    if not bonuses:
        return None
    skillClass = skill.get("Class", "")
    controller = record.get("itemSkillAutoController")
    trigger, chance = (None, None)
    if controller:
        trigger, chance = triggerAndChance([{"templateAutoCast": controller}])
    if WPS_CLASS in skillClass:
        kind, trigger = "wps", "attack"
        weight = lastValue(firstOf(records, "skillChanceWeight", 0)) or 0
        chance = round(float(weight) / 100.0, 2) or 1
    else:
        kind = "buff" if "Buff" in skillClass or "Passive" in skillClass else "attack"
    conditions = {"type": kind,
                  "trigger": trigger or triggerFor(skillClass), "chance": chance or 1,
                  "skillClass": skillClass}
    # The same geometry devotiongen emits, and for the same reason: how many
    # enemies a skill reaches is worked out at scoring time from the area it
    # covers. This was simply missing, so every skill an item granted was scored
    # single-target - Brutal Slam states a 4.5 metre radius and was being given
    # one enemy where the rule gives it nearly three.
    geometry = geometryFor(records)
    for key in ("radius", "projectiles", "sparkMaxNumber", "waveDistance",
                "waveStartWidth", "waveEndWidth"):
        if geometry.get(key):
            conditions[key] = round(float(geometry[key]), 2)
    for field, name in (("skillCooldownTime", "recharge"), ("skillActiveDuration", "duration")):
        value = firstOf(records, field, 0)
        if value:
            conditions[name] = round(float(value), 2)
    return db.name(skill) or "Item Skill", conditions, bonuses


def levelFor(record):
    """Character level the game asks for before the piece can be worn."""
    return int(lastValue(record.get("levelRequirement", 0)) or 0)


def itemLiteral(name, bonuses, locations, ability=None, level=0):
    parts = ["%r" % name, dictLiteral(bonuses), repr(locations)]
    if ability:
        label, conditions, abilityBonuses = ability
        parts.append("Ability(%r, %s, %s)"
                     % (label, dictLiteral(conditions), dictLiteral(abilityBonuses)))
    elif level:
        parts.append("None")           # keep level in its own position
    if level:
        parts.append("%d" % level)
    return "Item(%s)" % ", ".join(parts)


def collect(db, *classes):
    """Named records of these classes, best version of each name winning.

    The same item exists once per level bracket and again under records/items/
    upgraded, all sharing one name tag; what tells them apart is itemStyleTag,
    which is where the Empowered and Mythical in an item's name comes from. The
    highest item level is the one worth having.
    """
    best = {}
    for path in db.ofClass(*classes):
        record = db.read(path)
        name = db.name(record)
        if not name:
            continue
        style = db.tags.get(record.get("itemStyleTag") or "", "")
        full = ("%s %s" % (style, name)).strip()
        level = float(lastValue(record.get("itemLevel", 0)) or 0)
        if full not in best or level > best[full][0]:
            best[full] = (level, record)
    return {name: record for name, (_, record) in best.items()}


def setBonuses(db):
    """Set bonuses, one entry per piece count, named "<Set> (n)".

    A set states every bonus as an array indexed by how many pieces are worn
    less one, so Beastcaller's Regalia's [0, 5, 5, 5] defensive ability means
    nothing for one piece and 5 from the second onwards. Each count is emitted
    separately, matching the tiers the hand-written file wrote out by hand.
    """
    out = {}
    for path in db.under("records/items/lootsets/"):
        record = db.read(path)
        name = db.tags.get(record.get("setName") or "", "") if record else ""
        if not name:
            continue
        previous, granted = {}, False
        for pieces in range(1, len(record.get("setMembers") or []) + 1):
            tier = _atIndex(record, pieces - 1)
            total = itemBonuses(tier, db)
            # Each array holds the running total, so [0, 5, 5, 5] is 5 from the
            # second piece on rather than 5 more every piece. The optimiser adds
            # the tiers it has earned, so each one carries only what it adds.
            bonuses = {k: round(v - previous.get(k, 0), 2) if not isinstance(v, list) else v
                       for k, v in total.items()
                       if isinstance(v, list) or abs(v - previous.get(k, 0)) > 0.005}
            previous = {k: v for k, v in total.items() if not isinstance(v, list)}
            ability = None if granted else grantedAbility(tier, db)
            granted = granted or ability is not None
            if pieces > 1 and (bonuses or ability):
                out["%s (%d)" % (name, pieces)] = (bonuses, ability)
    return out


def _atIndex(record, index):
    """One tier of a set record, with its per-piece-count arrays collapsed.

    A pet bonus and a granted skill are gated on their own level array, so both
    are dropped from the tiers that have not earned them yet.
    """
    flat = {}
    for key, value in record.items():
        if isinstance(value, list) and value and not isinstance(value[0], str):
            flat[key] = value[index] if index < len(value) else 0
        else:
            flat[key] = value
    for level, gated in (("petBonusLevel", "petBonusName"), ("itemSkillLevel", "itemSkillName")):
        if level in record and not flat.get(level):
            flat.pop(gated, None)
    return flat


def generate(path="itemData.py", root=None):
    db = Database(root) if root else Database()
    import equipmentWanted

    lines = ['"""Generated from the Grim Dawn database - do not edit.',
             "",
             "Regenerate after a game patch with:  python devotion.py --regenerate",
             "",
             "Which named equipment appears here is chosen in equipmentWanted.py;",
             "components and augments are everything the game has.",
             '"""',
             "from dataModel import Item",
             "from ability import Ability",
             ""]

    counts = {}
    for label, recordClass in (("components", "ItemRelic"), ("augments", "ItemEnchantment")):
        entries = []
        for name, record in sorted(collect(db, recordClass).items()):
            locations = locationsFor(record)
            if not locations:
                continue
            entries.append("\t%s," % itemLiteral(name, itemBonuses(record, db), locations,
                                                 grantedAbility(record, db),
                                                 levelFor(record)))
        lines.append("%s = [" % label)
        lines.extend(entries)
        lines.append("]")
        lines.append("")
        counts[label] = len(entries)

    gear = collect(db, *GEAR_CLASSES)
    lines.append("equipment = {}")
    missing = []
    found = 0
    for name in equipmentWanted.WANTED:
        record = gear.get(name)
        if record is None:
            missing.append(name)
            continue
        # A single location is passed as a plain string, not a list: Item scales
        # a piece's armour by how much of your armour that slot is worth, and it
        # only does that when it can tell which slot it is.
        location = CLASS_SLOTS.get(record.get("Class"), "")
        lines.append('equipment[%r] = %s'
                     % (name, itemLiteral(name, itemBonuses(record, db), location or [],
                                          grantedAbility(record, db), levelFor(record))))
        found += 1
    sets = setBonuses(db)
    for name in equipmentWanted.WANTED_SETS:
        if name not in sets:
            missing.append(name)
            continue
        bonuses, ability = sets[name]
        lines.append('equipment[%r] = %s'
                     % (name, itemLiteral(name, bonuses, ["set"], ability)))
        found += 1
    counts["equipment"] = found
    counts["missing"] = missing

    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    return counts
