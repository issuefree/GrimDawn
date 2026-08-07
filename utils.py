from dataModel import *


def fmt(value, places=2):
	"""A number for reading rather than for round-tripping.

	Two decimals, trailing zeroes and the trailing point dropped, so 0.25 stays
	0.25, 19.800000000000001 becomes 19.8 and 8.957061529508433 becomes 8.96.
	Anything that is not a number is handed back untouched - a few weights are
	a [dps, seconds] pair.
	"""
	if isinstance(value, (list, tuple)):
		return "[%s]" % ", ".join(fmt(v, places) for v in value)
	if not isinstance(value, (int, float)) or isinstance(value, bool):
		return str(value)
	text = ("%%.%df" % places) % value
	return text.rstrip("0").rstrip(".") if "." in text else text


def getLinks(wanted, remaining=None):
	maxAffinities = Affinity()
	for c in wanted:
		maxAffinities = maxAffinities.maxAffinities(c.requires)

	if remaining == None:
		remaining = [p for p in Constellation.constellations if p.getTier() <= 1 and not p in wanted]

	possibles = [c for c in remaining if maxAffinities.intersects(c.provides)]

	return possibles

def printSolution(solution, model, pre=""):
	print(int(evaluateSolution(solution, model)),":",solutionPath(solution))

def solutionPath(solution, pre=""):
	out = ""
	for c in solution:
		out += c.id + ", "
	out = out[:-2]	
	return pre + "["+out+"],"

def evaluateSolution(solution, model, verbose=False):
	if verbose:
		print("Evaluating solution...")
		print("  " + solutionPath(solution))
	start = time()
	# Decorate with the sort key so the base value can be reused below instead of
	# calling evaluate a second time for every constellation.
	sSol = sorted(((c.evaluate(model), c) for c in solution), key=itemgetter(0), reverse=True)
	value = 0

	abilNum = 0
	for base, c in sSol:
		if verbose:
			print(c.name.ljust(40), int(base), int(c.evaluate(model, abilNum)))
		if c.hasAttackTrigger():
			value += c.evaluate(model, abilNum)
			abilNum += 1
		else:
			value += base
	timeMethod("evaluateSolution", start)
	return value

def orderSolution(solution, model, limit=18):
	"""Order a finished solution so its score climbs as early as it can.

	The solver picks a set; it does not say what to buy first. That is a
	separate question and the one that matters while you are levelling - a
	twenty point plan is also a ten point plan, and which ten depends entirely
	on the order.

	Two things constrain it. Affinity gates what can be taken next, and the
	score you actually play with between purchases is the score of what you
	have already bought. Maximising the score curve on the way up is the same
	as maximising the area under it, and the area falls out one purchase at a
	time: while saving the stars for c you hold the score of everything before
	it, so

	    area(T + c) = area(T) + score(T) * stars(c)

	That depends only on the set already taken, which makes it an exact subset
	dynamic program rather than a heuristic. A solution is a dozen or so
	constellations and a subset costs about 8 microseconds to score, so the
	whole thing is a tenth of a second.

	Scores are not additive and cannot be summed as we go: evaluateSolution
	ranks the attack-triggered constellations and hands each a different attack
	rate, so what a proc is worth depends on what else is in the set. score(T)
	is therefore evaluated per subset.

	Above `limit` constellations the 2^n gets uncomfortable and this falls back
	to taking the best score per star that affinity currently allows, which is
	the same objective decided one step at a time instead of all at once.
	"""
	solution = list(solution)
	n = len(solution)
	if n < 2:
		return solution

	stars = [len(c.stars) for c in solution]
	index = {id(c): i for i, c in enumerate(solution)}
	# conflicts as a bitmask over this solution, so the check is one AND
	conflict = [0] * n
	for i, c in enumerate(solution):
		for other in c.conflicts:
			if id(other) in index:
				conflict[i] |= 1 << index[id(other)]

	if n > limit:
		return _greedyOrder(solution, model, stars, conflict)

	scores = {}
	def score(mask):
		if mask not in scores:
			scores[mask] = evaluateSolution(
				[solution[i] for i in range(n) if mask >> i & 1], model)
		return scores[mask]

	# affinity of each subset, built off the subset with its lowest bit removed
	affinity = [None] * (1 << n)
	affinity[0] = [0, 0, 0, 0, 0]
	requires = [c.requires.affinities for c in solution]

	worst = float("-inf")
	best = [worst] * (1 << n)
	took = [-1] * (1 << n)
	best[0] = 0.0

	for mask in range(1 << n):
		if mask:
			low = mask & -mask
			i = low.bit_length() - 1
			have = list(affinity[mask ^ low])
			p = solution[i].provides.affinities
			for k in range(5):
				have[k] += p[k]
			affinity[mask] = have
		if best[mask] == worst:
			continue
		have = affinity[mask]
		here = score(mask)
		base = best[mask]
		for i in range(n):
			bit = 1 << i
			if mask & bit or mask & conflict[i]:
				continue
			need = requires[i]
			if (have[0] < need[0] or have[1] < need[1] or have[2] < need[2]
					or have[3] < need[3] or have[4] < need[4]):
				continue
			value = base + here * stars[i]
			if value > best[mask | bit]:
				best[mask | bit] = value
				took[mask | bit] = i

	full = (1 << n) - 1
	if best[full] == worst:
		# nothing orderable - the set cannot be bought in any sequence, so say
		# nothing about order rather than printing a plan that does not work
		return solution
	order, mask = [], full
	while mask:
		i = took[mask]
		order.append(solution[i])
		mask &= ~(1 << i)
	order.reverse()
	return order


def _greedyOrder(solution, model, stars, conflict):
	"""One step at a time: whatever affinity allows that buys the most per star."""
	remaining = set(range(len(solution)))
	taken, order, mask = [], [], 0
	while remaining:
		have = getAffinities(taken).affinities
		bestGain, bestIndex = None, None
		for i in sorted(remaining):
			if mask & conflict[i]:
				continue
			need = solution[i].requires.affinities
			if any(have[k] < need[k] for k in range(5)):
				continue
			gain = evaluateSolution(taken + [solution[i]], model) / stars[i]
			if bestGain is None or gain > bestGain:
				bestGain, bestIndex = gain, i
		if bestIndex is None:
			# unreachable from here; append the rest as they came
			order += [solution[i] for i in sorted(remaining)]
			break
		remaining.discard(bestIndex)
		mask |= 1 << bestIndex
		taken.append(solution[bestIndex])
		order.append(solution[bestIndex])
	return order


def getSolutionCost(solution):
	start = time()
	cost = 0
	for s in solution:
		cost += len(s.stars)
	timeMethod("getSolutionCost", start)
	return cost

def isGoodSolution(solution):
	affinities = Affinity()
	sol = []
	for c in solution:
		if c.canActivate(affinities):
			sol += [c]
			affinities = getAffinities(sol)
		else:
			print(c.name)
			return False
	return True

# cache if performance becomes an issue
def getAffinities(constellations):
	start = time()
	# Accumulate into a plain list: `affinities += c.provides` allocated a fresh
	# Affinity per constellation, which dominated Solution construction.
	total = [0, 0, 0, 0, 0]
	for c in constellations:
		p = c.provides.affinities
		total[0] += p[0]
		total[1] += p[1]
		total[2] += p[2]
		total[3] += p[3]
		total[4] += p[4]
	affinities = Affinity()
	affinities.affinities = total
	timeMethod("getAffinities", start)
	return affinities

def findBonus(targetBonuses):
	if type(targetBonuses) == type(""):
		targetBonuses = [targetBonuses]
	targets = []
	for c in Constellation.constellations:		
		for s in c.stars:
			if c in targets:
				break
			for targetBonus in targetBonuses:
				if targetBonus in s.bonuses:
					targets += [c]
					break
				if s.ability:
					if targetBonus in s.ability.bonuses:
						targets += [c]
						break
	return targets

def printBonusList():
	print("All constellation bonuses:")
	bonuses = {}
	for c in Constellation.constellations:
		for s in c.stars:
			for bonus in s.bonuses:
				bonuses[bonus] = True
			if s.ability:
				for bonus in s.ability.bonuses:
					bonuses[bonus] = True

	for key in sorted(bonuses.keys()):
		print("\t\t#\""+key+"\":0, ")
		
def getBonuses(constellations=Constellation.constellations, model=None):
	bonuses = {}
	for c in constellations:
		for s in c.stars:
			s.evaluate(model)
			for bonus in s.bonuses:
				if model and not bonus in model.bonuses:
					continue
				if bonus in bonuses:
					if type(s.bonuses[bonus]) == type([]):
						bonuses[bonus] = addDurationDamages(bonuses[bonus], s.bonuses[bonus])
					else:
						bonuses[bonus] += s.bonuses[bonus]
				else:
					bonuses[bonus] = s.bonuses[bonus]
	return bonuses

def getTriggerChance(chance, tps):
	return 1-(1-chance)**tps

def getPathBounds(path, model):
	score = 0
	provides = Affinity()
	points = 0
	for c in path:
		score += c.evaluate(model)
		provides += c.provides
		points += len(c.stars)
		print(points, score, provides)

def evaluateBonuses(model, bonuses):
	value = 0
	for bonus in model.bonuses:
		if bonus in bonuses:			
			value += model.calculateBonus(bonus, bonuses[bonus])
	return value

def startsWith(start, complete):
	if len(start) == 0:
		return False
	for i in range(len(start)):
		if start[i] != complete[i]:
			return False
	return True

def getHighestScoring(constellationRanks, verbose=True):
	constellationRanks.sort(key=itemgetter(1), reverse=True)
	thresh = constellationRanks[len(constellationRanks)//6][1] * .8

	if verbose:
		print("\n  Desired constellations (value > %s):"%thresh)
	wanted = []
	for c in constellationRanks:
		if c[1] > thresh:
			wanted += [c[0]]
			if verbose:
				print("         ", str(int(c[1])).rjust(7), c[0].name.ljust(45), c[0].requires)
		else:
			if verbose:
				print("       - ", str(int(c[1])).rjust(7), c[0].name.ljust(45), c[0].requires)

	return wanted, constellationRanks[0][1]

def getMostEfficient(constellationRanks, verbose=True):
	constellationRanks.sort(key=itemgetter(2), reverse=True)
	thresh = constellationRanks[len(constellationRanks)//6][2] * .8

	if verbose:
		print("\n  Desired constellations (efficiency > %s):"%thresh)
	wanted = []
	for c in constellationRanks:
		if c[2] > thresh:
			wanted += [c[0]]
			if verbose:
				print("      ", int(c[2]), c[0].name)
		else:
			if verbose:
				print("       - ", int(c[2]), c[0].name)

	return wanted, constellationRanks[0][2]

def getBestConstellations(model):
	print("\nEvaluating constellations...")
	constellationRanks = []
	for c in Constellation.constellations:
		if "[" in c.id:
			score = 0
		else:
			score = c.evaluate(model, True)		
		efficiency = c.evaluate(model)/len(c.stars)
		constellationRanks += [(c, score, efficiency)]
		c.buildRedundancies(model)

	return constellationRanks

def sortByLeastProvides(constellations, model):
	start = time()

	out = sorted(constellations, key=lambda c: c.provides.magnitude())

	timeMethod("sortByScore", start)
	return out

def sortByScore(constellations, model):
	start = time()
	out = sorted(constellations, key=lambda c: c.evaluate(model), reverse=True)
	timeMethod("sortByScore", start)
	return out

def sortByLowScore(constellations, model):
	start = time()
	out = sorted(constellations, key=lambda c: c.evaluate(model), reverse=False)
	timeMethod("sortByScore", start)
	return out

def sortByScorePerStar(constellations, model):
	start = time()
	out = sorted(constellations, key=lambda c: (c.evaluate(model)/len(c.stars)), reverse=True)
	timeMethod("sortConstellationsByScorePerStar", start)
	return out

def sortConstellationsByProvides(constellations):
	start = time()
	out = sorted(constellations, key=lambda c: c.provides.magnitude(), reverse=True)
	timeMethod("sortConstellationsByProvides", start)
	return out

def sortConstellationsByProvidesValue(constellations):
	start = time()
	out = sorted(constellations, key=lambda c: (c.provides*globalMetadata["providesValue"]).magnitude(), reverse=True)
	timeMethod("sortConstellationsByProvidesValue", start)
	return out

def sortConstellationsByProvidesValueScore(constellations, model, valueVector):
	out = sorted(constellations, key=lambda c: (c.provides*valueVector).magnitude()*c.evaluate(model), reverse=True)
	return out
