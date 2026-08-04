# Known modelling gaps

Things the optimiser gets wrong that are understood but not fixed. Each says
what breaks, what it costs, and what would fix it - so that picking one up does
not mean rediscovering it.

## Casters that make no weapon attack

**Status: partly fixed, and the remainder is structural.**

`applyDamagePriority` used to assume everything you deal goes through your
weapon: a point of flat X was worth `1 + X%/100` and a point of `X %` was worth
the sheet's flat X over a hundred. The held attack - the first entry in the
rotation - now supplies its weapon share and its own damage, so the split is
taken against what one cast actually delivers. A pure caster's gear flat prices
at zero and her percentages price against the spell.

What is still wrong, all of it visible in a hela run:

**`main attack %` comes out 0.** `swingPercent` expresses a cast as a percentage
of a bare swing, and divides by what one percent of a bare swing is worth. For a
caster that divisor is zero, so the unit does not survive the translation. The
consequence is that `mainAttackPercent` falls back to a bare 100% swing, so
every skill an item grants is priced against a swing she never makes - both what
pressing it costs her and whether it beats her own attack.

Fixing it means picking a different unit. "Percent of a bare swing" is the unit
the *game* quotes item skills in, which is why it was chosen; a caster needs
"damage per cast" and the two do not convert without knowing the weapon.

**`weapon damage %` dominates.** It is 7948 of hela's 10871 - 73% of the build -
because her 1700 flat aether is worth a great deal to a weapon-damage proc even
though her beam never touches it. That is defensible in principle and leans
entirely on whether she takes such a proc, which is the thing being optimised.
The model has no notion of "what fraction of my damage comes from weapon
attacks", and several of these questions reduce to it.

**Utility weights were never calibrated against damage priorities.** They are two
scales that only ever met by accident. A caster's damage priorities now buy much
less than they did, so `offense` and `attack speed` dominate her by default.

**`attacks/s` is doing duty as casts/s.** Mostly harmless - spells do trigger
attack-triggered devotions - but it also sets the DoT refresh interval in
`dotFactor`, and a channelled beam does not reapply a bleed the way a swing
does.

## One "hits taken/s" cannot serve a boss and a pack

**Half fixed.** The rate is derived now rather than stated: it is the same
circle `Ability.effectiveTargets` measures for a point-blank area effect, read
from the other end, so how many enemies are close enough to swing at you falls
out of density and playStyle. A tank takes 2.78 hits a second in a room, a
kiting archer 0.23, and one enemy is one hit a second whoever you are. The one
a second per enemy is measured - `characterAttackSpeed` has a median of exactly
1.000 across 3052 Monster records.

What is not fixed is that it cannot differ between the boss column and the pack
column. Enemy count is read during evaluation, so `showBothFights` can change it
and re-score; the retaliation and armor weights are worked out once in
`loadModel`, so a fight cannot change them. armitage runs 50% retaliation at one
hit a second and 74% at 2.78, and the constellations move with it - not a
rescale, a different answer.

`sweepHitsTaken()` in the sandbox is the stopgap: one process per rate, so each
gets an honest load. Sweep between the boss and pack figures for that playStyle
rather than round numbers.

The real fix is for the weights that depend on the fight to be worked out where
the fight is known. That would give proper boss and pack columns for retaliation
and for armor at once.

The one guess left in the chain is `ENGAGEMENT_RADIUS`, three metres. Monster
attack ranges live on their skills rather than their records, the same reason
`PHYSICAL_SHARE` is a guess.

## Retaliation builds

**Fixed.** `retaliationDamage` derives the flat and percentage weights the way
`rotationDamage` derives the attack ones, off flat retaliation per type on the
sheet times "% Retaliation Damage", at the rate you are hit. Retaliation keeps
its own multiplier and takes no attribute bonus, because the game's tooltip
says "% All Damage does not affect Retaliation damage".

The part that mattered was putting it on the same scale as the rotation. What
you deal by swinging against what you deal by being hit was the one balance
nobody could set honestly, since the two halves were hand-set in different
units. Both are damage a second per point now, so the split falls out.

What remains is which rate to use, above.

## Duration damage on pets and retaliation

`dotFactor` derives the refresh discount for your own flat damage from
`DOT_SECONDS` and your attack rate. `checkModel` still uses a flat half for
`pet X` and `X retaliation`. Both want their own derivation and neither has one:
a pet's swing interval is its own (`calculateBonus` already uses
`devotionderive.BASE_ATTACK_RATE + CHASE_SECONDS` for a pet's `[dps, seconds]`
pair), and retaliation is not reapplied by your attacks at all.

## autoCastEquation

`gameengine.dbr` carries `procRate * (1 + cooldown*81/100) * (1 - attackDuration*11/100)`
and nothing reads it. Blocked on two things: whether `cooldown` means the proc's
or the bound skill's, which one in-game tooltip check settles, and on the
resolved rotation carrying only rates and no cooldowns.

## Set bonuses are not extracted

`itemgen` does not read set records, so the Ultos' Storm bonuses at 2/3/4/5
pieces - including the Ultos' Wrath proc on the fifth - are invisible. lochlan
wears that set. They used to be hand-written in his model file; see the history
of `lochlan/lochlan.py` for what they said.

## Skills that yield no bonuses are dropped entirely

skillgen writes a Skill only if some level of it produced a bonus it could
read, so a skill whose whole payload is in fields the FLAT/DIRECT maps do not
cover vanishes rather than appearing empty. Wind Devil is the one that has come
up - a `Skill_TargetedSpawnPet` whose levelAbility returns `{}` - and lochlan
plays it, so his rotation has to carry a bare number where every other line
names a skill.

Worth a census: how many skills across the ten masteries produce nothing, and
which fields they have that nothing reads. The count is easy to get, since
skillsOf yields 33 for Soldier where skillData holds 27.

## Buff skills came out one rank long

**Fixed.** `skillgen` read a skill's ladder off the node the tree points at, and
a buff skill does not keep it there - `curse1.dbr` states no `skillMaxLevel` at
all, while `curse1_buff.dbr` states 10 and 20. Fifty of the three hundred skills
came out with a single level, and `Skill.getAbility` clamps, so a model naming
Blood of Dreeg at 8 silently got it at 1. `topLevel` now takes the ladder from
the first record in the chain that states one, the same way `skillsOf` takes the
name; 32 skills grew their real ladders and the remaining 18 are transmuters,
which genuinely take one point.

No score moved. The four affected skills in the current models - Curse of
Frailty, Bonechilling Cry, Blood of Dreeg and Rallying Cry, in fenris and morena
- are buffs that deal no damage and are pressed slower than they recharge, so
neither the damage split nor the rate depended on their rank. It matters for the
transcription below: until this, a rank written down for one of those was thrown
away on load.

## skillgen emits no parent/child links

`Ability.augment` and `Skill.childSkills` exist and are dead, because nothing
says which skill modifies which. The `onslaught1/2/3` naming plus `isCircular`
would give them.

`modelspec.isModifier` reads the half of this that the records do state: a
`SkillSecondary_` fires with its parent and a passive or a toggle is not a press,
so a rotation can say which of its entries are modifiers without saying what they
modify. It does not need to, because they all hang off the one held attack. A
model that wanted Blood Burst counted against Dreeg's Evil Eye rather than
against the attack it holds down would need the real link.

## Reading skills out of the save files

`savefile.py` decodes a player.gdc header - name, mastery pair and level - and
that much works for all eleven characters. The body does not.

The obfuscation is understood and implemented: the first word is a seed XORed
with 0x55555555, a 256-entry table is built from it by rotating right one bit
and multiplying by 39916801, and every read XORs against a running key which is
then advanced by table[b] for each ciphertext byte consumed. The header proves
it - `tagSkillClassName0207` does not fall out of a wrong key.

What is not understood is what follows the header. Blocks should start with a
small id and a length; nothing plausible appears at any offset, under any
combination of key-updating on the id and length, and a byte-by-byte scan of
the whole file finds no printable string at all - in a file that certainly
contains item record paths. So the key state diverges at the header boundary in
a way the header itself gives no sign of. Candidates not yet tried: extra
header fields in format version 2, or a second seed for the body.

Worth finishing. It would take transcription out of the loop entirely - skills,
devotions and gear, not just the level - and the level check it already does
caught gwyr's model sitting a level behind.

## Models that do not load

`kieri` and `lachesis` state no `devotionPoints`, which is not a thing that can
be inferred. `gwyr` and `lethe` are scaffolds with a level and nothing else.

## Per-character data still outstanding

Not modelling gaps - transcription. Every one of these is a number only the game
can supply.

| character | needs |
|---|---|
| all with a rotation | **skill ranks.** Every rank is a stub except fenris's four and hela's two. Every damage weight is priced against them |
| kieri, lachesis | `devotionPoints`. Neither loads without it |
| kieri, lachesis, lethe, lilith | their rotations - each is bare rates, so no skill is named and no main attack can be read |
| armitage, pakse | confirm the held attack, which is now whichever skill the rotation lists first. Fire Strike and Righteous Fervor are guesses; pakse's matters more, because his weapon pool claims 100% of swings at stub ranks so Righteous Fervor never fires |
| hela, kieri, lachesis, lethe, lilith, lochlan, pakse | `attacks/s` off the sheet. All are round numbers or the old whole-bar aggregate. The three that have been read moved 3 -> 1.64, 3 -> 1.91 and 2 -> 2.43 |
| everyone | resistances. `applyDefensePriority` derives nothing for `resist` because no sheet carries them |
| armitage | `hits taken/s` if 2.78 is wrong - it drives 76% of what he deals |
| fenris | is his slam Brutal Slam off Severed Claw or the plainer Slam off Chipped Claw? Same cooldown, different damage |
| nyx | level 24, Occultist/Shaman, no model at all |
