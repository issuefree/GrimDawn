"""Rank pieces of gear against a character and show where the difference is.

The question this answers is the one that kept getting hand-written into
sandbox.py: I have these pieces, which should I wear? That used to mean typing
each candidate's stats out as an Item literal before anything could score it.
Items come from the game files now, so naming one is enough.

Names are matched loosely - case and punctuation are ignored, and a name that is
not an exact match is looked up as a substring, so "thundertouch" finds
Empowered Thundertouch Bracers.
"""
import json
import os
import re

from dataModel import Item

# what a slot is worth is asked of the item, but a weapon has to be told which
# hand it is in for its ability's shape to resolve
SLOT_ALIASES = {"hands": "arms", "weapon": "sword", "2h": "twohand"}


def _key(name):
    return re.sub(r"[^a-z0-9]+", "", name.lower())


def index():
    """Every named item the data files know, by simplified name."""
    import itemData
    out = {}
    for item in itemData.components + itemData.augments:
        out.setdefault(_key(item.name), item)
    for name, item in itemData.equipment.items():
        out[_key(name)] = item
    return out


CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".gearindex.json")


def _databaseStamp():
    """What the cache is keyed on: the archives it was built from."""
    import gddata
    stamp = []
    for rel in gddata.LAYERS + gddata.TEXT_LAYERS:
        path = os.path.join(gddata.GD, rel)
        if os.path.exists(path):
            stamp.append("%s:%d" % (rel, os.path.getmtime(path)))
    return "|".join(stamp)


def gearIndex():
    """Simplified name -> record path, for every named piece of gear.

    Finding this out means reading every one of some eight thousand gear
    records, which is half a minute, so it is done once and kept. The cache is
    keyed on the archives it was built from, so a game patch rebuilds it and
    nothing else does.
    """
    stamp = _databaseStamp()
    try:
        with open(CACHE, encoding="utf-8") as handle:
            cached = json.load(handle)
        if cached.get("stamp") == stamp:
            return cached["gear"]
    except (OSError, ValueError, KeyError):
        pass

    import itemgen
    from gddata import Database

    print("  building the gear index (once per game patch)...")
    db = Database()
    best = {}
    for path in db.ofClass(*itemgen.GEAR_CLASSES):
        record = db.read(path)
        name = db.name(record)
        if not name:
            continue
        style = db.tags.get(record.get("itemStyleTag") or "", "")
        full = ("%s %s" % (style, name)).strip()
        level = float(record.get("itemLevel") or 0)
        if full not in best or level > best[full][0]:
            best[full] = (level, path)
    gear = {_key(full): [full, path] for full, (_, path) in best.items()}
    try:
        with open(CACHE, "w", encoding="utf-8") as handle:
            json.dump({"stamp": stamp, "gear": gear}, handle)
    except OSError:
        pass       # a read-only checkout is slower, not broken
    return gear


def fromDatabase(names):
    """Build Items for gear the data files do not carry, one lookup each.

    equipmentWanted.py only lists the pieces worth keeping in itemData.py.
    Anything else in the game can still be asked about without editing it.
    """
    gear = gearIndex()
    matched = {}
    for name in names:
        wanted = _key(name)
        hit = gear.get(wanted)
        if hit is None:
            candidates = [v for k, v in gear.items() if wanted in k]
            hit = min(candidates, key=lambda v: len(v[0])) if candidates else None
        if hit:
            matched[name] = hit
    if not matched:
        return {}

    import itemgen
    from gddata import Database

    db = Database()
    out = {}
    for name, (full, path) in matched.items():
        record = db.read(path)
        if not record:
            continue
        out[name] = Item(full, itemgen.itemBonuses(record, db),
                         itemgen.CLASS_SLOTS.get(record.get("Class"), "") or [],
                         _ability(itemgen.grantedAbility(record, db)))
    return out


def _ability(spec):
    if not spec:
        return None
    from ability import Ability
    label, conditions, bonuses = spec
    return Ability(label, conditions, bonuses)


def resolve(names):
    """Turn what the user typed into Items, reporting anything not found."""
    known = index()
    found, missing, unknown = [], [], []
    for name in names:
        item = known.get(_key(name))
        if item is None:
            item = next((v for k, v in known.items() if _key(name) in k), None)
        if item is None:
            unknown.append(name)
        else:
            found.append(item)
    # one pass over the database for everything the data files did not have
    built = fromDatabase(unknown) if unknown else {}
    for name in unknown:
        if name in built:
            found.append(built[name])
        else:
            missing.append(name)
    return found, missing


def compare(model, names, slot=None):
    """Print the pieces ranked, and what each bonus is worth on each."""
    items, missing = resolve(names)
    for name in missing:
        print("  no item found called %r" % name)
    if not items:
        return

    scored = []
    for item in items:
        where = SLOT_ALIASES.get(slot or "", slot) or (
            item.location if isinstance(item.location, str) else
            (item.location[0] if item.location else ""))
        scored.append((item.evaluate(model, where), item, where))
    scored.sort(key=lambda row: row[0], reverse=True)

    width = max(len(item.name) for _, item, _ in scored)
    width = min(max(width, 12), 40)
    print("\n  %-24s %s" % ("", "  ".join(("%*s" % (width, item.name[:width]))
                                          for _, item, _ in scored)))
    print("  %-24s %s" % ("slot", "  ".join("%*s" % (width, where) for _, _, where in scored)))

    # every bonus any of them carries that this character actually scores
    rows = {}
    for _, item, _ in scored:
        for bonus in item.bonuses:
            if model.get(bonus):
                rows[bonus] = True
        if item.ability:
            for bonus in item.ability.bonuses:
                if model.get(bonus):
                    rows[bonus] = True
    for bonus in sorted(rows, key=lambda b: -max(_worth(item, b, model)
                                                 for _, item, _ in scored)):
        cells = ["%*d" % (width, _worth(item, bonus, model)) for _, item, _ in scored]
        print("  %-24s %s" % (bonus[:24], "  ".join(cells)))
    if not rows:
        print("  none of these carry anything this character scores")
    print("  %-24s %s" % ("TOTAL", "  ".join("%*d" % (width, value)
                                             for value, _, _ in scored)))

    if len(scored) > 1 and scored[0][0]:
        lead = scored[0][0] - scored[1][0]
        print("\n  %s wins by %d (%.0f%%)"
              % (scored[0][1].name, lead, 100.0 * lead / scored[0][0]))


def _worth(item, bonus, model):
    """What one bonus on one item is worth to this character."""
    value = item.bonuses.get(bonus, 0)
    if isinstance(value, list):
        value = value[0]
    total = model.get(bonus) * value
    if item.ability and bonus in item.ability.bonuses:
        carried = item.ability.getTotalBonus(bonus)
        if isinstance(carried, list):
            carried = carried[0]
        total += model.get(bonus) * carried * item.ability.effective
    return total
