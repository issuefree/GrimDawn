# Known modelling gaps

Things the optimiser gets wrong that are understood but not fixed. Each says
what breaks, what it costs, and what would fix it - so that picking one up does
not mean rediscovering it.

## Casters that make no weapon attack

**Status: partly fixed, and the remainder is structural.**

`applyDamagePriority` used to assume everything you deal goes through your
weapon: a point of flat X was worth `1 + X%/100` and a point of `X %` was worth
the sheet's flat X over a hundred. Naming `main attack` now supplies the
attack's weapon share and its own damage, so the split is taken against what one
cast actually delivers. A pure caster's gear flat prices at zero and her
percentages price against the spell.

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

## Retaliation builds

`damagePriority` splits one preference into a flat weight and a percentage
weight using the sheet, and nothing does that for retaliation. `retaliation` and
`retaliation %` are two hand-written weights with no relationship to each other,
and `X retaliation` falls back to `retaliation` times a duration factor with no
multiplier at all - deliberately, because the game's own tooltip says "% All
Damage does not affect Retaliation damage".

But "+% Retaliation Damage" does affect it, and that is the split nobody
derives. armitage carries 450% retaliation on his sheet and no flat retaliation
figure at all, so there is nothing to derive it from even if the code asked -
the same shape as lochlan's missing flat damage. His retaliation lines are
20716 of his 88696, so this is not a corner.

What would fix it: flat retaliation per type on the sheet, then the same
treatment damage gets - a `retaliationPriority` block, or retaliation folded
into `damagePriority` as `X retaliation` entries.

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
or the bound skill's, which one in-game tooltip check settles, and on
`allAttacks/s` carrying only rates and no cooldowns.

## Set bonuses are not extracted

`itemgen` does not read set records, so the Ultos' Storm bonuses at 2/3/4/5
pieces - including the Ultos' Wrath proc on the fifth - are invisible. lochlan
wears that set. They used to be hand-written in his model file; see the history
of `lochlan/lochlan.py` for what they said.

## skillgen emits no parent/child links

`Ability.augment` and `Skill.childSkills` exist and are dead, because nothing
says which skill modifies which. The `onslaught1/2/3` naming plus `isCircular`
would give them.

## Models that do not load

`kieri` and `lachesis` state no `devotionPoints`, which is not a thing that can
be inferred. `gwyr` and `lethe` are scaffolds with a level and nothing else.
