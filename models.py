from dataModel import *
from constellationData import *

nyx = Model(
	{
		"spirit":12.5, 
		"offense":20, 
		"crit damage":5,
		"vitality %":20,
		"chaos %":7.5,
		"cast speed":5,
		"defense":5,
		"armor":3, 
		# armor absorb is good vs lots of little hits. This char regens fast with lots of little enemies so there's not much value
		"armor absorb":2,
		"health":.5, "health/s":1,
		"energy":.1, "energy/s":5,
		"avoid melee":10, "avoid ranged":15,
		"resist":7.5,

		"pet attack speed":5,
		"pet total speed":8,
		"pet offense":5,
		"pet offense %":50,
		"pet lifesteal %":2,
		"pet all damage %":7.5,
		"pet defense %":1,
		"pet resist":1.5,
		"pet health %":5,
		"pet health/s":1,
		"pet retaliation":1, "pet retaliaion %":3,

		"triggered vitality":30, "triggered vitality decay":10,
		"triggered chaos":10,
		"triggered fire":3,
		"triggered life leech":3,
		"triggered damage":1,
		
		"weapon damage %":1,
		"slow move":7,
		"stun %":10
	},

	{
		"attacks/s":10,
		"hits/s":1.5,
		"blocks/s":0,
		"kills/s":1,
		"crit chance":.12,
		"low healths/s":1.0/30, # total guesswork.

		"physique":650,
		"cunning":400,
		"spirit":650,

		"offense":1500,
		"defense":1000,

		"health":5000,
		"armor":450,

		"vitality %":750+350,
		"chaos %":350+350,

		"pet all damage %":200,

		"fight length":30,

		"weapons":["offhand"]
	}
)
nyx.blacklist = [
	sage, 			#seems cool but there's nothing but the ability
	wolf,			#relatively low value for the requirements
	soldier,			#relatively low value for the requirements
	tree, spear,
	falcon, hammer, owl, harpy, throne, wolverine, blade # don't need these. crook will supply all I need.
]
nyx.seedSolutions = [
    [xE, bat, scorpion, viper, gallows, eel, bonds, jackal, wendigo, revenant, xP, god],
    [xA, xC, fiend, bat, viper, gallows, eel, wendigo, manticore, xE, xP, revenant, god],
    [xA, xE, bat, fiend, viper, gallows, eel, wendigo, manticore, xO, xP, revenant, god],
    [xA, xC, fiend, bat, viper, gallows, eel, wendigo, manticore, xE, revenant, xP, god],
    [xA, xE, bat, fiend, viper, gallows, wendigo, manticore, xO, xP, eel, revenant, god],
    [xA, xC, fiend, bat, viper, gallows, guide, wendigo, manticore, revenant, xP, god],
    [xE, bat, fiend, viper, manticore, bonds, wraith, gallows, eel, wendigo, god],
    [xE, bat, fiend, witchblade, viper, manticore, gallows, wendigo, eel, wraith, god],
    [xP, gallows, eel, xE, imp, bat, jackal, manticore, bonds, wendigo, viper, god],
    [xC, viper, gallows, rat, wendigo, imp, bat, bonds, manticore, eel, god],
    [xC, viper, gallows, imp, eel, bat, wendigo, fiend, witchblade, bonds, god],
    [xO, tortoise, imp, gallows, eel, bat, fiend, wendigo, jackal, god, manticore],
    [xA, shepherd, wolverine, owl, xC, viper, jackal, eel, wendigo, xO, tortoise, panther, xP, god],
	[xO, tortoise, xE, raven, bat, rat, gallows, panther, watcher, viper, wendigo, god],
	[xA, shepherd, xE, bat, fiend, affliction, bonds, xO, tortoise, dryad, panther, wendigo],
	[xA, shepherd, xE, bat, raven, viper, affliction, bonds, xC, xO, tortoise, wendigo, dryad],
 	[xE, hawk, xO, tortoise, gallows, panther, bat, fiend, wendigo, viper, watcher, god],
 	[xE, hawk, xO, tortoise, gallows, panther, bat, rat, viper, wendigo, revenant, god]
]