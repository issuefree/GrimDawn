from dataModel import *
from itemData import *
from constellationData import *

devotionPoints = 52

stats = {
		"level":85,
		"difficulty":1,
		# estimate how frequent combat events are for calculating dynamic stats and abilities
		"attacks/s":2,
		"allAttacks/s":[
			2,	#savagery
			2,	#storm totem
			1,	#wind devil
			.33,#primal strike
		],
		"hits/s":2,
		"blocks/s":0,
		"kills/s":1.5,	
		"crit chance":.2,
		"low healths/s":1.0/20, # total guesswork.

		"fight length":10, # average length of a fight... this is for weighting abilities and over time effects. If you rely on wearing down opponents this should be long. If you are a glass cannon this should be small.

		# estimated sheet stats for target level
		"physique":842,
		"cunning":388,
		"spirit":488,

		"offense":2128,
		"defense":1722,

		"health":10331,
		"health/s":249,
		"health/s %":9+18+18+8+6+6+6+11+10+40,

		"armor":1507,
		# "armor absorb":76,

		"energy":2265,
		"energy/s":19.08,
		"energy/s %":154.9,
		
		"physical %":420+159,
		"lightning %":1523+229,
		"electrocute %":1280+244,

		"playStyle":"melee", # playstyle for weighting constellation abilities. [ranged/shortranged/melee/tank]
		"weapons":[
			"twohand", "2h-axe"
		],
		"blacklist":[
			# list of constellations that I want to manually exclude for some reason.
		]	
	}

weights = {
		"armor":2.5, "armor absorb":30,
		"avoid melee":30, "avoid ranged":25,
		"defense":15,

		"attack speed":75,
		"cast speed":25,

		"offense":20,
		# "crit damage":20,
		
		"health":1.5,
		"energy":1,
		"lifesteal %":100,

		"electrocute":20, "electrocute %":10, "electrocute duration":2.5,
		"physical":9, "physical %":7.5,
		"lightning":25, "lightning %":30,
		"bleed":7, "bleed %":3,
		"cold":10, "cold %":2,
		"frostburn":10,
		"internal":7.5,
		"burn":7.5,
		"aether":7.5,
		"fire":9,

		"physical to lightning":5,
		"physical to elemental":1,

		"weapon damage %":200, 
		"attack opportunity cost":-250-100-50, # I like basic attacks since they stack my savagery plus the auto attack replacements

		"resist":5,
		"physical resist":125,

		"pierce resist":20,
		"fire resist":0, 
		"cold resist":0, 
		"lightning resist":0, 
		"bleed resist":20,
		"acid resist":5,
		"aether resist":1,
		"chaos resist":25,
		"vitality resist":10,

		"stun %":25,
		"stun duration":5,

		"move speed":20,

		# scales with pet damage and we're not using that
		"Bysmiel's Command":0,
		"Shepherd's Call":0,
	}

items = [

	Item( "Ultos' Hood",
		{"armor":939, "lightning %":57, "electrocute %":57, "health":520, "physical resist":3, "cold resist":40, "vitality resist":25, "reduce cooldown":5, "Torrent":3}, 
		"head"
	),
	Item.getByName("Sacred Plating", components),
	Item.getByName("Kingsguard Powder", augments),

	Item( "Ultos' Stormseeker",
		{"physical":(270+386)/2, "attacks/s":1.45, "lightning":(5+53)/2, "lightning %":203, "electrocute %":203, "physical to lightning":45, "offense":18, "attack speed":16, "cast speed":16, "reduce cooldown":16, "Stormcaller's Pact":3},
		"twohand",
		Ability( "Lightning Nova",
			{"type":"attack", "trigger":"attack", "chance":.15, "recharge":1.8, "shape":"aoe", "targets":3},
			{"triggered lightning":(172+400)/2}
		)
	),
	Item.getByName("Bloody Whetstone", components),
	Item.getByName("Potent Creed's Cunning", augments),

	Item( "Ultos' Gem",
		{"lightning %":73, "electrocute %":73, "physical to lightning":10, "offense":34, "defense":30, "lightning resist":22, "chaos resist":15, "max lightning resist":8, "reduce cooldown":6, "Primal Strike":2, "Storm Surge":2},
		"amulet"
	),
	Item.getByName("Seal of Annihilation", components),
	Item.getByName("Kymon's Vision", augments),

	# Item( "Glyph of Kelphat'Zoth",
	# 	{"lightning":(1+13)/2, "vitality":9, "lightning %":46, "electrocute %":46, "defense":22, "elemental resist":35, "Stormcaller's Pact":2, "Conjure Primal Spirit":2, "pet crit damage":5, "pet lightning %":91, "pet total speed":8},
	# 	"ring",
	# 	Ability( "Glyph of Kelphat'Zoth",
	# 		{"type":"buff", "trigger":"attack", "chance":.1, "recharge":15, "duration":10},
	# 		{"lightning":(3+38)/2, "lightning %":50, "pet lightning":(3+18)/2, "pet lightning %":50, "pet physical to lightning":25}
	# 	)
	# ),
	# Item( "Glyph of Kelphat'Zoth",
	# 	{"lightning":(1+13)/2, "vitality":9, "lightning %":46, "electrocute %":46, "defense":22, "elemental resist":35, "Stormcaller's Pact":2, "Conjure Primal Spirit":2, "pet crit damage":5, "pet lightning %":91, "pet total speed":8},
	# 	"ring",
	# 	Ability( "Glyph of Kelphat'Zoth",
	# 		{"type":"buff", "trigger":"attack", "chance":.1, "recharge":15, "duration":10},
	# 		{"lightning":(3+38)/2, "lightning %":50, "pet lightning":(3+18)/2, "pet lightning %":50, "pet physical to lightning":25}
	# 	)
	# ),
	Item( "Mythical Glyph of Kelphat'Zoth",
		{"lightning":(1+18)/2, "vitality":10, "lightning %":91, "electrocute %":91, "defense":27, "elemental resist":37, "Stormcaller's Pact":2, "Conjure Primal Spirit":2, "Inquisitor's Seal":2,
		"pet crit damage":6, "pet lightning %":168, "pet total speed":9},
		"ring",
		Ability( "Glyph of Kelphat'Zoth",
			{"type":"buff", "trigger":"attack", "chance":.1, "recharge":15, "duration":10},
			{"lightning":(6+50)/2, "lightning %":125, "pet lightning":(5+21)/2, "pet lightning %":125, "pet physical to lightning":25}
		)
	),
	Item.getByName("Corpse Dust", components),
	Item.getByName("Survivor's Ingenuity", augments),

	Item( "Mythical Glyph of Kelphat'Zoth",
		{"lightning":(1+18)/2, "vitality":10, "lightning %":91, "electrocute %":91, "defense":27, "elemental resist":37, "Stormcaller's Pact":2, "Conjure Primal Spirit":2, "Inquisitor's Seal":2,
		"pet crit damage":6, "pet lightning %":168, "pet total speed":9},
		"ring",
		Ability( "Glyph of Kelphat'Zoth",
			{"type":"buff", "trigger":"attack", "chance":.1, "recharge":15, "duration":10},
			{"lightning":(6+50)/2, "lightning %":125, "pet lightning":(5+21)/2, "pet lightning %":125, "pet physical to lightning":25}
		)
	),
	Item.getByName("Corpse Dust", components),
	Item.getByName("Survivor's Ingenuity", augments),

	Item( "Ultos' Cuirass",
		{"armor":1071, "physical %":39, "lightning %":55, "internal %":39, "electrocute %":55, "electrocute duration":39, "health":540, "aether resist":22, "elemental resist":20, "Storm Touched":2, "Torrent":2},
		"chest"
	),
	Item.getByName("Chains of Oleron", components),
	Item.getByName("Kingsguard Powder", augments),

	Item( "Ultos' Spaulders",
		{"armor":939, "physical %":42, "lightning %":60, "internal %":42, "electrocute %":60, "offense":66, "defense":16, "physical resist":4, "lightning resist":33, "Savagery":2, "Primal Strike":2},
		"shoulders"
	),
	Item.getByName("Sacred Plating", components),
	Item.getByName("Kingsguard Powder", augments),

	# Item( "Empowered Thundertouch Bracers",
	# 	{"armor":589, "electrocute":[39/3, 3], "physical %":41, "lightning %":62, "cunning":32, "lightning resist":25, "aether resist":10, "Storm Surge":2, "Brute Force":2},
	# 	"arms",
	# 	Ability( "Lightning Bolt",
	# 		{"type":"attack", "trigger":"attack", "chance":.1, "recharge":2.5, "targets":1},
	# 		{"triggered lightning":(87+418)/2, "triggered electrocute":[218/2,2], "stun %":100}
	# 	)
	# ),
	Item( "Mythical Touch of the Everliving Grove",
		{"armor":1014, "health":452, "health %":4, "health/s":26, "health/s %":40, "elemental resist":18, "Hearth of the Wild":2, "Oak Skin":2,
		"pet health %":10, "pet defense %":12, "pet vitality resist":39},
		"arms",
		Ability( "Healing WInds",
			{"type":"heal", "trigger":"attack", "chance":.1, "recharge":6},
			{"health %":3, "health":1650}
		)
	),
	Item.getByName("Spellwoven Threads", components),
	Item.getByName("Kingsguard Powder", augments),

	Item( "Stormcage Legguards",
		{"armor":1190, "lightning %":81, "electrocute %":81, "spirit %":6, "offense":38, "defense":18, "electrocute retaliation":840, "Full Spread":2, "Maelstrom":2},
		"legs",
		Ability( "Chain Lightning",
			{"type":"attack", "trigger":"hit", "chance":.2, "recharge":2, "targets":2},
			{"triggered lightning":(124+406)/2}
		)
	),
	Item.getByName("Ancient Armor Plate", components),
	Item.getByName("Kingsguard Powder", augments),

	Item( "Stormtitan Treads",
		{"armor":1012, "lightning %":36, "electrocute %":36, "health":540, "health %":3, "move speed":10, "lightning resist":26, "reduced stun duration":25, "lightning retaliation":(1+606)/2, "Counter Strike":2, "Ulzuin's Wrath":2},
		"feet",
		Ability( "Storm Titan",
			{"type":"attack", "trigger":"hit", "chance":.25, "recharge":3, "duration":3, "targets":2.5},
			{"triggered lightning":(52+193)/2*3, "triggered electrocute":[240/2*3,2], "duration":{"reduce damage %":10}}
		)
	),
	Item.getByName("Mark of Mogdrogen", components),
	Item.getByName("Kingsguard Powder", augments),

	Item( "Eye of the Storm",
		{"lightning %":104, "spirit":66, "attack speed":8, "lightning retaliation":(255+874)/2, "skill cost %":-10, "Shaman":1},
		"relic",
		Ability( "Stormcaller Aura",
			{"type":"buff", "trigger":"toggle"},
			{"energy":-150, "energy/s":-2, "lightning":(1+76)/2, "electrocute":[318/3*.2,3], "lightning %":150, "electrocute %":150, "lightning resist":30, "lightning retaliation":(1+784)/2}
		)
	),

	Item( "Gladiator's Distinction",
		{"armor":72, "crit damage":4, "physical %":72, "internal %":72, "bleed %":72, "vitality to physical":100, "offense %":3, "chaos resist":18, "bleed resist":22, "max bleed resist":5, "Reaping Strike":3, "Markovian's Advantage":2, "physical":(12+16)/2, "offense":68, "armor %":8},
		"waist"
	),
	Item.getByName("Ugdenbog Leather", components),
	Item.getByName("Kingsguard Powder", augments),

	Item( "Badge of Mastery",
		{"all damage %":23, "offense %":4, "elemental resist":26, "Savagery":3, "Primal Strike":2},
		"medal",
		Ability( "Prowess",
			{"type":"buff", "trigger":"kill", "chance":1, "recharge":15, "duration":10},
			{"offense":100, "defense":50, "health/s":30}
		)
	),
	Item.getByName("Attuned Lodestone", components),

	Item( "Ultos' Storm (2)",
		{"lightning %":80},
		"set",
	),
	Item( "Ultos' Storm (3)",
		{"offense %":5, "lightning resist":20},
		"set",
	),
	Item( "Ultos' Storm (4)",
		{"Shaman":2},
		"set",
	),

	Item( "Ultos' Storm (5)",
		{"lightning":(1+72)/2},
		"set",
		Ability( "Ultos' Wrath",
			{"type":"attack", "trigger":"critical", "chance":.5, "recharge":3, "targets":3},
			{"triggered lightning":(62+224)/2*5, "triggered electrocute":[224/2*5,2]}
		)
	),
]

skills = {
	"Markovian's Advantage":6,
	"Fighting Spirit":4,
	"Menhir's Will":4,
	"Military Conditioning":5,
	"Zolhan's Technique":7,
	"Blitz":1,
	"Veterancy":1,
	"War Cry":3,
	"Field Command":9,
	"Terrify":3,
	"Decorated Soldier":1,
	"Blindside":2,
	"Squad Tactics":4,
	"Break Morale":1,
	"Counter Strike":1,
	"Scars of Battle":2,

	"Brute Force":1,
	"Savagery":9,
	"Primal Strike":6,
	"Might of the Bear":3,
	"Mogdrogen's Pact":2,
	"Feral Hunger":5,
	"Wind Devil":1,
	"Summon Briarthorn":1,
	"Torrent":4,
	"Tenacity of the Boar":3,
	"Heart of the Wild":5,
	"Wendigo Totem":2,
	"Raging Tempest":7,
	"Storm Surge":4,
	"Oak Skin":1,
	"Storm Totem":6,
	"Storm Touched":5,
	"Blood Pact":1,
	"Maelstrom":2,
	"Emboldening Presence":1,
	"Stormcaller's Pact":8,
	"Conjure Primal Spirit":1,
}

constellations = [xC, fiend, viper, tsunami, wraith, quill, kraken, tempest, hawk, eel, ultosHandofUltos, spear]