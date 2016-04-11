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

a = range(10)
print a
for i in range(1, len(a)):
	print a[:i+1]



# optimizations to try:
	# when considering path values, consider only up to our total needs.
		# if the max of our wanted is 2a 10o 6c it makes no sense to give more value to 10a 10o 6c. The extra ascendant is useless.

# consider tracking all bounded paths of low length or low points. It may be worth the extra time to nip paths in the bud early if they're redundant.