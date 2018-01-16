from utils import *
from solution import *
import random

class Search:		
	bestScorePerStar = 0

	def __init__(self, links, getRandomSolution=False):
		self.numChecked = 0
		self.bestScore = 0
		self.bestSolutions = []
		self.boundedPaths = []

		self.complete = False

		self.links = list(set(links))
		self.getRandomSolution = getRandomSolution

	def __str__(self):
		if self.complete:
			out = "Search: " + str(self.bestSolutions[0]) + " + " + str(len(self.bestSolutions)) + "\n"
			out += "  " + str([c.name for c in self.links])
		else:
			out = "Search from: " + str([c.name for c in self.links])
		return out

	def start(self):
		self.next(Search.wanted, Search.model.points, Solution([], Search.model), self.links)
		self.complete = True
		self.bestSolutions.sort(key=lambda s: s.score, reverse=True)
		return self.bestSolutions[0]

	def next(self, wanted, points, solution, remainingLinks, moveStr=""):
		if self.complete:
			return
		self.numChecked += 1

		ub = solution.score + points*Search.bestScorePerStar
		if ub < self.bestScore and solution.score < ub:
			# print ub, "<", globalMetadata["bestScore"]
			# print points, "points left before trim"
			solution.kill()
			return

		if self.boundPath(solution):
			# print "Killing bounded solution:", solution
			solution.kill()
			return

		neededAffinities = Solution.maxAffinities - solution.provides

		remainingLinks = [c for c in remainingLinks if neededAffinities.intersects(c.provides)]
		possibleMoves = wanted + remainingLinks

		nextMoves = self.getNextMoves(solution, possibleMoves, points)

		if self.getRandomSolution:
			method = random.randint(1,3)
			if method == 1:
				random.shuffle(nextMoves)
			elif method == 2:
				nextMoves = sortByScore(nextMoves, Search.model)
				nextMoves = nextMoves[:int(len(nextMoves)*.75)]
			elif method == 3:
				nextMoves = sortConstellationsByProvidesValueScore(nextMoves, Search.model, Solution.valueVector)
				nextMoves = nextMoves[:int(len(nextMoves)*.75)]
			
		else:
			nextMoves = sortConstellationsByProvidesValueScore(nextMoves, Search.model, Solution.valueVector)


		isSolution = True
		newWanted = wanted[:]
		links = remainingLinks[:]

		for move in nextMoves:
			isSolution = False
			newMoveStr = moveStr + move.id + "("+ str(int(move.evaluate(Search.model))) +")" +" {"+str(nextMoves.index(move)+1)+"/"+str(len(nextMoves))+"}, "

			try:
				links.remove(move)
			except:
				pass

			try:
				newWanted.remove(move)
			except:
				pass

			nextSolution = Solution(solution.constellations+[move], Search.model)
			if not nextSolution.isDead:
				self.next(newWanted, points-len(move.stars), nextSolution, links, newMoveStr)

		solution.kill()

		if isSolution:
			if self.getRandomSolution:
				self.bestScore = solution.score
				self.bestSolutions += [solution]
				self.complete = True
			if solution.score >= self.bestScore:
				self.bestScore = solution.score
				self.bestSolutions += [solution]

	def boundPath(self, solution, maxLength=5):
		if len(solution.constellations) > maxLength:
			return False

		for bpi in range(len(self.boundedPaths)-1, -1, -1):
			bp = self.boundedPaths[bpi]
			if solution <= bp and not solution == bp:
				return True
			elif solution >= bp:
				self.boundedPaths[bpi] = solution

		if len(solution.constellations) <= maxLength:
			self.boundedPaths += [solution]
		self.boundedPaths = list(set(self.boundedPaths))

		return False

	def getNextMoves(self, current, possibles, points):
		moves = [c for c in possibles if len(c.stars) <= points and c.canActivate(current.provides, current.constellations) and c not in current.constellations]

		tempMoves = moves[:]
		for move in tempMoves:
			for other in moves:
				if other in move.redundancies:
					moves.remove(move)
					break

		return moves
