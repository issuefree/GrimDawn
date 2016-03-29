def checkModel(model):
	# handle shorthand sets: retaliation, resist	
	# retaliation types
	parts = ["chaos retaliation", "life leech retaliation", "pierce retaliation", "vitality decay retaliation", "physical retaliation", "bleed retaliation"]

	model["retaliation"] = getValue("retaliation", model)
	for b in parts:
		model[b] = max(getValue(b, model), model["retaliation"])

	#resist types
	parts = ["physical resist", "fire resist", "cold resist", "lightning resist", "acid resist", "poison resist", "vitality resist", "pierce resist", "aether resist", "chaos resist"]
	model["resist"] = getValue("resist", model)
	for b in parts:
		model[b] = max(getValue(b, model), model["resist"])

	# elemental damage % and resist should be the sum of the individual components
	parts = ["cold %", "lightning %", "fire %"]
	model["elemental %"] = max(getValue("elemental %", model), sum([getValue(b, model) for b in parts]))

	# elemental resists are weird. e.g. fire resist protects against burn and elemental resist protects against fire but elemental resist does not protect against burn
	parts = ["cold resist", "lightning resist", "fire resist"]
	model["elemental resist"] = max(getValue("elemental resist", model), sum([getValue(b, model) for b in parts]))

	# all damage should be >= all other damage bonuses (sans retaliation)
	# don't count cold, lightning, or fire as they're already aggregated under elemental
	parts = ["acid %", "aether %", "bleed %", "burn %", "chaod %", "electrocute %", "elemental %", "frostburn %", "internal %", "physical %", "pierce %", "poison %", "vitality %"]
	model["all damage %"] = max(getValue("all damage %", model), sum([getValue(b, model) for b in parts]))

	#nothing grants total speed

	# physique grants health/s, health and defense so this should be accounted for
	val = 0
	val += getValue("health/s", model) * .04
	val += getValue("health", model) * 3
	val += getValue("defense", model) * .5

	model["physique"] = max(getValue("physique", model), val)

	# cunning grants physical %, pierce %, bleed %, internal % and offense.
	val = 0
	val += getValue("physical %", model) * .33
	val += getValue("pierce %", model) * .285
	val += getValue("bleed %", model) * .333
	val += getValue("internal %", model) * .333
	val += getValue("offense", model) * .5

	model["cunning"] = max(getValue("cunning", model), val)

	# spirit grants fire %, burn %, cold %, frostburn %, lightning %, electrocute %, acid %, poison %, vitality %, vitality decay%, aether %, chaos %, energy and energy regen
	val = 0
	val += sum([getValue(b, model) for b in ["elemental %", "acid %", "vitality %", "aether %", "chaos %"]]) * .33
	val += sum([getValue(b, model) for b in ["burn %", "frostburn %", "electrocute %", "poison %", "vitality decay %"]]) * .333
	val += getValue("energy", model) * 2
	val += getValue("energy/s", model) * .01

	model["spirit"] = max(getValue("spirit", model), val)

model = {"offense":10, "offense %":200, "vitality %":10, "chaos %":5, "defense":2, "defense %":20, "armor":2, "armor %":20, "resist":3}

checkModel(model)
print 
for bonus in sorted(model.keys()):
	if model[bonus] > 0:
		print bonus, model[bonus]
	