from constellationData import *
from dataModel import *
from models import *
from utils import *
from solution import *
from search import *
import random
import sys

class Population:

	def __init__(self, populationSize):
		self.generation = 0
		self.populationScore = 0

		self.populationSize = populationSize
		self.spawns = populationSize/2

		self.population = []

		print "Initializing population"
		for i in range(populationSize):
			self.population += [Search(links, True).start()]
			sys.stdout.write(".")
			sys.stdout.flush()
		print


	def evolve(self):
		self.generation += 1
		print "  generating mutants..."
		sys.stdout.write("    ")
		for i in range(self.spawns):
			self.population += [Search(links, True).start()]
			sys.stdout.write(".")
			sys.stdout.flush()
		print
		random.shuffle(self.population)
		newPop = []
		print "  breeding..."
		sys.stdout.write("    ")
		for i in range(0, len(self.population)-1, 2):
			newPop += [breed(self.population[i], self.population[i+1]).start()]
			sys.stdout.write(".")
			sys.stdout.flush()
		print
		self.population += newPop
		self.population = list(set(self.population))
		self.population.sort(key=lambda s: s.score, reverse=True)
		self.population = self.population[:self.populationSize]

		popScore = self.getPopScore()
		print popScore
		if popScore > self.populationScore:
			self.lastEvolvedGeneration = self.generation
			self.populationScore = popScore

		print str(self.population[0])
		print str(self.population[1])
		print str(self.population[2])
		print "..."
		print str(self.population[-2])
		print str(self.population[-1])

	def getPopScore(self):
		return int(sum([s.score for s in self.population]))

	def getStagnation(self):
		return self.generation - self.lastEvolvedGeneration

	def resetStagnation(self):
		self.populationScore = 0

	def getBest(self):
		return self.population[0]

	def getWorst(self):
		return self.population[-1]

	def getEntropy(self):
		return self.spawns

	def getMaxEntropy(self):
		return self.populationSize		

	def increaseEntropy(self):
		self.spawns += 1

	def reduceEntropy(self):
		self.spawns = max(self.spawns-1, self.getMinimumEntropy())

	def getMinimumEntropy(self):
		return max(self.populationSize/4, 1)

def breed(a, b):
	links = [c for c in a.getLinks() if c in b.getLinks()]
	other = [c for c in a.getLinks() + b.getLinks() if c not in links]
	links += random.sample(other, int(len(other)*.75))
	return Search(links)
	# return Search(a.getLinks() + b.getLinks())

model = Model.loadModel("Lochlan")

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

def run(size):
	population = Population(size)
	best = population.getBest()
	while True:
		print "\nGeneration:", population.generation, "(" + str(population.getEntropy()) + ")"
		population.evolve()

		if population.getBest().score > best.score:
			best = population.getBest()
			model.addSolution(best)
			model.saveSeedSolutions()

		if population.getStagnation() == 0:
			population.reduceEntropy()
			population.reduceEntropy()
			print "Population changed; reducing entropy:", str(population.getEntropy())
		elif population.getStagnation() % 10 == 0:
			population.increaseEntropy()
			print "Population stagnant; increasing entropy:", str(population.getEntropy())

		if population.getEntropy() > population.getMaxEntropy():
			print "Population stable under max entropy."
			for pop in population.population:
				print "  " + str(pop)
			break

model.points = 53
run(12)
