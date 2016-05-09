from dataModel import *

components = [
	Item("Bristly Fur", {"health":90, "constitution %":25}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Scavenged Plating", {"armor":15}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Rigid Shell", {"physique":10, "armor":24, "lightning resist":20}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Antivenom Salve", {"health/s":5, "armor":24, "acid resist":20}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Dense Fur", {"health":90, "armor":24, "cold resist":20}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Molten Skin", {"armor":24, "fire resist":20, "reduced burn duration":15}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Spined Carapace", {"armor":24, "pierce retaliation":55, "retaliation %":12}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),

	Item("Mutated Scales", {"health":180, "health %":3}, ["shoulders", "chest", "legs", "arms"]),
	Item("Silk Swatch", {"pierce resist":18, "bleed resist":18}, ["shoulders", "chest", "legs"]),
	Item("Scaled Hide", {"armor":35, "armor absorb":20}, ["shoulders", "chest", "legs"]),

	Item("Restless Remains", {"energy":110, "casting speed":10}, ["arms"]),
	Item("Spellwoven Threads", {"burn %":30, "frostburn %":30, "electrocute %":30, "spirit":15, "offense":18, "casting speed":8}, ["arms"]),
	Item("Consecrated Wrappings", {"chaos":3, "chaos %":8, "attack speed":5}, ["arms"]),
	Item("Unholy Inscription", {"vitality %":15, "offense":15, "vitality resist":10, "bleed resist":15}, ["arms"]),

	Item("Leathery Hide", {"health %":5, "armor":24, "reduced stun duration":25}, ["head"]),
	Item("Sanctified Bone", {"vitality resist":18, "chaos resist":12}, ["chest", "head"]),
	Item("Runestone", {"elemental %":12, "armor":18, "elemental resist":10}, ["head"]),
	Item("Prismatic Diamond", {"damage reflect %":20, "elemental":18, "elemental resist":7, "energy absorb":20}, ["head"],
		Ability(
			"Prismatic Rage",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":30, "duration":8},
			{"all damage %":50, "total speed":10, "offense":30}
		)
	),

	Item("Polished Emerald", {"physique":8, "cunning":8, "spirit":8}, ["shield", "offhand", "ring", "head", "chest"]),
	Item("Ectoplasm", {"energy %":20, "energy/s":2}, ["head", "ring", "amulet", "medal"]),

	Item("Roiling BLood", {"physical %":8, "offense":16}, ["ring", "amulet", "medal"]),
	Item("Corpse Dust", {"health %":3, "health regeneration":18, "vitality resist":6}, ["ring", "amulet", "medal"]),
	Item("Soul Shard", {"vitality %":12, "energy absorb":30, "vitality resist":6, "energy leech resist":25}, ["ring", "amulet", "medal"]),
	Item("Vengeful Wraith", {"cold %":12, "frostburn %":25, "frostburn duration":15, "offense":8, "cold retaliation":60}, ["ring", "amulet", "medal"]),

	Item("Frozen Heart", {"health":70, "cold resist":10, "reduced freeze duration":21}, ["ring"]),
	Item("Mark of Illusions", {"elemental %":15, "spirit":12, "defense":12, "energy/s":1.2}, ["ring", "amulet"]),

	Item("Focusing Prism", {"crit damage":5, "spirit":18, "skill cost":-10}, ["amulet"]),
	Item("Arcane Lens", {"elemental":(2+6)/2, "elemental %":15, "spirit %":3, "skill cost":-6}, ["amulet"]),

	Item("Wardstone", {"elemental resist":7, "bleed resist":15}, ["amulet", "medal"]),
	Item("Attuned Lodestone", {"all damage %":8, "crit damage":5, "lightning %":20, "lightning":(1+154)/2}, ["amulet", "medal"],
		Ability(
			"Static Charge",
			{"type":"attack", "trigger":"hit", "chance":.2, "recharge":2, "targets":2, "shape":"pbaoe"},
			{"weapon damage %":25, "triggered lightning":(54+129)/2, "stun %":100}
		)
	),
	Item("Arcane Spark", {"energy leech":45, "energy regeneration":20, "offense":36}, ["amulet", "medal"]),
	Item("Aether Soul", {"aether %":10, "aether resist":12, "damage from aetherials":-6}, ["amulet", "medal"]),
	Item("Black Tallow", {"chaos %":10, "chaos resist":12, "damage from chthonics":-6}, ["amulet", "medal"]),
	Item("Vicious Jawbone", {"physical %":15, "internal %":20, "cunning":12, "attack speed":3}, ["amulet", "medal"]),
	Item("Dread Skull", {"pierce %":12, "vitality %":8, "bleed %":30, "bleed duration":15, "attack speed":5, "move speed":3}, ["amulet", "medal"]),

	Item("Resilient Plating", {"defense":14, "armor":24, "pierce resist":10}, ["shield", "offhand", "chest", "shoulders"]),

	Item("Ancient Armor Plate", {"physique":18, "armor":35, "armor %":8}, ["chest", "legs"]),
	Item("Rotten Heart", {"chaos %":25, "poison %":25, "offense":18, "acid retaliation":75}, ["chest"]),	
	Item("Kilrian's Shattered Soul", {"fire %":40, "vitality %":40, "attack speed":5, "vitality resist":20}, ["chest"],		
		Ability(
			"Kilrian's Flame",
			# 3 meter radius
			{"type":"attack", "trigger":"hit", "chance":.1, "recharge":12, "duration":6, "targets":2, "shape":"pbaoe"},
			{"triggered fire":72*6, "triggered vitality":72*6, "attack as health %":33}
		)
	),
	Item("Chains of Oleron", {"all damage %":12, "offense":25, "offense %":2, "reduced entrapment duration":24}, ["chest"]),
	Item("Ballistic Plating", {"defense":12, "avoid ranged":10, "armor":18}, ["chest"]),
	Item("Bindings of Bysmiel", {"all damage %":8, "defense":25, "energy/s":1, "pet damage %":20, "pet health %":10}, ["chest"]),
	Item("Hallowed Ground", {"defense":25, "defense %":2, "health/s":6, "elemental resist":12}, ["chest"]),

	Item("Mark of the Traveler", {"health/s":10, "move %":6, "slow resist":10}, ["feet"]),
	Item("Mark of Mogdrogen", {"health %":4, "health/s":15, "health regeneration":10, "move %":3}, ["feet"]),

	Item("Battered Shell", {"physique":15, "block %":10}, ["shield"], 
		Ability(
			"Shield Slam",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2, "shape":"melee"},
			{"weapon damage %":125, "triggered physical":(85+112)/2, "stun %":100}
		)
	),
	Item("Reinforced Shell", {"physique":10, "block %":8, "blocked damage %":22}, ["shield"],
		Ability(
			"Blade Ward",
			{"type":"buff", "trigger":"hit", "chance":1, "recharge":24, "duration":8},
			{"pierce resist":24, "pierce retaliation":104}
		)
	),
	Item("Serrated Shell", {"shield recovery":20, "pierce retaliation":112, "retaliation %":20}, ["shield"],
		Ability(
			"Brutal Shield Slam",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"weapon damage %":180, "physical":(105+202)/2, "internal":225*.33, "stun %":1}
		)
	),
	Item("Radiant Gem", {"elemental %":10, "physical to elemental":10, "elemental resist":15}, ["shield", "offhand"],
		Ability(
			"Radiant Shield",
			{"type":"buff", "trigger":"hit", "chance":1, "recharge":30, "duration":8},
			{"fire resist":30, "cold resist":30, "lightning resist":30, "max fire resist":10, "max cold resist":10, "max lightning resist":10}
		)
	),
	Item("Mark of the Myrmidon", {"health":120, "defense":25, "shield recovery":15, "damage reflect %":16}, ["shield"],
		Ability(
			"Blade Barrier",
			{"type":"buff", "trigger":"hit", "chance":1, "recharge":24, "duration":8},
			{"pierce %":30, "pierce resist":30, "pierce retaliation":168}
		)
	),

	Item("Chipped Claw", {"physical":4, "physical %":12}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Slam",
			{"type":"attack", "trigger":"manual", "recharge":4},
			{"weapon damage %":200, "physical":(92+186)/2, "crit damage":30, "physical %":.25*50}
		)
	),
	Item("Chilled Steel", {"cold":4, "cold %":12, "physical to cold":10}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Ice Spike",
			{"type":"attack", "trigger":"manual", "targets":1.5, "shape":"line"}, # no actual recharge not sure how to handle attack replacement...
			{"weapon damage %":14, "triggered cold":(63+92)/2, "slow move":20}
		)
	),
	Item("Mutagenic Ichor", {"poison":15, "acid %":10, "poison %":10, "physical to acid":10}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Poison Bomb",
			{"type":"attack", "trigger":"manual", "targets":2.5, "shape":"pbaoe"},
			{"weapon damage %":8, "triggered acid":12, "triggered poison":144}
		)
	),
	Item("Searing Ember", {"fire":3, "fire %":12, "physical to fire":10}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Fireblast",
			{"type":"attack", "trigger":"manual","targets":1.5},
			{"weapon damage %":16, "triggered fire":(52+60)/2, "triggered burn":126}
		)
	),
	Item("Serrated Spike", {"pierce":3+4, "bleed":9, "bleed %":12, "energy":-50, "pet pierce":16, "pierce %":15, "pet pierce %":15}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"]),
	Item("Cracked Lodestone", {"lightning":(1+5)/2, "lightning %":12, "physical to lightning":10}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Lightning Nova",
			{"type":"attack", "trigger":"manual", "targets":2.5, "shape":"pbaoe"},
			{"weapon damage %":18, "triggered lightning":(22+108)/2}
		)
	),
	Item("Hollowed Fang", {"life leech":135*.05, "vitality %":18, "lifesteal %":4, "physical to vitality":10}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Blooddrinker",
			{"type":"buff", "trigger":"hit", "chance":1, "recharge":30, "duration":8},
			{"bleed":132*.25, "attack as health %":25}
		)
	),
	Item("Imbued Silver", {"defense":15, "bleed resist":15, "damage to chthonics":15, "energy":-150, "chaos resist":20, "pet chaos resist":20, "max chaos resist":3, "pet max chaos resist":3}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"]),
	
	# reduce resist applies only to weapon hits (and skills that have a weapon component)
	Item("Mark of Dreeg", {"poison":50, "acid %":30, "poison %":30, "reduce resist":15, "physical to acid":10, "light radius":6}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Dreeg's Infinite Gaze",
			{"type":"attack", "trigger":"manual", "recharge":2.5, "targets":2, "shape":"pbaoe"},
			{"weapon damage %":25, "triggered acid":62, "triggered poison":498}
		)
	),
	Item("Vicious Spikes", {"pierce":4+5, "pierce %":18+30, "reduce armor":25, "energy":-150}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"]),
	Item("Purified Salt", {"defense":15, "life leech resist":25, "damage to aetherials":15, "aether resist":20, "pet aether resist":20, "max aether resist":3, "pet max aether resist":3}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"]),
	Item("Severed Claw", {"physical":7, "physical %":25, "internal %":15}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Brutal Slam",
			{"type":"attack", "trigger":"manual", "recharge":3.5},
			{"weapon damage %":260, "triggered physical":(122+285)/2, "crit damage":50, "physical %":.33*50, "slow move":30}
		)
	),
	Item("Blessed Steel", {"elemental":4, "elemental %":18, "physical to elemental":10, "offense":18}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Sacred Strike",
			{"type":"attack", "trigger":"manual", "recharge":3, "duration":5, "shape":"weapon"},
			# reduce resist here is very strong against bosses but almost useless against trash (1/3)
			{"weapon damage %":250, "triggered elemental":(165+254)/2, "physical to elemental":100, "duration":{"reduce resist":30/3}}
		)
	),
	Item("Haunted Steel", {"vitality":8, "vitality %":25, "lifeleach %":8}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Bloodthirster",
			{"type":"buff", "trigger":"hit", "chance":1, "recharge":30, "duration":8},
			{"triggered bleed":216*.25, "lifesteal %":30, "bleed resist":20}
		)
	),
	Item("Symbol of Solael", {"chaos":(2+12)/2, "chaos %":35, "physical to chaos":10, "energy absorb":33}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		# the resist reduction is strong but it seems only powerful vs bosses /2.
		Ability(
			"Solael's Flame",
			{"type":"attack", "trigger":"manual", "recharge":8, "duration":8},
			{"triggered chaos":(44+136)/2*8, "duration":{"reduce resist":30/2}}
		)
	),

	Item("Enchanted Flint", {"fire":5+5, "fire %":25+35, "burn %":25+35, "physical to fire":10, "energy":-150, "burn":75*.1, "pet fire":5, "pet burn":75*.1, "pet fire %":35, "pet burn %":35}, ["sword", "axe", "mace", "dagger", "twohand", "shield", "offhand"]),
	Item("Wrathstone", {"aether":5+5, "aether %":25+35, "physical to aether":10, "energy":-150, "aether retaliation":44*.15, "pet aether damage":5, "pet aether %":35, "pet aether retaliation":44*.15}, ["sword", "axe", "mace", "dagger", "twohand", "shield", "offhand"]),
	Item("Coldstone", {"cold":5+5, "cold %":25+35, "frostburn %":25+35, "physical to cold":10, "energy":-150, "slow move":25*.08, "pet cold":5, "pet cold %":35, "pet frostburn %":35}, ["sword", "axe", "mace", "dagger", "twohand", "shield", "offhand"]),
	Item("Vitriolic Gallstone", {"poison":20+20, "acid %":25+35, "poison %":25+35, "poison duration":20, "physical to acid":10, "energy":-50, "pet poison":20, "pet acid %":35, "pet poison %":35}, ["sword", "axe", "mace", "dagger", "twohand", "shield", "offhand"]),
	Item("Amber", {"lightning":(2+8)/2, "lightning %":25, "electrocute %":25, "physical to lightning":10}, ["sword", "axe", "mace", "dagger", "twohand", "shield", "offhand"],
		Ability(
			"Empowered Lightning Nova",
			{"type":"attack", "trigger":"manual", "targets":2, "shape":"pbaoe"},
			{"weapon damage %":28, "triggered lightning":(69+341)/2}
		)
	),
	Item("Riftstone", {"chaos":(2+8)/2, "chaos %":25, "physical to chaos":10}, ["sword", "axe", "mace", "dagger", "twohand", "shield", "offhand"],
		Ability(
			"Chaos Strike",
			{"type":"attack", "trigger":"manual", "recharge":4, "targets":1.5},
			{"weapon damage %":220, "triggered chaos":(86+320)/2}
		)
	),
	Item("Blessed Whetstone", {"increase armor pierce":50, "bleed %":25, "offense":18}, ["sword", "axe", "twohand"],
		Ability(
			"Behead",
			{"type":"attack", "trigger":"manual", "recharge":3.5, "targets":1.5},
			{"weapon damage %":190, "triggered physical":(132+202)/2, "triggered bleed":460*.25, "crit damage":50}
		)
	),
	Item("Bloody Whetstone", {"bleed":30, "all damage %":8, "bleed %":30, "bleed duration":20}, ["sword", "axe", "twohand"], #two handed sword and axe
		Ability(
			"Decapitate",
			{"type":"attack", "trigger":"manual", "recharge":3.5, "targets":1.5},
			{"weapon damage %":200, "triggered physical":(164+236)/2, "triggered bleed":720*.35, "crit damage":50}
		)
	),
	Item("Oleron's Blood", {"physical %":25, "internal %":40, "offense":18, "total speed":2}, ["sword", "axe", "mace", "dagger", "twohand"],
		Ability(
			"Oleron's Might",
			{"type":"attack", "trigger":"manual", "recharge":3.5, "targets":1},
			{"weapon damage %":260, "triggered physical":(174+346)/2, "internal":210, "crit damage":50, "reduced damage":20}
		)
	),
	Item("Shard of Beronath", {"all damage %":15, "elemental":8, "offense":25, "physical to elemental":10}, ["sword", "axe", "mace", "dagger", "twohand"],
		Ability(
			"Beronath's Fury",
			{"type":"attack", "trigger":"manual", "recharge":.5, "shape":"weapon"},
			{"weapon damage %":135, "elemental":23, "all damage %":20, "elemental %":40}
		)
	),

	Item("Flintcore Bolts", {"fire":5, "burn":15, "fire %":25, "burn %":25, "physical to fire":10}, ["pistol", "rifle", "crossbow", "offhand"],
		Ability(
			"Greater Fireblast",
			{"type":"attack", "trigger":"manual", "targets":1.5},
			{"weapon damage %":22, "triggered fire":(95+124)/2, "triggerd burn":225, "stun %":15}
		)
	),
	Item("Deathchill Bolts", {"cold":5, "cold %":25, "frostburn %":25, "slow move":25*.12, "physical to cold":10}, ["pistol", "rifle", "crossbow", "offhand"],
		Ability(
			"Greater Ice Spike",
			{"type":"attack", "trigger":"manual", "targets":1.5, "shape":"line"},
			{"weapon damage %":20, "triggered cold":(125+166)/2, "stun %":15, "slow move":20}
		)
	),
	Item("Devil-Touched Ammo", {"fire":6, "all damage %":30*.09, "fire %":30, "chaos %":30, "physical to fire":10}, ["pistol", "rifle", "crossbow", "offhand"],
		Ability(
			"Demon's Breath",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2, "shape":"cone"},
			{"weapon damage %":25, "triggered fire":(44+72)/2, "triggered chaos":(85+136)/2, "reduce health %":5, "attack as health %":10}
		)
	),
	Item("Void-Touched Ammo", {"chaos":(2+8)/2, "chaos %":25, "physical to chaos":10}, ["pistol", "rifle", "crossbow", "offhand"],
		Ability(
			"Chaos Bolt",
			{"type":"attack", "trigger":"manual", "targets":2},
			{"weapon damage %":8, "triggered chaos":(42+112)/2}
		)
	),
	Item("Hell's Bane Ammo", {"lightning":(1+9)/2*2, "lightning %":25+35, "electrocute":25+35, "physical to lightning":10, "energy":-50, "stun %":8}, ["pistol", "rifle", "crossbow", "offhand"]),
	Item("Venom-Tipped Ammo", {"acid":4, "poison":20, "acid %":25, "poison %":25, "poison duration":10}, ["pistol", "rifle", "crossbow", "offhand"],
		Ability(
			"Noxious Poison Bomb",
			{"type":"attack", "trigger":"manual", "recharge":2, "targets":1.5, "shape":"circle"},
			{"weapon damage %":12, "triggered acid":20, "triggered poison":270, "stun %":25, "reduce resist":30}
		)
	),
	Item("Aethersteel Bolts", {"aether":5, "aether %":25, "physical to aether":10}, ["pistol", "rifle", "crossbow", "offhand"],
		Ability(
			"Aether Tendril",
			{"type":"attack", "trigger":"manual", "recharge":2.5},
			{"weapon damage %":40, "triggered aether":(975+1247)/2, "slow %":40, "reduce resist":30}
		)
	),
	Item("Silvercore Bolts", {"pierce":4, "all damage %":18, "offense":30/2, "damage to chthonics":20}, ["pistol", "rifle", "crossbow", "offhand"],
		Ability(
			"Silver Spread",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":4},
			{"weapon damage %":80, "triggered pierce":(125+250)/2, "damage to chthonics":50} #"damage to chthonics":62
		)
	),

	# Item("", {}, ["pistol", "rifle", "crossbow", "offhand"],
	# 	Ability(
	# 		"",
	# 		{"type":"attack", "trigger":"manual", "recharge":3.5, "targets":2},
	# 		{}
	# 	)
	# ),
]

augments = [
	#devil's crossing honored
	Item("Boneback Spine", {"pierce %":7, "bleed %":12, "bleed duration":15}, ["ring", "amulet"]),
	Item("Slith Venom", {"acid resist":15, "poison retaliation":210, "retaliation %":10}, ["ring", "amulet"]),
	Item("Gazer Eye", {"lightning %":10, "aether %":10}, ["ring", "amulet"]),
	Item("Corpsefiend Tentacle", {"vitality %":10, "aether %":10}, ["ring", "amulet"]),
	Item("Rifthound Salts", {"pet total speed":3, "pet elemental resist":15}, ["ring", "amulet"]),

	#devil's crossing revered
	Item("Survivor's Ingenuity", {"all damage %":7, "offense":10, "defense":5}, ["ring", "amulet"]),
	Item("Survivor's Resilience", {"health %":3, "block %":3, "blocked damage %":20}, ["ring", "amulet"]),
	Item("Survivor's Perseverence", {"aether %":15, "chaos %":15}, ["ring", "amulet"]),
	Item("Cairn's Hope", {"health regeneration":15, "energy regeneration":15, "constitution %":20}, ["ring", "amulet"]),
	Item("Song of the Elements", {"fire %":15, "cold %":15, "fire resist":18, "cold resist":18}, ["ring", "amulet"]),
	Item("Viloth's Bite", {"poison %":20, "poison duration":15, "stun %":3}, ["ring", "amulet"]),
	Item("Overseer's Gaze", {"lightning %":15, "stun duration":10, "offense":10}, ["ring", "amulet"]),
	Item("Survivor's Ally", {"pet all damage %":8, "pet health %":5, "pet energy regeneration":10}, ["ring", "amulet"]),

	Item("Bladeward Powder", {"pierce resist":10}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Mogdrogen's Touch", {"acid resist":10, "vitality resist":7}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),

	#rovers honored
	Item("Arkovian Rose Powder", {"elemental %":7, "energy/s":1}, ["ring", "amulet"]),
	Item("Rotbloom Powder", {"vitality %":10, "chaos %":10}, ["ring", "amulet"]),
	Item("Slithweed Powder", {"acid %":10, "poison %":15}, ["ring", "amulet"]),
	Item("Stormtail Viper Venom", {"physical %":10, "lightning %":10}, ["ring", "amulet"]),
	Item("Conjurer's Powder", {"elemental %":7, "pet all damage %":5}, ["ring", "amulet"]),

	Item("Arkovian Bonemeal", {"vitality %":15, "damage to undead":5}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Arkovian Bonemeal", {"vitality %":25, "damage to undead":8}, ["twohand", "rifle", "crossbow"]),
	Item("Troll Wart Powder", {"health %":3, "health/s":3, "health regeneration":10}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Troll Wart Powder", {"health %":5, "health/s":5, "health regeneration":18}, ["twohand", "rifle", "crossbow"]),
	Item("Winterbloom Powder", {"cold %":15, "frostburn %":18}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Winterbloom Powder", {"cold %":25, "frostburn %":32}, ["twohand", "rifle", "crossbow"]),

	#rovers revered
	Item("Rhowan's Wisdom", {"elemental %":12, "spirit":10, "energy":200, "cast speed":2}, ["ring", "amulet"]),
	Item("Mogdrogen's Security", {"health":180, "health/s":5, "elemental resist":12}, ["ring", "amulet"]),
	Item("Traveler's Boon", {"move %":2, "armor":12}, ["ring", "amulet"]),
	Item("Breath of Life", {"health %":4, "health regeneration":10, "vitality resist":15}, ["ring", "amulet"]),
	Item("Winter's Chill", {"cold %":15, "frostburn %":25, "stun %":3}, ["ring", "amulet"]),
	Item("Rhowan's Resolve", {"physical %":15, "defense":6, "retaliation %":16}, ["ring", "amulet"]),
	Item("Nature's Wrath", {"acid %":15, "poison %":20, "offense":10}, ["ring", "amulet"]),
	Item("Spirit of Vengeance", {"vitality %":15, "vitality retaliation":75, "retaliation %":16}, ["ring", "amulet"]),
	Item("Mogdrogen's Blessing", {"pet crit damage":10, "pet offense %":3, "pet attack speed":5}, ["ring", "amulet"]),

	Item("Venomguard Powder", {"acid resist":15}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Nightshade Powder", {"pierce resist":7, "cold resist":10}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),

	#kymon's honored
	Item("Divine Flame", {"fire %":10, "lightning %":10}, ["ring", "amulet"]),
	Item("Blessed Ashes", {"defense":6, "fire resist":15, "lightning resist":15}, ["ring", "amulet"]),
	Item("Consecrated Silver", {"physical %":10, "damage to chthonics":5}, ["ring", "amulet"]),
	Item("Firebloom Powder", {"burn %":18, "offense":10}, ["ring", "amulet"]),
	Item("Storm Powder", {"electrocute %":18, "lightning retaliation":(1+107)/2, "retaliation %":10}, ["ring", "amulet"]),

	#kymon's revered
	Item("Kymon's Will", {"fire %":15, "burn %":25, "reduce damage":20*.1}, ["ring", "amulet"]),
	Item("Kymon's Fury", {"physical %":15, "bleed %":25, "bleed duration":15}, ["ring", "amulet"]),
	Item("Kymon's Vision", {"lightning %":15, "electrocute %":25, "offense":10}, ["ring", "amulet"]),
	Item("Empyrion's Touch", {"electrocute %":35, "electrocute duration":30, "energy absorb":15}, ["ring", "amulet"]),
	Item("Infernal Dust", {"burn %":35, "burn duration":30, "fire resist":22}, ["ring", "amulet"]),

	Item("Kymon's Blessing", {"fire resist":15}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Kymon's Conduit", {"lightning resist":15}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Demonbane Powder", {"vitality resist":7, "chaos resist":7}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),

	#black legion honored
	Item("Manticore Venom", {"poison %":18, "damage to chthonics":5}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Manticore Venom", {"poison %":32, "damage to chthonics":8}, ["twohand", "rifle", "crossbow"]),
	Item("Voidbeast Powder", {"vitality %":15, "chaos %":15}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Voidbeast Powder", {"vitality %":25, "chaos %":25}, ["twohand", "rifle", "crossbow"]),
	Item("Blacksteel Powder", {"physical %":15, "fire %":10}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Blacksteel Powder", {"physical %":25, "fire %":17}, ["twohand", "rifle", "crossbow"]),
	Item("Aether Dust", {"aether %":15, "damage to aetherials":5}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Aether Dust", {"aether %":25, "damage to aetherials":8}, ["twohand", "rifle", "crossbow"]),
	Item("Witch's Powder", {"pet offense %":3, "pet attack speed":6}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Witch's Powder", {"pet offense %":5, "pet attack speed":10}, ["twohand", "rifle", "crossbow"]),

	#black legion revered
	Item("Ulgrim's Guile", {"pierce %":15, "cold %":20, "offense":10}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Ulgrim's Guile", {"pierce %":25, "cold %":35, "offense":16}, ["twohand", "rifle", "crossbow"]),
	Item("Creed's Cunning", {"elemental %":15, "offense":10, "energy/s":1}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Creed's Cunning", {"elemental %":25, "offense":16, "energy/s":1.5}, ["twohand", "rifle", "crossbow"]),
	Item("Oleron's Fervor", {"all damage %":50*.05, "physical %":20, "bleed %":25}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Oleron's Fervor", {"all damage %":50*.05, "physical %":35, "bleed %":45}, ["twohand", "rifle", "crossbow"]),
	Item("Aetherstorm Powder", {"lightning %":20, "aether %":20}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Aetherstorm Powder", {"lightning %":35, "aether %":35}, ["twohand", "rifle", "crossbow"]),
	Item("Essence of Ch'thon", {"vitality %":20, "chaos %":20, "reduce resist":30*.1}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Essence of Ch'thon", {"vitality %":35, "chaos %":35, "reduce resist":30*.1}, ["twohand", "rifle", "crossbow"]),

	Item("Mankind's Vigil", {"aether resist":7, "chaos resist":7}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Kingsguard Powder", {"pierce resist":7, "acid resist":10}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),

	#outcast revered
	Item("Outcast's Might", {"physical %":20, "pierce %":15, "reduce armor":60*.1}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Might", {"physical %":35, "pierce %":25, "reduce armor":60*.1}, ["twohand", "rifle", "crossbow"]),
	Item("Outcast's Frostbite", {"cold %":20, "frostburn %":25, "stun %":3}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Frostbite", {"cold %":35, "frostburn %":45, "stun %":3}, ["twohand", "rifle", "crossbow"]),
	Item("Outcast's Inferno", {"fire %":20, "burn %":25, "burn duration":20}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Inferno", {"fire %":35, "burn %":45, "burn duration":20}, ["twohand", "rifle", "crossbow"]),
	Item("Outcast's Thunder", {"lightning %":20, "electrocute %":25, "stun %":3}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Thunder", {"lightning %":35, "electrocute %":45, "stun %":3}, ["twohand", "rifle", "crossbow"]),
	Item("Outcast's Venom", {"acid %":20, "poison %":25, "poison duration":20}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Venom", {"acid %":35, "poison %":45, "poison duration":20}, ["twohand", "rifle", "crossbow"]),
	Item("Outcast's Deathtouch", {"vitality %":20, "vitality decay %":25, "vitality decay duration":20}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Deathtouch", {"vitality %":35, "vitality decay %":45, "vitality decay duration":20}, ["twohand", "rifle", "crossbow"]),
	Item("Outcast's Wrath", {"aether %":20, "offense":10, "damage to aetherials":6}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Wrath", {"aether %":35, "offense":16, "damage to aetherials":10}, ["twohand", "rifle", "crossbow"]),
	Item("Outcast's Riftstorm", {"chaos %":20, "offense":10, "energy/s":1}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Riftstorm", {"chaos %":35, "offense":16, "energy/s":1.5}, ["twohand", "rifle", "crossbow"]),
	Item("Outcast's Bastion", {"defense":8, "aether resist":12, "chaos resist":12}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Bastion", {"defense":12, "aether resist":20, "chaos resist":20}, ["twohand", "rifle", "crossbow"]),

	Item("Outcast's Warding Powder", {"aether resist":10}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Outcast's Elemental Scales", {"fire resist":10, "cold resist":10}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Outcast's Skyguard Powder", {"cold resist":10, "lightning resist":10}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),

	#homestead honored
	Item("Voidvine Powder", {"fire %":15, "chaos %":10}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Voidvine Powder", {"fire %":25, "chaos %":17}, ["twohand", "rifle", "crossbow"]),
	Item("Stonetusk Hoof", {"physical %":15, "internal %":18}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Stonetusk Hoof", {"physical %":25, "internal %":32}, ["twohand", "rifle", "crossbow"]),
	Item("Dermapteran Chitin", {"armor %":4, "pierce resist":12, "reduced stun duration":10}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Dermapteran Chitin", {"armor %":6, "pierce resist":20, "reduced stun duration":17}, ["twohand", "rifle", "crossbow"]),
	Item("Raincaller Powder", {"lightning %":15, "electrocute %":18}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Raincaller Powder", {"lightning %":25, "electrocute %":32}, ["twohand", "rifle", "crossbow"]),
	Item("Beast Tamer's Powder", {"pet all damage %":10, "pet defense %":4}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Beast Tamer's Powder", {"pet all damage %":16, "pet defense %":6}, ["twohand", "rifle", "crossbow"]),

	#homestead revered
	Item("Nature's Harvest", {"poison %":25, "offense":55*.1, "damage to humans":6}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Nature's Harvest", {"poison %":45, "offense":55*.1, "damage to humans":10}, ["twohand", "rifle", "crossbow"]),
	Item("Solar Radiance", {"fire %":20, "offense":10, "energy absorb":10}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Solar Radiance", {"fire %":35, "offense":16, "energy absorb":18}, ["twohand", "rifle", "crossbow"]),
	Item("Menhir's Blessing", {"stun duration":10, "physique":17, "armor %":5}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Menhir's Blessing", {"stun duration":18, "physique":28, "armor %":8}, ["twohand", "rifle", "crossbow"]),
	Item("Beastlord's Calling", {"pet all damage %":15, "pet health %":5, "pet defense %":3}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Beastlord's Calling", {"pet all damage %":24, "pet health %":8, "pet defense %":5}, ["twohand", "rifle", "crossbow"]),

	Item("Flameweave Powder", {"pierce resist":7, "fire resist":10}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Solarstorm Powder", {"fire resist":10, "lightning resist":10}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
]