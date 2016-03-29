from constellationData import *

def getAvailableStars():
	available = []
	for c in Constellation.constellations:
		for s in c.stars:
			if s.canActivate(getAffinities()):
				available += [s]
	return available


# cache if performance becomes an issue
def getAffinities():
	affinities = Affinity()
	affinities
	for c in Constellation.constellations:
		if c.isComplete():
			affinities += c.provides
	return affinities

def getBonuses():
	bonuses = {}
	for c in Constellation.constellations:
		for s in c.stars:
			if s.active:
				for bonus in s.bonuses.keys():
					if bonus in bonuses.keys():
						bonuses[bonus] += s.bonuses[bonus]
					else:
						bonuses[bonus] = s.bonuses[bonus]
	return bonuses

class Model:
	def __init__(self, model):
		self.model = model
		self.checkModel()

	def __str__(self):
		for key in sorted(self.model.keys()):
			print key, self.model[key]

	def checkModel(self):
		print self.getValue("elemental resist")
		self.setValue("elemental resist", max(self.getValue("cold resist"), self.getValue("lightning resist"), self.getValue("fire resist"), self.getValue("electrocute resist"), self.getValue("frostburn resist"), self.getValue("burn resist")))

	def getValue(self, key):
		if key in self.model.keys():
			return self.model[key]
		else:
			return 0
	def setValue(self, key, value):
		self.model[key] = value


a = Affinity(0,0,1,1,0)
b = Affinity("3e 2o")


xC.stars[0].active = True
# spider.stars[0].active = True
fiend.stars[0].active = True
fiend.stars[1].active = True
fiend.stars[2].active = True
fiend.stars[3].active = True
print getBonuses()

for s in getAvailableStars():
	print s

def evaluateBonuses(model, bonuses):
	value = 0
	for bonus in model.keys():
		if bonus in bonuses.keys():
			value += model[bonus]*bonuses[bonus]
	return value


# print evaluateBonuses(model, getBonuses())

# print spider.evaluate(model)
# print fiend.evaluate(model)
# print fiend.stars[0].evaluate(model)

# search methodology:
# I think it needs to be depth first because only a complete solution has value since I'm looking for optimal endgame.
# I'm not ready to consider both activating and refunding stars. This complicates things but I think it's required for an optimal solution.
# I don't know how to branch and bound because there could be lots of valueless steps in a path building requirements that ends up optimal.
# I don't think I can search the entire space.
# I think I'm going to have to build a fair amount of a priori knowledge into the search. This will probably result in "obvious" decent solutions early but push less obvious potentially more optimal solutions later.
	# I could evaluate constelations as a whole to prioritize solutions but I may want less valuable constellations if they're efficient for affinity requirements
	# However, if a constellation has no/low value and the high value constellations don't require what it provides I can prune it from the search space. This may cascade into a vastly reduced search space.
		# I think it makes sense to work from value down.
		#  Evaluate constellations and sort and process in order
		#  	Anything that provides something I need is marked as valuable and evaluated.
		#     Anything that provides something I need....
		# Repeat until I run out of constellations or I hit one below the threshold. All unmarked constellations are useless.
# If I approach this treating contellations as whole entities and trim the space as above for initial pass I think I may be able to evaluate the whole space.

# constellationRanks = []
# for c in Constellation.constellations:
# 	constellationRanks += [(c.name, c.evaluate(model))]
# print sorted(constellationRanks, key=itemgetter(1), reverse=True)

def getNeededConstellations(wanted, currentAffinity=Affinity(0)):
	needed = []
	for w in wanted:
		for c in Constellation.constellations:
			if w.needs(c, currentAffinity) and not c in needed:
				needed.append(c)
	return needed

# print tsunami
# for c in getNeededConstellations([tsunami]):
# 	print c

print "\n\n\n"

bonuses = {}
for c in Constellation.constellations:
	for s in c.stars:
		for bonus in s.bonuses.keys():
			bonuses[bonus] = True

# for bonus in sorted(bonuses.keys()):
# 	print bonus

model = Model({"cold %":1, "fire %":2})

print model
model.checkModel()
