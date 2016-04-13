import sys
import random

from constellationData import *
from dataModel import *
from models import *
from utils import *


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
	global globalMaxAffinities
	start = time()
	needed = wanted[:]

	#I'm doing this piece by piece when really I need the total need for my wants. This is probably more efficient.
	#I may also be able to identify needs that can be satified by a single constellation.

	if globalMaxAffinities.magnitude() == 0:
		globalMaxAffinities = Affinity()
		for c in wanted:
			globalMaxAffinities = globalMaxAffinities.maxAffinities(c.requires)

	neededAffinities = globalMaxAffinities - affinities

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


globalMaxAffinities = Affinity()

def addBoundedPath(solution, model):
	global globalMetadata

	if len(solution) > globalMetadata["boundedPathLengthMax"]:
		return False

	affinities = getAffinities(solution).minAffinities(globalMaxAffinities)
	cost = getSolutionCost(solution)
	score = evaluateSolution(solution, model)

	for bpi in range(len(globalMetadata["boundedPaths"])-1, -1, -1):
		bp = globalMetadata["boundedPaths"][bpi]
		if affinities <= bp[0] and cost >= bp[1] and score < bp[2]: 
			return True
		if affinities >= bp[0] and cost <= bp[1] and score > bp[2]:
			del globalMetadata["boundedPaths"][bpi]
		if affinities == bp[0] and cost == bp[1] and score == bp[2]:
			return False

	globalMetadata["boundedPaths"] += [[affinities, cost, score, solution]]
	return False

def checkBoundedPath(solution, model):
	global globalMetadata

	if globalMetadata["boundingRun"] == True:
		return addBoundedPath(solution, model)

	if len(solution) > globalMetadata["boundedPathLengthMax"]:
		return False	

	start = time()

	affinities = getAffinities(solution).minAffinities(globalMaxAffinities)
	cost = getSolutionCost(solution)
	score = evaluateSolution(solution, model)

	for bpi in range(len(globalMetadata["boundedPaths"])-1, -1, -1):
		bp = globalMetadata["boundedPaths"][bpi]
		if affinities <= bp[0] and cost >= bp[1] and score < bp[2]: 
			print "    <-<-  "+str(affinities)+" @ ("+str(cost)+") = "+ str(int(score)) + "  " + solutionPath(solution)
			print "      <<  "+str(bp[0])+" @ ("+str(bp[1])+") = "+ str(int(bp[2])) + "  " + solutionPath(bp[3])

			timeMethod("checkBoundedPath", start)
			return True
		if affinities >= bp[0] and cost <= bp[1] and score > bp[2]: 
			print "    -->>  "+str(affinities)+" @ ("+str(cost)+") = "+ str(int(score))+ "  " + str(int(affinities.magnitude()*score/cost)) + "  " + solutionPath(solution)
			print "      ->  "+str(bp[0])+" @ ("+str(bp[1])+") = "+ str(int(bp[2]))+ "  " + str(int(bp[0].magnitude()*bp[2]/bp[1])) + "  " + solutionPath(bp[3])
			
			globalMetadata["boundedPaths"][bpi] = [affinities, cost, score, solution]

			timeMethod("checkBoundedPath", start)
			return False
		if affinities == bp[0] and cost == bp[1] and score == bp[2]: 
			return False
	if len(solution) <= globalMetadata["boundedPathLengthMax"]:
		print "    -+->  "+str(affinities)+" @ ("+str(cost)+") = "+ str(int(score))+ "  " + str(int(affinities.magnitude()*score/cost)) + "  " + solutionPath(solution)		
		globalMetadata["boundedPaths"] += [[affinities, cost, score, solution]]
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
	deadNode = globalMetadata["deadSolutions"]
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
	deadNode = globalMetadata["deadSolutions"]
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


def doMove(model, wanted, points, solution=[], remaining=Constellation.constellations, moveStr=""):	
	global globalMetadata
	globalMetadata["numCheckedSolutions"] += 1

	if globalMetadata["boundingRun"] == True:
		if len(solution) >= globalMetadata["boundingRunDepth"]:
			return

	if len(solution) > 0:

		if isDeadSolution(solution):
			return

		ub = getUpperBoundScore(solution, points, wanted, model)
		if ub < globalMetadata["bestScore"] and evaluateSolution(solution, model) < ub:
			killSolution(solution)
			return

		if checkBoundedPath(solution, model):
			killSolution(solution)
			return
		
	affinities = getAffinities(solution)

	searchConstellations = getNeededConstellations(solution, points, wanted, affinities, remaining)	
	nextMoves = getNextMoves(solution, searchConstellations, affinities, points, model)

	nextMoves = sortByScore(nextMoves, model)
	# nextMoves = sortByScorePerStar(nextMoves, model)
	# nextMoves = sortConstellationsByProvides(nextMoves)
	# nextMoves = sorted(availableConstellations, key=lambda c: c.name, reverse=False)
	# random.shuffle(nextMoves)
	# nextMoves = availableConstellations

	isSolution = True
	for move in nextMoves:
		isSolution = False
		newMoveStr = moveStr + move.id + "("+ str(int(move.evaluate(model))) +")" +" {"+str(nextMoves.index(move)+1)+"/"+str(len(nextMoves))+"}, "

		doMove(model, wanted, points-len(move.stars), solution+[move], searchConstellations, newMoveStr)
	
	if globalMetadata["boundingRun"]:
		return

	killSolution(solution)
	if getSolutionCost(solution) <= 20:
		print "    <-X-  (" + str(getSolutionCost(solution)) + "): " + moveStr[:-2]
		print "      ", globalMetadata["numCheckedSolutions"], "  ", len(globalMetadata["boundedPaths"])
		# print "    ", str(methodTimes), sum([methodTimes[key] for key in methodTimes.keys()])
	
	if isSolution:
		score = evaluateSolution(solution, model)
		if score >= globalMetadata["bestScore"]:
			globalMetadata["bestScore"] = score
			globalMetadata["bestSolutions"] += [(score, solution)]

			model.seedSolutions += [solution]
			model.saveSeedSolutions()

			print "New best: "
			printSolution(solution, model)


def startSearch(model, startingSolution=[]):
	global globalMetadata

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
	
	globalMetadata["bestSolutions"] = [(evaluateSolution(solution, model), solution) for solution in model.seedSolutions]
	globalMetadata["bestSolutions"].sort(key=itemgetter(0), reverse=True)

	print "\nEvaluating seed solutions..."
	for solution in globalMetadata["bestSolutions"]:
		printSolution(solution[1], model, "  ")
		if solution[0] >= globalMetadata["bestScore"]:
			globalMetadata["bestScore"] = solution[0]
		for i in range(1, len(solution[1])):
			addBoundedPath(solution[1][:i+1], nyx)
		killSolution(solution[1])
	globalMetadata["bestSolutions"] = []


	if globalMetadata["boundingRun"]:
		print "\nPerforming a bounding run to depth", globalMetadata["boundingRunDepth"]
		doMove(model, wanted, globalMetadata["points"])
		globalMetadata["boundingRun"] = False
		globalMetadata["deadSolutions"] = {}
		print " ", len(globalMetadata["boundedPaths"]), "bounding paths created."

	print "\nExecuting search..."

	doMove(model, wanted, globalMetadata["points"], startingSolution)

	print "\n\n\n\n\nBest solutions found:"
	globalMetadata["bestSolutions"].sort(key=itemgetter(0), reverse=True)
	for solution in globalMetadata["bestSolutions"]:
		printSolution(solution[1], model, "  ")
	for solution in globalMetadata["bestSolutions"]:
		print solutionPath(solution[1], "    ")

globalMetadata = {}
globalMetadata["globalMaxAffinities"] = Affinity()

globalMetadata["bestScore"] = 0
globalMetadata["bestSolutions"] = []
globalMetadata["deadSolutions"] = {}
globalMetadata["boundedPaths"] = [[Affinity(),0,0]] #[affinities, cost, score]
globalMetadata["boundedPathLengthMax"] = 6

globalMetadata["boundingRun"] = False
globalMetadata["boundingRunDepth"] = 5

globalMetadata["numCheckedSolutions"] = 0

globalMetadata["points"] = 50


startSearch(nyx)

# I think the next step is to look at trying to branch and bound.
# I think this is pretty nonlinear so I don't have a real good way of doing that.
#	an expensive way would be to look at each solution's best possible outcome by adding the best scoring constellations to the solution up to the remaining points and if it's not better than my current best don't continue.


# I can kill a solution path if I have already seen a solution fewer points, greater affinities and greater score
# I don't need to evaluate needs every time. Adding a constellation can only remove needs so if I pass them in and trim the ones I no longer need that should save time.
# if i could have activated the next move in the last step then i dont need to evaluate it this step
