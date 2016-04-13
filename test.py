from dataModel import *
from constellationData import *
from models import nyx


# def getAffinities(constellations):
# 	start = time()
# 	affinities = Affinity()
# 	for c in constellations:
# 		affinities += c.provides
# 	timeMethod("getAffinities", start)
# 	return affinities

# affinities = Affinity()
# for seed in nyx.seedSolutions:
# 	sol = []
# 	for c in seed:
# 		if c.canActivate(affinities):
# 			sol += [c]
# 			affinities = getAffinities(sol)
# 			# print c
# 		else:
# 			print "FAIL FAIL FAIL"
# 			print [str(s) + ", " for s in sol]
# 			print affinities >= c.requires
# 			print affinities, " >= ", c.requires
# 			print affinities
# 			print c

nyx.checkModel()
print bonds.evaluate(nyx)
for star in bonds.stars:
	print star.evaluate(nyx)


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
