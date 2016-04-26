import sys
from dataModel import *
from constellationData import *
from utils import *
from models import *

import os

model = armitage
model.checkModel()
# print model

print "------------------------------"

def evalSol(solution):
	# print getSolutionCost(solution)

	if isGoodSolution(solution):
		for c in solution:
			print c.name, c.evaluate(model)
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



solution = [
	xC,
	viper,
	hound,
	xO,
	lion,
	targoShieldWall,
	xA,
	anvil,
	messenger,
	xE,
	light,
	behemothGiantsBlood,
	raven,
	crown,
	magiFissure
]

solution = [xO, dryad, tortoise, hound, targoShieldWall, xA, anvil, messenger, viper, xE, light, behemoth, crown]
# solution = [xO, dryad, tortoise, hound, targo, shieldmaiden, xA, anvil, messenger, viper, obelisk]

# solution = [xC, fiend, viper, hound, light, behemothGiantsBlood, xO, tortoise, lion, targoShieldWall, xA, anvil, messenger, crown]

# evalSol(solution)
print evaluateSolution(solution, model, True)



# bonuses = getBonuses(solution, model)
# for bonus in sorted(bonuses.keys(), key=lambda bonus: model.bonuses[bonus]*bonuses[bonus], reverse=True):
# 	print bonus.ljust(23), str(int(bonuses[bonus])).rjust(4), str(int(model.bonuses[bonus]*bonuses[bonus])).rjust(5)

evalCon(shieldmaiden)
