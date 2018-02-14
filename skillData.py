from dataModel import *

#http://wikiwiki.jp/gdcrate/?Masteries%2FSoldier%2FMarkovian%27s%20Advantage
Skill("Markovian's Advantage", "Soldier",
	["",
		Ability("1",
			{"type":"aar", "chance":.08, "recharge":0, "duration":5},
			{"weapon damage %":128, "physical":10, "all damage %":15, "duration":{"reduce defense":30}}
		),
		Ability("2",
			{"type":"aar", "chance":.12, "recharge":0, "duration":5},
			{"weapon damage %":128, "physical":19, "all damage %":25, "duration":{"reduce defense":40}}
		),
		Ability("3",
			{"type":"aar", "chance":.15, "recharge":0, "duration":5},
			{"weapon damage %":128, "physical":28, "all damage %":35, "duration":{"reduce defense":51}}
		),
		Ability("4",
			{"type":"aar", "chance":.18, "recharge":0, "duration":5},
			{"weapon damage %":128, "physical":38, "all damage %":45, "duration":{"reduce defense":62}}
		),
		Ability("5",
			{"type":"aar", "chance":.20, "recharge":0, "duration":5},
			{"weapon damage %":128, "physical":47, "all damage %":55, "duration":{"reduce defense":73}}
		),
		Ability("6",
			{"type":"aar", "chance":.22, "recharge":0, "duration":5},
			{"weapon damage %":128, "physical":57, "all damage %":65, "duration":{"reduce defense":84}}
		),
		Ability("7",
			{"type":"aar", "chance":.23, "recharge":0, "duration":5},
			{"weapon damage %":128, "physical":66, "all damage %":75, "duration":{"reduce defense":95}}
		),
		Ability("8",
			{"type":"aar", "chance":.24, "recharge":0, "duration":5},
			{"weapon damage %":128, "physical":76, "all damage %":85, "duration":{"reduce defense":106}}
		),
		Ability("9",
			{"type":"aar", "chance":.25, "recharge":0, "duration":5},
			{"weapon damage %":128, "physical":86, "all damage %":95, "duration":{"reduce defense":117}}
		),
		Ability("10",
			{"type":"aar", "chance":.25, "recharge":0, "duration":5},
			{"weapon damage %":128, "physical":97, "all damage %":105, "duration":{"reduce defense":128}}
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FSoldier%2FFighting%20Spirit
Skill( "Fighting Spirit", "Soldier",
	["",
		Ability("1",
			{"type":"buff", "trigger":"hit", "chance":.05, "recharge":16, "duration":8},
			{"all damage %":35, "offense":30}
		),
		Ability("2",
			{"type":"buff", "trigger":"hit", "chance":.10, "recharge":16, "duration":8},
			{"all damage %":50, "offense":50}
		),
		Ability("3",
			{"type":"buff", "trigger":"hit", "chance":.14, "recharge":16, "duration":8},
			{"all damage %":65, "offense":70}
		),
		Ability("4",
			{"type":"buff", "trigger":"hit", "chance":.18, "recharge":16, "duration":8},
			{"all damage %":80, "offense":90}
		),
		Ability("5",
			{"type":"buff", "trigger":"hit", "chance":.22, "recharge":16, "duration":8},
			{"all damage %":95, "offense":108}
		),
		Ability("6",
			{"type":"buff", "trigger":"hit", "chance":.25, "recharge":16, "duration":8},
			{"all damage %":110, "offense":126}
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FSoldier%2FMenhir%27s%20Will
Skill( "Menhir's Will", "Soldier", 
	["",
		Ability("1",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":25, "duration":10},
			{"health %":10, "health/s":16}
		),
		Ability("2",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":24, "duration":10},
			{"health %":18, "health/s":32}
		),
		Ability("3",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":23, "duration":10},
			{"health %":24, "health/s":48}
		),
		Ability("4",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":22, "duration":10},
			{"health %":30, "health/s":64}
		),
		Ability("5",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":22, "duration":10},
			{"health %":35, "health/s":80}
		),
		Ability("6",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":21, "duration":10},
			{"health %":40, "health/s":96}
		),
		Ability("7",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":21, "duration":10},
			{"health %":44, "health/s":112}
		),
		Ability("8",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":20, "duration":10},
			{"health %":47, "health/s":128}
		),
		Ability("9",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":20, "duration":10},
			{"health %":50, "health/s":144}
		),
		Ability("10",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":19, "duration":10},
			{"health %":52, "health/s":160}
		),
		Ability("11",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":19, "duration":10},
			{"health %":54, "health/s":176}
		),
		Ability("12",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":18, "duration":10},
			{"health %":56, "health/s":194}
		),
		Ability("13",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":18, "duration":10},
			{"health %":58, "health/s":212}
		),
		Ability("14",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":17, "duration":10},
			{"health %":60, "health/s":230}
		),
		Ability("15",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":17, "duration":10},
			{"health %":62, "health/s":250}
		),
		Ability("16",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":16, "duration":10},
			{"health %":65, "health/s":272}
		),
		Ability("17",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":16, "duration":10},
			{"health %":65, "health/s":292}
		),
		Ability("18",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":16, "duration":10},
			{"health %":65, "health/s":312}
		),
		Ability("19",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":16, "duration":10},
			{"health %":65, "health/s":334}
		),
		Ability("20",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":16, "duration":10},
			{"health %":65, "health/s":356}
		),
		Ability("21",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":16, "duration":10},
			{"health %":65, "health/s":378}
		),
		Ability("22",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":16, "duration":10},
			{"health %":65, "health/s":400}
		),
		Ability("23",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":16, "duration":10},
			{"health %":65, "health/s":424}
		),
		Ability("24",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":16, "duration":10},
			{"health %":65, "health/s":448}
		),
		Ability("25",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":16, "duration":10},
			{"health %":65, "health/s":475}
		),
		Ability("26",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":15, "duration":10},
			{"health %":66, "health/s":518}
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FSoldier%2FMilitary%20Conditioning
Skill( "Military Conditioning", "Soldier", 
	["",
		Ability("1",
			{"type":"buff", "trigger":"passive"},
			{"physique %":1, "health %":2}
		),
		Ability("2",
			{"type":"buff", "trigger":"passive"},
			{"physique %":3, "health %":4}
		),
		Ability("3",
			{"type":"buff", "trigger":"passive"},
			{"physique %":5, "health %":6}
		),
		Ability("4",
			{"type":"buff", "trigger":"passive"},
			{"physique %":6, "health %":8}
		),
		Ability("5",
			{"type":"buff", "trigger":"passive"},
			{"physique %":8, "health %":10}
		),
		Ability("6",
			{"type":"buff", "trigger":"passive"},
			{"physique %":10, "health %":11}
		),
		Ability("7",
			{"type":"buff", "trigger":"passive"},
			{"physique %":12, "health %":12}
		),
		Ability("8",
			{"type":"buff", "trigger":"passive"},
			{"physique %":14, "health %":13}
		),
		Ability("9",
			{"type":"buff", "trigger":"passive"},
			{"physique %":16, "health %":14}
		),
		Ability("10",
			{"type":"buff", "trigger":"passive"},
			{"physique %":18, "health %":15}
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FSoldier%2FZolhan%27s%20Technique
Skill( "Zolhan's Technique", "Soldier", 
	["",
		Ability("1",
			{"type":"aar", "chance":.08, "recharge":0, "duration":2.8, "targets":2},
			{"weapon damage %":110, "internal":[44/2,2], "duration":{"reduce attack speed":15}}
		),
		Ability("2",
			{"type":"aar", "chance":.12, "recharge":0, "duration":3.6, "targets":2},
			{"weapon damage %":116, "internal":[54/2,2], "duration":{"reduce attack speed":18}}
		),
		Ability("3",
			{"type":"aar", "chance":.15, "recharge":0, "duration":4.3, "targets":2},
			{"weapon damage %":122, "internal":[66/2,2], "duration":{"reduce attack speed":21}}
		),
		Ability("4",
			{"type":"aar", "chance":.18, "recharge":0, "duration":5.0, "targets":2},
			{"weapon damage %":128, "internal":[78/2,2], "duration":{"reduce attack speed":23}}
		),
		Ability("5",
			{"type":"aar", "chance":.20, "recharge":0, "duration":5.6, "targets":2},
			{"weapon damage %":134, "internal":[88/2,2], "duration":{"reduce attack speed":25}}
		),
		Ability("6",
			{"type":"aar", "chance":.22, "recharge":0, "duration":6.2, "targets":2},
			{"weapon damage %":140, "internal":[96/2,2], "duration":{"reduce attack speed":27}}
		),
		Ability("7",
			{"type":"aar", "chance":.23, "recharge":0, "duration":6.8, "targets":2},
			{"weapon damage %":146, "internal":[106/2,2], "duration":{"reduce attack speed":28}}
		),
		Ability("8",
			{"type":"aar", "chance":.24, "recharge":0, "duration":7.4, "targets":2},
			{"weapon damage %":152, "internal":[116/2,2], "duration":{"reduce attack speed":29}}
		),
		Ability("9",
			{"type":"aar", "chance":.25, "recharge":0, "duration":8.0, "targets":2},
			{"weapon damage %":158, "internal":[126/2,2], "duration":{"reduce attack speed":30}}
		),
		Ability("10",
			{"type":"aar", "chance":.25, "recharge":0, "duration":8.6, "targets":2},
			{"weapon damage %":164, "internal":[140/2,2], "duration":{"reduce attack speed":31}}
		),
		Ability("11",
			{"type":"aar", "chance":.25, "recharge":0, "duration":9.2, "targets":2},
			{"weapon damage %":170, "internal":[152/2,2], "duration":{"reduce attack speed":32}}
		),
		Ability("12",
			{"type":"aar", "chance":.25, "recharge":0, "duration":10, "targets":2},
			{"weapon damage %":175, "internal":[168/2,2], "duration":{"reduce attack speed":33}}
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FSoldier%2FBlitz
# I'm setting the recharge to 30 seconds since it's intended to be an opener
# if this is intended to be used on cooldown it should be changed
Skill( "Blitz", "Soldier", 
	["",
		Ability("1",
			{"type":"attack", "trigger":"manual", "recharge":30, "targets":2},
			{"energy":-30, "weapon damage %":125, "physical":90, "stun %":100, "move speed":300}
		),
		Ability("2",
			{"type":"attack", "trigger":"manual", "recharge":30, "targets":2},
			{"energy":-33, "weapon damage %":138, "physical":111, "stun %":100, "move speed":300}
		),
		Ability("3",
			{"type":"attack", "trigger":"manual", "recharge":30, "targets":2},
			{"energy":-36, "weapon damage %":151, "physical":132, "stun %":100, "move speed":300}
		),
		Ability("4",
			{"type":"attack", "trigger":"manual", "recharge":30, "targets":2},
			{"energy":-39, "weapon damage %":164, "physical":152, "stun %":100, "move speed":300}
		),
		Ability("5",
			{"type":"attack", "trigger":"manual", "recharge":30, "targets":2},
			{"energy":-42, "weapon damage %":177, "physical":174, "stun %":100, "move speed":300}
		),
		Ability("6",
			{"type":"attack", "trigger":"manual", "recharge":30, "targets":2},
			{"energy":-45, "weapon damage %":190, "physical":195, "stun %":100, "move speed":300}
		),
		Ability("7",
			{"type":"attack", "trigger":"manual", "recharge":30, "targets":2},
			{"energy":-48, "weapon damage %":203, "physical":218, "stun %":100, "move speed":300}
		),
		Ability("8",
			{"type":"attack", "trigger":"manual", "recharge":30, "targets":2},
			{"energy":-52, "weapon damage %":216, "physical":241, "stun %":100, "move speed":300}
		),
	]
)

#wikiwiki.jp/gdcrate/?Masteries%2FSoldier%2FVeterancy
Skill( "Veterancy", "Soldier", 
	["",
		Ability("1",
			{"type":"buff", "trigger":"passive"},
			{"health/s":4, "constitution":10, "armor physique requirements":-3}
		),
		Ability("2",
			{"type":"buff", "trigger":"passive"},
			{"health/s":7, "constitution":18, "armor physique requirements":-5}
		),
		Ability("3",
			{"type":"buff", "trigger":"passive"},
			{"health/s":10, "constitution":25, "armor physique requirements":-8}
		),
		Ability("4",
			{"type":"buff", "trigger":"passive"},
			{"health/s":13, "constitution":32, "armor physique requirements":-10}
		),
		Ability("5",
			{"type":"buff", "trigger":"passive"},
			{"health/s":16, "constitution":38, "armor physique requirements":-12}
		),
		Ability("6",
			{"type":"buff", "trigger":"passive"},
			{"health/s":20, "constitution":43, "armor physique requirements":-14}
		),
		Ability("7",
			{"type":"buff", "trigger":"passive"},
			{"health/s":24, "constitution":48, "armor physique requirements":-15}
		),
		Ability("8",
			{"type":"buff", "trigger":"passive"},
			{"health/s":28, "constitution":52, "armor physique requirements":-16}
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FSoldier%2FWar%20Cry
# everything this grants is pretty hard to quantify right now. No point in the data entry
# Skill( "War Cry", "Soldier", 
# 	[""]
# )

#http://wikiwiki.jp/gdcrate/?Masteries%2FSoldier%2FField%20Command
# TODO I need to add the pet component into this
Skill( "Field Command", "Soldier", 
	["",
		Ability("1",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-75, "offense":8, "defense":8, "armor %":5}
		),
		Ability("2",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-85, "offense":16, "defense":16, "armor %":8}
		),
		Ability("3",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-95, "offense":24, "defense":24, "armor %":11}
		),
		Ability("4",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-105, "offense":32, "defense":32, "armor %":13}
		),
		Ability("5",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-115, "offense":40, "defense":40, "armor %":15}
		),
		Ability("6",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-125, "offense":47, "defense":47, "armor %":18}
		),
		Ability("7",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-135, "offense":54, "defense":54, "armor %":20}
		),
		Ability("8",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-145, "offense":61, "defense":61, "armor %":21}
		),
		Ability("9",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-155, "offense":68, "defense":68, "armor %":23}
		),
		Ability("10",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-165, "offense":74, "defense":74, "armor %":24}
		),
		Ability("11",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-175, "offense":80, "defense":80, "armor %":25}
		),
		Ability("12",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-185, "offense":86, "defense":86, "armor %":28}
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FSoldier%2FDecorated%20Soldier
Skill( "Decorated Soldier", "Soldier", 
	["",
		Ability("1",
			{"type":"buff", "trigger":"passive"},
			{"physical %":8, "internal %":8, "elemental resist":5, "slow resist":5}
		),
		Ability("2",
			{"type":"buff", "trigger":"passive"},
			{"physical %":14, "internal %":14, "elemental resist":8, "slow resist":8}
		),
		Ability("3",
			{"type":"buff", "trigger":"passive"},
			{"physical %":20, "internal %":20, "elemental resist":10, "slow resist":10}
		),
		Ability("4",
			{"type":"buff", "trigger":"passive"},
			{"physical %":26, "internal %":26, "elemental resist":12, "slow resist":12}
		),
		Ability("5",
			{"type":"buff", "trigger":"passive"},
			{"physical %":32, "internal %":32, "elemental resist":14, "slow resist":14}
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FSoldier%2FBlindside
# TODO implement "reduce defense"
Skill( "Blindside", "Soldier", 
	["",
		Ability("1",
			{"type":"modifier", "targets":1, "duration":4},
			{"energy":-3, "internal":[60/2,2], "physical %":32, "internal %":32, "duration":{"reduce defense":15}}
		),
		Ability("2",
			{"type":"modifier", "targets":1, "duration":4},
			{"energy":-3, "internal":[72/2,2], "physical %":48, "internal %":48, "duration":{"reduce defense":30}}
		),
		Ability("3",
			{"type":"modifier", "targets":1, "duration":4},
			{"energy":-4, "internal":[84/2,2], "physical %":64, "internal %":64, "duration":{"reduce defense":45}}
		),
		Ability("4",
			{"type":"modifier", "targets":1, "duration":4},
			{"energy":-4, "internal":[96/2,2], "physical %":80, "internal %":80, "duration":{"reduce defense":60}}
		),
	],
	"Blitz"
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FSoldier%2FSquad%20Tactics
# not linking this to field command as they're independent passives
Skill( "Squad Tactics", "Soldier", 
	["",
		Ability("1",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-22, "all damage %":8, "attack speed":3}
		),
		Ability("2",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-25, "all damage %":15, "attack speed":4}
		),
		Ability("3",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-28, "all damage %":22, "attack speed":5}
		),
		Ability("4",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-30, "all damage %":29, "attack speed":6}
		),
		Ability("5",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-32, "all damage %":36, "attack speed":7}
		),
		Ability("6",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-35, "all damage %":43, "attack speed":8}
		),
		Ability("7",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-38, "all damage %":50, "attack speed":9}
		),
		Ability("8",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-40, "all damage %":57, "attack speed":10}
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FSoldier%2FCounter%20Strike
# this is a pretty weird skill, it has an attack component and a buff component
# I'm going to slap a duration component in there. This won't be quite right since there's a time to activate component but once it activates it should stay on for the rest of the fight.
Skill( "Counter Strike", "Soldier", 
	["",
		Ability("1",
			{"type":"attack", "trigger":"hit", "chance":.2, "recharge":1, "targets":2, "duration":100},
			{"weapon damage %":12, "triggered physical":70, "triggered bleed":[33/3,3], "duration":{"energy/s":-.8, "energy":-25, "physical retaliation":35, "retaliation %":20}}
		),
		Ability("2",
			{"type":"attack", "trigger":"hit", "chance":.22, "recharge":1, "targets":2, "duration":100},
			{"weapon damage %":12, "triggered physical":88, "triggered bleed":[60/3,3], "duration":{"energy/s":-.8, "energy":-30, "physical retaliation":56, "retaliation %":26}}
		),
		Ability("3",
			{"type":"attack", "trigger":"hit", "chance":.23, "recharge":1, "targets":2, "duration":100},
			{"weapon damage %":12, "triggered physical":104, "triggered bleed":[84/3,3], "duration":{"energy/s":-.9, "energy":-35, "physical retaliation":77, "retaliation %":32}}
		),
		Ability("4",
			{"type":"attack", "trigger":"hit", "chance":.24, "recharge":1, "targets":2, "duration":100},
			{"weapon damage %":12, "triggered physical":123, "triggered bleed":[114/3,3], "duration":{"energy/s":-9, "energy":-40, "physical retaliation":98, "retaliation %":38}}
		),
		Ability("5",
			{"type":"attack", "trigger":"hit", "chance":.25, "recharge":1, "targets":2, "duration":100},
			{"weapon damage %":12, "triggered physical":141, "triggered bleed":[141/3,3], "duration":{"energy/s":1, "energy":-45, "physical retaliation":119, "retaliation %":44}}
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FSoldier%2FScars%20of%20Battle
Skill( "Scars of Battle", "Soldier", 
	["",
		Ability("1",
			{"type":"buff", "trigger":"passive"},
			{"armor absorb":5, "bleed resist":4, "reduced stun duration":4, "reduced freeze duration":4}
		),
		Ability("2",
			{"type":"buff", "trigger":"passive"},
			{"armor absorb":9, "bleed resist":8, "reduced stun duration":8, "reduced freeze duration":8}
		),
		Ability("3",
			{"type":"buff", "trigger":"passive"},
			{"armor absorb":12, "bleed resist":12, "reduced stun duration":12, "reduced freeze duration":12}
		),
		Ability("4",
			{"type":"buff", "trigger":"passive"},
			{"armor absorb":15, "bleed resist":16, "reduced stun duration":16, "reduced freeze duration":16}
		),
		Ability("5",
			{"type":"buff", "trigger":"passive"},
			{"armor absorb":18, "bleed resist":20, "reduced stun duration":20, "reduced freeze duration":20}
		),
		Ability("6",
			{"type":"buff", "trigger":"passive"},
			{"armor absorb":21, "bleed resist":24, "reduced stun duration":24, "reduced freeze duration":24}
		),
		Ability("7",
			{"type":"buff", "trigger":"passive"},
			{"armor absorb":23, "bleed resist":28, "reduced stun duration":28, "reduced freeze duration":28}
		),
		Ability("8",
			{"type":"buff", "trigger":"passive"},
			{"armor absorb":25, "bleed resist":32, "reduced stun duration":32, "reduced freeze duration":32}
		),
	]
)


#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FBrute%20Force
Skill( "Brute Force", "Shaman", 
	["",
		Ability("1",
			{"type":"buff", "trigger":"passive"},
			{"lightning":8, "physical %":6, "internal %":6, "internal duration":5}
		),
		Ability("2",
			{"type":"buff", "trigger":"passive"},
			{"lightning":14, "physical %":12, "internal %":12, "internal duration":10}
		),
		Ability("3",
			{"type":"buff", "trigger":"passive"},
			{"lightning":20, "physical %":18, "internal %":18, "internal duration":14}
		),
		Ability("4",
			{"type":"buff", "trigger":"passive"},
			{"lightning":25, "physical %":24, "internal %":24, "internal duration":17}
		),
		Ability("5",
			{"type":"buff", "trigger":"passive"},
			{"lightning":30, "physical %":30, "internal %":30, "internal duration":20}
		),
		Ability("6",
			{"type":"buff", "trigger":"passive"},
			{"lightning":36, "physical %":36, "internal %":36, "internal duration":22}
		),
		Ability("7",
			{"type":"buff", "trigger":"passive"},
			{"lightning":42, "physical %":42, "internal %":42, "internal duration":24}
		),
		Ability("8",
			{"type":"buff", "trigger":"passive"},
			{"lightning":47, "physical %":48, "internal %":48, "internal duration":26}
		),
		Ability("9",
			{"type":"buff", "trigger":"passive"},
			{"lightning":53, "physical %":54, "internal %":54, "internal duration":28}
		),
		Ability("10",
			{"type":"buff", "trigger":"passive"},
			{"lightning":59, "physical %":60, "internal %":60, "internal duration":30}
		),
		Ability("11",
			{"type":"buff", "trigger":"passive"},
			{"lightning":65, "physical %":66, "internal %":66, "internal duration":32}
		),
		Ability("12",
			{"type":"buff", "trigger":"passive"},
			{"lightning":71, "physical %":72, "internal %":72, "internal duration":33}
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FSavagery
# not really sure how to do this one due to the charges.
# the mechanics as I understand them are that the charge levels apply only to the weapon damage % and the flat damage component.
# I think I'll make the % the average of the stacks just for convenience
Skill("Savagery", "Shaman",
	["",
		Ability("1",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-1, "weapon damage %":100*.6916, "lightning":5*.6916, "bleed":[12/3*.6916, 3], "duration":{"lightning %":8, "bleed %":8}}
		),
		Ability("2",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-1, "weapon damage %":104*.6916, "lightning":7*.6916, "bleed":[21/3*.6916, 3], "duration":{"lightning %":13, "bleed %":13}}
		),
		Ability("3",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-1, "weapon damage %":108*.6916, "lightning":9*.6916, "bleed":[30/3*.6916, 3], "duration":{"lightning %":18, "bleed %":18}}
		),
		Ability("4",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-2, "weapon damage %":112*.6916, "lightning":11*.6916, "bleed":[39/3*.6916, 3], "duration":{"lightning %":23, "bleed %":23}}
		),
		Ability("5",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-2, "weapon damage %":116*.6916, "lightning":13*.6916, "bleed":[48/3*.6916, 3], "duration":{"lightning %":28, "bleed %":28}}
		),
		Ability("6",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-2, "weapon damage %":120*.6916, "lightning":15*.6916, "bleed":[57/3*.6916, 3], "duration":{"lightning %":33, "bleed %":33}}
		),
		Ability("7",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-3, "weapon damage %":123*.6916, "lightning":17*.6916, "bleed":[66/3*.6916, 3], "duration":{"lightning %":38, "bleed %":38}}
		),
		Ability("8",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-3, "weapon damage %":126*.6916, "lightning":19*.6916, "bleed":[75/3*.6916, 3], "duration":{"lightning %":43, "bleed %":43}}
		),
		Ability("9",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-4, "weapon damage %":129*.7471, "lightning":21*.7471, "bleed":[84/3*.7471, 3], "duration":{"lightning %":48, "bleed %":48}}
		),
		Ability("10",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-4, "weapon damage %":132*.7471, "lightning":24*.7471, "bleed":[93/3*.7471, 3], "duration":{"lightning %":54, "bleed %":54}}
		),
		Ability("11",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-5, "weapon damage %":135*.7471, "lightning":27*.7471, "bleed":[102/3*.7471, 3], "duration":{"lightning %":60, "bleed %":60}}
		),
		Ability("12",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-5, "weapon damage %":138*.7471, "lightning":30*.7471, "bleed":[111/3*.7471, 3], "duration":{"lightning %":66, "bleed %":66}}
		),
		Ability("13",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-6, "weapon damage %":141*.7471, "lightning":33*.7471, "bleed":[120/3*.7471, 3], "duration":{"lightning %":72, "bleed %":72}}
		),
		Ability("14",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-6, "weapon damage %":144*.7471, "lightning":36*.7471, "bleed":[129/3*.7471, 3], "duration":{"lightning %":78, "bleed %":78}}
		),
		Ability("15",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-7, "weapon damage %":147*.7471, "lightning":39*.7471, "bleed":[138/3*.7471, 3], "duration":{"lightning %":84, "bleed %":84}}
		),
		Ability("16",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-7, "weapon damage %":150*.7975, "lightning":42*.7975, "bleed":[147/3*.7975, 3], "duration":{"lightning %":90, "bleed %":90}}
		),
		Ability("17",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-7, "weapon damage %":152*.7975, "lightning":46*.7975, "bleed":[159/3*.7975, 3], "duration":{"lightning %":96, "bleed %":96}}
		),
		Ability("18",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-8, "weapon damage %":153*.7975, "lightning":50*.7975, "bleed":[171/3*.7975, 3], "duration":{"lightning %":102, "bleed %":102}}
		),
		Ability("19",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-8, "weapon damage %":155*.7975, "lightning":54*.7975, "bleed":[183/3*.7975, 3], "duration":{"lightning %":108, "bleed %":108}}
		),
		Ability("20",
			{"type":"aar", "chance":1, "recharge":0, "duration":100},
			{"energy":-8, "weapon damage %":156*.7975, "lightning":58*.7975, "bleed":[195/3*.7975, 3], "duration":{"lightning %":114, "bleed %":114}}
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FPrimal%20Strike
Skill("Primal Strike", "Shaman",
	[26,
		Ability("1",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-32, "weapon damage %":110, "triggered physical":18, "triggered lightning":(7+22)/2, "trigered bleed":[10/2,2], "stun %":100}			
		),
		Ability("2",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-35, "weapon damage %":124, "triggered physical":32, "triggered lightning":(14+34)/2, "trigered bleed":[20/2,2], "stun %":100}			
		),
		Ability("3",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-38, "weapon damage %":138, "triggered physical":46, "triggered lightning":(20+46)/2, "trigered bleed":[30/2,2], "stun %":100}			
		),
		Ability("4",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-42, "weapon damage %":149, "triggered physical":60, "triggered lightning":(26+58)/2, "trigered bleed":[40/2,2], "stun %":100}			
		),
		Ability("5",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-46, "weapon damage %":159, "triggered physical":74, "triggered lightning":(33+70)/2, "trigered bleed":[50/2,2], "stun %":100}			
		),
		Ability("6",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-50, "weapon damage %":169, "triggered physical":88, "triggered lightning":(40+82)/2, "trigered bleed":[60/2,2], "stun %":100}			
		),
		Ability("7",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-54, "weapon damage %":178, "triggered physical":102, "triggered lightning":(47+95)/2, "trigered bleed":[70/2,2], "stun %":100}			
		),
		Ability("8",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-58, "weapon damage %":187, "triggered physical":116, "triggered lightning":(54+108)/2, "trigered bleed":[80/2,2], "stun %":100}			
		),
		Ability("9",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-62, "weapon damage %":196, "triggered physical":130, "triggered lightning":(61+121)/2, "trigered bleed":[90/2,2], "stun %":100}			
		),
		Ability("10",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-66, "weapon damage %":204, "triggered physical":145, "triggered lightning":(68+134)/2, "trigered bleed":[100/2,2], "stun %":100}			
		),
		Ability("11",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-70, "weapon damage %":212, "triggered physical":160, "triggered lightning":(75+147)/2, "trigered bleed":[110/2,2], "stun %":100}			
		),
		Ability("12",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-74, "weapon damage %":219, "triggered physical":176, "triggered lightning":(82+160)/2, "trigered bleed":[120/2,2], "stun %":100}			
		),
		Ability("13",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-78, "weapon damage %":227, "triggered physical":191, "triggered lightning":(90+173)/2, "trigered bleed":[130/2,2], "stun %":100}			
		),
		Ability("14",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-82, "weapon damage %":234, "triggered physical":206, "triggered lightning":(98+186)/2, "trigered bleed":[140/2,2], "stun %":100}			
		),
		Ability("15",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-86, "weapon damage %":242, "triggered physical":222, "triggered lightning":(106+200)/2, "trigered bleed":[150/2,2], "stun %":100}			
		),
		Ability("16",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-90, "weapon damage %":250, "triggered physical":240, "triggered lightning":(115+214)/2, "trigered bleed":[160/2,2], "stun %":100}			
		),
		Ability("17",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-94, "weapon damage %":255, "triggered physical":257, "triggered lightning":(124+228)/2, "trigered bleed":[172/2,2], "stun %":100}			
		),
		Ability("18",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"energy":-98, "weapon damage %":260, "triggered physical":274, "triggered lightning":(133+242)/2, "trigered bleed":[184/2,2], "stun %":100}			
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FMight%20of%20the%20Bear
Skill("Might of the Bear", "Shaman",
	[3,
		Ability("1",
			{"type":"modifier"},
			{"ability damage %":6, "physical resist":3}
		),
		Ability("2",
			{"type":"modifier"},
			{"ability damage %":12, "physical resist":5}
		),
		Ability("3",
			{"type":"modifier"},
			{"ability damage %":18, "physical resist":8}
		),
	],
	"Savagery"
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FMogdrogen%27s%20Pact
Skill("Mogdrogen's Pact", "Shaman",
	["",
		Ability("1",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-50, "physical":(3+6)/2, "pet physical":(3+6)/2, "health/s":3, "pet health/s":3, "energy/s":0.8}
		),
		Ability("2",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-60, "physical":(5+8)/2, "pet physical":(5+8)/2, "health/s":6, "pet health/s":6, "energy/s":1.4}
		),
		Ability("3",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-70, "physical":(6+10)/2, "pet physical":(6+10)/2, "health/s":8, "pet health/s":8, "energy/s":2.0}
		),
		Ability("4",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-80, "physical":(8+12)/2, "pet physical":(8+12)/2, "health/s":10, "pet health/s":10, "energy/s":2.5}
		),
		Ability("5",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-90, "physical":(9+14)/2, "pet physical":(9+14)/2, "health/s":12, "pet health/s":12, "energy/s":3}
		),
		Ability("6",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-100, "physical":(11+16)/2, "pet physical":(11+16)/2, "health/s":15, "pet health/s":15, "energy/s":3.5}
		),
		Ability("7",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-110, "physical":(12+18)/2, "pet physical":(12+18)/2, "health/s":18, "pet health/s":18, "energy/s":4.0}
		),
		Ability("8",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-120, "physical":(14+20)/2, "pet physical":(14+20)/2, "health/s":21, "pet health/s":21, "energy/s":4.5}
		),
		Ability("9",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-130, "physical":(16+22)/2, "pet physical":(16+22)/2, "health/s":24, "pet health/s":24, "energy/s":5.0}
		),
		Ability("10",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-140, "physical":21, "pet physical":21, "health/s":27, "pet health/s":27, "energy/s":5.5}
		),
		Ability("11",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-150, "physical":23, "pet physical":23, "health/s":30, "pet health/s":30, "energy/s":6.0}
		),
		Ability("12",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-160, "physical":26, "pet physical":26, "health/s":34, "pet health/s":34, "energy/s":6.5}
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FFeral%20Hunger
# this skill is TECHNICALLY a child of Brute Force but they appear to be completely independent
#TODO verify that lifesteal is being used correctly (applied to only the given attack, adding to health, etc)
Skill("Feral Hunger", "Shaman",
	["",
		Ability("1",
			{"type":"aar", "chance":.08, "targets":2},
			{"weapon damage %":110, "bleed":[28/2,2], "lifesteal %":10}
		),
		Ability("2",
			{"type":"aar", "chance":.12, "targets":2},
			{"weapon damage %":116, "bleed":[48/2,2], "lifesteal %":14}
		),
		Ability("3",
			{"type":"aar", "chance":.15, "targets":2},
			{"weapon damage %":121, "bleed":[68/2,2], "lifesteal %":17}
		),
		Ability("4",
			{"type":"aar", "chance":.18, "targets":2},
			{"weapon damage %":127, "bleed":[88/2,2], "lifesteal %":20}
		),
		Ability("5",
			{"type":"aar", "chance":.20, "targets":2},
			{"weapon damage %":132, "bleed":[108/2,2], "lifesteal %":23}
		),
		Ability("6",
			{"type":"aar", "chance":.22, "targets":2},
			{"weapon damage %":138, "bleed":[124/2,2], "lifesteal %":25}
		),
		Ability("7",
			{"type":"aar", "chance":.23, "targets":2},
			{"weapon damage %":143, "bleed":[146/2,2], "lifesteal %":27}
		),
		Ability("8",
			{"type":"aar", "chance":.25, "targets":2},
			{"weapon damage %":149, "bleed":[164/2,2], "lifesteal %":29}
		),
		Ability("9",
			{"type":"aar", "chance":.25, "targets":2},
			{"weapon damage %":154, "bleed":[184/2,2], "lifesteal %":31}
		),
		Ability("10",
			{"type":"aar", "chance":.25, "targets":2},
			{"weapon damage %":160, "bleed":[204/2,2], "lifesteal %":33}
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FWind%20Devil
#TODO

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FSummon%20Briarthorn
#TODO

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FTorrent
Skill("Torrent", "Shaman",
	[22,
		Ability("1",
			{"type":"attack", "trigger":"parent", "targets":2},
			{"weapon damage %":10, "triggered lightning":(5+60)/2}
		),
		Ability("2",
			{"type":"attack", "trigger":"parent", "targets":2},
			{"weapon damage %":13, "triggered lightning":(13+80)/2}
		),
		Ability("3",
			{"type":"attack", "trigger":"parent", "targets":2},
			{"weapon damage %":16, "triggered lightning":(21+100)/2}
		),
		Ability("4",
			{"type":"attack", "trigger":"parent", "targets":2},
			{"weapon damage %":19, "triggered lightning":(29+120)/2}
		),
		Ability("5",
			{"type":"attack", "trigger":"parent", "targets":2},
			{"weapon damage %":22, "triggered lightning":(37+140)/2}
		),
		Ability("6",
			{"type":"attack", "trigger":"parent", "targets":2.5},
			{"weapon damage %":24, "triggered lightning":(45+154)/2}
		),
		Ability("7",
			{"type":"attack", "trigger":"parent", "targets":2.5},
			{"weapon damage %":26, "triggered lightning":(53+168)/2}
		),
		Ability("8",
			{"type":"attack", "trigger":"parent", "targets":2.5},
			{"weapon damage %":28, "triggered lightning":(61+182)/2}
		),
		Ability("9",
			{"type":"attack", "trigger":"parent", "targets":2.5},
			{"weapon damage %":30, "triggered lightning":(69+196)/2}
		),
		Ability("10",
			{"type":"attack", "trigger":"parent", "targets":2.5},
			{"weapon damage %":32, "triggered lightning":(77+210)/2}
		),
		Ability("11",
			{"type":"attack", "trigger":"parent", "targets":2.5},
			{"weapon damage %":34, "triggered lightning":(85+224)/2}
		),
		Ability("12",
			{"type":"attack", "trigger":"parent", "targets":3},
			{"weapon damage %":36, "triggered lightning":(93+238)/2}
		),
		Ability("13",
			{"type":"attack", "trigger":"parent", "targets":3},
			{"weapon damage %":37, "triggered lightning":(102+253)/2}
		),
		Ability("14",
			{"type":"attack", "trigger":"parent", "targets":3.5},
			{"weapon damage %":38, "triggered lightning":(111+268)/2}
		),
	],
	"Primal Strike"
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FTenacity%20of%20the%20Boar
Skill("Tenacity of the Boar", "Shaman",
	[22,
		Ability("1",
			{"type":"modifier"},
			{"energy":-1, "duration":{"offense":12, "defense":10, "health/s %":10, "slow resist":5}}
		),
		Ability("2",
			{"type":"modifier"},
			{"energy":-1, "duration":{"offense":20, "defense":16, "health/s %":20, "slow resist":7}}
		),
		Ability("3",
			{"type":"modifier"},
			{"energy":-1, "duration":{"offense":28, "defense":22, "health/s %":28, "slow resist":9}}
		),
		Ability("4",
			{"type":"modifier"},
			{"energy":-1, "duration":{"offense":36, "defense":28, "health/s %":36, "slow resist":11}}
		),
		Ability("5",
			{"type":"modifier"},
			{"energy":-1, "duration":{"offense":44, "defense":34, "health/s %":44, "slow resist":13}}
		),
		Ability("6",
			{"type":"modifier"},
			{"energy":-1, "duration":{"offense":53, "defense":41, "health/s %":52, "slow resist":15}}
		),
		Ability("7",
			{"type":"modifier"},
			{"energy":-1, "duration":{"offense":62, "defense":48, "health/s %":60, "slow resist":17}}
		),
		Ability("8",
			{"type":"modifier"},
			{"energy":-2, "duration":{"offense":71, "defense":55, "health/s %":68, "slow resist":19}}
		),
	],
	"Savagery"
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FHeart%20of%20the%20Wild
# no need to link, it works standalone
Skill("Heart of the Wild", "Shaman",
	[20,
		Ability("1",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-50, "health %":3, "reduced poison duration":2, "reduced bleed time":2}
		),
		Ability("2",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-60, "health %":6, "reduced poison duration":5, "reduced bleed time":5}
		),
		Ability("3",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-70, "health %":9, "reduced poison duration":8, "reduced bleed time":8}
		),
		Ability("4",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-80, "health %":12, "reduced poison duration":11, "reduced bleed time":11}
		),
		Ability("5",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-90, "health %":15, "reduced poison duration":14, "reduced bleed time":14}
		),
		Ability("6",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-100, "health %":18, "reduced poison duration":16, "reduced bleed time":16}
		),
		Ability("7",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-110, "health %":21, "reduced poison duration":18, "reduced bleed time":18}
		),
		Ability("8",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-120, "health %":24, "reduced poison duration":20, "reduced bleed time":20}
		),
		Ability("9",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-130, "health %":27, "reduced poison duration":22, "reduced bleed time":22}
		),
		Ability("10",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-140, "health %":30, "reduced poison duration":25, "reduced bleed time":25}
		),
		Ability("11",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-150, "health %":31, "reduced poison duration":26, "reduced bleed time":26}
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FWendigo%20Totem
#TODO skipping for now

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FRaging%20Tempest
#TODO

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FStorm%20Surge
Skill("Storm Surge", "Shaman",
	[22,
		Ability("1",
			{"type":"modifier"},
			{"energy":-3, "triggered lightning":(9+14)/2, "triggered electrocute":[78/3,3], "physical %":8, "bleed %":8, "bleed duration":30}
		),
		Ability("2",
			{"type":"modifier"},
			{"energy":-3, "triggered lightning":(12+21)/2, "triggered electrocute":[132/3,3], "physical %":16, "bleed %":16, "bleed duration":40}
		),
		Ability("3",
			{"type":"modifier"},
			{"energy":-4, "triggered lightning":(15+28)/2, "triggered electrocute":[186/3,3], "physical %":24, "bleed %":24, "bleed duration":49}
		),
		Ability("4",
			{"type":"modifier"},
			{"energy":-4, "triggered lightning":(18+35)/2, "triggered electrocute":[240/3,3], "physical %":32, "bleed %":32, "bleed duration":57}
		),
		Ability("5",
			{"type":"modifier"},
			{"energy":-5, "triggered lightning":(21+42)/2, "triggered electrocute":[294/3,3], "physical %":40, "bleed %":40, "bleed duration":64}
		),
		Ability("6",
			{"type":"modifier"},
			{"energy":-5, "triggered lightning":(24+49)/2, "triggered electrocute":[348/3,3], "physical %":48, "bleed %":48, "bleed duration":70}
		),
		Ability("7",
			{"type":"modifier"},
			{"energy":-6, "triggered lightning":(27+56)/2, "triggered electrocute":[402/3,3], "physical %":56, "bleed %":56, "bleed duration":75}
		),
		Ability("8",
			{"type":"modifier"},
			{"energy":-6, "triggered lightning":(30+63)/2, "triggered electrocute":[456/3,3], "physical %":64, "bleed %":64, "bleed duration":80}
		),
		Ability("9",
			{"type":"modifier"},
			{"energy":-7, "triggered lightning":(33+70)/2, "triggered electrocute":[510/3,3], "physical %":72, "bleed %":72, "bleed duration":85}
		),
		Ability("10",
			{"type":"modifier"},
			{"energy":-7, "triggered lightning":(36+77)/2, "triggered electrocute":[564/3,3], "physical %":80, "bleed %":80, "bleed duration":90}
		),
		Ability("11",
			{"type":"modifier"},
			{"energy":-8, "triggered lightning":(39+84)/2, "triggered electrocute":[618/3,3], "physical %":88, "bleed %":88, "bleed duration":95}
		),
	],
	"Primal Strike"
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FOak%20Skin
# not linking since it's independent
Skill("Oak Skin", "Shaman",
	[20,
		Ability("1",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-50, "health/s %":6, "armor":15, "pierce resist":3, "retaliation %":10}
		),
		Ability("2",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-60, "health/s %":9, "armor":23, "pierce resist":6, "retaliation %":20}
		),
		Ability("3",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-70, "health/s %":12, "armor":31, "pierce resist":10, "retaliation %":30}
		),
		Ability("4",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-80, "health/s %":15, "armor":39, "pierce resist":14, "retaliation %":40}
		),
		Ability("5",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-90, "health/s %":17, "armor":49, "pierce resist":18, "retaliation %":50}
		),
		Ability("6",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-100, "health/s %":20, "armor":59, "pierce resist":22, "retaliation %":60}
		),
		Ability("7",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-110, "health/s %":22, "armor":69, "pierce resist":25, "retaliation %":70}
		),
		Ability("8",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-120, "health/s %":25, "armor":81, "pierce resist":28, "retaliation %":80}
		),
		Ability("9",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-130, "health/s %":27, "armor":93, "pierce resist":32, "retaliation %":90}
		),
		Ability("10",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-140, "health/s %":30, "armor":105, "pierce resist":36, "retaliation %":100}
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FStorm%20Totem
#TODO skipping for now since it's a "pet"

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FStorm%20Touched
Skill("Storm Touched", "Shaman",
	[22,
		Ability("1",
			{"type":"modifier"},
			{"energy":-1, "triggered electrocute":[(42+96)/2/3, 3], "duration":{"physical %":6, "lightning %":60*.2, "attack speed":3}}
		),
		Ability("2",
			{"type":"modifier"},
			{"energy":-1, "triggered electrocute":[(60+132)/2/3, 3], "duration":{"physical %":10, "lightning %":80*.2, "attack speed":5}}
		),
		Ability("3",
			{"type":"modifier"},
			{"energy":-1, "triggered electrocute":[(78+156)/2/3, 3], "duration":{"physical %":14, "lightning %":100*.2, "attack speed":6}}
		),
		Ability("4",
			{"type":"modifier"},
			{"energy":-1, "triggered electrocute":[(96+186)/2/3, 3], "duration":{"physical %":18, "lightning %":120*.2, "attack speed":7}}
		),
		Ability("5",
			{"type":"modifier"},
			{"energy":-1, "triggered electrocute":[(114+216)/2/3, 3], "duration":{"physical %":22, "lightning %":140*.2, "attack speed":7}}
		),
		Ability("6",
			{"type":"modifier"},
			{"energy":-1, "triggered electrocute":[(132+246)/2/3, 3], "duration":{"physical %":26, "lightning %":160*.2, "attack speed":8}}
		),
		Ability("7",
			{"type":"modifier"},
			{"energy":-1, "triggered electrocute":[(150+276)/2/3, 3], "duration":{"physical %":30, "lightning %":180*.2, "attack speed":9}}
		),
		Ability("8",
			{"type":"modifier"},
			{"energy":-2, "triggered electrocute":[(168+306)/2/3, 3], "duration":{"physical %":34, "lightning %":200*.2, "attack speed":9}}
		),
		Ability("9",
			{"type":"modifier"},
			{"energy":-2, "triggered electrocute":[(186+336)/2/3, 3], "duration":{"physical %":38, "lightning %":220*.2, "attack speed":10}}
		),
		Ability("10",
			{"type":"modifier"},
			{"energy":-2, "triggered electrocute":[(204+366)/2/3, 3], "duration":{"physical %":42, "lightning %":240*.2, "attack speed":11}}
		),
		Ability("11",
			{"type":"modifier"},
			{"energy":-2, "triggered electrocute":[(222+396)/2/3, 3], "duration":{"physical %":46, "lightning %":260*.2, "attack speed":11}}
		),
		Ability("12",
			{"type":"modifier"},
			{"energy":-2, "triggered electrocute":[(240+426)/2/3, 3], "duration":{"physical %":50, "lightning %":280*.2, "attack speed":12	}}
		),
	],
	"Savagery"
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FBlood%20Pact
#TODO implement when I do wendigo totem

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FMaelstrom
#TODO implement when I do wind devil

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FEmboldening%20Presence
# Not linking to Summon Briarthorn since it's a standalone buff
#TODO implement pet bonuses since it's an aura stuff
Skill( "Emboldening Presence", "Shaman", 
	[22,
		Ability("1",
			{"type":"buff", "trigger":"toggle"},
			{"all damage %":5, "offense":5, "physical resist":1, "bleed resist":3, "retaliation %":12}
		),
		Ability("2",
			{"type":"buff", "trigger":"toggle"},
			{"all damage %":10, "offense":12, "physical resist":2, "bleed resist":6, "retaliation %":20}
		),
		Ability("3",
			{"type":"buff", "trigger":"toggle"},
			{"all damage %":14, "offense":18, "physical resist":3, "bleed resist":9, "retaliation %":28}
		),
		Ability("4",
			{"type":"buff", "trigger":"toggle"},
			{"all damage %":18, "offense":24, "physical resist":4, "bleed resist":12, "retaliation %":36}
		),
		Ability("5",
			{"type":"buff", "trigger":"toggle"},
			{"all damage %":22, "offense":30, "physical resist":5, "bleed resist":15, "retaliation %":44}
		),
		Ability("6",
			{"type":"buff", "trigger":"toggle"},
			{"all damage %":26, "offense":36, "physical resist":6, "bleed resist":18, "retaliation %":52}
		),
		Ability("7",
			{"type":"buff", "trigger":"toggle"},
			{"all damage %":30, "offense":42, "physical resist":7, "bleed resist":21, "retaliation %":60}
		),
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FStormcaller%27s%20Pact
Skill( "Stormcaller's Pact", "Shaman", 
	[22,
		Ability("1",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(24+39)/2/3,3], "crit damage":8, "lightning":65*.33, "frostburn %":25, "electrocute %":25, "physical to lightning":15}
		),
		Ability("2",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(30+51)/2/3,3], "crit damage":13, "lightning":90*.33, "frostburn %":35, "electrocute %":35, "physical to lightning":15}
		),
		Ability("3",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(36+60)/2/3,3], "crit damage":18, "lightning":116*.33, "frostburn %":45, "electrocute %":45, "physical to lightning":15}
		),
		Ability("4",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(42+72)/2/3,3], "crit damage":22, "lightning":142*.33, "frostburn %":55, "electrocute %":55, "physical to lightning":15}
		),
		Ability("5",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(48+81)/2/3,3], "crit damage":25, "lightning":168*.33, "frostburn %":65, "electrocute %":65, "physical to lightning":15}
		),
		Ability("6",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(54+93)/2/3,3], "crit damage":27, "lightning":194*.33, "frostburn %":75, "electrocute %":75, "physical to lightning":15}
		),
		Ability("7",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(60+102)/2/3,3], "crit damage":29, "lightning":220*.33, "frostburn %":85, "electrocute %":85, "physical to lightning":15}
		),
		Ability("8",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(66+114)/2/3,3], "crit damage":31, "lightning":246*.33, "frostburn %":95, "electrocute %":95, "physical to lightning":15}
		),
		Ability("9",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(72+123)/2/3,3], "crit damage":32, "lightning":272*.33, "frostburn %":105, "electrocute %":105, "physical to lightning":15}
		),
		Ability("10",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(78+135)/2/3,3], "crit damage":33, "lightning":298*.33, "frostburn %":115, "electrocute %":115, "physical to lightning":15}
		),
		Ability("11",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(84+144)/2/3,3], "crit damage":34, "lightning":324*.33, "frostburn %":125, "electrocute %":125, "physical to lightning":15}
		),
		Ability("12",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(90+156)/2/3,3], "crit damage":35, "lightning":350*.33, "frostburn %":135, "electrocute %":135, "physical to lightning":15}
		),
		Ability("13",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(99+168)/2/3,3], "crit damage":37, "lightning":372*.33, "frostburn %":143, "electrocute %":143, "physical to lightning":15}
		),
		Ability("14",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(105+180)/2/3,3], "crit damage":40, "lightning":394*.33, "frostburn %":150, "electrocute %":150, "physical to lightning":15}
		),
		Ability("15",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(114+192)/2/3,3], "crit damage":43, "lightning":416*.33, "frostburn %":158, "electrocute %":158, "physical to lightning":15}
		),
		Ability("16",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(120+204)/2/3,3], "crit damage":46, "lightning":438*.33, "frostburn %":165, "electrocute %":165, "physical to lightning":15}
		),
		Ability("17",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(129+216)/2/3,3], "crit damage":50, "lightning":460*.33, "frostburn %":173, "electrocute %":173, "physical to lightning":15}
		),
		Ability("18",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(138+231)/2/3,3], "crit damage":54, "lightning":482*.33, "frostburn %":180, "electrocute %":180, "physical to lightning":15}
		),
		Ability("19",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(147+246)/2/3,3], "crit damage":58, "lightning":504*.33, "frostburn %":188, "electrocute %":188, "physical to lightning":15}
		),
		Ability("20",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(156+267)/2/3,3], "crit damage":62, "lightning":526*.33, "frostburn %":195, "electrocute %":195, "physical to lightning":15}
		),
		Ability("21",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(168+288)/2/3,3], "crit damage":66, "lightning":548*.33, "frostburn %":203, "electrocute %":203, "physical to lightning":15}
		),
		Ability("22",
			{"type":"buff", "trigger":"toggle"},
			{"electrocute":[(186+327)/2/3,3], "crit damage":70, "lightning":570*.33, "frostburn %":210, "electrocute %":210, "physical to lightning":15}
		)
	]
)

#http://wikiwiki.jp/gdcrate/?Masteries%2FShaman%2FConjure%20Primal%20Spirit
#TODO skipping pet for now