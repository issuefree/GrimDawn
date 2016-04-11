import sys
import random

from constellationData import *
from dataModel import *
from models import *

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


def getNextMoves(current, constellations, affinities, points, model):
	start = time()
	moves = []
	for c in constellations:
		if c in current:
			continue
		if len(c.stars) > points:
			continue
		if not c.canActivate(affinities):
			continue
		moves += [c]
	tempMoves = moves[:]
	for move in tempMoves:
		for other in tempMoves:
			if other in move.redundancies:
				moves.remove(move)
				break

	timeMethod("getNextMoves", start)
	return moves

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

def sortByScore(constellations, model):
	start = time()
	out = sorted(constellations, key=lambda c: c.evaluate(model), reverse=True)
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

def evaluateBonuses(model, bonuses):
	value = 0
	for bonus in model.keys():
		if bonus in bonuses.keys():
			value += model[bonus]*bonuses[bonus]
	return value

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


def getNeededConstellations(current, points, wanted, affinities=Affinity(0), possibles=Constellation.constellations):
	start = time()
	needed = wanted[:]

	#I'm doing this piece by piece when really I need the total need for my wants. This is probably more efficient.
	#I may also be able to identify needs that can be satified by a single constellation.

	maxAffinities = Affinity()
	for c in wanted:
		maxAffinities = maxAffinities.maxAffinities(c.requires)

	neededAffinities = maxAffinities - affinities

	for c in possibles:
		if len(c.stars) > points:  #I don't have enough points so it doesn't matter if I need it
			continue
		if c in current or c in needed:	#I've either already used it or already selected it
			continue
		if c.requires.magnitude() > 1: # Don't select tier 2 constellations JUST because they have a needed affinity.
			continue

		if neededAffinities.intersects(c.provides):
			needed.append(c)			
	timeMethod("getNeededConstellations", start)
	return needed

def printBonusList():
	print "All constellation bonuses:"
	bonuses = {}
	for c in Constellation.constellations:
		for s in c.stars:
			for bonus in s.bonuses.keys():
				bonuses[bonus] = True
	for key in sorted(bonuses.keys()):
		print "  "+key

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

boundedPaths = [[Affinity(),0,0]] #[affinities, cost, score]
def addBoundedPath(solution, model):
	start = time()
	global boundedPaths
	affinities = getAffinities(solution)
	cost = getSolutionCost(solution)
	score = evaluateSolution(solution, model)

	deadBPIs = []
	for bpi in range(len(boundedPaths)-1, -1, -1):
		bp = boundedPaths[bpi]
		if affinities <= bp[0] and cost >= bp[1] and score <= bp[2]: 
			timeMethod("addBoundedPath", start)
			return True
		if affinities >= bp[0] and cost <= bp[1] and score >= bp[2]: 
			# boundedPaths[bpi] = [affinities, cost, score, str(affinities), solutionPath(solution)]
			del boundedPaths[bpi]
	boundedPaths += [[affinities, cost, score, str(affinities), solutionPath(solution)]]
	timeMethod("addBoundedPath", start)
	return False

def checkBoundedPath(solution, model):
	start = time()
	global boundedPaths
	affinities = getAffinities(solution)
	cost = getSolutionCost(solution)
	score = evaluateSolution(solution, model)

	for bpi in range(len(boundedPaths)-1, -1, -1):
		bp = boundedPaths[bpi]
		if affinities <= bp[0] and cost >= bp[1] and score < bp[2]: 
			print "    <-<-  "+str(affinities)+" @ ("+str(cost)+") = "+ str(int(score))
			print "            "+solutionPath(solution)
			print "          "+str(bp[0])+" @ ("+str(bp[1])+") = "+ str(int(bp[2]))
			timeMethod("checkBoundedPath", start)
			return True
		if affinities >= bp[0] and cost <= bp[1] and score > bp[2]: 
			boundedPaths[bpi] = [affinities, cost, score, str(affinities), solutionPath(solution)]
			print "    -->>  "+str(affinities)+" @ ("+str(cost)+") = "+ str(int(score))+ "  " + str(affinities.magnitude()*score/cost)
			print "          "+str(bp[0])+" @ ("+str(bp[1])+") = "+ str(int(bp[2]))+ "  " + str(bp[0].magnitude()*bp[2]/bp[1])
			print "            "+solutionPath(solution)
			timeMethod("checkBoundedPath", start)
			return False
	timeMethod("checkBoundedPath", start)
	return False

def getUpperBoundScore(solution, points, wanted, model):
	start = time()
	score = evaluateSolution(solution, model)
	for c in wanted:
		if not c in solution and len(c.stars) <= points:
			score += c.evaluate(model)
			points -= len(c.stars)
	timeMethod("getUpperBoundScore", start)
	return score

def killSolution(solution):
	start = time()
	# print "Killing solution: " + solutionPath(solution)
	sSol = sorted(solution, key=lambda c: c.evaluate)
	deadNode = deadSolutions
	for sol in sSol:
		if sol == sSol[-1]:
			deadNode[sol.name] = True
			timeMethod("killSolution", start)
			return

		if not sol.name in deadNode.keys():
			deadNode[sol.name] = {}
		deadNode = deadNode[sol.name]		
	timeMethod("killSolution", start)


def isDeadSolution(solution):
	start = time()
	sSol = sorted(solution, key=lambda c: c.evaluate)
	deadNode = deadSolutions
	for sol in sSol:
		if not sol.name in deadNode.keys():
			timeMethod("isDeadSolution", start)
			return False
		if deadNode[sol.name] == True:
			timeMethod("isDeadSolution", start)
			return True
		deadNode = deadNode[sol.name]
	timeMethod("isDeadSolution", start)
	return False

def startsWith(start, complete):
	if len(start) == 0:
		return False
	for i in range(len(start)):
		if start[i] != complete[i]:
			return False
	return True

numCheckedSolutions = 0
def doMove(model, wanted, points, solution=[], remaining=Constellation.constellations, moveStr=""):	
	global bestScore, bestSolutions, checkedSolutions, deadSolutions, numCheckedSolutions
	numCheckedSolutions += 1

	if len(solution) > 0:
		# if startsWith(solution, testSolution):
		# 	print "Solution: ", solutionPath(solution)

		if isDeadSolution(solution):
			# if startsWith(solution, testSolution):
			# 	print "Start of test solution is marked as dead."
			return

		ub = getUpperBoundScore(solution, points, wanted, model)
		if ub < bestScore and evaluateSolution(solution, model) < ub:
			# if startsWith(solution, testSolution):
			# 	print "Start of test solution is marked as low upper bound.", str(ub)

			killSolution(solution)
			return

		if checkBoundedPath(solution, model):
			# if startsWith(solution, testSolution):
			# 	print "Start of test solution is marked as bounded."

			killSolution(solution)
			return
		
	affinities = getAffinities(solution)

	searchConstellations = getNeededConstellations(solution, points, wanted, affinities, remaining)	
	nextMoves = getNextMoves(solution, searchConstellations, affinities, points, model)

	# if startsWith(solution, testSolution):
	# 	print "searchConstellations", solutionPath(searchConstellations)
	# 	print "nextMoves", solutionPath(nextMoves)

	# nextMoves = sortByScore(nextMoves, model)
	# nextMoves = sortByScorePerStar(nextMoves, model)
	nextMoves = sortConstellationsByProvides(nextMoves)
	# nextMoves = sorted(availableConstellations, key=lambda c: c.name, reverse=False)
	# random.shuffle(nextMoves)
	# nextMoves = availableConstellations

	isSolution = True
	for move in nextMoves:
		isSolution = False
		newMoveStr = moveStr + move.id + "("+ str(int(move.evaluate(model))) +")" +" {"+str(nextMoves.index(move)+1)+"/"+str(len(nextMoves))+"}, "

		doMove(model, wanted, points-len(move.stars), solution+[move], searchConstellations, newMoveStr)
	
	killSolution(solution)
	if getSolutionCost(solution) <= 20:
		print "    <-X-  (" + str(getSolutionCost(solution)) + "): " + moveStr[:-2]
		print "      ", numCheckedSolutions, "  ", len(boundedPaths)
		# print "    ", str(methodTimes), sum([methodTimes[key] for key in methodTimes.keys()])
	
	# printSolution(solution, model)
	if isSolution:
		score = evaluateSolution(solution, model)
		if score >= bestScore:
			bestScore = score
			bestSolutions += [(score, solution)]
			print "New best: "
			printSolution(solution, model)
		# printSolution(solution, model)
	# print "checked:", str(numCheckedSolutions), str(methodTimes), sum([methodTimes[key] for key in methodTimes.keys()])
	# if numCheckedSolutions > 5000:
	# 	sys.exit(0)



bestSolutions = []
bestScore = 0
checkedSolutions = {}
deadSolutions = {}

def startSearch(model):
	global bestScore, bestSolutions

	# initialize model
	model.checkModel()

	print "\nEvaluating constellations..."
	constellationRanks = []
	for c in Constellation.constellations:
		constellationRanks += [(c, c.evaluate(nyx))]
		c.buildRedundancies(model)

	constellationRanks.sort(key=itemgetter(1), reverse=True)

	thresh = constellationRanks[len(constellationRanks)/4][1]*.9

	print "\n  Desired constellations:"
	wanted = []
	for c in constellationRanks:
		if c[1] > thresh:
			wanted += [c[0]]
			print "      ", c[0].evaluate(nyx), c[0].name
	print "  Total:", len(wanted)


	# getNeededConstellations(current, points, wanted, affinities=Affinity(0), possibles=Constellation.constellations):
	needed = getNeededConstellations([], 50, wanted)
	print "\nSearch Space: "+str(len(needed))
	# return
	
	bestSolutions = [(evaluateSolution(solution, model), solution) for solution in model.seedSolutions]
	bestSolutions.sort(key=itemgetter(0), reverse=True)

	print "\nEvaluating seed solutions..."
	for solution in bestSolutions:
		printSolution(solution[1], model, "  ")
		if solution[0] >= bestScore:
			bestScore = solution[0]
		for i in range(1, len(solution[1])-1):
			addBoundedPath(solution[1][:i+1], nyx)
	bestSolutions = []

	print "\nExecuting search..."
	doMove(model, wanted, 50)

	print "\n\n\n\n\nBest solutions found:"
	bestSolutions.sort(key=itemgetter(0), reverse=True)
	for solution in bestSolutions:
		printSolution(solution[1], model, "  ")
	for solution in bestSolutions:
		print solutionPath(solution[1], "    ")


startSearch(nyx)

# test = chariot
# print test.evaluate(nyx)
# print test.evaluate(nyx)/len(test.stars)
# for star in test.stars:
# 	print star.evaluate(nyx)


# for c in Constellation.constellations:
# 	if c.requires > Affinity("1a"):
# 		print c.name, c.evaluate(nyx)

# I think the next step is to look at trying to branch and bound.
# I think this is pretty nonlinear so I don't have a real good way of doing that.
#	an expensive way would be to look at each solution's best possible outcome by adding the best scoring constellations to the solution up to the remaining points and if it's not better than my current best don't continue.


# I can kill a solution path if I have already seen a solution fewer points, greater affinities and greater score
# I don't need to evaluate needs every time. Adding a constellation can only remove needs so if I pass them in and trim the ones I no longer need that should save time.
# if i could have activated the next move in the last step then i dont need to evaluate it this step