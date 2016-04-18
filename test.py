import sys
from dataModel import *
from constellationData import *
from utils import *
from models import *

import os

model = armitage
model.checkModel()
# print model

solution = [
	xC,
	fiend,
	viper,
	hound,
	light,
	manticore,
	behemothGiantsBlood,
	anvil,
	crown,
	messengerMessengerofWar,
	xO,
	dryad,
	targoShieldWall
]

# sSol = sorted(solution, key=lambda c: c.evaluate(model))
# for c in sSol:
# 	print c.id, int(c.evaluate(model))

# print getSolutionCost(solution)

if isGoodSolution(solution):
	for c in solution:
		print c.name, c.evaluate(model)
else:
	print "FAIL"

# print
# print

# solByVal = sorted(solution, key=lambda c: c.evaluate(model), reverse=True)

# print solutionPath(solByVal)
# print isGoodSolution(solution)

# print
# print

# optimizations to try:

# consider tracking all bounded paths of low length or low points. It may be worth the extra time to nip paths in the bud early if they're redundant.

# consider making a run with path length capped at some low number to identify useless paths across the set. 
	# If we start on xA and there's an optimal start at xC we may evaluate several million unnecessary solutions.
	# the cost of a run to detph 3 or 4 may not be very high relative to the gain.

# there's a flaw in our approach to attack triggered abilities.
#	1. I don't want more attack triggered abilities than I have decent attacks.
#	2. The attacks per second isn't our total attacks per second it's the a/s of the linked ablity.
#		I don't know the ability at analysis time so I can't really put a good a/s number on it.
#		I think I'll have to use this as a guide and tweak the numbers after the fact.

# Some abilities may have pretty different value for melee vs ranged characters. Specifically pbaoe abilities.
	# consider a pbaoe flag in the ability and adjust the dynamic values based on the characters flag of melee/ranged

#IN GAME:
	# check if fetid pool ticks damage on targets.


print
print
c = manticore

print c.evaluate(model)

for star in c.stars:
	if star.ability:
		print star.ability.name, star.ability.effective
	for bonus in star.bonuses:
		if model.get(bonus) != 0:
			print str(bonus).ljust(25), int(star.bonuses[bonus]), "\t", int(model.get(bonus)*star.bonuses[bonus])

print
print
print

# for c in sorted(Constellation.constellations, key=lambda c: c.evaluate(model)/len(c.stars), reverse=True):
# 	print c.name, int(c.evaluate(model)/len(c.stars))

# print "eel", len(eel.stars), eel.provides, eel.evaluate(model)
# print "lizard", len(lizard.stars), lizard.provides, lizard.evaluate(model)
# print "guide", len(guide.stars), guide.provides, guide.evaluate(model)
# print "tsunami", len(tsunami.stars), tsunami.provides, tsunami.evaluate(model)
# print "gallows", len(gallows.stars), gallows.provides, gallows.evaluate(model)

# providers = [eel, lizard, guide, tsunami, gallows]

# def getSolutionProvides(solution):
# 	provides = Affinity()
# 	for c in solution:
# 		provides += c.provides
# 	return provides

# def getMinProviders(solution, remaining, need):
# 	global globalMetadata
# 	provides = getSolutionProvides(solution)
# 	# print solutionPath(solution), provides, getSolutionCost(solution), evaluateSolution(solution, model)
# 	if provides >= need:
# 		addBoundedPath(solution, need, model)
# 		return
# 	print provides, solutionPath(solution)
# 	needLeft = need - provides
# 	for p in remaining:
# 		if p.provides.intersects(needLeft):
# 			newRemaining = remaining[:]
# 			newRemaining.remove(p)
# 			getMinProviders(solution + [p], newRemaining, need)

# # print solutionPath(minProviders)

# globalMetadata = {}
# globalMetadata["boundedPaths"] = [] 

# def addBoundedPath(solution, need, model):
# 	global globalMetadata

# 	affinities = getAffinities(solution).minAffinities(need)
# 	cost = getSolutionCost(solution)
# 	score = evaluateSolution(solution, model)

# 	for bpi in range(len(globalMetadata["boundedPaths"])-1, -1, -1):
# 		bp = globalMetadata["boundedPaths"][bpi]
# 		if affinities <= bp[0] and cost >= bp[1] and score < bp[2]: 
# 			return 
# 		if affinities >= bp[0] and cost <= bp[1] and score > bp[2]:
# 			del globalMetadata["boundedPaths"][bpi]
# 	globalMetadata["boundedPaths"] += [[affinities, cost, score, solution]]


# need = Affinity()
# wanted = [targo, obelisk]
# for c in wanted:
# 	need = need.maxAffinities(c.requires)


# providers = []
# for c in Constellation.constellations:
# 	if c.requires.magnitude() <= 1 and need.intersects(c.provides):
# 		providers += [c]

# print(solutionPath(providers))

# getMinProviders([], sorted(providers, key=lambda c: c.provides, reverse=True), need)

# # print globalMetadata["boundedPaths"][0]

# for s in globalMetadata["boundedPaths"]:
# 	print solutionPath(s[3]).ljust(28), str(s[1]).rjust(3), str(int(s[2])).rjust(5), s[2]/s[1]

# needs = []
# for s in globalMetadata["boundedPaths"]:
# 	for p in s[3]:
# 		if p not in needs:
# 			needs += [p]
# print solutionPath(needs)

# for p in providers:
# 	if not p in needs:
# 		print p
# # print getSolutionCost([xC, fiend, viper, hound, light, behemothGiantsBlood, manticore, anvil, messengerMessengerofWar, crown, xO, dryad, targoShieldWall])

# now we snag any t1 constellation that can possibly help get a wanted constellation
	# for each wanted c figure minimAl SETs of t1 to get it. merge them for stepping stones.



# def isUnary(c, afC):
# 	if len(afC) > 1:
# 		print "Single character affinity string pls."
# 		return False
# 	affinity = Affinity("1000"+afC)
# 	if c.requires.magnitude() != 1:
# 		return False
# 	if affinity > c.provides and c.provides.get(afC) > 0:
# 		return True
# 	return False

# need = obelisk.requires.maxAffinities(leviathan.requires)
# afV = "a"
# providesV = []
# for c in Constellation.constellations:
# 	if isUnary(c, afV):
# 		providesV += [c]
# for c in providesV:
# 	c.evaluate(model)
# 	print c.name, int(c.evaluate()), len(c.stars), c.provides.get(afV)

# def isBetter(c1, c2):
# 	if len(c1.stars) <= len(c2.stars) and c1.evaluate() >= c2.evaluate() and c1.provides >= c2.provides:
# 		if len(c1.stars) == len(c2.stars) and c1.evaluate() == c2.evaluate() and c1.provides == c2.provides:
# 			return False
# 		else:
# 			return True
# 	return False

# def isWorse(c1, c2):
# 	if len(c1.stars) >= len(c2.stars) and c1.evaluate() <= c2.evaluate() and c1.provides <= c2.provides:
# 		if len(c1.stars) == len(c2.stars) and c1.evaluate() == c2.evaluate() and c1.provides == c2.provides:
# 			return False
# 		else:
# 			return True
# 	return False

# scores = []
# for c in providesV:
# 	score = 0
# 	for d in providesV:
# 		if isWorse(c, d):
# 			score += 1
# 	scores += [(c, score)]


# scores = [score[0] for score in sorted(scores, key=lambda c: c[1], reverse=True)]
# print [c.name for c in scores]
# print need.get(afV)-1
# for i in range(len(scores)):
# 	total = sum([c.provides.get(afV) for c in scores[i:]])
# 	if total < need.get(afV)-1:
# 		break

# print(sum([c.provides.get(afV) for c in scores[i-1:]]))
# print [c.name for c in scores[i-1:]]