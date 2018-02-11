from dataModel import *

components = [
	Item("Bristly Fur", {"health":90, "constitution %":25}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Scavenged Plating", {"armor":15}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Rigid Shell", {"physique":10, "armor":24, "lightning resist":20}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Antivenom Salve", {"health/s":5, "armor":24, "acid resist":20}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Dense Fur", {"health":90, "armor":24, "cold resist":20}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Molten Skin", {"armor":24, "fire resist":20, "reduced burn duration":15}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Spined Carapace", {"armor":24, "pierce retaliation":55, "retaliation %":12}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Bladed Plating", {"health":70, "offense":22, "retaliation %":30}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Enchanted Earth", {"health %":4, "health/s":5, "armor %":4}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Spellscorched Plating", {"health":50, "armor":30, "elemental resist":15}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Ugdenbog Leather", {"defense":30, "acid resist":20, "bleed resist":20}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),

	Item("Mutated Scales", {"health":180, "health %":3}, ["shoulders", "chest", "legs", "arms"]),
	Item("Silk Swatch", {"pierce resist":18, "bleed resist":18}, ["shoulders", "chest", "legs"]),
	Item("Scaled Hide", {"armor":35, "armor absorb":20}, ["shoulders", "chest", "legs"]),

	Item("Living Armor", {"offense":35, "chaos resist":8, "elemental resist":10, "armor absorb":12}, ["shoulders", "chest", "head"]),
	Item("Sacred Plating", {"health":210, "vitality resist":14, "aether resist":18, "armor absorb":12}, ["shoulders", "chest", "head"]),

	Item("Restless Remains", {"lifesteal %":3, "energy":220, "cast speed":10}, ["arms"]),
	Item("Spellwoven Threads", {"burn %":30, "frostburn %":30, "electrocute %":30, "spirit":15, "offense":18, "cast speed":8}, ["arms"]),
	Item("Consecrated Wrappings", {"chaos":3, "chaos %":8, "attack speed":5}, ["arms"]),
	Item("Unholy Inscription", {"vitality %":15, "vitality decay %":15, "offense":15, "vitality resist":10, "bleed resist":15}, ["arms"]),

	Item("Leathery Hide", {"health %":5, "armor":24, "reduced stun duration":25}, ["head"]),
	Item("Sanctified Bone", {"vitality resist":18, "chaos resist":12, "damage to undead":12, "damage to chthonics":12}, ["chest", "head"]),
	Item("Eldritch Mirror", {"attack speed":5, "cast speed":5, "vitality resist":10, "pet total speed":8}, ["chest", "head"]),
	Item("Titan Plating", {"physique %":3, "pierce resist":24, "reflected damage reduction":15, "armor %":8}, ["chest", "head"]),
	Item("Runestone", {"elemental %":10, "armor":18, "aether resist":12, "elemental resist":12}, ["head"]),
	Item("Prismatic Diamond", {"elemental":18, "energy absorb":20, "vitality resist":15, "damage reflect":20}, ["head"],
		Ability(
			"Prismatic Rage",
			{"type":"buff", "trigger":"low health", "chance":1, "recharge":25, "duration":8},
			{"all damage %":10, "total speed":10, "damage absorb":130}
		)
	),

	Item("Polished Emerald", {"physique":8, "cunning":8, "spirit":8}, ["shield", "offhand", "ring", "head", "chest"]),
	Item("Ectoplasm", {"energy %":20, "energy/s":2}, ["head", "ring", "amulet", "medal"]),

	Item("Roiling Blood", {"physical %":8, "offense":16}, ["ring", "amulet", "medal"]),
	Item("Corpse Dust", {"health %":3, "health/s %":18, "vitality resist":6}, ["ring", "amulet", "medal"]),
	Item("Soul Shard", {"vitality %":12, "vitality decay %":12, "energy absorb":30, "vitality resist":10, "energy leech resist":25}, ["ring", "amulet", "medal"]),
	Item("Vengeful Wraith", {"cold %":12, "frostburn %":25, "frostburn duration":15, "offense":8, "cold retaliation":60}, ["ring", "amulet", "medal"]),
	Item("Bloodied Crystal", {"bleed %":40, "bleed resist":24, "armor %":6}, ["ring", "amulet", "medal"]),
	Item("Runebound Topaz", {"health":160, "defense %":3, "blocked damage %":8}, ["ring", "amulet", "medal"]),

	Item("Frozen Heart", {"health":70, "cold resist":10, "reduced freeze duration":21}, ["ring"]),
	Item("Mark of Illusions", {"elemental %":15, "spirit":12, "defense":12, "energy/s":1.2}, ["ring", "amulet"]),

	Item("Focusing Prism", {"crit damage":5, "spirit":18, "skill cost %":-10}, ["amulet"]),
	Item("Arcane Lens", {"elemental":(2+6)/2, "elemental %":15, "spirit %":3, "skill cost %":-6}, ["amulet"]),
	Item("Seal of Ancestry", {"health %":5, "energy/s":1.5, "energy/s %":10, "vitality resist":20}, ["amulet"],
		Ability(
			"Ancestral Ward",
			# I'm not sure how I code up damage shields
			{"type":"buff", "trigger":"hit", "chance":1, "recharge":16},
			{}
		)		
	),
	Item("Seal of Annihilation", {"spirit":20, "attack speed":5, "cast speed":5, "skill cost %":-10}, ["amulet"],
		Ability(
			"Annihilation",
			{"type":"buff", "trigger":"critical", "chance":.15, "recharge":1, "duration":5},
			{"reduce health":20, "offense":70, "defense":70, "reduce health/s %":50}
		)		
	),

	Item("Wardstone", {"move speed":3, "elemental resist":7, "bleed resist":15}, ["amulet", "medal"]),
	Item("Attuned Lodestone", {"all damage %":8, "crit damage":5, "lightning %":20, "electrocute %":20, "lightning retaliation":(1+154)/2}, ["amulet", "medal"],
		Ability(
			"Static Charge",
			{"type":"attack", "trigger":"hit", "chance":.2, "recharge":2, "targets":2, "shape":"pbaoe"},
			{"weapon damage %":15, "triggered lightning":(54+129)/2, "stun %":100}
		)
	),
	Item("Arcane Spark", {"energy leech":45, "energy/s %":20, "offense":36}, ["amulet", "medal"]),
	Item("Aether Soul", {"aether %":10, "aether resist":16, "damage from aetherials":-6}, ["amulet", "medal"]),
	Item("Black Tallow", {"chaos %":10, "chaos resist":16, "damage from chthonics":-6}, ["amulet", "medal"]),
	Item("Vicious Jawbone", {"physical %":15, "internal %":20, "cunning":12, "attack speed":3}, ["amulet", "medal"]),
	Item("Dread Skull", {"pierce %":12, "vitality %":8, "bleed %":30, "bleed duration":15, "attack speed":5, "move speed":5}, ["amulet", "medal"]),
	Item("Blazing Ruby", {"physical %":35, "fire %":35, "health":100, "health %":4}, ["amulet", "medal"]),
	Item("Tainted Heart", {"crit damage":5, "offense":15, "vitality resist":12, "aether resist":12}, ["amulet", "medal"]),

	Item("Resilient Plating", {"defense":26, "armor":24, "pierce resist":15}, ["shield", "offhand", "chest", "shoulders"]),

	Item("Ancient Armor Plate", {"physique":18, "armor":35, "armor %":8, "armor absorb":8}, ["chest", "legs"]),
	Item("Rotten Heart", {"chaos %":25, "poison %":25, "offense":18, "acid retaliation":75}, ["chest"]),	
	Item("Kilrian's Shattered Soul", {"fire %":40, "vitality %":40, "burn %":40, "vitality decay %":40, "attack speed":5, "vitality resist":20}, ["chest"],		
		Ability(
			"Kilrian's Flame",
			# 3 meter radius
			{"type":"attack", "trigger":"hit", "chance":.1, "recharge":12, "duration":6, "targets":2, "shape":"pbaoe"},
			{"attack as health %":33, "duration":{"triggered fire":72, "triggered vitality":72, "triggered vitality decay":[80/2,2]}}
		)
	),
	Item("Chains of Oleron", {"all damage %":12, "offense":25, "offense %":2, "reduced entrapment duration":24}, ["chest"]),
	Item("Ballistic Plating", {"defense":22, "avoid ranged":10, "armor":18}, ["chest"]),
	Item("Bindings of Bysmiel", {"all damage %":8, "defense":25, "energy/s":1, "pet damage %":20, "pet health %":10}, ["chest"]),
	Item("Hallowed Ground", {"defense":25, "defense %":2, "health/s":6, "elemental resist":12}, ["chest"]),

	Item("Mark of the Traveler", {"health/s":10, "move speed":8, "slow resist":10}, ["feet"]),
	Item("Mark of Mogdrogen", {"health %":4, "health/s":15, "health/s %":10, "move speed":6}, ["feet"]),

	Item("Battered Shell", {"physique":15, "block %":10}, ["shield"], 
		Ability(
			"Shield Slam",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2, "shape":"melee"},
			{"weapon damage %":230, "triggered physical":(85+112)/2, "stun %":100}
		)
	),
	Item("Reinforced Shell", {"physique":10, "block %":8, "blocked damage %":22}, ["shield"],
		Ability(
			"Blade Ward",
			{"type":"buff", "trigger":"hit", "chance":1, "recharge":24, "duration":8},
			{"pierce resist":24, "pierce retaliation":224}
		)
	),
	Item("Serrated Shell", {"shield recovery":20, "pierce retaliation":112, "retaliation %":20}, ["shield"],
		Ability(
			"Brutal Shield Slam",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2},
			{"weapon damage %":300, "physical":(105+202)/2, "internal":[480*.33/5,5], "stun %":1}
		)
	),
	Item("Radiant Gem", {"elemental %":10, "physical to elemental":10, "elemental resist":15}, ["shield", "offhand"],
		Ability(
			"Radiant Shield",
			{"type":"buff", "trigger":"manual", "recharge":30, "duration":12},
			{"fire resist":30, "cold resist":30, "lightning resist":30, "max fire resist":10, "max cold resist":10, "max lightning resist":10}
		)
	),
	Item("Mark of the Myrmidon", {"health":120, "defense":25, "shield recovery":15, "damage reflect %":16}, ["shield"],
		Ability(
			"Blade Barricade",
			{"type":"buff", "trigger":"manual", "recharge":24, "duration":8},
			{"pierce %":90, "pierce resist":30, "max pierce resist":5, "pierce retaliation":424}
		)
	),

	Item("Chipped Claw", {"physical":4, "physical %":12}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Slam",
			{"type":"attack", "trigger":"manual", "recharge":3.5},
			{"weapon damage %":240, "physical":(92+186)/2, "crit damage":30, "physical %":.25*50}
		)
	),
	Item("Chilled Steel", {"cold":3, "cold %":12, "physical to cold":10}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Ice Spike",
			{"type":"attack", "trigger":"manual", "targets":1.5, "shape":"line"}, # no actual recharge not sure how to handle attack replacement...
			{"weapon damage %":22, "triggered cold":(63+92)/2, "slow move":20}
		)
	),
	Item("Mutagenic Ichor", {"poison":[15/5,5], "acid %":10, "poison %":10, "physical to acid":10}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Poison Bomb",
			{"type":"attack", "trigger":"manual", "targets":2.5, "shape":"pbaoe"},
			{"weapon damage %":12, "triggered acid":12, "triggered poison":[124/2,2]}
		)
	),
	Item("Searing Ember", {"fire":3, "fire %":12, "physical to fire":10}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Fireblast",
			{"type":"attack", "trigger":"manual","targets":1.5},
			{"weapon damage %":20, "triggered fire":(52+60)/2, "triggered burn":[126/3,3]}
		)
	),
	Item("Serrated Spike", {"pierce":3+5, "bleed":[9/3,3], "bleed %":12, "energy":-50, "pet pierce":5, "pierce %":25, "pet pierce %":25}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"]),
	Item("Cracked Lodestone", {"lightning":(1+5)/2, "lightning %":12, "physical to lightning":10}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Lightning Nova",
			{"type":"attack", "trigger":"manual", "targets":2.5, "shape":"pbaoe"},
			{"weapon damage %":22, "triggered lightning":(22+108)/2}
		)
	),
	Item("Hollowed Fang", {"vitality decay":[18/3,3], "vitality %":18, "vitality decay %":18, "lifesteal %":5, "physical to vitality":10}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Blooddrinker",
			{"type":"buff", "trigger":"manual", "chance":1, "recharge":26, "duration":8},
			{"bleed":[162/3*.25,3], "attack as health %":20}
		)
	),
	Item("Imbued Silver", {"defense":15, "bleed resist":15, "damage to chthonics":15, "energy":-150, "chaos resist":20, "pet chaos resist":20, "max chaos resist":3, "pet max chaos resist":3}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"]),
	Item("Seal of Blades", {"pierce":10, "lifesteal %":5, "bleed":[30/3,3], "pierce %":50, "bleed %":50, "pierce resist":15, "armor %":8}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Whirling Blades",
			# always on but it ticks damage? 1/s?
			{"type":"attack", "trigger":"attack", "chance":1, "recharge":1, "targets":2.5, "shape":"pbaoe"},
			{"triggered pierce":144, "triggered bleed":[100,1]}
		)
	),
	Item("Seal of Blight", {"vitality":(9+12)/2, "crit damage":6, "acid %":50, "vitality %":50, "poison %":50, "vitality decay %":50, "physical to vitality":10}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Acid Purge",
			#looks like a sustained attack that triggers 3/s. Shape and targets are total guess
			{"type":"attack", "trigger":"manual", "recharge":1, "targets":1.5*3, "shape":"cone"},
			{"weapon damage %":28, "triggered acid":(100+205)/2, "triggered vitality":166, "triggered poison":[950/5,5], "crit damage":25}
		)
	),
	Item("Seal of Corruption", {"aether":11, "lightning %":50, "aether %":50, "electrocute %":50, "physical to aether":10, "offense %":3}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Aether Corruption",
			# looks like a single target that jumps?
			{"type":"attack", "trigger":"manual", "recharge":5, "targets":2.5, "duration":5},
			{"duration":{"triggered lightning":(92+200)/2, "triggered aether":165, "reduce attack speed":25, "reduce cast speed":25, "reduce lightning resist":8, "reduce aether resist":8}}
		)
	),
	Item("Seal of Destruction", {"fire":(8+13)/2, "crit damage":6, "fire %":50, "lightning %":50, "burn %":50, "electrocute %":50, "physical to fire":10}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Stormfire",
			# guessing a lauch that explodes 3-4 fragments (dunno if a target can be hit by mults)
			{"type":"attack", "trigger":"manual", "targets":3.5, "shape":"circle"},
			{"triggered fire":(152+242)/2, "triggered lightning":(136+314)/2, "triggered electrocute":[330/3,3], "crit damage":25}
		)
	),
	Item("Seal of Might", {"physical":13, "physical %":50, "internal %":50, "bleed %":50, "aether to physical":25, "health":160, "energy":-300, "physical resist":4, "pierce resist":12, "vitality resist":12, "bleed resist":12, "pet physical resist":4, "pet pierce resist":12, "pet vitality resist":12, "pet bleed resist":12}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"]),
	Item("Seal of Resonance", {"elemental":10, "aether %":50, "elemental %":50, "physical to elemental":10, "health":160}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"]),
	Item("Seal of Shadows", {"acid":(8+13)/2, "pierce %":50, "acid %":50, "poison %":50, "physical to acid":10, "attack speed":4}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Biting Blades",
			# looks like a line attack with some width?
			{"type":"attack", "trigger":"manual", "recharge":.5, "targets":1.5, "shape":"line"},
			{"weapon damage %":45, "triggered pierce":274, "triggered acid":334, "crit damage":25}
		)
	),
	Item("Seal of Skies", {"lightning":(3+18)/2, "cold %":50, "lightning %":50, "frostburn %":50, "electrocute %":50, "physical to lightning":10, "cast speed":4}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Chain Lightning",
			{"type":"attack", "trigger":"manual", "targets":2},
			{"triggered cold":190, "triggered lightning":(104+385)/2, "crit damage":35}
		)
	),
	Item("Seal of the Night", {"cold":11, "pierce %":50, "cold %":50, "frostburn %":50, "physical to cold":10, "offence %":3}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Chillspikes",
			# cone? 5 projectiles can multiples hit a single target?
			{"type":"attack", "trigger":"manual", "targets":3, "shape":"cone"},
			{"weapon damage %":24, "triggered pierce":116, "triggered cold":(106+184)/2, "triggered frostburn":[525/3,3], "crit damage":35}
		)
	),
	Item("Seal of the Void", {"chaos":(2+19)/2, "fire %":50, "chaos %":50, "burn %":50, "physical to chaos":10, "cast speed":4}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Burning Void",
			{"type":"attack", "trigger":"attack", "chance":.16, "targets":1.5},
			{"weapon damage %":130, "triggered fire":122, "triggered chaos":(65+142)/2, "stun %":100}
		)
	),
	
	# reduce resist applies only to weapon hits (and skills that have a weapon component)
	Item("Mark of Dreeg", {"poison":[50/5,5], "acid %":30, "poison %":30, "reduce resist":10, "physical to acid":10, "light radius":6}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Dreeg's Infinite Gaze",
			{"type":"attack", "trigger":"manual", "recharge":2.5, "targets":2, "shape":"pbaoe"},
			{"weapon damage %":35, "triggered acid":62, "triggered poison":[450/3,3]}
		)
	),
	Item("Vicious Spikes", {"pierce":4+10, "crit damage":4, "pierce %":18+75, "energy":-150, "pet pierce damage":8, "pet pierce damage %":75}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"]),
	Item("Purified Salt", {"defense":15, "life leech resist":25, "damage to aetherials":15, "energy":-150, "aether resist":20, "pet aether resist":20, "max aether resist":3, "pet max aether resist":3}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"]),
	Item("Severed Claw", {"physical":7, "physical %":25, "internal %":15}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Brutal Slam",
			{"type":"attack", "trigger":"manual", "recharge":3.5},
			{"weapon damage %":330, "triggered physical":(122+285)/2, "crit damage":50, "physical %":.33*50, "slow move":30}
		)
	),
	Item("Blessed Steel", {"elemental":4, "elemental %":18, "physical to elemental":10, "offense":18}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Sacred Strike",
			{"type":"attack", "trigger":"manual", "recharge":3, "duration":5, "shape":"weapon"},
			{"weapon damage %":350, "triggered elemental":(165+254)/2, "physical to elemental":100, "duration":{"reduce resist":18}}
		)
	),
	Item("Haunted Steel", {"vitality":8, "vitality %":25, "vitality decay %":25, "lifeleach %":8}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		Ability(
			"Bloodthirster",
			{"type":"buff", "trigger":"manual", "recharge":26, "duration":8},
			{"bleed":[276/3*.25,3], "lifesteal %":24, "bleed resist":20}
		)
	),
	Item("Symbol of Solael", {"chaos":(2+12)/2, "chaos %":35, "physical to chaos":10, "energy absorb":33}, ["sword", "axe", "mace", "dagger", "pistol", "rifle", "crossbow", "twohand", "shield", "offhand"],
		# the resist reduction is strong but it seems only powerful vs bosses /2.
		Ability(
			"Solael's Flame",
			{"type":"attack", "trigger":"manual", "recharge":8, "duration":8},
			{"duration":{"triggered chaos":(84+155)/2, "reduce vitality resist":10, "reduce chaos resist":10}}
		)
	),

	Item("Enchanted Flint", {"fire":5+10, "fire %":25+75, "burn %":25+75, "physical to fire":10, "energy":-150, "burn":[.15*135/3,3], "pet fire":8, "pet burn":135*.15, "pet fire %":75, "pet burn %":75}, ["sword", "axe", "mace", "dagger", "twohand", "shield", "offhand"]),
	Item("Wrathstone", {"aether":5+10, "aether %":25+75, "physical to aether":10, "energy":-150, "aether retaliation":84, "pet aether damage":8, "pet aether %":75, "pet aether retaliation":84}, ["sword", "axe", "mace", "dagger", "twohand", "shield", "offhand"]),
	Item("Coldstone", {"cold":5+10, "cold %":25+75, "frostburn %":25+75, "physical to cold":10, "energy":-150, "slow move":10, "pet cold":8, "pet cold %":75, "pet frostburn %":75}, ["sword", "axe", "mace", "dagger", "twohand", "shield", "offhand"]),
	Item("Vitriolic Gallstone", {"acid":4, "poison":[(20+45)/5,5], "acid %":25+75, "poison %":25+75, "poison duration":20, "physical to acid":10, "energy":-150, "pet poison":35, "pet acid %":75, "pet poison %":75}, ["sword", "axe", "mace", "dagger", "twohand", "shield", "offhand"]),
	Item("Amber", {"lightning":(2+8)/2, "lightning %":25, "electrocute %":25, "physical to lightning":10}, ["sword", "axe", "mace", "dagger", "twohand", "shield", "offhand"],
		Ability(
			"Empowered Lightning Nova",
			{"type":"attack", "trigger":"manual", "targets":2, "shape":"pbaoe"},
			{"weapon damage %":30, "triggered lightning":(40+226)/2}
		)
	),
	Item("Riftstone", {"chaos":(2+8)/2, "chaos %":25, "physical to chaos":10}, ["sword", "axe", "mace", "dagger", "twohand", "shield", "offhand"],
		Ability(
			"Chaos Strike",
			{"type":"attack", "trigger":"manual", "recharge":4, "targets":1.5, "shape":"weapon"},
			{"weapon damage %":270, "triggered vitality":202, "triggered chaos":(86+320)/2}
		)
	),
	Item("Blessed Whetstone", {"pierce %":18, "increase armor pierce":50, "bleed %":25, "offense":18}, ["sword", "axe", "twohand"],
		Ability(
			"Behead",
			{"type":"attack", "trigger":"manual", "recharge":3.5, "targets":1.5},
			{"weapon damage %":280, "triggered pierce":(132+202)/2, "triggered bleed":[660/3*.25,3], "crit damage":50}
		)
	),
	Item("Bloody Whetstone", {"bleed":[30/3,3], "all damage %":8, "bleed %":30, "bleed duration":20}, ["sword", "axe", "twohand"], #two handed sword and axe
		Ability(
			"Decapitate",
			{"type":"attack", "trigger":"manual", "recharge":3.5, "targets":1.5},
			{"weapon damage %":300, "triggered physical":(164+236)/2, "triggered bleed":[920/3*.35,3], "crit damage":50}
		)
	),
	Item("Oleron's Blood", {"physical %":25, "internal %":40, "offense":18, "total speed":2}, ["sword", "axe", "mace", "dagger", "twohand", "pistol", "rifle", "crossbow"],
		Ability(
			"Oleron's Might",
			{"type":"attack", "trigger":"manual", "recharge":3.5, "targets":1, "shape":"weapon"},
			{"weapon damage %":355, "triggered physical":(174+346)/2, "internal":[360/5,5], "crit damage":50, "reduced damage":20}
		)
	),
	Item("Shard of Beronath", {"elemental":8, "all damage %":18, "elemental":8, "offense":25, "physical to elemental":10}, ["sword", "axe", "mace", "dagger", "twohand"],
		Ability(
			"Beronath's Fury",
			# this one is a bit weird with the stacking charges, not gonna mess with it too much
			{"type":"attack", "trigger":"manual", "recharge":.5, "shape":"weapon"},
			{"weapon damage %":114, "elemental":33, "all damage %":20, "elemental %":40}
		)
	),

	Item("Flintcore Bolts", {"fire":5, "burn":[15/3,3], "fire %":25, "burn %":25, "physical to fire":10}, ["pistol", "rifle", "crossbow", "offhand"],
		Ability(
			"Greater Fireblast",
			{"type":"attack", "trigger":"manual", "targets":1.5},
			{"weapon damage %":28, "triggered fire":(95+124)/2, "triggerd burn":[225/3,3], "stun %":15}
		)
	),
	Item("Deathchill Bolts", {"cold":5, "cold %":25, "frostburn %":25, "slow move":25*.12, "physical to cold":10}, ["pistol", "rifle", "crossbow", "offhand"],
		Ability(
			"Greater Ice Spike",
			{"type":"attack", "trigger":"manual", "targets":1.5, "shape":"line"},
			{"weapon damage %":32, "triggered cold":(125+166)/2, "stun %":15, "slow move":20}
		)
	),
	Item("Devil-Touched Ammo", {"fire":6, "all damage %":30*.09, "fire %":30, "chaos %":30, "physical to fire":10}, ["pistol", "rifle", "crossbow", "offhand"],
		Ability(
			"Demon's Breath",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2, "shape":"cone"},
			{"weapon damage %":75, "triggered fire":(144+172)/2, "triggered chaos":(185+236)/2, "attack as health %":8}
		)
	),
	Item("Void-Touched Ammo", {"chaos":(2+8)/2, "chaos %":25, "physical to chaos":10}, ["pistol", "rifle", "crossbow", "offhand"],
		Ability(
			"Chaos Bolt",
			{"type":"attack", "trigger":"manual", "targets":2, "shape":"cone"},
			{"weapon damage %":12, "triggered chaos":(55+118)/2}
		)
	),
	Item("Hell's Bane Ammo", {"lightning":(1+9)/2+(5+15)/2, "lightning %":25+75, "electrocute %":25+75, "physical to lightning":10, "energy":-150, "stun %":12, "pet lightning":(4+12)/2, "pet lightning %":75, "pet electrocute %":75}, ["pistol", "rifle", "crossbow", "offhand"]),
	Item("Venom-Tipped Ammo", {"acid":4, "poison":[20/5,5], "acid %":25, "poison %":25, "poison duration":10, "physical to acid":10}, ["pistol", "rifle", "crossbow", "offhand"],
		Ability(
			"Noxious Poison Bomb",
			{"type":"attack", "trigger":"manual", "targets":1.5, "shape":"circle"},
			{"weapon damage %":15, "triggered acid":32, "triggered poison":[264/2,2], "stun %":25, "reduce resist":12}
		)
	),
	Item("Aethersteel Bolts", {"aether":5, "aether %":25, "physical to aether":10}, ["pistol", "rifle", "crossbow", "offhand"],
		Ability(
			"Aether Tendril",
			{"type":"attack", "trigger":"manual", "recharge":2.5},
			{"weapon damage %":40, "triggered aether":(412+625)/2, "slow %":40, "reduce resist":15}
		)
	),
	Item("Silvercore Bolts", {"pierce":4, "all damage %":18, "offense":30/2, "damage to chthonics":20}, ["pistol", "rifle", "crossbow", "offhand"],
		Ability(
			"Silver Spread",
			{"type":"attack", "trigger":"manual", "recharge":3, "targets":2.5, "shape":"cone"},
			{"weapon damage %":90, "triggered pierce":(122+174)/2, "damage to chthonics":50} #"damage to chthonics":150
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
	Item("Boneback Spine", {"pierce %":25, "bleed %":25, "offense":20}, ["ring", "amulet"]),
	Item("Corpsefiend Tentacle", {"vitality %":25, "aether %":25, "vitality resist":10}, ["ring", "amulet"]),
	Item("Gazer Eye", {"lightning %":25, "aether %":25, "aether resist":10}, ["ring", "amulet"]),
	Item("Rifthound Salts", {"pet total speed":3, "pet elemental resist":15, "pet chaos resist":8}, ["ring", "amulet"]),
	Item("Slith Venom", {"acid resist":15, "bleed resist":15, "poison retaliation":210, "retaliation %":10}, ["ring", "amulet"]),

	#devil's crossing revered
	Item("Cairn's Hope", {"health/s %":15, "energy/s %":15, "constitution %":20, "bleed resist":18}, ["ring", "amulet"]),
	Item("Overseer's Gaze", {"lightning %":30, "stun duration":10, "offense":25, "aether resist":15}, ["ring", "amulet"]),
	Item("Song of the Elements", {"fire %":30, "cold %":30, "elemental resist":15}, ["ring", "amulet"]),
	Item("Survivor's Ally", {"elemental resist":12, "pet all damage %":15, "pet health %":12}, ["ring", "amulet"]),
	Item("Survivor's Ingenuity", {"all damage %":20, "offense %":2, "defense %":2}, ["ring", "amulet"]),
	Item("Survivor's Perseverence", {"aether %":30, "chaos %":30, "aether resist":12, "chaos resist":12}, ["ring", "amulet"]),
	Item("Survivor's Resilience", {"health %":3, "block %":3, "blocked damage %":20}, ["ring", "amulet"]),
	Item("Viloth's Bite", {"poison":[80/5,5], "poison %":30, "stun %":3, "vitality resist":12}, ["ring", "amulet"]),

	Item("Bladeward Powder", {"pierce resist":10}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Mogdrogen's Touch", {"acid resist":10, "vitality resist":7}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),

	#rovers honored
	Item("Arkovian Rose Powder", {"elemental %":18, "energy/s":1, "elemental resist":10}, ["ring", "amulet"]),
	Item("Conjurer's Powder", {"elemental %":20, "health %":3, "pet all damage %":12}, ["ring", "amulet"]),
	Item("Rotbloom Powder", {"vitality %":25, "chaos %":25, "health %":3}, ["ring", "amulet"]),
	Item("Slithweed Powder", {"acid %":25, "poison %":25, "defense":14}, ["ring", "amulet"]),
	Item("Stormtail Viper Venom", {"lightning %":25, "electrocute %":25, "offense":20}, ["ring", "amulet"]),

	Item("Arkovian Bonemeal", {"vitality":8, "vitality %":25, "damage to undead":8}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Arkovian Bonemeal", {"vitality":18, "vitality %":60, "damage to undead":16}, ["twohand", "rifle", "crossbow"]),
	Item("Troll Wart Powder", {"health %":3, "health/s":3, "health/s %":8}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Troll Wart Powder", {"health %":7, "health/s":8, "health/s %":16}, ["twohand", "rifle", "crossbow"]),
	Item("Winterbloom Powder", {"cold %":25, "frostburn %":25, "offense":18}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Winterbloom Powder", {"cold %":60, "frostburn %":60, "offense":40}, ["twohand", "rifle", "crossbow"]),

	#rovers revered
	Item("Breath of Life", {"health %":4, "health/s %":10, "vitality resist":15}, ["ring", "amulet"]),
	Item("Mogdrogen's Blessing", {"pet crit damage":10, "pet offense %":3, "pet attack speed":5}, ["ring", "amulet"]),
	Item("Mogdrogen's Security", {"health":180, "health/s":5, "elemental resist":12}, ["ring", "amulet"]),
	Item("Nature's Wrath", {"acid %":30, "poison %":30, "offense %":2}, ["ring", "amulet"]),
	Item("Rhowan's Resolve", {"physical %":30, "armor absorb":2, "acid retaliation":75, "retaliation %":16}, ["ring", "amulet"]),
	Item("Rhowan's Wisdom", {"elemental %":30, "spirit %":2, "cast speed":2, "elemental resist":12}, ["ring", "amulet"]),
	Item("Spirit of Vengeance", {"vitality %":30, "health %":4, "vitality retaliation":75, "retaliation %":16}, ["ring", "amulet"]),
	Item("Traveler's Boon", {"move speed":2, "armor":40, "slow resist":15}, ["ring", "amulet"]),
	Item("Winter's Chill", {"cold %":30, "frostburn %":30, "stun %":3}, ["ring", "amulet"]),

	Item("Nightshade Powder", {"pierce resist":7, "cold resist":10}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Venomguard Powder", {"acid resist":15}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),

	#kymon's honored
	Item("Blessed Ashes", {"defense":14, "fire resist":15, "lightning resist":15}, ["ring", "amulet"]),
	Item("Consecrated Silver", {"physical %":25, "damage to chthonics":5, "chaos resist":12}, ["ring", "amulet"]),
	Item("Divine Flame", {"fire %":25, "lightning %":25, "elemental resist":10}, ["ring", "amulet"]),
	Item("Firebloom Powder", {"burn %":35, "offense":20, "health/s":8}, ["ring", "amulet"]),
	Item("Storm Powder", {"health":100, "lightning resist":15, "lightning retaliation":(1+107)/2, "retaliation %":10}, ["ring", "amulet"]),

	#kymon's revered
	Item("Empyrion's Touch", {"electrocute":[30/3,3], "electrocute %":100, "health/s":8, "energy absorb":10}, ["ring", "amulet"]),
	Item("Infernal Dust", {"burn":[30/3,3], "burn %":100, "elemental resist":12}, ["ring", "amulet"]),
	Item("Kymon's Fury", {"physical %":30, "bleed %":30, "defense %":2}, ["ring", "amulet"]),
	Item("Kymon's Vision", {"lightning %":30, "electrocute %":30, "offense":25, "chaos resist":12}, ["ring", "amulet"]),
	Item("Kymon's Will", {"fire %":30, "burn %":30, "reduce damage":10*.15, "defense %":2}, ["ring", "amulet"]),

	Item("Demonbane Powder", {"vitality resist":7, "chaos resist":7}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Kymon's Blessing", {"fire resist":15}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Kymon's Conduit", {"lightning resist":15}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),

	#black legion honored
	Item("Aether Dust", {"aether":8, "aether %":25, "damage to aetherials":5}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Aether Dust", {"aether":18, "aether %":60, "damage to aetherials":10}, ["twohand", "rifle", "crossbow"]),
	Item("Blacksteel Powder", {"physical %":25, "fire %":25, "offense":18}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Blacksteel Powder", {"physical %":60, "fire %":60, "offense":40}, ["twohand", "rifle", "crossbow"]),
	Item("Manticore Venom", {"poison":[40/5,5], "poison %":25, "damage to chthonics":5}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Manticore Venom", {"poison":[90/5,5], "poison %":60, "damage to chthonics":10}, ["twohand", "rifle", "crossbow"]),
	Item("Voidbeast Powder", {"vitality %":25, "chaos %":25, "offense":18}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Voidbeast Powder", {"vitality %":60, "chaos %":60, "offense":40}, ["twohand", "rifle", "crossbow"]),
	Item("Witch's Powder", {"pet offense %":3, "pet attack speed":6}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Witch's Powder", {"pet offense %":6, "pet attack speed":12}, ["twohand", "rifle", "crossbow"]),

	#black legion revered
	Item("Aetherstorm Powder", {"lightning %":35, "aether %":35, "elemental resist":10}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Aetherstorm Powder", {"lightning %":80, "aether %":80, "elemental resist":20}, ["twohand", "rifle", "crossbow"]),
	Item("Creed's Cunning", {"elemental %":35, "health":200, "offense":22, "energy/s":1}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Creed's Cunning", {"elemental %":80, "health":440, "offense":45, "energy/s":2}, ["twohand", "rifle", "crossbow"]),
	Item("Essence of Ch'thon", {"vitality %":35, "chaos %":35, "reduce resist":15*.15, "chaos resist":8}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Essence of Ch'thon", {"vitality %":80, "chaos %":80, "reduce resist":60*.15, "chaos resist":16}, ["twohand", "rifle", "crossbow"]),
	Item("Oleron's Fervor", {"all damage %":200*.1, "physical %":35, "bleed %":35, "pierce resist":10}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Oleron's Fervor", {"all damage %":500*.1, "physical %":80, "bleed %":80, "pierce resist":20}, ["twohand", "rifle", "crossbow"]),
	Item("Ulgrim's Guile", {"pierce":8, "pierce %":25, "cold %":35, "offense":22}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Ulgrim's Guile", {"pierce":18, "pierce %":60, "cold %":80, "offense":45}, ["twohand", "rifle", "crossbow"]),

	Item("Kingsguard Powder", {"pierce resist":7, "acid resist":10}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Mankind's Vigil", {"aether resist":7, "chaos resist":7}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),

	#outcast revered
	Item("Outcast's Bastion", {"defense":10, "aether resist":8, "chaos resist":8}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Bastion", {"defense":22, "aether resist":16, "chaos resist":16}, ["twohand", "rifle", "crossbow"]),
	Item("Outcast's Deathtouch", {"vitality":10, "vitality %":35, "vitality decay %":35, "health":200}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Deathtouch", {"vitality":22, "vitality %":80, "vitality decay %":80, "health":440}, ["twohand", "rifle", "crossbow"]),
	Item("Outcast's Frostbite", {"cold %":35, "frostburn %":35, "stun %":3, "health":200}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Frostbite", {"cold %":80, "frostburn %":80, "stun %":6, "health":440}, ["twohand", "rifle", "crossbow"]),
	Item("Outcast's Inferno", {"fire %":35, "burn %":35, "health":200, "fire resist":12}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Inferno", {"fire %":80, "burn %":80, "health":440, "fire resist":24}, ["twohand", "rifle", "crossbow"]),
	Item("Outcast's Might", {"physical %":35, "pierce %":25, "health":200, "aether resist":8}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Might", {"physical %":80, "pierce %":60, "health":440, "aether resist":16}, ["twohand", "rifle", "crossbow"]),
	Item("Outcast's Riftstorm", {"chaos %":35, "health":200, "offense":22, "energy/s":1}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Riftstorm", {"chaos %":80, "health":440, "offense":45, "energy/s":2}, ["twohand", "rifle", "crossbow"]),
	Item("Outcast's Thunder", {"lightning %":35, "electrocute %":35, "stun %":3, "health":200}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Thunder", {"lightning %":80, "electrocute %":80, "stun %":6, "health":440}, ["twohand", "rifle", "crossbow"]),
	Item("Outcast's Venom", {"acid":10, "acid %":35, "poison %":35, "health":200}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Venom", {"acid":22, "acid %":80, "poison %":80, "health":440}, ["twohand", "rifle", "crossbow"]),
	Item("Outcast's Wrath", {"aether %":35, "offense":11, "damage to aetherials":6, "health":200}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Outcast's Wrath", {"aether %":80, "offense":45, "health":440, "damage to aetherials":12}, ["twohand", "rifle", "crossbow"]),

	Item("Outcast's Elemental Scales", {"fire resist":10, "cold resist":10}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Outcast's Skyguard Powder", {"cold resist":10, "lightning resist":10}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Outcast's Warding Powder", {"aether resist":10}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),

	#homestead honored
	Item("Beast Tamer's Powder", {"pet all damage %":12, "pet defense %":4}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Beast Tamer's Powder", {"pet all damage %":28, "pet defense %":8}, ["twohand", "rifle", "crossbow"]),
	Item("Dermapteran Chitin", {"armor %":4, "pierce resist":8, "reduced stun duration":10}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Dermapteran Chitin", {"armor %":8, "pierce resist":16, "reduced stun duration":20}, ["twohand", "rifle", "crossbow"]),
	Item("Raincaller Powder", {"lightning %":25, "electrocute %":25, "offense":18}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Raincaller Powder", {"lightning %":60, "electrocute %":60, "offense":40}, ["twohand", "rifle", "crossbow"]),
	Item("Stonetusk Hoof", {"physical %":25, "internal %":25, "armor":35}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Stonetusk Hoof", {"physical %":60, "internal %":60, "armor":80}, ["twohand", "rifle", "crossbow"]),
	Item("Voidvine Powder", {"fire":8, "fire %":25, "chaos resist":6}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Voidvine Powder", {"fire":18, "fire %":60, "chaos resist":12}, ["twohand", "rifle", "crossbow"]),

	#homestead revered
	Item("Beastlord's Calling", {"pet all damage %":15, "pet health %":5, "pet defense %":3}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Beastlord's Calling", {"pet all damage %":32, "pet health %":10, "pet defense %":6}, ["twohand", "rifle", "crossbow"]),
	Item("Menhir's Blessing", {"stun duration":10, "physique":17, "armor %":5}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Menhir's Blessing", {"stun duration":20, "physique":35, "armor %":10}, ["twohand", "rifle", "crossbow"]),
	Item("Nature's Harvest", {"poison %":35, "offense":55*.1, "damage to humans":6, "health %":3}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Nature's Harvest", {"poison %":80, "offense":55*.2, "damage to humans":12, "health %":7}, ["twohand", "rifle", "crossbow"]),
	Item("Solar Radiance", {"fire":10, "fire %":35, "offense":22, "energy absorb":10}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Solar Radiance", {"fire":22, "fire %":80, "offense":45, "energy absorb":20}, ["twohand", "rifle", "crossbow"]),

	Item("Flameweave Powder", {"pierce resist":7, "fire resist":10}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Solarstorm Powder", {"fire resist":10, "lightning resist":10}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),

	#death's vigil honored?
	Item("Binding Dust", {"health %":8, "vitality resist":15}, ["ring", "amulet"]),
	Item("Chillheart Powder", {"frostburn %":35, "cold resist":15, "vitality resist":10}, ["ring", "amulet"]),
	Item("Mortal Coil", {"cold %":25, "frostburn %":25, "health":150}, ["ring", "amulet"]),
	Item("Necrotic Flesh", {"vitality %":25, "vitality decay %":15, "bleed resist":15}, ["ring", "amulet"]),
	Item("Ritual Salts", {"burn %":70, "frostburn %":70, "electrocute %":70}, ["ring", "amulet"]),

	#death's vigil revered?
	Item("Keeper's Binding Dust", {"vitality %":30, "pet vitality resist":18}, ["ring", "amulet"]),
	Item("Malkadarr's Chillbane", {"frostburn":[30/3,3], "frostburn %":100, "health":150, "offense":25}, ["ring", "amulet"]),
	Item("Uroboruuk's Anguish", {"vitality %":30, "chaos %":30, "health":200}, ["ring", "amulet"]),
	Item("Uroboruuk's Path", {"aether %":30, "health %":4, "energy/s":1.2}, ["ring", "amulet"]),
	Item("Uroboruuk's Word", {"cold %":30, "vitality %":30, "defense":18, "bleed resist":18}, ["ring", "amulet"]),

	Item("Spellward Powder", {"lightning resist":10, "aether resist":7}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Spiritguard Powder", {"vitality resist":10}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Wraithtouch Powder", {"cold resist":15}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),

	#malmouth resistance honored?
	Item("Blazecore Powder", {"burn":[36/3,3], "fire %":36, "lightning %":36, "burn %":36, "electrocute %":36}, ["ring", "amulet"]),
	Item("Colossus Spine", {"physique":30, "armor %":4, "armor absorb":2}, ["ring", "amulet"]),
	Item("Fleshwarp Powder", {"internal":[60/5,5], "physical %":36, "aether %":36, "internal %":36}, ["ring", "amulet"]),
	Item("Mender's Powder", {"pet health %":10, "pet aether resist":20, "pet chaos resist":20}, ["ring", "amulet"]),
	Item("Nightsteel Polish", {"pierce":10, "pierce %":36, "cold %":36, "frostburn %":36}, ["ring", "amulet"]),
	Item("Void Ash", {"chaos":10, "acid %":36, "chaos %":36, "poison %":36}, ["ring", "amulet"]),

	Item("Imp Eye Powder", {"aether":10, "vitalit %":40, "aether %":40, "vitality decay %":40}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Imp Eye Powder", {"aether":22, "vitalit %":90, "aether %":90, "vitality decay %":90}, ["twohand", "rifle", "crossbow"]),
	Item("Machinist Powder", {"physical %":40, "pierce %":40, "internal %":40, "armor %":5}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Machinist Powder", {"physical %":90, "pierce %":90, "internal %":90, "armor %":10}, ["twohand", "rifle", "crossbow"]),
	Item("Sparkbloom Powder", {"elemental":10, "elemental %":40, "offense":25, "pet attack speed":3}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Sparkbloom Powder", {"elemental":22, "elemental %":90, "offense":50, "pet attack speed":6}, ["twohand", "rifle", "crossbow"]),
	Item("Void Tar", {"chaos %":40, "health %":4, "armor %":5}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Void Tar", {"chaos %":90, "health %":8, "armor %":10}, ["twohand", "rifle", "crossbow"]),

	#Malmouth resistance revered?
	Item("Arcane Heart Powder", {"fire %":50, "aether %":50, "burn %":50, "health":225, "energy/s":1.5}, ["ring", "amulet"]),
	Item("Arcanum Dust", {"elemental %":50, "health":225, "energy/s":1.5, "elemental resist":10}, ["ring", "amulet"]),
	Item("Forgefire", {"aether %":50, "elemental %":50, "defense":25, "energy/s":1.5}, ["ring", "amulet"]),
	Item("Hammerfall Powder", {"physical %":50, "pierce %":50, "internal %":50, "defense":25, "energy/s":1.5}, ["ring", "amulet"]),
	Item("Rotgut Venom", {"acid %":50, "poison %":50, "defense":25, "energy/s":1.5, "pet attack speed":5}, ["ring", "amulet"]),
	Item("Steelbloom Powder", {"physical %":50, "internal %":50, "bleed %":50, "health":225, "energy/s":1.5}, ["ring", "amulet"]),
	Item("Typhoon Powder", {"pierce %":50, "lightning %":50, "electrocute %":50, "health":225, "energy/s":1.5}, ["ring", "amulet"]),

	Item("Malmouth's Aegis", {"cold":12, "cold %":55, "frostburn %":55, "aether resist":10, "armor %":5}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Malmouth's Aegis", {"cold":22, "cold %":120, "frostburn %":120, "aether resist":20, "armor %":10}, ["twohand", "rifle", "crossbow"]),
	Item("Malmouth's Heart", {"lightning":12, "fire %":55, "lightning %":55, "burn %":55, "electrocute %":55, "bleed resist":10}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Malmouth's Heart", {"lightning":25, "fire %":120, "lightning %":120, "burn %":120, "electrocute %":120, "bleed resist":20}, ["twohand", "rifle", "crossbow"]),
	Item("Malmouth's Soul", {"elemental":12, "aether %":55, "elemental %":55, "pierce resist":10}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Malmouth's Soul", {"elemental":25, "aether %":120, "elemental %":120, "pierce resist":20}, ["twohand", "rifle", "crossbow"]),
	Item("Malmouth's Will", {"physical %":55, "lightning %":55, "internal %:":55, "electrocute %":55, "health":250, "vitality resist":10}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Malmouth's Will", {"physical %":120, "lightning %":120, "internal %":120, "electrocute %":120, "health":550, "vitality resist":20}, ["twohand", "rifle", "crossbow"]),

	Item("Malmouth Fortifying Powder", {"health/s %":3, "vitality resist":8}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Malmouth Soulguard Powder", {"pierce resist":8, "aether resist":8}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),
	Item("Malmouth Woundsear Powder", {"vitality resist":8, "bleed resist":8}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),

	#barrowholm honored
	Item("Bloodscale Powder", {"bleed %":40, "health":200, "health %":4}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Bloodscale Powder", {"bleed %":90, "health":440, "health %":8}, ["twohand", "rifle", "crossbow"]),
	Item("Haunted Powder", {"lightning %":40, "aether %":40, "electrocute %":40}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Haunted Powder", {"lightning %":90, "aether %":90, "electrocute %":90}, ["twohand", "rifle", "crossbow"]),
	Item("Spikeshell Powder", {"cold %":40, "acid %":40, "frostburn %":40, "poison %":40, "offense":25, "pet health %":6}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Spikeshell Powder", {"cold %":90, "acid %":90, "frostburn %":90, "poison %":90, "offense":50, "pet health %":12}, ["twohand", "rifle", "crossbow"]),
	Item("Wendigo Fur", {"physical %":40, "vitality %":40, "internal %":40, "vitality %":40, "health":200}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	Item("Potent Wendigo Fur", {"physical %":90, "vitality %":90, "internal %":90, "vitality %":90, "health":440}, ["twohand", "rifle", "crossbow"]),

	#barrowholm revered


	# Item("", {}, ["ring", "amulet"]),

	# Item("", {}, ["sword", "axe", "mace", "dagger", "pistol", "shield", "offhand"]),
	# Item("Potent ", {}, ["twohand", "rifle", "crossbow"]),

	# Item(" Powder", {}, ["head", "chest", "shoulders", "arms", "legs", "feet", "waist"]),

]

equipment = {}

# === ONE HAND MELEE WEAPONS ===
# --- 50 ---
equipment["Black Scourge"] = Item( "Black Scourge",
	{"chaos":(38+77)/2.0, "chaos %":120, "health":140, "offense":22, "reduce cooldown":4, "pet all damage %":45, "pet offence %":6, "pet attack speed":4, "pet chaos resist":30}, 
	["scepter"],
	Ability(
		"Conjure Black Scourge",
		{"type":"summon", "trigger":"kill", "chance":.3, "lifespan":8/2, "recharge":8/3},
		{"triggered chaos":(243+287)/2+142, "triggered physical":140}
	)
)
equipment["Death Omen"] = Item( "Death Omen",
	{"physical":(54+146)/2, "vitality":13, "vitality %":83, "vitality decay %":75, "lifesteal %":7, "physical to vitality":13, "health":249, "health/s %":5, "attack speed":13},
	["mace"],
	Ability( "Mark of Death",
		{"type":"attack", "trigger":"hit", "chance":1, "recharge":2, "duration":5},
		{"triggered vitality":122*5, "reduce health %":20, "reduce defense":100, "slow move":20, "slow attack":20}
	)
)

# === AMULETS ===
# --- 40 ---
equipment["Rhowari Lifecaller"] = Item( "Rhowari Lifecaller", 
	{"vitality %":36, "health":178, "offense":50, "pet all damage %":15, "pet crit damage":9, "pet attack speed":6}, ["amulet"] )
equipment["The Peerless Eye of Beronath"] = Item( "The Peerless Eye of Beronath",
	{"crit damage":8, "offense":75, "health/s %":11, "light radius":20, "elemental resist":15, "all skills":1}, ["amulet"],
	# Ability( "Gaze of Beronath",
	# 	{"type":"attack", "trigger":"manual", "recharge":6, "duration":8, "targets":3, "shape":"pbaoe"},
	# 	{"stun %":20, "defense":70/3} 
	# )
)
equipment["Empowered Bramblewood Amulet"] = Item( "Empowered Bramblewood Amulet",
	{"lightning %":65, "health":355, "acid resist":60, "max acid resist":5, "pierce retaliation":354, "all retaliation %":30, "shaman skills":1, "pet all damage %":43}, ["amulet"] )
equipment["Empowered Stormcaller's Gem"] = Item( "Empowered Stormcaller's Gem",
	{"lightning":(1+17)/2, "lightning %":49, "elemental resist":20, "lightning retaliation":(26+285)/2, "lightning retaliation %":100, "reduce cooldown":5, "storm totem":2, "stormcaller's pact":2}, 
	["amulet"],
	Ability("Lightning Bolt",
		{"type":"attack", "trigger":"attack", "chance":.1, "recharge":2.5, "targets":1.5, "shape":"circle"},
		{"triggered lightning":(78+376)/2.0, "triggered electrocute":[192/2.0,2], "stun %":100})
)


# --- 50 ---
equipment["Pendant of the Royal Crown"] = Item( "Pendant of the Royal Crown", # SET(Royal Exuberance)
	{"all damage %":26, "cunning %":3, "spirit %":3, "offense":65}, ["amulet"] )

# === RINGS ===
# --- 40 ---
equipment["Rhowari Void Seal"] = Item( "Rhowari Void Seal",
	{"chaos":(1+11)/2, "vitality %":21, "chaos %":42, "offense":44, "energy/s %":9, "elemental resist":9}, ["ring"] )

# --- 50 ---
equipment["Seal of the Royal Crown"] = Item( "Seal of the Royal Crown", # SET(Royal Exuberance)
	{"elemental":7, "elemental %":42, "energy":366, "offense":24, "fire resist":38, "lightning resist":34}, ["ring"] )
# --- 58 ---
equipment["Lifegiver Signet"] = Item( "Lifegiver Signet",
	{"lifesteal %":6, "health":464, "offense":4, "defense":23, "constitution %":53, "vitality resist":46, "max vitality resist":3}, ["ring"],
	Ability( "Lifedrinker",
		{"type":"attack", "trigger":"attack", "chance":.08, "recharge":5, "targets":2},
		{"weapon damage %":33, "triggered vitality":72, "attack as health %":33}
	) 
)

# === CHEST ===
equipment["Necrolord's Shroud"] = Item( "Necrolord's Shroud",
	{"armor":909, "health":550, "energy/s":6.6, "physical resist":3, "elemental resist":33, "Undead Legion":3, "Will of the Crypt":3, "pet crit damage":8, "pet health %":5, "pet elemental resist":35,
	 },
	"chest",
	Ability("Necrolord's Aura",
		{"type":"buff", "trigger":"toggle"},
		{"energy/s":-3, "energy":-150, "vitality %":35, "pet vitality %":35, "vitality decay %":35, "pet vitalisty decay %":35, "health %":8, "pet health %":8}
	)
)
equipment["Beastcaller's Shroud"] = Item( "Beastcaller's Shroud",
	{"armor":982, "spirit":24, "health":311, "defense":31, "elemental resist":26, "Summon Hellhound":2, "pet health %":12, "pet attack speed":9, "pet armor %":18, "pet elemental resist":29},
	"chest"
)

# === SET BONUSES ===
equipment["Royal Exuberance (2)"] = Item("Royal Exuberance (2)", 
	{"physique %":5, "cunning %":5, "spirit %":5}, ["set"])
equipment["Royal Exuberance (3)"] = Item("Royal Exuberance (3)", 
	{"all skills":1}, ["set"])

equipment["Beastcaller's Regalia (2)"] = Item("Beastcaller's Regalia (2)",
	{"defense %":5}, ["set"])

equipment["Beastcaller's Regalia (3)"] = Item("Beastcaller's Regalia (3)",
	{"physical resist":8, "pet crit damage":10, "pet health %":5, "pet offense %":5, "pet aether resist":30, "pet chaos resist":30}, ["set"])

equipment["Beastcaller's Regalia (4)"] = Item("Beastcaller's Regalia (4)",
	{"Conjure Primal Spirit":3, "Bonds of Bysmiel":3}, 
	["set"], 
	Ability( "Bestial Rage", 
		{"type":"buff", "trigger":"hit", "chance":1, "recharge":15, "duration":6},
		{"pet total speed":15}
	)
)
