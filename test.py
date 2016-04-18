import sys
from dataModel import *
from constellationData import *
from utils import *
from models import *

import os


def getWanted(model):
	print "\nEvaluating constellations..."
	constellationRanks = []
	for c in Constellation.constellations:
		constellationRanks += [(c, c.evaluate(model), c.evaluate(model)/len(c.stars))]
		c.buildRedundancies(model)

	constellationRanks.sort(key=itemgetter(1), reverse=True)
	thresh = constellationRanks[len(constellationRanks)/6][1] * .9

	print "\n  Desired constellations (value > %s):"%thresh
	wanted = []
	cv = constellationRanks[0][1]
	for c in constellationRanks:
		if c[1] > thresh:
			wanted += [c[0]]
			print "      ", int(c[1]), c[0].name
		else:
			print "       - ", int(c[1]), c[0].name

	constellationRanks.sort(key=itemgetter(2), reverse=True)
	thresh = constellationRanks[len(constellationRanks)/6][2]

	print "\n  Desired constellations (efficiency > %s):"%thresh
	wanted = []
	for c in constellationRanks:
		if c[2] > thresh and not c[0] in wanted:
			wanted += [c[0]]
			print "      ", int(c[2]), c[0].name
		else:
			print "       - ", int(c[2]), c[0].name

	print "  Total:", len(wanted)
	return wanted


model = armitage
model.checkModel()
# print model

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
