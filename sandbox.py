import sys
from dataModel import *
from constellationData import *
from itemData import *
from utils import *
from models import *

from solution import *

import os

model = Model.loadModel("Armitage")
model.checkModel()
# print model

print "------------------------------"

def evalSol(solution):
	# print getSolutionCost(solution)

	cost = 0
	score = 0
	for c in solution:
		cost += len(c.stars)
		score += c.evaluate(model)
		print c.name.ljust(33), str(int(c.evaluate(model))).ljust(5), cost
	print "Total score: ", score

	if not isGoodSolution(solution):
		print "FAIL"

def printSol(sol):
	bonuses = getBonuses(sol, model)
	calculatedBonuses = []
	for bonus in bonuses:
		calculatedBonuses.append([bonus, int(bonuses[bonus]), int(evaluateBonuses(model.bonuses, {bonus:bonuses[bonus]}))])
	calculatedBonuses.sort(key = lambda b: b[2], reverse=True)
	for bonus in calculatedBonuses:
		print bonus[0].ljust(25), str(bonus[1]).ljust(5), str(bonus[2])

def evalItemMods(location, itemType):
	# location = "amulet"
	items = Item.getByLocation(location, itemType)
	for item in items:
		item.evaluate(model, location)
		# print item.name.ljust(20), item.value
	items.sort(key=lambda i: i.value, reverse=True)
	for item in items:
		if item.value > 0:
			print item.evaluate(model, location, True)

def evalItems(itemList):
	items = []
	for item in itemList:
		if type(item) == type(""):
			item = equipment[item]
		items += [item]
		item.evaluate(model)
	items.sort(key=lambda i: i.value, reverse=True)
	for item in items:
		if item.value > 0:
			print item.evaluate(model, "", True)



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

# model.bonuses["reduce resist"] = 0
# evalItemMods("waist", augments )

# sol = [
# 	xC, 
# 	fiend, 
# 	light, 
# 	raven, 
# 	magiFissure, 
# 	xA, 
# 	anvil, 
# 	viper, 
# 	hound, 
# 	messenger, 
# 	behemoth, 
# 	torch,
# ]

# sol = [xC, jackal, rat, raven, bonds, xA, shepherd]
# evalSol(sol)

# sol = [xA, xC, shepherd, wolverine, toad, raven, jackal]
# evalSol(sol)

# sol = [xC, jackal, xA, shepherd, xE, raven, bonds, crownElementalStorm]
# evalSol(sol)
# printSol(sol)

  
# sol = [xC, xE, fiend, viper, hound, raven, behemoth, quill, messenger, hammer, toad, sage, torchMeteorShower, ] #59173

# sol = [xE, spider, quill, light, hawk, xC, viper, hound, messenger, jackal, ultos, torch, behemothGiantsBlood]

sol = [raven, hammer, panther, wraith, tempest]
sol = [hawk, rat, light, eel, jackal, hound, ultosHandofUltos]
print Solution([xP, xC, eel, hound, viper, imp, light, lizard, raven, rat, hawk, jackal, behemothGiantsBlood, ultosHandofUltos, torch], model)
# evalSol(sol)
print Solution([xE, hawk, eye, fox, xP, imp, xC, viper, messenger, jackal, torch, ultos, behemothGiantsBlood], model)
# sol = [light, eel, kraken, hammer, tempest, behemothGiantsBlood]
print Solution([xE, light, quill, hammer, xC, toad, raven, wolverine, vulture, fiend, crownElementalStorm, sageElementalSeeker, torch, xO, xA], model)
# printSol(sol)
# [xC, jackal, xA, shepherd, toad, raven, bonds]
print

# evalCon(torch)
# print eye.stars[4].ability.bonuses

# print blackScourge.evaluate(model, "scepter", True)
# print deathOmen.evaluate(model, "mace", True)

# print equipment["Pendant of the Royal Crown"].evaluate(model, "", True)
# print rhowariLifecaller.evaluate(model, "amulet", True)


# evalItems(["Lifegiver Signet", "Rhowari Void Seal"])

# getPathBounds(sol, model)

# print torch.evaluate(model, 3)

import random

print random.sample(Constellation.constellations, 2)