import os
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

def scoreAgainst(model, constellations, enemies):
	"""Score a finished solution against a stated number of enemies.

	Restores the model afterwards, and resets every constellation on the way in
	and out, because a constellation caches what it scored and the whole point
	here is that it scores differently.
	"""
	was = model.stats.get("enemies")
	if enemies is None:
		model.stats.pop("enemies", None)
	else:
		model.stats["enemies"] = enemies
	for c in Constellation.constellations:
		c.reset()
	total = evaluateSolution(constellations, model)
	each = [(c.name, c.evaluate(model)) for c in constellations]
	if was is None:
		model.stats.pop("enemies", None)
	else:
		model.stats["enemies"] = was
	for c in Constellation.constellations:
		c.reset()
	return total, each


def showBothFights(model, constellations):
	"""The same build against one enemy, and against what the model fights.

	These are two different fights and one number cannot hold both. The hardest
	fight in the game is a single enemy; the commonest is a room of them. A
	build tuned on an average of the two is tuned for a fight that never
	happens, and the average also hides which way a solution leans - a devotion
	that only pays off across a pack reads exactly like one that always pays.

	So both are shown rather than blended. The right column is what the solver
	optimised, from the model's own enemy density; the left is the same build
	with only one thing to hit. The ratio between them is how much of a pick is
	clear speed, and a pick at 1.0 is one a boss cannot take away from you.
	"""
	one, eachOne = scoreAgainst(model, constellations, 1)
	many, eachMany = scoreAgainst(model, constellations, None)
	if abs(one - many) < 1e-6:
		return          # nothing in this solution cares how many there are

	print("\n  Against one enemy, and against a pack:")
	print("     %-38s %8s %8s %8s" % ("", "boss", "pack", "x"))
	for (name, a), (_, b) in zip(eachOne, eachMany):
		print("     %-38s %8d %8d %7.1f" % (name, a, b, (b / a) if a else 0))
	print("     %-38s %8d %8d %7.1f" % ("TOTAL", one, many, (many / one) if one else 0))


def showSolution(model, constellations, bonusCount=18):
	"""Break a finished solution down: what it costs, what it buys, why.

	Three questions the bare list of names never answered. What is each
	constellation actually worth here, and is it paying for its stars. What
	stats the whole thing adds up to, biggest first, since that is what gets
	compared against a character sheet. And which procs are in it, with how
	much of a fight each is up for - a proc that fires once a minute reads the
	same as one that never stops until you look.

	Returns the constellations in the order it printed them, which is not the
	order it was given: see orderSolution.
	"""
	# The set is the solver's answer; the order is a separate question, and the
	# one that matters while levelling. "total" is what the whole thing is worth
	# once this line is bought, so a 20 point plan can be read as a 10 point one.
	constellations = orderSolution(constellations, model)

	print("\n  Take in this order:")
	print("     %-38s %5s %6s %6s %5s %7s  %-11s %s"
		  % ("", "stars", "score", "/star", "spent", "total", "requires", "provides"))
	spent = 0
	for i, c in enumerate(constellations):
		spent += len(c.stars)
		score = c.evaluate(model)
		print("     %-38s %5d %6d %6d %5d %7d  %-11s %s"
			  % (c.name, len(c.stars), score, score / len(c.stars), spent,
				 evaluateSolution(constellations[:i + 1], model),
				 c.requires.short(), c.provides.short()))

	showBothFights(model, constellations)

	bonuses = getBonuses(constellations, model)
	ranked = sorted(((evaluateBonuses(model, {name: value}), name, value)
					 for name, value in bonuses.items()),
					reverse=True, key=lambda row: row[0])
	shown = [row for row in ranked if row[0] > 0][:bonusCount]
	if shown:
		print("\n  What it buys:")
		for worth, name, value in shown:
			if isinstance(value, list):
				value = "%g over %gs" % (value[0], value[1])
			else:
				value = "%g" % value
			print("     %-30s %12s %8d" % (name, value, worth))
		rest = sum(row[0] for row in ranked[len(shown):] if row[0] > 0)
		if rest:
			print("     %-30s %12s %8d" % ("... everything else", "", rest))

	procs = [(c, star.ability) for c in constellations for star in c.stars if star.ability]
	if procs:
		print("\n  Procs:")
		for c, ability in procs:
			print("     %-30s %-22s %s"
				  % (c.name[:30], ability.name[:22], ability.describe()))

	# the caller prints the path, and it should read in the order just shown
	return constellations


def showAugments(model, count=3):
	"""The best augments this character could put in each slot.

	Augments are picked slot by slot rather than solved for: unlike devotions
	they cost nothing but faction standing and one does not rule out another, so
	the best in each slot is simply the best in each slot.
	"""
	from itemData import augments

	print("\n  Best augments per slot:")
	for location in sorted({slot for item in augments for slot in item.location}):
		ranked = sorted(((item.evaluate(model, location), item)
						 for item in Item.getByLocation(location, augments)),
						key=itemgetter(0), reverse=True)
		best = [(value, item) for value, item in ranked[:count] if value > 0]
		print("    %-9s %s" % (location,
							   "   ".join("%s (%d)" % (item.name, value) for value, item in best)
							   or "- nothing this character scores"))


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

	constellations = showSolution(model, constellations)

	print("\n  " + solutionPath(constellations))

	# keep it as a seed so the exhaustive search can start from here
	# (loadModel already read any existing seeds, so this adds rather than replaces)
	model.addSolution(Solution(constellations, model))
	model.saveSeedSolutions()
	print("\n  saved to %s/solutions.py" % model.name.lower())

	# augments are not part of the answer to "which devotions" and were twenty
	# lines of unrelated table on the end of every search. Ask for them:
	#     bestAugments()   in the sandbox


def main(argv=None, modelName=None):
	"""The command line, as a function so a model file can be its own entry point.

	usage: python devotion.py [modelName] [--budget S] [--seeds N] [--exhaustive]
	  e.g. python devotion.py armitage

	constellationData.py is generated from the installed game; rebuild it after
	a patch with --regenerate.

	The heuristic solver is the default: it returns in seconds and matches the
	exhaustive search on every model where that search terminates. --exhaustive
	runs the old branch-and-bound, which does not terminate on large models.

	modelName overrides whatever the arguments name, so a model file can pass
	its own and still take every flag from the command line.
	"""
	argv = list(sys.argv[1:] if argv is None else argv)
	exhaustive = "--exhaustive" in argv
	regenerate = "--regenerate" in argv
	compare = []
	if "--compare" in argv:
		# everything after --compare is an item name, so the model has to be
		# named before it: python devotion.py armitage --compare "a" "b"
		index = argv.index("--compare")
		compare = [a for a in argv[index + 1:] if not a.startswith("-")]
		del argv[index:]
	if "--fast" in argv:
		argv.remove("--fast") # now the default; accepted so old invocations still work
	budget = 1.0
	seeds = 5
	newModel = None
	archetype = "physical"
	for flag, cast in (("--new", str), ("--archetype", str), ("--budget", float), ("--seeds", int)):
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
			elif flag == "--seeds":
				seeds = value
			elif flag == "--new":
				newModel = value
			else:
				archetype = value
			del argv[i:i + 2]
	names = [a for a in argv if not a.startswith("-")]
	if modelName is None:
		modelName = names[0] if names else DEFAULT_MODEL

	if regenerate:
		import devotiongen, itemgen, skillgen
		try:
			count, procs = devotiongen.generate()
			items = itemgen.generate()
			masteries, skills, orphans = skillgen.generate()
		except FileNotFoundError as e:
			sys.exit("Could not read the Grim Dawn database: %s. Set GRIM_DAWN_DIR if the game is installed elsewhere." % e)
		print("Wrote constellationData.py: %d constellations, %d procs" % (count, procs))
		print("Wrote itemData.py: %d components, %d augments, %d named pieces"
			  % (items["components"], items["augments"], items["equipment"]))
		print("Wrote skillData.py: %d skills across %d masteries" % (skills, masteries))
		if orphans:
			print("  modifiers whose record name does not say what they modify, so they "
				  "cannot be attached to a skill:")
			for mastery, name, stem in orphans:
				print("    %-13s %-24s (%s)" % (mastery, name, stem))
		if items["missing"]:
			print("  not found in the game files, check the spelling in equipmentWanted.py:")
			for name in items["missing"]:
				print("    " + name)
	elif newModel:
		import modelspec
		try:
			path = modelspec.scaffold(newModel, archetype)
		except ValueError as e:
			sys.exit(str(e))
		print("Created %s (archetype: %s)" % (path, archetype))
		print("  Fill in your character sheet, then run:  python %s" % path)
		print("  Archetypes available: %s" % ", ".join(sorted(modelspec.ARCHETYPES)))
	else:
		# a broken model file is a user error, not a crash - report it plainly
		try:
			model = Model.loadModel(modelName)
		except (ValueError, FileNotFoundError) as e:
			sys.exit(str(e))
		if compare:
			import gearcompare
			gearcompare.compare(model, compare)
		elif exhaustive:
			startSearch(model)
		else:
			fastSearch(model, budget, seeds)


def runModelFile(path):
	"""Search for the devotions of the model file being run directly.

	A model file is data, and loadModel reads it by exec'ing it, so it cannot
	simply call the search at the bottom - it would fire again on every load.
	Instead each file guards on __name__ and hands its own path here, which
	names the model after the file and runs from the repo root, because
	loadModel and saveSeedSolutions both address models by relative path.
	"""
	folder = os.path.dirname(os.path.abspath(path))
	os.chdir(os.path.dirname(folder))
	return main(modelName=os.path.splitext(os.path.basename(path))[0])


if __name__ == "__main__":
	main()


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