from dataModel import *

xA = Constellation("Crossroads Ascendant", "", "1a")
xA.id = "xA"
Star(xA, [], {"offense":15})
xC = Constellation("Crossroads Chaos", "", "1c")
xC.id = "xC"
Star(xC, [], {"health %":5})
xE = Constellation("Crossroads Eldrich", "", "1e")
xE.id = "xE"
Star(xE, [], {"offense":15})
xO = Constellation("Crossroads Order", "", "1o")
xO.id = "xO"
Star(xO, [], {"health %":5})
xP = Constellation("Crossroads Primordial", "", "1p")
xP.id = "xP"
Star(xP, [], {"defense":15})

	# ignore this
	# we'll use 75% chance of triggering for our timing
	# 1-((1-.15)^x) = .75 -> log_.25(1-.15) = 8.5 attacks to trigger after cooldown, 4 attacks in the cooldown

falcon = Constellation("Falcon", "1a", "3a 3e")
falcon.id = "falcon"
a = Star(falcon, [], {"physical %":15})
b = Star(falcon, a, {"bleed %":24})
c = Star(falcon, b, {"cunning":15})
d = Star(falcon, c, {"physical %":24})
e = Star(falcon, d, {})
# 6 projectiles
# 150 deg cone 
# multi hit doesnt stack
e.addAbility(Ability(
	"Falcon Swoop", {"type":"attack", "trigger":"attack", "chance":.15, "recharge":1, "targets":3, "shape":"cone"}, 
	{"weapon damage %":65, "triggered bleed":[135,3]} ))

shepherd = Constellation("Shepherd's Crook", "1a", "5a")
shepherd.id = "shepherd"
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
hammer.id = "hammer"
a = Star(hammer, [], {"physical %":15})
b = Star(hammer, a, {"defense":8, "internal %":30})
c = Star(hammer, b, {"physical %":15, "internal %":30})

anvil = Constellation("Anvil", "1a", "5a")
anvil.id = "anvil"
anvil.restricts = ["shield"]
a = Star(anvil, [], {"defense":10})
b = Star(anvil, a, {"physique":10})
c = Star(anvil, b, {"armor absorb":3})
d = Star(anvil, c, {"defense":15, "constitution %":20})
e = Star(anvil, d, {"Targo's Hammer":True})
# like the eye. summons a hammer that floats around me smackin shit it hits.
e.addAbility(Ability("Targo's Hammer", 
	{"type":"attack", "trigger":"block", "chance":.25, "targets":2, "shape":"pbaoe"},
	{"stun %":50, "weapon damage %":92*5, "triggered physical":100*5, "internal %":145} ))

owl = Constellation("Owl", "1a", "5a")
owl.id = "owl"
a = Star(owl, [], {"spirit":10})
b = Star(owl, a, {"elemental resist":8, "skill cost %":-5})
c = Star(owl, b, {"burn %":30, "electrocute %":30, "frostburn %":30})
d = Star(owl, b, {"elemental %":24, "reflected damage reduction":15})

harpy = Constellation("Harpy", "1a", "5a")
harpy.id = "harpy"
a = Star(harpy, [], {"pierce %":15, "cold %":15})
b = Star(harpy, a, {"cunning":10})
c = Star(harpy, b, {"bleed resist":10, "offense":15})
d = Star(harpy, b, {"pierce":(3+7)/2, "pierce %":24, "cold %":24})

throne = Constellation("Empty Throne", "1a", "5a")
throne.id = "throne"
a = Star(throne, [], {"reduced stun duration":15})
b = Star(throne, a, {"pierce resist":8, "pet pierce resist":8})
c = Star(throne, b, {"chaos resist":8, "pet chaos resist":8})
d = Star(throne, b, {"aether resist":8, "pet aether resist":8})

wolverine = Constellation("Wolverine", "1a", "6a")
wolverine.id = "wolverine"
a = Star(wolverine, [], {"defense":15, "pet pierce resist":10})
b = Star(wolverine, a, {"pierce retaliation":30, "retaliation %":20, "pet pierce retaliation":50})
c = Star(wolverine, b, {"defense":18, "pet bleed resist":25})
d = Star(wolverine, c, {"retaliation %":35, "pet retaliation %":50})
e = Star(wolverine, c, {"defense %":3, "melee weapon physique requirements":-10, "melee weapon cunning requirements":-10, "pet defense %":5})

crab = Constellation("Crab", "6a 4o", "3a")
crab.id = "crab"
a = Star(crab, [], {"constitution %":15, "physique":20})
b = Star(crab, a, {"elemental %":30, "internal %":70})
c = Star(crab, b, {"Elemental Barrier":True})
d = Star(crab, c, {"pierce resist":18, "defense":10})
e = Star(crab, d, {"elemental %":40, "elemental resist":15})

scepter = Constellation("Rhowan's Scepter", "6a 4o", "3a 2o")
scepter.id = "scepter"
scepter.restricts = ["mace"]
a = Star(scepter, [], {"defense":15})
b = Star(scepter, a, {"health %":6})
c = Star(scepter, b, {"physical %":50})
d = Star(scepter, c, {"internal %":80})
e = Star(scepter, b, {"defense":18})
f = Star(scepter, e, {"physical":(8+12)/2,"stun %":5, "stun duration":10})

boar = Constellation("Autumn Boar", "4a 3o 4p", "3a")
boar.id = "boar"
boar.restricts = ["shield"]
a = Star(boar, [], {"physique":10, "cunning":10})
b = Star(boar, a, {"pierce resist":15, "physique":10})
c = Star(boar, b, {"physique %":5})
d = Star(boar, c, {"physical resist":4, "fire resist":20})
e = Star(boar, c, {"stun duration":10, "physical retaliation":150})
f = Star(boar, e, {"bleed retaliation":2100*.1})
g = Star(boar, e, {})
# long line in diretion of hitter
g.addAbility(Ability(
	"Trample", 
	{"type":"attack", "trigger":"block", "chance":.25, "recharge":1, "targets":2.5, "shape":"line"},
	{"stun %":100, "weapon damage %":80, "internal":404} ))

scythe = Constellation("Harvestman's Scythe", "3a 3o 5p", "3a 3p")
scythe.id = "scythe"
a = Star(scythe, [], {"energy/s":2})
b = Star(scythe, a, {"health/s":12})
c = Star(scythe, b, {"physique %":4, "constitution %":20})
d = Star(scythe, c, {"health regeneration":20})
e = Star(scythe, d, {"energy regeneration":20})
f = Star(scythe, e, {"cunning %":4, "spirit %":4})

crown = Constellation("Rhowan's Crown", "4a 6e", "1a 1e")
crown.id = "crown"
a = Star(crown, [], {"elemental %":30, "elemental":(6+9)/2})
b = Star(crown, a, {"spirit":20, "pet elemental %":40})
c = Star(crown, b, {})
storm = Ability(
	"Elemental Storm",
	{"type":"attack", "trigger":"attack", "chance":.25, "recharge":1.5, "duration":5, "targets":2.5, "shape":"ground"},
	{"triggered elemental":114*5, "duration":{"triggered frostburn":100, "triggered electrocute":100, "triggered burn":100, "reduce elemental resist":30/2.5}})
c.addAbility(storm)
d = Star(crown, c, {"elemental resist":18, "pet elemental resist":10})
e = Star(crown, d, {"elemental %":40, "burn %":60, "electrocute %":60, "frostburn %":60, "chaos resist":8})

huntress = Constellation("Huntress", "4a 3c 4e", "1a 1e")
huntress.id = "huntress"
a = Star(huntress, [], {"offense":15})
b = Star(huntress, a, {"pierce %":35})
c = Star(huntress, b, {"bleed %":60})
d = Star(huntress, c, {"pierce resist":8, "damage beast %":15, "health":100})
e = Star(huntress, c, {"offense %":3, "pet offense %":5})
f = Star(huntress, e, {"bleed":30, "bleed %":50, "bleed duration":20})
g = Star(huntress, e, {})
# no stat for reducing opponent offense so we'll call it defense

#halfway between an attack and a buff. Since the debuff doesn't overlap I'm going to set the recharge to the duration.
# this will slightly undervalue the skill as it can refresh within it's duration.
# I can't decide if I want to use targets. The "defense" part assumes I'll hit everything hitting me so it's over valued.
# the bleed resist reduction feels like I shouldn't count it per target since it only matters on the things I'm hitting and hitting things is already accounted for.

# I'm treating reduced offense like defense so don't count the targets (it's built into that conversion)
# reduced resist only matters when other stuff hits so reducing resist on stuff I'm not hitting doesn't count for anything.
# remove the multi target component (I'm overcounting defense and undercounting reduced resist a bit).
rend = Ability("Rend", 
	{"type":"attack", "trigger":"attack", "chance":.2, "recharge":0, "duration":5, "targets":3, "shape":"circle"},
	{"triggered bleed":[307,5], "duration":{"defense":125/3, "reduce bleed resist":33/3}} )
g.addAbility(rend)

leviathan = Constellation("Leviathan", "13a 13e")
leviathan.id = "leviathan"
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
# ticks per second, cold stacks, fostburn doesnt
# big radius but i'm taking a damage tick away because it's long lasting ground target
g.addAbility(Ability(
	"Whirlpool", 
	{"type":"attack", "trigger":"attack", "chance":.3, "recharge":3, "targets":3, "duration":6, "shape":"ground"}, 
	{"triggered cold":322*5, "duration":{"triggered frostburn":133, "slow move":35}} ))
# g.addAbility(Ability(	
	# "TEST", 
	# {"type":"attack", "trigger":"attack", "chance":1, "recharge":0, "targets":1, "duration":1}, 
	# {"triggered cold":100, "duration":{"triggered frostburn":100, "offense":35}} ))

oleron = Constellation("Oleron", "20a 7o")
oleron.id = "oleron"
a = Star(oleron, [], {"physique":20, "cunning":20, "health":100})
b = Star(oleron, a, {"physical %":80, "internal %":80})
c = Star(oleron, b, {"pierce resist":20, "bleed resist":10, "offense":30})
d = Star(oleron, c, {"physical resist":4, "health":200})
e = Star(oleron, d, {"physical":(9+18)/2, "physical %":100})
f = Star(oleron, d, {"offense":15, "internal":25*5, "internal %":100, "max pierce resist":2})
g = Star(oleron, d, {})

# If we assume everything has enough armor for all of the reduce armor to take effect (if they have less and we're doing physical damage they're probably dead already anyway)
# Then if we know our flat physical we can assume 70% absorb
g.addAbility(Ability(
	"Blind Fury", 
	{"type":"attack", "trigger":"critical", "chance":1, "recharge":1, "duration":5, "targets":2.5, "shape":"pbaoe"},
	{"weapon damage %":85, "triggered internal":[162,2], "triggered bleed":[162,2], "duration":{"slow attack":25, "reduce armor":275}} ))

tortoise = Constellation("Tortoise", "1o", "2o 3p")
tortoise.id = "tortoise"
a = Star(tortoise, [], {"defense":10, "health":25})
b = Star(tortoise, a, {"defense":12, "shield physique requirements":-10})
c = Star(tortoise, b, {"defense":12, "health":100})
d = Star(tortoise, c, {"health %":4, "defense":10, "armor %":4})
e = Star(tortoise, c, {})
e.addAbility(Ability(
	"Turtle Shell", 
	{"type":"shield", "trigger":"low health", "chance":1, "recharge":30},
	{"health":2700} ))

blade = Constellation("Assassin's Blade", "1o", "3a 2o")
blade.id = "blade"
a = Star(blade, [], {"pierce %":15})
b = Star(blade, a, {"offense":12})
c = Star(blade, a, {"bleed %":15, "pierce %":15})
d = Star(blade, c, {"bleed %":30})
e = Star(blade, d, {})
e.addAbility(Ability(
	"Assassin's Mark", 
	{"type":"buff", "trigger":"critical", "chance":1, "recharge":0, "duration":15},
	{"reduce physical resist":33, "reduce pierce resist":33} ))

lion = Constellation("Lion", "1o", "3o")
lion.id = "lion"
a = Star(lion, [], {"health %":4, "defense":8, "pet health %":3})
b = Star(lion, a, {"spirit":10, "health":100})
c = Star(lion, b, {"all damage %":15, "pet all damage %":12})

crane = Constellation("Crane", "1o", "5o")
crane.id = "crane"
a = Star(crane, [], {"physique":8, "spirit":8})
b = Star(crane, a, {"acid resist":12})
c = Star(crane, b, {"all damage %":15, "weapon spirit requirements":-10})
d = Star(crane, c, {"vitality resist":8})
e = Star(crane, d, {"elemental resist":10})

panther = Constellation("Panther", "1o", "2o 3p")
panther.id = "panther"
a = Star(panther, [], {"offense":12, "pet offense %":2})
b = Star(panther, a, {"cunning":8, "spirit":8, "pet all damage %":15})
c = Star(panther, b, {"all damage %":15, "energy regeneration":10, "pet offense %":3})
d = Star(panther, c, {"offense":20, "pet crit damage":5})

dryad = Constellation("Dryad", "1o", "3o")
dryad.id = "dryad"
a = Star(dryad, [], {"acid resist":10, "energy":200})
b = Star(dryad, a, {"energy/s":1, "health":80})
c = Star(dryad, b, {"reduced poison duration":20, "reduced bleed duration":20})
d = Star(dryad, c, {"spirit %":5, "jewelry spirit requirements":-10})
e = Star(dryad, d, {})
e.addAbility(Ability(
	"Dryad's Blessing", 
	{"type":"heal", "trigger":"attack", "chance":.33, "recharge":4},
	{"health %":8, "health":350, "reduced poison duration":30, "reduced bleed duration":30} ))

shieldmaiden = Constellation("Shieldmaiden", "4o 6p", "2o 3p")
shieldmaiden.id = "shieldmaiden"
shieldmaiden.restricts = ["shield"]
a = Star(shieldmaiden, [], {"block %":4})
b = Star(shieldmaiden, a, {"armor absorb":5})
c = Star(shieldmaiden, b, {"blocked damage %":18})
d = Star(shieldmaiden, c, {"retaliation %":50})
e = Star(shieldmaiden, b, {"reduced stun duration":25, "blocked damage %":15})
f = Star(shieldmaiden, e, {"shield recovery":15, "stun retaliation":15})

scales = Constellation("Scales of Ulcama", "8o", "2o")
scales.id = "scales"
a = Star(scales, [], {"health":250, "energy":300})
b = Star(scales, a, {"health/s":6, "health regeneration":10})
c = Star(scales, b, {"health %":6})
d = Star(scales, c, {"energy regeneration":10, "energy/s":2})
e = Star(scales, b, {"all damage %":30})
f = Star(scales, e, {})
# assuming single target
f.addAbility(Ability(
	"Tip the Scales", 
	# 1.0/8, 
	{"type":"attack", "trigger":"hit", "chance":.2, "recharge":1.5},
	{"triggered vitality":170, "energy":320, "attack as health %":135} ))

assassin = Constellation("Assassin", "6a 4o", "1a 1o")
assassin.id = "assassin"
a = Star(assassin, [], {"pierce %":30})
b = Star(assassin, a, {"cunning":15})
c = Star(assassin, b, {"offense":18, "defense":10})
d = Star(assassin, b, {"bleed resist":8, "cunning %":5})
e = Star(assassin, d, {"defense":12, "acid resist":8, "damage human %":15})
f = Star(assassin, d, {"pierce":6, "pierce %":40})
g = Star(assassin, f, {})

# projectiles fire in every direction. I think I'll use pbaoe shape since it's best if surrounded.
g.addAbility(Ability(
	"Blades of Wrath", 
	{"type":"attack", "trigger":"critical", "chance":1, "recharge":2, "targets":4, "shape":"pbaoe"},
	{"triggered pierce":168, "weapon damage %":25} ))

blades = Constellation("Blades of Nadaan", "10a", "3a 2o")
blades.id = "blades"
blades.restricts = ["sword"]
a = Star(blades, [], {"avoid melee":2, "avoid ranged":2})
b = Star(blades, a, {"pierce %":40})
c = Star(blades, b, {"pierce %":50})
d = Star(blades, b, {"attack speed":5})
e = Star(blades, b, {"attack speed":5})
f = Star(blades, b, {"armor piercing %":100})

targo = Constellation("Targo the Builder", "4o 6p", "1o")
targo.id = "targo"
targo.restricts = ["shield"]
a = Star(targo, [], {"defense":15})
b = Star(targo, a, {"health %":5})
c = Star(targo, b, {"armor %":5})
d = Star(targo, b, {"health %":5})
e = Star(targo, d, {"defense":20, "health":300})
f = Star(targo, d, {"armor %":5, "blocked damage %":20})
g = Star(targo, f, {})
g.addAbility(Ability(
	"Shield Wall", 
	{"type":"buff", "trigger":"attack", "chance":.33, "recharge":8, "duration":5},
	{"damage reflect %":125, "blocked damage %":125, "armor %":30} ))

obelisk = Constellation("Obelisk of Menhir", "8o 15p")
obelisk.id = "obelisk"
obelisk.restricts = ["shield"]
a = Star(obelisk, [], {"armor %":7})
b = Star(obelisk, a, {"defense":30, "armor":150})
c = Star(obelisk, b, {"retaliation %":100})
d = Star(obelisk, a, {"defense %":5, "defense":25})
e = Star(obelisk, d, {"block %":5, "blocked damage %":30})
f = Star(obelisk, e, {"reduced stun duration":30, "reduced freeze duration":30, "armor %":4, "max pierce resist":3})
g = Star(obelisk, f, {})
g.addAbility(Ability(
	"Stone Form", 
	{"type":"buff", "trigger":"block", "chance":.15, "recharge":12, "duration":8},
	{"armor %":50, "armor absorb":20, "pierce resist":50, "reduced poison duration":50, "reduced bleed duration":50, "retaliation %":70} ))

soldier = Constellation("Unknown Soldier", "15a 8o")
soldier.id = "soldier"
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
	{"type":"summon", "trigger":"critical", "chance":1, "recharge":6, "lifespan":20},
	{"triggered bleed":35+(48*2*5), "triggered pierce":68.5+45.5*5} ))

scorpion = Constellation("Scorpion", "1e", "5e")
scorpion.id = "scorpion"
a = Star(scorpion, [], {"offense":12})
b = Star(scorpion, a, {"poison %":24})
c = Star(scorpion, b, {"offense":18})
d = Star(scorpion, c, {"acid %":15, "poison %":30})
e = Star(scorpion, c, {})
# it's a pbaoe with a decent range. It's weird for a ranged character since it triggers close to you regardless
# of what you hit.
# It can be put on a pet or totem so it'll pbaoe whatever they're hitting so it's still pretty decent.
# Still cutting this down to 2 targets.
# further since it doesn't actually hit what you're hitting often the defense reduction as offense
# doesn't follow. I'm going to divide that by 2.
e.addAbility(Ability(
	"Scorpion Sting", 
	{"type":"attack", "trigger":"attack", "chance":.25, "recharge":1.5, "targets":2, "duration":5, "shape":"pbaoe"},
	{"triggered poison":[64,5], "duration":{"offense":140/2/2}, "weapon damage %":30} ))

eye = Constellation("Eye of the Guardian", "1e", "3a 3e")
eye.id = "eye"
a = Star(eye, [], {"acid %":15, "poison %":15})
b = Star(eye, a, {"chaos %":15})
c = Star(eye, b, {"chaos %":15, "poison %":15})
d = Star(eye, c, {"poison %":30})
e = Star(eye, d, {})
# this one is pretty cool.
# when it triggers an eye floats around me in a circle hitting things as it goes. pretty small range
# it circles 5 times before disappearing
e.addAbility(Ability(
	"Guardian's Gaze", 
	{"type":"attack", "trigger":"attack", "chance":.15, "recharge":.5, "shape":"pbaoe", "targets":1.5*5},
	{"weapon damage %":18, "triggered chaos":78, "triggered poison":[78,2]} ))

bat = Constellation("Bat", "1e", "2c 3e")
bat.id = "bat"
a = Star(bat, [], {"vitality %":15, "bleed %":15})
b = Star(bat, a, {"vitality decay":166*.15})
c = Star(bat, b, {"vitality %":24, "bleed %":30})
d = Star(bat, c, {"life leech %":30, "lifesteal %":3})
e = Star(bat, d, {})
# two spikes shoot out from you toward what you triggered on. They're pretty narrowly focused and not particularly well aimed. They don't seem to hit a ton. On the fence on 1.5 - 2 targets.
e.addAbility(Ability(
	"Twin Fangs", 
	{"type":"attack", "trigger":"attack", "chance":.2, "recharge":1, "targets":1.5, "shape":"cone"},
	{"weapon damage %":25, "triggered pierce":116, "triggered vitality":111, "attack as health %":50} ))

spider = Constellation("Spider", "1e", "6e")
spider.id = "spider"
a = Star(spider, [], {"cunning":10, "spirit":10})
b = Star(spider, a, {"offense":10, "chaos resist":8})
c = Star(spider, a, {"offense":15, "defense":10, "damage from insectoids":-12, "damage from arachnids":-12})
d = Star(spider, a, {"cunning %":3, "spirit %":3})
e = Star(spider, a, {"cast speed":3, "attack speed retaliation":20, "move speed retaliation":20})

raven = Constellation("Raven", "1e", "5e")
raven.id = "raven"
a = Star(raven, [], {"spirit":8, "pet all damage %":15})
b = Star(raven, a, {"energy/s":1, "spirit":10})
c = Star(raven, b, {"offense":15, "pet offense %":5})
d = Star(raven, b, {"all damage %":15, "pet lightning damage %":60})

fox = Constellation("Fox", "1e", "5e")
fox.id = "fox"
a = Star(fox, [], {"cunning":10})
b = Star(fox, a, {"bleed":10*3, "bleed %":24})
c = Star(fox, b, {"bleed resist":8, "cunning":15})
d = Star(fox, c, {"bleed":14*3, "bleed %":45})

light = Constellation("Scholar's Light", "1e", "4e")
light.id = "light"
a = Star(light, [], {"fire %":15})
b = Star(light, a, {"elemental resist":8, "physique":10})
c = Star(light, b, {"elemental %":24, "elemental":8, "energy/s":1.5})

hawk = Constellation("Hawk", "1e", "3e")
hawk.id = "hawk"
a = Star(hawk, [], {"offense":15})
b = Star(hawk, a, {"crit damage":8})
c = Star(hawk, b, {"offense %":3, "cunning ranged requirements":-10})

witchblade = Constellation("Solael's Witchblade", "4c 6e", "1c 1e")
witchblade.id = "witchblade"
a = Star(witchblade, [], {"chaos %":40})
b = Star(witchblade, a, {"offense":10, "spirit":15})
c = Star(witchblade, b, {"energy burn %":10, "chaos %":30})
d = Star(witchblade, c, {"fire %":50, "chaos %":50, "fire resist":15})
e = Star(witchblade, d, {})
# says "spreads wildly among your foes"
# Jumps 4m. I'm going to call it 3 targets for now
# rapidly reapplying seems to prevent spreading.
# it doesn't seem to stack
e.addAbility(Ability(
	"Eldritch Fire", 
	{"type":"attack", "trigger":"attack", "chance":.15, "duration":4, "targets":3},
	{"duration":{"triggered fire":102, "triggered chaos":102, "slow move":33, "reduce fire resist":20/3, "reduce chaos resist":20/3}} ))

bonds = Constellation("Bysmiel's Bonds", "4c 6e", "3e")
bonds.id = "bonds"
a = Star(bonds, [], {"offense":15, "pet all damage %":30})
b = Star(bonds, a, {"cast speed":5, "pet total speed":8})
c = Star(bonds, b, {"vitality resist":15, "pet vitality resist":20})
d = Star(bonds, c, {"all damage %":30, "pet all damage %":40, "pet health %":8})
e = Star(bonds, d, {})
#20% on attack
#30 second recharge
#20 second lifespan
#1 lifespan per fight
# 5 main attack and 2 secondary attacks per lifespan
e.addAbility(Ability(
	"Bysmiel's Command", 
	{"type":"summon", "trigger":"attack", "chance":.2, "recharge":30, "lifespan":20},
	{"pet physical":73.5*5, "pet acid":78*5+105*2*2, "pet poison":188*2} ))

magi = Constellation("Magi", "10e", "3e")
magi.id = "magi"
a = Star(magi, [], {"fire %":40, "burn %":50})
b = Star(magi, a, {"elemental resist":8})
c = Star(magi, b, {"fire resist":25})
d = Star(magi, c, {"cast speed":5, "burn %":60})
e = Star(magi, c, {"fire":(6+8)/2, "fire %":40})
f = Star(magi, c, {"burn":12*3, "burn %":30, "burn duration":30})
g = Star(magi, f, {})
# 1 meter radius
# 7 fragments
# trigger creates a volcano that spits out 8 volleys of ~7 fireballs about 2m
# there can be multiples active.
fissure = Ability(
	"Fissure", 
	{"type":"attack", "trigger":"attack", "chance":.15, "recharge":1.5, "duration":5, "targets":3, "shape":"ground"},
	{"triggered fire":116*8, "duration":{"triggered burn":132}, "stun %":15} )
g.addAbility(fissure)

berserker = Constellation("Berserker", "5a 5e", "2c 3e")
berserker.id = "berserker"
berserker.restricts = ["axe"]
a = Star(berserker, [], {"offense":15})
b = Star(berserker, a, {"physical %":50})
c = Star(berserker, b, {"offense":25})
d = Star(berserker, a, {"bleed %":80, "lifesteal %":3})
e = Star(berserker, d, {"bleed %":100*.15, "bleed duration":100*.15, "crit damage":5})
f = Star(berserker, f, {"pierce resist":10, "reduced bleed duration":20})

lantern = Constellation("Oklaine's Lantern", "10e", "3e 2o")
lantern.id = "lantern"
lantern.restricts = ["scepter", "dagger", "offhand"]
a = Star(lantern, [], {"energy regeneration":15})
b = Star(lantern, a, {"offense":25})
c = Star(lantern, b, {"offense":15, "crit damage":5})
d = Star(lantern, c, {"all damage %":50, "reduced entrapment duration":25})
e = Star(lantern, d, {"cast speed":5, "attack speed":5, "energy/s":2})

behemoth = Constellation("Behemoth", "3c 4e 4p", "2c 3e")
behemoth.id = "behemoth"
a = Star(behemoth, [], {"health/s":10})
b = Star(behemoth, a, {"health":300, "pet health %":5})
c = Star(behemoth, b, {"health/s":15, "constitution %":25})
d = Star(behemoth, b, {"health %":4})
e = Star(behemoth, b, {"health regeneration":10, "pet health regeneration":20})
f = Star(behemoth, b, {})
ability = Ability(
	"Giant's Blood", 
	{"type":"heal", "trigger":"hit", "chance":.15, "recharge":30, "duration":10},
	{"health":1000, "health %":20, "duration":{"health/s":240}} )
f.addAbility(ability)

affliction = Constellation("Affliction", "4a 3c 4e", "1a 1e")
affliction.id = "affliction"
a = Star(affliction, [], {"vitality %":40, "poison %":40})
b = Star(affliction, a, {"spirit":15, "vitality decay retaliation":300})
c = Star(affliction, b, {})
# this tends to hit ranged a fair amount which are often much more spread out so it doesn't and/or stay on targets.
# it's unlikely something will stay in this for the full 6 seconds. I'll make it 4 ticks of damage.
pool = Ability(
	"Fetid Pool", 
	{"type":"attack", "trigger":"hit", "chance":.33, "recharge":2, "duration":6, "targets":1, "shape":"ground"},
	{"triggered vitality":128*4, "duration":{"triggered poison":68, "slow move":25}} )
c.addAbility(pool)
d = Star(affliction, c, {"offense":18, "defense":10})
e = Star(affliction, d, {"crit damage":10, "vitality decay retaliation":360})
f = Star(affliction, c, {"vitality":(11+21)/2, "acid resist":10})
g = Star(affliction, f, {"offense %":3, "vitality %":50, "acid %":50})

manticore = Constellation("Manticore", "4c 6e", "1a 1e")
manticore.id = "manticore"
a = Star(manticore, [], {"offense":15})
b = Star(manticore, a, {"acid %":50, "poison %":50})
c = Star(manticore, b, {"health %":4})
d = Star(manticore, c, {"offense":10, "acid resist":25})
e = Star(manticore, c, {"poison":8*5, "acid %":40, "poison %":40})
f = Star(manticore, e, {})
# weird shape. It hits the target and things behind it in a cone. It's pretty strong for any kiter. Shortranged may suffer since the direction will be pretty random in aoe situations.
spray = Ability(
	"Acid Spray", 
	{"type":"attack", "trigger":"attack", "chance":.15, "recharge":1, "duration":5, "targets":3},
	{"triggered acid":148, "triggered poison":[90,2], "duration":{"reduce armor":250/3, "reduce resist":30/3}} )
f.addAbility(spray)

abomination = Constellation("Abomination", "8c 18e")
abomination.id = "abomination"
a = Star(abomination, [], {"chaos %":80, "poison %":80})
b = Star(abomination, a, {"vitality %":80, "acid %":80})
c = Star(abomination, b, {"offense":40, "acid resist":20, "max acid resist":3})
d = Star(abomination, c, {"offense":20, "chaos %":80, "health":150})
e = Star(abomination, d, {})
abominableMight = Ability(
	"Abominable Might",
	{"type":"buff", "trigger":"kill", "chance":1, "recharge":18, "duration":12},
	{"chaos":101, "chaos %":230, "health %":20, "physical to chaos":50} )
e.addAbility(abominableMight)
f = Star(abomination, c, {"offense":20, "poison %":80, "health":150})
g = Star(abomination, f, {"acid %":100, "poison %":100})
h = Star(abomination, g, {})
# 10 meter radius (huge)
taintedEruption = Ability(
	"Tainted Eruption",
	{"type":"attack", "trigger":"attack", "chance":.15, "recharge":3, "targets":5, "shape":"pbaoe"},
	{"triggered poison":[264,5], "stun %":100} )
h.addAbility(taintedEruption)

sage = Constellation("Blind Sage", "10a 18e")
sage.id = "sage"
a = Star(sage, [], {"offense":15, "spirit":25})
b = Star(sage, a, {"offense":15, "elemental %":80})
c = Star(sage, b, {"crit damage":10, "skill disruption protection":30})
d = Star(sage, c, {"cold resist":20, "cold %":100, "frostburn %":100})
e = Star(sage, c, {"lightning %":100, "electrocute %":100, "lightning resist":20})
f = Star(sage, c, {"fire %":100, "burn %":100, "fire resist":20})
g = Star(sage, f, {})
# 5 s lifespan
# call it 3 attacks and a detonate each hitting 2 targets
# 4 attacks per
g.addAbility(Ability(
	"Elemental Seeker",
	{"type":"summon", "trigger":"attack", "chance":1, "recharge":1.5, "lifespan":5},
	{"triggered elemental":60*3*2+132*2, "stun %":100} ))

wolf = Constellation("Mogdrogen the Wolf", "15a 12e")
wolf.id = "wolf"
a = Star(wolf, [], {"offense":35, "pet offense %":5})
b = Star(wolf, a, {"bleed %":80, "pet all damage %":30})
c = Star(wolf, b, {"vitality resist":20, "pet total speed":6})
d = Star(wolf, c, {"bleed":25*5, "bleed %":80})
e = Star(wolf, d, {"bleed resist":15, "elemental resist":15, "max bleed resist":3, "pet all damage %":80})
f = Star(wolf, e, {})
f.addAbility(Ability(
	"Howl of Mogdrogen", 
	{"type":"buff", "trigger":"attack", "chance":.2, "recharge":15, "duration":10},
	{"bleed":44*3, "bleed %":200, "offense":120*.15*3/10, "attack speed":15, "pet offense %":15, "pet total speed":35} ))

rat = Constellation("Rat", "1c", "2c 3e")
rat.id = "rat"
a = Star(rat, [], {"cunning":8, "spirit":8})
b = Star(rat, a, {"poison":8*5, "poison %":24})
c = Star(rat, b, {"acid resist":10, "cunning":15, "spirit":15})
d = Star(rat, c, {"poison":12*5, "poison %":20, "poison duration":30})

ghoul = Constellation("Ghoul", "1c", "3c")
ghoul.id = "ghoul"
a = Star(ghoul, [], {"physique":10})
b = Star(ghoul, a, {"health/s":6, "life leech":15*2})
c = Star(ghoul, b, {"physique":10, "spirit":10})
d = Star(ghoul, b, {"health regeneration":15, "lifesteal %":4})
e = Star(ghoul, d, {})
e.addAbility(Ability(
	"Ghoulish Hunger", 
	{"type":"buff", "trigger":"low health", "chance":1, "recharge":30, "duration":6},
	{"life leach":94*2, "life leach %":135, "lifesteal %":60, "attack speed":20} ))

jackal = Constellation("Jackal", "1c", "3c")
jackal.id = "jackal"
a = Star(jackal, [], {"energy %":6, "pet health %":3})
b = Star(jackal, a, {"offense":12, "attack speed":6})
c = Star(jackal, b, {"all damage %":15, "pet attack speed":5})

fiend = Constellation("Fiend", "1c", "2c 3e")
fiend.id = "fiend"
a = Star(fiend, [], {"fire %":15, "chaos %":15})
b = Star(fiend, a, {"spirit":10, "pet fire damage %":25})
c = Star(fiend, b, {"chaos resist":8})
d = Star(fiend, c, {"fire %":24, "chaos %":24, "pet fire damage %":40})
e = Star(fiend, d, {})
#100% pass through
# 2 projectiles (I can't tell if each hits. I'll count like they do.)
e.addAbility(Ability(
	"Flame Torrent", 
	{"type":"attack", "trigger":"attack", "chance":.25, "recharge":.5, "targets":3, "shape":"pbaoe"},
	{"weapon damage %":35, "triggered fire":132, "triggered chaos":56, "triggered burn":[168/2,3]} ))

viper = Constellation("Viper", "1c", "2c 3p")
viper.id = "viper"
a = Star(viper, [], {"spirit":10})
b = Star(viper, a, {"energy absorb":10, "energy leech":18*2*.15})
c = Star(viper, b, {"vitality resist":10})
d = Star(viper, c, {"offense %":3, "reduce elemental resist":20})

vulture = Constellation("Vulture", "1c", "5c")
vulture.id = "vulture"
a = Star(vulture, [], {"cunning":10})
b = Star(vulture, a, {"bleed resist":15})
c = Star(vulture, b, {"life leech":15*2, "life leech resist":30})
d = Star(vulture, b, {"cunning %":5})
e = Star(vulture, b, {"vitality resist":15, "life leech %":50})

wendigo = Constellation("Wendigo", "4c 6p", "2c")
wendigo.id = "wendigo"
a = Star(wendigo, [], {"vitality %":40, "vitality decay %":40})
b = Star(wendigo, a, {"spirit":15, "health":100})
c = Star(wendigo, b, {"cast speed":5, "vitality resist":10})
d = Star(wendigo, c, {"health %":5, "damage from beasts":-10})
e = Star(wendigo, d, {"vitality %":50, "vitality decay %":50, "life leech %":50})
f = Star(wendigo, e, {})
#giving it 3 targets since it's 0 recharge I can keep a few going.
f.addAbility(Ability(
	"Wendigo's Mark", 
	{"type":"attack", "trigger":"attack", "chance":.25, "recharge":0, "duration":8, "targets":3},
	{"duration":{"triggered vitality":186}, "attack as health %":90} ))

hydra = Constellation("Hydra", "3a 3c 5e", "2c 3e")
hydra.id = "hydra"
hydra.restricts = ["ranged"]
a = Star(hydra, [], {"offense":15})
b = Star(hydra, a, {"all damage %":15})
c = Star(hydra, b, {"pierce %": 40})
d = Star(hydra, b, {"offense":20})
e = Star(hydra, d, {"offense %":3, "slow resist":20})
f = Star(hydra, b, {"all damage %":35})

chariot = Constellation("Chariot of the Dead", "5a 5e", "2c 3e")
chariot.id = "chariot"
a = Star(chariot, [], {"cunning":15})
b = Star(chariot, a, {"offense":15})
c = Star(chariot, b, {"cunning":20})
d = Star(chariot, c, {"vitality resist":10})
e = Star(chariot, c, {"offense":25})
f = Star(chariot, e, {"offense %":3, "offense":10})
g = Star(chariot, f, {})
# it's when hit by a crit so...
g.addAbility(Ability(
	"Wayward Soul", 
	{"type":"heal", "trigger":"hit", "chance":.1, "recharge":18, "duration":7},
	{"health %":10, "health":1300, "duration":{"defense":120}} ))

revenant = Constellation("Revenant", "8c", "1c 1p")
revenant.id = "revenant"
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
f.addAbility(Ability(
	"Raise the Dead", 
	{"type":"summon", "trigger":"kill", "chance":1, "recharge":3, "lifespan":25},
	{"pet physical":53*10, "slow move":.25} ))

torch = Constellation("Ulzuin's Torch", "8c 15e")
torch.id = "torch"
a = Star(torch, [], {"offense":20, "fire %":80})
b = Star(torch, a, {"offense %":5, "chaos resist":15})
c = Star(torch, b, {"move %":5, "crit damage":10})
d = Star(torch, c, {"fire %":100, "fire resist":20})
e = Star(torch, d, {"burn":25*3, "burn %":100, "max fire resist":3})
f = Star(torch, c, {"burn %":100, "burn duration":100})
g = Star(torch, f, {})
#6m area
#2m radius
#15 meteors
# large area, call it 6 targets in the area
# each missile hits a smallish area, let's say each target gets hit 3 times
# let's say the burn overlaps twice.
g.addAbility(Ability(
	"Meteor Shower", 
	{"type":"attack", "trigger":"attack", "chance":.3, "recharge":3.5, "duration":3, "targets":6, "shape":"ground"},
	{"triggered fire":90*3, "triggered physical":90*3, "triggered burn":[82*2,2]} ))

torchOffense = Constellation("Ulzuin's Torch (offense %)", "8c 15e")
torchOffense.id = "torchOffense"
a = Star(torchOffense, [], {"offense":20, "fire %":80})
b = Star(torchOffense, a, {"offense %":5, "chaos resist":15})

torch.addConflicts([torchOffense])

god = Constellation("Dying God", "8c 15p")
god.id = "god"
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
g.addAbility(Ability(
	"Hungering Void", 
	{"type":"buff", "trigger":"attack", "chance":1, "recharge":30, "duration":20},
	{"health/s":-275, "crit damage":30, "vitality %":215, "chaos %":215, "total speed":8, "chaos retaliation":485, "terrify retaliation":55, "pet all damage %":150, "pet crit damage":20, "stun %":10, "slow move":30*.45} ))

imp = Constellation("Imp", "1p", "3e 3p")
imp.id = "imp"
a = Star(imp, [], {"fire %":15, "aether %":15})
b = Star(imp, a, {"spirit":10})
c = Star(imp, b, {"aether resist":8})
d = Star(imp, c, {"fire %":24, "aether %":24})
e = Star(imp, d, {})
#aoe is on target
#it ticks per second for duration
#it stacks on itself
e.addAbility(Ability(
	"Aetherfire", 
	{"type":"attack", "trigger":"attack", "chance":.15, "duration":3, "targets":1.5, "duration":3, "shape":"ground"},
	{"triggered fire":50*3, "triggered aether":125*3, "stun %":33} ))

tsunami = Constellation("Tsunami", "1p", "5p")
tsunami.id = "tsunami"
a = Star(tsunami, [], {"lightning %": 15, "cold %":15})
b = Star(tsunami, a, {"spirit":10})
c = Star(tsunami, b, {"electrocute %":40, "frostburn %":40})
d = Star(tsunami, c, {"lightning %":24, "cold %":24})
e = Star(tsunami, d, {})
#35% on attack
#1.5s recharge
#12m range
# pretty wide line attack from me toward target with 100% pass through
e.addAbility(Ability(
	"Tsunami", 
	{"type":"attack", "trigger":"attack", "chance":.35, "recharge":1.5, "targets":2.5, "shape":"line"},
	{"weapon damage %":32, "triggered cold":115, "triggered lightning":51} ))

gallows = Constellation("Gallows", "1p", "5p")
gallows.id = "gallows"
a = Star(gallows, [], {"vitality %":15})
b = Star(gallows, a, {"life leech retaliation":100*.15})
c = Star(gallows, b, {"vitality resist":10})
d = Star(gallows, c, {"vitality":7, "vitality %":24, "chaos %":24})

lizard = Constellation("Lizard", "1p", "4p")
lizard.id = "lizard"
a = Star(lizard, [], {"health/s":6, "constitution %":15})
b = Star(lizard, a, {"health/s":10, "health":50})
c = Star(lizard, b, {"constitution %":15, "health regeneration":15})

guide = Constellation("Sailor's Guide", "1p", "5p")
guide.id = "guide"
a = Star(guide, [], {"physique":10})
b = Star(guide, a, {"reduced freeze":15, "slow resist":15})
c = Star(guide, b, {"move %":5, "physique":10})
d = Star(guide, b, {"cold resist":15, "lightning resist":15})

bull = Constellation("Bull", "1p", "2o 3p")
bull.id = "bull"
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
e.addAbility(Ability(
	"Bull Rush", 
	{"type":"attack", "trigger":"attack", "chance":.25, "recharge":.5, "targets":2, "shape":"pbaoe"},
	{"weapon damage %":45, "triggered physical":114, "triggered internal":[125,2]} ))

wraith = Constellation("Wraith", "1p", "3a 3p")
wraith.id = "wraith"
a = Star(wraith, [], {"aether %":15, "lightning %":15})
b = Star(wraith, a, {"spirit":10, "aether resist":8})
c = Star(wraith, a, {"energy absorb":15, "offense":10})
d = Star(wraith, a, {"aether":4, "aether %":24, "lightning":(1+7)/2, "lightning %":24})

eel = Constellation("Eel", "1p", "5p")
eel.id = "eel"
a = Star(eel, [], {"defense":10, "avoid melee":2})
b = Star(eel, a, {"defense":10, "avoid ranged":2})
c = Star(eel, b, {"pierce resist":10, "defense":10})

hound = Constellation("Hound", "1p", "4p")
hound.id = "hound"
a = Star(hound, [], {"physique":10, "pet health %":4})
b = Star(hound, a, {"armor %":2, "pierce retaliation":30, "retaliation %":20})
c = Star(hound, b, {"armor %":2, "physique":15, "retaliation %":30, "pet retaliation %":30})

messenger = Constellation("Messenger of War", "3a 7p", "2c 3p")
messenger.id = "messenger"
a = Star(messenger, [], {"pierce retaliation":90, "retaliation %":30})
b = Star(messenger, a, {"move %":5, "physique":10})
c = Star(messenger, b, {"armor":50, "retaliation %":50})
d = Star(messenger, c, {"armor %":6, "pierce retaliation":120})
e = Star(messenger, b, {"pierce resist":15, "damage reflect %":25})
f = Star(messenger, e, {})
# 20% when hit
# 15s recharge
# 8s duration
war = Ability(
	"Messenger of War", 
	{"type":"buff", "trigger":"hit", "chance":.2, "recharge":15, "duration":8},
	{"move %":30, "slow resist":70, "pierce retaliation":800, "retaliation %":200} )
f.addAbility(war)

tempest = Constellation("Tempest", "5a 5p", "1e 1p")
tempest.id = "tempest"
a = Star(tempest, [], {"lightning %":40})
b = Star(tempest, a, {"lightning":(1-24)/2})
c = Star(tempest, b, {"lightning %":50, "electrocute %":50})
d = Star(tempest, c, {"offense":10, "lightning resist":25})
e = Star(tempest, d, {"move %":3, "lightning %":200*.3})
f = Star(tempest, d, {"offense":15, "electrocute %":50, "electrocute duration":30})
g = Star(tempest, f, {})
# 3 target max
# 8 meter radius
# .5s interval
# 12 bolts / electrocute will tick 8 times
g.addAbility(Ability(
	"Reckless Tempest", 
	{"type":"attack", "trigger":"critical", "chance":1, "recharge":10, "duration":6, "targets":3},
	{"triggered lightning":113.5*12, "triggered electrocute":[128,2*8], "stun %":20} ))

widow = Constellation("Widow", "6e 4p", "3p")
widow.id = "widow"
a = Star(widow, [], {"aether %":40})
b = Star(widow, a, {"offense":18, "energy %":5})
c = Star(widow, b, {"aether %":30, "spirit":10})
d = Star(widow, c, {"vitality resist":8, "aether resist":18})
e = Star(widow, d, {"aether %":50, "lightning %":50})
f = Star(widow, e, {})
# reduced offense is a bit tricky. It's like defense if all enemies hitting you are affected.
# lets say in the average fight 6 are trying to attack you and you hit x targets.
# so divide the defense stat by 6 and the targets will take care of the numerator.
f.addAbility(Ability(
	"Arcane Bomb", 
	{"type":"attack", "trigger":"attack", "chance":.25, "recharge":2, "targets":2, "shape":"ground"},
	{"triggered lightning":88, "triggered aether":88, "defense":80/6, "reduce lightning resist":33/2, "reduce aether resist":33/2} ))

kraken = Constellation("Kraken", "5e 5p", "2c 3p")
kraken.id = "kraken"
kraken.restricts = ["twohand"]
a = Star(kraken, [], {"all damage %":35})
b = Star(kraken, a, {"physical %":40, "attack speed":10})
c = Star(kraken, a, {"physical %":40, "attack speed":10})
d = Star(kraken, a, {"all damage %":50, "move %":5})
e = Star(kraken, a, {"all damage %":35, "crit damage":15})

winter = Constellation("Amatok the Spirit of Winter", "4e 6p", "1e 1p")
winter.id = "winter"
a = Star(winter, [], {"cold %":40})
b = Star(winter, a, {"health %":3, "defense":15})
c = Star(winter, b, {"cold resist":25, "offense":10})
d = Star(winter, b, {"cold %":50, "frostburn %":50})
e = Star(winter, d, {"frostburn":12*3, "frostburn %":70})
f = Star(winter, b, {"offense":15, "frostburn %":30, "frostburn duration":30})
g = Star(winter, f, {})
#1.5m radius
#looks like there are multiple missiles but it's not listed
blizzard = Ability(
	"Blizzard", 
	{"type":"attack", "trigger":"critical", "chance":1, "recharge":3.5, "targets":4, "shape":"ground"},
	{"weapon damage %":10, "triggered cold":165.5, "triggered frostburn":[93,2], "stun %":40, "slow move":60} )
g.addAbility(blizzard)

bear = Constellation("Dire Bear", "5a 5p", "1a 1p")
bear.id = "bear"
a = Star(bear, [], {"physical %":40})
b = Star(bear, a, {"physique":10, "cunning":10})
c = Star(bear, b, {"constitution %":15, "attack speed":5})
d = Star(bear, c, {"reduced stun duration":15, "reduced freeze duration":15, "health %":5})
e = Star(bear, [], {"physical %":50, "internal %":50})
f = Star(bear, d, {})
#4m radius
f.addAbility(Ability(
	"Maul", 
	{"type":"attack", "trigger":"attack", "chance":.15, "recharge":1, "targets":3, "shape":"pbaoe"},
	{"weapon damage %":75, "triggered physical":161.5, "stun %":100} ))

ulo = Constellation("Ulo the Keeper of the Waters", "4o 6p", "2o 3p")
ulo.id = "ulo"
a = Star(ulo, [], {"elemental resist":10, "pet elemental resist":10})
b = Star(ulo, a, {"life leech resist":30, "energy leech resist":30})
c = Star(ulo, b, {"acid resist":15, "pet acid resist":15})
d = Star(ulo, b, {"chaos resist":10, "pet chaos resist":10})
e = Star(ulo, b, {})
#3m radius
e.addAbility(Ability(
	"Cleansing Waters", 
	{"type":"attack", "trigger":"attack", "chance":1, "recharge":22, "targets":2, "duration":8},
	{"slow move":40} ))

watcher = Constellation("Solemn Watcher", "10p", "2o 3p")
watcher.id = "watcher"
a = Star(watcher, [], {"physique":15})
b = Star(watcher, a, {"cold resist":25})
c = Star(watcher, b, {"pierce resist":18})
d = Star(watcher, c, {"defense":30, "physique %":3})
e = Star(watcher, d, {"defense %":5, "reflected damage reduction":20})

hourglass = Constellation("Aeon's Hourglass", "8c 18p")
hourglass.id = "hourglass"
a = Star(hourglass, [], {"physique":30, "cunning":30, "spirit":30})
b = Star(hourglass, a, {"defense":25, "reduced burn duration":20, "reduced frostburn duration":20, "reduced electrocute duration":20})
c = Star(hourglass, b, {"slow resist":50, "aether resist":20})
d = Star(hourglass, c, {"defense":35, "vitality resist":15, "max vitality resist":4})
e = Star(hourglass, d, {"avoid melee":6, "avoid ranged":6, "reduced entrapment duration":30, "reflected damage reduction":25})
f = Star(hourglass, e, {})
#3m radius
f.addAbility(Ability(
	"Time Stop", 
	{"type":"attack", "trigger":"hit", "chance":.3, "recharge":3, "targets":1.5, "duration":3, "shape":"circle"},
	{"stun %":100, "duration":{"slow move":70}} ))

spear = Constellation("Spear of the Heavens", "7c 20p")
spear.id = "spear"
a = Star(spear, [], {"offense":20, "lightning %":80})
b = Star(spear, a, {"offense":20, "aether %":80})
c = Star(spear, b, {"offense %":5, "aether resist":15})
d = Star(spear, c, {"crit damage":10, "lightning resist":20})
e = Star(spear, d, {"aether %":100, "lightning %":100, "max lightning resist":3})
f = Star(spear, e, {})
#.5m radius
f.addAbility(Ability(
	"Spear of the Heavens", 
	{"type":"attack", "trigger":"hit", "chance":.5, "recharge":1, "targets":1.5, "shape":"circle"},
	{"triggered lightning":162, "triggered aether":176, "stun %":100} ))

tree = Constellation("Tree of Life", "7o 20p")
tree.id = "tree"
a = Star(tree, [], {"health %":5, "pet health %":5})
b = Star(tree, a, {"health/s":20, "pet health regeneration":20})
c = Star(tree, b, {"health %":8, "pet health %":5})
d = Star(tree, b, {"health/s":15, "defense":30, "pet health regeneration":20})
e = Star(tree, d, {"health %":4, "health regeneration":20, "pet health/s":50})
f = Star(tree, d, {})
#25% when hit
#12s recharge
f.addAbility(Ability(
	"Healing Rain", 
	{"type":"heal", "trigger":"hit", "chance":.25, "recharge":12, "duration":8},
	{"duration":{"health/s":100, "energy/s":10, "health regeneration":50, "energy regeneration":50}, "health %":10, "health":550} ))

empyrion = Constellation("Light of Empyrion", "8o 18p")
empyrion.id = "empyrion"
a = Star(empyrion, [], {"elemental resist":10, "pet elemental resist":10}) #not quite right but close enough
b = Star(empyrion, a, {"fire %":80, "damage chthonics %":10})
c = Star(empyrion, b, {"elemental resist":15, "pet elemental resist":15})
d = Star(empyrion, c, {"vitality resist":15, "pet vitality resist":15})
e = Star(empyrion, d, {"aether resist":15, "chaos resist":15, "pet aether resist":15, "pet chaos resist":15})
f = Star(empyrion, e, {"fire":(8+14)/2, "max aether resist":3, "max chaos resist":3, "pet max all resist":5})
g = Star(empyrion, f, {})
#20% when attacked
#4s recharge
#5m radius
g.addAbility(Ability(
	"Light of Empyrion", 
	{"type":"attack", "trigger":"hit", "chance":.2, "recharge":4, "targets":3, "duration":10, "shape":"pbaoe"},
	{"weapon damage %":35, "triggered fire":226, "triggered burn":[102,2], "stun %":50, "duration":{"reduce armor":225}, "damage to undead":50, "damage to cthonics":50} ))


def getRequires(star):
	if not star.requires:
		return []
	return [star.requires] + getRequires(star.requires)

abilityFragments = []

origConstellations = Constellation.constellations[:]
for c in origConstellations:
	# print c
	newFragments = []
	for ability in c.abilities:
		required = [ability] + getRequires(ability)
		if len(required) < len(c.stars):
			subC = Constellation(c.name+" ("+ability.name+")", c.requires)
			subC.id = c.id + ability.name.replace(" ", "").replace("'", "")
			subC.stars = required
			subC.abilities = [ability]
			subC.restricts = c.restricts

			# print "  ", subC
			abilityFragments += [subC]
			newFragments += [subC]
	c.addConflicts(newFragments)

for c in abilityFragments:
	globals()[c.id] = c

