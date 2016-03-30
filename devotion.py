from time import time
from constellationData import *

methodTimes = {}
def timeMethod(label, startTime):
	if label in methodTimes.keys():
		methodTimes[label] += time()-startTime
	else:
		methodTimes[label] = time()-startTime



def getAvailableStars(constellations=Constellation.constellations):
	start = time()
	available = []
	for c in constellations:
		for s in c.stars:
			if s.canActivate(getAffinities()):
				available += [s]
	timeMethod("getAvailableStars", start)
	return available

def getAvailableConstellations(constellations=Constellation.constellations, affinities=Affinity()):
	start = time()
	available = []
	for c in constellations:
		if c.canActivate(affinities):
			available.append(c)
	timeMethod("getAvailableConstellations", start)
	return available

# cache if performance becomes an issue
def getAffinities():
	start = time()
	affinities = Affinity()
	for c in Constellation.constellations:
		if c.isComplete():
			affinities += c.provides
	timeMethod("getAffinities", start)
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

def sortConstellations(constellations, model):
	start = time()
	list = sorted(constellations, key=lambda c: c.evaluate(model), reverse=True)
	timeMethod("sortConstellations", start)
	return list


class Model:
	def __init__(self, model):
		self.model = model
		self.checkModel()

	def __str__(self):
		out = ""
		for key in sorted(self.model.keys()):
			if self.get(key) > 0:
				out += key + " " + str(self.model[key]) + "\n"
		return out

	def checkModel(self):
		# handle shorthand sets: retaliation, resist	
		# retaliation types
		retaliations = [
			"chaos retaliation", 
			"life leech retaliation", 
			"pierce retaliation", 
			"vitality decay retaliation", 
			"physical retaliation", 
			"bleed retaliation"
		]
		for b in retaliations:
			self.set(b, max(self.get(b), self.get("retaliation")))
			self.set("pet "+b, max(self.get("pet "+b), self.get("pet retaliation")))

		#resist types
		resists = [
			"physical resist", 
			"fire resist", 
			"cold resist", 
			"lightning resist", 
			"acid resist", 
			"poison resist", 
			"vitality resist", 
			"pierce resist", 
			"aether resist", 
			"chaos resist"
		]
		for b in resists:
			self.set(b, max(self.get(b), self.get("resist")))
			self.set("pet "+b, max(self.get("pet "+b), self.get("pet resist")))


		# elemental damage % and resist should be the sum of the individual components
		self.set("elemental %", max(self.get("elemental %"), sum([self.get(b) for b in ["cold %", "lightning %", "fire %"]])))

		# elemental resists are weird. e.g. fire resist protects against burn and elemental resist protects against fire but elemental resist does not protect against burn
		self.set("elemental resist", max(self.get("elemental resist"), sum([self.get(b) for b in ["cold resist", "lightning resist", "fire resist"]])))

		# all damage should be >= all other damage bonuses (sans retaliation)
		# don't count cold, lightning, or fire as they're already aggregated under elemental
		parts = ["acid %", "aether %", "bleed %", "burn %", "chaos %", "electrocute %", "elemental %", "frostburn %", "internal %", "physical %", "pierce %", "poison %", "vitality %"]
		self.model["all damage %"] = max(self.get("all damage %"), sum([self.get(b) for b in parts]))

		#nothing grants total speed

		# physique grants health/s, health and defense so this should be accounted for
		val = 0
		val += self.get("health/s") * .04
		val += self.get("health") * 3
		val += self.get("defense") * .5

		self.model["physique"] = max(self.get("physique"), val)

		# cunning grants physical %, pierce %, bleed %, internal % and offense.
		val = 0
		val += self.get("physical %") * .33
		val += self.get("pierce %") * .285
		val += self.get("bleed %") * .333
		val += self.get("internal %") * .333
		val += self.get("offense") * .5

		self.model["cunning"] = max(self.get("cunning"), val)

		# spirit grants fire %, burn %, cold %, frostburn %, lightning %, electrocute %, acid %, poison %, vitality %, vitality decay%, aether %, chaos %, energy and energy regen
		val = 0
		val += sum([self.get(b) for b in ["elemental %", "acid %", "vitality %", "aether %", "chaos %"]]) * .33
		val += sum([self.get(b) for b in ["burn %", "frostburn %", "electrocute %", "poison %", "vitality decay %"]]) * .333
		val += self.get("energy") * 2
		val += self.get("energy/s") * .01

		self.model["spirit"] = max(self.get("spirit"), val)

	def get(self, key):
		if key in self.model.keys():
			return self.model[key]
		else:
			return 0
	def set(self, key, value):
		self.model[key] = value



# xC.stars[0].active = True
# # spider.stars[0].active = True
# fiend.stars[0].active = True
# fiend.stars[1].active = True
# fiend.stars[2].active = True
# fiend.stars[3].active = True
# # print getBonuses()

def evaluateBonuses(model, bonuses):
	value = 0
	for bonus in model.keys():
		if bonus in bonuses.keys():
			value += model[bonus]*bonuses[bonus]
	return value

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


def getNeededConstellations(wanted, currentAffinity=Affinity(0)):
	start = time()
	needed = wanted[:]
	for c in Constellation.constellations:
		if not c in needed and not c.isComplete():
			for w in wanted:
				if w.needs(c, currentAffinity):
					needed.append(c)
					break
	timeMethod("getNeededConstellations", start)
	return needed

# print tsunami
# for c in getNeededConstellations([tsunami]):
# 	print c

bonuses = {}
for c in Constellation.constellations:
	for s in c.stars:
		for bonus in s.bonuses.keys():
			bonuses[bonus] = True

# for bonus in sorted(bonuses.keys()):
# 	# if bonus.find("retaliation") >= 0:
# 	print bonus

model = Model({
	"spirit":12.5, "spirit %":100,
	"offense":10, "offense %":150, 
	"crit damage":3,
	"vitality %":10, 
	"chaos %":2.5, 
	"cast speed":5,
	"defense":5, "defense %":50, 
	"armor":3, "armor %":8, "armor absorb":10,
	"health":.5, "health %":25,
	"avoid melee":5, "avoid ranged":7,
	"resist":7.5, "physical resist":20,
	"pet attack speed":1,
	"pet total speed":2,
	"pet lifesteal %":2,
	"pet all damage %":7.5,
	"pet defense %":1,
	"pet resist":1.5,
	"pet health %":5,
	"pet health/s":1,
	"pet retaliation":1, "pet retaliaion %":3,

	"Shepherd's Call":50,
	"Twin Fangs":75,
	"Guardian's Gaze":25,
	"Dryad's Blessing":10,
	"Turtle Shell":15,
	"Fetid Pool":150,
	"Giant's Blood":25,
	"Bysmiel's Command":50,
	"Wayward Soul":25,
	"Raise the Dead":75,
	"Tip the Scales":150,
	"Eldritch Fire":50,
	"Wendigo's Mark":100,
	"Tainted Eruption":50,
	"Abominable Might":25,
	"Hungering Void":100,
	"Mogdrogen the Wolf":25
	})

# print model
# model.checkModel()
# print model

constellationRanks = []
for c in Constellation.constellations:
	constellationRanks += [(c, c.evaluate(model))]

thresh = 400
wanted = []
for c in sorted(constellationRanks, key=itemgetter(1), reverse=True):
	if c[1] > thresh:
		wanted += [c[0]]

# searchConstellations = getNeededConstellations(wanted)


def printSolution(solution, model):
	value = 0
	out = ""
	for c in solution:
		out += c.name + ", "
		value += c.evaluate(model)
	print value,":",out

def evaluateSolution(solution, model):
	value = 0
	for c in solution:
		value += c.evaluate(model)
	return value

# print len(searchConstellations)

bestScore = 0
bestSolution = []

searchConstellations = getNeededConstellations(wanted)
def doMove(points, constellation=None, solution=[]):
	global bestScore, bestSolution
	if constellation:
		constellation.activate()
		# print "+"+constellation.name
		points -= len(constellation.stars)
	searchConstellations = getNeededConstellations(wanted, getAffinities())
	nextMoves = sortConstellations(getAvailableConstellations(searchConstellations, getAffinities()), model)
	for move in nextMoves:
		if points >= len(move.stars):
			doMove(points, move, solution+[move])
	# printSolution(solution, model)
	score = evaluateSolution(solution, model)
	if score > bestScore:
		bestScore = score
		bestSolution = solution
		printSolution(solution, model)
	if constellation:
		constellation.deactivate()
		# print "-"+constellation.name
	# print methodTimes

doMove(50)
