import sys
from dataModel import *
from constellationData import *
from utils import *
from models import *

import os

model = lochlan
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


evalCon(tortoise)