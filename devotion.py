import sys

from constellationData import *
from dataModel import *
from models import *
from utils import *
from solution import *

def getNextMoves(current, possibles, points, model):
	start = time()

	moves = [c for c in possibles if len(c.stars) <= points and c.canActivate(current.provides, current.constellations) and c not in current.constellations]
	# redundantMoves = []

	tempMoves = moves[:]
	for move in tempMoves:
		for other in moves:
			if other in move.redundancies:
				moves.remove(move)
				# redundantMoves.append(move)
				break

	timeMethod("getNextMoves", start)
	return moves#, redundantMoves

def getRemainingLinks(wanted, neededAffinities, remainingLinks):
	start = time()

	links = []
	for c in remainingLinks:
		if neededAffinities.intersects(c.provides):
			links.append(c)

	timeMethod("getRemainingLinks", start)

	return links


def getNeededConstellations(current, wanted, model, affinities=Affinity(0), remaining=None):
	start = time()

	neededAffinities = Solution.maxAffinities - affinities

	# possibles should be all tier 0-1 constellations sans the ones we remove.
	if remaining == None:
		possibles = [p for p in Constellation.constellations if p.getTier() <= 1 and not p in wanted]
	else:
		possibles = remaining[:]

	# print(neededAffinities)
	for c in possibles[:]:
		if not neededAffinities.intersects(c.provides):
			possibles.remove(c)
			# print("Discarding unnecessary constellation", c.name)

	timeMethod("getNeededConstellations", start)
	return possibles

def getWanted(model):
	print("\nEvaluating constellations...")
	constellationRanks = []
	for c in Constellation.constellations:
		print(c)
		constellationRanks += [(c, c.evaluate(model), c.evaluate(model)/len(c.stars))]
		c.buildRedundancies(model)

	constellationRanks.sort(key=itemgetter(1), reverse=True)
	thresh = constellationRanks[len(constellationRanks)//6][1] * .5

	print("\n  Desired constellations (value > %s):"%thresh)
	wanted = []
	for c in constellationRanks:
		if c[1] > thresh:
			wanted += [c[0]]
			print("         ", str(int(c[1])).rjust(7), c[0].name.ljust(45), c[0].requires)
		else:
			print("       - ", str(int(c[1])).rjust(7), c[0].name.ljust(45), c[0].requires)

	constellationRanks.sort(key=itemgetter(2), reverse=True)
	thresh = constellationRanks[len(constellationRanks)//6][2] * .5

	print("\n  Desired constellations (efficiency > %s):"%thresh)
	for c in constellationRanks:
		if c[2] > thresh and not c[0] in wanted:
			wanted += [c[0]]
			print("      ", int(c[2]), c[0].name)
		else:
			print("       - ", int(c[2]), c[0].name)

	globalMetadata["bestScorePerStar"] = constellationRanks[0][2]
	print("  Best score per star:", globalMetadata["bestScorePerStar"])

	print("  Total:", len(wanted))

	wanted.sort(key=lambda c: c.evaluate(model), reverse=True)
	return wanted


def checkBoundedPath(solution):
	maxLen = globalMetadata["boundedPathLengthMax"]
	if len(solution.constellations) > maxLen:
		return False

	start = time()

	boundedPaths = globalMetadata["boundedPaths"]
	# Duplicates can only be introduced by the overwrite below: appending `solution`
	# is only reachable when no entry equalled it (equality implies >=, which
	# overwrites instead). So the dedupe is a no-op unless we actually overwrote,
	# and running it unconditionally was rehashing the whole list on every call.
	overwrote = False

	for bpi in range(len(boundedPaths)-1, -1, -1):
		bp = boundedPaths[bpi]
		if solution <= bp and not solution == bp:
			timeMethod("checkBoundedPath", start)
			return True
		elif solution >= bp:
			boundedPaths[bpi] = solution
			overwrote = True

	boundedPaths.append(solution)
	if overwrote:
		globalMetadata["boundedPaths"] = list(set(boundedPaths))

	timeMethod("checkBoundedPath", start)
	return False

def getUpperBoundScore(solutionScore, points):
	start = time()
	solutionScore += points * globalMetadata["bestScorePerStar"]
	timeMethod("getUpperBoundScore", start)
	return solutionScore

def doMove(model, wanted, points, solution, remainingLinks, moveStr=""):
	if globalMetadata["boundingRun"] == True:
		if len(solution.constellations) >= globalMetadata["boundingRunDepth"]:
			return

	globalMetadata["numCheckedSolutions"] += 1

	if solution.isDead: # should never hit this check but...
		return

	ub = getUpperBoundScore(solution.score, points)
	if ub < globalMetadata["bestScore"] and solution.score < ub:
		# print(ub, "<", globalMetadata["bestScore"])
		# print(points, "points left before trim")
		solution.kill()
		return

	if checkBoundedPath(solution):
		# print("Killing bounded solution:", solution)
		solution.kill()
		return

	neededAffinities = Solution.maxAffinities - solution.provides

	remainingLinks = getRemainingLinks(wanted, neededAffinities, remainingLinks)
	possibleMoves = wanted + remainingLinks

	nextMoves = getNextMoves(solution, possibleMoves, points, model)
	# nextMoves, redundantMoves = getNextMoves(solution, possibleMoves, affinities, points, model)
	nextMoves = sortByScore(nextMoves, model)
	# nextMoves = sortConstellationsByProvidesValueScore(nextMoves, model)
	# random.shuffle(nextMoves)

	isSolution = True
	newWanted = wanted[:]
	links = remainingLinks[:]

	numMoves = len(nextMoves)
	for moveNum, move in enumerate(nextMoves, 1):
		isSolution = False
		# enumerate rather than nextMoves.index(move), which rescanned the list
		newMoveStr = moveStr + move.id + "("+ str(int(move.evaluate(model))) +")" +" {"+str(moveNum)+"/"+str(numMoves)+"}, "

		try:
			links.remove(move)
		except:
			pass

		try:
			newWanted.remove(move)
		except:
			pass

		nextSolution = Solution(solution.constellations+[move], model)
		if not nextSolution.isDead:
			doMove(model, newWanted, points-len(move.stars), nextSolution, links, newMoveStr)

	if globalMetadata["boundingRun"]:
		return

	solution.kill()
	if len(solution.constellations) <= model.points/8.0:
		print("    <-X-  (" + str(solution.cost) + "): " + moveStr[:-2])
		print("      ", globalMetadata["numCheckedSolutions"])#, "  ", len(globalMetadata["boundedPaths"]))
		# print("    ", str(methodTimes), sum([methodTimes[key] for key in methodTimes]))

	if isSolution:
		if solution.score >= globalMetadata["bestScore"]:
			globalMetadata["bestScore"] = solution.score
			globalMetadata["bestSolutions"] += [(solution.score, solution.constellations)]

			model.seedSolutions += [solution]
			model.saveSeedSolutions()

			print("New best: ")
			print(solution)

def startSearch(model, startingSolution=[]):
	model.points -= getSolutionCost(startingSolution)

	model.initialize()

	Solution.resetDeadSolutions()

	wanted = getWanted(model)

	Solution.maxAffinities = Affinity()
	for c in wanted:
		Solution.maxAffinities = Solution.maxAffinities.maxAffinities(c.requires)
	print(Solution.maxAffinities)

	aVector = Affinity()
	for c in Constellation.constellations:
		# print(c.evaluate(model))
		score = c.evaluate(model)
		aVector += c.requires*score
	aVector = aVector/aVector.magnitude()

	globalMetadata["providesValue"] = aVector

	out = "Affinity value: "
	for i in range(len(aVector.affinities)):
		out += "%0.2f"%aVector.affinities[i] + Affinity.sh[i] + " "
	print(out)


	# getNeededConstellations(current, points, wanted, affinities=Affinity(0), possibles=Constellation.constellations):
	needed = getNeededConstellations([], wanted, model)
	print(solutionPath(needed))
	print("\nSearch Space: "+str(len(needed)))
	# return
	wanted.sort(key=lambda c: c.evaluate(model), reverse=True)
	
	globalMetadata["bestSolutions"] = [(evaluateSolution(solution.constellations, model), solution) for solution in model.seedSolutions]
	globalMetadata["bestSolutions"].sort(key=itemgetter(0), reverse=True)

	print("\nEvaluating seed solutions...")
	for score, solution in globalMetadata["bestSolutions"]:
		print("\t" + str(solution))
		if solution.score >= globalMetadata["bestScore"]:
			globalMetadata["bestScore"] = solution.score
		for i in range(1, len(solution.constellations)):			
			checkBoundedPath(Solution(solution.constellations[:i+1], model))
	globalMetadata["bestSolutions"] = []


	if globalMetadata["boundingRun"]:
		print("\nPerforming a bounding run to depth", globalMetadata["boundingRunDepth"])
		doMove(model, wanted, model.points, Solution([], model), needed)
		
		globalMetadata["boundingRun"] = False
		# globalMetadata["deadSolutions"] = {}
		print(" ", len(globalMetadata["boundedPaths"]), "bounding paths created.")

	# if globalMetadata["globalMaxAffinities"].magnitude() == 0:
	# 	globalMetadata["globalMaxAffinities"] = Affinity()
	# 	for c in wanted:
	# 		globalMetadata["globalMaxAffinities"] = globalMetadata["globalMaxAffinities"].maxAffinities(c.requires)

	print("\nExecuting search...")

	# needed = list(set(random.sample(needed, 5) + [xC, xA, xP, xO, xE]))
	# print(needed)
	doMove(model, wanted, model.points, Solution([], model), needed)

	print("Evaluated " + str(globalMetadata["numCheckedSolutions"]))

	print("\n\n\n\n\nBest solutions found:")
	globalMetadata["bestSolutions"].sort(key=itemgetter(0), reverse=True)
	for solution in globalMetadata["bestSolutions"]:
		printSolution(solution[1], model, "  ")
	for solution in globalMetadata["bestSolutions"]:
		print(solutionPath(solution[1], "    "))

globalMetadata = {}
globalMetadata["globalMaxAffinities"] = Affinity()
globalMetadata["bestScorePerStar"] = 0
globalMetadata["providesValue"] = Affinity()

globalMetadata["bestScore"] = 0
globalMetadata["bestSolutions"] = []
globalMetadata["deadSolutions"] = {}
globalMetadata["boundedPaths"] = []
globalMetadata["boundedPathLengthMax"] = 7

globalMetadata["boundingRun"] = False
globalMetadata["boundingRunDepth"] = 5

globalMetadata["numCheckedSolutions"] = 0

globalMetadata["startTime"] = time()

DEFAULT_MODEL = "morena"

def fastSearch(model, budget, seeds):
	from fastsolve import solveModel

	print("\nFast solve: %s   (%d points, %.1fs x %d seeds)" % (model.name, model.points, budget, seeds))
	start = time()
	prob, constellations, score, restarts = solveModel(model, budget, seeds)
	elapsed = time() - start

	# re-verify through the real scorer rather than trusting the solver's own arithmetic
	verified = evaluateSolution(constellations, model)
	cost = getSolutionCost(constellations)

	print("\n  score      : %.0f   (verified %.0f via evaluateSolution)" % (score, verified))
	print("  cost       : %d / %d stars" % (cost, model.points))
	print("  restarts   : %d in %.2fs" % (restarts, elapsed))
	if abs(score - verified) > 1e-6:
		print("  WARNING: solver score disagrees with evaluateSolution - treat with suspicion")
	if not prob.feasible([prob.cons.index(c) for c in constellations]):
		print("  WARNING: solution is not feasible")

	print("\n  Take in this order:")
	for c in constellations:
		print("     %-38s %d stars  %s" % (c.name, len(c.stars), c.requires))

	print("\n  " + solutionPath(constellations))

	# keep it as a seed so the exhaustive search can start from here
	# (loadModel already read any existing seeds, so this adds rather than replaces)
	model.addSolution(Solution(constellations, model))
	model.saveSeedSolutions()
	print("\n  saved to %s/solutions.py" % model.name.lower())

if __name__ == "__main__":
	# usage: python devotion.py [modelName] [--budget S] [--seeds N] [--exhaustive]
	#   e.g. python devotion.py armitage
	#
	# The heuristic solver is the default: it returns in seconds and matches the
	# exhaustive search on every model where that search terminates. --exhaustive
	# runs the old branch-and-bound, which does not terminate on large models.
	argv = sys.argv[1:]
	exhaustive = "--exhaustive" in argv
	if "--fast" in argv:
		argv.remove("--fast") # now the default; accepted so old invocations still work
	budget = 1.0
	seeds = 5
	for flag, cast in (("--budget", float), ("--seeds", int)):
		if flag in argv:
			i = argv.index(flag)
			if i + 1 >= len(argv):
				sys.exit("%s needs a value" % flag)
			try:
				value = cast(argv[i + 1])
			except ValueError:
				sys.exit("%s needs a %s" % (flag, cast.__name__))
			if flag == "--budget":
				budget = value
			else:
				seeds = value
			del argv[i:i + 2]
	names = [a for a in argv if not a.startswith("-")]
	modelName = names[0] if names else DEFAULT_MODEL

	if exhaustive:
		startSearch(Model.loadModel(modelName))
	else:
		fastSearch(Model.loadModel(modelName), budget, seeds)


# I think the next step is to look at trying to branch and bound.
# I think this is pretty nonlinear so I don't have a real good way of doing that.
#	an expensive way would be to look at each solution's best possible outcome by adding the best scoring constellations to the solution up to the remaining points and if it's not better than my current best don't continue.

# too expensive to evaluate
	# I can kill a solutiond path if I have already seen a solution fewer points, greater affinities and greater score
	# I don't need to evaluate needs every time. Adding a constellation can only remove needs so if I pass them in and trim the ones I no longer need that should save time.

# I can probably eliminate constellations from the initial search space by looking at the total needed affinity. With unneeded constellations I jsut need to satisfy the need I don't need all possible ways of satisfying the need. 
#if I need 5 and 
#	a provides 2
#	b provides 4 
#	c provides 5
# if a + b is cheaper and higher scoring than c then c is udseless.
# if c is cheaper and higher scoring than a + b then they are useless.