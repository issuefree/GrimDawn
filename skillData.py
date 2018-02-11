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
# TODO I don't have a good way of handling skill modifiers at this time so I'm skipping this one
# Skill( "Blindside", "Soldier", 
# 	[""]
# )

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