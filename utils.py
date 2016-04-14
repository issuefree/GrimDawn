from dataModel import *

def printSolution(solution, model, pre=""):
	value = 0
	out = pre
	for c in solution:
		out += c.name + ", "
		value += c.evaluate(model)
	out = out[:-2]
	print int(value),":",out

def solutionPath(solution, pre=""):
	out = ""
	for c in solution:
		out += c.id + ", "
	out = out[:-2]	
	return pre + "["+out+"],"

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

def isGoodSolution(solution):
	affinities = Affinity()
	sol = []
	for c in solution:
		if c.canActivate(affinities):
			sol += [c]
			affinities = getAffinities(sol)
		else:
			print c.name
			return False
	return True

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
			for bonus in s.bonuses.keys():
				if bonus in bonuses.keys():
					bonuses[bonus] += s.bonuses[bonus]
				else:
					bonuses[bonus] = s.bonuses[bonus]
	return bonuses