from constellationData import *
from dataModel import *
from models import *
from utils import *
from solution import *
from search import *
import random

def breed(a, b):
	links = [c for c in a.getLinks() if c in b.getLinks()]
	other = [c for c in a.getLinks() + b.getLinks() if c not in links]
	links += random.sample(other, len(other)/2)
	return Search(links)
	# return Search(a.getLinks() + b.getLinks())

model = Model.loadModel("Lilith")

best = getBestConstellations(model)
highest, _ = getHighestScoring(best)
efficient, Search.bestScorePerStar = getMostEfficient(best)

wanted = list(set(highest + efficient))

Solution.maxAffinities = Affinity()
for c in wanted:
	Solution.maxAffinities = Solution.maxAffinities.maxAffinities(c.requires)
print Solution.maxAffinities

aVector = Affinity()
for c in Constellation.constellations:
	score = c.evaluate(model)
	aVector += c.requires*score
aVector = aVector/aVector.magnitude()
Solution.valueVector = aVector
out = "Affinity value: "
for i in range(len(aVector.affinities)):
	out += "%0.2f"%aVector.affinities[i] + Affinity.sh[i] + " "
print out

links = getLinks(wanted)

Search.wanted = wanted
Search.model = model

populationSize = 12
randomsPerGen = 8
minRandomsPerGen = 2

population = [] #solutions

for i in range(populationSize):
	population += [Search(links, True).start()]

def generation(population):	
	for i in range(randomsPerGen):
		population += [Search(links, True).start()]
	random.shuffle(population)
	newPop = []
	for i in range(0, len(population)-1, 2):
		newPop += [breed(population[i], population[i+1]).start()]
	population += newPop
	population = list(set(population))
	population.sort(key=lambda s: s.score, reverse=True)
	population = population[:populationSize]
	print str(population[0])
	print str(population[1])
	print str(population[2])
	print "..."
	print str(population[-2])
	print str(population[-1])
	return population

gen = 0
worst = population[-1]
worstAge = 0
best = population[0]
while True:
	gen += 1
	print "\nGeneration:", gen, "(" + str(randomsPerGen) + ")"
	population = generation(population)

	if population[0].score > best.score:
		best = population[0]
		model.addSolution(best)
		model.saveSeedSolutions()

	if not population[-1] == worst:
		worst = population[-1]
		worstAge = 0
		if randomsPerGen > minRandomsPerGen:
			randomsPerGen = minRandomsPerGen
			print "Population diverse; decreasing randoms:", str(randomsPerGen)
	else:
		worstAge += 1
		if worstAge >= 25:
			randomsPerGen += 1
			print "Population stagnant; increasing randoms:", str(randomsPerGen)
			worstAge = 0
	if randomsPerGen > populationSize:
		print "Population unchanged for "+str(25*(populationSize - minRandomsPerGen)) +" generations."
		for pop in population:
			print "  " + str(pop)
		break