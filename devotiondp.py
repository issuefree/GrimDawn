from constellationData import *
from dataModel import *
from models import *
from utils import *
from solution import *
from devotion import getWanted
from devotion import getNeededConstellations

import itertools
import string

def getUpperBound(sol, totalPoints):
	global globalMetadata

	return sol.score + (totalPoints - sol.cost)*globalMetadata["bestScorePerStar"]



model = Model.loadModel("Armitage")
model.initialize()


wanted = getWanted(model)
# wanted = [tree, sage]

maxAffinities = Affinity()
for c in wanted:
	maxAffinities = maxAffinities.maxAffinities(c.requires)

print "Maximum needed affinities:",maxAffinities
Solution.maxAffinities = maxAffinities

links = getNeededConstellations(Solution([], model), wanted, model)

searchSpace = sorted(wanted+links, key=lambda c: c.evaluate(model), reverse=True)

print solutionPath(links+wanted)
print "\nSearch Space: "+str(len(links+wanted))

longestConstellation = 0
for c in searchSpace:
	if len(c.stars) > longestConstellation:
		longestConstellation = len(c.stars)
longestConstellation += 1

aVector = Affinity()
for c in Constellation.constellations:
	# print c.evaluate(model)
	score = c.evaluate(model)
	aVector += c.requires*score
aVector = aVector/aVector.magnitude()

print aVector

afs = ["1a", "1e", "1c", "1o", "1p"]

vectors = []

for i in range(5):
	vectors += [Affinity(string.join(list(a), " ")) for a in list(itertools.combinations(afs, i+1))]

#solutions organized by point cost
# optimalSolutions = [[], [Solution([], model)]]
optimalSolutions = [[Solution([], model)]]
# optimalSolutions.append([Solution([xA], model), Solution([xC], model), Solution([xE], model), Solution([xO], model), Solution([xP], model)])

totalPoints = model.points

# affinities = [Affinity("1a")*aVector, Affinity("1c")*aVector, Affinity("1e")*aVector, Affinity("1o")*aVector, Affinity("1p")*aVector]
# affinities = sorted(affinities, key=lambda a: a.magnitude(), reverse=True)
# for affinity in affinities:
# print affinity
points = 0
while points < totalPoints:
	numProvidedCaps = 0
	numLinksSkipped = 0
	numOverwrites = 0
	numSkipped = 0
	numCappedSolutionsSkipped = 0

	points += 1

	if points > longestConstellation:
		optimalSolutions[points - longestConstellation] = []

	print "Evaluating:", points
	start = time()
	if len(optimalSolutions) <= points:
		optimalSolutions.append([])

	for c in searchSpace:
		# if c.requires.magnitude() == 0:
		# 	if not c.provides.intersects(affinity):
		# 		continue
		# elif not c.requires.intersects(affinity):
		# 	continue

		cost = len(c.stars)
		if cost > points:  # no need to look at these since they're bigger than we can match
			continue

		isLink = c in links

		testSolutions = optimalSolutions[points - cost]
		for testSolution in testSolutions:
			skip = False
			if testSolution.provides >= maxAffinities and isLink:
				numLinksSkipped += 1
				continue

			if isLink:
				if c.provides < testSolution.cappingAffinity:
					numCappedSolutionsSkipped += 1
					continue

			if c.canActivate(testSolution.provides, testSolution.constellations) and not c in testSolution.constellations:
				newSolution = Solution(testSolution.constellations + [c], model)

				for i in range(len(optimalSolutions[points])):
					if newSolution <= optimalSolutions[points][i]:
						skip = True
						numSkipped += 1
						break
					elif newSolution >= optimalSolutions[points][i]:
						skip = True
						optimalSolutions[points][i] = newSolution
						numOverwrites += 1

				if not skip:
					optimalSolutions[points].append(newSolution)

		optimalSolutions[points] = list(set(optimalSolutions[points]))

	print "  Found:", len(optimalSolutions[points]), "in", str(int(time() - start))
	print "    ...skipped:", numSkipped
	print "    ...provided capped:", numProvidedCaps
	print "    ...links skipped:", numLinksSkipped
	print "    ...overwrites:", numOverwrites
	print "    ...cap skips:", numCappedSolutionsSkipped

	# here we are going to try cleaning up all but the best vectors
	bests = []
	for v in vectors:
		best = Solution([], model)
		bv = best.provides * v
		for solution in optimalSolutions[points]:
			if solution.provides >= v:
				vs = solution.provides * v
				if vs.magnitude() > bv.magnitude() or (vs.magnitude() == bv.magnitude() and solution.score > best.score):
					best = solution
					bv = best.provides * v
		bests += [best]		

	# for b in bests:
	# 	print b

	optimalSolutions[points] = list(set(bests))

	optimalSolutions[points] = sorted(optimalSolutions[points], key=lambda s: s.score, reverse=True)
	for i in range(min(3, len(optimalSolutions[points]))):
		print optimalSolutions[points][i]

print
print

for i in range(len(optimalSolutions)):
	print i
	for sol in optimalSolutions[i]:
		print "  " + str(sol)
