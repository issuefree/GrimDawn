from dataModel import *

def getLinks(wanted, remaining=None):
	maxAffinities = Affinity()
	for c in wanted:
		maxAffinities = maxAffinities.maxAffinities(c.requires)

	if remaining == None:
		remaining = [p for p in Constellation.constellations if p.getTier() <= 1 and not p in wanted]

	possibles = [c for c in remaining if maxAffinities.intersects(c.provides)]

	return possibles

def printSolution(solution, model, pre=""):
	print int(evaluateSolution(solution, model)),":",solutionPath(solution)

def solutionPath(solution, pre=""):
	out = ""
	for c in solution:
		out += c.id + ", "
	out = out[:-2]	
	return pre + "["+out+"],"

def evaluateSolution(solution, model, verbose=False):
	if verbose:
		print "Evaluating solution..."
		print "  " + solutionPath(solution)
	start = time()
	sSol = sorted(solution, key=lambda c: c.evaluate(model), reverse=True)
	value = 0

	abilNum = 0
	for c in sSol:
		if verbose:
			print c.name.ljust(40), int(c.evaluate(model)), int(c.evaluate(model, abilNum))
		if c.hasAttackTrigger():
			value += c.evaluate(model, abilNum)
			abilNum += 1
		else:
			value += c.evaluate(model)
	timeMethod("evaluateSolution", start)
	return value

def getSolutionCost(solution):
	start = time()
	cost = 0
	for s in solution:
		cost += len(s.stars)
	timeMethod("getSolutionCost", start)
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

def findBonus(targetBonuses):
	if type(targetBonuses) == type(""):
		targetBonuses = [targetBonuses]
	targets = []
	for c in Constellation.constellations:		
		for s in c.stars:
			if c in targets:
				break
			for targetBonus in targetBonuses:
				if targetBonus in s.bonuses.keys():
					targets += [c]
					break
				if s.ability:
					if targetBonus in s.ability.bonuses.keys():
						targets += [c]
						break
	return targets

def printBonusList():
	print "All constellation bonuses:"
	bonuses = {}
	for c in Constellation.constellations:
		for s in c.stars:
			for bonus in s.bonuses.keys():
				bonuses[bonus] = True
			if s.ability:
				for bonus in s.ability.bonuses.keys():
					bonuses[bonus] = True

	for key in sorted(bonuses.keys()):
		print "\t\t#\""+key+"\":0, "
		
def getBonuses(constellations=Constellation.constellations, model=None):
	bonuses = {}
	for c in constellations:
		for s in c.stars:
			s.evaluate(model)
			for bonus in s.bonuses.keys():
				if model and not bonus in model.bonuses.keys():
					continue
				if bonus in bonuses.keys():
					bonuses[bonus] += s.bonuses[bonus]
				else:
					bonuses[bonus] = s.bonuses[bonus]
	return bonuses

def getPathBounds(path, model):
	score = 0
	provides = Affinity()
	points = 0
	for c in path:
		score += c.evaluate(model)
		provides += c.provides
		points += len(c.stars)
		print points, score, provides

def evaluateBonuses(model, bonuses):
	value = 0
	for bonus in model.keys():
		if bonus in bonuses.keys():
			value += model.get(bonus)*bonuses[bonus]
	return value

def startsWith(start, complete):
	if len(start) == 0:
		return False
	for i in range(len(start)):
		if start[i] != complete[i]:
			return False
	return True

def getHighestScoring(constellationRanks, verbose=True):
	constellationRanks.sort(key=itemgetter(1), reverse=True)
	thresh = constellationRanks[len(constellationRanks)/6][1] * .8

	if verbose:
		print "\n  Desired constellations (value > %s):"%thresh
	wanted = []
	cv = constellationRanks[0][1]
	for c in constellationRanks:
		if c[1] > thresh:
			wanted += [c[0]]
			if verbose:
				print "         ", str(int(c[1])).rjust(7), c[0].name.ljust(45), c[0].requires
		else:
			if verbose:
				print "       - ", str(int(c[1])).rjust(7), c[0].name.ljust(45), c[0].requires

	return wanted, constellationRanks[0][1]

def getMostEfficient(constellationRanks, verbose=True):
	constellationRanks.sort(key=itemgetter(2), reverse=True)
	thresh = constellationRanks[len(constellationRanks)/6][2] * .8

	if verbose:
		print "\n  Desired constellations (efficiency > %s):"%thresh
	wanted = []
	for c in constellationRanks:
		if c[2] > thresh:
			wanted += [c[0]]
			if verbose:
				print "      ", int(c[2]), c[0].name
		else:
			if verbose:
				print "       - ", int(c[2]), c[0].name

	return wanted, constellationRanks[0][2]

def getBestConstellations(model):
	print "\nEvaluating constellations..."
	constellationRanks = []
	for c in Constellation.constellations:
		if "[" in c.id:
			score = 0
		else:
			score = c.evaluate(model)		
		efficiency = c.evaluate(model)/len(c.stars)
		constellationRanks += [(c, score, efficiency)]
		c.buildRedundancies(model)

	return constellationRanks

def sortByLeastProvides(constellations, model):
	start = time()

	out = sorted(constellations, key=lambda c: c.provides.magnitude())

	timeMethod("sortByScore", start)
	return out

def sortByScore(constellations, model):
	start = time()
	out = sorted(constellations, key=lambda c: c.evaluate(model), reverse=True)
	timeMethod("sortByScore", start)
	return out

def sortByLowScore(constellations, model):
	start = time()
	out = sorted(constellations, key=lambda c: c.evaluate(model), reverse=False)
	timeMethod("sortByScore", start)
	return out

def sortByScorePerStar(constellations, model):
	start = time()
	out = sorted(constellations, key=lambda c: (c.evaluate(model)/len(c.stars)), reverse=True)
	timeMethod("sortConstellationsByScorePerStar", start)
	return out

def sortConstellationsByProvides(constellations):
	start = time()
	out = sorted(constellations, key=lambda c: c.provides.magnitude(), reverse=True)
	timeMethod("sortConstellationsByProvides", start)
	return out

def sortConstellationsByProvidesValue(constellations):
	global globalMetadata
	start = time()
	out = sorted(constellations, key=lambda c: (c.provides*globalMetadata["providesValue"]).magnitude(), reverse=True)
	timeMethod("sortConstellationsByProvidesValue", start)
	return out

def sortConstellationsByProvidesValueScore(constellations, model, valueVector):
	out = sorted(constellations, key=lambda c: (c.provides*valueVector).magnitude()*c.evaluate(model), reverse=True)
	return out

