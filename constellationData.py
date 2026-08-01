from dataModel import *

# these can be temporariliy removed to try starting with 1 of each affinity provided to reduce the search space

xA = Constellation("Crossroads Ascendant", "", "1a")
xA.id = "xA"
Star(xA, [], {"offense":18})
xC = Constellation("Crossroads Chaos", "", "1c")
xC.id = "xC"
Star(xC, [], {"health %":5})
xE = Constellation("Crossroads Eldrich", "", "1e")
xE.id = "xE"
Star(xE, [], {"offense":18})
xO = Constellation("Crossroads Order", "", "1o")
xO.id = "xO"
Star(xO, [], {"health %":5})
xP = Constellation("Crossroads Primordial", "", "1p")
xP.id = "xP"
Star(xP, [], {"defense":18})

anvil = Constellation("Anvil", "1a", "5a")
anvil.id = "anvil"
anvil.restricts = ["shield"]
a = Star(anvil, [], {"defense":15})
b = Star(anvil, a, {"physique":20})
c = Star(anvil, b, {"armor":45, "armor absorb":3})
d = Star(anvil, c, {"internal":[60, 5], "offense":10, "defense":15, "constitution %":20})
e = Star(anvil, d, {})
# like the eye. summons a hammer that floats around me smackin shit it hits.
e.addAbility(Ability("Targo's Hammer", 
	{"type":"attack", "trigger":"block", "chance":.5, "recharge":.1, "targets":2, "shape":"pbaoe", "duration":5},
	{"stun %":50, "weapon damage %":45, "triggered physical":203, "duration":{"internal %":370, "retaliation to attack":17}} ))

throne = Constellation("Empty Throne", "1a", "5a")
throne.id = "throne"
a = Star(throne, [], {"defense":12, "slow resist":10})
b = Star(throne, a, {"defense":20, "pierce resist":8, "pet pierce resist":15})
c = Star(throne, b, {"chaos resist":10, "pet chaos resist":15, "stun resist":25, "pet stun resist":25})
d = Star(throne, b, {"aether resist":10, "freeze resist":25, "pet aether resist":15, "pet freeze resist":25})

falcon = Constellation("Falcon", "1a", "3a 3e")
falcon.id = "falcon"
a = Star(falcon, [], {"physical %":15, "bleed %":15})
b = Star(falcon, a, { "health":60, "offense":15})
c = Star(falcon, b, {"cunning":20})
d = Star(falcon, c, {"physical %":24, "bleed %":24})
e = Star(falcon, d, {})
# 6 projectiles
# 150 deg cone 
# multi hit doesnt stack
e.addAbility(Ability(
	"Falcon Swoop", 
	{"type":"attack", "trigger":"attack", "chance":.15, "recharge":2, "targets":3, "shape":"cone"}, 
	{"weapon damage %":24, "triggered physical":116, "triggered bleed":[225,3]} ))

hammer = Constellation("Hammer", "1a", "4a")
hammer.id = "hammer"
a = Star(hammer, [], {"physical %":15, "armor":20})
b = Star(hammer, a, {"defense":15, "internal %":50})
c = Star(hammer, b, {"physical %":24, "internal %":30, "armor %":8})

harpy = Constellation("Harpy", "1a", "5a")
harpy.id = "harpy"
a = Star(harpy, [], {"pierce %":15, "cold %":15})
b = Star(harpy, a, {"cunning":15, "energy/s":1})
c = Star(harpy, b, {"bleed resist":10, "offense":24})
d = Star(harpy, b, {"pierce":(4+8)/2, "pierce %":24, "cold %":24, "crit damage":3})

nighttalon = Constellation("Nighttalon", "3a, 2c")
nighttalon.id = "nighttalon"
a = Star(nighttalon, [], {"cunning":15, "pet all damage %":15})
b = Star(nighttalon, a, {"elemental resist":10, "pet elemental resist":10})
c = Star(nighttalon, b, {"bleed %":20, "pet bleed":[12,3], "pet damage %":25})
d = Star(nighttalon, c, {"bleed %":50, "pet bleed":[24,3], "pet bleed %":60, "pet attack speed":5})

owl = Constellation("Owl", "1a", "5a")
owl.id = "owl"
a = Star(owl, [], {"spirit":15, "cunnint":15})
b = Star(owl, a, {"elemental resist":8, "skill cost %":-5})
c = Star(owl, b, {"internal %":50, "bleed %":50, "burn %":50, "electrocute %":50, "frostburn %":50, "poison %":50, "vitality decay %":50})
d = Star(owl, b, {"all damage %":30, "reflected damage reduction":15, "defense":15})

shepherd = Constellation("Shepherd's Crook", "1a", "5a")
shepherd.id = "shepherd"
a = Star(shepherd, [], {"health":40, "pet health %":8})
b = Star(shepherd, a, {"cunning":15, "health":40})
c = Star(shepherd, b, {"elemental resist":10, "pet elemental resist":15})
d = Star(shepherd, c, {"health %":3, "pet health %":8, "pet defense %":5})
e = Star(shepherd, d, {})
e.addAbility(Ability(
	"Shepherd's Call", 
	{"type":"buff", "trigger":"attack", "chance":.25, "duration":4, "recharge":6},
	{"offense":85, "pet all damage %":250, "pet crit damage":28, "pet retaliation %":300} ))

toad = Constellation("Toad", "1a", "3a 3e")
toad.id = "toad"
a = Star(toad, [], {"vitality resist":8})
b = Star(toad, a, {"spirit":15, "offense":10, "pet all damage %":25, "pet offence %":3})
c = Star(toad, b, {"lifesteal %":3, "health":60, "pet all damage %":25, "pet lifesteal %":4})
d = Star(toad, c, {"vitality %":24, "aether %":24, "damage beast %":6, "pet offense %":3})

wolverine = Constellation("Wolverine", "1a", "6a")
wolverine.id = "wolverine"
a = Star(wolverine, [], {"defense":15, "pet pierce resist":10})
b = Star(wolverine, a, {"armor":30, "retaliation %":30, "pet vitality resist":15})
c = Star(wolverine, b, {"defense":25, "pet acid resist":15, "pet poison resist":15})
d = Star(wolverine, c, {"retaliation %":50, "armor":30, "pet bleed resist":25})
e = Star(wolverine, c, {"defense %":4, "melee weapon physique requirements":-10, "melee weapon cunning requirements":-10, "pet defense %":5})

fiend = Constellation("Fiend", "1c", "2c 3e")
fiend.id = "fiend"
a = Star(fiend, [], {"fire %":15, "chaos %":15})
b = Star(fiend, a, {"spirit":15, "pet all damage %":30})
c = Star(fiend, b, {"chaos resist":8})
d = Star(fiend, c, {"fire %":24, "chaos %":24, "pet fire damage %":80})
e = Star(fiend, d, {})
#100% pass through
# 2 projectiles (I can't tell if each hits. I'll count like they do.)
e.addAbility(Ability(
	"Flame Torrent", 
	{"type":"attack", "trigger":"attack", "chance":.25, "recharge":.5, "targets":3, "shape":"pbaoe"},
	{"weapon damage %":20, "triggered fire":178, "triggered chaos":126, "triggered burn":[190,3]} ))

ghoul = Constellation("Ghoul", "1c", "3c")
ghoul.id = "ghoul"
a = Star(ghoul, [], {"physique":15, "defense":8})
b = Star(ghoul, a, {"health/s":16, "health %":3})
c = Star(ghoul, b, {"physique":15, "spirit":15, "defense":15})
d = Star(ghoul, b, {"health/s %":30, "lifesteal %":5})
e = Star(ghoul, d, {})
e.addAbility(Ability(
	"Ghoulish Hunger", 
	{"type":"buff", "trigger":"low health", "chance":1, "recharge":30, "duration":5},
	{"lifesteal %":80, "attack speed":22, "cast speed":22, "healing %":40, "physical resist":18} ))

jackal = Constellation("Jackal", "1c", "3c")
jackal.id = "jackal"
a = Star(jackal, [], {"energy %":6, "pet health %":8})
b = Star(jackal, a, {"offense":12, "total speed":6})
c = Star(jackal, b, {"all damage %":15, "physical resist":2, "pet attack speed":5})

mantis = Constellation("mantis", "1c", "3a 2c")
mantis.id = "mantis"
a = Star(mantis, [], {"pierce %":15, "armor":20})
b = Star(mantis, a, {"defense":10, "elemental resist":10})
c = Star(mantis, b, {"health":80, "energy/s":1})
d = Star(mantis, c, {"pierce":5, "pierce %":24, "physical resist":3})

rat = Constellation("Rat", "1c", "2c 3e")
rat.id = "rat"
a = Star(rat, [], {"cunning":15, "spirit":15})
b = Star(rat, a, {"poison":[40,5], "poison %":24, "acid retaliation":20})
c = Star(rat, b, {"acid resist":10, "poison resist":10, "cunning":20, "spirit":20, "acid retaliation":30})
d = Star(rat, c, {"poison":[60,5], "poison %":50, "poison duration":30, "all retaliation %":40})

viper = Constellation("Viper", "1c", "2c 3p")
viper.id = "viper"
a = Star(viper, [], {"spirit":15, "cunning":15})
b = Star(viper, a, {"energy absorb":10, "energy leech":18*2*.15})
c = Star(viper, b, {"vitality resist":10})
d = Star(viper, c, {"offense %":3, "reduce elemental resist":20})

vulture = Constellation("Vulture", "1c", "5c")
vulture.id = "vulture"
a = Star(vulture, [], {"cunning":15, "spirit":15})
b = Star(vulture, a, {"offense":15, "life leach resist":30, "bleed resist":15})
c = Star(vulture, b, {"health":80, "energy":200, "offense":15})
d = Star(vulture, b, {"cunning %":5, "spirit %":5, "offense":15})
e = Star(vulture, b, {"offense":15, "vitality resist":15, "chaos resist":8})

wretch = Constellation("Wretch", "1c", "2c 3p")
wretch.id = "wretch"
a = Star(wretch, [], {"acid %":15, "chaos %":15})
b = Star(wretch, a, {"physique":15, "bleed resist":12})
c = Star(wretch, b, {"health":140, "defense":15, "acid retaliation":44})
d = Star(wretch, c, {"acid %":24, "chaos %":24, "acid %":24, "damage undead %":6})

scorpion = Constellation("Scorpion", "1e", "5e")
scorpion.id = "scorpion"
a = Star(scorpion, [], {"offense":12})
b = Star(scorpion, a, {"acid %":15, "poison %":24, "physique":15})
c = Star(scorpion, b, {"acid %":24, "offense":18})
d = Star(scorpion, c, {"poison %":30, "poison duration":30})
e = Star(scorpion, c, {})
# it's a pbaoe with a decent range. It's weird for a ranged character since it triggers close to you regardless
# of what you hit.
# It can be put on a pet or totem so it'll pbaoe whatever they're hitting so it's still pretty decent.
# Still cutting this down to 2 targets.
e.addAbility(Ability(
	"Scorpion Sting", 
	{"type":"attack", "trigger":"attack", "chance":.25, "recharge":1.5, "targets":2, "duration":5, "shape":"pbaoe"},
	{"triggered poison":[225,5], "duration":{"reduce defense":150}, "weapon damage %":40} ))

bat = Constellation("Bat", "1e", "2c 3e")
bat.id = "bat"
a = Star(bat, [], {"vitality %":15, "bleed %":15})
b = Star(bat, a, {"vitality decay %":30, "offense":15})
c = Star(bat, b, {"vitality %":24, "bleed %":30})
d = Star(bat, c, {"vitality":6, "lifesteal %":3, "defense":10})
e = Star(bat, d, {})
# two spikes shoot out from you toward what you triggered on. They're pretty narrowly focused and not particularly well aimed. They don't seem to hit a ton. On the fence on 1.5 - 2 targets.
e.addAbility(Ability(
	"Twin Fangs", 
	{"type":"attack", "trigger":"attack", "chance":.2, "recharge":.6, "targets":1.5, "shape":"cone"},
	{"weapon damage %":22, "triggered pierce":165, "triggered vitality":(128+221)/2, "lifesteal %":40} ))

eye = Constellation("Eye of the Guardian", "1e", "3a 3e")
eye.id = "eye"
a = Star(eye, [], {"acid %":15, "poison %":15})
b = Star(eye, a, {"offense":16, "defense":16})
c = Star(eye, b, {"chaos %":20, "poison %":15})
d = Star(eye, c, {"poison %":30, "vitality resist":8})
e = Star(eye, d, {})
# this one is pretty cool.
# when it triggers an eye floats around me in a circle hitting things as it goes. pretty small range
# it circles 5 times before disappearing
e.addAbility(Ability(
	"Guardian's Gaze", 
	{"type":"attack", "trigger":"attack", "chance":.15, "recharge":.5, "shape":"pbaoe", "targets":1.5*5},
	{"weapon damage %":15, "triggered acid":83, "lifesteal %":15, "triggered poison":[190,2]} ))

fox = Constellation("Fox", "1e", "5e")
fox.id = "fox"
a = Star(fox, [], {"cunning":15, "spirit":15})
b = Star(fox, a, {"bleed":[24,3], "bleed %":24})
c = Star(fox, b, {"bleed resist":8, "cunning":25})
d = Star(fox, c, {"lifesteal %":6, "bleed":[36,3], "bleed %":50, "health/s":10})

hawk = Constellation("Hawk", "1e", "3e")
hawk.id = "hawk"
a = Star(hawk, [], {"offense":15})
b = Star(hawk, a, {"crit damage":8, "pet crit damage":8})
c = Star(hawk, b, {"offense %":3, "cunning ranged requirements":-10, "pet offense %":3})

quill = Constellation("Quill", "1e", "3a 3e")
quill.id = "quill"
a = Star(quill, [], {"elemental %":15})
b = Star(quill, a, {"aether resist":8})
c = Star(quill, b, {"health":100, "energy":150})
d = Star(quill, c, {"elemental %":24, "energy %":5, "defense %":2})

raven = Constellation("Raven", "1e", "5e")
raven.id = "raven"
a = Star(raven, [], {"spirit":15, "pet all damage %":15})
b = Star(raven, a, {"offense":10, "energy/s":1})
c = Star(raven, b, {"offense":15, "pet lightning %":80})
d = Star(raven, b, {"all damage %":20, "pet lightning":6, "pet lightning damage %":60})

light = Constellation("Scholar's Light", "1e", "4e")
light.id = "light"
a = Star(light, [], {"elemental %":15})
b = Star(light, a, {"elemental resist":8, "physique":15, "defense":15})
c = Star(light, b, {"elemental %":24, "aether %":8, "energy/s":2.5})

spider = Constellation("Spider", "1e", "6e")
spider.id = "spider"
a = Star(spider, [], {"cunning":15, "spirit":15})
b = Star(spider, a, {"spirit %":3, "offense":20})
c = Star(spider, a, {"offense":20, "cast speed":5})
d = Star(spider, a, {"defense":20, "attack speed":5})
e = Star(spider, a, {"cunning %":3, "defense":20})

blade = Constellation("Assassin's Blade", "1o", "3a 2o")
blade.id = "blade"
a = Star(blade, [], {"defense":12})
b = Star(blade, a, {"physical %":15, "pierce %":15})
c = Star(blade, b, {"physical %":15, "pierce %":15})
d = Star(blade, c, {"offense":18})
e = Star(blade, d, {})
e.addAbility(Ability(
	"Assassin's Mark", 
	{"type":"buff", "trigger":"critical", "chance":1, "recharge":0, "duration":18},
	{"reduce physical resist":32, "reduce pierce resist":32} ))

crane = Constellation("Crane", "1o", "5o")
crane.id = "crane"
a = Star(crane, [], {"physique":15, "spirit":15})
b = Star(crane, a, {"acid resist":12, "poison resist":12, "pet acid resist":20, "pet poison resist":20})
c = Star(crane, b, {"all damage %":15, "weapon spirit requirements":-10})
d = Star(crane, c, {"vitality resist":12, "pet vitality resist":20})
e = Star(crane, d, {"elemental resist":16, "bleed resist":16, "reflected damage reduction":22})

dryad = Constellation("Dryad", "1o", "3o")
dryad.id = "dryad"
a = Star(dryad, [], {"physique":15, "acid resist":10, "poison resist":10, "energy":200})
b = Star(dryad, a, {"energy/s":1, "health":80})
c = Star(dryad, b, {"move speed":3, "slow resist":15})
d = Star(dryad, c, {"spirit %":5, "weapon spirit requirements":-10, "jewelry spirit requirements":-10, "physical resist":3})
e = Star(dryad, d, {})
e.addAbility(Ability(
	"Dryad's Blessing", 
	{"type":"heal", "trigger":"attack", "chance":.33, "recharge":2.7, "duration":10},
	{"health %":10, "health":848, "armor":70, "reduced poison duration":36, "reduced bleed duration":36} ))

lion = Constellation("Lion", "1o", "3o")
lion.id = "lion"
a = Star(lion, [], {"health %":4, "defense":8, "pet health %":8})
b = Star(lion, a, {"spirit":15, "armor":30, "move speed":6})
c = Star(lion, b, {"all damage %":15, "physical resist":2, "pet all damage %":20})

lotus = Constellation("Lotus", "1o", "3a 2o")
lotus.id = "lotus"
a = Star(lotus, [], {"health":30, "energy":100})
b = Star(lotus, a, {"energy/s":1, "energy/s %":15})
c = Star(lotus, a, {"health":80, "energy %":4, "vitality resist":8})
d = Star(lotus, a, {"healing %":10, "physical resist":3})

panther = Constellation("Panther", "1o", "2o 3p")
panther.id = "panther"
a = Star(panther, [], {"offense":25, "crit damage":6, "pet all damage %":30, "pet crit damage":8})
b = Star(panther, a, {"offense":20, "energy/s %":15, "pet offense %":3})
c = Star(panther, b, {"cunning":15, "spirit":15, "pet all damage %":20})
d = Star(panther, c, {"offense":12, "offense %":2})

stag = Constellation("Stag", "1o", "2o 3p")
stag.id = "stag"
a = Star(stag, [], {"physical %":15, "bleed %":15, "pet all damage %":20})
b = Star(stag, a, {"physique":15, "pierce resist":10, "move speed":5})
c = Star(stag, b, {"health":110, "defense":15, "retaliation %":30, "pet physical %":30, "pet defense %":3})
d = Star(stag, c, {"physical %":24, "bleed %":24, "physical resist":3, "pet physical %":50})

tortoise = Constellation("Tortoise", "1o", "2o 3p")
tortoise.id = "tortoise"
a = Star(tortoise, [], {"defense":12, "armor":20})
b = Star(tortoise, a, {"defense":15, "shield physique requirements":-10, "armor":20})
c = Star(tortoise, b, {"defense":15, "armor":40})
d = Star(tortoise, c, {"health %":4, "defense":10, "armor %":8})
e = Star(tortoise, c, {})
e.addAbility(Ability(
	"Turtle Shell", 
	{"type":"shield", "trigger":"low health", "chance":1, "recharge":8},
	{"damage absorb":6100}))

bull = Constellation("Bull", "1p", "2o 3p")
bull.id = "bull"
a = Star(bull, [], {"physique":15})
b = Star(bull, a, {"internal %":24, "internal duration":20, "move speed":3})
c = Star(bull, b, {"physique":15, "armor":30})
d = Star(bull, c, {"internal":[60,5], "internal %":30, "armor physique requirements":-10})
e = Star(bull, d, {})
#25% on attack
#.5s recharge
#3.5 meter radius
# 2 targets
# 4 attacks trigger, 1 attack recharge
e.addAbility(Ability(
	"Bull Rush", 
	{"type":"attack", "trigger":"attack", "chance":.25, "recharge":.4, "targets":2, "shape":"pbaoe"},
	{"weapon damage %":32, "triggered physical":(115+230)/2, "triggered internal":[225,2]} ))

eel = Constellation("Eel", "1p", "5p")
eel.id = "eel"
a = Star(eel, [], {"defense":12, "avoid melee":2})
b = Star(eel, a, {"defense":15, "avoid ranged":2})
c = Star(eel, b, {"pierce resist":10, "defense":20, "move speed":6})

gallows = Constellation("Gallows", "1p", "5p")
gallows.id = "gallows"
a = Star(gallows, [], {"vitality %":15, "chaos %":15})
b = Star(gallows, a, {"health %":3, "bleed resist":10})
c = Star(gallows, b, {"health %":3, "vitality resist":10})
d = Star(gallows, c, {"vitality":8, "vitality %":24, "chaos %":24, "damage undead %":6, "damage human %":6})

hound = Constellation("Hound", "1p", "4p")
hound.id = "hound"
a = Star(hound, [], {"physique":15, "pet health %":8})
b = Star(hound, a, {"armor %":6, "retaliation %":30})
c = Star(hound, b, {"armor %":9, "physique":20, "retaliation %":40, "pet health %":12, "stun resist":15})

imp = Constellation("Imp", "1p", "3e 3p")
imp.id = "imp"
a = Star(imp, [], {"fire %":15, "aether %":15})
b = Star(imp, a, {"spirit":15, "defense":10})
c = Star(imp, b, {"physique":15, "aether resist":8})
d = Star(imp, c, {"fire %":24, "aether %":24})
e = Star(imp, d, {})
#aoe is on target
#it ticks per second for duration
#it stacks on itself
e.addAbility(Ability(
	"Aetherfire", 
	{"type":"attack", "trigger":"attack", "chance":.15, "targets":1.5, "duration":3, "shape":"ground"},
	{"triggered fire":140*3, "triggered aether":190*3, "stun %":33} ))

lizard = Constellation("Lizard", "1p", "4p")
lizard.id = "lizard"
a = Star(lizard, [], {"health/s":8, "constitution %":15})
b = Star(lizard, a, {"health/s":16, "health":50, "move speed":3})
c = Star(lizard, b, {"health":50, "health/s %":40, "healing %":6})

guide = Constellation("Sailor's Guide", "1p", "5p")
guide.id = "guide"
a = Star(guide, [], {"physique":15, "defense":8})
b = Star(guide, a, {"reduced freeze":18, "slow resist":18})
c = Star(guide, b, {"move speed":10, "physique":15})
d = Star(guide, b, {"physical resist":3, "elemental resist":15})

scarab = Constellation("Scarab", "1p", "2o 3p")
scarab.id = "scarab"
a = Star(scarab, [], {"physique":15, "armor":20})
b = Star(scarab, a, {"blocked damage %":16})
c = Star(scarab, b, {"bleed resist":15, "armor %":8})
d = Star(scarab, b, {"stun resist":15, "damage blocked %":16, "acid retaliation":40})

tsunami = Constellation("Tsunami", "1p", "5p")
tsunami.id = "tsunami"
a = Star(tsunami, [], {"lightning %": 15, "cold %":15})
b = Star(tsunami, a, {"spirit":15, "defense":20})
c = Star(tsunami, b, {"electrocute %":40, "frostburn %":40, "physique":15})
d = Star(tsunami, c, {"lightning %":24, "cold %":24})
e = Star(tsunami, d, {})
#35% on attack
#12m range
# pretty wide line attack from me toward target with 100% pass through
e.addAbility(Ability(
	"Tsunami", 
	{"type":"attack", "trigger":"attack", "chance":.35, "recharge":1, "targets":2.5, "shape":"line"},
	{"weapon damage %":45, "triggered cold":(180+215)/2, "triggered lightning":(82+130)/2, "triggered frostburn":[225,2]} ))

wraith = Constellation("Wraith", "1p", "3a 3p")
wraith.id = "wraith"
a = Star(wraith, [], {"aether %":15, "lightning %":15})
b = Star(wraith, a, {"spirit":15, "aether resist":8, "retaliation %":30})
c = Star(wraith, a, {"energy absorb":15, "offense":24, "lightning retaliation":(25+85)/2})
d = Star(wraith, a, {"aether %":24, "lightning %":24, "damage undead %":6})

affliction = Constellation("Affliction", "4a 3c 4e", "1a 1e")
affliction.id = "affliction"
a = Star(affliction, [], {"vitality %":40, "poison %":40})
b = Star(affliction, a, {"spirit":20, "offense":20, "defense":20, "acid retaliation":60})
c = Star(affliction, b, {})
# small enough to not catch multiples.
c.addAbility(Ability(
	"Fetid Pool", 
	{"type":"attack", "trigger":"hit", "chance":.33, "recharge":2, "duration":6, "targets":1, "shape":"ground"},
	{"retaliation damage %":8, "slow move":30, "triggered vitality":370, "vitality decay":[490, 2]} ))
d = Star(affliction, c, {"poison %":50, "offense %":4, "all retaliation %":60})
e = Star(affliction, d, {"vitality decay":[45, 3], "vitality decay %":60, "vitality decay duration":50, "offense":40, "acid retaliation":90})
f = Star(affliction, c, {"poison %":50, "defense %":4, "retaliation %":60})
g = Star(affliction, f, {"vitality decay":[45, 3], "vitality decay %":60, "vitality decay duration %":50, "defense":40, "acid retaliation":90})

phoenix = Constellation("Alladrah's Phoenix", "6e 3o 6p", "2a 2e")
phoenix.id = "phoenix"
a = Star(phoenix, [], {"aether %":40, "elemental %":40})
b = Star(phoenix, a, {"health":250, "chaos resist":12})
c = Star(phoenix, b, {"aether %":30, "elemental %":30, "freeze resist":15, "fire retaliation":200})
d = Star(phoenix, c, {"crit damage":10, "fire %":50, "burn %":50, "burn duration":30, "retaliation %":80})
e = Star(phoenix, d, {})
# haven't seen this one in actions so all of these numbers are guestimates
e.addAbility(Ability(
	"Phoenix Fire",
	{"type":"attack", "trigger":"critical", "chance":1, "recharge":12, "duration":7, "targets":2.5, "shape":"pbaoe"},
	{ "damage absorb":188, "fire retaliation":360, "retaliation %":140, "triggered fire":92, "triggered aether":92, "triggered burn":[195, 2]} ))

winter = Constellation("Amatok the Spirit of Winter", "4e 6p", "1e 1p")
winter.id = "winter"
a = Star(winter, [], {"cold %":40})
b = Star(winter, a, {"health %":6, "defense":15})
c = Star(winter, b, {"armor":80, "defense":30})
d = Star(winter, b, {"cold %":50, "frostburn %":50, "armor":60})
e = Star(winter, d, {"frostburn":[36,3], "cold %":50, "frostburn %":100})
f = Star(winter, b, {"offense":25, "frostburn %":50, "frostburn duration":50})
g = Star(winter, f, {})
#2m radius
#looks like there are multiple missiles but it's not listed
g.addAbility(Ability(
	"Blizzard", 
	{"type":"attack", "trigger":"critical", "chance":1, "recharge":3.2, "targets":3, "shape":"ground"},
	{"weapon damage %":16, "triggered cold":(315+392)/2, "triggered frostburn":[245,2], "stun %":50, "slow move":70} ))

assassin = Constellation("Assassin", "6a 4o", "1a 1o")
assassin.id = "assassin"
a = Star(assassin, [], {"pierce %":40})
b = Star(assassin, a, {"cunning":20, "armor":60})
c = Star(assassin, b, {"offense":18, "defense":10, "avoid ranged":4})
d = Star(assassin, b, {"bleed resist":10, "cunning %":5})
e = Star(assassin, d, {"defense":25, "acid resist":10, "poison resist":10, "damage human %":8})
f = Star(assassin, d, {"pierce":8, "pierce %":50})
g = Star(assassin, f, {})
# projectiles fire in every direction. I think I'll use pbaoe shape since it's best if surrounded.
g.addAbility(Ability(
	"Blades of Wrath", 
	{"type":"attack", "trigger":"critical", "chance":1, "recharge":2, "targets":4, "shape":"pbaoe"},
	{"triggered pierce":(270+310)/2, "weapon damage %":25} ))

boar = Constellation("Autumn Boar", "4a 3o 4p", "3a")
boar.id = "boar"
boar.restricts = ["shield"]
a = Star(boar, [], {"physique":20, "cunning":20, "retaliation %":30})
b = Star(boar, a, {"pierce resist":15, "physique":15})
c = Star(boar, b, {"physique %":5, "retaliation %":30})
d = Star(boar, c, {"defense":25, "move speed":5})
e = Star(boar, c, {"defense":30, "retaliation %":60})
f = Star(boar, e, {"physical resist":4, "reflected damage reduction":15, "physical retaliation":150})
g = Star(boar, e, {})
# long line in direction of hitter
g.addAbility(Ability(
	"Trample", 
	{"type":"attack", "trigger":"block", "chance":.33, "recharge":1, "targets":2.5, "shape":"line"},
	{"stun %":100, "weapon damage %":55, "retaliation to attack":18, "triggered internal":[285, 2]} ))

harp = Constellation("Bard's Harp", "6a 3o 6p", "2o 2p")
harp.id = "harp"
a = Star(harp, [], {"health":200, "constitution %":20})
b = Star(harp, a, {"pierce %":40, "elemental %":40, "energy/s %":10})
c = Star(harp, b, {"health":300, "pierce resist":15, "bleed resist":10})
d = Star(harp, c, {"energy %":10, "energy/s":3})
e = Star(harp, c, {"pierce %":50, "elemental %":50, "burn %":80, "frostburn %":80, "electrocute %":80, "elemental resist":15})
f = Star(harp, e, {})
#15m radius
f.addAbility(Ability(
	"Inspiration", 
	{"type":"buff", "trigger":"hit", "chance":.15, "recharge":12, "duration":6},
	{"energy %":25, "pet energy %":25, "offense":130, "pet offense":130, "defense":160, "pet defense":160, "energy/s":7, "pet energy/s":7, "slow resist":45} ))

behemoth = Constellation("Behemoth", "3c 4e 4p", "2c 3e")
behemoth.id = "behemoth"
a = Star(behemoth, [], {"health/s":30})
b = Star(behemoth, a, {"health":300, "pet health %":12})
c = Star(behemoth, b, {"health/s":70, "healing %":6})
d = Star(behemoth, b, {"health %":8, "armor":80, "pet armor":100})
e = Star(behemoth, b, {"health/s %":80, "pet health/s %":100})
f = Star(behemoth, b, {})
ability = Ability(
	"Giant's Blood", 
	{"type":"heal", "trigger":"hit", "chance":.15, "recharge":25, "duration":12},
	{"health":1200, "health %":20, "health/s":280} )
f.addAbility(ability)

berserker = Constellation("Berserker", "5a 5e", "2c 3e")
berserker.id = "berserker"
berserker.restricts = ["axe", "2h-axe", "spear"]
a = Star(berserker, [], {"offense":20, "health":300})
b = Star(berserker, a, {"physical %":50, "bleed %":50, "freeze resist":15})
c = Star(berserker, b, {"offense":60, "crit damage":5})
f = Star(berserker, a, {"health/s":15, "healing %":15, "physical resist":4, "pierce resist":15})
d = Star(berserker, a, {"bleed %":50, "physical %":50, "stun resist":15})
e = Star(berserker, d, {"bleed":[60, 3], "bleed %":50, "bleed %":50, "bleed duration":50})

blades = Constellation("Blades of Nadaan", "10a", "3a 2o")
blades.id = "blades"
blades.restricts = ["sword"]
a = Star(blades, [], {"avoid melee":2, "avoid ranged":2})
b = Star(blades, a, {"pierce %":40})
c = Star(blades, b, {"pierce %":50})
d = Star(blades, b, {"attack speed":4, "defense":15})
e = Star(blades, b, {"attack speed":4, "defense":15})
f = Star(blades, b, {"armor piercing %":100, "pierce":12})

bonds = Constellation("Bysmiel's Bonds", "4c 6e", "3e")
bonds.id = "bonds"
a = Star(bonds, [], {"offense":15, "pet all damage %":30})
b = Star(bonds, a, {"physique":15, "cast speed":5, "pet all damage %":50})
c = Star(bonds, b, {"vitality resist":15, "pet vitality resist":20})
d = Star(bonds, c, {"all damage %":30, "pet all damage %":50})
e = Star(bonds, d, {})
#20% on attack
#30 second recharge
#20 second lifespan
#1 lifespan per fight
# 4 attacks?
# scales with pet bonuses
e.addAbility(Ability(
	"Bysmiel's Command", 
	{"type":"summon", "trigger":"attack", "chance":.2, "recharge":30, "lifespan":20},
	{"triggered physical":(125+192)/2*4, "triggered acid":(154+212)/2*4} ))

chariot = Constellation("Chariot of the Dead", "5a 5e", "2c 3e")
chariot.id = "chariot"
a = Star(chariot, [], {"cunning":20, "physique":20})
b = Star(chariot, a, {"offense":15, "slow resist":10})
c = Star(chariot, b, {"cunning":25, "armor":60})
d = Star(chariot, c, {"vitality resist":16, "stun resist":20})
e = Star(chariot, c, {"offense":25, "slow resist":15})
f = Star(chariot, e, {"offense %":4, "offense":15})
g = Star(chariot, f, {})
g.addAbility(Ability(
	"Wayward Soul", 
	{"type":"heal", "trigger":"hit", "chance":.2, "recharge":8, "duration":5},
	{"health %":12, "health":1550, "defense":130, "armor":460} ))

crab = Constellation("Crab", "6a 4o", "3a")
crab.id = "crab"
a = Star(crab, [], {"constitution %":15, "physique":25})
b = Star(crab, a, {"elemental %":40, "internal %":40, "physical %":40})
c = Star(crab, b, {})
c.addAbility(Ability(
	"Arcane Barrier",
	{"type":"shield", "trigger":"hit", "chance":.15, "recharge":3},
	{"elemental shield":1150} ))
d = Star(crab, c, {"pierce resist":18, "defense":35})
e = Star(crab, d, {"elemental":15, "elemental %":40, "elemental resist":15})

crab = Constellation("Crab", "6a 4o", "3a")
crab.id = "crab"
a = Star(crab, [], {"constitution %":15, "physique":25})
b = Star(crab, a, {"elemental %":50, "internal %":50, "physical %":50})
c = Star(crab, b, {})
c.addAbility(Ability(
	"Arcane Barrier",
	{"type":"shield", "trigger":"hit", "chance":.30, "recharge":3},
	{"elemental shield":2900} ))
d = Star(crab, c, {"pierce resist":18, "offense":40, "defense":40})
e = Star(crab, d, {"elemental":15, "elemental %":60, "burn %":100, "frostburn %":100, "electrocute":100, "elemental resist":15})

bear = Constellation("Dire Bear", "5a 5p", "1a 1p")
bear.id = "bear"
a = Star(bear, [], {"physical %":40})
b = Star(bear, a, {"physique":20, "cunning":20, "defense":15})
c = Star(bear, b, {"physical %":50, "armor":60})
d = Star(bear, c, {"stun resist":15, "freeze resist":15, "health %":6})
e = Star(bear, [], {"armor":80, "lifesteal %":4})
f = Star(bear, d, {})
#4.5m radius
f.addAbility(Ability(
	"Maul", 
	{"type":"attack", "trigger":"attack", "chance":.2, "recharge":1, "targets":3, "shape":"pbaoe"},
	{"lifesteal %":45, "triggered physical":305, "armor %":35} )) # is this really supposed to be -35 armor %?

scythe = Constellation("Harvestman's Scythe", "3a 3o 5p", "3a 3p")
scythe.id = "scythe"
a = Star(scythe, [], {"energy/s":2, "move speed":3})
b = Star(scythe, a, {"health":200, "energy":200, "move speed":3})
c = Star(scythe, b, {"physique %":4, "healing %":10})
d = Star(scythe, c, {"cunning %":4, "spirit %":4})
e = Star(scythe, d, {"defense %":4, "health/s %":60, "energy/s %":30})
f = Star(scythe, e, {"health %":8, "energy %":8, "health/s":50, "energy/s":3})

huntress = Constellation("Huntress", "4a 3c 4e", "1a 1e")
huntress.id = "huntress"
a = Star(huntress, [], {"health":200, "offense":15})
b = Star(huntress, a, {"pierce %":50, "cunning":20})
c = Star(huntress, b, {"bleed %":60, "offense":25})
d = Star(huntress, c, {"pierce resist":8, "damage beast %":8, "armor":60, "all damage %":40, "pet health %":12})
e = Star(huntress, c, {"offense %":3, "health/s":25, "healing %":12, "pet offense %":5})
f = Star(huntress, e, {"bleed":[45,3], "bleed %":50, "bleed duration":20, "pet bleed %":80})
g = Star(huntress, e, {})
# no stat for reducing opponent offense so we'll call it defense

#halfway between an attack and a buff. Since the debuff doesn't overlap I'm going to set the recharge to the duration.
# this will slightly undervalue the skill as it can refresh within it's duration.
# I can't decide if I want to use targets. The "defense" part assumes I'll hit everything hitting me so it's over valued.
# the bleed resist reduction feels like I shouldn't count it per target since it only matters on the things I'm hitting and hitting things is already accounted for.

# I'm treating reduced offense like defense so don't count the targets (it's built into that conversion)
# reduced resist only matters when other stuff hits so reducing resist on stuff I'm not hitting doesn't count for anything.
# remove the multi target component (I'm overcounting defense and undercounting reduced resist a bit).
g.addAbility(Ability(
	"Rend", 
	{"type":"attack", "trigger":"attack", "chance":.2, "recharge":0, "duration":5, "targets":3, "shape":"circle"},
	{"defense":150, "reduced bleed resist":32, "triggered bleed":[325, 5]} ))

hydra = Constellation("Hydra", "3a 3c 5e", "2c 3e")
hydra.id = "hydra"
hydra.restricts = ["ranged"]
a = Star(hydra, [], {"offense":25})
b = Star(hydra, a, {"offense":35, "move speed":6})
f = Star(hydra, b, {"all damage %":50, "attack speed":5, "max move speed":3})
c = Star(hydra, b, {"lifesteal %":5, "attack speed":5, "max move speed":3})
d = Star(hydra, b, {"physical":6, "offense":25})
e = Star(hydra, d, {"physical":12, "offense %":4, "slow resist":20})

kraken = Constellation("Kraken", "5e 5p", "2c 3p")
kraken.id = "kraken"
kraken.restricts = ["twohand"]
a = Star(kraken, [], {"all damage %":50})
b = Star(kraken, a, {"crit damage":15, "physical resist":4})
c = Star(kraken, a, {"all damage %":70, "move speed":5})
d = Star(kraken, a, {"health":250, "attack speed":13, "cast speed":5})
e = Star(kraken, a, {"health":250, "attack speed":13, "cast speed":5})

magi = Constellation("Magi", "10e", "3e")
magi.id = "magi"
a = Star(magi, [], {"fire %":40})
b = Star(magi, a, {"elemental resist":8, "defense":15})
c = Star(magi, b, {"defense":20, "energy/s":1.5, "entrapment resist":15, })
d = Star(magi, c, {"burn %":50, "physique":15, "attack speed":5, "cast speed":5})
e = Star(magi, c, {"fire":(11+14)/2, "fire %":40, "freeze resist":15})
f = Star(magi, c, {"burn":[36,3], "burn %":50, "burn duration":30})
g = Star(magi, f, {})
# 1 meter radius
# 7 fragments
# trigger creates a volcano that spits out 8 volleys of ~7 fireballs about 2m
# there can be multiples active.
g.addAbility(Ability(
	"Fissure", 
	{"type":"attack", "trigger":"attack", "chance":.15, "recharge":1.8, "duration":5, "targets":2, "shape":"ground"},
	{"triggered fire":(160+198)/2, "triggered burn":[195,2], "stun %":25} ))

manticore = Constellation("Manticore", "4c 6e", "1a 1e")
manticore.id = "manticore"
a = Star(manticore, [], {"health":250, "offense":15})
b = Star(manticore, a, {"acid %":50, "poison %":50, "pet acid %":60, "pet poison %":60})
c = Star(manticore, b, {"health %":6, "pet health %":12})
d = Star(manticore, c, {"offense":20, "physical resist":4, "acid resist":10, "poison resist":10, "pet all damage %":40, "pet offense %":4})
e = Star(manticore, c, {"poison":[40,5], "acid %":40, "poison %":40, "poison duration":30, "pet acid %":60, "pet poison %":60})
f = Star(manticore, e, {})
# weird shape. It hits the target and things behind it in a cone. It's pretty strong for any kiter. Shortranged may suffer since the direction will be pretty random in aoe situations.
f.addAbility(Ability(
	"Acid Spray", 
	{"type":"attack", "trigger":"attack", "chance":.15, "recharge":1, "duration":5, "targets":2},
	{"triggered acid":217, "triggered poison":[195,2], "reduce resist":28} ))

messenger = Constellation("Messenger of War", "3a 7p", "2c 3p")
messenger.id = "messenger"
a = Star(messenger, [], {"fire retaliation":90, "retaliation %":30})
b = Star(messenger, a, {"offense":20, "move speed":5, "physique":20})
c = Star(messenger, b, {"offense":25, "retaliation %":60})
d = Star(messenger, c, {"armor %":12, "fire retaliation":120})
e = Star(messenger, b, {"elemental resist":15, "fire retaliation":120})
f = Star(messenger, e, {})
# 20% when hit
# 15s recharge
# 8s duration
f.addAbility(Ability(
	"Messenger of War", 
	{"type":"buff", "trigger":"hit", "chance":.2, "recharge":15, "duration":8},
	{"move speed":30, "slow resist":70, "fire retaliation":860, "retaliation %":140, "fire retaliation %":140} ))

mistress = Constellation("Murmur, Mistress of Rumors", "3c 6e 6p", "2c 2e")
mistress.id = "mistress"
a = Star(mistress, [], {"cold %":40, "acid %":40})
b = Star(mistress, a, {"avoid melee":3, "avoid ranged":3})
c = Star(mistress, b, {"health":200, "defense":20})
d = Star(mistress, c, {})
#untested
d.addAbility(Ability(
	"Rumor", 
	{"type":"attack", "trigger":"attack", "chance":.15, "recharge":1, "duration":4, "targets":3}, #guesses
	{"triggered acid":97, "triggered cold":97, "defense":96, "reduce cold resist":23, "reduce acid resist":30, "reduce poison resist":30} ))
e = Star(mistress, d, {"defense":20, "vitality resist":15})
f = Star(mistress, d, {"cold %":50, "acid %":50, "frostburn %":80})

lantern = Constellation("Oklaine's Lantern", "10e", "3e 2o")
lantern.id = "lantern"
lantern.restricts = ["scepter", "dagger", "offhand"]
a = Star(lantern, [], {"energy/s %":15})
b = Star(lantern, a, {"offense":25, "defense":20})
c = Star(lantern, b, {"offense":15, "crit damage":5})
d = Star(lantern, c, {"all damage %":50, "reduced entrapment duration":25})
e = Star(lantern, d, {"cast speed":5, "attack speed":5, "energy/s":2})

revenant = Constellation("Revenant", "8c", "1c 1p")
revenant.id = "revenant"
a = Star(revenant, [], {"energy leech":40*.1, "energy absorb":15})
b = Star(revenant, a, {"health %":6, "damage from undead":-10})
c = Star(revenant, b, {"vitality resist":24, "stun resist":20})
d = Star(revenant, c, {"vitality%":60, "health":250, "lifesteal %":6})
e = Star(revenant, d, {"aether %":60, "attack speed":4, "cast speed":4})
f = Star(revenant, e, {})
#100% on enemy kill from the selected skill
#3 s recharge
#5 summon limit
# 20 s lifespan
# 10 attacks per summon (1/2.5s)
lifespan = 20
secondsPerAttack = 2+4 #2 seconds per attack? 4 seconds spent chasing on average
numAttacks = lifespan/secondsPerAttack
f.addAbility(Ability(
	"Raise the Dead", 
	{"type":"summon", "trigger":"attack", "chance":.2, "recharge":2, "lifespan":lifespan, "limit":6},
	{"triggered vitality":230*numAttacks, "triggered aether":230*numAttacks, "slow move":45, "reduce resist":24*1/secondsPerAttack} ))

crown = Constellation("Rhowan's Crown", "4a 6e", "1a 1e")
crown.id = "crown"
storm = Ability(
	"Elemental Storm",
	{"type":"attack", "trigger":"attack", "chance":.25, "recharge":1.5, "duration":5, "targets":2.5, "shape":"ground"},
	{"duration":{"triggered elemental":132, "triggered frostburn":[196,2], "triggered electrocute":[196,2], "triggered burn":[196,2], "reduce elemental resist":32}} )
a = Star(crown, [], {"elemental %":30, "elemental":(6+9)/2})
b = Star(crown, a, {"spirit":20, "defense":20, "pet elemental %":60})
c = Star(crown, b, {})
c.addAbility(storm)
d = Star(crown, c, {"offense":20, "elemental resist":18, "pet elemental resist":18})
e = Star(crown, d, {"elemental %":40, "burn %":60, "electrocute %":60, "frostburn %":60, "chaos resist":8})

crownStorm = Constellation("Rhowan's Crown (Elemental Storm)", "4a 6e", "")
crownStorm.id = "crownStorm"
a = Star(crownStorm, [], {"elemental %":30, "elemental":(6+9)/2})
b = Star(crownStorm, a, {"spirit":20, "defense":20, "pet elemental %":60})
c = Star(crownStorm, b, {})
c.addAbility(storm)

scepter = Constellation("Rhowan's Scepter", "6a 4o", "3a 2o")
scepter.id = "scepter"
scepter.restricts = ["mace"]
a = Star(scepter, [], {"defense":20, "armor":30})
b = Star(scepter, a, {"health %":6, "armor":80})
c = Star(scepter, b, {"physical %":50, "petrify resist":25})
d = Star(scepter, c, {"physical":10, "physical %":50, "armor %":8})
e = Star(scepter, b, {"internal %":50, "defense":50})
f = Star(scepter, e, {"internal":[100, 5], "internal %":80, "internal duration":50})

scales = Constellation("Scales of Ulcama", "8o", "2o")
scales.id = "scales"
a = Star(scales, [], {"health":250, "energy":300})
b = Star(scales, a, {"health %":6, "move speed":6})
c = Star(scales, b, {"energy/s":2.5, "energy/s %":33})
d = Star(scales, c, {"lifesteal %":5, "health/s":30, "health/s %":33})
e = Star(scales, b, {"physique":20, "defense":45})
f = Star(scales, e, {})
# assuming single target
f.addAbility(Ability(
	"Tip the Scales", 
	{"type":"attack", "trigger":"hit", "chance":.33, "recharge":1},
	{"weapon damage %":33, "triggered vitality":310, "energy":400, "lifesteal %":132, "reduce resists":20} ))

shieldmaiden = Constellation("Shieldmaiden", "4o 6p", "2o 3p")
shieldmaiden.id = "shieldmaiden"
shieldmaiden.restricts = ["shield"]
a = Star(shieldmaiden, [], {"defense":20, "blocked damage %":30})
b = Star(shieldmaiden, a, {"internal %":50, "retaliation %":60})
c = Star(shieldmaiden, b, {"defense":50, "block %":5})
d = Star(shieldmaiden, c, {"internal":[100,5], "block %":6, "physical retaliation":200})
e = Star(shieldmaiden, b, {"stun resist":25, "blocked damage %":50})
f = Star(shieldmaiden, e, {"shield recovery":25, "blocked damage %":80})

witchblade = Constellation("Solael's Witchblade", "4c 6e", "1c 1e")
witchblade.id = "witchblade"
a = Star(witchblade, [], {"chaos %":40})
b = Star(witchblade, a, {"offense":10, "spirit":15, "physique":15})
c = Star(witchblade, b, {"chaos %":30, "fire %":30, "defense":15})
d = Star(witchblade, c, {"fire %":50, "chaos %":50, "defense":25})
e = Star(witchblade, d, {})
# says "spreads wildly among your foes" max 3
# Jumps 4m. I'm going to call it 2.5 targets for now
# rapidly reapplying seems to prevent spreading.
# it doesn't seem to stack
e.addAbility(Ability(
	"Eldritch Fire", 
	{"type":"attack", "trigger":"attack", "chance":.15, "recharge":1, "duration":4, "targets":2.5},
	{"triggered fire":120, "triggered chaos":120, "slow move":36, "reduce fire resist":23, "reduce chaos resist":35} ))

watcher = Constellation("Solemn Watcher", "10p", "2o 3p")
watcher.id = "watcher"
a = Star(watcher, [], {"physique":25})
b = Star(watcher, a, {"armor":40, "chaos resist":18})
c = Star(watcher, b, {"armor":40, "pierce resist":18})
d = Star(watcher, c, {"defense":30, "physique %":3})
e = Star(watcher, d, {"defense %":5, "reflected damage reduction":20})

staff = Constellation("Staff of Rattosh", "3c 3o 6p", "2c 2p")
staff.id = "staff"
a = Star(staff, [], {"defense":20, "pet defense %":3})
b = Star(staff, a, {"aether resist":15, "pet aether resist":20})
c = Star(staff, b, {"health":250, "pet all damage %":50, "pet aether %":70})
d = Star(staff, c, {"health %":5, "vitality resist":10, "pet vitality resist":20})
e = Star(staff, d, {"aether damage %":50, "pet all damage %":50, "pet aether %":70})
f = Star(staff, e, {"offense %":4, "pet offense %":3, "pet total speed":8})

targo = Constellation("Targo the Builder", "4o 6p", "1o")
targo.id = "targo"
targo.restricts = ["shield"]
a = Star(targo, [], {"defense":20, "retaliation %":30})
b = Star(targo, a, {"health %":6, "aether resist":8})
c = Star(targo, b, {"armor %":8, "physical retaliation":150})
d = Star(targo, b, {"health %":6, "chaos resist":8})
e = Star(targo, d, {"defense":35, "health":300, "retaliation %":90})
f = Star(targo, d, {"armor %":12, "blocked damage %":24})
g = Star(targo, f, {})
g.addAbility(Ability(
	"Shield Wall", 
	{"type":"buff", "trigger":"attack", "chance":.25, "recharge":8, "duration":5},
	{"physical retaliation":525, "blocked damage %":210, "armor %":50} ))

tempest = Constellation("Tempest", "5a 5p", "1e 1p")
tempest.id = "tempest"
a = Star(tempest, [], {"lightning %":40})
b = Star(tempest, a, {"lightning":(8+20)/2, "physique":20})
c = Star(tempest, b, {"lightning %":50, "electrocute %":50})
d = Star(tempest, c, {"offense":25, "defense":25, "slow resist":10})
e = Star(tempest, d, {"total speed":4, "lightning %":250*.3, "stun resist":15})
f = Star(tempest, d, {"offense":20, "electrocute %":50, "electrocute duration":50})
g = Star(tempest, f, {})
# 3 target max
# 8 meter radius
# .5s interval
# 12 bolts
g.addAbility(Ability(
	"Reckless Tempest", 
	{"type":"attack", "trigger":"critical", "chance":1, "recharge":10, "duration":6, "targets":3},
	{"triggered lightning":(118+290)/2, "triggered electrocute":[245,2], "stun %":20} ))

typhos = Constellation("Typhos, Jailor of Souls", "6a 3c 3o", "2a 2o")
typhos.id = "typhos"
a = Star(typhos, [], {"offense":20, "pet offense %":3})
b = Star(typhos, a, {"defense":20, "pet defense %":3})
c = Star(typhos, b, {"acid resist":15, "poison resist":15, "bleed resist":15, "pet acid resist":15, "pet poison resist":15, "pet bleed resist":15})
d = Star(typhos, c, {"total speed":4, "pet physical resist":6, "pet stun resist":50, "pet mind control duration":-50})
e = Star(typhos, c, {"health %":6, "offense":20, "pet all damage %":40, "pet offense %":3})
f = Star(typhos, e, {"crit damage":10, "pet all damage %":40, "pet crit damage %":15})

ulo = Constellation("Ulo the Keeper of the Waters", "4o 6p", "2o 3p")
ulo.id = "ulo"
a = Star(ulo, [], {"elemental resist":15, "pet elemental resist":15})
b = Star(ulo, a, {"health":300, "energy":300, "life leech resist":30, "energy leech resist":30})
c = Star(ulo, b, {"stun resist":15, "freeze resist":15, "petrify resist":15, "pet stun resist":15, "pet freeze resist":15, "pet petrify resist":15})
d = Star(ulo, b, {"acid resist":20, "poison resist":20, "chaos resist":20, "pet acid resist":20, "pet poison resist":20, "pet chaos resist":20})
e = Star(ulo, b, {})
#3m radius
# cleansing effect is very hard to quantify :(
e.addAbility(Ability(
	"Cleansing Waters", 
	{"type":"attack", "trigger":"attack", "chance":1, "recharge":10, "targets":2, "duration":1, "shape":"pbaoe"},
	{"slow move":50} ))

wendigo = Constellation("Wendigo", "4c 6p", "2c")
wendigo.id = "wendigo"
a = Star(wendigo, [], {"vitality %":40, "vitality decay %":40})
b = Star(wendigo, a, {"spirit":20, "health":300})
c = Star(wendigo, b, {"defense":40, "total speed":5})
d = Star(wendigo, c, {"health %":6, "damage from beasts":-10})
e = Star(wendigo, d, {"vitality decay":[36,3], "vitality %":50, "vitality decay %":50})
f = Star(wendigo, e, {})
#giving it 3 targets since it's 0 recharge I can keep a few going.
f.addAbility(Ability(
	"Wendigo's Mark", 
	{"type":"attack", "trigger":"attack", "chance":.15, "recharge":0, "duration":10, "targets":3},
	{"triggered vitality":270, "lifesteal %":65} ))

widow = Constellation("Widow", "6e 4p", "3p")
widow.id = "widow"
a = Star(widow, [], {"aether %":40})
b = Star(widow, a, {"offense":18, "defense":10, "energy %":5})
c = Star(widow, b, {"aether %":30, "spirit":15, "physique":15})
d = Star(widow, c, {"vitality resist":8, "aether resist":18})
e = Star(widow, d, {"aether %":50, "lightning %":50, "offense %":2})
f = Star(widow, e, {})
f.addAbility(Ability(
	"Arcane Bomb", 
	{"type":"attack", "trigger":"attack", "chance":.25, "recharge":2, "targets":2, "shape":"ground"},
	{"triggered lightning":120, "triggered aether":160, "defense":95, "reduce lightning resist":35, "reduce aether resist":40} ))

abomination = Constellation("Abomination", "8c 18e")
abomination.id = "abomination"
a = Star(abomination, [], {"chaos %":80, "poison %":80})
b = Star(abomination, a, {"vitality %":80, "vitality decay %":80, "acid %":80})
c = Star(abomination, b, {"offense":40, "acid resist":20, "max acid resist":3, "poison resist":20, "max poison resist":3})
d = Star(abomination, c, {"vitality %":80, "chaos %":80, "health":400, "offense":40})
e = Star(abomination, d, {})
e.addAbility(Ability(
	"Abominable Might",
	{"type":"buff", "trigger":"attack", "chance":.2, "recharge":18, "duration":12},
	{"chaos":(54-135)/2, "vitality %":310, "chaos %":260, "vitality decay %":310, "physical to chaos":50, "health/s %":100} ))
f = Star(abomination, c, {"poison %":80, "vitality decay %":80, "health":400, "offense":40})
g = Star(abomination, f, {"acid":12, "acid %":100, "poison %":100})
h = Star(abomination, g, {})
# 10 meter radius (huge)
h.addAbility(Ability(
	"Tainted Eruption",
	{"type":"attack", "trigger":"attack", "chance":.15, "recharge":3, "targets":3, "shape":"pbaoe"},
	{"triggered poison":[1560,5], "stun %":100} ))

hourglass = Constellation("Aeon's Hourglass", "8c 18p")
hourglass.id = "hourglass"
a = Star(hourglass, [], {"physique":40, "cunning":40, "spirit":40})
b = Star(hourglass, a, {
	"reduced internal duration":25,
	"reduced bleed duration":25, 
	"reduced burn duration":25, 
	"reduced frostburn duration":25, 
	"reduced electrocute duration":25, 
	"reduced poison duration":25,
	"reduced vitality decay duration":25 })
c = Star(hourglass, b, {"reflected damage reduction":25, "entrapment resist":30, "slow resist":50})
d = Star(hourglass, c, {"vitality resist":15, "max vitality resist":4, "aether resist":20})
e = Star(hourglass, d, {"defense":70, "avoid melee":6, "avoid ranged":6})
f = Star(hourglass, e, {})
#no idea how to quantify this one
f.addAbility(Ability(
	"Time Dilation", 
	{"type":"attack", "trigger":"attack", "chance":.2, "recharge":16},
	{"reduce cooldown":6} ))

mirage = Constellation("Attak Seru, the Mirage", "16a 14e")
mirage.id = "mirage"
a = Star(mirage, [], {"aether %":80, "defense":25})
b = Star(mirage, a, {"elemental %":80, "defense":25})
c = Star(mirage, b, {"health":300, "pierce resist":25, "bleed resist":25})
d = Star(mirage, c, {"offense %":4, "defense %":6, "armor":100})
e = Star(mirage, d, {"elemental":16, "aether %":100, "elemental %":100})
f = Star(mirage, d, {})
# max 4 summons
# lasts 3 seconds (guessing 2 attacks)
f.addAbility(Ability(
	"Arcane Currents", 
	{"type":"summon", "trigger":"attack", "chance":.25, "recharge":1, "lifespan":4.5},
	{"triggered elemental":235*2, "triggered aether":235*2} ))

sage = Constellation("Blind Sage", "10a 18e")
sage.id = "sage"
a = Star(sage, [], {"offense":25, "spirit":30, "physique":30})
b = Star(sage, a, {"elemental %":80, "defense":40, "elemental resist":15})
c = Star(sage, b, {"crit damage":12, "physical resist":4, "skill disruption protection":30})
d = Star(sage, c, {"cold %":100, "frostburn %":250, "frostburn duration":25, "offense":45})
e = Star(sage, c, {"lightning %":100, "electrocute %":250, "electrocute duration":25, "offense":45})
f = Star(sage, c, {"fire %":100, "burn %":250, "burn duration":25, "offense":45})
g = Star(sage, f, {})
# 5 s lifespan
# call it 3 attacks and a detonate hitting 2 targets
# reducing the stun because it's on detonate after 5 seconds etc.
g.addAbility(Ability(
	"Elemental Seeker",
	{"type":"summon", "trigger":"attack", "chance":1, "recharge":1.2, "lifespan":3},
	{"triggered elemental":400*1.5 + 555*1.5, "stun %":100} ))

god = Constellation("Dying God", "8c 15p")
god.id = "god"
a = Star(god, [], {"offense":20, "vitality %":80})
b = Star(god, a, {"offense":20, "chaos %":80})
c = Star(god, b, {"offense %":3, "spirit":35, "pet all damage %":60, "pet chaos %":120})
d = Star(god, c, {"offense":45, "defense":25, "chaos resist":15})
e = Star(god, d, {"vitality %":100, "chaos %":100, "defense":30})
f = Star(god, e, {"chaos":(5+18)/2, "crit damage %":4, "pet all damage %":80, "pet crit damage":10})
g = Star(god, e, {})
g.addAbility(Ability(
	"Hungering Void", 
	{"type":"buff", "trigger":"attack", "chance":.33, "recharge":30, "duration":20},
	{"health/s":-308, "crit damage":18, 
		"vitality %":370, 
		"chaos %":370, 
		"vitality decay %":370, 
		"total speed":10, "chaos retaliation":720, "terrify retaliation":70, 
		"pet all damage %":250, "pet crit damage":20, "stun %":10, "slow move":30*.56} ))

maiden = Constellation("Ishtak, the Spring Maiden", "10o 15p")
maiden.id = "maiden"
a = Star(maiden, [], {"health":300, "energy":300})
b = Star(maiden, a, {"health":300, "acid resist":25, "poison resist":25, "pet acid resist":30, "pet poison resist":30})
c = Star(maiden, b, {"total speed":6, "slow resist":30, "pet all damage %":80})
d = Star(maiden, c, {"health":300, "bleed resist":20, "pet all damage %":80, "pet bleed resist":30})
e = Star(maiden, d, {"spirit %":3, "defense %":4, "pet physical resist":5, "life reduction resist":20})
f = Star(maiden, e, {})
f.addAbility(Ability(
	"Nature's Guardian", 
	{"type":"buff", "trigger":"hit", "chance":.25, "recharge":15, "duration":8},
	{"damage absorb %":25, "pet physical":40, "pet offense":130, "pet defense":130, "reduced resist":18} ))

leviathan = Constellation("Leviathan", "13a 13e")
leviathan.id = "leviathan"
a = Star(leviathan, [], {"cold":6, "cold %":80})
b = Star(leviathan, a, {"health %":8, "physique":35})
c = Star(leviathan, b, {"defense":60, "energy/s %":20, "energy %":10})
d = Star(leviathan, c, {"physical resist":5, "pierce resist":20, "vitality resist":20})
e = Star(leviathan, d, {"cold":12, "cold %":100})
f = Star(leviathan, d, {"frostburn":[60,3], "frostburn %":100, "max cold resist":3})
g = Star(leviathan, d, {})
# 30% on attack
# 3 second recharge
# 6 second duration
# 3.5 meter radius
# ticks per second, cold stacks, fostburn doesnt
# big radius but i'm taking a damage tick away because it's long lasting ground target
g.addAbility(Ability(
	"Whirlpool", 
	{"type":"attack", "trigger":"attack", "chance":.3, "recharge":2, "targets":2, "duration":6, "shape":"ground"}, 
	{"triggered cold":420, "triggered frostburn":[270,2], "slow move":40} ))

empyrion = Constellation("Light of Empyrion", "8o 18p")
empyrion.id = "empyrion"
a = Star(empyrion, [], {"elemental resist":15}) #not quite right but close enough
b = Star(empyrion, a, {"physical %":80, "fire %":80, "damage to cthonics":10, "defense":30})
c = Star(empyrion, b, {"health %":10})
d = Star(empyrion, c, {"health %":10, "vitality resist":15})
e = Star(empyrion, d, {"aether resist":20, "chaos resist":20})
f = Star(empyrion, e, {"fire":(6+10)/2, "physical":(10+14)/2, "max aether resist":3, "max chaos resist":3})
g = Star(empyrion, f, {})
#20% when attacked
#4s recharge
#5m radius
g.addAbility(Ability(
	"Light of Empyrion", 
	{"type":"attack", "trigger":"hit", "chance":.2, "recharge":2.5, "targets":3, "duration":3, "shape":"pbaoe"},
	{"weapon damage %":54, "triggered fire":(280+385)/2, "triggered physical":315, "triggered burn":[270, 2], "stun %":100, "duration":{"reduce damage %":24}, "damage to undead":50, "damage to cthonics":50} ))

wolf = Constellation("Mogdrogen the Wolf", "15a 12e")
wolf.id = "wolf"
a = Star(wolf, [], {"health":300, "offense":35})
b = Star(wolf, a, {"bleed %":80, "damage to undead":10, "pet all damage %":60})
c = Star(wolf, b, {"health":350, "defense":50, "vitality resist":20, "pet bleed damage %":120, "health %":10})
d = Star(wolf, c, {"bleed":[54,3], "bleed %":80, "bleed duration":50, "healing":20})
e = Star(wolf, d, {"offense %":4, "bleed resist":15, "elemental resist":15, "max bleed resist":3, "pet all damage %":80})
f = Star(wolf, e, {})
f.addAbility(Ability(
	"Howl of Mogdrogen", 
	{"type":"buff", "trigger":"attack", "chance":.2, "recharge":15, "duration":10},
	{"bleed":[174,3], "pet bleed":174, "bleed %":275, "offense":144, "health/s %":100, "attack speed":18, "cast speed":15,
		"pet bleed":[96,3], "pet offense %":15, "pet total speed":30 } ))

obelisk = Constellation("Obelisk of Menhir", "8o 15p")
obelisk.id = "obelisk"
obelisk.restricts = ["shield"]
a = Star(obelisk, [], {"armor %":10})
b = Star(obelisk, a, {"defense":30, "armor":150})
c = Star(obelisk, b, {"pierce retaliation":120, "retaliation %":100})
d = Star(obelisk, a, {"defense %":5, "defense":25})
e = Star(obelisk, d, {"block %":5, "blocked damage %":30})
f = Star(obelisk, e, {"armor absorb":18, "reduced stun duration":30, "reduced freeze duration":30, "max pierce resist":3})
g = Star(obelisk, f, {})
g.addAbility(Ability(
	"Stone Form", 
	{"type":"buff", "trigger":"block", "chance":.15, "recharge":12, "duration":8},
	{"damage absorb":400, "reduced poison duration":50, "reduced bleed duration":50, "retaliation %":220} ))

oleron = Constellation("Oleron", "20a 7o")
oleron.id = "oleron"
a = Star(oleron, [], {"physique":30, "cunning":30, "health":100})
b = Star(oleron, a, {"physical %":80, "internal %":80})
c = Star(oleron, b, {"pierce resist":20, "bleed resist":10, "offense":30})
d = Star(oleron, c, {"physical resist":4, "health":200})
e = Star(oleron, d, {"physical":(9+12)/2, "physical %":100})
f = Star(oleron, d, {"offense":15, "internal":[25,5], "internal %":100, "max pierce resist":2})
g = Star(oleron, d, {})

# If we assume everything has enough armor for all of the reduce armor to take effect (if they have less and we're doing physical damage they're probably dead already anyway)
# Then if we know our flat physical we can assume 70% absorb
g.addAbility(Ability(
	"Blind Fury", 
	{"type":"attack", "trigger":"critical", "chance":1, "recharge":1, "duration":5, "targets":2.5, "shape":"pbaoe"},
	{"weapon damage %":70, "triggered pierce":85, "triggered internal":[490/2,2], "triggered bleed":[490/2,2], "duration":{"slow attack":25, "reduce physical resist":12*3/5}} ))

rattosh = Constellation("Rattosh, the Veilwarden", "6c 10e 6o")
rattosh.id = "rattosh"
a = Star(rattosh, [], {"health":150, "offense":20})
b = Star(rattosh, a, {"vitality %":80, "aether %":80})
c = Star(rattosh, b, {"vitality decay %":150, "health":250, "offense":35})
d = Star(rattosh, c, {"vitality %":100, "aether %":100, "vitality decay":48})
e = Star(rattosh, d, {"health":250, "vitality resist":15, "pierce resist":15})
f = Star(rattosh, e, {})
f.addAbility(Ability(
	"Will of Rattosh", 
	{"type":"attack", "trigger":"attack", "chance":.15, "duration":8, "targets":1},
	{"duration":{"triggered vitality":140, "triggered aether":160, "reduce vitality resist":20, "reduce life leech resist":8}} ))

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
	{"weapon damage %":60, "triggered lightning":(192+332)/2, "triggered aether":294, "triggered electrocute":[236/2,2], "stun %":100} ))

tree = Constellation("Tree of Life", "7o 20p")
tree.id = "tree"
a = Star(tree, [], {"health %":5, "pet health %":5})
b = Star(tree, a, {"health/s":20, "pet health/s %":20})
c = Star(tree, b, {"health %":8, "pet health %":5})
d = Star(tree, b, {"health/s":15, "defense":30, "pet health/s %":20})
e = Star(tree, d, {"health %":4, "health/s %":20, "pet health/s":50})
f = Star(tree, d, {})
#25% when hit
#12s recharge
f.addAbility(Ability(
	"Healing Rain", 
	{"type":"heal", "trigger":"hit", "chance":.25, "recharge":12, "duration":8},
	{"duration":{"health/s":100, "energy/s":12, "health/s %":40, "energy/s %":55}, "health %":10, "health":700} ))

ultos = Constellation("Ultos, Shepherd of Storms", "6c 10e 10p")
ultos.id = "ultos"
a = Star(ultos, [], {"cold %":80, "offense":25})
b = Star(ultos, a, {"lightning %":80, "offense":25})
c = Star(ultos, b, {"health":180, "chaos resist":15})
d = Star(ultos, b, {"crit damage":5, "frostburn %":120, "electrocute %":120, "offense":20})
e = Star(ultos, d, {"lightning":(3+20)/2, "cold %":100, "lightning %":100})
f = Star(ultos, e, {})
# says it'll 10 targets but how often will that actually happen. Dropping to 5.
f.addAbility(Ability(
	"Hand of Ultos", 	
	{"type":"attack", "trigger":"critical", "chance":1, "recharge":1.5, "targets":3.5, "duration":3},
	{"weapon damage %":24, "triggered lightning":(224+434)/2, "triggered electrocute":[696/2,2], "duration":{"reduce elemental resist":25}} ))

torch = Constellation("Ulzuin's Torch", "8c 15e")
torch.id = "torch"
a = Star(torch, [], {"offense":20, "fire %":80})
b = Star(torch, a, {"offense %":5, "chaos resist":15})
c = Star(torch, b, {"move speed":5, "crit damage":10})
d = Star(torch, c, {"fire %":100, "fire resist":20})
e = Star(torch, d, {"burn":[25,3], "burn %":100, "max fire resist":3})
f = Star(torch, c, {"burn %":100, "burn duration":100})
g = Star(torch, f, {})
#6m area
#2m radius
#15 meteors
# large area, call it 4 targets in the area
# each missile hits a smallish area, let's say each target gets hit 3 times
# let's say the burn overlaps twice.
g.addAbility(Ability(
	"Meteor Shower", 
	{"type":"attack", "trigger":"attack", "chance":1, "recharge":3.5, "duration":3, "targets":4, "shape":"ground"},
	{"duration":{"triggered fire":(216+265)/2, "triggered physical":(200+228)/2, "triggered burn":376/2}} ))

torchOffense = Constellation("Ulzuin's Torch (offense %)", "8c 15e")
torchOffense.id = "torchOffense"
a = Star(torchOffense, [], {"offense":20, "fire %":80})
b = Star(torchOffense, a, {"offense %":5, "chaos resist":15})

torch.addConflicts([torchOffense])

soldier = Constellation("Unknown Soldier", "15a 8o")
soldier.id = "soldier"
a = Star(soldier, [], {"offense":15, "pierce %":60})
b = Star(soldier, a, {"bleed":[18,3], "bleed %":80})
c = Star(soldier, b, {"attack speed":5, "health":280})
d = Star(soldier, b, {"bleed %":80, "pierce %":80})
e = Star(soldier, d, {"health %":4, "offense":40})
f = Star(soldier, e, {"pierce":12, "crit damage":10})
g = Star(soldier, f, {})
#100% on crit: 15% on attack
#6 second recharge
#3 summon limit
#20 second lifespan
# even more guessworky than most others...
# 2 attacks. shadow strike and shadow blades.
# I'm assuming strike is an engage and blades is the normal attack
# lets assume 1 strike and 4 normal attacks in a lifespan
# 3.3 s to trigger 6 second recharge means 2.5 lifespans in a 30 second fight.
g.addAbility(Ability(
	"Living Shadow", 
	{"type":"summon", "trigger":"critical", "chance":1, "recharge":6, "lifespan":24},
	{"triggered bleed":178+(320*4), "triggered pierce":(205+273)/2+(172+226)/2*4} ))

vire = Constellation("Vire, the Stone Matron", "12a, 18p")
vire.id = "vire"
a = Star(vire, [], {"health":150, "armor":75})
b = Star(vire, a, {"aether resist":10, "chaos resist":10, "physical retaliation":70})
c = Star(vire, b, {"health %":4, "armor":40, "blocked damage %":12})
d = Star(vire, c, {"physical %":80, "internal %":80, "cunning %":3, "retaliation %":80})
e = Star(vire, c, {"physical resist":4, "pierce resist":20, "bleed resist":20})
f = Star(vire, e, {})
f.addAbility(Ability(
	"Fist of Vire", 
	{"type":"attack", "trigger":"hit", "chance":.2, "recharge":1, "duration":5, "targets":1.5, "shape":"circle"},
	{"stun %":100, "weapon damage %":40, "triggered physical":245, "duration":{"triggered internal":970, "physical resist":25}} ))


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
			subC.addConflicts(c.conflicts)

			# print "  ", subC
			abilityFragments += [subC]
			newFragments += [subC]
	# for i in range(min(2, len(c.stars))):
	# 	# for i in range(len(c.stars)):
	# 	star = c.stars[i]
	# 	if star.ability != None:
	# 		continue
	# 	required = [star] + getRequires(star)
	# 	if len(required) < len(c.stars):
	# 		subC = Constellation(c.name + "[" + str(i+1) + "]", c.requires)
	# 		subC.id = c.id + "[" + str(i+1) + "]"
	# 		subC.stars = required
	# 		subC.restricts = c.restricts
	# 		subC.addConflicts(c.conflicts)

	# 		abilityFragments += [subC]
	# 		newFragments += [subC]
	c.addConflicts(newFragments)

for c in abilityFragments:
	globals()[c.id] = c

torch.addConflicts([torchMeteorShower])
