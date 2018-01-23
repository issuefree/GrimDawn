import sys
from dataModel import *
from constellationData import *
from itemData import *
from utils import *
from models import *

from solution import *

import os

model = Model.loadModel("Lilith")

# best = getBestConstellations(model)
# highest, _ = getHighestScoring(best)
# efficient, _ = getMostEfficient(best)

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
				print str(bonus).ljust(25), str(star.bonuses[bonus]).ljust(8), "\t", int(model.calculateBonus(bonus, star.bonuses[bonus]))

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
# print Solution([xP, xC, eel, hound, viper, imp, light, lizard, raven, rat, hawk, jackal, behemothGiantsBlood, ultosHandofUltos, torch], model)
# # evalSol(sol)
# print Solution([xE, hawk, eye, fox, xP, imp, xC, viper, messenger, jackal, torch, ultos, behemothGiantsBlood], model)
# # sol = [light, eel, kraken, hammer, tempest, behemothGiantsBlood]
# print Solution([xE, light, quill, hammer, xC, toad, raven, wolverine, vulture, fiend, crownElementalStorm, sageElementalSeeker, torch, xO, xA], model)
# print Solution([xC, fiend, viper, imp, behemoth, quill, xP, messenger, ultos, magi, torch], model)
# print Solution([xC, xE, fiend, viper, xP, behemoth, imp, magi, quill, messenger, torch, ultosHandofUltos], model)
# # printSol(sol)
# # [xC, jackal, xA, shepherd, toad, raven, bonds]
# print

# evalCon(torch)
# print eye.stars[4].ability.bonuses

# print blackScourge.evaluate(model, "scepter", True)
# print deathOmen.evaluate(model, "mace", True)

# print equipment["Pendant of the Royal Crown"].evaluate(model, "", True)
# print rhowariLifecaller.evaluate(model, "amulet", True)


# evalItems(["Lifegiver Signet", "Rhowari Void Seal"])

# getPathBounds(sol, model)

# print torch.evaluate(model, 3)

# print len(torch.stars)


# print Solution([xC, xP, fiend, viper, wraith, light, messenger, behemoth, hawk, magi, torch, ultosHandofUltos], model)
# print Solution([xP, imp, hound, xA, wolverine, messenger, fiend, quill, behemoth, hawk, magi, sageElementalSeeker, ultosHandofUltos], model)
# print Solution([xP, imp, quill, wolverine, crown, hound, messenger, fiend, xE, light, behemoth, sage, ultosHandofUltos], model)

# print Solution([xP, imp, hound, xA, wolverine, messenger, fiend, quill, behemoth, hawk, magi, sageElementalSeeker, ultosHandofUltos], model)

# print Solution([xC, fiend, viper, xE, imp, behemoth, xO, xA, lion, targo, shieldmaiden, phoenix, messenger, ultosHandofUltos], model) 
# print Solution([xO, lion, xC, fiend, viper, eel, targo, shieldmaiden, quill, messenger, behemoth, phoenix, ultosHandofUltos], model)
# print Solution([xC, xO, fiend, tortoise, panther, quill, targo, behemoth, shieldmaiden, messenger, phoenix, xA, ultosHandofUltos], model)

# print Solution([xE, quill, xA, xO, lion, xC, viper, hound, behemoth, shieldmaiden, phoenix, messenger, ultosHandofUltos, targoShieldWall, magiFissure], model)
# print Solution([xE, light, xA, xO, lion, xC, viper, hound, behemoth, shieldmaiden, phoenix, messenger, ultos, targoShieldWall, magiFissure], model)
# print Solution([xE, light, xO, dryad, xC, viper, hound, behemoth, shieldmaiden, phoenix, wolverine, messenger, ultosHandofUltos, targoShieldWall], model)
# print Solution([xE, spider, xA, xO, lion, xC, fiend, viper, hound, behemoth, phoenix, messenger, targoShieldWall, ultosHandofUltos, torchMeteorShower], model)
# print Solution([xE, hawk, xO, lion, xC, fiend, viper, hound, phoenix, behemoth, toad, messenger, torchMeteorShower, ultosHandofUltos, targoShieldWall], model)
# evalCon(obelisk)

# best = getBestConstellations(model)
# highest, _ = getHighestScoring(best)
# efficient, _ = getMostEfficient(best)

# wanted = list(set(highest + efficient))

# print Solution([xE, raven, light, xC, viper, eel, jackal, lizard, ultosHandofUltos], model) # 32894
# print Solution([xE, spider, xC, viper, imp, eel, jackal, ultosHandofUltos], model) # 32003
# print Solution([xE, spider, xC, viper, rat, eel, wretch, ultosHandofUltos], model) # 31189

# print Solution([xA, xO, lion, xC, fiend, viper, hound, light, behemoth, phoenix, messenger, hawk, targoShieldWall, ultosHandofUltos, torchMeteorShower], model)  # 57740 (56)
# print Solution([xE, hawk, xO, lion, xC, fiend, viper, hound, phoenix, behemoth, toad, messenger, torchMeteorShower, ultosHandofUltos, targoShieldWall], model)

sol = Solution([xC, jackal, viper, imp, raven, bonds, hound, xO, panther, staff, god], model)
print(sol)
sol = Solution([xC, vulture, xO, panther, hound, staff, eel, lion, xE, raven, bonds, xP, god], model)
print(sol)

evalCon(wendigo)

# evalItemMods("ring", augments )
# evalItems(["Necrolord's Shroud", "Beastcaller's Shroud", "Beastcaller's Regalia (4)"])

# for c in Constellation.constellations:
# 	# if not c.requires.intersects(Affinity("1c")) and c.provides > Affinity("1c"):
# 	# if not c.requires.intersects(Affinity("1a")) and c.provides > Affinity("1a"):
# 	if sol.provides > c.requires and len(c.stars) <= 5 and not c in sol.constellations:
# 		print c.id, c.evaluate(model)
