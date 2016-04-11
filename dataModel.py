import re
from operator import *
from time import time

methodTimes = {}
def timeMethod(label, startTime):
	if label in methodTimes.keys():
		methodTimes[label] += time()-startTime
	else:
		methodTimes[label] = time()-startTime

primaryDamages = [
	"acid",
	"aether", 
	"bleed", 
	"fire",
	"chaos", 
	"lightning",
	"elemental", 
	"cold",
	"physical",
	"pierce",
	"vitality",
	"life leech"
]

damages = [
	"acid", "poison",
	"aether", 
	"bleed", 
	"fire", "burn", 
	"chaos", 
	"lightning", "electrocute", 
	"elemental", 
	"cold", "frostburn", 
	"physical", "internal",
	"pierce",
	"vitality", "vitality decay",
	"life leech"
]

durationDamages = [
	"bleed",
	"poison",
	"burn",
	"electrocute",
	"frostburn",
	"internal",
	"vitality decay"
]

retaliations = [
	"chaos retaliation", 
	"life leech retaliation", 
	"pierce retaliation", 
	"vitality decay retaliation", 
	"physical retaliation", 
	"bleed retaliation"
]

resists = [
	"physical resist", 
	"fire resist", 
	"cold resist", 
	"lightning resist", 
	"acid resist", 
	"acid resist", 
	"vitality resist", 
	"pierce resist", 
	"aether resist", 
	"chaos resist",
	"bleed resist"
]

class Model:	
	def __init__(self, bonuses, stats):
		self.bonuses = bonuses
		self.stats = stats

		self.seedSolutions = []

	def __str__(self):
		out = ""
		for key in sorted(self.bonuses.keys()):
			if self.get(key) > 0:
				out += key + " " + str(self.bonuses[key]) + "\n"
		return out

	def checkModel(self):
		print "Checking model..."
		if not "fight length" in self.stats.keys():
			self.stats["fight length"] = 30

		self.stats["criticals/s"] = self.getStat("attacks/s")*self.getStat("crit chance")


		# physique grants health/s, health and defense so this should be accounted for
		val = 0
		val += self.get("health/s") * .04
		val += self.get("health") * 3
		val += self.get("defense") * .5

		self.set("physique", max(self.get("physique"), val))
		print "  Physique:", self.get("physique")

		# cunning grants physical %, pierce %, bleed %, internal % and offense.
		val = 0
		val += self.get("physical %") * .33
		val += self.get("pierce %") * .285
		val += self.get("bleed %") * .333
		val += self.get("internal %") * .333
		val += self.get("offense") * .5

		self.set("cunning", max(self.get("cunning"), val))
		print "  Cunning:", self.get("cunning")

		# spirit grants fire %, burn %, cold %, frostburn %, lightning %, electrocute %, acid %, poison %, vitality %, vitality decay%, aether %, chaos %, energy and energy regen
		val = 0
		val += sum([self.get(b) for b in ["elemental %", "acid %", "vitality %", "aether %", "chaos %"]]) * .33
		val += sum([self.get(b) for b in ["burn %", "frostburn %", "electrocute %", "poison %", "vitality decay %"]]) * .333
		val += self.get("energy") * 2
		val += self.get("energy/s") * .01

		self.set("spirit", max(self.get("spirit"), val))
		print "  Spirit:", self.get("spirit")

		#check stats vs % stats
		percStats = ["physique", "cunning", "spirit", "offense", "defense", "health", "energy", "armor"]
		for stat in percStats:
			self.set(stat+" %", self.getStat(stat) * self.get(stat) / 100)
			print "  " + stat + " %: " + str(self.get(stat+" %"))

		#check resist reduction
		# I'm assuming 20% resistance for the purposes of calculating value.
		# at that resistance each point of resist reduction resulst in 1.33% more overall damage.
		# if we have +400% vitality damage (500% total) a 1 percent reduction in resist is worth
		# 500*.0133 vitality % or 6.65 %
		# Testing against dummy is giving me 7.5 increased damage for -10% resist. Using that
		for damage in primaryDamages:
			if self.get(damage+" %") > 0:
				self.set("reduce "+damage+" resist", self.getStat(damage+" %")*.0075*self.get(damage+" %"))
				print "  reduce "+damage+" resist: " + str(self.get("reduce "+damage+" resist"))

		# handle shorthand sets: retaliation, resist	
		# retaliation types
		for b in retaliations:
			self.set(b, max(self.get(b), self.get("retaliation")))
			self.set("pet "+b, max(self.get("pet "+b), self.get("pet retaliation")))

		#resist types
		for b in resists:
			self.set(b, max(self.get(b), self.get("resist")))
			self.set("pet "+b, max(self.get("pet "+b), self.get("pet resist")))

			self.set("reduce "+b, max(self.get("reduce "+b), self.get("reduce resist")))
		for b in resists:
			self.set("reduce resist", max(self.get("reduce resist"), self.get("reduce "+b)))


		# elemental damage % and resist should be the sum of the individual components
		self.set("elemental %", max(self.get("elemental %"), sum([self.get(b) for b in ["cold %", "lightning %", "fire %"]])))
		print "  elemental %:", self.get("elemental %")

		# elemental resists are weird. e.g. fire resist protects against burn and elemental resist protects against fire but elemental resist does not protect against burn
		self.set("elemental resist", max(self.get("elemental resist"), sum([self.get(b) for b in ["cold resist", "lightning resist", "fire resist"]])))
		print "  elemental resist:", self.get("elemental resist")

		# all damage should be >= all other damage bonuses (sans retaliation)
		# don't count cold, lightning, or fire as they're already aggregated under elemental
		parts = ["acid %", "aether %", "bleed %", "burn %", "chaos %", "electrocute %", "elemental %", "frostburn %", "internal %", "physical %", "pierce %", "poison %", "vitality %", "vitality decay %"]
		self.set("all damage %", max(self.get("all damage %"), sum([self.get(b) for b in parts])))
		print "  all damage %:", self.get("all damage %")

		# catch all for flat damage of any type
		# triggered flat damage should be either specified manually or be equivalent to normal flat damage.
		# catch all for triggered damage of any type (no triggered damage is useless right?)		
		for damage in damages:
			# duration damage is counted for half
			factor = 1
			if damage in durationDamages:
				factor = .5

			self.set(damage, max(self.get(damage), self.get("damage")*factor))
			# pet flat damage?

			self.set("triggered "+damage, max([self.get("triggered "+damage), self.get(damage), self.get("triggered damage")*factor]))

		#nothing grants total speed

		self.filterConstellations()

	def filterConstellations(self):
		print "\n  Checking for weapon restricted constellations..."
		for c in self.blacklist:
			Constellation.constellations.remove(c)
			print "    -", c.name, "blacklisted "
		for c in Constellation.constellations[:]:
			if c.restricts:
				satisfied = False
				for weapon in self.getStat("weapons"):
					if weapon in c.restricts:
						satisfied = True
				if not satisfied:
					Constellation.constellations.remove(c)
					print "    -", c.name, "removed <-",str(c.requires)


	def get(self, key):
		if key in self.bonuses.keys():
			return self.bonuses[key]
		else:
			return 0
	def set(self, key, value):
		self.bonuses[key] = value

	def getStat(self, key):
		if key in self.stats.keys():
			return self.stats[key]
		else:
			return 0

class Affinity:
	def __init__(self, ascendant=0, chaos=0, eldritch=0, order=0, primordial=0):
		self.affinities = [0,0,0,0,0]

		if type(ascendant) == type(""):
			m = re.search("(\d+)+a", ascendant)
			if m:
				self.affinities[0] = int(m.group(1))

			m = re.search("(\d+)+c", ascendant)
			if m:
				self.affinities[1] = int(m.group(1))

			m = re.search("(\d+)+e", ascendant)
			if m:
				self.affinities[2] = int(m.group(1))

			m = re.search("(\d+)+o", ascendant)
			if m:
				self.affinities[3] = int(m.group(1))

			m = re.search("(\d+)+p", ascendant)
			if m:
				self.affinities[4] = int(m.group(1))
		else:
			self.affinities = [ascendant, chaos, eldritch, order, primordial]

	def magnitude(self):
		return sum(self.affinities)

	def maxAffinities(self, other):
		m = Affinity()
		for i in range(len(self.affinities)):
			m.affinities[i] = max(self.affinities[i], other.affinities[i])
		return m

	def intersects(self, other):
		for i in range(len(self.affinities)):
			if self.affinities[i] > 0 and other.affinities[i] > 0:
				return True
		return False

	def __eq__(self, other):
		for i in range(len(self.affinities)):
			if self.affinities[i] != other.affinities[i]:
				return False
		return True
	def __gt__(self, other):
		for i in range(len(self.affinities)):
			if self.affinities[i] == 0 and other.affinities[i] == 0:
				continue
			if self.affinities[i] <= other.affinities[i]:
				return False
		return True
	def __ge__(self, other):
		for i in range(len(self.affinities)):
			if self.affinities[i] == 0 and other.affinities[i] == 0:
				continue
			if self.affinities[i] < other.affinities[i]:
				return False
		return True
	def __lt__(self, other):
		for i in range(len(self.affinities)):
			if self.affinities[i] == 0 and other.affinities[i] == 0:
				continue
			if self.affinities[i] >= other.affinities[i]:
				return False
		return True
	def __le__(self, other):
		for i in range(len(self.affinities)):
			if self.affinities[i] == 0 and other.affinities[i] == 0:
				continue
			if self.affinities[i] > other.affinities[i]:
				return False
		return True

	def __add__(self, other):
		a = Affinity()
		for i in range(len(self.affinities)):
			a.affinities[i] = self.affinities[i] + other.affinities[i]
		return a

	def __sub__(self, other):
		a = Affinity()
		for i in range(len(self.affinities)):
			a.affinities[i] = max(self.affinities[i] - other.affinities[i], 0)
		return a

	def __str__(self):
		out = ""
		sh = ["a", "c", "e", "o", "p"]
		for i in range(len(self.affinities)):
			out += str(self.affinities[i]) + sh[i] + " "
		return out

class Ability:
	def __init__(self, name, conditions, bonuses):
		self.name = name		
		self.bonuses = bonuses

		self.conditions = conditions
		#Conditions
		# type:[buff, attack, heal, shield]
		# trigger:[attack,critical,hit,block]
		# chance:[0-1]
		# recharge:[seconds]
		# duration:[seconds]
		# targets[number of things an attack will likely hit]

		self.triggerTime = 0
		self.effective = 0		

	def gc(self, key):
		if key in self.conditions.keys():
			return self.conditions[key]
		else:
			return 0

	def gb(self, key):
		if key in self.bonuses.keys():
			return self.bonuses[key]
		else:
			return 0

	def calculateEffective(self, model):
		self.calculateTriggerTime(model)

		targets = max(1, self.gc("targets"))
		if self.gc("type") == "buff":
			self.effective = self.getUpTime(model)*targets
		elif self.gc("type") == "attack":
			# normalized around 2 attacks per second. If I use actual attack speed we get inverse calculated value to actual value. ie triggered attacks are more valuable to people who attack a lot but dividing by number of attacks devalues it
			self.effective = self.getNumTriggers(model)/(2.0*model.getStat("fight length"))*targets

			# print "nt", self.getNumTriggers(model)

			interval = self.triggerTime+self.gc("recharge")
			for dam in durationDamages:
				if "triggered "+dam in self.bonuses.keys():
					if type(self.bonuses["triggered "+dam]) == type([]):
						damage, ticks = self.bonuses["triggered "+dam]
						if ticks < interval:
							self.bonuses["triggered "+dam] = damage*ticks
						else:
							self.bonuses["triggered "+dam] = damage*interval

			if "duration" in self.bonuses.keys():
				#find duration based elements (for attacks that include a debuff component)
				upTime = self.getUpTime(model)
				# print "up", upTime
				durationBonuses = self.bonuses["duration"]
				for bonus in durationBonuses.keys():
					self.bonuses[bonus] = durationBonuses[bonus]*upTime/self.effective*targets
				del self.bonuses["duration"]

		elif self.gc("type") == "shield":
			self.effective = self.getNumTriggers(model)
		elif self.gc("type") == "heal":
			# we're counting half effectiveness due to overheal
			self.effective = self.getNumTriggers(model)*.5
		elif self.gc("type") == "summon":
			self.effective = self.getUpTime(model)


	def calculateTriggerTime(self, model):
		triggerFrequency = model.getStat(self.gc("trigger")+"s/s")
		self.triggerTime = 1.0/triggerFrequency * 1.0/self.gc("chance")

	def getUpTime(self, model):
		up = 0.0
		fightRemaining = model.getStat("fight length") - self.triggerTime		
		while fightRemaining > 0:
			up += min(max(self.gc("duration"), self.gc("lifespan")), fightRemaining)
			fightRemaining -= max(self.gc("duration"), self.gc("recharge")) + self.triggerTime
		return up/model.getStat("fight length")

	def getNumTriggers(self, model):
		triggers = 0
		fightRemaining = model.getStat("fight length") - self.triggerTime
		while fightRemaining > 0:
			triggers += 1
			fightRemaining -= self.gc("recharge") + self.triggerTime

		triggers = max(triggers, 1) # this will usually catch low health events which don't happen often. We'll calculate stats as if they happen once a fight.

		return triggers

	def calculateDynamicBonuses(self, model):
		damages = [
			"acid", "poison",
			"aether", 
			"bleed", 
			"fire", "burn", 
			"chaos", 
			"lightning", "electrocute", 
			"elemental", 
			"cold", "frostburn", 
			"physical", "internal",
			"pierce",
			"vitality", "vitality decay",
			"life leech"
		]
		if "attack as health %" in self.bonuses.keys():
			totalDamage = 0
			for dam in damages:
				if "triggered "+dam in self.bonuses.keys():
					totalDamage += self.bonuses["triggered "+dam]*model.getStat(dam+" %")*self.bonuses["attack as health %"]/100/100.0

			if "health" in self.bonuses.keys():
				self.bonuses["health"] += totalDamage
			else:
				self.bonuses["health"] = totalDamage

		if self.gc("type") == "attack":
			for dam in damages:
				# % damage depends on a weapon component and a flat damage component to be meaningful
				# technically it could depend on a triggered component of the spell as well but I don't think that scenario exists.
				# actually I think only targo's hammer is an attack ability with a %damage increase.
				if dam+" %" in self.bonuses.keys():
					if model.getStat(dam) <= 0:
						print "    " +self.name+" requires a defined internal damage _stat_ in the model."
					else:
						self.bonuses[dam] = self.gb(dam) + (self.model.getStat(dam) * self.gb("weapon %")/100.0 + self.gb(dam)) * self.gb(dam+" %")/100.0

		# armor reduction is like + physical damage that isn't affected by %damage
		if self.gb("reduce armor") > 0:
			if model.getStat("physical %") <= 0:
				print "    " +self.name+" requires a defined stat for physical %."
			else:
				self.bonuses["physical"] = self.gb("physical") + self.gb("reduce armor")*.7 / (model.getStat("physical %")/100.0)

		# handle damage that scales with pet damage
		for dam in damages:
			if self.gb("pet "+dam) > 0:
				if model.getStat("pet all damage %") == 0:
					print "    " +self.name+" requires a defined stat for pet all damage %."
				else:
					self.bonuses["triggered "+dam] = self.gb("triggered "+dam) + self.gb("pet "+dam)*model.getStat("pet all damage %")/100

	def calculateValue(self, model):

		self.calculateEffective(model)
		# print "Effective %:", self.name, self.effective

		self.calculateDynamicBonuses(model)
		
		self.star.bonuses[self.name] = 1
		for bonus in self.bonuses.keys():
			self.star.bonuses[bonus] = self.bonuses[bonus]*self.effective			

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

		self.name = ""

		self.ability = None
		self.value = None

		self.constellation.addStar(self)

	def __str__(self):
		return self.constellation.name + "." + str(self.constellation.stars.index(self)) + ": " + str(self.value)

	def canActivate(self, affinities):
		if self.active:
			return False
		for star in self.requires:
			if not star.active:
				return False
		if affinities < self.constellation.requires:
			return False
		return True

	def evaluate(self, model):
		if self.value != None:
			return self.value
		value = float(0)
		if self.ability != None:
			self.ability.calculateValue(model)
			# print self.ability.bonuses
		for bonus in model.bonuses.keys():
			if bonus in self.bonuses.keys():
				value += model.get(bonus)*self.bonuses[bonus]
		self.value = value
		return value

	# buffs
	#	relatively easy, estimate uptime times buff stats
	# heals/shields
	#	a heal for x is like having had x more health (unless you were already full)
	#   a shield for x is like having had x more health (if you're getting attacked (which if we weren't why would we care))
	#   estimate length of a fight times estimated how many times the thing will trigger time value of equivalent health
	# attacks
	#	much tricker.
	#   We're trying to gauge relative value so we'd want the value of the attack to be equivalent to adding a corresponding amount of damage
	#	this falls apart for casters since added flat damage isn't valuable but a triggered attack certainly could be
	#	Example:
	#		I'm a bleed based caster so % bleed damage is valuable but flat bleed damage is not (since I don't use weapon attacks)
	#			Now, there's an ability that triggers bleed damage. This would be very valuable to my kit.
	#		I'm a bleed based auto attacker so both %bleed and flat bleed are valuable.
	#			A triggered ability that caused bleed damage would still be valuable.
	#	I think we'll need an aggregated stat to handle it. "triggered bleed"
	#   % damage is a weird one because it applies to the weapon damage portion of an attack.
	#   In our bleed based melee build lets say we have a weapon that does massive bleed damage on attack. A triggered ability with % bleed damage and a weapon component might be pretty valuable. It's like the weapon damage component * the % damage * the flat damage number (not triggered) so if I value flat bleed at say 100 (for easy math) and my ability has a 30% weapon component and increases bleed damage by 40% I should value that stat at 100*40*.3 = 120

	def addAbility(self, ability, perc=0, bonuses={}):
		if type(ability) == type(""):			
			self.name = ability
			self.bonuses[self.name] = 1
			for bonus in bonuses.keys():
				self.bonuses[bonus] = bonuses[bonus]*perc
			self.constellation.abilities += [self]
		else:
			ability.star = self
			self.name = ability.name
			self.ability = ability	
			self.constellation.abilities += [self]

class Constellation:

	constellations = []	

	def __init__(self, name, requires, provides=Affinity()):
		self.name = name
		if type(requires) == type(""):
			self.requires = Affinity(requires)
		else:
			self.requires = requires

		if type(provides) == type(""):
			self.provides = Affinity(provides)
		else:
			self.provides = provides

		self.restricts = []
		self.stars = []
		self.abilities = []
		self.value = 0

		self.redundancies = []

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
		if self.value > 0:
			return self.value
		self.value = float(0)
		for star in self.stars:
			self.value += star.evaluate(model)

		return self.value

	def needs(self, other, current=Affinity()):
		# if I already have everything I need then I don't need the other
		if current >= self.requires:
			return False

		need = self.requires - current
		for i in range(len(need.affinities)):
			if need.affinities[i] > 0 and other.provides.affinities[i] > 0:
				return True

		return False

	def buildRedundancies(self, model):
		if self.requires.magnitude() > 1:
			return
		for c in Constellation.constellations:
			if c.requires.magnitude() > 1:
				continue
			if self.value < c.evaluate(model) and len(self.stars) >= len(c.stars) and self.provides <= c.provides:
				self.redundancies += [c]

	def canActivate(self, current=Affinity()):
		if not self.isComplete() and current >= self.requires:
			return True
		return False

	def activate(self):
		for s in self.stars:
			s.active = True
	def deactivate(self):
		for s in self.stars:
			s.active = False
