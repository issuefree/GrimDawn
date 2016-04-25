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

def evaluateSolution(solution, model, verbose=False):
	if verbose:
		print "Evaluating solution..."
		print "  " + solutionPath(solution)
	start = time()
	attackAbilities = []
	for c in solution:
		for star in c.abilities:
			if star.ability.gc("trigger") == "attack" or star.ability.gc("trigger") == "critical":
				attackAbilities += [star]
	attackAbilities.sort(key=lambda s: s.evaluate(model), reverse=True)	
	if verbose:
		print "   ", len(attackAbilities), "attack abilities"
	value = 0		
	# if "allAttacks/s" in model.stats.keys() and model.getStat("numAttackAbilities") != numAttackAbilities:
	# 	model.stats["numAttackAbilities"] = numAttackAbilities
	# 	if numAttackAbilities > 1:
	# 		model.stats["attacks/s"] = sum(model.stats["allAttacks/s"][:numAttackAbilities])/numAttackAbilities
	# 	else:
	# 		model.stats["attacks/s"] = model.stats["allAttacks/s"][0]
	# 	if verbose:
	# 		print "    ", model.stats["attacks/s"], "effective attacks/s"
	# 	for c in solution:
	# 		c.value = None
	# 		for star in c.abilities:
	# 			star.value = None
	# 		value += c.evaluate(model)
	# 		if verbose:
	# 			print c.name.ljust(25), c.evaluate(model)
	# else:
	for c in solution:
		value += c.evaluate(model)		
		if verbose:
			print c.name.ljust(25), c.evaluate(model)
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


def printBonusList():
	print "All constellation bonuses:"
	bonuses = {}
	for c in Constellation.constellations:
		for s in c.stars:
			for bonus in s.bonuses.keys():
				bonuses[bonus] = True
	for key in sorted(bonuses.keys()):
		print "  "+key
		
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

def evaluateBonuses(model, bonuses):
	value = 0
	for bonus in model.keys():
		if bonus in bonuses.keys():
			value += model[bonus]*bonuses[bonus]
	return value

def startsWith(start, complete):
	if len(start) == 0:
		return False
	for i in range(len(start)):
		if start[i] != complete[i]:
			return False
	return True