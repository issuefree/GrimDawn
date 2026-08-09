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

## A percentage multiplies what the total came from

**Fixed where the percentage is stated, which is one stat on one model.**

`health %` was priced as one percent of the health on the sheet. A further point
does not multiply the total, it multiplies what the total came from - so it is
worth `total / (1 + what you already have)`, exactly as `unmultiplyFlat` divides
the multiplier back out of damage.

The wrong turn is worth keeping. lochlan's sheet says 10178 health and the game
also shows a "base health" of 1070, so the first fix priced a percentage point
at 10.7. That is base from level alone: his Physique is 752, which is another
1880 before any gear, and a percentage multiplies all of it. At his +31% the
answer is `10178 / 1.31 / 100` = 77.7 - where the total said 101.8 and base said
10.7. The original was 31% high and the correction was seven times low.

The records do not state any of this. `gameengine.dbr` carries one equation and
it is `autoCastEquation`; everything else under `records/game` is item cost and
attribute requirements. So this is read off the character, not derived.

It applies to all eight stats that take a percentage - physique, cunning, spirit,
offense, defense, health, energy, armor - and `"<stat> %"` in stats says what you
already carry, the same key `"lightning %"` uses and for the same reason. Where
it is missing the weight falls back to the total and the load names which:

    note: no "physique %", "cunning %", "spirit %", "offense %", "defense %",
    "energy %", "armor %" stated

lochlan's health % goes 254 -> 194 and he goes 58342 -> 61558.

**How much the rest is worth.** None of the eight is on the character sheet -
they have to be read off gear - so it matters which are worth the trouble. What
each actually buys in a solved build, across five models:

    armitage  armor %   11.1%   health %  5.7%   defense %  2.5%
    lochlan   health %  11.6%
    pakse     armor %    5.0%   health %  2.8%
    gwyr      health %   4.1%   armor %   2.7%   defense %  0.3%
    morena    health %   0.3%

Only `armor %` and `health %` ever reach a percent of a solution. `physique %`,
`cunning %`, `spirit %`, `energy %` and `offense %` do not appear in any of them,
and `defense %` is a rounding error. So this is two numbers per character, not
eight.

And the error is bounded by the percentage itself: a weight is high by exactly
what you carry, so a rough figure is worth nearly as much as an exact one. At
lochlan's +31% health, the unstated case overprices 11.6% of his solution by
31%, which is about 3% of his total.

## What share of incoming damage is each type

**Derived.** Every resistance was priced identically - a point of bleed resist
was worth a point of physical resist - which only makes sense if you take an
equal beating from all ten types. You do not.

Monster records carry no damage of their own; it is all on the skills they name.
But they do name them, so `devotionderive.measureIncoming` walks 2964 Monster
records under `records/creatures/enemies` to the 2934 whose skills deal
anything, sums each one's offensive damage by type, and takes the mean of their
shares - each monster counting once, so a boss with six skills does not outvote
a trash mob:

    physical 40.7%   chaos     6.8%   pierce  5.7%
    acid      8.9%   vitality  6.8%   aether  5.1%
    cold      8.4%   lightning 6.5%   bleed   4.0%
    fire      6.9%

`applyDefensePriority` weights each resistance by its share now, and `max <type>
resist` with it. lochlan's bleed resist goes from 99 a point to 38, and his
aether from 28 to 14 - he takes ten times as much physical as bleed and the
model had been saying they were worth the same.

It also retires `PHYSICAL_SHARE`, which was the one number in the defensive
chain with nothing behind it. It guessed a half; the answer is 0.407, and armor
is priced against that now.

The weighting is a flat mean over the bestiary, which is the same footing
`ENEMY_RESIST_BASE` and `characterAttackSpeed` already stand on. What it cannot
know is what you personally fight - an Aetherial-heavy stretch of the game is
not the mean - so a model that wants to say so should be able to override it.
Nothing reads such an override yet.

## A weight cannot say "and no more than that"

**Fixed for resistance, and the general case is still there.**

Every weight is a value per point and the solver adds it up for as many points
as it can buy. That is right for damage and wrong for anything the game caps.
lochlan sits at 73 bleed resist, seven short of the cap, where a point is worth
more than almost anything else he could take - and the solution bought 68 points
of it across five constellations. No single one was over the headroom; together
they were ten times it.

The score is additive per constellation in both scorers, so this could not be
capped per star or per constellation. `utils.resistOvercap` prices the overshoot
back out of the whole selection, and both `evaluateSolution` and
`fastsolve.Problem.score` subtract it - they have to agree or the run warns, and
they do. It costs nothing measurable: lochlan went from 1198 restarts in five
seconds to 1725, because the cheaper solutions it now finds are smaller.

lochlan 122263 -> 79102, and his bleed resist overshoot is down from 61 wasted
points to 9. It only applies to a type the sheet states, since headroom cannot be
known without one, so the other eight models are untouched.

**The general case.** Resistance is the sharpest instance but not the only one.
Anything with a ceiling has it: `armor absorb` stops at 100, `avoid melee` and
`avoid ranged` likewise, and `block %` at 100. None of those is capped, and a
solution that stacks avoidance past 100% is scoring points that do not exist. The
shape of the fix is the same each time - a headroom, and a correction against the
whole selection - so the third one of these should probably generalise
`resistOvercap` rather than copy it.

## Flat damage over time and % weapon damage

**Open, and the one thing left that is definitely wrong.**

The sheet states a damage over time as a rate. lochlan's sheet says 1001 bleed
where Primal Strike's own tooltip says 2002 over two seconds, and his sheet says
500 electrocute where Stormcaller's Pact reads ~1400 over three. `unmultiplyFlat`
takes the rate over `DOT_SECONDS` now, which is what everything downstream wants:
what one application lays down.

That fixed electrocute - 2.04 over against the game, then 1.16, in line with
lightning's 1.15 and physical's 1.32.

It broke bleed, to 8.33 over, and the reason is the question in the title. The
model scales a sheet's flat damage over time by the skill's weapon damage
percentage, the way it scales flat hit damage. Primal Strike carries 309%, so
lochlan's 1050 bleed becomes 3244 before his multiplier touches it.

The measurement says otherwise, and says it directly: Primal Strike's bleed rate
*is* the sheet's bleed rate, 1001 either way. No weapon scaling and no addition
of the skill's own 145. Taken at face value a flat damage over time is applied
once at its stated rate whatever the attack's weapon percentage.

But the same reading breaks electrocute back the other way, to 0.67 under,
because Storm Surge's electrocute plainly does add to what the sheet carries.
The two cannot both be right and I could not find the rule that separates them.

Five characters carry a sheet damage over time and all five are affected:
armitage's burn, fenris's and morena's bleed, gwyr's burn, lochlan's both.

What would settle it: one skill with a large weapon damage percentage and one
with none, both reporting the same duration type, off the same character. Primal
Strike at 309% against something at 0% would say in one comparison whether the
weapon percentage multiplies it.

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
attack ranges live on their skills rather than their records - though the
records do name the skills, which is how `INCOMING_SHARE` was measured, so this
is reachable by the same route.

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

## Set bonuses

**Read, and applied.** `itemgen.setBonuses` has extracted them for a while - the
note here saying otherwise was stale - but nothing was working out which sets a
character actually wears, so they reached itemData and stopped.

`sheetOf` counts worn pieces per set now and adds the tiers earned. A set states
its bonuses as a running total per piece count and setBonuses has already turned
that into what each count adds, so wearing n pieces is the sum of tiers two to n.

It was worth more than it looked. lochlan's three Royal Crown pieces are the
Royal Exuberance set: 5% to each attribute at two, and **+1 to all skills** at
three. That last was the rank his hand-transcribed ranks had and the derivation
did not, on every skill at once - and with it his ranks land exactly where he
had written them. The attribute percentage closed most of the rest: spirit is
now exact, cunning within one percent, physique within four.

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

A modifier is no longer written into the rotation at all - see below.

The derived parent used to only *check* the nesting: a modifier nested under the
wrong skill said so, and one left at the top level was told which entry to move
inside. It decides it now, and the nesting is what is left over for the links
the records do not carry - the five it cannot place, a shapeshift form and the
attack it grants, and whatever a mod spells differently.

`Ability.augment` is still dead.

## Reading the save files

**The body opens now.** What had stalled it was four fields between the header
and the first block that nothing was reading: a byte (7 on these saves, 3 on the
older ones a reference implementation was written against), an int read *without*
advancing the key, the data version, and a sixteen-byte uid. NOTES had listed
"extra header fields in format version 2" as an untried candidate and that is
what it was.

With those consumed the blocks fall out with sane types and lengths and a zero
trailer on each, which is the check that the key is still in step. Eleven of the
twelve saves walk.

**Block 2 is read**, forty-eight bytes on every character - a version and eleven
fields:

    level  experience  attribute points  skill points  devotion points
    total devotion  physique  cunning  spirit  health  energy

That is three things the models had been transcribing by hand or guessing.
`total devotion` is the number kieri and lachesis could not be modelled without.
The attributes are what you have before gear. And `health` is *base* health,
which is on no character sheet at all and is what a "+% Health" bonus multiplies
- lochlan's reads 1070 against the 1070 read off the game by hand, which is the
check that the block is what it looks like.

`python savefile.py` prints the lot and flags a model that disagrees. Every one
of them disagreed about devotion:

    armitage 52 (model 57)   fenris 13 (20)    kieri 13 (15)
    lethe 20 (55)            lilith 34 (45)    pakse 34 (28)

**The skills are read.** `python savefile.py Gwyr` prints his ranks in the syntax
a rotation wants - Fire Strike 7, Brimstone 6, Explosive Strike 3, against a
model that stubs all three at 12. That was the largest piece of transcription
left and the thing every damage weight is priced against.

Four things had moved on from the reference implementation, and each put the
*next* field out rather than failing where it went wrong:

    the item grew four fields          inventory version 4 -> 11
    a stash tab grew five              version 6 -> 11
    a skill record grew a byte         version 5 -> 8, and two saves are still 6
    what follows the skill list        two lists, not one

The inventory and the stash are consumed rather than interpreted - only their
nested block lengths are read properly, since those cannot be skipped. No item
is parsed, which is deliberate: the item record is the part that keeps changing.

An item skill entry gives the devotion proc bound to that skill and the
controller that fires it, which is the binding the optimiser exists to choose
and could never be read back. What granted it is spelled two ways - a component
puts an int before the path where a transformation does not - so the path is
looked for rather than assumed.

**The gear is read too.** `python savefile.py Lochlan gear` names every piece
and what is socketed into it:

    Dread-Mask of Gurgoth        Polished Emerald
    Pendant of the Royal Crown   Attuned Lodestone, Stormtail Viper Venom
    Falcon's Claw                Oleron's Blood, Potent Stonetusk Hoof

The item record had moved on the same way everything else had - four numbers in
inventory version 4, eight in 11, and the same two characters are still on 4.
Only what you are wearing is parsed; the bags are consumed, because they hold
loot rather than a build and an odd thing in one should not cost the parse.

The prefix and suffix are recorded but not reported. They are tags, and what
they rolled comes from a seed against a range in the records - a seed on its own
says nothing without the game's own roller.

**Reconstructing the sheet.** `python savefile.py Lochlan stats` adds up your
base from the save, then your masteries and passives, then your gear, then what
the attributes are worth in turn. Against his own sheet:

    physique  668 / 763      energy   2606 / 2358
    cunning   367 / 400      health   6883 / 10178
    spirit    418 / 451      offense   731 / 1964

The attributes land inside a tenth, which they did not before: the mastery bar
is the single largest contributor and was missing entirely - Soldier at 50 is
250 physique and 1400 health on its own.

Which skills count is a question of class, not of level. `Skill_Mastery` and
`Skill_Passive` always, a `Skill_Buff*Toggled` when the save records it running
- the sheet is read in town and that is where the three lochlan leaves on show
up. A `Skill_Modifier` or `Skill_Transmuter` never: Torrent's lightning is
Primal Strike's and not yours. Nor a `Skill_PassiveOn*`, which fires on a hit or
at low life and is not up in town.

Two things are still out and one is a bug:

  - an item's prefix and suffix are read now, and a damage range is taken at its
    average, which is what `starBonuses` already did for every other range in
    the project. lochlan turns out to have almost none - his gear is legendaries
    and the one affix pair he carries grants skill ranks - so this was never the
    missing health it looked like.
  - offensive and defensive ability gain per level, which is in neither the save
    nor the records and had been most of their gap. Fitted rather than read -
    see below.
  - **armor coverage was tried and does not work.** combatformulas.dbr gives the
    chances a hit lands on each part - torso 26, legs 20, head 15, shoulders 15,
    arms 12, feet 12 - and weighting the pieces by them reads **+77%** against
    gwyr's freshly read sheet where an even average reads -21%. Against three
    characters no aggregation fits: sheet over even-average is 2.16 for
    armitage, 1.26 for gwyr, 1.58 for lochlan, so it is not a constant factor
    and the coverage is not what is wrong. Something about the per-piece figure
    is - `defensiveProtection` off the base record, 636 on a level 50 head.
    `savefile.REGIONS` keeps the mapping for whoever tries next.
  - armor is averaged rather than summed. The game picks a body part per hit and
    each piece protects its own, so the average is both nearer the sheet and the
    quantity `applyDefensePriority` wants when it prices what armor stops per
    hit. Summing read 5275 against a sheet of 1353; averaging reads 659. It is
    low because a chest plate covers more of you than a belt and nothing here
    weights them by coverage, which is what would close the rest.

So the attributes, the resistances, the conversions and `+skills` are worth
taking; the rest is a cross-check against the sheet rather than a replacement
for it, and the output says so.

## combatformulas.dbr states the equations outright

`records/game/combatformulas.dbr` was never opened, and it has the answers to
several things that were being worked out the hard way:

    offensiveAbilityEquation  (offensiveAbilityDV + (characterLevelDV * 12)
                               + ((dexterityDV + bonusDV) * 0.5))
                              * (1 + (offensiveAbilityModifierDV / 100)) + 53

    defensiveAbilityEquation  ...the same, against strength

    combatRegionTorsoChance 26   HeadChance 15   ShouldersChance 15
    combatRegionLegsChance  20   ArmsChance 12   FeetChance      12

    physicalDamageEquation         physicalDamageDV*((dexterityDV/245)+1)
    physicalDurationDamageEquation physicalDamageDV*((dexterityDV/215)+1)
    magicalDamageEquation          magicalDamageDV*((intelligenceDV/215)+1)
    magicalDurationDamageEquation  magicalDamageDV*((intelligenceDV/200)+1)

The four damage equations confirm every attribute constant already in models.py.
The region chances are the armour coverage weighting that was an open question -
a chest is hit twice as often as a boot - and they sum to a hundred.

**The ability constant was fitted at 14.84 and is 12.** The fit had the shape
right and the size wrong. It said the missing term was level rather than an
attribute, and that the 0.5 per point was already correct; both are exactly what
the equation says, and it also correctly called pakse and lachesis stale. But it
was against level-1 rather than level, it missed the flat 53 that lands after
the percentage, and 14.84 was absorbing something else - the derived side reads
about 11% under on most characters even with the game's own arithmetic, which is
a real gap the fit had been hiding by inflating the per-level term.

The lesson is the obvious one: the equations were in the database the whole time,
and a fit against ten hand-typed sheets was never going to beat reading them.
Look for the record before fitting anything.

## Offensive and defensive ability gain per level

Both read 48-70% low against every sheet. Three things were missing and the
third is the only interesting one.

**The base.** `records/creatures/pc/malepc01.dbr` states 65 offensive and 65
defensive ability, beside the 50 of each attribute a level 1 character starts
with. Small, and it was not being added.

**The percentage.** `offense %` and `defense %` were read off the gear and then
applied to nothing. Lochlan carries +10%.

**The per-level gain**, which was the rest of it. The game's own text says
offensive ability comes from "skills, items, and Cunning" and defensive from
"skills, items, and Physique", and states no rate for either - the enemy records
state theirs as a level equation, `(charLevel*6)+50` and the like, and the
player record has no equation at all. So this one is **fitted**, which nothing
else in the project is. Against ten characters, sheet minus everything that can
be accounted for:

| explanation | OA rms | DA rms |
|---|---|---|
| against the attribute | 43% | 25% |
| against level | 22% | 16% |
| both together | 22% | 16% |

Level explains it and the attribute does not. Fitting both together drives the
attribute coefficient to 0.146 for offense and to **-0.094** for defense, so the
existing 0.5 per point is already about right and what is missing is not an
attribute at all. That is the part worth trusting. The size is worth less.

**One constant, not two.** Fitted separately the two come out 14.55 and 15.14 at
rms 11% and 14%; a single 14.84 scores the same 11% and 14%. So the engine gives
both the same gain and two numbers was fitting noise. A round 15 sits well inside
the error as well - nothing here can tell 14.8 from 15.

Pakse and lachesis are out of the fit, and their stated abilities are deleted
rather than annotated. They implied 6.9/9.8 and 11.7/10.0 against a 12.3-18.0
spread across everyone else, which is a sheet nobody has read in a while rather
than a different rule.

    before   -48% .. -70% on all ten
    after    lochlan +0% and +4%, six of the eight within 7%

Armitage is the widest of the eight at +12% and -11%, in opposite directions,
which is what a sheet read at two different times looks like.

## Armor absorption has a base of 70

`armorDefensiveAbsorption: 70.0` in `records/game/gameengine.dbr`, and what gear
and skills grant is a percentage *of* it rather than points added to it - the
game's own tooltip says "Increases Armor Absorption by X%". A single Scaly Hide
is `defensiveAbsorptionModifier 20.0`, so one is 84 and two are 98.

What was being reported was the bonus on its own. Every character other than
lochlan had no `armor absorb` stated and was filled in at whatever their gear
granted - 0 for most of them - so armor was being priced against a character who
absorbs nothing. They now read 75 to 98.

## The saves are live, so derived numbers move under you

Worth knowing before chasing a discrepancy. Lochlan's armor absorption was 84
one minute and 98 the next, and nothing in the code had changed: he was being
played, and a second Scaly Hide went in. His components went 8 to 12 and his
derived health 8420 to 9045 in the same stretch, which took health inside 5% and
deleted it from his model.

    python - <<'PY'
    import savefile, os, time
    for n, i in savefile.characters().items():
        print(n, time.ctime(os.path.getmtime(i["path"])))
    PY

Two things follow. A stated sheet is a photograph and the derived one is live, so
a gap can be either a modelling error or a week of play - check the file's date
before believing the gap. And pakse's save is **226 days old**, which is a better
explanation of him than anything about his sheet: his derived numbers are of a
character nobody has played since, so re-reading his sheet will not help until
he is loaded and saved.

## A modifier counts when what it modifies counts

`Skill_Modifier` was excluded wholesale, then excluded unless the records gave
it no parent. Both were approximations of the real rule: **a modifier is on your
sheet exactly when the thing it hangs off is.**

    Temper          -> Flame Touched   an aura he leaves running  -> counts
    Squad Tactics   -> Field Command   an aura he leaves running  -> counts
    Static Strike   -> Fire Strike     an attack                  -> does not
    Blindside       -> Blitz           an attack                  -> does not
    Heart of the Wild -> nothing       a character passive        -> counts

Follow the chain, because they stack two deep - Searing Might modifies Explosive
Strike modifies Fire Strike. A toggle that is switched off carries none of its
modifiers in, which the save records per skill.

Temper alone is +66% physical, internal and pierce and +114% retaliation, and
Squad Tactics is +85% all damage. Against armitage's freshly read sheet this
took `physical %` from 8 to 159 against a stated 256 - from -98% to -38%.

## Percentages that were read and never applied

Four of them, all the same bug: the value was extracted off the gear, reported
as a stat, and multiplied into nothing.

    offense %    defense %    armor %    health/s %    energy/s %

Lochlan's `health/s %` is 111, of which 48 is Heart of the Wild. Armitage
carries 5% armor off a Menhir's Blessing augment and 45% health regeneration.
Health and energy were the only two that had ever been applied.

## A modifier that modifies nothing is a character passive

`Skill_Modifier` was excluded wholesale, on the grounds that it belongs to one
skill rather than to you: Torrent's lightning is Primal Strike's. That is right
where the records name a parent, and wrong where they do not, which is how a
mastery states a plain always-on passive.

Lochlan has two:

    Heart of the Wild    health % 22, health/s % 48
    Oak Skin             armor 14, defence 11, aether and pierce resist 3

Both are his. Neither was counted. `recordedParent` already knew the difference
- Storm Touched names Savagery, Storm Surge names Primal Strike, and these two
name nothing at all.

The exclusions that stay are worth noting because they look similar and are not:
lochlan's Menhir's Will is `Skill_PassiveOnLifeBuffSel` and fires at low life,
and gwyr's Word of Renewal is a cast buff. The sheet is read in town, so neither
is on it.

## Health

Better, and not finished. Devotion coming off the stated side and the two
passives above took lochlan from -30% to -13%, and gearing he did while this was
being written took him inside 5% and out of his model altogether:

    fenris -13%   gwyr  -1%   hela -29%   kieri -10%
    lilith -16%   lochlan -6%   pakse -6%

What is left has no shape to it. Fitted against level it is 74% rms, against
physique 81%, against both 68% - so unlike offensive ability there is no single
missing term, and `PHYSIQUE_HEALTH = 2.5` is not wrong in a way more physique
would fix. The residual is per character, which points at gear: an affix rolls
its value from a seed against a range and the range's average is what gets read.
Hela is the worst at -29% and has no skipped skill carrying health at all.

## Current devotion comes off the baseline

The sheet is read in town with the devotions you already have, so every number
copied off it includes them - and the optimiser then scored a candidate
constellation set on top, counting the set you are wearing twice.

`savefile.devotionOf` reads what they are worth and `Model.removeCurrentDevotion`
takes it off anything the model states. Only what the model states: a stat filled
in from the save was built out of gear and skills and never had devotion in it.

Lochlan's are worth rather more than the two abilities that led here:

    health 500      lightning % 340    all damage % 120    offense 96
    defense 105     electrocute % 100  retaliation % 180   internal % 90

A star's passive bonuses only. A proc contributes none - `templateAutoCast` is
the test, the same one devotiongen uses to decide whether a star carries bonuses
or an ability - because a proc's damage is not on your sheet and the optimiser
already scores it separately.

A capped resistance comes off too, and should: at 80 fire with 20 of it from a
constellation, the baseline is 60 and a point of fire resistance is worth
something again.

This also improved the largest unexplained family. `lightning %` read 930 stated
against 631 derived, a -32% gap; 340 of that 930 is Ulo and Tempest, and with it
off the two are 590 against 631.

## A rotation says what is on the bar and nothing else

Two of the three things a rotation entry carried were derivable, so they are
derived. What is left is what nothing else can know: which skills are on the
bar, the order you play them in, and where you press one slower than the game
would let you.

    "Mortar Trap"                 fires on its own cooldown
    ("Flashbang", 3.0)            ...unless you press it slower than that
    0.5                           a bare rate, for what cannot be named

The **rank** is the points you have spent, off the save. Every model got it
wrong: three stated a flat 12 on every line, morena stated her skill screen so
her gear counted twice, and lethe named two skills she had never put a point in.
Naming a skill with nothing in it is now said out loud rather than scored at
rank zero.

The **modifiers** come off the records. `deriveModifiers` walks each modifier
you have points in up its parent chain, and the first entry on the bar it
reaches is the one it rides. Fifty-one were written out across the models and
all fifty-one come back on their own, including the two-deep ones - Searing
Might modifies Explosive Strike modifies Fire Strike, and only Fire Strike is a
button.

One relationship is not in the records and still has to be nested by hand:

    ("Feral Claws", ["Werewolf"])

Nothing in the naming ties a shapeshift form to the attack it grants. Saying it
is enough, though, because an explicitly nested name is an attachment point
too - so Recklessness and Voracity reach Feral Claws by modifying Werewolf.

The number after the name means the press interval now, where it used to mean
the rank with the press second. There is no way to tell the two apart in an old
model, so anything written against the old grammar reads its rank as a press.
All eleven were converted with the change.

## A model loaded by a lowercase name got no save at all

`devotion.py lochlan` passes the name as typed and `savefile.characters()` keys
on the game's capitalisation, so `sheetOf("lochlan")` returned an empty sheet -
not an error, just nothing. Every model run from the command line was scored
with none of its save behind it, which is every run except the ones made from a
Python call. Lochlan scored 53428 that way against 65434 with his save.

The lesson is the missing-data path rather than the case: `sheetOf` returns
`({}, [])` for a character it does not have, which is indistinguishable from a
character whose save contributes nothing. `Model.saveName` resolves the name
once and says so when there is no save.

## A model states only what the save gets wrong

`Model.fillFromSave` fills every stat a model leaves out, so what a model states
is an override rather than a transcription. A stated stat still wins, which is
what a plan holding gear the character has not got yet needs.

Applied across all eleven: a stat the save agreed with to within 5% was deleted,
and one further off kept its value and gained a comment saying what was derived.
Twenty-two stats came out. That is the honest yield, and it is small - the point
of the exercise turned out not to be the deletions but what the annotations
line up into. The gap is not noise per character, it is the same handful of
gaps repeating:

| family | n | median | range |
|---|---|---|---|
| `<type> %` | 41 | -57% | -98% .. -31% |
| flat `<type>` | 19 | -62% | -92% .. +616% |
| `offense` | 10 | -62% | -77% .. -56% |
| `defense` | 10 | -67% | -70% .. -59% |
| `armor` | 10 | -42% | -64% .. -23% |
| `energy` | 10 | **+14%** | +9% .. +45% |
| `energy/s` | 7 | -82% | -95% .. -57% |
| `health/s` | 7 | -45% | -75% .. -14% |
| `health` | 8 | -10% | -30% .. +20% |
| attributes | 16 | -7% | -15% .. +9% |

Four of those already have an entry above saying why - offensive and defensive
ability have a base from level that is in neither the save nor the records,
armor wants coverage weighting. The attributes are the one family that is
basically right, which is why most of the deletions are attributes.

`<type> %` is the largest and has no explanation yet. Forty-one readings across
ten characters, all in the same direction, most of them clustered around half
the stated figure. Something contributes a percentage to the sheet that is not
being added up here, and its size is stable enough across very different builds
that it is likely one mechanism rather than an accumulation of small ones.

`energy` over-reading by a consistent +14% is the other odd one: it is the only
family that leans positive on every character, which usually means something is
being counted twice rather than missed.

A resistance reads high where the sheet is capped and the gear is not - lochlan
states 80 fire against a derived 120, which is not an error but forty points of
overcap, and `resistOvercap` already prices that.

## Models that do not load

`kieri` and `lachesis` state no `devotionPoints`, which is not a thing that can
be inferred.

## Per-character data still outstanding

Not modelling gaps - transcription. Every one of these is a number only the game
can supply.

Skill ranks and `+skills` have both come off this list: every rotation states
points spent, read out of the save, and the gear ranks are derived at load. So
have the resistances, which now come off the save for everyone.

| character | needs |
|---|---|
| everyone | **`attacks/s`**, which is the one thing on this list that cannot be derived. The weapon states a speed *class* - `characterBaseAttackSpeed -0.16`, `tagAttackSpeedVerySlow` - and `attack speed %` comes off the gear, but the seconds a swing takes is in the animation assets rather than the record database, and the game warns the two do not simply multiply: "Slower weapons gain less from % Attack Speed bonuses". The weapon's own tooltip prints it (`tagAttackSpeed`, "{%.2f0} Attacks per Second"), so it is one number to read per character |
| **pakse, lachesis** | **a fresh sheet.** Both are stale enough to have been thrown out of the LEVEL_ABILITY fit, and their stated offensive and defensive ability are deleted rather than annotated. Everything else they state is off the same reading, so the derived figures in their comments are the better number until they are re-read - and re-reading either is what would pin 14.84 down |
| kieri, lachesis | `devotionPoints`. Neither loads without it |
| kieri, lachesis, lilith | their rotations - each is bare rates, so no skill is named and no main attack can be read |
| lethe | a main attack. She has no default-attack replacer at all, so her rotation leads with a bare rate and every granted skill is priced against a 100% swing |
| armitage, pakse | confirm the held attack, which is whichever skill the rotation lists first. Fire Strike and Righteous Fervor are guesses. Pakse's now matters differently: his weapon pool skills are at 1-2 points rather than a stubbed 12, so Righteous Fervor does get to fire |
| hela, kieri, lachesis, lilith, lochlan, pakse | `attacks/s` off the sheet. All are round numbers or the old whole-bar aggregate. The four that have been read moved 3 -> 1.64, 3 -> 1.91, 2 -> 2.43 and 2 -> 1.76 |
| armitage | `hits taken/s` if 2.78 is wrong - it drives 76% of what he deals |
| fenris | is his slam Brutal Slam off Severed Claw or the plainer Slam off Chipped Claw? Same cooldown, different damage |
| nyx | level 24, Occultist/Shaman, no model at all |
