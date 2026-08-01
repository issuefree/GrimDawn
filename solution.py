from models import *
from utils import *

class Solution:
	maxAffinities = None
	valueVector = None

	# Shared prefix-trie of fully-explored / pruned constellation sets, keyed by
	# canonical (index-sorted) order so [A,B] and [B,A] collapse to one entry.
	# This MUST be class level: as an instance attribute every solution got a
	# fresh empty trie, so kill() wrote to a dict that was thrown away and
	# isDeadSolution() always returned False.
	deadSolutions = {}

	@classmethod
	def resetDeadSolutions(cls):
		cls.deadSolutions = {}

	def __init__(self, constellations, model):
		self.links = None
		# /100.0 did not affect ordering, it just cost a float division per element
		self.canonicalOrder = sorted(constellations, key=attrgetter("index"))
		self.isDead = self.isDeadSolution()
		if self.isDead:
			return

		self.cost = getSolutionCost(constellations)
		self.provides = getAffinities(constellations)
		self.score = evaluateSolution(constellations, model)
		self.constellations = constellations

		self.cappingAffinity = Affinity()
		if Solution.maxAffinities:
			# index the lists directly rather than going through get/set per axis
			provides = self.provides.affinities
			maxes = Solution.maxAffinities.affinities
			capping = self.cappingAffinity.affinities
			for i in range(5):
				if provides[i] > maxes[i]:
					provides[i] = maxes[i]
					capping[i] = 99

	# we're only comparing solutions to see if they should replace an optimal solution for a given point cost
	# so we're greater than if the cost is the same (or less) and either the provides or the score is greater
	# We'll ignore the equals case for now since it doesn't really matter (the score is unlikely to be EXACTLY the same and if it is then there's no downside to replacing the old one)
	# scalar comparisons first - `provides` is an Affinity compare and much dearer
	def __ge__(self, other):
		return self.cost <= other.cost and self.score >= other.score and self.provides >= other.provides

	def __le__(self, other):
		return self.cost >= other.cost and self.score <= other.score and self.provides <= other.provides

	#true equality would be the same constellations but we only care about score, provides and cost (for now?)
	def __eq__(self, other):
		return self.cost == other.cost and self.provides == other.provides and self.score == other.score

	# Hash on the same fields __eq__ compares. Formatting these into a string was
	# costing a full Affinity.__str__ per call, and this runs over a million times.
	def __hash__(self):
		return hash((self.cost, tuple(self.provides.affinities), self.score))

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


	# dead if this set, or any prefix of it in canonical order, has been marked.
	# A marked prefix means that whole subtree was already explored or pruned.
	def isDeadSolution(self):
		deadNode = Solution.deadSolutions
		for c in self.canonicalOrder:
			if not c.id in deadNode:
				return False
			if deadNode[c.id] is True:
				return True
			deadNode = deadNode[c.id]
		return False

	def kill(self, verbose=False):
		if verbose:
			print("Killing solution: " + solutionPath(self.canonicalOrder))
		deadNode = Solution.deadSolutions
		last = len(self.canonicalOrder) - 1
		for i, c in enumerate(self.canonicalOrder):
			if i == last:
				deadNode[c.id] = True
				return

			if not c.id in deadNode:
				deadNode[c.id] = {}
			elif deadNode[c.id] is True:
				return # a shorter prefix is already dead, so this path is covered
			deadNode = deadNode[c.id]