from models import *
from utils import *

class Solution:
	maxAffinities = None
	valueVector = None

	def __init__(self, constellations, model):
		self.deadSolutions = {}
		self.boundedPaths = []
		self.links = None
		self.canonicalOrder = sorted(constellations, key=lambda c: c.index/100.0)
		self.isDead = self.isDeadSolution()
		if self.isDead:
			return

		self.cost = getSolutionCost(constellations)
		self.provides = getAffinities(constellations)
		self.score = evaluateSolution(constellations, model)
		self.constellations = constellations

		self.cappingAffinity = Affinity()
		if Solution.maxAffinities != None:
			for ac in Affinity.sh:
				if self.provides.get(ac) > Solution.maxAffinities.get(ac):
					self.provides.set(ac, Solution.maxAffinities.get(ac))
					self.cappingAffinity.set(ac, 99)

	# we're only comparing solutions to see if they should replace an optimal solution for a given point cost
	# so we're greater than if the cost is the same (or less) and either the provides or the score is greater
	# We'll ignore the equals case for now since it doesn't really matter (the score is unlikely to be EXACTLY the same and if it is then there's no downside to replacing the old one)
	def __ge__(self, other):
		if self.cost <= other.cost and self.provides >= other.provides and self.score >= other.score:
			return True

		return False

	def __le__(self, other):
		if self.cost >= other.cost and self.provides <= other.provides and self.score <= other.score:
			return True

		return False

	#true equality would be the same constellations but we only care about score, provides and cost (for now?)
	def __eq__(self, other):
		return self.cost == other.cost and self.provides == other.provides and self.score == other.score

	def __hash__(self):
		return (str(self.cost)+str(self.provides)+str(self.score)).__hash__()

	def __str__(self):
		out = str(self.cost) + "\t" + str(int(self.score)).rjust(7) + "\t\t"
		out += solutionPath(self.constellations) + " "
		# out += str(self.provides)
		return out

	def getLinks(self):
		if self.links:
			return self.links
		else:
			self.links = [c for c in self.constellations if c.getTier() <= 1]
			return self.links


	def isDeadSolution(self):
		deadNode = self.deadSolutions
		for c in self.canonicalOrder:
			if not c.id in deadNode.keys():
				return False
			if deadNode[c.id] == True:
				return True
			deadNode = deadNode[c.id]
		return False

	def kill(self, verbose=False):
		if verbose:
			print "Killing solution: " + solutionPath(self.canonicalOrder)
		deadNode = self.deadSolutions
		for c in self.canonicalOrder:
			if c == self.canonicalOrder[-1]:
				deadNode[c.id] = True
				return

			if not c.id in deadNode.keys():
				deadNode[c.id] = {}
			deadNode = deadNode[c.id]