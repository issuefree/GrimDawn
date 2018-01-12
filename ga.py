from constellationData import *
from dataModel import *
from models import *
from utils import *
from solution import *

model = Model.loadModel("Armitage")
model.initialize(False)

wanted = getWanted(model)

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

needed = getNeededConstellations([], wanted, model)

