import sys
from dataModel import *
from constellationData import *
from itemData import *
from utils import *
from models import *

import os

model = lachesis
model.checkModel()
# print model

print "------------------------------"

def evalSol(solution):
	# print getSolutionCost(solution)

	if isGoodSolution(solution):
		cost = 0
		for c in solution:
			cost += len(c.stars)
			print c.name.ljust(33), str(int(c.evaluate(model))).ljust(5), cost
	else:
		print "FAIL"




def evalCon(c):
	print c.evaluate(model)

	for star in c.stars:
		if star.ability:
			print star.ability.name, star.ability.effective
		for bonus in star.bonuses:
			if model.get(bonus) != 0:
				print str(bonus).ljust(25), int(star.bonuses[bonus]), "\t", int(model.get(bonus)*star.bonuses[bonus])

# print solutionPath(findBonus("stun %"))

# print leatheryHide.evaluate(model, True)
# print sanctifiedBone.evaluate(model, True)
# print runestone.evaluate(model, True)


# for item in arms:
# 	print item.evaluate(model, "arms", True)

location = "sword"
items = Item.getByLocation(location, components)
for item in items:
	item.evaluate(model, location)
	# print item.name.ljust(20), item.value
items.sort(key=lambda i: i.value, reverse=True)
for item in items:
	print item.evaluate(model, location, True)

sol = [
	xC, 
	fiend, 
	light, 
	raven, 
	magiFissure, 
	xA, 
	anvil, 
	viper, 
	hound, 
	messenger, 
	behemoth, 
	torch,
]
# evalSol(sol)


# evalCon(crown)

