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

## Anything that lands once was priced against attacks/s

**Fixed.** A point of flat damage on the sheet is delivered by weapon damage, so
what delivers it is `sum(rate * weapon%)` over the rotation - `modelspec.
deliveryRate`. `applyDamagePriority` divided by `attacks/s` instead, for both
`triggered X` and `weapon damage %`, which are the two weights priced per
delivery rather than per second.

The two are only the same number when the whole bar is one plain 100% swing, and
no model is:

    armitage  2.41 attacks/s -> 5.49 delivered/s   2.28x
    pakse     2.00            -> 5.32              2.66x
    fenris    1.64            -> 3.82              2.33x
    gwyr      2.43            -> 4.25              1.75x
    lochlan   2.00            -> 3.50              1.75x
    morena    1.88            -> 3.11              1.65x

So every proc's damage and every proc's weapon damage was worth between 1.65 and
2.66 times what it delivers. It showed up as Hyrian's Glare - 85% weapon damage
on one star - taking 61% of morena's solution, which is what prompted looking.
It is 52% now against a pack and 34% against a boss.

Nothing else moved by much, because the error was uniform across every proc: it
changed the balance between what a devotion adds and what the sheet already has,
not the ranking within the devotions. armitage barely moved at all.

hela is untouched. Her weights come from the hand-stated path, where the flat
weights are built per cast off `mainAttackDamage` rather than per second off a
rotation, and whether the same divisor is wrong there has not been checked.

## Resistance had no cap and no per-type curve

**Fixed.** `applyDefensePriority` took the mean of your ten resistances and
derived one `resist` weight from `health / (100 - mean)`. Two things wrong with
that. The curve is steep, so a mean is not a summary of it - at 20 fire and 79
cold a point of cold is worth four points of fire, and one number said they were
the same. And the game caps resistance at 80, where a point is worth nothing at
all, which nothing in the model knew.

Per type now, with `MAX_RESIST = 80` and `"max <type> resist"` on the sheet
raising it. lochlan sits at the cap on fire, cold, lightning and pierce - worth
nothing - and at 6 aether and 14 chaos, worth 28 and 31.

The cap is not in the records. `gameengine.dbr` names a dozen caps for run
speed, attack speed and cast speed and not this one, so 80 is stated in
modelspec beside `PHYSICAL_SHARE` and `ENGAGEMENT_RADIUS` as a number the game
documents and the data does not.

`gddata` now reads `defensive<Type>MaxResist` as `max <type> resist`. That is
what raises the cap, and it is a different stat from the resistance itself -
nine constellations and six items grant it and none of them scored a thing for
it. It is priced as the mirror of the above: worth a point of resistance once
you are at the cap, worth nothing below it, because below it the cap is not what
is stopping you.

What is still hand-set is a resistance the sheet does not carry. lochlan states
nine and not physical, so `physical resist` is the one weight left in his file.

## The sheet's damage is already multiplied

**Fixed, and measured against the game.** Grim Dawn computes damage as
`flat * (1 + X%/100)` and the character sheet shows the left side *already
multiplied*. So lochlan's `"lightning": 5000` beside `"lightning %": 1138` is
not 5000 flat waiting for a multiplier - it is what 403 flat has already become.
Everything downstream multiplied it a second time.

One Primal Strike with Torrent and Storm Surge on it, 309% weapon damage,
against the game's own damage breakdown:

    lightning   242408 before    23391 after    22000 in the game

Six percent, and lightning is 88% of what he deals. The reading also settles
that his breakdown is taken uncharged like the sheet: charged, Savagery's +72%
and +37 flat put the model at 26293, which is what he would actually hit for.

`unmultiplyFlat` divides it back out once at load, before anything prices a
damage type, so the rotation's damage, the weapon damage weight and what one
swing is worth all read a number the game's equation would recognise. The
percentages are untouched - they were always what they said.

What this moves is the balance between flat and percentage. A point of gear flat
was always priced right, because a point of it really does become `multiplier`
more damage; it is the percentage weight that was overstated, by the size of the
multiplier itself - ten to sixteen times on most of these models. Every solution
had been buying `+% damage` stars over flat ones on a false rate.

Scores move accordingly and are not comparable across the change: gwyr 36415 ->
21870, morena 7261 -> 4436, lochlan 83277 -> 121795. The splits move too, and
towards what the characters look like - gwyr's fire and burn separate from 60/31
to 49/36, and morena's bleed and pierce swap places.

The three types beyond lightning are still out by two or three: physical is
over, which a conversion he carries would do, and the two duration types are the
difference between damage a second and damage a tick. Worth chasing with a
second measurement.

`applyDamagePriority` - hela's hand-stated path - reads the corrected sheet too,
since the correction is upstream of both paths.

## The damage chain, checked against the game

lochlan's Primal Strike, with Torrent and Storm Surge on it, at 309% weapon
damage, against the breakdown the game gives:

    type          model  measured   ratio
    physical       1324      1000    1.32
    lightning     25264     22000    1.15
    electrocute    3297      2500    1.32
    bleed          1369      1000    1.37
    TOTAL         31254     26500    1.18

Uniformly a fifth to a third over, with no type out of line - which is what a
sheet carrying estimates looks like, and not what a modelling error looks like.
Getting here took three corrections and two wrong guesses, and the wrong guesses
are worth recording because each looked right:

**The sheet's damage is already multiplied.** Before this the same skill read
242408 lightning against 22000. Fixed, and confirmed twice - the second time by
Stormcaller's Pact, whose tooltip reads ~1400 where the record's 30/s at rank 8
times lochlan's own 15.70 electrocute multiplier gives 1413.

**Conversion moved nothing.** 51% physical to lightning was priced as a weight
and never applied, so physical read 2702 against 1000.

**Electrocute was the last hold-out at 2.04, and it was not a units problem.**
Two guesses missed: that the sheet's 500 electrocute was a double count of the
skill's own, and that the gap was a damage-a-second against damage-a-total
mix-up. It was neither. The 500 is Stormcaller's Pact, real and correctly on the
sheet, and the Pact is its own damage over time rather than something Primal
Strike carries - so it does not belong in that skill's number at all. Take it
out and electrocute joins the cluster at 1.32.

Two things the game does that are worth keeping straight, since both cost time
here. The sheet reports a damage over time as a **rate** and a skill tooltip
reports it as the **total over its duration** - lochlan's 500 and ~1400 are the
same effect, three seconds apart. And the sheet is read in town, so it carries
the three toggles that are up there and nothing else.

What is not resolved is whether flat damage over time on the sheet should be
scaled by a skill's weapon damage percentage the way flat hit damage is. The
model scales it. It does not matter for the numbers above, because the one type
it would have moved is the one that turned out not to belong.

## Damage conversion was a weight and nothing else

**Fixed.** `conversions()` gave every "X to Y" name to the weight vocabulary, so
a devotion granting conversion could be priced - but a conversion *you already
have* did nothing whatever to what the build deals. lochlan converts 51% of his
physical to lightning off his weapon and the model was scoring all of it as
physical.

`rotationDamage` moves it now, before either multiplier applies, which is the
order the game uses and the whole reason conversion is worth having: the
converted share takes the target's percentage instead of the source's. For
lochlan that is physical's 10.7 traded for lightning's 14.2.

Two details worth keeping. Conversions out of one type come off its whole share
at once, so two of them cannot each take half of what the other left, and they
normalise at 100% because you cannot convert more of a type than you have. And a
point of gear flat of a converted type is worth its own multiplier for the share
that stays plus each target's for what it becomes, which is what `dFlat` now
carries.

The sheet does not show conversion, so it has to be stated - it is a stat, not a
weight, and the two happen to share a spelling.

Against the same Primal Strike measurement, physical goes from 2702 to 1324
against 1000 in the game. Lightning goes the other way, 23391 to 25264 against
22000, because it now receives what physical gave up. The split is much closer;
the total is not, and both are about 25% over.

**What is still out.** Three types are over by 30% to 100% - physical 1324
against 1000, electrocute 5101 against 2500, bleed 1369 against 1000 - on a
build where they are 2%, 13% and 7% of the damage. Lightning at 77% lands within
15%. The two duration types are the suspicious pair, and one more reading would
settle them: whether the game's breakdown reports a damage-over-time as its total
over the duration or as damage a second. At three seconds that is the whole
factor.

## The sheet is read in town, so no temporary buff is on it

The character sheets in these models are read in town with only passive buffs
up. That is the right way to read them - it is repeatable - but it means nothing
the rotation presses is in the numbers, and the model has to supply it.

**Fixed for charged replacers.** Savagery and Righteous Fervor state their flat
and percentage damage as charge bonuses: added in full from the first charge,
kept while any charge is up, and applied to every weapon attack you make, a
weapon pool skill included. `rotationDamage` counted them as damage the
replacer's own swing deals, at the replacer's own rate. They ride the whole
rotation's weapon delivery rate now, and their percentages join the multiplier
the sheet cannot carry.

The records draw the line rather than a guess: `Skill_WeaponPool_ChargedScaling`
carries `skillChargeMultipliers`, where Fire Strike has no charge fields at all,
Onslaught has a combo counter and Cadence a two-charge finale with no
multiplier. So it is exactly those two skills.

It only shows once there is a pool. lochlan's claims 61%, so Savagery swings
0.69 times a second against 3.68 weapon deliveries and its flat lightning was
counted at a fifth of what it lands - 84526 -> 83277, the drop being his
lightning % rising by Savagery's 72 on top of the sheet's 930 and rescaling
everything against it. pakse is sharper: his pool claims every swing, so
Righteous Fervor was dropped from the rotation outright and took its damage with
it. It is kept at a rate of nothing now, for its charge bonuses alone, and his
burn appears for the first time - 47118 -> 47166.

The charge multiplier is a different thing and is not modelled: up to 120% more
at nine charges, applying to the replacer's own damage only, so it does not
travel to a weapon pool skill.

**Not fixed for everything else.** Every other buff in a rotation is in the same
position and none of them is handled: Blood of Dreeg, Overguard, Ascension, War
Cry, Rallying Cry, Pneumatic Burst. Their damage is counted at their own press
rate, which is roughly right for damage they deal themselves and wrong for
damage they hand your attacks; their armor, health, resistances and offensive
ability are not counted at all, because nothing adds a buff's non-damage bonuses
to the sheet. armitage's Overguard is invisible to his own model.

Doing it properly wants an uptime: a buff with a 60 second duration on a 24
second cooldown is always up, one at 12 on 24 is up half the time, and both
numbers are on the records now that `levelAbility` reads timing across the
chain.

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

**Mostly fixed.** skillgen wrote a Skill only if some level produced a bonus it
could read, so sixteen skills whose payload is in fields the FLAT/DIRECT maps do
not cover vanished rather than appearing empty - and a rotation naming one was
told there was no such skill. Frenzied Cry is the sharpest case: its whole
record is `skillCooldownTime: -4.0` and not one other number.

A skill is now kept if it states a recharge, a recharge change or a duration,
which brought back seven: Frenzied Cry, Runic Seal, Undead Legion, Unstable
Anomaly, Blade Spirit, Wind Devil and Summon Guardian of Empyrion. Wind Devil is
the one lochlan plays, so his rotation no longer has to carry a bare number.

Nine are still dropped and all nine are transmuters whose payload is a damage
conversion or a behaviour change with no number attached:

    Skyfire Grenado, Ring of Frost, Tainted Power, Corrupted Storm,
    Dreeg's Reproach, Scion of Dreeg, Covenant of Ch'thon,
    Blight of Ch'thon, Talons of Ch'thon

Those want the conversion fields read, which is a different job from this one.

## Buff skills kept their timing where they kept their name

**Fixed.** A `Skill_BuffRadius` states its cooldown and duration on the buff
record it delegates to, not on the node the tree points at. `rallyingcry1.dbr`
carries neither; `rallyingcry1_buff.dbr` carries 12 seconds and 60. `levelAbility`
read the node alone, so ten skills looked like they had no cooldown at all -
Rallying Cry, Bonechilling Cry, Blood of Dreeg, Word of Renewal, Ill Omen,
Siphon Souls among them - and a rotation naming one either fell back to the
press interval or was told nothing said how often it fired.

It reads across the chain now, the same way `topLevel` and `skillsOf` do. fenris
had three rates wrong on this: he says he presses Bonechilling Cry every 3
seconds against a real 6, and Blood of Dreeg and Rallying Cry every 3 and 4
against a real 12.

A modifier is the exception and reads its own record only. Its
`skillCooldownTime` is a change to what it modifies rather than a cooldown of
its own, so it is emitted as `recharge change` and `resolveRotation` adds it to
the host: Rallying Cry is 12 seconds, or 8 with Frenzied Cry nested in it. Twelve
modifiers take time off and five add it - Focused Gaze makes Dreeg's Evil Eye a
charged shot and costs four seconds - so it is a sum rather than a discount.
Reading down the chain here would have been wrong: Spectral Wrath delegates to a
buff whose 0.5s is that buff's timing and nothing Spectral Binding gains.

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

## Two skills carrying one damage type

**Fixed.** The main attack was walked twice - once in `checkModel` to price a
swing against a granted skill, once in `mainAttackDamage` to price the damage
weights - and the two accumulated flat damage differently. `checkModel` kept the
first value per type and `mainAttackDamage` summed. gwyr is the case: Fire Strike
carries 55 fire and Brimstone adds 60, which the game adds, so a swing was being
measured at 55 while the weights were built on 115.

`modelspec.mainAttack` is the one walk now, and `addFlat` says what adding means
in each of `calculateBonus`'s two units - numbers on the hit sum, `[dps, seconds]`
pairs sum their damage over the longer of the two windows, and a type arriving as
both is refused rather than converted. No record in the game does that, and the
load warns by name if one ever does.

gwyr's `main attack %` went 178.7 -> 180.3. Nothing else moved, and no total did.

## Which skill a modifier modifies

**Fixed.** `isModifier` said an entry was not a press; nothing said what it
modified, so every modifier was attached to the attack you hold down. That is
right for Open Wounds and wrong for Fault Line, and the two are indistinguishable
without the link. Ten skills the current models press have modifiers in the data
- Leap, Ring of Steel, Shadow Strike, Amarasta's Blade Burst, War Cry, Judgment,
Aegis of Menhir, Primal Strike, Flashbang, Inquisitor Seal - and each would have
had its modifier's damage credited to the held attack, inflating `main attack %`
and every weight priced against a swing.

Nothing on a modifier's record names its parent, but the tree's record names do:
`onslaught2` is Open Wounds and `leap2` is Fault Line. `skillgen.parentStems`
takes that apart and `skillgen` emits the parent, which fills in the
`Skill.parentSkillName` and `Skill.childSkills` that had been dead since they
were written. 129 of 309 skills carry one.

A zero-padded number is deliberately not a family: `passive01` through
`passive04` are four separate skills a mastery grants, so reading Form of the
Beast as a child of `passive01` would invent a link. Five modifiers cannot be
placed at all - two of them because the game misspells `natureblessing1` as the
parent of `naturesblessing2` - and `--regenerate` names them rather than
guessing.

A modifier goes inside the entry for the skill it modifies:

    ("Leap", 8, 1.5, [("Fault Line", 8)])
    ("Onslaught", 1, [("Open Wounds", 3), ("Endless Rage", 1)])

The nesting is the link, so there is nothing to spell and nothing to keep in step
with a name written elsewhere. The elements after the name are read by type
rather than by position, so a skill with modifiers and no press interval leaves
no hole to count past.

The derived parent is what checks the nesting rather than what decides it: a
modifier nested under the wrong skill says so, and one left at the top level is
told which entry to move inside. That keeps the derivation earning its place
without it being the only way to say where something goes - which matters for the
five it cannot place, and for whatever a mod spells differently.

`Ability.augment` is still dead.

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
| all with a rotation | **`+skills` off the gear** - `{"all": 1, "Berserker": 2}`. Ranks in a rotation are what you spent; the gear is stated once and added on load |
| all with a rotation | **skill ranks.** Every rank is a stub except fenris's four and hela's two. Every damage weight is priced against them |
| kieri, lachesis | `devotionPoints`. Neither loads without it |
| kieri, lachesis, lethe, lilith | their rotations - each is bare rates, so no skill is named and no main attack can be read |
| armitage, pakse | confirm the held attack, which is now whichever skill the rotation lists first. Fire Strike and Righteous Fervor are guesses; pakse's matters more, because his weapon pool claims 100% of swings at stub ranks so Righteous Fervor never fires |
| hela, kieri, lachesis, lethe, lilith, lochlan, pakse | `attacks/s` off the sheet. All are round numbers or the old whole-bar aggregate. The three that have been read moved 3 -> 1.64, 3 -> 1.91 and 2 -> 2.43 |
| everyone | resistances. `applyDefensePriority` derives nothing for `resist` because no sheet carries them |
| armitage | `hits taken/s` if 2.78 is wrong - it drives 76% of what he deals |
| fenris | is his slam Brutal Slam off Severed Claw or the plainer Slam off Chipped Claw? Same cooldown, different damage |
| nyx | level 24, Occultist/Shaman, no model at all |
