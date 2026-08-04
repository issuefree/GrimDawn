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

## One "hits taken/s" cannot serve a boss and a pack

Retaliation is derived now, and its rate is "hits taken/s". But that is not one
number: a boss is a single slow heavy hitter and a pack is everything swinging
at once, so a retribution build's whole damage profile moves between the two
fights. armitage runs 20% retaliation at a quarter of a hit a second and 80% at
four, and the constellations change with it - Autumn Boar, Anvil and Tsunami at
boss rates against Wraith and Harvestman's Scythe at pack rates. Not a rescale:
a different answer.

This is exactly the question showBothFights already answers for enemy count, by
scoring the same solution against one enemy and against a room. It cannot be
answered the same way here. Enemy count is read during evaluation, so changing
it and re-scoring works; the retaliation weights are worked out once, in
loadModel, so a fight cannot change them.

sweepHitsTaken() in the sandbox is the stopgap - one process per rate, so each
gets an honest load. The real fix is for hits taken/s to be read where the
enemy count is read, which would let the boss and pack columns differ properly
and would make armor per-fight as well, since armor is counted against the same
figure.

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
or the bound skill's, which one in-game tooltip check settles, and on
`allAttacks/s` carrying only rates and no cooldowns.

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

## skillgen emits no parent/child links

`Ability.augment` and `Skill.childSkills` exist and are dead, because nothing
says which skill modifies which. The `onslaught1/2/3` naming plus `isCircular`
would give them.

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
