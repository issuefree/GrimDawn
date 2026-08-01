"""Rank pieces of gear against a character and show where the difference is.

The question this answers is the one that kept getting hand-written into
sandbox.py: I have these pieces, which should I wear? That used to mean typing
each candidate's stats out as an Item literal before anything could score it.
Items come from the game files now, so naming one is enough.

Names are matched loosely - case and punctuation are ignored, and a name that is
not an exact match is looked up as a substring, so "thundertouch" finds
Empowered Thundertouch Bracers.
"""
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


def fromDatabase(name):
    """Build an Item for any gear record the game has, named or not in itemData.

    equipmentWanted.py only lists the pieces worth keeping in the data file.
    Anything else in the game can still be asked about here without editing it.
    """
    import itemgen
    from gddata import Database

    db = Database()
    wanted = _key(name)
    best = None
    for full, record in itemgen.collect(db, *itemgen.GEAR_CLASSES).items():
        key = _key(full)
        if key == wanted or wanted in key:
            if best is None or key == wanted or len(key) < len(_key(best[0])):
                best = (full, record)
    if not best:
        return None
    full, record = best
    ability = itemgen.grantedAbility(record, db)
    return Item(full, itemgen.itemBonuses(record, db),
                itemgen.CLASS_SLOTS.get(record.get("Class"), "") or [],
                _ability(ability))


def _ability(spec):
    if not spec:
        return None
    from ability import Ability
    label, conditions, bonuses = spec
    return Ability(label, conditions, bonuses)


def resolve(names):
    """Turn what the user typed into Items, reporting anything not found."""
    known = index()
    found, missing = [], []
    for name in names:
        item = known.get(_key(name))
        if item is None:
            item = next((v for k, v in known.items() if _key(name) in k), None)
        if item is None:
            item = fromDatabase(name)
        if item is None:
            missing.append(name)
        else:
            found.append(item)
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
