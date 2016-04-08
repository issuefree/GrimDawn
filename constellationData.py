from dataModel import *

xA = Constellation("Crossroads Ascendant", "", "1a")
Star(xA, [], {"offense":15})
xC = Constellation("Crossroads Chaos", "", "1c")
Star(xC, [], {"health %":5})
xE = Constellation("Crossroads Eldrich", "", "1e")
Star(xE, [], {"offense":15})
xO = Constellation("Crossroads Order", "", "1o")
Star(xO, [], {"health %":5})
xP = Constellation("Crossroads Primordial", "", "1p")
Star(xP, [], {"defense":15})

	# ignore this
	# we'll use 75% chance of triggering for our timing
	# 1-((1-.15)^x) = .75 -> log_.25(1-.15) = 8.5 attacks to trigger after cooldown, 4 attacks in the cooldown

falcon = Constellation("Falcon", "1a", "3a 3e")
a = Star(falcon, [], {"physical %":15})
b = Star(falcon, a, {"bleed %":24})
c = Star(falcon, b, {"cunning":15})
d = Star(falcon, c, {"physical %":24})
e = Star(falcon, d, {})
# 6 projectiles
# 100% chance to pierce (assume pierce means on average 2 hits)
# I'm guestimating I'll get 4 hits per.
e.addAbility(Ability(
	"Falcon Swoop", {"type":"attack", "trigger":"attack", "chance":.15, "recharge":1, "targets":4, "duration":3}, 
	{"weapon damage %":65, "duration":{"triggered bleed":135*3}} ))

shepherd = Constellation("Shepherd's Crook", "1a", "5a")
a = Star(shepherd, [], {"health":40, "pet health %":8})
b = Star(shepherd, a, {"cunning":10, "health":40})
c = Star(shepherd, b, {"elemental resist":10, "pet elemental resist":15})
d = Star(shepherd, c, {"health %":3, "pet health %":5, "pet defense %":5})
e = Star(shepherd, d, {})
e.addAbility(Ability(
	"Shepherd's Call", 
	{"type":"buff", "trigger":"attack", "chance":.25, "duration":4, "recharge":6},
	{"offense":70, "pet all damage %": 190, "pet crit damage":25, "pet retaliation %":250} ))

hammer = Constellation("Hammer", "1a", "4a")
a = Star(hammer, [], {"physical %":15})
b = Star(hammer, a, {"defense":8, "internal %":30})
c = Star(hammer, b, {"physical %":15, "internal %":30})

anvil = Constellation("Anvil", "1a", "5a")
a = Star(anvil, [], {"defense":10})
b = Star(anvil, a, {"physique":10})
c = Star(anvil, b, {"armor absorb":3})
d = Star(anvil, c, {"defense":15, "constitution %":20})
e = Star(anvil, d, {"Targo's Hammer":True})
# 25% chance on block
e.addAbility(Ability("Targo's Hammer", 
	{"type":"attack", "trigger":"block", "chance":.25, "targets":3},
	{"stun %":50, "weapon damage %":92, "physical":100, "internal %":145} ))

owl = Constellation("Owl", "1a", "5a")
a = Star(owl, [], {"spirit":10})
b = Star(owl, a, {"elemental resist":8, "skill cost %":-5})
c = Star(owl, b, {"burn %":30, "electrocute %":30, "frostburn %":30})
d = Star(owl, b, {"elemental %":24, "reflected damage reduction":15})

harpy = Constellation("Harpy", "1a", "5a")
a = Star(harpy, [], {"pierce %":15, "cold %":15})
b = Star(harpy, a, {"cunning":10})
c = Star(harpy, b, {"bleed resist":10, "offense":15})
d = Star(harpy, b, {"pierce":(3+7)/2, "pierce %":24, "cold %":24})

throne = Constellation("Empty Throne", "1a", "5a")
a = Star(throne, [], {"reduced stun duration":15})
b = Star(throne, a, {"pierce resist":8, "pet pierce resist":8})
c = Star(throne, b, {"chaos resist":8, "pet chaos resist":8})
d = Star(throne, b, {"aether resist":8, "pet aether resist":8})

wolverine = Constellation("Wolverine", "1a", "6a")
a = Star(wolverine, [], {"defense":15, "pet pierce resist":10})
b = Star(wolverine, a, {"pierce retaliation":30, "retaliation %":20, "pet pierce retaliation":50})
c = Star(wolverine, b, {"defense":18, "pet bleed resist":25})
d = Star(wolverine, c, {"retaliation %":35, "pet retaliation %":50})
e = Star(wolverine, c, {"defense %":3, "melee weapon physique requirements":-10, "melee weapon cunning requirements":-10, "pet defense %":5})

crab = Constellation("Crab", "6a 4o", "3a")
a = Star(crab, [], {"constitution %":15, "physique":20})
b = Star(crab, a, {"elemental %":30, "internal %":70})
c = Star(crab, b, {"Elemental Barrier":True})
d = Star(crab, c, {"pierce resist":18, "defense":10})
e = Star(crab, d, {"elemental %":40, "elemental resist":15})

scepter = Constellation("Rhowan's Scepter (requires mace)", "6a 4o", "3a 2o")
a = Star(scepter, [], {"defense":15})
b = Star(scepter, a, {"health %":6})
c = Star(scepter, b, {"physical %":50})
d = Star(scepter, c, {"internal %":80})
e = Star(scepter, b, {"defense":18})
f = Star(scepter, e, {"physical":(8+12)/2,"stun %":5, "stun duration":10})

boar = Constellation("Autumn Boar", "4a 3o 4p", "3a")
a = Star(boar, [], {"physique":10, "cunning":10})
b = Star(boar, a, {"pierce resist":15, "physique":10})
c = Star(boar, b, {"physique %":5})
d = Star(boar, c, {"physical resist":4, "fire resist":20})
e = Star(boar, c, {"stun duration":10, "physical retaliation":150})
f = Star(boar, e, {"bleed retaliation":2100*.1})
g = Star(boar, e, {})
# 25% on block
# ~.75 seconds per block (.5 s per attack)
# 1 second recharge
# description sounds like a frontal cone so we'll go with 2 targets avg
# 1 in 4 blocks will trigger .55/.75 = .66 so 1 in ~6 attack equivalents + 2 from the recharge
# 1/8*2 = .25
g.addAbility(Ability(
	"Trample", 
	{"type":"attack", "trigger":"block", "chance":.25, "recharge":1, "targets":2},
	{"stun %":100, "weapon damage %":80, "internal":404} ))

scythe = Constellation("Harvestman's Scythe", "3a 3o 5p", "3a 3p")
a = Star(scythe, [], {"energy/s":2})
b = Star(scythe, a, {"health/s":12})
c = Star(scythe, b, {"physique %":4, "constitution %":20})
d = Star(scythe, c, {"health regeneration":20})
e = Star(scythe, d, {"energy regeneration":20})
f = Star(scythe, e, {"cunning %":4, "spirit %":4})

crown = Constellation("Rhowan's Crown", "4a 6e", "1a 1e")
a = Star(crown, [], {"elemental %":30, "elemental":(6+9)/2})
b = Star(crown, a, {"spirit":20, "pet elemental %":40})
c = Star(crown, b, {"Elemental Storm":True})
d = Star(crown, c, {"elemental resist":18, "pet elemental resist":10})
e = Star(crown, d, {"elemental %":40, "burn %":60, "electrocute %":60, "frostburn %":60, "chaos resist":8})

huntress = Constellation("Huntress", "4a 3c 4e", "1a 1e")
a = Star(huntress, [], {"offense":15})
b = Star(huntress, a, {"pierce %":35})
c = Star(huntress, b, {"bleed %":60})
d = Star(huntress, c, {"pierce resist":8, "damage beast %":15, "health":100})
e = Star(huntress, c, {"offense %":3, "pet offense %":5})
f = Star(huntress, e, {"bleed":30, "bleed %":50, "bleed duration":20})
g = Star(huntress, e, {})
# 20% on attack, 5 second duration, no recharge
# calling it .9
# no stat for reducing opponent offense so we'll call it defense

#halfway between an attack and a buff. Since the debuff doesn't overlap I'm going to set the recharge to the duration.
# this will slightly undervalue the skill as it can refresh within it's duration.
# I can't decide if I want to use targets. The "defense" part assumes I'll hit everything hitting me so it's over valued.
# the bleed resist reduction feels like I shouldn't count it per target since it only matters on the things I'm hitting and hitting things is already accounted for.

# I'm treating reduced offense like defense so don't count the targets (it's built into that conversion)
# reduced resist only matters when other stuff hits so reducing resist on stuff I'm not hitting doesn't count for anything.
# remove the multi target component (I'm overcounting defense and undercounting reduced resist a bit).
g.addAbility(Ability("Rend", 
	{"type":"attack", "trigger":"attack", "chance":.2, "recharge":1, "duration":5, "targets":3},
	{"duration":{"defense":125/3, "reduce bleed resist":33/3, "triggered bleed":307*5}} ))

leviathan = Constellation("Leviathan", "13a 13e")
a = Star(leviathan, [], {"cold":8, "cold %":80})
b = Star(leviathan, a, {"health %":5, "physique":25})
c = Star(leviathan, b, {"defense":26, "energy regeneration":20, "energy %":10})
d = Star(leviathan, c, {"pierce resist":20, "cold resist":20})
e = Star(leviathan, d, {"cold":(12+16)/2, "cold %":100})
f = Star(leviathan, d, {"frostburn":25*3, "frostburn %":100})
g = Star(leviathan, d, {})
# 30% on attack
# 3 second recharge
# 6 second duration
# 3.5 meter radius
# decent sized aoe probably 2.5 targets, it lasts and hits stuff that walks in (I assume) so call it another .5
g.addAbility(Ability(
	"Whirlpool", 
	{"type":"attack", "trigger":"attack", "chance":.3, "recharge":3, "targets":3, "duration":6}, 
	{"triggered cold":322, "duration":{"triggered frostburn":133*2}, "slow move":35} ))

oleron = Constellation("Oleron", "20a 7o")
a = Star(oleron, [], {"physique":20, "cunning":20, "health":100})
b = Star(oleron, a, {"physical %":80, "internal %":80})
c = Star(oleron, b, {"pierce resist":20, "bleed resist":10, "offense":30})
d = Star(oleron, c, {"physical resist":4, "health":200})
e = Star(oleron, d, {"physical":(9+18)/2, "physical %":100})
f = Star(oleron, d, {"offense":15, "internal":25*5, "internal %":100, "max pierce resist":2})
g = Star(oleron, d, {})
# 100% on critical (hrm, call it 15%)
# 1 second recharge
# 5 meter pbaoe for 3 targets
# weird one. There are two duration components with different durations. I can either scale the damage to be over a longer time or scale the others to be shorter.
# I'll make the damages longer.
# If we assume everything has enough armor for all of the reduce armor to take effect (if they have less and we're doing physical damage they're probably dead already anyway)
# Then if we know our flat physical we can assume 70% absorb
g.addAbility(Ability(
	"Blind Fury", 
	# .1*3, 
	{"type":"attack", "trigger":"critical", "chance":1, "recharge":1, "targets":3, },
	{"weapon damage %":85, "internal":324, "bleed":324, "slow attack":25, "reduce armor":275} ))

tortoise = Constellation("Tortoise", "1o", "2o 3p")
a = Star(tortoise, [], {"defense":10, "health":25})
b = Star(tortoise, a, {"defense":12, "shield physique requirements":-10})
c = Star(tortoise, b, {"defense":12, "health":100})
d = Star(tortoise, c, {"health %":4, "defense":10, "armor %":4})
e = Star(tortoise, c, {})
# 100% chance at 40% health
# 30 second recharge
e.addAbility(Ability(
	"Turtle Shell", 
	# 1, 
	{"type":"shield", "trigger":"low health", "chance":1, "recharge":30},
	{"health":2700} ))

blade = Constellation("Assassin's Blade", "1o", "3a 2o")
a = Star(blade, [], {"pierce %":15})
b = Star(blade, a, {"offense":12})
c = Star(blade, a, {"bleed %":15, "pierce %":15})
d = Star(blade, c, {"bleed %":30})
e = Star(blade, d, {})
#100% on crit: ~15% on attack
#15 second duration, so on big targets we'll have nearly 100% uptime. for small stuff it doesn't matter.
#call it 66%?
e.addAbility(Ability(
	"Assassin's Mark", 
	# .66, 
	{"type":"buff", "trigger":"critical", "chance":1, "recharge":0, "duration":3},
	{"reduce physical resist":33, "reduce pierce resist":33} ))

lion = Constellation("Lion", "1o", "3o")
a = Star(lion, [], {"health %":4, "defense":8, "pet health %":3})
b = Star(lion, a, {"spirit":10, "health":100})
c = Star(lion, b, {"all damage %":15, "pet all damage %":12})

crane = Constellation("Crane", "1o", "5o")
a = Star(crane, [], {"physique":8, "spirit":8})
b = Star(crane, a, {"acid resist":12})
c = Star(crane, b, {"all damage %":15, "weapon spirit requirements":-10})
d = Star(crane, c, {"vitality resist":8})
e = Star(crane, d, {"elemental resist":10})

panther = Constellation("Panther", "1o", "2o 3p")
a = Star(panther, [], {"offense":12, "pet offense %":2})
b = Star(panther, a, {"cunning":8, "spirit":8, "pet all damage %":15})
c = Star(panther, b, {"all damage %":15, "energy regeneration":10, "pet offense %":3})
d = Star(panther, c, {"offense":20, "pet crit damage":5})

dryad = Constellation("Dryad", "1o", "3o")
a = Star(dryad, [], {"acid resist":10, "energy":200})
b = Star(dryad, a, {"energy/s":1, "health":80})
c = Star(dryad, b, {"reduced poison duration":20, "reduced bleed duration":20})
d = Star(dryad, c, {"spirit %":5, "jewelry spirit requirements":-10})
e = Star(dryad, d, {})
#33% on attack
#4 second recharge
#8%+350 health restored
# how long is a fight? call it... 30 seconds.
# 1 in 3 attacks triggers it, .5 seconds per attack = 1.5 seconds + 4 seconds recharge = 5.5 seconds. Will trigger ~5 times per fight.
# lets say half of them aren't used because we're near full health
e.addAbility(Ability(
	"Dryad's Blessing", 
	# 2.5, 
	{"type":"heal", "trigger":"attack", "chance":.33, "recharge":4},
	{"health %":8, "health":350, "reduced poison duration":30, "reduced bleed duration":30} ))

shieldmaiden = Constellation("Shieldmaiden (requires shield)", "4o 6p", "2o 3p")
a = Star(shieldmaiden, [], {"block %":4})
b = Star(shieldmaiden, a, {"armor absorb":5})
c = Star(shieldmaiden, b, {"blocked damage %":18})
d = Star(shieldmaiden, c, {"retaliation %":50})
e = Star(shieldmaiden, b, {"reduced stun duration":25, "blocked damage %":15})
f = Star(shieldmaiden, e, {"shield recovery":15, "stun retaliation":15})

scales = Constellation("Scales of Ulcama", "8o", "2o")
a = Star(scales, [], {"health":250, "energy":300})
b = Star(scales, a, {"health/s":6, "health regeneration":10})
c = Star(scales, b, {"health %":6})
d = Star(scales, c, {"energy regeneration":10, "energy/s":2})
e = Star(scales, b, {"all damage %":30})
f = Star(scales, e, {})
# assuming single target
# 20% when hit
# 1.5 s recharge
# I have no idea how to handle the 135% attack damage converted to health
# assume I get hit 2 times a second so 2.5 seconds + 1.5 seconds = 4 seconds between
# normalizing to .5 s per attack = 1/8
# let's say I get... 300 health per, it triggers 3 times in a fight that's 900 health in a fight.
# multiply by 8 since it's not weapon attack adjusted
f.addAbility(Ability(
	"Tip the Scales", 
	# 1.0/8, 
	{"type":"attack", "trigger":"hit", "chance":.2, "recharge":1.5},
	{"triggered vitality":170, "energy":320, "attack as health":135} ))

assassin = Constellation("Assassin", "6a 4o", "1a 1o")
a = Star(assassin, [], {"pierce %":30})
b = Star(assassin, a, {"cunning":15})
c = Star(assassin, b, {"offense":18, "defense":10})
d = Star(assassin, b, {"bleed resist":8, "cunning %":5})
e = Star(assassin, d, {"defense":12, "acid resist":8, "damage human %":15})
f = Star(assassin, d, {"pierce":6, "pierce %":40})
g = Star(assassin, f, {})
#100% on crit: ~15% on hit
#18 projectiles
#100% pass through
# call it 6 hits
# 4 attacks for recharge, ~6 attacks between hits = .1
g.addAbility(Ability(
	"Blades of Wrath", 
	{"type":"attack", "trigger":"critical", "chance":1, "recharge":2, "targets":6},
	{"triggered pierce":168, "weapon damage %":25} ))

blades = Constellation("Blades of Nadaan (requires sword)", "10a", "3a 2o")
a = Star(blades, [], {"avoid melee":2, "avoid ranged":2})
b = Star(blades, a, {"pierce %":40})
c = Star(blades, b, {"pierce %":50})
d = Star(blades, b, {"attack speed":5})
e = Star(blades, b, {"attack speed":5})
f = Star(blades, b, {"armor piercing %":100})

targo = Constellation("Targo the Builder", "4o 6p", "1o")
a = Star(targo, [], {"defense":15})
b = Star(targo, a, {"health %":5})
c = Star(targo, b, {"armor %":5})
d = Star(targo, b, {"health %":5})
e = Star(targo, d, {"defense":20, "health":300})
f = Star(targo, d, {"armor %":5, "blocked damage %":20})
g = Star(targo, f, {})
#33% on attack (1.5 s to trigger)
#8 second recharge
#5 second duration
#9.5 seconds
g.addAbility(Ability(
	"Shield Wall", 
	# 5/9.5, 
	{"type":"buff", "trigger":"attack", "chance":.33, "recharge":8, "duration":5},
	{"damage reflect %":125, "blocked damage %":125, "armor %":30} ))

obelisk = Constellation("Obelisk of Menhir", "8o 15p")
a = Star(obelisk, [], {"armor %":7})
b = Star(obelisk, a, {"defense":30, "armor":150})
c = Star(obelisk, b, {"retaliation %":100})
d = Star(obelisk, a, {"defense %":5, "defense":25})
e = Star(obelisk, d, {"block %":5, "blocked damage %":30})
f = Star(obelisk, e, {"reduced stun duration":30, "reduced freeze duration":30, "armor %":4, "max pierce resist":3})
g = Star(obelisk, f, {})
#15% on block (1/.15/.75*.5) = 4.44 seconds to trigger
#12 second recharge
#8 second duration
#8/16.4
g.addAbility(Ability(
	"Stone Form", 
	# 8/16.4, 
	{"type":"buff", "trigger":"block", "chance":.15, "recharge":12, "duration":8},
	{"armor %":50, "armor absorb":20, "pierce resist":50, "reduced poison duration":50, "reduced bleed duration":50, "retaliation %":70} ))

soldier = Constellation("Unknown Soldier", "15a 8o")
a = Star(soldier, [], {"offense":15, "pierce %":60})
b = Star(soldier, a, {"bleed":21*3, "bleed %":80})
c = Star(soldier, b, {"lifesteal %":3, "attack speed":5, "health":150})
d = Star(soldier, b, {"bleed %":80, "pierce %":80})
e = Star(soldier, d, {"health %":4, "offense":40})
f = Star(soldier, e, {"pierce":20, "crit damage":10})
g = Star(soldier, f, {})
#100% on crit: 15% on attack
#6 second recharge
#3 summon limit
#20 second lifespan
# even more guessworky than most others...
# 2 attacks. shadow strike and shadow blades.
# I'm assuming strike is an engage and blades is the normal attack
# lets assume 1 strike and 5 normal attacks in a lifespan
# 3.3 s to trigger 6 second recharge means 2.5 lifespans in a 30 second fight.
g.addAbility(Ability(
	"Living Shadow", 
	# 2.5, 
	{"type":"summon", "trigger":"critical", "chance":1, "recharge":6, "lifespan":20},
	{"triggered bleed":35+(48*2*5), "triggered pierce":68.5+45.5*5} ))

scorpion = Constellation("Scorpion", "1e", "5e")
a = Star(scorpion, [], {"offense":12})
b = Star(scorpion, a, {"poison %":24})
c = Star(scorpion, b, {"offense":18})
d = Star(scorpion, c, {"acid %":15, "poison %":30})
e = Star(scorpion, c, {})
#25% on attack
#1.5 s recharge
#6 projectiles
#100% passthrough
# 4 hits
# reduced defense will count as offense
# 3 attack recharge, 4 attack trigger = 1/7
e.addAbility(Ability(
	"Scorpion Sting", 
	# 1.0/7, 
	{"type":"attack", "trigger":"attack", "chance":.25, "recharge":1.5, "targets":4},
	{"reduce defense":140, "triggered poison":320, "weapon damage %":30} ))

eye = Constellation("Eye of the Guaridan", "1e", "3a 3e")
a = Star(eye, [], {"acid %":15, "poison %":15})
b = Star(eye, a, {"chaos %":15})
c = Star(eye, b, {"chaos %":15, "poison %":15})
d = Star(eye, c, {"poison %":30})
e = Star(eye, d, {})
#15% on attack
#.5 s recharge
#100% pass through
#6.6 attacks to trigger 1 attack cooldown
e.addAbility("Guardian's Gaze", 1/7.6, {"weapon damage %":18, "triggered chaos":78, "triggered poison":156})

bat = Constellation("Bat", "1e", "2c 3e")
a = Star(bat, [], {"vitality %":15, "bleed %":15})
b = Star(bat, a, {"vitality decay":166*.15})
c = Star(bat, b, {"vitality %":24, "bleed %":30})
d = Star(bat, c, {"life leech %":30, "lifesteal %":3})
e = Star(bat, d, {})
#20% on attack
#1 second recharge
#2 projectiles
#70% pass through
# call it 2.5 hits on average
#2 attacks recharge and 5 attacks trigger
# 3.5 seconds between ~= 8 hits per fight. ~250 damage = 125 heal per hit = 1000 health per fight
e.addAbility("Twin Fangs", 2.5/7, {"weapon damage":25, "triggered pierce":116, "triggered vitality":111, "health":1000})

spider = Constellation("Spider", "1e", "6e")
a = Star(spider, [], {"cunning":10, "spirit":10})
b = Star(spider, a, {"offense":10, "chaos resist":8})
c = Star(spider, a, {"offense":15, "defense":10, "damage from insectoids":-12, "damage from arachnids":-12})
d = Star(spider, a, {"cunning %":3, "spirit %":3})
e = Star(spider, a, {"cast speed":3, "attack speed retaliation":20, "move speed retaliation":20})

raven = Constellation("Raven", "1e", "5e")
a = Star(raven, [], {"spirit":8, "pet all damage %":15})
b = Star(raven, a, {"energy/s":1, "spirit":10})
c = Star(raven, b, {"offense":15, "pet offense %":5})
d = Star(raven, b, {"all damage %":15, "pet lightning damage %":60})

fox = Constellation("Fox", "1e", "5e")
a = Star(fox, [], {"cunning":10})
b = Star(fox, a, {"bleed":10*3, "bleed %":24})
c = Star(fox, b, {"bleed resist":8, "cunning":15})
d = Star(fox, c, {"bleed":14*3, "bleed %":45})

light = Constellation("Scholar's Light", "1e", "4e")
a = Star(light, [], {"fire %":15})
b = Star(light, a, {"elemental resist":8, "physique":10})
c = Star(light, b, {"elemental %":24, "elemental":8, "energy/s":1.5})

hawk = Constellation("Hawk", "1e", "3e")
a = Star(hawk, [], {"offense":15})
b = Star(hawk, a, {"crit damage":8})
c = Star(hawk, b, {"offense %":3, "cunning ranged requirements":-10})

witchblade = Constellation("Solael's Witchblade", "4c 6e", "1c 1e")
a = Star(witchblade, [], {"chaos %":40})
b = Star(witchblade, a, {"offense":10, "spirit":15})
c = Star(witchblade, b, {"energy burn %":10, "chaos %":30})
d = Star(witchblade, c, {"fire %":50, "chaos %":50, "fire resist":15})
e = Star(witchblade, d, {})
#15% on attack
#4 second duration
# says "spreads wildly among your foes" so there's probably some aoe component but we're treating it as single target
e.addAbility("Eldritch Fire", 1/6.6, {"triggered fire":102, "triggered chaos":102, "slow move":33, "reduce fire resist":20, "reduce chaos resist":20})

bonds = Constellation("Bysmiel's Bonds", "4c 6e", "3e")
a = Star(bonds, [], {"offense":15, "pet all damage %":30})
b = Star(bonds, a, {"cast speed":5, "pet total speed":8})
c = Star(bonds, b, {"vitality resist":15, "pet vitality resist":20})
d = Star(bonds, c, {"all damage %":30, "pet all damage %":40, "pet health %":8})
e = Star(bonds, d, {})
#20% on attack
#30 second recharge
#20 second lifespan
#1 lifespan per fight
# ~7.5 attacks per lifespan
# this guy scales with pet damage so I'm not sure how to handle it
# there's a scale factor we need to account for somehow at some point
e.addAbility("Bysmiel's Command", 7.5, {"triggered physical":26.5, "triggered acid":38.5})

magi = Constellation("Magi", "10e", "3e")
a = Star(magi, [], {"fire %":40, "burn %":50})
b = Star(magi, a, {"elemental resist":8})
c = Star(magi, b, {"fire resist":25})
d = Star(magi, c, {"cast speed":5, "burn %":60})
e = Star(magi, c, {"fire":(6+8)/2, "fire %":40})
f = Star(magi, c, {"burn":12*3, "burn %":30, "burn duration":30})
g = Star(magi, f, {})
#15% on attack
#1.5 s recharge
#5 second duration
# 1 meter radius
#7 fragments
# call it 4 targets
# 3 attacks recharge 6.66 attacks trigger
g.addAbility("Fissure", 4/9.6, {"triggered fire":116, "triggered burn":264, "stun %":1.5})

berserker = Constellation("Berserker (requires axe)", "5a 5e", "2c 3e")
a = Star(berserker, [], {"offense":15})
b = Star(berserker, a, {"physical %":50})
c = Star(berserker, b, {"offense":25})
d = Star(berserker, a, {"bleed %":80, "lifesteal %":3})
e = Star(berserker, d, {"bleed %":100*.15, "bleed duration":100*.15, "crit damage":5})
f = Star(berserker, f, {"pierce resist":10, "reduced bleed duration":20})

lantern = Constellation("Oklaine's Lantern (requires scepter, dagger or caster off-hand)", "10e", "3e 2o")
a = Star(lantern, [], {"energy regeneration":15})
b = Star(lantern, a, {"offense":25})
c = Star(lantern, b, {"offense":15, "crit damage":5})
d = Star(lantern, c, {"all damage %":50, "reduced entrapment duration":25})
e = Star(lantern, d, {"cast speed":5, "attack speed":5, "energy/s":2})

behemoth = Constellation("Behemoth", "3c 4e 4p", "2c 3e")
a = Star(behemoth, [], {"health/s":10})
b = Star(behemoth, a, {"health":300, "pet health %":5})
c = Star(behemoth, b, {"health/s":15, "constitution %":25})
d = Star(behemoth, b, {"health %":4})
e = Star(behemoth, b, {"health regeneration":10, "pet health regeneration":20})
f = Star(behemoth, b, {})
#15 % when hit
#30s recharge
#10s duration
# will trigger once per 30s fight but will probably overheal
f.addAbility("Giant's Blood", .75, {"health%":20, "health":1000, "health/s":240})

affliction = Constellation("Affliction", "4a 3c 4e", "1a 1e")
a = Star(affliction, [], {"vitality %":40, "poison %":40})
b = Star(affliction, a, {"spirit":15, "vitality decay retaliation":600, })
c = Star(affliction, b, {"Fetid Pool":True})
#33% when hit
#2 second recharge
#6 second duration
# 3 meter radius
# 2 targets
# 4 hits recharge, 3.33 hits trigger
c.addAbility("Fetid Pool", 2/7.33, {"triggered vitality":128, "triggered poison":136, "slow move":25})
d = Star(affliction, c, {"offense":18, "defense":10})
e = Star(affliction, d, {"crit damage":10, "vitality decay retaliation":720})
f = Star(affliction, c, {"vitality":(11+21)/2, "acid resist":10})
g = Star(affliction, f, {"offense %":3, "vitality %":50, "acid %":50})

manticore = Constellation("Manticore", "4c 6e", "1a 1e")
a = Star(manticore, [], {"offense":15})
b = Star(manticore, a, {"acid %":50, "poison %":50})
c = Star(manticore, b, {"health %":4})
d = Star(manticore, c, {"offense":10, "acid resist":25})
e = Star(manticore, c, {"poison":8*5, "acid %":40, "poison %":40})
f = Star(manticore, e, {})
#15% on attack
#1 second recharge
#4 meter range
#call it 1.5 targets
#2 attack recharge 6.66 attack trigger
f.addAbility("Acid Spray", 1.5/8.66, {"triggered acid":148, "triggered poison":180, "reduce armor":250, "reduce resist":30})

abomination = Constellation("Abomination", "8c 18e")
a = Star(abomination, [], {"chaos %":80, "poison %":80})
b = Star(abomination, a, {"vitality %":80, "acid %":80})
c = Star(abomination, b, {"offense":40, "acid resist":20, "max acid resist":3})
d = Star(abomination, c, {"offense":20, "chaos %":80, "health":150})
e = Star(abomination, d, {})
#100% on enemy death
#18 s recharge
#12 s duration
#hard to say how long to kill an enemy. seems pretty darn quick mostly. Call it a second.
e.addAbility("Abominable Might", 12.0/19, {"chaos":336.5, "chaos %":230, "health %":20, "physical to chaos":50})
f = Star(abomination, c, {"offense":20, "poison %":80, "health":150})
g = Star(abomination, f, {"acid %":100, "poison %":100})
h = Star(abomination, g, {})
#15% on attack
#3 second recharge
#6 attacks recharge, 6.66 attacks trigger
# 10 meter radius
# call it 4 targets
h.addAbility("Tainted Eruption", 4/12.66, {"triggered poison":1320, "stun %":100})

sage = Constellation("Blind Sage", "10a 18e")
a = Star(sage, [], {"offense":15, "spirit":25})
b = Star(sage, a, {"offense":15, "elemental %":80})
c = Star(sage, b, {"crit damage":10, "skill disruption protection":30})
d = Star(sage, c, {"cold resist":20, "cold %":100, "frostburn %":100})
e = Star(sage, c, {"lightning %":100, "electrocute %":100, "lightning resist":20})
f = Star(sage, c, {"fire %":100, "burn %":100, "fire resist":20})
g = Star(sage, f, {})
#100% on attack
# 1.5 second recharge
# 5 s lifespan
# call it 2 attacks and a detonate each hitting 2 targets
# 4 attacks per
g.addAbility("Elemental Seeker", 1.0/4, {"triggered elemental":60*2*2+132*2, "stun %":100})

wolf = Constellation("Mogdrogen the Wolf", "15a 12e")
a = Star(wolf, [], {"offense":35, "pet offense %":5})
b = Star(wolf, a, {"bleed %":80, "pet all damage %":30})
c = Star(wolf, b, {"vitality resist":20, "pet total speed":6})
d = Star(wolf, c, {"bleed":25*5, "bleed %":80})
e = Star(wolf, d, {"bleed resist":15, "elemental resist":15, "max bleed resist":3, "pet all damage %":80})
f = Star(wolf, e, {})
#20% on attack
#15 s recharge
#10 s duration
# 5 attack trigger = 2.5 s
f.addAbility("Howl of Mogdrogen", 10/17.5, {"triggered bleed":396, "bleed %":200, "offense":120*.38, "attack speed":15, "pet offense %":15, "pet total speed":35})

rat = Constellation("Rat", "1c", "2c 3e")
a = Star(rat, [], {"cunning":8, "spirit":8})
b = Star(rat, a, {"poison":8*5, "poison %":24})
c = Star(rat, b, {"acid resist":10, "cunning":15, "spirit":15})
d = Star(rat, c, {"poison":12*5, "poison %":20, "poison duration":30})

ghoul = Constellation("Ghoul", "1c", "3c")
a = Star(ghoul, [], {"physique":10})
b = Star(ghoul, a, {"health/s":6, "life leech":15*2})
c = Star(ghoul, b, {"physique":10, "spirit":10})
d = Star(ghoul, b, {"health regeneration":15, "lifesteal %":4})
e = Star(ghoul, d, {})
# 100% at 33% health
# 30s recharge
# 6s duration
# lets say we hit 33% 1 / 3 fights
e.addAbility("Ghoulish Hunger", 6.0/30/3, {"life leach":442, "life leach %":135, "lifesteal %":60, "attack speed":20})

jackal = Constellation("Jackal", "1c", "3c")
a = Star(jackal, [], {"energy %":6, "pet health %":3})
b = Star(jackal, a, {"offense":12, "attack speed":6})
c = Star(jackal, b, {"all damage %":15, "pet attack speed":5})

fiend = Constellation("Fiend", "1c", "3c 3e")
a = Star(fiend, [], {"fire %":15, "chaos %":15})
b = Star(fiend, a, {"spirit":10, "pet fire damage %":25})
c = Star(fiend, b, {"chaos resist":8})
d = Star(fiend, c, {"fire %":24, "chaos %":24, "pet fire damage %":40})
e = Star(fiend, d, {})
#25% on attack
#.5 s recharge
#100% pass through
# 2 projectiles
# 2.5 targets
# 1 attack recharge, 4 attack trigger
e.addAbility("Flame Torrent", 2.5/5, {"weapon damage %":35, "triggered fire":132, "triggered chaos":56, "triggered burn":504})

viper = Constellation("Viper", "1c", "2c 3p")
a = Star(viper, [], {"spirit":10})
b = Star(viper, a, {"energy absorb":10, "energy leech":18*2*.15})
c = Star(viper, b, {"vitality resist":10})
d = Star(viper, c, {"offense %":3, "reduce elemental resist":20})

vulture = Constellation("Vulture", "1c", "5c")
a = Star(vulture, [], {"cunning":10})
b = Star(vulture, a, {"bleed resist":15})
c = Star(vulture, b, {"life leech":15*2, "life leech resist":30})
d = Star(vulture, b, {"cunning %":5})
e = Star(vulture, b, {"vitality resist":15, "life leech %":50})

wendigo = Constellation("Wendigo", "4c 6p", "2c")
a = Star(wendigo, [], {"vitality %":40, "vitality decay %":40})
b = Star(wendigo, a, {"spirit":15, "health":100})
c = Star(wendigo, b, {"cast speed":5, "vitality resist":10})
d = Star(wendigo, c, {"health %":5, "damage from beasts":-10})
e = Star(wendigo, d, {"vitality %":50, "vitality decay %":50, "life leech %":50})
f = Star(wendigo, e, {})
# 25% on attack
# 8s duration
# I have no idea how this one works. I'm guessing vitality damage per second for the duration.
f.addAbility("Wendigo's Mark", .5, {"triggered vitality":186, "health":186*.9})

hydra = Constellation("Hydra (requires ranged)", "3a 3c 5e", "2c 3e")
a = Star(hydra, [], {"offense":15})
b = Star(hydra, a, {"all damage %":15})
c = Star(hydra, b, {"pierce %": 40})
d = Star(hydra, b, {"offense":20})
e = Star(hydra, d, {"offense %":3, "slow resist":20})
f = Star(hydra, b, {"all damage %":35})

chariot = Constellation("Chariot of the Dead", "5a 5e", "2c 3e")
a = Star(chariot, [], {"cunning":15})
b = Star(chariot, a, {"offense":15})
c = Star(chariot, b, {"cunning":20})
d = Star(chariot, c, {"vitality resist":10})
e = Star(chariot, c, {"offense":25})
f = Star(chariot, e, {"offense %":3, "offense":10})
g = Star(chariot, f, {})
# 100% when hit by critical: ??? .15% when hit
#18 s recharge
#7 s duration
#6.66 s to trigger so 7/24.66
g.addAbility("Wayward Soul", 7/24.66, {"health %":10, "health":1300, "defense":120})

revenant = Constellation("Revenant", "8c", "1c 1p")
a = Star(revenant, [], {"energy leech":20*2*.1, "lifesteal %":3})
b = Star(revenant, a, {"health %":3, "damage from undead":-10})
c = Star(revenant, b, {"vitality resist":20, "pet vitality resist":15})
d = Star(revenant, c, {"energy absorb":15, "lifesteal %":6})
e = Star(revenant, d, {"damage undead %":15, "attack speed":6, "pet lifesteal %":5})
f = Star(revenant, e, {})
#100% on enemy death
#3 s recharge
#5 summon limit
# 25 s lifespan
# 10 attacks per summon (1/2.5s)
#scales with pet bonuses which I don't have an answer for
# 1-26 = 10
# 5-30 = 10
# 9-34 = 8
# 13-38 = 6
# 17-42 = 5
f.addAbility("Raise the Dead", 39, {"triggered physical":18, "slow move":.25})

torch = Constellation("Ulzuin's Torch", "8c 15e")
a = Star(torch, [], {"offense":20, "fire %":80})
b = Star(torch, a, {"offense %":5, "chaos resist":15})
c = Star(torch, b, {"move %":5, "crit damage":10})
d = Star(torch, c, {"fire %":100, "fire resist":20})
e = Star(torch, d, {"burn":25*3, "burn %":100, "max fire resist":3})
f = Star(torch, c, {"burn %":100, "burn duration":100})
g = Star(torch, f, {})
#30% on attack
#3.5s recharge
#3 s duration
#6m area
#2m radius
#15 meteors
#call it 15 hits...
# 3.3 attacks trigger, 7 attacks recharge
g.addAbility("Meteor Shower", 15/10.3, {"triggered fire":90, "triggered physical":90, "triggered burn":164/2})

god = Constellation("Dying God", "8c 15p")
a = Star(god, [], {"offense":20, "vitality %":80})
b = Star(god, a, {"offense":20, "chaos %":80})
c = Star(god, b, {"offense %":3, "spirit":25, "pet all damage %":30, "pet attack speed":5})
d = Star(god, c, {"offense":45, "chaos resist":15})
e = Star(god, d, {"vitality %":100, "chaos %":100})
f = Star(god, e, {"chaos":(5+24)/2, "pet all damage %":60, "pet crit damage":10})
g = Star(god, f, {})
#100% on attack
#30s recharge
#20s duration
#12 meter radius
g.addAbility("Hungering Void", 20.0/31, {"health/s":-275, "crit damage":30, "vitality %":215, "chaos%":215, "total speed":8, "chaos retaliation":485, "terrify retaliation":55, "pet all damage %":150, "pet crit damage":20, "stun %":10, "slow move":30*.45})

imp = Constellation("Imp", "1p", "3e 3p")
a = Star(imp, [], {"fire %":15, "aether %":15})
b = Star(imp, a, {"spirit":10})
c = Star(imp, b, {"aether resist":8})
d = Star(imp, c, {"fire %":24, "aether %":24})
e = Star(imp, d, {})
#15% on attack
#3s duration
#2.5 radius
#1.5 targets
e.addAbility("Aetherfire", 1.5/6.66, {"trigered fire":50, "triggered aether":125, "stun %":33})

tsunami = Constellation("Tsunami", "1p", "5p")
a = Star(tsunami, [], {"lightning %": 15, "cold %":15})
b = Star(tsunami, a, {"spirit":10})
c = Star(tsunami, b, {"electrocute %":40, "frostburn %":40})
d = Star(tsunami, c, {"lightning %":24, "cold %":24})
e = Star(tsunami, d, {})
#35% on attack
#1.5s recharge
#12m range
# call it 2 targets
#2.85 attacks trigger, 3 attacks recharge
e.addAbility("Tsunami", 2/5.85, {"weapon damage %":32, "triggered cold":115, "triggered lightning":51})

gallows = Constellation("Gallows", "1p", "5p")
a = Star(gallows, [], {"vitality %":15})
b = Star(gallows, a, {"life leech retaliation":100*.15})
c = Star(gallows, b, {"vitality resist":10})
d = Star(gallows, c, {"vitality":7, "vitality %":24, "chaos %":24})

lizard = Constellation("Lizard", "1p", "4p")
a = Star(lizard, [], {"health/s":6, "constitution %":15})
b = Star(lizard, a, {"health/s":10, "health":50})
c = Star(lizard, b, {"constitution %":15, "health regeneration":15})

guide = Constellation("Sailor's Guide", "1p", "5p")
a = Star(guide, [], {"physique":10})
b = Star(guide, a, {"reduced freeze":15, "slow resist":15})
c = Star(guide, b, {"move %":5, "physique":10})
d = Star(guide, b, {"cold resist":15, "lightning resist":15})

bull = Constellation("Bull", "1p", "2o 3p")
a = Star(bull, [], {"physique":10})
b = Star(bull, a, {"internal %":24, "internal duration":20})
c = Star(bull, b, {"stun %":8, "stun duration":10})
d = Star(bull, c, {"internal":12*5, "armor physique requirements":-10})
e = Star(bull, d, {})
#25% on attack
#.5s recharge
#3.5 meter radius
# 2 targets
# 4 attacks trigger, 1 attack recharge
e.addAbility("Bull Rush", 2.0/5, {"weapon damage %":45, "triggered physical":114, "triggered internal":250})

wraith = Constellation("Wraith", "1p", "3a 3p")
a = Star(wraith, [], {"aether %":15, "lightning %":15})
b = Star(wraith, a, {"spirit":10, "aether resist":8})
c = Star(wraith, a, {"energy absorb":15, "offense":10})
d = Star(wraith, a, {"aether":4, "aether %":24, "lightning":(1+7)/2, "lightning %":24})

eel = Constellation("Eel", "1p", "5p")
a = Star(eel, [], {"defense":10, "avoid melee":2})
b = Star(eel, a, {"defense":10, "avoid ranged":2})
c = Star(eel, b, {"pierce resist":10, "defense":10})

hound = Constellation("Hound", "1p", "4p")
a = Star(hound, [], {"physique":10, "pet health %":4})
b = Star(hound, a, {"armor %":2, "pierce retaliation":30, "retaliation %":20})
c = Star(hound, b, {"armor %":2, "physique":15, "retaliation %":30, "pet retaliation %":30})

messenger = Constellation("Messenger of War", "3a 7p", "2c 3p")
a = Star(messenger, [], {"pierce retaliation":90, "retaliation %":30})
b = Star(messenger, a, {"move %":5, "physique":10})
c = Star(messenger, b, {"armor":50, "retaliation %":50})
d = Star(messenger, c, {"armor %":6, "pierce retaliation":120})
e = Star(messenger, b, {"pierce resist":15, "damage reflect %":25})
f = Star(messenger, e, {})
# 20% when hit
# 15s recharge
# 8s duration
f.addAbility("Messenger of War", 8/17.5, {"move speed":30, "slow resist":70, "pierce retaliation":2400, "retaliation %":200})

tempest = Constellation("Tempest", "5a 5p", "1e 1p")
a = Star(tempest, [], {"lightning %":40})
b = Star(tempest, a, {"lightning":(1-24)/2})
c = Star(tempest, b, {"lightning %":50, "electrocute %":50})
d = Star(tempest, c, {"offense":10, "lightning resist":25})
e = Star(tempest, d, {"move %":3, "lightning %":200*.3})
f = Star(tempest, d, {"offense":15, "electrocute %":50, "electrocute duration":30})
g = Star(tempest, f, {})
#100% on critical: 15% on attack
#10s recharge
#6s duration
# 3 target max
# 8 meter radius
# .5s interval
# 36/26.66
g.addAbility("Reckless Tempest", 12*3/26.66, {"triggered lightning":113.5, "triggered, electrocute":256/2, "stun %":20})

widow = Constellation("Widow", "6e 4p", "3p")
a = Star(widow, [], {"aether %":40})
b = Star(widow, a, {"offense":18, "energy %":5})
c = Star(widow, b, {"aether %":30, "spirit":10})
d = Star(widow, c, {"vitality resist":8, "aether resist":18})
e = Star(widow, d, {"aether %":50, "lightning %":50})
f = Star(widow, e, {})
#25% on attack
#2s recharge
# 2 targets
# 4 attack to trigger 4 to recharge
f.addAbility("Arcane Bomb", 2.0/8, {"triggered lightning":40, "triggered aether":40, "defense":35, "reduce lightning resist":5, "reduce aether resist":5})

kraken = Constellation("Kraken (requires two-hand)", "5e 5p", "2c 3p")
a = Star(kraken, [], {"all damage %":35})
b = Star(kraken, a, {"physical %":40, "attack speed":10})
c = Star(kraken, a, {"physical %":40, "attack speed":10})
d = Star(kraken, a, {"all damage %":50, "move %":5})
e = Star(kraken, a, {"all damage %":35, "crit damage":15})

winter = Constellation("Amatok the Spirit of Winter", "4e 6p", "1e 1p")
a = Star(winter, [], {"cold %":40})
b = Star(winter, a, {"health %":3, "defense":15})
c = Star(winter, b, {"cold resist":25, "offense":10})
d = Star(winter, b, {"cold %":50, "frostburn %":50})
e = Star(winter, d, {"frostburn":12*3, "frostburn %":70})
f = Star(winter, b, {"offense":15, "frostburn %":30, "frostburn duration":30})
g = Star(winter, f, {})
#100% on crit: 15% on attack
#3.5s recharge
#1.5m radius
#6.66 attacks to trigger, 7 attacks to recharge
#looks like there are multiple missiles but it's not listed
g.addAbility("Blizzard", 4.0/13.66, {"weapon damage %":10, "triggered cold":165.5, "triggered frostburn":164, "stun %":36, "slow move":54})

bear = Constellation("Dire Bear", "5a 5p", "1a 1p")
a = Star(bear, [], {"physical %":40})
b = Star(bear, a, {"physique":10, "cunning":10})
c = Star(bear, b, {"constitution %":15, "attack speed":5})
d = Star(bear, c, {"reduced stun duration":15, "reduced freeze duration":15, "health %":5})
e = Star(bear, [], {"physical %":50, "internal %":50})
f = Star(bear, d, {})
#15% on attack
#1s recharge
#4m radius
#2 targets
f.addAbility("Maul", 2.0/8.66, {"weapon damage %":75, "triggered physical":161.5, "stun %":100})

ulo = Constellation("Ulo the Keeper of the Waters", "4o 6p", "2o 3p")
a = Star(ulo, [], {"elemental resist":10, "pet elemental resist":10})
b = Star(ulo, a, {"life leech resist":30, "energy leech resist":30})
c = Star(ulo, b, {"acid resist":15, "pet acid resist":15})
d = Star(ulo, b, {"chaos resist":10, "pet chaos resist":10})
e = Star(ulo, b, {})
# 100% on attack
#22s recharge
#1s duration (actually 8)
#3m radius
#2 targets
# 44 attacks recharge, 1 attack trigger
e.addAbility("Cleansing Waters", 8.0/45, {"slow move":40})

watcher = Constellation("Solemn Watcher", "10p", "2o 3p")
a = Star(watcher, [], {"physique":15})
b = Star(watcher, a, {"cold resist":25})
c = Star(watcher, b, {"pierce resist":18})
d = Star(watcher, c, {"defense":30, "physique %":3})
e = Star(watcher, d, {"defense %":5, "reflected damage reduction":20})

hourglass = Constellation("Aeon's Hourglass", "8c 18p")
a = Star(hourglass, [], {"physique":30, "cunning":30, "spirit":30})
b = Star(hourglass, a, {"defense":25, "reduced burn duration":20, "reduced frostburn duration":20, "reduced electrocute duration":20})
c = Star(hourglass, b, {"slow resist":50, "aether resist":20})
d = Star(hourglass, c, {"defense":35, "vitality resist":15, "max vitality resist":4})
e = Star(hourglass, d, {"avoid melee":6, "avoid ranged":6, "reduced entrapment duration":30, "reflected damage reduction":25})
f = Star(hourglass, e, {})
#30 chance when hit
#3s recharge
#3m radius
# 3.33 for trigger, 6 for recharge
# 1.5 targets
f.addAbility("Time Stop", 1.5/9.33, {"stun %":100, "slow move":70})

spear = Constellation("Spear of the Heavens", "7c 20p")
a = Star(spear, [], {"offense":20, "lightning %":80})
b = Star(spear, a, {"offense":20, "aether %":80})
c = Star(spear, b, {"offense %":5, "aether resist":15})
d = Star(spear, c, {"crit damage":10, "lightning resist":20})
e = Star(spear, d, {"aether %":100, "lightning %":100, "max lightning resist":3})
f = Star(spear, e, {})
#50% when hit
#1s recharge
#.5m radius
#2 for recharge, 2 for trigger
f.addAbility("Spear of the Heavens", 1.0/4, {"triggered lightning":162, "triggered aether":176, "stun %":100})

tree = Constellation("Tree of Life", "7o 20p")
a = Star(tree, [], {"health %":5, "pet health %":5})
b = Star(tree, a, {"health/s":20, "pet health regeneration":20})
c = Star(tree, b, {"health %":8, "pet health %":5})
d = Star(tree, b, {"health/s":15, "defense":30, "pet health regeneration":20})
e = Star(tree, d, {"health %":4, "health regeneration":20, "pet health/s":50})
f = Star(tree, d, {})
#25% when hit
#12s recharge
#8s 2 per
f.addAbility("Healing Rain", 16.0/28, {"health/s":100, "energy/s":10, "health regeneration":50, "energy regeneration":50, "health%":10*2, "health":550*2})

empyrion = Constellation("Light of Empyrion", "8o 18p")
a = Star(empyrion, [], {"elemental resist":10, "pet elemental resist":10}) #not quite right but close enough
b = Star(empyrion, a, {"fire %":80, "damage chthonics %":10})
c = Star(empyrion, b, {"elemental resist":15, "pet elemental resist":15})
d = Star(empyrion, c, {"vitality resist":15, "pet vitality resist":15})
e = Star(empyrion, d, {"aether resist":15, "chaos resist":15, "pet aether resist":15, "pet chaos resist":15})
b = Star(empyrion, a, {"fire":(8+14)/2, "max aether resist":3, "max chaos resist":3, "pet max all resist":5})
g = Star(empyrion, f, {})
#20% when attacked
#4s recharge
#5m radius
# 2 targets
# 8 recharge, 5 triggerd
g.addAbility("Light of Empyrion", 2.0/13, {"weapon damage %":35, "triggered fire":226, "triggered burn":204, "stun %":50, "reduce armor":225, "damage to undead":50, "damage to cthonics":50})