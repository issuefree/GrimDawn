class Search:
	def startSearch(model, startingSolution=[]):


	globalMetadata["providesValue"] = aVector

	# getNeededConstellations(current, points, wanted, affinities=Affinity(0), possibles=Constellation.constellations):
	needed = getNeededConstellations([], wanted, model)
	print solutionPath(needed)
	print "\nSearch Space: "+str(len(needed))
	# return
	wanted.sort(key=lambda c: c.evaluate(model), reverse=True)
	
	globalMetadata["bestSolutions"] = [(evaluateSolution(solution, model), solution) for solution in model.seedSolutions]
	globalMetadata["bestSolutions"].sort(key=itemgetter(0), reverse=True)

	print "\nEvaluating seed solutions..."
	for constellations in globalMetadata["bestSolutions"]:
		solution = Solution(constellations[1], model)
		print "\t" + str(solution)
		if solution.score >= globalMetadata["bestScore"]:
			globalMetadata["bestScore"] = solution.score
		for i in range(1, len(solution.constellations)):			
			checkBoundedPath(Solution(solution.constellations[:i+1], model))
	globalMetadata["bestSolutions"] = []


	if globalMetadata["boundingRun"]:
		print "\nPerforming a bounding run to depth", globalMetadata["boundingRunDepth"]
		doMove2(model, wanted, model.points, Solution([], model), needed)
		
		globalMetadata["boundingRun"] = False
		# globalMetadata["deadSolutions"] = {}
		print " ", len(globalMetadata["boundedPaths"]), "bounding paths created."

	# if globalMetadata["globalMaxAffinities"].magnitude() == 0:
	# 	globalMetadata["globalMaxAffinities"] = Affinity()
	# 	for c in wanted:
	# 		globalMetadata["globalMaxAffinities"] = globalMetadata["globalMaxAffinities"].maxAffinities(c.requires)

	print "\nExecuting search..."

	# needed = list(set(random.sample(needed, 5) + [xC, xA, xP, xO, xE]))
	# print needed
	doMove2(model, wanted, model.points, Solution([], model), needed)

	print "Evaluated " + str(globalMetadata["numCheckedSolutions"])

	print "\n\n\n\n\nBest solutions found:"
	globalMetadata["bestSolutions"].sort(key=itemgetter(0), reverse=True)
	for solution in globalMetadata["bestSolutions"]:
		printSolution(solution[1], model, "  ")
	for solution in globalMetadata["bestSolutions"]:
		print solutionPath(solution[1], "    ")