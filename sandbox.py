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

def evalSol():
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



solution = [xO, dryad, tortoise, hound, targoShieldWall, xA, anvil, messenger, fiend, light, behemoth, crown]

# evalSol(solution)

evalCon(crown)