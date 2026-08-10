# Handoff

Read `NOTES.md` first - it is the real record and every claim below is expanded
there. This file is only what a new session needs to pick up without re-deriving
the picture.

## Where things stand

`master` at `c67e5f4`, in sync with origin. All eleven models load and solve,
`sandbox.py`, `savefile.py` and `devotion.py --new` are clean.

The theme is unchanged: **replace hand-chosen numbers with numbers the game
states.** A model now says what the save gets wrong and almost nothing else.
Ranks, gear bonuses, set tiers, modifiers, level and `+skills` are all derived;
what a model states is an override, and the comment beside it is what was
derived.

    python devotion.py <name> [--budget N] [--seeds N]
    python savefile.py [name [gear|stats]]
    python statpass.py [--write]     refresh the derived comments in every model

`statpass.py` implements the convention: a stat within 5% of derived is deleted
from the model, one further off keeps its value and gains a `# derived X ±Y%`
comment. It is idempotent. Run it after any change to what `sheetOf` derives.

## The open gaps, in the order I would take them

Measured against armitage's and gwyr's freshly read sheets. Everyone else's
sheet is older than their save and cannot arbitrate anything - check the file
date first, always:

    python -c "import savefile,os,time; [print(n, time.ctime(os.path.getmtime(i['path']))) for n,i in savefile.characters().items()]"

1. **Damage percentages, -18% to -42%.** The largest unexplained family and the
   one I have twice predicted a cause for and been wrong. Both fixes that did
   help were about *which skills count* - modifiers of counted skills, item
   toggles - so a third such category is plausible but unproven.
2. **Regeneration.** `health/s` -64%, `energy/s` -80%, on both fresh sheets.
   Systematic across characters, which is the signature that found the level
   term and the modifier rule. The percentages are applied now, so it is the
   base that is short.
3. **Fire retaliation -47% where physical is +1% and lightning -15%.** Physical
   landing exact means the formula is right and something type-specific is
   missing. Not Burning Weapons - that carries damage percentages.
4. **Armor.** Gwyr's fresh sheet lands at -2% on the game's stated rule, so the
   rule is right; armitage is -23% and it is *not* his shield, which grants no
   armor at all. Lochlan's -21% is against a stale sheet.
5. **Flat damage, -58% to -82%**, both characters.

Smaller and well-bounded:

- `applyDefensePriority` prices armor linearly. `combatformulas.dbr` says damage
  under your protection is reduced by the absorption and damage over it passes
  the excess through, so armor is worth much more up to the size of hits you
  take and much less after. A scoring change, not a derivation one.
- `itemAbilities` is built from `itemData`, whose `equipment` holds seventeen
  pieces - gear is not indexed. `sheetOf` sidesteps it by reading worn records
  directly, but a *rotation* naming a skill granted by unlisted gear will not
  resolve. Fix in `itemgen` if something needs it.
- `blockAbsorption` is unread; it is 100 on 361 of 367 shields.
- `attacks/s` cannot be derived. The weapon states a speed class and the gear a
  percentage, but seconds-per-swing is in the animation assets, and the game
  warns the two do not simply multiply. The weapon tooltip prints it.

Per character: pakse's save is **226 days old**, so nothing about him is
current; lachesis's sheet is stale and both are excluded from the
`LEVEL_ABILITY` fit. kieri, lachesis and lilith have bare-rate rotations with no
main attack. lethe has no default-attack replacer at all.

## Three things that cost me time

**Look for the record before fitting anything.** I fitted the per-level ability
gain across ten characters, got 14.84 at 13% rms, and wrote a careful note
saying it was the one fitted number in the project. `records/game/combatformulas.dbr`
states it as 12, along with the attribute conversions, the armor regions and the
hit formula. The fit had the shape right and the size wrong, and 14.84 was
silently absorbing a *different* missing term.

**The saves are live.** Lochlan's armor absorption read 84 one minute and 98 the
next with no code between - it was being played. I reported an exact match that
was a moving number. Check the mtime before believing any comparison.

**My predictions about where a gap would close were wrong twice running**, both
times plausible and both times confidently stated. The gaps that did close were
found by reading a record or being told a fact, never by reasoning about which
mechanism *ought* to be missing.

## What is worth asking for

Only the game can supply these, and each unblocks something specific:

- `attacks/s` off the weapon tooltip for hela, kieri, lachesis, lilith, lochlan
  and pakse - all are round numbers or an old whole-bar aggregate.
- Pakse loaded and saved, which is the only way anything about him becomes real.
- A fresh sheet for lachesis, and for anyone else before trusting their gaps.
- The buff list for any character being worked on. Armitage's - Counter Strike,
  Menhir's Bulwark, Vindictive Flame, Burning Weapons, Divine Guard, Field
  Command, Flame Touched - is what found two whole categories of missing skill.
