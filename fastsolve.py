"""Heuristic devotion solver - near-optimal solutions in about a second.

The exhaustive search in devotion.py does not terminate on large models (armitage,
57 points). It does not need to: evaluateSolution is almost entirely additive. Each
constellation contributes a fixed value, and the only coupling is that attack-trigger
constellations take a rank-based discount, with the (nAps+1)-th onward worth exactly
zero. That makes this a knapsack with affinity prerequisites, which greedy
construction plus local search solves very well.

Problem.score() is a flat-array reimplementation of utils.evaluateSolution and is
kept exactly in step with it - see test in devotion.py --fast output, which
re-verifies the winning score through the real evaluateSolution.
"""
import time
import random

from dataModel import Constellation


class Problem:
	"""Flattens the loaded model into arrays that can be scored cheaply."""

	def __init__(self, model):
		self.model = model
		self.cons = list(Constellation.constellations)
		for c in self.cons:
			c.evaluate(model)

		self.points = model.points
		self.n = len(self.cons)

		self.cost = [len(c.stars) for c in self.cons]
		self.base = [float(c.evaluate(model)) for c in self.cons]
		self.isTrig = [bool(c.hasAttackTrigger()) for c in self.cons]
		# value of a trigger constellation when it is the r-th trigger selected
		self.byRank = [list(c.apsValue) if c.hasAttackTrigger() else [] for c in self.cons]
		self.requires = [tuple(c.requires.affinities) for c in self.cons]
		self.provides = [tuple(c.provides.affinities) for c in self.cons]

		# Resistance a solution can overshoot, and how much each constellation
		# grants of it - see utils.cappedResists. Kept as parallel flat lists so
		# score() can add them up without touching a dict.
		from utils import cappedResists
		self.capped = cappedResists(model)
		self.resistGrant = []
		for c in self.cons:
			row = [0.0] * len(self.capped)
			for star in c.stars:
				for k, (damage, _, _) in enumerate(self.capped):
					row[k] += star.bonuses.get(damage, 0.0)
			self.resistGrant.append(row if any(row) else None)

		idx = {id(c): i for i, c in enumerate(self.cons)}
		self.conflicts = [frozenset(idx[id(x)] for x in c.conflicts if id(x) in idx)
						  for c in self.cons]

	def score(self, sel):
		"""Mirrors utils.evaluateSolution for a list of constellation indices."""
		total = 0.0
		trig = []
		for i in sel:
			if self.isTrig[i]:
				trig.append(i)
			else:
				total += self.base[i]
		if trig:
			trig.sort(key=lambda i: -self.base[i])
			for r, i in enumerate(trig):
				# as in Constellation.evaluate, a rank past the end is worth 0
				ranks = self.byRank[i]
				if r < len(ranks):
					total += ranks[r]
		# The one part of the score that is not additive: a resistance stops
		# counting at its cap, so what the selection grants past the headroom
		# has to come back off. Skipped entirely when nothing is near a cap,
		# which is every model that does not state its resistances.
		if self.capped:
			for k, (_, head, weight) in enumerate(self.capped):
				given = 0.0
				for i in sel:
					row = self.resistGrant[i]
					if row is not None:
						given += row[k]
				if given > head:
					total -= (given - head) * weight
		return total

	def feasible(self, sel):
		if sum(self.cost[i] for i in sel) > self.points:
			return False
		s = set(sel)
		for i in sel:
			if self.conflicts[i] & s:
				return False
		return self.activationOrder(sel) is not None

	def activationOrder(self, sel):
		"""Order the set so each pick is activatable when taken; None if impossible.

		Greedy is exact: provides are non-negative, so taking a constellation never
		makes another ineligible. If nothing is eligible now, nothing ever will be.
		"""
		remaining = list(sel)
		have = [0, 0, 0, 0, 0]
		order = []
		while remaining:
			progressed = False
			for k in range(len(remaining) - 1, -1, -1):
				i = remaining[k]
				req = self.requires[i]
				if (have[0] >= req[0] and have[1] >= req[1] and have[2] >= req[2]
						and have[3] >= req[3] and have[4] >= req[4]):
					p = self.provides[i]
					have[0] += p[0]; have[1] += p[1]; have[2] += p[2]
					have[3] += p[3]; have[4] += p[4]
					order.append(i)
					remaining.pop(k)
					progressed = True
			if not progressed:
				return None
		return order


class Solver:
	freshEvery = 2 # every n-th restart rebuilds from scratch rather than perturbing

	def __init__(self, prob, seed=0):
		self.p = prob
		self.rng = random.Random(seed)
		# Pure enablers: require nothing, provide affinity. Several are worth ~0 on
		# their own (Crossroads Chaos scores exactly 0), so a gain-driven constructor
		# never buys them and everything gated behind their affinity stays invisible.
		# Seeding restarts with them is what makes gated branches reachable.
		self.enablers = [i for i in range(prob.n)
						 if sum(prob.requires[i]) == 0 and sum(prob.provides[i]) > 0]

	def provideSum(self, sel):
		h = [0, 0, 0, 0, 0]
		for i in sel:
			q = self.p.provides[i]
			h[0] += q[0]; h[1] += q[1]; h[2] += q[2]; h[3] += q[3]; h[4] += q[4]
		return h

	def canAdd(self, selSet, have, cost, i):
		p = self.p
		if i in selSet or cost + p.cost[i] > p.points:
			return False
		if p.conflicts[i] & selSet:
			return False
		r = p.requires[i]
		# feasible set + non-negative provides => appending last is always valid
		return (have[0] >= r[0] and have[1] >= r[1] and have[2] >= r[2]
				and have[3] >= r[3] and have[4] >= r[4])

	def greedy(self, sel=None, rcl=1):
		"""rcl=1 is pure greedy; rcl>1 picks among the top rcl candidates (GRASP),
		which is what lets restarts reach genuinely different basins."""
		p = self.p
		sel = list(sel) if sel else []
		selSet = set(sel)
		cost = sum(p.cost[i] for i in sel)
		have = self.provideSum(sel)
		cur = p.score(sel)
		while True:
			cands = []
			for i in range(p.n):
				if not self.canAdd(selSet, have, cost, i):
					continue
				gain = (p.score(sel + [i]) - cur) / p.cost[i]
				if gain > 0.0:
					cands.append((gain, i))
			if not cands:
				break
			if rcl > 1 and len(cands) > 1:
				cands.sort(key=lambda t: -t[0])
				pick = cands[self.rng.randrange(min(rcl, len(cands)))][1]
			else:
				pick = max(cands)[1]
			sel.append(pick)
			selSet.add(pick)
			cost += p.cost[pick]
			q = p.provides[pick]
			for k in range(5):
				have[k] += q[k]
			cur = p.score(sel)
		return sel, cur

	def localSearch(self, sel):
		p = self.p
		sel = list(sel)
		cur = p.score(sel)
		improved = True
		while improved:
			improved = False
			selSet = set(sel)
			cost = sum(p.cost[i] for i in sel)
			have = self.provideSum(sel)
			for i in range(p.n):
				if self.canAdd(selSet, have, cost, i):
					s = p.score(sel + [i])
					if s > cur + 1e-9:
						sel.append(i)
						cur = s
						improved = True
						selSet.add(i)
						cost += p.cost[i]
						q = p.provides[i]
						for k in range(5):
							have[k] += q[k]
			if improved:
				continue

			bestDelta, bestMove = 1e-9, None
			for a in range(len(sel)):
				trimmed = sel[:a] + sel[a + 1:]
				if p.activationOrder(trimmed) is None:
					continue
				tSet = set(trimmed)
				tCost = sum(p.cost[i] for i in trimmed)
				tHave = self.provideSum(trimmed)
				for i in range(p.n):
					if not self.canAdd(tSet, tHave, tCost, i):
						continue
					s = p.score(trimmed + [i])
					if s - cur > bestDelta:
						bestDelta, bestMove = s - cur, (a, i)
			if bestMove:
				a, i = bestMove
				sel = sel[:a] + sel[a + 1:] + [i]
				cur = p.score(sel)
				improved = True
				continue

			# Last resort: force each unused enabler in (dropping one pick to pay for
			# it) and refill greedily. Single swaps cannot reach a better basin when
			# it is gated behind cheap affinity, because buying the enabler is a loss
			# until the constellation it unlocks is also bought.
			for e in self.enablers:
				if e in sel:
					continue
				for a in range(len(sel)):
					trimmed = sel[:a] + sel[a + 1:] + [e]
					if p.activationOrder(trimmed) is None:
						continue
					cand, candScore = self.greedy(trimmed)
					if candScore > cur + 1e-9:
						sel, cur = cand, candScore
						improved = True
						break
				if improved:
					break
		return sel, cur

	def solve(self, budget=1.0):
		p = self.p
		t0 = time.time()
		sel, cur = self.localSearch(self.greedy()[0])
		best, bestScore = list(sel), cur
		restarts = 0
		while time.time() - t0 < budget:
			restarts += 1
			if restarts % Solver.freshEvery == 0:
				# fresh build seeded with a random enabler set
				keep = (self.rng.sample(self.enablers,
										self.rng.randint(0, min(4, len(self.enablers))))
						if self.enablers else [])
			else:
				# ruin & recreate: drop a random slice of the incumbent
				keep = list(best)
				for _ in range(self.rng.randint(1, max(2, len(keep) // 2))):
					if keep:
						keep.pop(self.rng.randrange(len(keep)))
				if p.activationOrder(keep) is None:
					keep = []
			sel, cur = self.localSearch(self.greedy(keep, rcl=self.rng.choice((1, 2, 3, 4)))[0])
			if cur > bestScore:
				best, bestScore = list(sel), cur
		return best, bestScore, restarts


def solveModel(model, budget=1.0, seeds=5, verbose=True):
	"""Multi-start solve. Returns (constellations in activation order, score).

	Independent seeds land in different basins, so the best of several short runs
	beats one long run. Each seed gets the full budget.
	"""
	prob = Problem(model)
	best, bestScore, totalRestarts = None, -1.0, 0
	for s in range(max(1, seeds)):
		sel, score, restarts = Solver(prob, seed=s).solve(budget)
		totalRestarts += restarts
		if score > bestScore:
			best, bestScore = sel, score
		if verbose:
			print("  seed %d: %10.0f%s" % (s, score, "   <- best" if score >= bestScore else ""))
	order = prob.activationOrder(best) or best
	return prob, [prob.cons[i] for i in order], bestScore, totalRestarts
