"""Generated from the Grim Dawn database - do not edit.

Regenerate with:  python devotion.py --regenerate

Values are raw game numbers. Proc shape, target count and duration
scaling are derived at scoring time by devotionderive.py.
"""
from dataModel import Constellation, Star
from ability import Ability

bat = Constellation('Bat', '1e', '2c 3e')
bat.id = 'bat'
bat_0 = Star(bat, [], {"bleed %":15, "vitality %":15})
bat_1 = Star(bat, bat_0, {"offense":15, "vitality decay %":30})
bat_2 = Star(bat, bat_1, {"bleed %":50, "vitality %":24})
bat_3 = Star(bat, bat_2, {"defense":10, "lifesteal %":3, "vitality":6})
bat_4 = Star(bat, bat_3, {})
bat_4.addAbility(Ability('Twin Fangs', {"chance":0.2, "projectiles":2, "recharge":0.6, "skillClass":'Skill_AttackProjectileBurst', "trigger":'attack', "type":'attack'}, {"lifesteal %":40, "triggered pierce":165, "triggered vitality":174.5, "weapon damage %":22}))

akeronsScorpion = Constellation("Akeron's Scorpion", '1e', '5e')
akeronsScorpion.id = 'akeronsScorpion'
akeronsScorpion_0 = Star(akeronsScorpion, [], {"offense":12})
akeronsScorpion_1 = Star(akeronsScorpion, akeronsScorpion_0, {"acid %":15, "physique":15, "poison %":30})
akeronsScorpion_2 = Star(akeronsScorpion, akeronsScorpion_1, {"acid %":24, "offense":18})
akeronsScorpion_3 = Star(akeronsScorpion, akeronsScorpion_2, {"poison %":50, "poison duration":30})
akeronsScorpion_4 = Star(akeronsScorpion, akeronsScorpion_3, {})
akeronsScorpion_4.addAbility(Ability('Scorpion Sting', {"chance":0.25, "projectiles":6, "radius":0.1, "recharge":1.5, "skillClass":'Skill_AttackProjectileRing', "trigger":'attack', "type":'attack'}, {"triggered poison":[225, 5], "weapon damage %":40}))

raven = Constellation('Raven', '1e', '5e')
raven.id = 'raven'
raven_0 = Star(raven, [], {"pet all damage %":15, "spirit":15})
raven_1 = Star(raven, raven_0, {"energy/s":1.5, "offense":10})
raven_2 = Star(raven, raven_1, {"offense %":3, "pet all damage %":60, "pet offense %":5})
raven_3 = Star(raven, raven_2, {"offense":15, "pet lightning %":80})

hammer = Constellation('Hammer', '1a', '4a')
hammer.id = 'hammer'
hammer_0 = Star(hammer, [], {"armor":20, "physical %":15})
hammer_1 = Star(hammer, hammer_0, {"defense":15, "internal %":30, "internal duration":30})
hammer_2 = Star(hammer, hammer_1, {"armor %":8, "internal %":60, "physical %":24})

anvil = Constellation('Anvil', '1a', '5a')
anvil.id = 'anvil'
anvil_0 = Star(anvil, [], {"defense":15})
anvil_1 = Star(anvil, anvil_0, {"physique":20})
anvil_2 = Star(anvil, anvil_1, {"armor":45, "armor absorb":3})
anvil_3 = Star(anvil, anvil_2, {"block %":5, "defense":15, "internal":[12, 5], "offense":10})
anvil_4 = Star(anvil, anvil_3, {})
anvil_4.addAbility(Ability("Targo's Hammer", {"chance":0.5, "projectiles":10, "radius":0.25, "recharge":0.1, "skillClass":'Skill_AttackProjectileOrbiting', "trigger":'block', "type":'attack'}, {"triggered internal":[225, 2], "triggered physical":203, "weapon damage %":45}))

shepherdsCrook = Constellation("Shepherd's Crook", '1a', '5a')
shepherdsCrook.id = 'shepherdsCrook'
shepherdsCrook_0 = Star(shepherdsCrook, [], {"health":40, "pet health %":8})
shepherdsCrook_1 = Star(shepherdsCrook, shepherdsCrook_0, {"cunning":15, "health":40})
shepherdsCrook_2 = Star(shepherdsCrook, shepherdsCrook_1, {"elemental resist":10, "pet elemental resist":15})
shepherdsCrook_3 = Star(shepherdsCrook, shepherdsCrook_2, {"health %":3, "pet defense %":5, "pet health %":8})
shepherdsCrook_4 = Star(shepherdsCrook, shepherdsCrook_3, {})
shepherdsCrook_4.addAbility(Ability("Shepherd's Call", {"activeDuration":4, "chance":0.25, "recharge":6, "skillClass":'Skill_BuffSelfDuration', "trigger":'attack', "type":'buff'}, {"offense":85}))

sailorsGuide = Constellation("Sailor's Guide", '1p', '5p')
sailorsGuide.id = 'sailorsGuide'
sailorsGuide_0 = Star(sailorsGuide, [], {"defense":8, "physique":15})
sailorsGuide_1 = Star(sailorsGuide, sailorsGuide_0, {"freeze resist":18, "slow resist":18})
sailorsGuide_2 = Star(sailorsGuide, sailorsGuide_1, {"move speed":10, "physique":15})
sailorsGuide_3 = Star(sailorsGuide, sailorsGuide_2, {"elemental resist":15, "physical resist":3})

assassinsBlade = Constellation("Assassin's Blade", '1o', '3a 2o')
assassinsBlade.id = 'assassinsBlade'
assassinsBlade_0 = Star(assassinsBlade, [], {"physical %":15, "pierce %":15})
assassinsBlade_1 = Star(assassinsBlade, assassinsBlade_0, {"defense":12})
assassinsBlade_2 = Star(assassinsBlade, assassinsBlade_1, {"physical %":24, "pierce %":24})
assassinsBlade_3 = Star(assassinsBlade, assassinsBlade_2, {"offense":18})
assassinsBlade_4 = Star(assassinsBlade, assassinsBlade_3, {})

eyeofDreeg = Constellation('Eye of Dreeg', '1e', '3e 3a')
eyeofDreeg.id = 'eyeofDreeg'
eyeofDreeg_0 = Star(eyeofDreeg, [], {"acid %":15, "poison %":15})
eyeofDreeg_1 = Star(eyeofDreeg, eyeofDreeg_0, {"defense":16, "offense":16})
eyeofDreeg_2 = Star(eyeofDreeg, eyeofDreeg_1, {"chaos %":20, "poison %":15})
eyeofDreeg_3 = Star(eyeofDreeg, eyeofDreeg_2, {"energy/s":1, "poison %":30, "vitality resist":8})
eyeofDreeg_4 = Star(eyeofDreeg, eyeofDreeg_3, {})
eyeofDreeg_4.addAbility(Ability("Guardian's Gaze", {"chance":0.15, "projectiles":8, "radius":0.25, "recharge":0.5, "skillClass":'Skill_AttackProjectileOrbiting', "trigger":'attack', "type":'attack'}, {"lifesteal %":15, "triggered acid":83, "triggered chaos":193, "triggered poison":[190, 2], "weapon damage %":15}))

falcon = Constellation('Falcon', '1a', '3e 3a')
falcon.id = 'falcon'
falcon_0 = Star(falcon, [], {"bleed %":15, "physical %":15})
falcon_1 = Star(falcon, falcon_0, {"health":60, "offense":15})
falcon_2 = Star(falcon, falcon_1, {"cunning":20})
falcon_3 = Star(falcon, falcon_2, {"bleed %":50, "physical %":24})
falcon_4 = Star(falcon, falcon_3, {})
falcon_4.addAbility(Ability('Falcon Swoop', {"chance":0.15, "projectiles":6, "radius":0.1, "recharge":2, "skillClass":'Skill_AttackProjectileBurst', "trigger":'attack', "type":'attack'}, {"triggered bleed":[225, 3], "triggered physical":116, "weapon damage %":24}))

attakSeru = Constellation('AttakSeru', '16a 14e', '')
attakSeru.id = 'attakSeru'
attakSeru_0 = Star(attakSeru, [], {"aether %":80, "defense":25})
attakSeru_1 = Star(attakSeru, attakSeru_0, {"defense":25, "elemental %":80})
attakSeru_2 = Star(attakSeru, attakSeru_1, {"bleed resist":25, "health":300, "pierce resist":25})
attakSeru_3 = Star(attakSeru, attakSeru_2, {"armor":100, "defense %":6, "offense %":4})
attakSeru_4 = Star(attakSeru, attakSeru_3, {"aether %":100, "elemental":16, "elemental %":100})
attakSeru_5 = Star(attakSeru, attakSeru_4, {})
attakSeru_5.addAbility(Ability('Arcane Currents', {"chance":0.25, "recharge":0.7, "skillClass":'Skill_TargetedSpawnPet', "trigger":'attack', "type":'summon'}, {}))

rattosh = Constellation('Rattosh', '10e 6c 6o', '')
rattosh.id = 'rattosh'
rattosh_0 = Star(rattosh, [], {"health":350, "offense":30})
rattosh_1 = Star(rattosh, rattosh_0, {"aether %":80, "vitality %":80})
rattosh_2 = Star(rattosh, rattosh_1, {"defense":45, "offense":45, "vitality decay %":150, "vitality decay duration":50})
rattosh_3 = Star(rattosh, rattosh_2, {"aether %":100, "vitality %":100, "vitality decay":[18, 3]})
rattosh_4 = Star(rattosh, rattosh_3, {"bleed resist":15, "physical resist":5, "pierce resist":15, "vitality":10})
rattosh_5 = Star(rattosh, rattosh_4, {})

sandclaw = Constellation('Sandclaw', '1a', '3a 2c')
sandclaw.id = 'sandclaw'
sandclaw_0 = Star(sandclaw, [], {"cunning":15, "health/s":8, "pet all damage %":20})
sandclaw_1 = Star(sandclaw, sandclaw_0, {"elemental resist":10, "pet bleed %":30, "pet elemental resist":15})
sandclaw_2 = Star(sandclaw, sandclaw_1, {"bleed %":20, "bleed duration":20, "pet all damage %":60})
sandclaw_3 = Star(sandclaw, sandclaw_2, {"bleed %":50, "pet bleed %":50, "physical resist":3})

mantis = Constellation('Mantis', '1c', '3a 2c')
mantis.id = 'mantis'
mantis_0 = Star(mantis, [], {"armor":20, "pierce %":15})
mantis_1 = Star(mantis, mantis_0, {"defense":10, "elemental resist":10})
mantis_2 = Star(mantis, mantis_1, {"energy/s":1, "health":80})
mantis_3 = Star(mantis, mantis_2, {"physical resist":3, "pierce":7, "pierce %":24})

beetle = Constellation('Beetle', '1p', '3p 2o')
beetle.id = 'beetle'
beetle_0 = Star(beetle, [], {"armor":20, "physique":15})
beetle_1 = Star(beetle, beetle_0, {"blocked damage %":16, "shield recovery":5})
beetle_2 = Star(beetle, beetle_1, {"armor %":8, "bleed resist":15})
beetle_3 = Star(beetle, beetle_2, {"acid retaliation":40, "blocked damage %":16, "shield recovery":10, "stun resist":15})

lotus = Constellation('Lotus', '1o', '3e 2o')
lotus.id = 'lotus'
lotus_0 = Star(lotus, [], {"energy":100, "health":30})
lotus_1 = Star(lotus, lotus_0, {"energy/s":1, "energy/s %":15})
lotus_2 = Star(lotus, lotus_1, {"energy %":4, "health":80, "vitality resist":8})
lotus_3 = Star(lotus, lotus_2, {"healing %":20, "health/s %":20, "reflected damage reduction":25})

ulzaad = Constellation('Ulzaad', '8a 6p', '2e 2a')
ulzaad.id = 'ulzaad'
ulzaad_0 = Star(ulzaad, [], {"physical %":40})
ulzaad_1 = Star(ulzaad, ulzaad_0, {"acid resist":15, "defense":25})
ulzaad_2 = Star(ulzaad, ulzaad_1, {"internal %":50, "physical":10.5, "physical %":50})
ulzaad_3 = Star(ulzaad, ulzaad_2, {})
ulzaad_3.addAbility(Ability('Ulzaad Decree', {"activeDuration":10, "chance":0.2, "recharge":22, "skillClass":'Skill_BuffSelfDuration', "trigger":'attack', "type":'buff'}, {"armor":190, "internal %":200, "physical %":200, "physical retaliation":327.5, "pierce %":200, "triggered physical":43.5}))
ulzaad_4 = Star(ulzaad, ulzaad_3, {"aether resist":10, "defense %":1, "health":250})
ulzaad_5 = Star(ulzaad, ulzaad_4, {"chaos resist":10, "defense %":1, "health":250})

hyrian = Constellation('Hyrian', '8e 6a', '2a 2p')
hyrian.id = 'hyrian'
hyrian_0 = Star(hyrian, [], {"elemental %":40, "retaliation %":40})
hyrian_1 = Star(hyrian, hyrian_0, {"blocked damage %":30, "health":300, "pierce resist":10})
hyrian_2 = Star(hyrian, hyrian_1, {"armor %":9, "healing %":10, "health":300})
hyrian_3 = Star(hyrian, hyrian_2, {"armor %":9, "burn %":80, "electrocute %":80, "elemental %":50, "elemental resist":15, "frostburn %":80})
hyrian_4 = Star(hyrian, hyrian_3, {})
hyrian_4.addAbility(Ability('Hyrian Glare', {"chance":0.3, "recharge":2, "skillClass":'Skill_AttackWave', "trigger":'hit', "type":'attack', "waveDistance":10, "waveEndWidth":3, "waveStartWidth":3}, {"triggered burn":[95, 2], "triggered electrocute":[95, 2], "triggered elemental":280, "triggered frostburn":[95, 2], "weapon damage %":85}))
hyrian_5 = Star(hyrian, hyrian_4, {"blocked damage %":40, "elemental":16, "retaliation %":50})

korvaak = Constellation('Korvaak', '18p 10e', '')
korvaak.id = 'korvaak'
korvaak_0 = Star(korvaak, [], {"all damage %":30, "health":300, "pet all damage %":40})
korvaak_1 = Star(korvaak, korvaak_0, {"energy/s":2, "health %":8, "pet health %":12})
korvaak_2 = Star(korvaak, korvaak_1, {"chaos resist":20, "pet chaos resist":20})
korvaak_3 = Star(korvaak, korvaak_2, {"all damage %":50, "offense %":5, "pet all damage %":80, "pet offense %":5})
korvaak_4 = Star(korvaak, korvaak_3, {})
korvaak_4.addAbility(Ability("Korvaak's Eye", {"chance":1, "projectiles":6, "radius":1, "recharge":1.5, "skillClass":'Skill_AttackProjectileRing', "trigger":'critical', "type":'attack'}, {"weapon damage %":18}))
korvaak_5 = Star(korvaak, korvaak_4, {"all damage %":50, "crit damage":5, "pet all damage %":80, "pet crit damage":5})

azrakaa = Constellation('Azrakaa', '12a 8p 6o', '')
azrakaa.id = 'azrakaa'
azrakaa_0 = Star(azrakaa, [], {"physical %":80, "pierce %":80})
azrakaa_1 = Star(azrakaa, azrakaa_0, {"armor":90, "health":300})
azrakaa_2 = Star(azrakaa, azrakaa_1, {"defense":50, "health":350, "move speed":6})
azrakaa_3 = Star(azrakaa, azrakaa_2, {"physical %":120, "pierce":14, "pierce %":120})
azrakaa_4 = Star(azrakaa, azrakaa_3, {})
azrakaa_4.addAbility(Ability('Shifting Sands', {"activeDuration":1, "chance":0.2, "projectiles":5, "radius":2, "recharge":0.5, "skillClass":'Skill_AttackProjectile', "trigger":'attack', "type":'attack'}, {"crit damage":40, "triggered physical":205, "triggered pierce":335, "weapon damage %":30}))
azrakaa_5 = Star(azrakaa, azrakaa_4, {"attack speed":6, "cast speed":6, "defense":50})

eel = Constellation('Eel', '1p', '5p')
eel.id = 'eel'
eel_0 = Star(eel, [], {"avoid melee":2, "defense":12})
eel_1 = Star(eel, eel_0, {"avoid ranged":2, "defense":15})
eel_2 = Star(eel, eel_1, {"defense":20, "move speed":6, "pierce resist":10})

yugol = Constellation('Yugol', '20e 7c', '')
yugol.id = 'yugol'
yugol_0 = Star(yugol, [], {"cold %":80, "offense":25})
yugol_1 = Star(yugol, yugol_0, {"acid %":80, "health":300, "offense":25})
yugol_2 = Star(yugol, yugol_1, {"petrify resist":30, "reflected damage reduction":10, "vitality resist":25})
yugol_3 = Star(yugol, yugol_2, {"acid %":100, "cold %":100, "spirit %":4})
yugol_4 = Star(yugol, yugol_3, {"acid":8, "cold":8, "life leech resist":40, "lifesteal %":8})
yugol_5 = Star(yugol, yugol_4, {})
yugol_5.addAbility(Ability('Black Blood of Yugol', {"chance":0.3, "recharge":0.8, "skillClass":'Skill_TargetedSpawnPet', "trigger":'hit', "type":'summon'}, {}))

owl = Constellation('Owl', '1a', '5a')
owl.id = 'owl'
owl_0 = Star(owl, [], {"cunning":15, "spirit":15})
owl_1 = Star(owl, owl_0, {"elemental resist":8})
owl_2 = Star(owl, owl_1, {"bleed %":50, "bleed duration":50, "burn %":50, "burn duration":50, "electrocute %":50, "electrocute duration":50, "frostburn %":50, "frostburn duration":50, "internal %":50, "internal duration":50, "poison %":50, "poison duration":50, "vitality decay %":50, "vitality decay duration":50})
owl_3 = Star(owl, owl_2, {"all damage %":30, "defense":15, "reflected damage reduction":15})

viper = Constellation('Viper', '1c', '3p 2c')
viper.id = 'viper'
viper_0 = Star(viper, [], {"cunning":15, "spirit":15})
viper_1 = Star(viper, viper_0, {"energy absorb":10})
viper_2 = Star(viper, viper_1, {"vitality resist":10})
viper_3 = Star(viper, viper_2, {"offense %":3, "reduce elemental resist":20})

gallows = Constellation('Gallows', '1p', '5p')
gallows.id = 'gallows'
gallows_0 = Star(gallows, [], {"chaos %":15, "vitality %":15})
gallows_1 = Star(gallows, gallows_0, {"bleed resist":10, "health %":3})
gallows_2 = Star(gallows, gallows_1, {"health %":3, "vitality resist":10})
gallows_3 = Star(gallows, gallows_2, {"chaos %":24, "vitality":8, "vitality %":24})

xP = Constellation('Crossroads Primordial', '', '1p')
xP.id = 'xP'
xP_0 = Star(xP, [], {"defense":18})

emptyThrone = Constellation('Empty Throne', '1a', '5a')
emptyThrone.id = 'emptyThrone'
emptyThrone_0 = Star(emptyThrone, [], {"defense":12, "slow resist":10})
emptyThrone_1 = Star(emptyThrone, emptyThrone_0, {"defense":20, "pet pierce resist":15, "pierce resist":8})
emptyThrone_2 = Star(emptyThrone, emptyThrone_1, {"aether resist":10, "freeze resist":25, "pet aether resist":15, "pet freeze resist":25})
emptyThrone_3 = Star(emptyThrone, emptyThrone_2, {"chaos resist":10, "pet chaos resist":15, "pet stun resist":25, "stun resist":25})

rat = Constellation('Rat', '1c', '3e 2c')
rat.id = 'rat'
rat_0 = Star(rat, [], {"cunning":15, "spirit":15})
rat_1 = Star(rat, rat_0, {"acid retaliation":20, "poison":[8, 5], "poison %":30})
rat_2 = Star(rat, rat_1, {"acid resist":10, "acid retaliation":30, "cunning":20, "spirit":20})
rat_3 = Star(rat, rat_2, {"poison":[12, 5], "poison %":60, "poison duration":30, "retaliation %":40})

tsunami = Constellation('Tsunami', '1p', '5p')
tsunami.id = 'tsunami'
tsunami_0 = Star(tsunami, [], {"cold %":15, "lightning %":15})
tsunami_1 = Star(tsunami, tsunami_0, {"defense":20, "spirit":15})
tsunami_2 = Star(tsunami, tsunami_1, {"electrocute %":50, "frostburn %":50, "physique":15})
tsunami_3 = Star(tsunami, tsunami_2, {"cold %":24, "lightning %":24})
tsunami_4 = Star(tsunami, tsunami_3, {})
tsunami_4.addAbility(Ability('Tsunami', {"chance":0.35, "recharge":0.7, "skillClass":'Skill_AttackWave', "trigger":'attack', "type":'attack', "waveDistance":12, "waveEndWidth":3, "waveStartWidth":3}, {"triggered cold":197.5, "triggered frostburn":[225, 2], "triggered lightning":106, "weapon damage %":45}))

imp = Constellation('Imp', '1p', '3p 3e')
imp.id = 'imp'
imp_0 = Star(imp, [], {"aether %":15, "fire %":15})
imp_1 = Star(imp, imp_0, {"defense":10, "spirit":15})
imp_2 = Star(imp, imp_1, {"aether resist":8, "physique":15})
imp_3 = Star(imp, imp_2, {"aether %":24, "fire %":24})
imp_4 = Star(imp, imp_3, {})
imp_4.addAbility(Ability('Aetherfire', {"activeDuration":3, "chance":0.15, "projectiles":8, "radius":2.5, "skillClass":'Skill_AttackProjectileAreaEffect', "trigger":'attack', "type":'attack'}, {"triggered aether":190, "triggered fire":140}))

fiend = Constellation('Fiend', '1c', '3e 2c')
fiend.id = 'fiend'
fiend_0 = Star(fiend, [], {"chaos %":15, "fire %":15})
fiend_1 = Star(fiend, fiend_0, {"pet all damage %":30, "spirit":15})
fiend_2 = Star(fiend, fiend_1, {"chaos resist":8})
fiend_3 = Star(fiend, fiend_2, {"chaos %":24, "fire %":24, "pet fire %":80})
fiend_4 = Star(fiend, fiend_3, {})
fiend_4.addAbility(Ability('Flame Torrent', {"chance":0.25, "projectiles":4, "radius":0.5, "recharge":0.5, "skillClass":'Skill_AttackProjectileOrbiting', "trigger":'attack', "type":'attack'}, {"triggered burn":[190, 3], "triggered chaos":126, "triggered fire":178, "weapon damage %":20}))

bull = Constellation('Bull', '1p', '2o 3p')
bull.id = 'bull'
bull_0 = Star(bull, [], {"defense":8, "physique":15})
bull_1 = Star(bull, bull_0, {"internal %":30, "internal duration":30, "move speed":3})
bull_2 = Star(bull, bull_1, {"armor":30, "physique":15})
bull_3 = Star(bull, bull_2, {"defense":10, "internal":[12, 5], "internal %":50})
bull_4 = Star(bull, bull_3, {})
bull_4.addAbility(Ability('Bull Rush', {"chance":0.25, "radius":3.5, "recharge":0.4, "skillClass":'Skill_AttackRadius', "trigger":'attack', "type":'attack'}, {"triggered internal":[225, 2], "triggered physical":172.5, "weapon damage %":32}))

wraith = Constellation('Wraith', '1p', '3a 3p')
wraith.id = 'wraith'
wraith_0 = Star(wraith, [], {"aether %":15, "lightning %":15})
wraith_1 = Star(wraith, wraith_0, {"aether resist":8, "retaliation %":30, "spirit":15})
wraith_2 = Star(wraith, wraith_1, {"energy absorb":15, "lightning retaliation":55, "offense":24})
wraith_3 = Star(wraith, wraith_2, {"aether %":24, "lightning %":24, "physical resist":3})

harpy = Constellation('Harpy', '1a', '5a')
harpy.id = 'harpy'
harpy_0 = Star(harpy, [], {"cold %":15, "pierce %":15})
harpy_1 = Star(harpy, harpy_0, {"cunning":15, "energy/s":1})
harpy_2 = Star(harpy, harpy_1, {"bleed resist":10, "offense":24})
harpy_3 = Star(harpy, harpy_2, {"cold %":24, "crit damage":5, "pierce":8, "pierce %":24})

fox = Constellation('Fox', '1e', '5e')
fox.id = 'fox'
fox_0 = Star(fox, [], {"cunning":15, "spirit":15})
fox_1 = Star(fox, fox_0, {"bleed":[8, 3], "bleed %":30})
fox_2 = Star(fox, fox_1, {"bleed resist":8, "cunning":25})
fox_3 = Star(fox, fox_2, {"bleed":[12, 3], "bleed %":60, "health/s":10, "lifesteal %":6})

ghoul = Constellation('Ghoul', '1c', '3c')
ghoul.id = 'ghoul'
ghoul_0 = Star(ghoul, [], {"defense":8, "physique":15})
ghoul_1 = Star(ghoul, ghoul_0, {"health %":3, "health/s":16})
ghoul_2 = Star(ghoul, ghoul_1, {"defense":15, "physique":15, "spirit":15})
ghoul_3 = Star(ghoul, ghoul_2, {"health/s %":30, "lifesteal %":5})
ghoul_4 = Star(ghoul, ghoul_3, {})

dryad = Constellation('Dryad', '1o', '3o')
dryad.id = 'dryad'
dryad_0 = Star(dryad, [], {"acid resist":10, "energy":200, "physique":15})
dryad_1 = Star(dryad, dryad_0, {"energy/s":1, "health":80})
dryad_2 = Star(dryad, dryad_1, {"move speed":3, "slow resist":15})
dryad_3 = Star(dryad, dryad_2, {"physical resist":3, "spirit %":5})
dryad_4 = Star(dryad, dryad_3, {})
dryad_4.addAbility(Ability("Dryad's Blessing", {"activeDuration":10, "chance":0.33, "recharge":2.2, "skillClass":'Skill_BuffSelfDuration', "trigger":'attack', "type":'buff'}, {"armor":70}))

hawk = Constellation('Hawk', '1e', '3e')
hawk.id = 'hawk'
hawk_0 = Star(hawk, [], {"offense":15})
hawk_1 = Star(hawk, hawk_0, {"crit damage":5, "pet crit damage":5})
hawk_2 = Star(hawk, hawk_1, {"offense %":3, "pet offense %":3})

wolverine = Constellation('Wolverine', '1a', '6a')
wolverine.id = 'wolverine'
wolverine_0 = Star(wolverine, [], {"defense":15, "pet pierce resist":10})
wolverine_1 = Star(wolverine, wolverine_0, {"armor":30, "pet vitality resist":15, "retaliation %":30})
wolverine_2 = Star(wolverine, wolverine_1, {"defense":25, "pet acid resist":15})
wolverine_3 = Star(wolverine, wolverine_2, {"armor":30, "move speed":3, "pet bleed resist":25, "retaliation %":50})
wolverine_4 = Star(wolverine, wolverine_3, {"defense %":4, "pet defense %":5})

turtle = Constellation('Turtle', '1o', '3p 2o')
turtle.id = 'turtle'
turtle_0 = Star(turtle, [], {"armor":20, "defense":12})
turtle_1 = Star(turtle, turtle_0, {"armor":20, "defense":15})
turtle_2 = Star(turtle, turtle_1, {"armor":40, "defense":15})
turtle_3 = Star(turtle, turtle_2, {"armor %":8, "defense":10, "health %":4})
turtle_4 = Star(turtle, turtle_3, {})

panther = Constellation('Panther', '1o', '3p 2o')
panther.id = 'panther'
panther_0 = Star(panther, [], {"offense":12, "pet offense %":2})
panther_1 = Star(panther, panther_0, {"cunning":15, "pet all damage %":20, "spirit":15})
panther_2 = Star(panther, panther_1, {"energy/s %":15, "offense":20, "pet offense %":3})
panther_3 = Star(panther, panther_2, {"crit damage":5, "offense":25, "pet all damage %":30, "pet crit damage":5})

crane = Constellation('Crane', '1o', '5o')
crane.id = 'crane'
crane_0 = Star(crane, [], {"physique":15, "spirit":15})
crane_1 = Star(crane, crane_0, {"acid resist":12, "pet acid resist":20})
crane_2 = Star(crane, crane_1, {"all damage %":15})
crane_3 = Star(crane, crane_2, {"pet vitality resist":20, "vitality resist":12})
crane_4 = Star(crane, crane_3, {"bleed resist":16, "elemental resist":16, "reflected damage reduction":22})

vulture = Constellation('Vulture', '1c', '5c')
vulture.id = 'vulture'
vulture_0 = Star(vulture, [], {"cunning":15, "spirit":15})
vulture_1 = Star(vulture, vulture_0, {"bleed resist":15, "life leech resist":30, "offense":15})
vulture_2 = Star(vulture, vulture_1, {"energy":200, "health":80, "offense":15})
vulture_3 = Star(vulture, vulture_2, {"cunning %":5, "offense":15, "spirit %":5})
vulture_4 = Star(vulture, vulture_3, {"chaos resist":8, "offense":15, "vitality resist":15})

hound = Constellation('Hound', '1p', '4p')
hound.id = 'hound'
hound_0 = Star(hound, [], {"pet health %":8, "physique":15})
hound_1 = Star(hound, hound_0, {"armor %":6, "retaliation %":30})
hound_2 = Star(hound, hound_1, {"armor %":9, "pet health %":12, "pet stun resist":15, "physique":20, "retaliation %":40})

spider = Constellation('Spider', '1e', '6e')
spider.id = 'spider'
spider_0 = Star(spider, [], {"cunning":15, "spirit":15})
spider_1 = Star(spider, spider_0, {"offense":20, "spirit %":3})
spider_2 = Star(spider, spider_1, {"cast speed":5, "offense":20})
spider_3 = Star(spider, spider_2, {"attack speed":5, "defense":20})
spider_4 = Star(spider, spider_3, {"cunning %":3, "defense":20})

lizard = Constellation('Lizard', '1p', '4p')
lizard.id = 'lizard'
lizard_0 = Star(lizard, [], {"constitution %":15, "health/s":8})
lizard_1 = Star(lizard, lizard_0, {"health":50, "health/s":16, "move speed":3})
lizard_2 = Star(lizard, lizard_1, {"healing %":6, "health":50, "health/s %":40})

rhowansCrown = Constellation("Rhowan's Crown", '6e 4a', '1e 1a')
rhowansCrown.id = 'rhowansCrown'
rhowansCrown_0 = Star(rhowansCrown, [], {"elemental":7.5, "elemental %":30})
rhowansCrown_1 = Star(rhowansCrown, rhowansCrown_0, {"defense":20, "pet elemental %":60, "spirit":20})
rhowansCrown_2 = Star(rhowansCrown, rhowansCrown_1, {})
rhowansCrown_2.addAbility(Ability('Elemental Storm', {"activeDuration":5, "chance":0.25, "radius":3.5, "recharge":1.5, "skillClass":'Skill_AttackProjectileAreaEffect', "trigger":'attack', "type":'attack'}, {"duration":{"reduce elemental resist":32}, "triggered burn":[98, 2], "triggered electrocute":[98, 2], "triggered elemental":132, "triggered frostburn":[98, 2]}))
rhowansCrown_3 = Star(rhowansCrown, rhowansCrown_2, {"elemental resist":18, "offense":20, "pet elemental resist":18})
rhowansCrown_4 = Star(rhowansCrown, rhowansCrown_3, {"burn %":60, "chaos resist":8, "electrocute %":60, "elemental %":40, "frostburn %":60})

scalesofUlcama = Constellation('Scales of Ulcama', '8o', '2o')
scalesofUlcama.id = 'scalesofUlcama'
scalesofUlcama_0 = Star(scalesofUlcama, [], {"energy":300, "health":250})
scalesofUlcama_1 = Star(scalesofUlcama, scalesofUlcama_0, {"health %":6, "move speed":6})
scalesofUlcama_2 = Star(scalesofUlcama, scalesofUlcama_1, {"energy/s":2.5, "energy/s %":33})
scalesofUlcama_3 = Star(scalesofUlcama, scalesofUlcama_2, {"health/s":30, "health/s %":33, "lifesteal %":5})
scalesofUlcama_4 = Star(scalesofUlcama, scalesofUlcama_3, {"defense":45, "physique":20})
scalesofUlcama_5 = Star(scalesofUlcama, scalesofUlcama_4, {})
scalesofUlcama_5.addAbility(Ability('Tip the Scales', {"chance":0.33, "recharge":1, "skillClass":'Skill_AttackSpell', "trigger":'hit', "type":'attack'}, {"duration":{"reduce resist":20}, "lifesteal %":132, "triggered vitality":310, "weapon damage %":33}))

wendigo = Constellation('Wendigo', '6p 4c', '2c')
wendigo.id = 'wendigo'
wendigo_0 = Star(wendigo, [], {"vitality %":40, "vitality decay %":40})
wendigo_1 = Star(wendigo, wendigo_0, {"health":300, "spirit":20})
wendigo_2 = Star(wendigo, wendigo_1, {"defense":40, "total speed":5, "vitality decay %":40})
wendigo_3 = Star(wendigo, wendigo_2, {"health %":6})
wendigo_4 = Star(wendigo, wendigo_3, {"vitality %":50, "vitality decay":[12, 3], "vitality decay %":50})
wendigo_5 = Star(wendigo, wendigo_4, {})

huntress = Constellation('Huntress', '4a 4e 3c', '1e 1a')
huntress.id = 'huntress'
huntress_0 = Star(huntress, [], {"health":200, "offense":15})
huntress_1 = Star(huntress, huntress_0, {"cunning":20, "pierce %":50})
huntress_2 = Star(huntress, huntress_1, {"bleed %":60, "offense":25})
huntress_3 = Star(huntress, huntress_2, {"armor":60, "pet all damage %":40, "pet health %":12, "pierce resist":8})
huntress_4 = Star(huntress, huntress_3, {"healing %":12, "health/s":25, "offense %":3, "pet offense %":5})
huntress_5 = Star(huntress, huntress_4, {"bleed":[15, 3], "bleed %":50, "bleed duration":20, "pet bleed %":80})
huntress_6 = Star(huntress, huntress_5, {})

direBear = Constellation('Dire Bear', '5a 5p', '1p 1a')
direBear.id = 'direBear'
direBear_0 = Star(direBear, [], {"physical %":40})
direBear_1 = Star(direBear, direBear_0, {"cunning":20, "defense":15, "physique":20})
direBear_2 = Star(direBear, direBear_1, {"armor":60, "physical %":50})
direBear_3 = Star(direBear, direBear_2, {"freeze resist":15, "health %":6, "stun resist":15})
direBear_4 = Star(direBear, direBear_3, {"armor":80, "lifesteal %":4})
direBear_5 = Star(direBear, direBear_4, {})

assassin = Constellation('Assassin', '6a 4o', '1a 1o')
assassin.id = 'assassin'
assassin_0 = Star(assassin, [], {"pierce %":40})
assassin_1 = Star(assassin, assassin_0, {"armor":60, "cunning":20})
assassin_2 = Star(assassin, assassin_1, {"avoid melee":4, "defense":10, "offense":18})
assassin_3 = Star(assassin, assassin_2, {"bleed resist":10, "cunning %":5, "pierce %":50})
assassin_4 = Star(assassin, assassin_3, {"acid resist":10, "defense":25})
assassin_5 = Star(assassin, assassin_4, {"pierce":12, "pierce %":50})
assassin_6 = Star(assassin, assassin_5, {})
assassin_6.addAbility(Ability('Blade Burst', {"chance":1, "projectiles":16, "recharge":1.8, "skillClass":'Skill_AttackProjectileRing', "trigger":'critical', "type":'attack'}, {"triggered pierce":290, "weapon damage %":25}))

magi = Constellation('Magi', '10e', '3e')
magi.id = 'magi'
magi_0 = Star(magi, [], {"fire %":40})
magi_1 = Star(magi, magi_0, {"defense":15, "elemental resist":8})
magi_2 = Star(magi, magi_1, {"defense":20, "energy/s":1.5, "trap resist":15})
magi_3 = Star(magi, magi_2, {"attack speed":5, "burn %":50, "cast speed":5, "physique":15})
magi_4 = Star(magi, magi_3, {"fire":12.5, "fire %":40, "freeze resist":15})
magi_5 = Star(magi, magi_4, {"burn":[12, 3], "burn %":50, "burn duration":30})
magi_6 = Star(magi, magi_5, {})
magi_6.addAbility(Ability('Volcano', {"activeDuration":5, "chance":0.15, "radius":1, "recharge":1.8, "skillClass":'Skill_AttackProjectileAreaEffect', "trigger":'attack', "type":'attack'}, {"triggered burn":[195, 2], "triggered fire":179}))

autumnBoar = Constellation('Autumn Boar', '4p 4a 3o', '3a')
autumnBoar.id = 'autumnBoar'
autumnBoar_0 = Star(autumnBoar, [], {"cunning":20, "physique":20, "retaliation %":30})
autumnBoar_1 = Star(autumnBoar, autumnBoar_0, {"physique":15, "pierce resist":15, "slow resist":15})
autumnBoar_2 = Star(autumnBoar, autumnBoar_1, {"physique %":5, "retaliation %":30})
autumnBoar_3 = Star(autumnBoar, autumnBoar_2, {"block %":5, "defense":25, "move speed":5})
autumnBoar_4 = Star(autumnBoar, autumnBoar_3, {"defense":30, "retaliation %":40})
autumnBoar_5 = Star(autumnBoar, autumnBoar_4, {"physical resist":4, "physical retaliation":150, "reflected damage reduction":15, "shield recovery":10})
autumnBoar_6 = Star(autumnBoar, autumnBoar_5, {})
autumnBoar_6.addAbility(Ability('Trample', {"chance":0.5, "radius":0.1, "recharge":0.3, "skillClass":'Skill_AttackProjectile', "trigger":'block', "type":'attack'}, {"triggered internal":[285, 2], "weapon damage %":55}))

widow = Constellation('Widow', '6e 4p', '3p')
widow.id = 'widow'
widow_0 = Star(widow, [], {"aether %":40})
widow_1 = Star(widow, widow_0, {"defense":10, "energy %":5, "offense":18})
widow_2 = Star(widow, widow_1, {"aether %":30, "physique":15, "spirit":15})
widow_3 = Star(widow, widow_2, {"aether resist":18, "vitality resist":8})
widow_4 = Star(widow, widow_3, {"aether %":50, "lightning %":50, "offense %":2})
widow_5 = Star(widow, widow_4, {})
widow_5.addAbility(Ability('Arcane Bomb', {"chance":0.25, "radius":1, "recharge":1, "skillClass":'Skill_TargetedSpawnPet', "trigger":'attack', "type":'summon'}, {}))

revenant = Constellation('Revenant', '8c', '1p 1c')
revenant.id = 'revenant'
revenant_0 = Star(revenant, [], {"energy absorb":15})
revenant_1 = Star(revenant, revenant_0, {"health %":6})
revenant_2 = Star(revenant, revenant_1, {"stun resist":20, "vitality resist":24})
revenant_3 = Star(revenant, revenant_2, {"health":250, "lifesteal %":6, "vitality %":60})
revenant_4 = Star(revenant, revenant_3, {"aether %":60, "attack speed":4, "cast speed":4})
revenant_5 = Star(revenant, revenant_4, {})
revenant_5.addAbility(Ability('Raise Skeleton', {"chance":0.2, "recharge":2, "skillClass":'Skill_TargetedSpawnPet', "trigger":'attack', "type":'summon'}, {}))

samaelsWitchblade = Constellation("Samael's Witchblade", '6e 4c', '1e 1c')
samaelsWitchblade.id = 'samaelsWitchblade'
samaelsWitchblade_0 = Star(samaelsWitchblade, [], {"chaos %":40})
samaelsWitchblade_1 = Star(samaelsWitchblade, samaelsWitchblade_0, {"offense":10, "physique":15, "spirit":15})
samaelsWitchblade_2 = Star(samaelsWitchblade, samaelsWitchblade_1, {"chaos %":30, "defense":15, "fire %":30})
samaelsWitchblade_3 = Star(samaelsWitchblade, samaelsWitchblade_2, {"chaos %":50, "defense":25, "fire %":50})
samaelsWitchblade_4 = Star(samaelsWitchblade, samaelsWitchblade_3, {})

bysmielsBond = Constellation("Bysmiel's Bond", '6e 4c', '3e')
bysmielsBond.id = 'bysmielsBond'
bysmielsBond_0 = Star(bysmielsBond, [], {"offense":15, "pet all damage %":30})
bysmielsBond_1 = Star(bysmielsBond, bysmielsBond_0, {"cast speed":5, "pet all damage %":50, "physique":15})
bysmielsBond_2 = Star(bysmielsBond, bysmielsBond_1, {"pet vitality resist":20, "vitality resist":15})
bysmielsBond_3 = Star(bysmielsBond, bysmielsBond_2, {"all damage %":30, "pet all damage %":50, "pet trap resist":20, "trap resist":20})
bysmielsBond_4 = Star(bysmielsBond, bysmielsBond_3, {})
bysmielsBond_4.addAbility(Ability("Bysmiel's Command", {"chance":0.2, "recharge":30, "skillClass":'Skill_TargetedSpawnPet', "trigger":'attack', "type":'summon'}, {}))

tempest = Constellation('Tempest', '5p 5a', '1e 1p')
tempest.id = 'tempest'
tempest_0 = Star(tempest, [], {"lightning %":40})
tempest_1 = Star(tempest, tempest_0, {"lightning":14, "physique":20})
tempest_2 = Star(tempest, tempest_1, {"electrocute %":50, "lightning %":50})
tempest_3 = Star(tempest, tempest_2, {"defense":25, "offense":25, "slow resist":10})
tempest_4 = Star(tempest, tempest_3, {"lightning %":250, "stun resist":15, "total speed":4})
tempest_5 = Star(tempest, tempest_4, {"electrocute %":50, "electrocute duration":50, "offense":20})
tempest_6 = Star(tempest, tempest_5, {})
tempest_6.addAbility(Ability('Reckless Tempest', {"activeDuration":6, "chance":1, "radius":8, "recharge":10, "skillClass":'Skill_BuffAttackRadiusLightning', "trigger":'critical', "type":'attack'}, {"triggered electrocute":[245, 2], "triggered lightning":204}))

targotheBuilder = Constellation('Targo the Builder', '6p 4o', '1o')
targotheBuilder.id = 'targotheBuilder'
targotheBuilder_0 = Star(targotheBuilder, [], {"defense":20, "retaliation %":30})
targotheBuilder_1 = Star(targotheBuilder, targotheBuilder_0, {"aether resist":8, "health %":6})
targotheBuilder_2 = Star(targotheBuilder, targotheBuilder_1, {"armor %":8, "physical retaliation":150})
targotheBuilder_3 = Star(targotheBuilder, targotheBuilder_2, {"chaos resist":8, "health %":6})
targotheBuilder_4 = Star(targotheBuilder, targotheBuilder_3, {"defense":35, "health":300, "retaliation %":60})
targotheBuilder_5 = Star(targotheBuilder, targotheBuilder_4, {"armor %":12, "blocked damage %":24})
targotheBuilder_6 = Star(targotheBuilder, targotheBuilder_5, {})
targotheBuilder_6.addAbility(Ability('Shield Wall', {"activeDuration":5, "chance":0.25, "recharge":8, "skillClass":'Skill_BuffSelfDuration', "trigger":'attack', "type":'buff'}, {"armor %":50, "blocked damage %":210, "physical retaliation":730}))

callerofTheFrost = Constellation('Caller of The Frost', '6p 4e', '1p 1e')
callerofTheFrost.id = 'callerofTheFrost'
callerofTheFrost_0 = Star(callerofTheFrost, [], {"cold %":40})
callerofTheFrost_1 = Star(callerofTheFrost, callerofTheFrost_0, {"defense":15, "health %":6})
callerofTheFrost_2 = Star(callerofTheFrost, callerofTheFrost_1, {"armor":80, "defense":30})
callerofTheFrost_3 = Star(callerofTheFrost, callerofTheFrost_2, {"armor":60, "cold %":50, "frostburn %":50})
callerofTheFrost_4 = Star(callerofTheFrost, callerofTheFrost_3, {"cold %":50, "frostburn":[12, 3], "frostburn %":100})
callerofTheFrost_5 = Star(callerofTheFrost, callerofTheFrost_4, {"frostburn %":50, "frostburn duration":50, "offense":25})
callerofTheFrost_6 = Star(callerofTheFrost, callerofTheFrost_5, {})
callerofTheFrost_6.addAbility(Ability('Blizzard', {"chance":1, "radius":6.5, "recharge":3.2, "skillClass":'Skill_AttackProjectileDrop', "trigger":'critical', "type":'attack'}, {"triggered cold":353.5, "triggered frostburn":[245, 2], "weapon damage %":16}))

pestilence = Constellation('Pestilence', '4e 4a 3c', '1e 1a')
pestilence.id = 'pestilence'
pestilence_0 = Star(pestilence, [], {"poison %":40, "vitality decay %":40})
pestilence_1 = Star(pestilence, pestilence_0, {"acid retaliation":60, "defense":20, "offense":20, "spirit":20})
pestilence_2 = Star(pestilence, pestilence_1, {})
pestilence_2.addAbility(Ability('Fetid pool', {"activeDuration":6, "chance":0.33, "radius":3, "recharge":2, "skillClass":'Skill_AttackProjectileAreaEffect', "trigger":'hit', "type":'attack'}, {"triggered vitality":370, "triggered vitality decay":[245, 2]}))
pestilence_3 = Star(pestilence, pestilence_2, {"offense %":4, "poison %":50, "retaliation %":60})
pestilence_4 = Star(pestilence, pestilence_3, {"acid retaliation":90, "offense":40, "vitality decay":[15, 3], "vitality decay %":60, "vitality decay duration":50})
pestilence_5 = Star(pestilence, pestilence_4, {"defense %":4, "poison %":50, "retaliation %":60})
pestilence_6 = Star(pestilence, pestilence_5, {"acid retaliation":90, "defense":40, "vitality decay":[15, 3], "vitality decay %":60, "vitality decay duration":50})

crab = Constellation('Crab', '6a 4o', '3a')
crab.id = 'crab'
crab_0 = Star(crab, [], {"constitution %":15, "physique":25})
crab_1 = Star(crab, crab_0, {"elemental %":50, "internal %":50, "physical %":50})
crab_2 = Star(crab, crab_1, {})
crab_2.addAbility(Ability('Arcane Barrier', {"chance":0.3, "recharge":3, "skillClass":'Skill_BuffSelfShield', "trigger":'hit', "type":'shield'}, {}))
crab_3 = Star(crab, crab_2, {"defense":40, "offense":40, "pierce resist":18})
crab_4 = Star(crab, crab_3, {"burn %":100, "electrocute %":100, "elemental":15, "elemental %":60, "elemental resist":15, "frostburn %":100})

manticore = Constellation('Manticore', '6e 4c', '1a 1e')
manticore.id = 'manticore'
manticore_0 = Star(manticore, [], {"health":250, "offense":15})
manticore_1 = Star(manticore, manticore_0, {"acid %":50, "pet acid %":60, "pet poison %":60, "poison %":50})
manticore_2 = Star(manticore, manticore_1, {"health %":6, "pet health %":12})
manticore_3 = Star(manticore, manticore_2, {"acid resist":10, "offense":20, "pet all damage %":40, "pet offense %":4, "physical resist":4})
manticore_4 = Star(manticore, manticore_3, {"acid %":40, "pet acid %":60, "pet poison %":60, "poison":[8, 5], "poison %":40, "poison duration":30})
manticore_5 = Star(manticore, manticore_4, {})
manticore_5.addAbility(Ability('Acid Spray', {"chance":0.15, "recharge":1, "skillClass":'Skill_AttackWave', "trigger":'attack', "type":'attack', "waveDistance":4, "waveEndWidth":4, "waveStartWidth":2}, {"duration":{"reduce resist":28}, "triggered acid":217, "triggered poison":[195, 2]}))

solemnWatcher = Constellation('Solemn Watcher', '10p', '3p 2o')
solemnWatcher.id = 'solemnWatcher'
solemnWatcher_0 = Star(solemnWatcher, [], {"physique":25})
solemnWatcher_1 = Star(solemnWatcher, solemnWatcher_0, {"armor":40, "chaos resist":18})
solemnWatcher_2 = Star(solemnWatcher, solemnWatcher_1, {"armor":40, "pierce resist":18})
solemnWatcher_3 = Star(solemnWatcher, solemnWatcher_2, {"defense":30, "physique %":3})
solemnWatcher_4 = Star(solemnWatcher, solemnWatcher_3, {"defense %":5, "reflected damage reduction":20})

messengerofWar = Constellation('Messenger of War', '7p 3a', '3p 2c')
messengerofWar.id = 'messengerofWar'
messengerofWar_0 = Star(messengerofWar, [], {"fire retaliation":90, "retaliation %":30})
messengerofWar_1 = Star(messengerofWar, messengerofWar_0, {"move speed":5, "offense":20, "physique":20})
messengerofWar_2 = Star(messengerofWar, messengerofWar_1, {"offense":25, "retaliation %":60})
messengerofWar_3 = Star(messengerofWar, messengerofWar_2, {"armor %":12, "fire retaliation":120})
messengerofWar_4 = Star(messengerofWar, messengerofWar_3, {"elemental resist":15, "fire retaliation":120})
messengerofWar_5 = Star(messengerofWar, messengerofWar_4, {})

kraken = Constellation('Kraken', '5p 5e', '3p 2c')
kraken.id = 'kraken'
kraken.restricts = ['2h-axe', '2h-mace', '2h-sword', 'ranged']
kraken_0 = Star(kraken, [], {"all damage %":50, "retaliation %":80})
kraken_1 = Star(kraken, kraken_0, {"attack speed":13, "cast speed":5, "health":250})
kraken_2 = Star(kraken, kraken_1, {"attack speed":13, "cast speed":5, "health":250})
kraken_3 = Star(kraken, kraken_2, {"all damage %":70, "move speed":5, "retaliation %":100})
kraken_4 = Star(kraken, kraken_3, {"crit damage":15, "physical resist":4})

hydra = Constellation('Hydra', '5e 3a 3c', '3e 2c')
hydra.id = 'hydra'
hydra.restricts = ['ranged']
hydra_0 = Star(hydra, [], {"offense":25})
hydra_1 = Star(hydra, hydra_0, {"move speed":10, "offense":35})
hydra_2 = Star(hydra, hydra_1, {"attack speed":5, "cast speed":5, "lifesteal %":5})
hydra_3 = Star(hydra, hydra_2, {"offense":25, "physical":6})
hydra_4 = Star(hydra, hydra_3, {"offense %":4, "physical":12, "slow resist":20})
hydra_5 = Star(hydra, hydra_4, {"all damage %":50, "attack speed":5, "cast speed":5})

bladesofNadaan = Constellation('Blades of Nadaan', '10a', '3a 2o')
bladesofNadaan.id = 'bladesofNadaan'
bladesofNadaan.restricts = ['2h-sword', 'sword']
bladesofNadaan_0 = Star(bladesofNadaan, [], {"avoid melee":2, "avoid ranged":2})
bladesofNadaan_1 = Star(bladesofNadaan, bladesofNadaan_0, {"pierce %":40})
bladesofNadaan_2 = Star(bladesofNadaan, bladesofNadaan_1, {"pierce %":50})
bladesofNadaan_3 = Star(bladesofNadaan, bladesofNadaan_2, {"attack speed":4, "defense":15})
bladesofNadaan_4 = Star(bladesofNadaan, bladesofNadaan_3, {"attack speed":4, "defense":15})
bladesofNadaan_5 = Star(bladesofNadaan, bladesofNadaan_4, {"pierce":16, "pierce %":50})

rhowansScepter = Constellation("Rhowan's Scepter", '6a 4o', '3a 2o')
rhowansScepter.id = 'rhowansScepter'
rhowansScepter.restricts = ['2h-mace', 'mace']
rhowansScepter_0 = Star(rhowansScepter, [], {"armor":30, "defense":20})
rhowansScepter_1 = Star(rhowansScepter, rhowansScepter_0, {"armor":80, "health %":6})
rhowansScepter_2 = Star(rhowansScepter, rhowansScepter_1, {"petrify resist":25, "physical %":50})
rhowansScepter_3 = Star(rhowansScepter, rhowansScepter_2, {"armor %":8, "physical":10, "physical %":50, "retaliation %":50})
rhowansScepter_4 = Star(rhowansScepter, rhowansScepter_3, {"defense":50, "internal %":50})
rhowansScepter_5 = Star(rhowansScepter, rhowansScepter_4, {"internal":[20, 5], "internal %":80, "internal duration":50, "retaliation %":50})

berserker = Constellation('Berserker', '5a 5e', '3e 2c')
berserker.id = 'berserker'
berserker.restricts = ['2h-axe', 'axe']
berserker_0 = Star(berserker, [], {"health":300, "offense":20})
berserker_1 = Star(berserker, berserker_0, {"bleed %":50, "freeze resist":15, "physical %":50})
berserker_2 = Star(berserker, berserker_1, {"crit damage":8, "offense":60})
berserker_3 = Star(berserker, berserker_2, {"bleed %":50, "physical %":50, "stun resist":15})
berserker_4 = Star(berserker, berserker_3, {"bleed":[20, 3], "bleed %":50, "bleed duration":50})
berserker_5 = Star(berserker, berserker_4, {"healing %":15, "health/s":25, "physical resist":4, "pierce resist":15})

oklainesLantern = Constellation("Oklaine's Lantern", '10e', '3e 2o')
oklainesLantern.id = 'oklainesLantern'
oklainesLantern.restricts = ['dagger', 'offhand', 'scepter']
oklainesLantern_0 = Star(oklainesLantern, [], {"energy/s %":15})
oklainesLantern_1 = Star(oklainesLantern, oklainesLantern_0, {"defense":20, "offense":25})
oklainesLantern_2 = Star(oklainesLantern, oklainesLantern_1, {"defense":20, "offense":25})
oklainesLantern_3 = Star(oklainesLantern, oklainesLantern_2, {"all damage %":50, "trap resist":25})
oklainesLantern_4 = Star(oklainesLantern, oklainesLantern_3, {"attack speed":5, "cast speed":5, "energy/s":2})

shieldmaiden = Constellation('Shieldmaiden', '6p 4o', '3p 2o')
shieldmaiden.id = 'shieldmaiden'
shieldmaiden.restricts = ['shield']
shieldmaiden_0 = Star(shieldmaiden, [], {"blocked damage %":30, "defense":20})
shieldmaiden_1 = Star(shieldmaiden, shieldmaiden_0, {"internal %":50, "retaliation %":40})
shieldmaiden_2 = Star(shieldmaiden, shieldmaiden_1, {"block %":5, "defense":50})
shieldmaiden_3 = Star(shieldmaiden, shieldmaiden_2, {"block %":6, "internal":[20, 5], "physical retaliation":200})
shieldmaiden_4 = Star(shieldmaiden, shieldmaiden_3, {"blocked damage %":50, "stun resist":25})
shieldmaiden_5 = Star(shieldmaiden, shieldmaiden_4, {"blocked damage %":80, "shield recovery":30})

behemoth = Constellation('Behemoth', '4p 4e 3c', '3e 2c')
behemoth.id = 'behemoth'
behemoth_0 = Star(behemoth, [], {"health/s":30})
behemoth_1 = Star(behemoth, behemoth_0, {"health":300, "pet health %":12})
behemoth_2 = Star(behemoth, behemoth_1, {"healing %":6, "health/s":70})
behemoth_3 = Star(behemoth, behemoth_2, {"armor":80, "health %":8, "pet armor":100})
behemoth_4 = Star(behemoth, behemoth_3, {"health/s %":80, "pet health/s %":100})
behemoth_5 = Star(behemoth, behemoth_4, {})
behemoth_5.addAbility(Ability('Giantsblood', {"activeDuration":12, "chance":0.15, "recharge":25, "skillClass":'Skill_BuffSelfDuration', "trigger":'hit', "type":'buff'}, {"health/s":590}))

chariotoftheDead = Constellation('Chariot of the Dead', '5a 5e', '3e 2c')
chariotoftheDead.id = 'chariotoftheDead'
chariotoftheDead_0 = Star(chariotoftheDead, [], {"cunning":20, "physique":20})
chariotoftheDead_1 = Star(chariotoftheDead, chariotoftheDead_0, {"offense":15, "slow resist":10})
chariotoftheDead_2 = Star(chariotoftheDead, chariotoftheDead_1, {"armor":60, "cunning":25})
chariotoftheDead_3 = Star(chariotoftheDead, chariotoftheDead_2, {"stun resist":20, "vitality resist":16})
chariotoftheDead_4 = Star(chariotoftheDead, chariotoftheDead_3, {"offense":25, "slow resist":15})
chariotoftheDead_5 = Star(chariotoftheDead, chariotoftheDead_4, {"offense":15, "offense %":4})
chariotoftheDead_6 = Star(chariotoftheDead, chariotoftheDead_5, {})
chariotoftheDead_6.addAbility(Ability('Wayward Soul', {"activeDuration":5, "chance":0.2, "recharge":8, "skillClass":'Skill_BuffSelfDuration', "trigger":'hit', "type":'buff'}, {"armor":460, "defense":130}))

uloKeeperoftheWaters = Constellation('Ulo Keeper of the Waters', '6p 4o', '3p 2o')
uloKeeperoftheWaters.id = 'uloKeeperoftheWaters'
uloKeeperoftheWaters_0 = Star(uloKeeperoftheWaters, [], {"elemental resist":15, "pet elemental resist":15})
uloKeeperoftheWaters_1 = Star(uloKeeperoftheWaters, uloKeeperoftheWaters_0, {"energy":300, "health":300, "life leech resist":30})
uloKeeperoftheWaters_2 = Star(uloKeeperoftheWaters, uloKeeperoftheWaters_1, {"freeze resist":15, "pet freeze resist":15, "pet petrify resist":15, "pet stun resist":15, "pet trap resist":15, "petrify resist":15, "stun resist":15, "trap resist":15})
uloKeeperoftheWaters_3 = Star(uloKeeperoftheWaters, uloKeeperoftheWaters_2, {"acid resist":20, "chaos resist":20, "pet acid resist":20, "pet chaos resist":20})
uloKeeperoftheWaters_4 = Star(uloKeeperoftheWaters, uloKeeperoftheWaters_3, {})
uloKeeperoftheWaters_4.addAbility(Ability('Purge', {"activeDuration":1, "chance":1, "radius":3.5, "recharge":10, "skillClass":'Skill_DispelMagic', "trigger":'attack', "type":'buff'}, {}))

aeonsHourglass = Constellation("Aeon's Hourglass", '8c 18p', '')
aeonsHourglass.id = 'aeonsHourglass'
aeonsHourglass_0 = Star(aeonsHourglass, [], {"cunning":40, "physique":40, "spirit":40})
aeonsHourglass_1 = Star(aeonsHourglass, aeonsHourglass_0, {})
aeonsHourglass_2 = Star(aeonsHourglass, aeonsHourglass_1, {"reflected damage reduction":25, "slow resist":50, "trap resist":30})
aeonsHourglass_3 = Star(aeonsHourglass, aeonsHourglass_2, {"aether resist":20, "vitality resist":15})
aeonsHourglass_4 = Star(aeonsHourglass, aeonsHourglass_3, {"avoid melee":6, "avoid ranged":6, "defense":70})
aeonsHourglass_5 = Star(aeonsHourglass, aeonsHourglass_4, {})
aeonsHourglass_5.addAbility(Ability('Time Dilation', {"chance":1, "recharge":8, "skillClass":'Skill_RefreshCooldown', "trigger":'attack', "type":'buff'}, {}))

abomination = Constellation('Abomination', '8c 18e', '')
abomination.id = 'abomination'
abomination_0 = Star(abomination, [], {"chaos %":80, "poison %":80})
abomination_1 = Star(abomination, abomination_0, {"acid %":80, "vitality %":80, "vitality decay %":80})
abomination_2 = Star(abomination, abomination_1, {"acid resist":20, "offense":40})
abomination_3 = Star(abomination, abomination_2, {"chaos %":80, "health":400, "offense":40, "vitality %":80})
abomination_4 = Star(abomination, abomination_3, {})
abomination_4.addAbility(Ability('Abominable Might', {"activeDuration":12, "chance":0.2, "recharge":18, "skillClass":'Skill_BuffSelfDuration', "trigger":'attack', "type":'buff'}, {"chaos %":260, "health/s %":100, "triggered chaos":94.5, "vitality %":310, "vitality decay %":310}))
abomination_5 = Star(abomination, abomination_4, {"health":400, "offense":40, "poison %":80, "vitality decay %":80})
abomination_6 = Star(abomination, abomination_5, {"acid":12, "acid %":100, "poison %":100})
abomination_7 = Star(abomination, abomination_6, {})
abomination_7.addAbility(Ability('Tainted Eruption', {"chance":0.15, "radius":10, "recharge":3, "skillClass":'Skill_AttackRadius', "trigger":'attack', "type":'attack'}, {"triggered poison":[472, 5]}))

lightofEmpyrion = Constellation('Light of Empyrion', '8o 18p', '')
lightofEmpyrion.id = 'lightofEmpyrion'
lightofEmpyrion_0 = Star(lightofEmpyrion, [], {"defense":25, "fire %":80})
lightofEmpyrion_1 = Star(lightofEmpyrion, lightofEmpyrion_0, {"defense":25, "physical %":80})
lightofEmpyrion_2 = Star(lightofEmpyrion, lightofEmpyrion_1, {"elemental resist":15, "health %":10, "vitality resist":15})
lightofEmpyrion_3 = Star(lightofEmpyrion, lightofEmpyrion_2, {"fire %":100, "health %":10, "physical %":100})
lightofEmpyrion_4 = Star(lightofEmpyrion, lightofEmpyrion_3, {"aether resist":20, "chaos resist":20})
lightofEmpyrion_5 = Star(lightofEmpyrion, lightofEmpyrion_4, {"fire":19})
lightofEmpyrion_6 = Star(lightofEmpyrion, lightofEmpyrion_5, {})
lightofEmpyrion_6.addAbility(Ability('Light of Empyrion', {"chance":0.3, "radius":5, "recharge":2, "skillClass":'Skill_AttackRadius', "trigger":'hit', "type":'attack'}, {"triggered burn":[270, 2], "triggered fire":332.5, "triggered physical":315, "weapon damage %":54}))

oleron = Constellation('Oleron', '20a 7o', '')
oleron.id = 'oleron'
oleron_0 = Star(oleron, [], {"cunning":30, "health":300, "physique":30})
oleron_1 = Star(oleron, oleron_0, {"bleed %":80, "internal %":80, "physical %":80})
oleron_2 = Star(oleron, oleron_1, {"armor":80, "bleed resist":10, "offense":35})
oleron_3 = Star(oleron, oleron_2, {"health":350, "physical resist":4})
oleron_4 = Star(oleron, oleron_3, {"bleed %":100, "physical":14, "physical %":120})
oleron_5 = Star(oleron, oleron_4, {"internal":[24, 5], "internal %":120, "offense":35})
oleron_6 = Star(oleron, oleron_5, {})
oleron_6.addAbility(Ability('Blind Fury', {"chance":1, "radius":6, "recharge":1, "skillClass":'Skill_AttackRadius', "trigger":'critical', "type":'attack'}, {"triggered bleed":[335, 5], "triggered internal":[335, 5], "triggered physical":220, "weapon damage %":75}))

menhirsObelisk = Constellation("Menhir's Obelisk", '8o 15p', '')
menhirsObelisk.id = 'menhirsObelisk'
menhirsObelisk_0 = Star(menhirsObelisk, [], {"armor %":10})
menhirsObelisk_1 = Star(menhirsObelisk, menhirsObelisk_0, {"armor":210, "defense":30})
menhirsObelisk_2 = Star(menhirsObelisk, menhirsObelisk_1, {"defense":40, "defense %":6})
menhirsObelisk_3 = Star(menhirsObelisk, menhirsObelisk_2, {"physical retaliation":120, "retaliation %":140})
menhirsObelisk_4 = Star(menhirsObelisk, menhirsObelisk_3, {"block %":5, "blocked damage %":40})
menhirsObelisk_5 = Star(menhirsObelisk, menhirsObelisk_4, {"armor absorb":18, "freeze resist":30, "stun resist":30})
menhirsObelisk_6 = Star(menhirsObelisk, menhirsObelisk_5, {})

spearoftheHeavens = Constellation('Spear of the Heavens', '20p 7c', '')
spearoftheHeavens.id = 'spearoftheHeavens'
spearoftheHeavens_0 = Star(spearoftheHeavens, [], {"lightning %":80, "offense":20})
spearoftheHeavens_1 = Star(spearoftheHeavens, spearoftheHeavens_0, {"aether %":80, "offense":20})
spearoftheHeavens_2 = Star(spearoftheHeavens, spearoftheHeavens_1, {"aether resist":15, "offense %":5})
spearoftheHeavens_3 = Star(spearoftheHeavens, spearoftheHeavens_2, {"aether":10, "crit damage":5, "energy/s %":15})
spearoftheHeavens_4 = Star(spearoftheHeavens, spearoftheHeavens_3, {"aether %":100, "lightning %":100})
spearoftheHeavens_5 = Star(spearoftheHeavens, spearoftheHeavens_4, {})
spearoftheHeavens_5.addAbility(Ability('Spear of the Heavens', {"chance":0.5, "radius":2.4, "recharge":1, "skillClass":'Skill_AttackProjectileDrop', "trigger":'hit', "type":'attack'}, {"triggered aether":324, "triggered electrocute":[355, 2], "triggered lightning":227.5, "weapon damage %":60}))

ulzuinsTorch = Constellation("Ulzuin's Torch", '8c 15e', '')
ulzuinsTorch.id = 'ulzuinsTorch'
ulzuinsTorch_0 = Star(ulzuinsTorch, [], {"fire %":80, "offense":20})
ulzuinsTorch_1 = Star(ulzuinsTorch, ulzuinsTorch_0, {"chaos resist":15, "offense %":5})
ulzuinsTorch_2 = Star(ulzuinsTorch, ulzuinsTorch_1, {"crit damage":5, "move speed":5})
ulzuinsTorch_3 = Star(ulzuinsTorch, ulzuinsTorch_2, {"fire":13.5, "fire %":100})
ulzuinsTorch_4 = Star(ulzuinsTorch, ulzuinsTorch_3, {"burn":[18, 3], "burn %":100, "stun resist":20})
ulzuinsTorch_5 = Star(ulzuinsTorch, ulzuinsTorch_4, {"armor":120, "burn %":100, "burn duration":50})
ulzuinsTorch_6 = Star(ulzuinsTorch, ulzuinsTorch_5, {})
ulzuinsTorch_6.addAbility(Ability('Meteor Shower', {"activeDuration":3, "chance":0.3, "projectiles":1, "radius":5, "recharge":3.5, "skillClass":'Skill_BuffAttackRadiusDrop', "trigger":'attack', "type":'attack'}, {"triggered burn":[270, 2], "triggered fire":211, "triggered physical":197.5}))

dyingGod = Constellation('Dying God', '8c 15p', '')
dyingGod.id = 'dyingGod'
dyingGod_0 = Star(dyingGod, [], {"offense":20, "vitality %":80})
dyingGod_1 = Star(dyingGod, dyingGod_0, {"chaos %":80, "offense":20})
dyingGod_2 = Star(dyingGod, dyingGod_1, {"offense %":3, "pet all damage %":60, "pet chaos %":120, "spirit":35})
dyingGod_3 = Star(dyingGod, dyingGod_2, {"chaos resist":15, "defense":25, "offense":45})
dyingGod_4 = Star(dyingGod, dyingGod_3, {"chaos %":100, "defense":30, "vitality %":100})
dyingGod_5 = Star(dyingGod, dyingGod_4, {"chaos":11.5, "crit damage":4, "pet all damage %":80, "pet crit damage":6})
dyingGod_6 = Star(dyingGod, dyingGod_5, {})

treeofLife = Constellation('Tree of Life', '20p 7o', '')
treeofLife.id = 'treeofLife'
treeofLife_0 = Star(treeofLife, [], {"health %":8, "pet health %":12})
treeofLife_1 = Star(treeofLife, treeofLife_0, {"health/s":60, "pet health/s %":50})
treeofLife_2 = Star(treeofLife, treeofLife_1, {"health %":8, "health/s %":30, "pet health %":15})
treeofLife_3 = Star(treeofLife, treeofLife_2, {"defense":30, "health/s":60, "pet health/s %":50})
treeofLife_4 = Star(treeofLife, treeofLife_3, {"health %":8, "health/s %":30, "pet health/s":80})
treeofLife_5 = Star(treeofLife, treeofLife_4, {})

mogdrogentheWolf = Constellation('Mogdrogen the Wolf', '15a 12e', '')
mogdrogentheWolf.id = 'mogdrogentheWolf'
mogdrogentheWolf_0 = Star(mogdrogentheWolf, [], {"health":300, "offense":35, "pet offense %":5})
mogdrogentheWolf_1 = Star(mogdrogentheWolf, mogdrogentheWolf_0, {"bleed %":80, "pet all damage %":60})
mogdrogentheWolf_2 = Star(mogdrogentheWolf, mogdrogentheWolf_1, {"defense":50, "health":350, "pet bleed %":120, "pet health %":10, "vitality resist":20})
mogdrogentheWolf_3 = Star(mogdrogentheWolf, mogdrogentheWolf_2, {"bleed":[18, 3], "bleed %":80, "bleed duration":50, "healing %":20})
mogdrogentheWolf_4 = Star(mogdrogentheWolf, mogdrogentheWolf_3, {"bleed resist":15, "elemental resist":15, "offense %":4, "pet all damage %":80})
mogdrogentheWolf_5 = Star(mogdrogentheWolf, mogdrogentheWolf_4, {})
mogdrogentheWolf_5.addAbility(Ability('Howl of Mogdrogen', {"activeDuration":10, "chance":0.2, "recharge":15, "skillClass":'Skill_BuffSelfDuration', "trigger":'attack', "type":'buff'}, {"attack speed":18, "bleed %":275, "cast speed":15, "health/s %":100, "triggered bleed":[58, 3]}))

blindSage = Constellation('Blind Sage', '10a 18e', '')
blindSage.id = 'blindSage'
blindSage_0 = Star(blindSage, [], {"offense":25, "physique":30, "spirit":30})
blindSage_1 = Star(blindSage, blindSage_0, {"defense":40, "elemental %":80, "elemental resist":15})
blindSage_2 = Star(blindSage, blindSage_1, {"crit damage":12, "physical resist":4, "skill disruption protection":30})
blindSage_3 = Star(blindSage, blindSage_2, {"cold %":100, "frostburn %":250, "frostburn duration":25, "offense":45})
blindSage_4 = Star(blindSage, blindSage_3, {"electrocute %":250, "electrocute duration":25, "lightning %":100, "offense":45})
blindSage_5 = Star(blindSage, blindSage_4, {"burn %":250, "burn duration":25, "fire %":100, "offense":45})
blindSage_6 = Star(blindSage, blindSage_5, {})
blindSage_6.addAbility(Ability('Elemental Seeker', {"chance":1, "radius":1, "recharge":0.8, "skillClass":'Skill_TargetedSpawnPet', "trigger":'attack', "type":'summon'}, {}))

leviathan = Constellation('Leviathan', '13e 13a', '')
leviathan.id = 'leviathan'
leviathan_0 = Star(leviathan, [], {"cold":6, "cold %":80})
leviathan_1 = Star(leviathan, leviathan_0, {"health %":8, "physique":35})
leviathan_2 = Star(leviathan, leviathan_1, {"defense":60, "energy %":10, "energy/s %":20})
leviathan_3 = Star(leviathan, leviathan_2, {"physical resist":5, "pierce resist":20, "vitality resist":20})
leviathan_4 = Star(leviathan, leviathan_3, {"cold":12, "cold %":100})
leviathan_5 = Star(leviathan, leviathan_4, {"frostburn":[20, 3], "frostburn %":100})
leviathan_6 = Star(leviathan, leviathan_5, {})
leviathan_6.addAbility(Ability('Whirlpool', {"activeDuration":6, "chance":0.3, "radius":3.5, "recharge":2, "skillClass":'Skill_AttackProjectileAreaEffect', "trigger":'attack', "type":'attack'}, {"triggered cold":420, "triggered frostburn":[270, 2]}))

theUnknownSoldier = Constellation('The Unknown Soldier', '15a 8o', '')
theUnknownSoldier.id = 'theUnknownSoldier'
theUnknownSoldier_0 = Star(theUnknownSoldier, [], {"offense":15, "pierce %":80})
theUnknownSoldier_1 = Star(theUnknownSoldier, theUnknownSoldier_0, {"bleed":[18, 3], "bleed %":80, "offense":40})
theUnknownSoldier_2 = Star(theUnknownSoldier, theUnknownSoldier_1, {"attack speed":5, "health":400})
theUnknownSoldier_3 = Star(theUnknownSoldier, theUnknownSoldier_2, {"bleed %":120, "pierce %":120})
theUnknownSoldier_4 = Star(theUnknownSoldier, theUnknownSoldier_3, {"health %":8, "offense":40, "skill disruption protection":30})
theUnknownSoldier_5 = Star(theUnknownSoldier, theUnknownSoldier_4, {"crit damage":6, "offense %":4, "pierce":20})
theUnknownSoldier_6 = Star(theUnknownSoldier, theUnknownSoldier_5, {})
theUnknownSoldier_6.addAbility(Ability('Living Shadow', {"chance":1, "recharge":6, "skillClass":'Skill_SpawnPet', "trigger":'critical', "type":'summon'}, {}))

harvestmansScythe = Constellation("Harvestman's Scythe", '3a 5p 3o', '3p 3a')
harvestmansScythe.id = 'harvestmansScythe'
harvestmansScythe_0 = Star(harvestmansScythe, [], {"energy/s":2, "move speed":3})
harvestmansScythe_1 = Star(harvestmansScythe, harvestmansScythe_0, {"energy":200, "health":200, "move speed":3})
harvestmansScythe_2 = Star(harvestmansScythe, harvestmansScythe_1, {"healing %":10, "physique %":4})
harvestmansScythe_3 = Star(harvestmansScythe, harvestmansScythe_2, {"cunning %":4, "spirit %":4})
harvestmansScythe_4 = Star(harvestmansScythe, harvestmansScythe_3, {"defense %":4, "energy/s %":30, "health/s %":60})
harvestmansScythe_5 = Star(harvestmansScythe, harvestmansScythe_4, {"energy %":8, "energy/s":3, "health %":8, "health/s":50})

xC = Constellation('Crossroads Chaos', '', '1c')
xC.id = 'xC'
xC_0 = Star(xC, [], {"health %":5})

xO = Constellation('Crossroads Order', '', '1o')
xO.id = 'xO'
xO_0 = Star(xO, [], {"health %":5})

xE = Constellation('Crossroads Eldritch', '', '1e')
xE.id = 'xE'
xE_0 = Star(xE, [], {"offense":18})

xA = Constellation('Crossroads Ascendant', '', '1a')
xA.id = 'xA'
xA_0 = Star(xA, [], {"offense":18})

candle = Constellation('Candle', '1e', '4e')
candle.id = 'candle'
candle_0 = Star(candle, [], {"elemental %":15})
candle_1 = Star(candle, candle_0, {"defense":15, "elemental resist":8, "physique":15})
candle_2 = Star(candle, candle_1, {"aether resist":8, "elemental %":24, "energy/s":2.5})

lion = Constellation('Lion', '1o', '3o')
lion.id = 'lion'
lion_0 = Star(lion, [], {"defense":8, "health %":4, "pet health %":8})
lion_1 = Star(lion, lion_0, {"armor":30, "move speed":6, "spirit":15})
lion_2 = Star(lion, lion_1, {"all damage %":15, "pet all damage %":20, "physical resist":2})

jackal = Constellation('Jackal', '1c', '3c')
jackal.id = 'jackal'
jackal_0 = Star(jackal, [], {"energy/s %":10, "pet health %":8})
jackal_1 = Star(jackal, jackal_0, {"offense":12, "total speed":6})
jackal_2 = Star(jackal, jackal_1, {"all damage %":15, "pet attack speed":5, "physical resist":2})

stag = Constellation('Stag', '1o', '2o 3p')
stag.id = 'stag'
stag_0 = Star(stag, [], {"bleed %":15, "pet all damage %":20, "physical %":15})
stag_1 = Star(stag, stag_0, {"move speed":5, "pet all damage %":60, "pet pierce resist":15, "physique":15, "pierce resist":10})
stag_2 = Star(stag, stag_1, {"defense":15, "health":110, "pet defense %":3, "pet physical %":30, "retaliation %":30})
stag_3 = Star(stag, stag_2, {"armor %":10, "bleed %":50, "pet physical %":50, "physical %":24})

wretch = Constellation('Wretch', '1c', '2c 3p')
wretch.id = 'wretch'
wretch_0 = Star(wretch, [], {"acid %":15, "chaos %":15})
wretch_1 = Star(wretch, wretch_0, {"bleed resist":12, "physique":15})
wretch_2 = Star(wretch, wretch_1, {"acid retaliation":44, "defense":15, "health":140})
wretch_3 = Star(wretch, wretch_2, {"acid %":24, "chaos %":24})

quill = Constellation('Quill', '1e', '3e 3a')
quill.id = 'quill'
quill_0 = Star(quill, [], {"elemental %":15})
quill_1 = Star(quill, quill_0, {"aether resist":8})
quill_2 = Star(quill, quill_1, {"energy":150, "health":100})
quill_3 = Star(quill, quill_2, {"defense %":2, "elemental %":24, "energy/s %":10})

toad = Constellation('Toad', '1a', '3a 3e')
toad.id = 'toad'
toad_0 = Star(toad, [], {"vitality resist":8})
toad_1 = Star(toad, toad_0, {"offense":10, "pet all damage %":25, "pet offense %":3, "spirit":15})
toad_2 = Star(toad, toad_1, {"health":60, "lifesteal %":3, "pet all damage %":25, "pet lifesteal %":4})
toad_3 = Star(toad, toad_2, {"aether %":24, "pet offense %":3, "vitality %":24})

murmur = Constellation('Murmur', '6e 6p 3c', '2e 2c')
murmur.id = 'murmur'
murmur_0 = Star(murmur, [], {"acid %":40, "cold %":40})
murmur_1 = Star(murmur, murmur_0, {"avoid melee":3, "avoid ranged":3})
murmur_2 = Star(murmur, murmur_1, {"defense":20, "health":200})
murmur_3 = Star(murmur, murmur_2, {})
murmur_4 = Star(murmur, murmur_3, {"defense":20, "vitality resist":15})
murmur_5 = Star(murmur, murmur_4, {"acid %":50, "cold %":50, "frostburn %":80})

staffRattosh = Constellation('StaffRattosh', '6p 3o 3c', '3p 2c')
staffRattosh.id = 'staffRattosh'
staffRattosh_0 = Star(staffRattosh, [], {"defense":20, "pet defense %":3})
staffRattosh_1 = Star(staffRattosh, staffRattosh_0, {"aether resist":15, "pet aether resist":20})
staffRattosh_2 = Star(staffRattosh, staffRattosh_1, {"health":250, "pet aether %":70, "pet all damage %":50})
staffRattosh_3 = Star(staffRattosh, staffRattosh_2, {"health %":5, "pet vitality resist":20, "vitality resist":10})
staffRattosh_4 = Star(staffRattosh, staffRattosh_3, {"all damage %":50, "pet aether %":70, "pet all damage %":50})
staffRattosh_5 = Star(staffRattosh, staffRattosh_4, {"offense %":4, "pet offense %":3, "pet total speed":8})

alladrahPhoenix = Constellation('AlladrahPhoenix', '6e 6p 3o', '2e 2a')
alladrahPhoenix.id = 'alladrahPhoenix'
alladrahPhoenix_0 = Star(alladrahPhoenix, [], {"aether %":40, "elemental %":40})
alladrahPhoenix_1 = Star(alladrahPhoenix, alladrahPhoenix_0, {"chaos resist":12, "health":250})
alladrahPhoenix_2 = Star(alladrahPhoenix, alladrahPhoenix_1, {"aether %":30, "elemental %":30, "fire retaliation":200, "freeze resist":15})
alladrahPhoenix_3 = Star(alladrahPhoenix, alladrahPhoenix_2, {"burn %":50, "burn duration":30, "crit damage":8, "fire %":50, "retaliation %":80})
alladrahPhoenix_4 = Star(alladrahPhoenix, alladrahPhoenix_3, {})
alladrahPhoenix_4.addAbility(Ability('Phoenix Fire', {"activeDuration":7, "chance":1, "radius":5, "recharge":12, "skillClass":'Skill_BuffAttackRadiusDuration', "trigger":'critical', "type":'attack'}, {"fire retaliation":360, "retaliation %":140, "triggered aether":92, "triggered burn":[195, 2], "triggered fire":92}))

typhos = Constellation('Typhos', '6a 3o 3c', '3a 2o')
typhos.id = 'typhos'
typhos_0 = Star(typhos, [], {"offense":20, "pet offense %":3})
typhos_1 = Star(typhos, typhos_0, {"defense":20, "pet defense %":3})
typhos_2 = Star(typhos, typhos_1, {"acid resist":15, "bleed resist":15, "pet acid resist":15, "pet bleed resist":15})
typhos_3 = Star(typhos, typhos_2, {"health %":6, "offense":20, "pet all damage %":40, "pet offense %":3})
typhos_4 = Star(typhos, typhos_3, {"crit damage":6, "pet all damage %":40, "pet crit damage":10})
typhos_5 = Star(typhos, typhos_4, {"pet physical resist":6, "pet stun resist":50, "total speed":6})

harp = Constellation('Harp', '6p 6a 3o', '2p 2o')
harp.id = 'harp'
harp_0 = Star(harp, [], {"defense":15, "health":200})
harp_1 = Star(harp, harp_0, {"elemental %":40, "energy/s %":25, "pierce %":40})
harp_2 = Star(harp, harp_1, {"bleed resist":10, "health":300, "pierce resist":15})
harp_3 = Star(harp, harp_2, {"defense":30, "energy/s":3, "total speed":6})
harp_4 = Star(harp, harp_3, {"burn %":80, "electrocute %":80, "elemental %":50, "elemental resist":15, "frostburn %":80, "pierce %":50})
harp_5 = Star(harp, harp_4, {})

ultos = Constellation('Ultos', '6c 10e 10p', '')
ultos.id = 'ultos'
ultos_0 = Star(ultos, [], {"cold %":80, "offense":25})
ultos_1 = Star(ultos, ultos_0, {"lightning %":80, "offense":25})
ultos_2 = Star(ultos, ultos_1, {"chaos resist":15, "health":350})
ultos_3 = Star(ultos, ultos_2, {"crit damage":5, "electrocute %":120, "frostburn %":120, "offense":20})
ultos_4 = Star(ultos, ultos_3, {"cold %":100, "lightning":20, "lightning %":100})
ultos_5 = Star(ultos, ultos_4, {})
ultos_5.addAbility(Ability('Hand of Ultos', {"chance":1, "recharge":1.5, "skillClass":'Skill_AttackChain', "sparkMaxNumber":10, "trigger":'critical', "type":'attack'}, {"duration":{"reduce elemental resist":20}, "triggered electrocute":[270, 2], "triggered lightning":328, "weapon damage %":20}))

ishtak = Constellation('Ishtak', '10o 15p', '')
ishtak.id = 'ishtak'
ishtak_0 = Star(ishtak, [], {"energy":300, "health":300, "pet armor":200})
ishtak_1 = Star(ishtak, ishtak_0, {"acid resist":25, "health":300, "pet acid resist":30})
ishtak_2 = Star(ishtak, ishtak_1, {"pet all damage %":80, "slow resist":30, "total speed":6})
ishtak_3 = Star(ishtak, ishtak_2, {"bleed resist":20, "health":300, "pet all damage %":80, "pet bleed resist":30})
ishtak_4 = Star(ishtak, ishtak_3, {"defense %":4, "pet physical resist":5, "spirit %":3})
ishtak_5 = Star(ishtak, ishtak_4, {})
ishtak_5.addAbility(Ability('Nature Guardian', {"activeDuration":8, "chance":0.25, "recharge":15, "skillClass":'Skill_BuffSelfDuration', "trigger":'hit', "type":'buff'}, {}))

vire = Constellation('Vire', '18p 12a', '')
vire.id = 'vire'
vire_0 = Star(vire, [], {"armor":50, "health":300})
vire_1 = Star(vire, vire_0, {"internal %":80, "physical %":80, "physical retaliation":120})
vire_2 = Star(vire, vire_1, {"armor":80, "blocked damage %":30, "health %":8})
vire_3 = Star(vire, vire_2, {"cunning %":3, "internal %":120, "physical %":120, "retaliation %":140})
vire_4 = Star(vire, vire_3, {"aether resist":15, "bleed resist":15, "chaos resist":15, "physical resist":5})
vire_5 = Star(vire, vire_4, {})
vire_5.addAbility(Ability('Fist of Vire', {"activeDuration":1, "chance":0.2, "projectiles":5, "radius":2.5, "recharge":1, "skillClass":'Skill_AttackProjectileAreaEffect', "trigger":'hit', "type":'attack'}, {"triggered internal":[320, 5], "triggered physical":245, "weapon damage %":65}))

