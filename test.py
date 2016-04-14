from dataModel import *
from constellationData import *
from utils import *

import os

# def loadModel(name):
# 	exec("from models import "+name)
# 	model = eval(name)
# 	model.checkModel()
# 	model.readSeedSolutions()
# 	return model

# nyx = loadModel("nyx")

# from models import nyx

# def getAffinities(constellations):
# 	start = time()
# 	affinities = Affinity()
# 	for c in constellations:
# 		affinities += c.provides
# 	timeMethod("getAffinities", start)
# 	return affinities

# affinities = Affinity()
# for seed in nyx.seedSolutions:
# 	sol = []
# 	for c in seed:
# 		if c.canActivate(affinities):
# 			sol += [c]
# 			affinities = getAffinities(sol)
# 			# print c
# 		else:
# 			print "FAIL FAIL FAIL"
# 			print [str(s) + ", " for s in sol]
# 			print affinities >= c.requires
# 			print affinities, " >= ", c.requires
# 			print affinities
# 			print c

# for s in sorted(nyx.seedSolutions, key=lambda c: evaluateSolution(c, nyx), reverse=True):
# 	print solutionPath(s), evaluateSolution(s, nyx)

# solution = [
# 	xE, 
# 	bat, 
# 	viper, 
# 	gallows, 
# 	hawk, 
# 	manticore, 
# 	jackal, 
# 	eel, 
# 	wendigo, 
# 	revenant, 
# 	xP,
# 	xA,
# 	god
# ]
# # checkSolution(solution)
# # for c in solution:
# # 	print c.name, c.evaluate(nyx)

# print
# print

# solByVal = sorted(solution, key=lambda c: c.evaluate(nyx), reverse=True)

# print solutionPath(solByVal)
# print isGoodSolution(solution)

# print
# print

# bonuses = {}
# for c in solution:
# 	for s in c.stars:
# 		for bonus in s.bonuses.keys():
# 			if bonus == "triggered physical":
# 				print c.name
# 			if not bonus in bonuses.keys():
# 				bonuses[bonus] = 0
# 			bonuses[bonus] += s.bonuses[bonus]
# for bonus in sorted(bonuses.keys()):
# 	print bonus, bonuses[bonus]

# print revenant.abilities[0].ability.effective

# optimizations to try:

# consider tracking all bounded paths of low length or low points. It may be worth the extra time to nip paths in the bud early if they're redundant.

# consider making a run with path length capped at some low number to identify useless paths across the set. 
	# If we start on xA and there's an optimal start at xC we may evaluate several million unnecessary solutions.
	# the cost of a run to detph 3 or 4 may not be very high relative to the gain.

# there's a flaw in our approach to attack triggered abilities.
#	1. I don't want more attack triggered abilities than I have decent attacks.
#	2. The attacks per second isn't our total attacks per second it's the a/s of the linked ablity.
#		I don't know the ability at analysis time so I can't really put a good a/s number on it.
#		I think I'll have to use this as a guide and tweak the numbers after the fact.

# Some abilities may have pretty different value for melee vs ranged characters. Specifically pbaoe abilities.
	# consider a pbaoe flag in the ability and adjust the dynamic values based on the characters flag of melee/ranged

#IN GAME:
	# check if fetid pool ticks damage on targets.




# try:
# 	os.mkdir("nyx")
# except:
# 	pass
# file = open("nyx/solutions.py", 'w')
# out = "nyx.seedSolutions = [\n"
# for s in nyx.seedSolutions:
# 	out += "  "+solutionPath(s)+"\n"
# out = out[:-2] + "\n"
# out += "]"
# file.write(out)
# file.close()

# nyx.seedSolutions = None

# file = open("nyx/solutions.py", "r")
# lines = file.read()
# exec(lines)

# nyx.readSeedSolutions()

# print nyx.seedSolutions



for bonus in sorted(getBonuses().keys()):
	print bonus
