import sys
from time import time
import random

from constellationData import *
from dataModel import *

methodTimes = {}
def timeMethod(label, startTime):
	if label in methodTimes.keys():
		methodTimes[label] += time()-startTime
	else:
		methodTimes[label] = time()-startTime


#this relies on state which I'd rather not
def getAvailableStars(constellations, affinities):
	start = time()
	available = []
	for c in constellations:
		for s in c.stars:
			if s.canActivate(affinities):
				available += [s]
	timeMethod("getAvailableStars", start)
	return available

def getAvailableConstellations(current, constellations, affinities):
	start = time()
	available = []
	for c in constellations:
		if not c in current and c.canActivate(affinities):
			available.append(c)
	timeMethod("getAvailableConstellations", start)
	return available

# cache if performance becomes an issue
def getAffinities(constellations):
	start = time()
	affinities = Affinity()
	for c in constellations:
		affinities += c.provides
	timeMethod("getAffinities", start)
	return affinities

def getBonuses():
	bonuses = {}
	for c in Constellation.constellations:
		for s in c.stars:
			if s.active:
				for bonus in s.bonuses.keys():
					if bonus in bonuses.keys():
						bonuses[bonus] += s.bonuses[bonus]
					else:
						bonuses[bonus] = s.bonuses[bonus]
	return bonuses

def sortConstellationsByScore(constellations, model):
	start = time()
	list = sorted(constellations, key=lambda c: c.evaluate(model), reverse=True)
	timeMethod("sortConstellationsByScore", start)
	return list

def sortConstellationsByProvides(constellations):
	start = time()
	list = sorted(constellations, key=lambda c: c.provides.magnitude(), reverse=True)
	timeMethod("sortConstellationsByProvides", start)
	return list



# xC.stars[0].active = True
# # spider.stars[0].active = True
# fiend.stars[0].active = True
# fiend.stars[1].active = True
# fiend.stars[2].active = True
# fiend.stars[3].active = True
# # print getBonuses()

def evaluateBonuses(model, bonuses):
	value = 0
	for bonus in model.keys():
		if bonus in bonuses.keys():
			value += model[bonus]*bonuses[bonus]
	return value

# print spider.evaluate(model)
# print fiend.evaluate(model)
# print fiend.stars[0].evaluate(model)

# search methodology:
# I think it needs to be depth first because only a complete solution has value since I'm looking for optimal endgame.
# I'm not ready to consider both activating and refunding stars. This complicates things but I think it's required for an optimal solution.
# I don't know how to branch and bound because there could be lots of valueless steps in a path building requirements that ends up optimal.
# I don't think I can search the entire space.
# I think I'm going to have to build a fair amount of a priori knowledge into the search. This will probably result in "obvious" decent solutions early but push less obvious potentially more optimal solutions later.
	# I could evaluate constellations as a whole to prioritize solutions but I may want less valuable constellations if they're efficient for affinity requirements
	# However, if a constellation has no/low value and the high value constellations don't require what it provides I can prune it from the search space. This may cascade into a vastly reduced search space.
		# I think it makes sense to work from value down.
		#  Evaluate constellations and sort and process in order
		#  	Anything that provides something I need is marked as valuable and evaluated.
		#     Anything that provides something I need....
		# Repeat until I run out of constellations or I hit one below the threshold. All unmarked constellations are useless.
# If I approach this treating contellations as whole entities and trim the space as above for initial pass I think I may be able to evaluate the whole space.


def getNeededConstellations(current, points, wanted, affinities=Affinity(0)):
	start = time()
	needed = wanted[:]
	for c in Constellation.constellations:
		if not c in current and not len(c.stars) > points and c.canActivate(affinities) and not c in needed:
			for w in wanted:
				if not len(w.stars) > points and w.canActivate(affinities) and w.needs(c, affinities):
					needed.append(c)
					break
	timeMethod("getNeededConstellations", start)
	return needed

bonuses = {}
for c in Constellation.constellations:
	for s in c.stars:
		for bonus in s.bonuses.keys():
			bonuses[bonus] = True

# for bonus in sorted(bonuses.keys()):
# 	# if bonus.find("retaliation") >= 0:
# 	print bonus



# print model
# model.checkModel()
# print model

# searchConstellations = getNeededConstellations(wanted)


def printSolution(solution, model, pre=""):
	value = 0
	out = pre
	for c in solution:
		out += c.name + ", "
		value += c.evaluate(model)
	print value,":",out

def solutionPath(solution, pre=""):
	out = pre
	for c in solution:
		out += c.name + ", "
	return out

def getSolutionHash(solution):
	sSol = sorted(solution, key=lambda c: c.name)
	sol = ""
	for c in sSol:
		sol += c.name
	return sol


def evaluateSolution(solution, model):
	value = 0
	for c in solution:
		value += c.evaluate(model)
	return value

# print len(searchConstellations)

def getSolutionCost(solution):
	cost = 0
	for s in solution:
		cost += len(s.stars)
	return cost

def getUpperBoundScore(solution, points, wanted, model):
	score = evaluateSolution(solution, model)
	for c in wanted:
		if not c in solution and len(c.stars) <= points:
			score += c.evaluate(model)
			points -= len(c.stars)
	return score

# {"one":
# 	{"two":
# 		{"three":True},
# 		{"four":True},
# 		{"five":
# 			{"six":True}
# 		}
# 	}
# }


def killSolution(solution):
	# print "Killing solution: " + solutionPath(solution)
	sSol = sorted(solution, key=lambda c: c.name)
	deadNode = deadSolutions
	for sol in sSol:
		if sol == sSol[-1]:
			deadNode[sol.name] = True			
			return

		if not sol.name in deadNode.keys():
			deadNode[sol.name] = {}
		deadNode = deadNode[sol.name]		


def isDeadSolution(solution):
	sSol = sorted(solution, key=lambda c: c.name)
	deadNode = deadSolutions
	for sol in sSol:
		if not sol.name in deadNode.keys():
			return False
		if deadNode[sol.name] == True:
			return True
		deadNode = deadNode[sol.name]
	return False


def doMove(model, wanted, points, solution=[]):	
	global bestScore, bestSolution, checkedSolutions, deadSolutions

	if len(solution) > 0:
		# sol = getSolutionHash(solution)
		# if sol in checkedSolutions:
		# 	return
		# checkedSolutions[sol] = True

		if isDeadSolution(solution):
			return

		trimSolution = solution[:]
		ub = getUpperBoundScore(trimSolution, points, wanted, model)
		while ub < bestScore:
			killSolution(trimSolution)

			trimMove = trimSolution[-1]
			trimSolution = trimSolution[:-1]
			# print "Dead branch : best possible score: " + str(ub)
			# printSolution(solution, model, "    ")
			# print "Skipping due to low score:", str(ub), "<", bestScore
			# printSolution(solution, model)
			ub = getUpperBoundScore(trimSolution, points+len(trimMove.stars), wanted, model)
			if ub < bestScore:
				print "    Trimming branch (" +str(getSolutionCost(trimSolution)) +"): " + solutionPath(trimSolution)
		
		if isDeadSolution(solution):
			return

	affinities = getAffinities(solution)
	
	searchConstellations = getNeededConstellations(solution, points, wanted, affinities)
	availableConstellations = getAvailableConstellations(solution, searchConstellations, affinities)
	# nextMoves = sortConstellationsByScore(availableConstellations, model)
	# nextMoves = sortConstellationsByProvides(availableConstellations)
	random.shuffle(availableConstellations)
	nextMoves = availableConstellations

	# printSolution(solution, model)
	# print "Points remaining:" + str(points)
	# if len(solution) >= 5:
	# 	return
	# for nm in nextMoves:
	# 	print "    " + str(nm.name) + ": " + str(nm.evaluate(model) )

	isSolution = True
	for move in nextMoves:
		if points >= len(move.stars):
			isSolution = False
			doMove(model, wanted, points-len(move.stars), solution+[move])
	
	killSolution(solution)
	if getSolutionCost(solution) < 25:
		print "    Trimming evaluated branch (" + str(getSolutionCost(solution)) + "): " + solutionPath(solution)
	
	# printSolution(solution, model)
	if isSolution:
		score = evaluateSolution(solution, model)
		if score > bestScore:
			bestScore = score
			bestSolution = solution
			print "New best: "
			# printSolution(solution, model)
		printSolution(solution, model)
	# print methodTimes

nyx = Model(
	{
		"spirit":12.5, 
		"offense":15, 
		"crit damage":3,
		"vitality %":20,
		"chaos %":7.5,
		"cast speed":5,
		"defense":5,
		"armor":3, 
		# armor absorb is good vs lots of little hits. This char regens fast with lots of little enemies so there's not much value
		"armor absorb":2,
		"health":.5, "health/s":1,
		"energy":.1, "energy/s":5,
		"avoid melee":10, "avoid ranged":15,
		"resist":7.5,

		"pet attack speed":3,
		"pet total speed":5,
		"pet offense":5,
		"pet offense %":50,
		"pet lifesteal %":2,
		"pet all damage %":7.5,
		"pet defense %":1,
		"pet resist":1.5,
		"pet health %":5,
		"pet health/s":1,
		"pet retaliation":1, "pet retaliaion %":3,

		"triggered vitality":30, "triggered vitality decay":10,
		"triggered chaos":3,
		"triggered fire":1.5,
		"triggered life leech":1.5,
		"triggered damage":1,
		
		"weapon damage %":1,
		"slow move":7,
		"stun %":10
	},

	{
		"attacks/s":10,
		"hits/s":1.5,
		"blocks/s":0,
		"crit chance":.09,
		"low healths/s":1.0/30, # total guesswork.

		"physique":650,
		"cunning":400,
		"spirit":650,

		"offense":1350,
		"defense":1000,

		"health":5000,
		"armor":450,

		"vitality %":750+350,
		"chaos %":350,

		"fight length":30
	}
)

print nyx

Constellation.constellations.remove(hydra)
Constellation.constellations.remove(scepter)
Constellation.constellations.remove(shieldmaiden)
Constellation.constellations.remove(blades)
Constellation.constellations.remove(berserker)
Constellation.constellations.remove(kraken)
#shield based abilities
Constellation.constellations.remove(anvil)
Constellation.constellations.remove(boar)
Constellation.constellations.remove(targo)
Constellation.constellations.remove(obelisk)


constellationRanks = []
for c in Constellation.constellations:
	constellationRanks += [(c, c.evaluate(nyx)/len(c.stars))]

constellationRanks.sort(key=itemgetter(1), reverse=True)

thresh = constellationRanks[len(constellationRanks)/2][1]*.9

print "Desired constellations"
wanted = []
for c in constellationRanks:
	if c[1] > thresh:
		wanted += [c[0]]
		print "  ", c[0].evaluate(nyx), c[0].name
print len(wanted)


# 17714.3822581 : Crossroads Ascendant, Shepherd's Crook, Wolverine, Owl, Crossroads Chaos, Viper, Jackal, Eel, Wendigo, Crossroads Order, Tortoise, Panther, Crossroads Primordial, Dying God
#17748.2414442 : Crossroads Ascendant, Shepherd's Crook, Crossroads Eldrich, Bat, Raven, Viper, Affliction, Bysmiel's Bonds, Crossroads Chaos, Crossroads Order, Tortoise, Wendigo, Dryad, 
#17775.7414442 : Crossroads Ascendant, Shepherd's Crook, Crossroads Eldrich, Bat, Fiend, Affliction, Bysmiel's Bonds, Crossroads Order, Tortoise, Dryad, Panther, Wendigo, 
#19187.7679724 : Crossroads Order, Tortoise, Crossroads Eldrich, Raven, Bat, Rat, Gallows, Panther, Solemn Watcher, Viper, Wendigo, Dying God, 
# New best: 
# 19576.7679724 : Crossroads Eldrich, Hawk, Crossroads Order, Tortoise, Gallows, Panther, Bat, Fiend, Wendigo, Viper, Solemn Watcher, Dying God, 
# New best: 
# 19581.4179724 : Crossroads Eldrich, Hawk, Crossroads Order, Tortoise, Gallows, Panther, Bat, Rat, Viper, Wendigo, Revenant, Dying God, 
seedSolutions = [
	[xA, shepherd, wolverine, owl, xC, viper, jackal, eel, wendigo, xO, tortoise, panther, xP, god],
	[xO, tortoise, xE, raven, bat, rat, gallows, panther, watcher, viper, wendigo, god],
	[xA, shepherd, xE, bat, fiend, affliction, bonds, xO, tortoise, dryad, panther, wendigo],
	[xA, shepherd, xE, bat, raven, viper, affliction, bonds, xC, xO, tortoise, wendigo, dryad],
	[xE, hawk, xO, tortoise, gallows, panther, bat, fiend, wendigo, viper, watcher, god],
	[xE, hawk, xO, tortoise, gallows, panther, bat, rat, viper, wendigo, revenant, god]
]



bestSolution = []
bestScore = 0

for sol in seedSolutions:
	score = evaluateSolution(sol, nyx)
	printSolution(sol, nyx)
	if score > bestScore:
		bestScore = score
		bestSolution = sol
print bestScore

checkedSolutions = {}
deadSolutions = {}

# doMove(nyx, wanted, 50)

for c in Constellation.constellations:
	for a in c.abilities:
		print a.name, a.evaluate(nyx)

# killSolution([xA, hawk, shepherd])
# print deadSolutions
# killSolution([xA, hawk, viper])
# print deadSolutions
# killSolution([xP, hawk, viper])
# print deadSolutions
# # killSolution([xA, hawk])
# print isDeadSolution([xA, hawk, scepter])

# I think the next step is to look at trying to branch and bound.
# I think this is pretty nonlinear so I don't have a real good way of doing that.
#	an expensive way would be to look at each solution's best possible outcome by adding the best scoring constellations to the solution up to the remaining points and if it's not better than my current best don't continue.

print scales.stars[-1].bonuses
