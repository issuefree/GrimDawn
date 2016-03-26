import re
from operator import *

def getAvailableStars():
	available = []
	for c in Constellation.constellations:
		for s in c.stars:
			if s.canActivate():
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

class Affinity:
	def __init__(self, ascendant=0, chaos=0, eldritch=0, order=0, primordial=0):
		self.ascendant = 0
		self.chaos = 0
		self.eldritch = 0
		self.order = 0
		self.primordial = 0

		if type(ascendant) == type(""):
			m = re.search("(\d)+a", ascendant)
			if m:
				self.ascendant = int(m.group(1))

			m = re.search("(\d)+c", ascendant)
			if m:
				self.chaos = int(m.group(1))

			m = re.search("(\d)+e", ascendant)
			if m:
				self.eldritch = int(m.group(1))

			m = re.search("(\d)+o", ascendant)
			if m:
				self.order = int(m.group(1))

			m = re.search("(\d)+p", ascendant)
			if m:
				self.primordial = int(m.group(1))
		else:
			self.ascendant = ascendant
			self.chaos = chaos
			self.eldritch = eldritch
			self.order = order
			self.primordial = primordial

	def __ge__(self, other):
		return self.ascendant >= other.ascendant and self.chaos >= other.chaos and self.eldritch >= other.eldritch and self.order >= other.order and self.primordial >= other.primordial
	def __lt__(self, other):
		return not self >= other


	def __add__(self, other):
		return Affinity(self.ascendant+other.ascendant, self.chaos+other.chaos, self.eldritch+other.eldritch, self.order+other.order, self.primordial+other.primordial)

	def __sub__(self, other):
		return Affinity(self.ascendant-other.ascendant, self.chaos-other.chaos, self.eldritch-other.eldritch, self.order-other.order, self.primordial-other.primordial)

	def __str__(self):
		return "" + str(self.ascendant) + "a " + str(self.chaos) + "c " + str(self.eldritch) + "e " + str(self.order) + "o " + str(self.primordial) + "p"

class Star:
	def __init__(self, constellation, requires=[], bonuses={}):
		self.constellation = constellation

		#array of stars
		if type(requires) != type([]):
			self.requires = [requires]
		else:
			self.requires = requires 

		self.active = False
		self.bonuses = bonuses

		self.constellation.addStar(self)

	def __str__(self):
		return self.constellation.name + "." + str(self.constellation.stars.index(self))

	def canActivate(self):
		if self.active:
			return False
		for star in self.requires:
			if not star.active:
				return False
		if getAffinities() < self.constellation.requires:
			return False
		return True

	def evaluate(self, model):
		value = 0
		for bonus in model.keys():
			if bonus in self.bonuses.keys():
				value += model[bonus]*self.bonuses[bonus]
		return value

class Constellation:

	constellations = []	

	def __init__(self, name, requires, provides):
		self.name = name
		if type(requires) == type(""):
			self.requires = Affinity(requires)
		else:
			self.requires = requires

		if type(provides) == type(""):
			self.provides = Affinity(provides)
		else:
			self.provides = provides

		self.stars = []		

		Constellation.constellations += [self]

	def __str__(self):
		return self.name + ": (" + str(self.requires) + ")  (" + str(self.provides) + ")"

	def isComplete(self):
		for star in self.stars:
			if not star.active:
				return False
		return True

	def addStar(self, star):
		self.stars += [star]

	def evaluate(self, model):
		value = 0
		for star in self.stars:
			value += star.evaluate(model)
		return value

	def needs(self, other, current=Affinity()):
		# if I already have everything I need then I don't need the other
		if current >= self.requires:
			return False

		need = self.requires - current
		if need.ascendant > 0 and other.provides.ascendant > 0:
			return True
		if need.chaos > 0 and other.provides.chaos > 0:
			return True
		if need.eldritch > 0 and other.provides.eldritch > 0:
			return True
		if need.order > 0 and other.provides.order > 0:
			return True
		if need.primordial > 0 and other.provides.primordial > 0:
			return True

		return False




a = Affinity(0,0,1,1,0)
b = Affinity("3e 2o")

xA = Constellation("Crossroads Ascendant", "", "1a")
Star(xA, [], {"offense":15})
xC = Constellation("Crossroads Chaos", "", "1c")
Star(xC, [], {"health %":5})
xE = Constellation("Crossroads Eldrich", "", "1e")
Star(xE, [], {"offense":15})
xO = Constellation("Crossroads Order", "", "1o")
Star(xO, [], {"health %":5})
xP = Constellation("Crossroads Primordial", "", "1p")
Star(xP, [], {"defense":15})

tsunami = Constellation("Tsunami", "1p", "5p")
a = Star(tsunami, [], {"lightning %": 15, "cold %":15})
b = Star(tsunami, a, {"spirit":10})
c = Star(tsunami, b, {"electrocute %":40, "frostburn %":40})
d = Star(tsunami, c, {"lightning %":24, "cold %":24})
e = Star(tsunami, d, {"Tsunami":True})

spider = Constellation("Spider", "1e", "6e")
a = Star(spider, [], {"cunning":10, "spirit":10})
b = Star(spider, a, {"offense":10})
c = Star(spider, a, {"offense":15, "defense":10})
d = Star(spider, a, {"cunning %":3, "spirit %":3})
e = Star(spider, a, {"cast speed %": 3})

fiend = Constellation("Fiend", "1c", "3c 3e")
a = Star(fiend, [], {"fire %":15, "chaos %":15})
b = Star(fiend, a, {"spirit":10})
c = Star(fiend, b, {}) # MISSING BONUS
d = Star(fiend, c, {"fire %":24, "chaos %":24})
e = Star(fiend, d, {"Flame Torrent":True})

hydra = Constellation("Hydra", "3a 3c 5e", "2c 3e")
a = Star(hydra, [], {"offense":15})
b = Star(hydra, a, {"all damage %":15})
c = Star(hydra, b, {"pierce %": 40})
d = Star(hydra, b, {"offense":20})
e = Star(hydra, d, {"offense %":3, "slow resist %":20})
f = Star(hydra, b, {"all damage %":35})

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

model = {"offense":1, "fire %":2}

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

constellationRanks = []
for c in Constellation.constellations:
	constellationRanks += [(c.name, c.evaluate(model))]
print sorted(constellationRanks, key=itemgetter(1), reverse=True)

def getNeededConstellations(wanted, currentAffinity=Affinity(0)):
	needed = []
	for w in wanted:
		for c in Constellation.constellations:
			if w.needs(c, currentAffinity) and not c in needed:
				needed.append(c)
	return needed

for c in getNeededConstellations([tsunami]):
	print c

