import sys
import random

from constellationData import *
from dataModel import *
from models import *
from utils import *

def getNextMoves(current, possibles, affinities, points, model):
	start = time()
	moves = []
	# print solutionPath(current)
	# print solutionPath(possibles)

	moves = [c for c in possibles if len(c.stars) <= points and c.canActivate(affinities, current)]

	tempMoves = moves[:]
	for move in tempMoves:
		for other in tempMoves:
			if other in move.redundancies:
				moves.remove(move)
				break

	timeMethod("getNextMoves", start)
	return moves

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

def getProvidersForVector(possibles, neededAffinities, afV, model):
	start = time()

	providesV = []
	for c in possibles:
		if c.provides.isVector(afV) and c.getTier() == 1:
			providesV += [c]
	for c in providesV:
		c.evaluate(model)

	scores = []
	for c in providesV:
		score = 0
		for d in providesV:
			if c.isWorse(d, model):
				score -= 1
			if c.isBetter(d, model):
				score += 1
		scores += [(c, score)]


	scores.sort(key=lambda c: c[1], reverse=True)

	providers = [score[0] for score in scores]

	goodProviders = []
	badProviders = []
	for i in range(len(providers)):
		if i == len(providers)-1:
			goodProviders = providers[:]
			break
		if scores[i][1] == scores[i+1][1]:
			continue
		if getAffinities(providers[:i+1]).get(afV) >= neededAffinities.get(afV)-1:
			goodProviders = providers[:i+1]
			badProviders = providers[i+1:]
			break

	timeMethod("getProvidersForVector", start)
	return (goodProviders, badProviders)

def getNeededConstellations(current, wanted, model, affinities=Affinity(0), remaining=None):
	global globalMetadata
	start = time()

	if globalMetadata["globalMaxAffinities"].magnitude() == 0:
		globalMetadata["globalMaxAffinities"] = Affinity()
		for c in wanted:
			globalMetadata["globalMaxAffinities"] = globalMetadata["globalMaxAffinities"].maxAffinities(c.requires)

	neededAffinities = globalMetadata["globalMaxAffinities"] - affinities

	# possibles should be all tier 0-1 constellations sans the ones we remove.
	if remaining == None:
		possibles = [p for p in Constellation.constellations if p.getTier() <= 1 and not p in wanted]
		for afV in Affinity.sh:
			_, badProviders = getProvidersForVector(possibles, neededAffinities, afV, model)
			for p in badProviders:
				if p in possibles:
					possibles.remove(p)
					print "Discarding weak vector", p.name
	else:
		possibles = remaining[:]

	# print neededAffinities
	for c in possibles[:]:
		if not neededAffinities.intersects(c.provides):
			possibles.remove(c)
			# print "Discarding unnecessary constellation", c.name

	timeMethod("getNeededConstellations", start)
	return possibles

def getWanted(model):
	print "\nEvaluating constellations..."
	constellationRanks = []
	for c in Constellation.constellations:
		constellationRanks += [(c, c.evaluate(model), c.evaluate(model)/len(c.stars))]
		c.buildRedundancies(model)

	constellationRanks.sort(key=itemgetter(1), reverse=True)
	thresh = constellationRanks[len(constellationRanks)/6][1] * .9

	print "\n  Desired constellations (value > %s):"%thresh
	wanted = []
	cv = constellationRanks[0][1]
	for c in constellationRanks:
		if c[1] > thresh:
			wanted += [c[0]]
			print "      ", int(c[1]), c[0].name
		else:
			print "       - ", int(c[1]), c[0].name

	constellationRanks.sort(key=itemgetter(2), reverse=True)
	thresh = constellationRanks[len(constellationRanks)/6][2] * .9

	print "\n  Desired constellations (efficiency > %s):"%thresh
	wanted = []
	for c in constellationRanks:
		if c[2] > thresh and not c[0] in wanted:
			wanted += [c[0]]
			print "      ", int(c[2]), c[0].name
		else:
			print "       - ", int(c[2]), c[0].name

	print "  Total:", len(wanted)

	wanted.sort(key=lambda c: c.evaluate(model), reverse=True)
	return wanted


def addBoundedPath(solution, model):
	global globalMetadata

	if len(solution) > globalMetadata["boundedPathLengthMax"]:
		return False

	affinities = getAffinities(solution).minAffinities(globalMetadata["globalMaxAffinities"])
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

	if len(solution) > globalMetadata["boundedPathLengthMax"]:
		return False	

	start = time()

	affinities = getAffinities(solution).minAffinities(globalMetadata["globalMaxAffinities"])
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
		if len(c.stars) <= points:
			score += c.evaluate(model)
			points -= len(c.stars)
	timeMethod("getUpperBoundScore", start)
	return score

def sortDeadSolution(solution, model):
	return sorted(solution, key=lambda c: c.evaluate(model), reverse=True)

def killSolution(solution, model):
	global globalMetadata
	start = time()
	# print "Killing solution: " + solutionPath(solution)
	sSol = sortDeadSolution(solution, model)
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


def isDeadSolution(solution, model):
	start = time()
	sSol = sortDeadSolution(solution, model)
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




def doMove(model, wanted, points, solution=[], affinities=Affinity(), remaining=None, moveStr=""):	
	global globalMetadata
	globalMetadata["numCheckedSolutions"] += 1

	# if globalMetadata["boundingRun"] == True:
	# 	if len(solution) >= globalMetadata["boundingRunDepth"]:
	# 		return

	if len(solution) > 0:

		if isDeadSolution(solution, model):
			return

		ub = getUpperBoundScore(solution, points, wanted, model)
		if ub < globalMetadata["bestScore"] and evaluateSolution(solution, model) < ub:
			killSolution(solution, model)
			return

		# if checkBoundedPath(solution, model):
		# 	killSolution(solution, model)
		# 	return
		
	# if not remaining:
	remaining = getNeededConstellations(solution, wanted, model, affinities, remaining)
	possibleMoves = wanted + remaining
	# print len(possibleMoves)
	nextMoves = getNextMoves(solution, possibleMoves, affinities, points, model)

	# if len(solution) > 0:
	# 	lastMove = solution[-1]
	# 	if lastMove.provides.magnitude() == 0:
	# 		neededAffinities = globalMetadata["globalMaxAffinities"] - affinities
	# 		for move in nextMoves[:]:
	# 			provides = move.provides.minAffinities(neededAffinities)
	# 			if provides.magnitude() > 0:
	# 				nextMoves.remove(move)

	# nextMoves = sortByLeastProvides(nextMoves, model)
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

		try:
			remaining.remove(move)
		except:
			pass

		newWanted = wanted[:]
		try:
			newWanted.remove(move)
		except:
			pass
		doMove(model, newWanted, points-len(move.stars), solution+[move], affinities+move.provides, remaining, newMoveStr)
	
	# if globalMetadata["boundingRun"]:
	# 	return

	# killSolution(solution, model)
	if len(solution) <= globalMetadata["points"]/9:
		print "    <-X-  (" + str(getSolutionCost(solution)) + "): " + moveStr[:-2]
		print "      ", globalMetadata["numCheckedSolutions"]#, "  ", len(globalMetadata["boundedPaths"])
		# print "    ", str(methodTimes), sum([methodTimes[key] for key in methodTimes.keys()])
	
	# if globalMetadata["numCheckedSolutions"] > 20000:
	# 	print (time() - globalMetadata["startTime"]), "seconds"
	# 	print "    ", str(methodTimes), sum([methodTimes[key] for key in methodTimes.keys()])
	# 	sys.exit(0)

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

	globalMetadata["points"] -= getSolutionCost(startingSolution)

	model.initialize()

	wanted = getWanted(model)

	# getNeededConstellations(current, points, wanted, affinities=Affinity(0), possibles=Constellation.constellations):
	needed = getNeededConstellations([], wanted, model)
	print solutionPath(needed)
	print "\nSearch Space: "+str(len(needed))
	# return
	wanted.sort(key=lambda c: c.evaluate(model), reverse=True)
	
	globalMetadata["bestSolutions"] = [(evaluateSolution(solution, model), solution) for solution in model.seedSolutions]
	globalMetadata["bestSolutions"].sort(key=itemgetter(0), reverse=True)

	print "\nEvaluating seed solutions..."
	for solution in globalMetadata["bestSolutions"]:
		printSolution(solution[1], model, "  ")
		if solution[0] >= globalMetadata["bestScore"]:
			globalMetadata["bestScore"] = solution[0]
		# for i in range(1, len(solution[1])):
		# 	addBoundedPath(solution[1][:i+1], model)
		# killSolution(solution[1], model)
	globalMetadata["bestSolutions"] = []


	# if globalMetadata["boundingRun"]:
	# 	print "\nPerforming a bounding run to depth", globalMetadata["boundingRunDepth"]
	# 	doMove(model, wanted, globalMetadata["points"])
	# 	globalMetadata["boundingRun"] = False
	# 	globalMetadata["deadSolutions"] = {}
	# 	print " ", len(globalMetadata["boundedPaths"]), "bounding paths created."

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
# globalMetadata["boundedPaths"] = [[Affinity(),0,0]] #[affinities, cost, score]
# globalMetadata["boundedPathLengthMax"] = 6

# globalMetadata["boundingRun"] = False
# globalMetadata["boundingRunDepth"] = 4

globalMetadata["numCheckedSolutions"] = 0

globalMetadata["points"] = 50

globalMetadata["startTime"] = time()
startSearch(armitage)

# I think the next step is to look at trying to branch and bound.
# I think this is pretty nonlinear so I don't have a real good way of doing that.
#	an expensive way would be to look at each solution's best possible outcome by adding the best scoring constellations to the solution up to the remaining points and if it's not better than my current best don't continue.

# too expensive to evaluate
	# I can kill a solution path if I have already seen a solution fewer points, greater affinities and greater score
	# I don't need to evaluate needs every time. Adding a constellation can only remove needs so if I pass them in and trim the ones I no longer need that should save time.

# I can probably eliminate constellations from the initial search space by looking at the total needed affinity. With unneeded constellations I jsut need to satisfy the need I don't need all possible ways of satisfying the need. 
#if I need 5 and 
#	a provides 2
#	b provides 4 
#	c provides 5
# if a + b is cheaper and higher scoring than c then c is useless.
# if c is cheaper and higher scoring than a + b then they are useless.