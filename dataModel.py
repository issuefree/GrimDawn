import re
import copy
from operator import *
from time import time

import traceback

damages = [
	"acid", "poison",
	"aether", 
	"bleed", 
	"fire", "burn", 
	"chaos", 
	"lightning", "electrocute", 
	"cold", "frostburn", 
	"physical", "internal",
	"pierce",
	"vitality", "vitality decay",
	"life leech",

	"elemental", 
	"all damage"
]

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

durationDamages = [
	"bleed",
	"poison",
	"burn",
	"electrocute",
	"frostburn",
	"internal",
	"vitality decay"
]

magicalDamage = [
	"acid",
	"aether",
	"fire",
	"chaos",
	"lightning",
	"cold",
	"vitality",
	"life leech"
]

magicalDurationDamage = [
	"burn",
	"frostburn",
	"electrocute",
	"poison",
	"vitality decay"
]

physicalDamage = [
	"physical",
	"pierce"
]

physicalDurationDamage = [
	"bleed",
	"internal"
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
	"vitality resist", 
	"pierce resist", 
	"aether resist", 
	"chaos resist",
	"bleed resist"
]

elementals = [
	"cold",
	"fire",
	"lightning"
]

methodTimes = {}
def timeMethod(label, startTime):
	if label in methodTimes.keys():
		methodTimes[label] += time()-startTime
	else:
		methodTimes[label] = time()-startTime

class Affinity:
	sh = ["a", "c", "e", "o", "p"] # vectors
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

	# total sum of affinities
	def magnitude(self):
		return sum(self.affinities)

    # returns an affinity with the max values of each.
	def maxAffinities(self, other):
		a = Affinity()
		for i in range(len(self.affinities)):
			a.affinities[i] = max(self.affinities[i], other.affinities[i])
		return a

	# returns an affinity with the min values of each.
	def minAffinities(self, other):
		a = Affinity()
		for i in range(len(self.affinities)):
			a.affinities[i] = min(self.affinities[i], other.affinities[i])
		return a

    # returns true if both affinities have value in any category
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

	def __mul__(self, other):		
		a = Affinity()
		if type(other) == type(1.0):
			for i in range(len(self.affinities)):
				a.affinities[i] = self.affinities[i]*other
		elif type(other) == type(self):
			for i in range(len(self.affinities)):
				a.affinities[i] = self.affinities[i]*other.affinities[i]
		return a


	def __div__(self, other):
		a = Affinity()
		if type(other) == type(1.0):
			for i in range(len(self.affinities)):
				a.affinities[i] = self.affinities[i]/other
		elif type(other) == type(self):
			for i in range(len(self.affinities)):
				a.affinities[i] = self.affinities[i]/other.affinities[i]
		return a

	def __str__(self):
		out = ""		
		for i in range(len(self.affinities)):
			out += str(self.affinities[i]) + Affinity.sh[i] + " "
		return out

	# a vector is one type of affinity or an affinity set that provides only one type.
	def isVector(self, vector=None):
		if self.magnitude() == 0:
			return False

		if not vector:			
			for i in range(len(self.affinities)):
				if self.affinities[i] != 0 and self.affinities[i] != self.magnitude():
					return False
			return True

		if self.magnitude() == self.get(vector):
			return True
		return False

	def set(self, ac, val):
		self.affinities[Affinity.sh.index(ac)] = val
	def get(self, ac):
		return self.affinities[Affinity.sh.index(ac)]

class Ability:
	minTriggerTime = .25  # there are gaps between skills etc

	def __init__(self, name, conditions, bonuses):
		self.name = name		
		self.bonuses = bonuses

		self.dynamicBonuses = {}

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

		self.star = None

	def copy(self):
		return Ability(self.name, copy.deepcopy(self.conditions), copy.deepcopy(self.bonuses))

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

	def getTotalBonus(self, key):
		value = 0
		if key in self.bonuses.keys():
			if type(self.bonuses[key]) == type([]) and value == 0:
				value = self.bonuses[key]
			else:
				# print self.name
				# print self.bonuses
				# print key
				# print value
				value += self.bonuses[key]
		if key in self.dynamicBonuses.keys():
			if type(self.dynamicBonuses[key]) == type([]) and value == 0:
				value = self.dynamicBonuses[key]
			else:
				value += self.dynamicBonuses[key]
		return value

	def calculateEffective(self, model, verbose=False):
		self.calculateTriggerTime(model, verbose)
		if self.triggerTime == -1:
			self.effective = 0
			return

		targets = max(1, self.gc("targets"))
		if self.gc("type") == "buff":
			self.effective = self.getUpTime(model)*targets
			# print "buff uptime:", self.getUpTime(model)
		if self.gc("type") == "attack" or self.gc("type") == "aar":

			if self.gc("shape") == "???":
				print "    Shape unknown for", self.name

			if model.getStat("playStyle") == "ranged":
				# Characters who try to keep enemies as far away as possible. Often kiting.
				# Optimal range 10+ yards
				# Ground target abilities will often miss due to mobility.
				# Circle is strong due to it hitting the point of the enemy spear where most enemies will clump.
				# Cone/line abilities may not hit many enemies due to long range.
				# pbaoe abilities may be of limited value
				if self.gc("shape") == "cone" or self.gc("shape") == "line":
					targets = targets * .75
				elif self.gc("shape") == "ground":
					targets = targets * .5
				elif self.gc("shape") == "circle":
					pass
				elif self.gc("shape") == "pbaoe":
					targets = targets * .125
				elif self.gc("shape") == "melee":
					targets = targets * .05

			elif model.getStat("playStyle") == "shortranged":
				# Characters who have short ranged abilities and try to keep monsters from hittim him but kiting is minimal and mostly for the purposes of clumping.
				# 	Low mobility and close range tend to make crowd control common. Lots of slows and stuns.
				# Optimal range 5-10 yards
				# Ground target abilities are strong due to clumping and funneling.
				# Circle is strong due to clumping and funneling.
				# Cone/line abilities should have the desired effect.
				# pbaoe abilities aren't ideal if they're very short ranged.
				if self.gc("shape") == "cone" or self.gc("shape") == "line":
					pass
				elif self.gc("shape") == "ground":
					targets = targets * 1.25
				elif self.gc("shape") == "circle":
					targets = targets * 1.25
				elif self.gc("shape") == "pbaoe":
					targets = targets * .75
				elif self.gc("shape") == "melee":
					targets = targets * .1

			elif model.getStat("playStyle") == "melee":
				# Characters who engage in melee but aim to kill fast and minimize getting surrounded or take a beating.
				# Optimal range is melee but not surrounded.
				# Ground target abilities are strong due to melee range and not getting surrounded. 
				#	Mobility is required so value may be somewhat limited.
				# Circle is strong due to clumping.
				# Cone/Line abilities are ideal due to keeping enemies close but on one side.
				# pbaoe abilities are strong but not ideal due to trying not to get surrounded.
				if self.gc("shape") == "cone" or self.gc("shape") == "line":
					targets = targets * 1.33
				elif self.gc("shape") == "ground":
					pass
				elif self.gc("shape") == "circle":
					targets = targets * 1.25
				elif self.gc("shape") == "pbaoe":
					pass
				elif self.gc("shape") == "melee":
					pass

			elif model.getStat("playStyle") == "tank":
				# Characters who run into the fray and try to take hits. Often retaliation based.
				# Optimal range is all enemies up close and personal.
				# Ground target abilities are strong due to low mobility and enemy gathering. Not ideal as surrounding can spread them out.
				# Circle is strong due to clumping and gathering.
				# Cone/Line abilities are decent but similar to ground target, enemies can be spread in a lot of directions.
				# pbaoe are ideal.
				if self.gc("shape") == "cone" or self.gc("shape") == "line":
					pass
				elif self.gc("shape") == "ground":
					pass
				elif self.gc("shape") == "circle":
					pass
				elif self.gc("shape") == "pbaoe":
					targets = targets * 1.5
				elif self.gc("shape") == "melee":
					pass

			if self.gc("trigger") == "manual":
				self.bonuses["attack opportunity cost"] = 100/targets
				if self.gc("recharge") == 0:
					self.conditions["recharge"] = 1

			self.effective = self.getNumTriggers(model, verbose)*targets/model.getStat("fight length")

			if verbose:
				print "nt", self.getNumTriggers(model)

			if "duration" in self.bonuses.keys():
				self.setDebuffValue(targets, model)
			# TODO I've removed damage % modifiers from attack abilities as these are only supposed to affect the attack itself not all damage.
			# this needs to be fixed and this can be removed
			for damage in damages:
				if damage+" %" in self.bonuses.keys():
					del self.bonuses[damage+" %"]


			interval = self.triggerTime+self.gc("recharge")
			for dam in durationDamages:
				if "triggered "+dam in self.bonuses.keys():
					if type(self.gb("triggered "+dam)) == type([]):
						damage, ticks = self.bonuses["triggered "+dam]
						if ticks < interval:
							self.bonuses["triggered "+dam] = damage*ticks
						else:
							self.bonuses["triggered "+dam] = damage*interval
				
		if self.gc("type") == "shield":
			self.effective = self.getNumTriggers(model)
		if self.gc("type") == "heal":
			# we're counting half effectiveness due to overheal
			self.effective = self.getNumTriggers(model)*.5

			if "duration" in self.bonuses.keys():
				self.setDebuffValue(max(1, self.gc("targets")), model)

		if self.gc("type") == "summon":
			self.effective = self.getUpTime(model)

	def setDebuffValue(self, targets, model):
		#find duration based elements (for attacks that include a debuff component)
		upTime = self.getUpTime(model)
		# print "up", upTime
		durationBonuses = self.bonuses["duration"]
		for bonus in durationBonuses.keys():
			self.bonuses[bonus] = durationBonuses[bonus]*upTime/self.effective*targets
			#reduce duration based damage as the foe may die due to other effects durring the duration
			if bonus in ["triggered "+damage for damage in damages]:
				self.bonuses[bonus] = self.bonuses[bonus] / 2
		del self.bonuses["duration"]

	def calculateTriggerTime(self, model, verbose=False):
		if self.gc("trigger") == "manual" or self.gc("trigger") == "parent":
			self.triggerTime = Ability.minTriggerTime
			return
		if self.gc("trigger") == "toggle" or self.gc("trigger") == "passive":
			self.triggerTime = 0
			return
		if self.gc("type") == "aar":
			triggerFrequency = model.getStat("attacks/s")
		else:
			triggerFrequency = model.getStat(self.gc("trigger")+"s/s")
		if triggerFrequency == 0:
			self.triggerTime = -1
			return
		
		self.triggerTime = 1.0/triggerFrequency * 1.0/self.gc("chance")
		# print "tt", self.triggerTime

	#uptime is a percent so we'll use a scalar of fight length to get an average across multiple fights
	def getUpTime(self, model):
		if self.gc("trigger") == "toggle" or self.gc("trigger") == "passive":
			return 1
		up = 0.0
		fightLen = model.getStat("fight length")*5
		fightRemaining = fightLen - self.triggerTime		
		while fightRemaining >= 0:
			up += min(max(self.gc("duration"), self.gc("lifespan")), fightRemaining)
			fightRemaining -= max(self.gc("duration"), self.gc("recharge") + self.triggerTime) 
		return up/fightLen

	#average over a number of fights
	def getNumTriggers(self, model, verbose=False):
		numFights = 10.0
		triggers = 0
		fightRemaining = model.getStat("fight length")*numFights - self.triggerTime		
		while fightRemaining >= 0:
			triggers += 1
			fightRemaining -= self.gc("recharge") + self.triggerTime

		triggers = max(triggers, 1) # this will usually catch low health events which don't happen often. We'll calculate stats as if they happen once a fight.

		if verbose:
			print self.name, "getNumTriggers"
			print "   recharge", self.gc("recharge")
			print "   triggerTime", self.triggerTime
			print "   fight length", model.stats["fight length"]
			print "   total triggers", triggers
			print "   nt", triggers/numFights

		return triggers/numFights

	def calculateDynamicBonuses(self, model):
		self.dynamicBonuses = {}
		if "attack as health %" in self.bonuses.keys():
			totalDamage = 0
			for dam in damages:
				if "triggered "+dam in self.bonuses.keys():
					totalDamage += self.bonuses["triggered "+dam]*(model.getStat(dam+" %")+100)/100.0
			totalDamage = totalDamage*self.bonuses["attack as health %"]/100.0
			# count as half due to overheal
			if "health" in self.bonuses.keys():				
				self.dynamicBonuses["health"] += totalDamage
			else:
				self.dynamicBonuses["health"] = totalDamage


		if self.gc("type") == "attack":
			for dam in damages:
				# % damage depends on a weapon component and a flat damage component to be meaningful
				# technically it could depend on a triggered component of the spell as well but I don't think that scenario exists.
				# actually I think only targo's hammer is an attack ability with a %damage increase.
				if dam+" %" in self.bonuses.keys():
					if model.getStat(dam) <= 0:
						print "    " +self.name+" requires a defined " + dam + " _stat_ in the model."
					else:
						self.dynamicBonuses[dam] = (model.getStat(dam) * self.gb("weapon damage %")/100.0 + self.gb(dam)) * self.gb(dam+" %")/100.0

		if self.gc("type") == "aar":
			self.dynamicBonuses["weapon damage %"] = -100

		# armor reduction is like + physical damage that isn't affected by %damage
		if self.gb("reduce armor") > 0:
			if model.getStat("physical %") <= 0:
				print "    " +self.name+" requires a defined stat for physical %."
			else:
				self.dynamicBonuses["physical"] = self.gb("reduce armor")*.7 / (model.getStat("physical %")/100.0)

	def getBonuses(self, model):
		bonuses = {}
		self.calculateEffective(model)
		# print "Effective %:", self.name, self.effective

		self.calculateDynamicBonuses(model)

		# if the ability has been manually valued in the model
		modelFactor = 1
		if self.name in model.bonuses.keys():
			modelFactor = model.get(self.name)

		for bonus in self.bonuses.keys() + self.dynamicBonuses.keys():
			total = self.getTotalBonus(bonus)
			if type(total) == type([]):
				total = [total[0]*self.effective*modelFactor, total[1]]
			else:
				total = total*self.effective * modelFactor
			bonuses[bonus] = total
		return bonuses


	def calculateValue(self, model):
		self.calculateEffective(model)
		# print "Effective %:", self.name, self.effective

		self.calculateDynamicBonuses(model)
		
		# if the ability has been manually valued in the model
		modelFactor = 1
		if self.name in model.bonuses.keys():
			modelFactor = model.get(self.name)

		for bonus in self.bonuses.keys() + self.dynamicBonuses.keys():
			total = self.getTotalBonus(bonus)
			if type(total) == type([]):
				total = [total[0]*self.effective*modelFactor, total[1]]
			else:
				total = total*self.effective * modelFactor
			self.star.bonuses[bonus] = total
		self.star.bonuses[self.name] = 1

	def augment(self, ability, verbose=False):
		# augmenting abilities can affect conditions. Targets come to mind. I'm going to handle it as a one off for now.
		if "targets" in ability.conditions:
			self.conditions["targets"] = self.gc("targets") + ability.conditions["targets"]
		if "ability damage %" in ability.bonuses.keys():
			for damage in damages+["weapon damage %"]:
				if damage in self.bonuses.keys():
					if type(self.bonuses[damage]) == type([]):						
						self.bonuses[damage] = [self.bonuses[damage][0]*(1+ability.bonuses["ability damage %"]/100.0), self.bonuses[damage][1]]
					else:
						self.bonuses[damage] *= 1+ability.bonuses["ability damage %"]/100.0
			del ability.bonuses["ability damage %"]
		for bonus in ability.bonuses:
			if type(ability.bonuses[bonus]) == type([]):
				if bonus in self.bonuses.keys():					
					self.bonuses[bonus] = addDurationDamages(self.bonuses[bonus], ability.bonuses[bonus])
				else:
					self.bonuses[bonus] = ability.bonuses[bonus]
			elif type(ability.bonuses[bonus]) == type({}):
				if bonus in self.bonuses.keys():
					self.bonuses[bonus] = mergeBonuses(self.bonuses[bonus], ability.bonuses[bonus])
				else:
					self.bonuses[bonus] = ability.bonuses[bonus]
			else:
				if verbose:
					print bonus, self.gb(bonus)
				self.bonuses[bonus] = self.gb(bonus) + ability.bonuses[bonus]

class Star:
	def __init__(self, constellation, requires=[], bonuses={}):
		self.constellation = constellation

		self.requires = requires 

		self.bonuses = bonuses

		self.name = ""

		self.ability = None
		self.value = None

		self.constellation.addStar(self)

	def __str__(self):
		return self.constellation.name + "." + str(self.constellation.stars.index(self)) + ": " + str(self.value)

	def reset(self):
		self.value = None

	def evaluate(self, model=None):
		if self.value:
			return self.value
		value = float(0)
		if self.ability != None:
			self.ability.calculateValue(model)
		for bonus in model.bonuses.keys():
			if bonus in self.bonuses.keys():
				value += model.calculateBonus(bonus, self.bonuses[bonus])
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

		self.value = None
		self.apsValue = []

		self.redundancies = []
		self.conflicts = []

		self.index = len(Constellation.constellations)

		Constellation.constellations += [self]

	def __str__(self):
		return self.name + ": (" + str(self.requires) + ")  (" + str(self.provides) + ")"

	def addStar(self, star):
		self.stars += [star]

	def reset(self):
		self.value = None
		for star in self.stars:
			star.value = None

	def hasAttackTrigger(self):
		for star in self.abilities:
			if star.ability.gc("trigger") == "attack" or star.ability.gc("trigger") == "critical":
				return True
		return False

	def evaluate(self, model=None, apsIndex=0):
		if self.value:
			if not self.hasAttackTrigger():
				return self.value
			else:
				if apsIndex >= len(self.apsValue):
					return 0
				return self.apsValue[apsIndex]
		if self in model.getStat("blacklist"):
			self.value = float(0)
			return self.value
		self.value = float(0)
		for star in self.stars:
			self.value += star.evaluate(model)
		if self.hasAttackTrigger():
			self.apsValue = [0]*len(model.getStat("allAttacks/s"))
			for i in range(len(model.getStat("allAttacks/s"))-1, -1, -1):
				apsModel = copy.deepcopy(model)
				apsModel.stats["attacks/s"] = apsModel.stats["allAttacks/s"][i]
				for star in self.stars:
					star.reset()
					self.apsValue[i] += star.evaluate(apsModel)
			if apsIndex >= len(self.apsValue):
				return 0
			return self.apsValue[apsIndex]
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

	def isBetter(self, other, model):
		if len(self.stars) <= len(other.stars) and self.evaluate(model) >= other.evaluate(model) and self.provides >= other.provides:
			if len(self.stars) == len(other.stars) and self.evaluate(model) == other.evaluate(model) and self.provides == other.provides:
				return False
			else:
				return True
		return False

	def isWorse(self, other, model):
		if len(self.stars) >= len(other.stars) and self.evaluate(model) <= other.evaluate(model) and self.provides <= other.provides:
			if len(self.stars) == len(other.stars) and self.evaluate(model) == other.evaluate(model) and self.provides == other.provides:
				return False
			else:
				return True
		return False

	def buildRedundancies(self, model):		
		if self.getTier() > 1:
			return
		for c in Constellation.constellations:
			if c.getTier() > 1:
				continue
			if self.value < c.evaluate(model) and len(self.stars) >= len(c.stars) and self.provides <= c.provides:
				self.redundancies += [c]

	def canActivate(self, affinities=Affinity(), current=[]):
		if affinities >= self.requires:
			for conflict in self.conflicts:
				if conflict in current:
					return False
			return True
		return False

	def addConflicts(self, others):
		for i in range(len(others)):
			other = others[i]
			self.conflicts += [other]
			other.conflicts += [self]			
			other.addConflicts(others[i+1:])

	# tier 0: a crossroards constellation
	# tier 1: just like the game defines: requires 1 affinity, provides many affinity.
	# tier 2: requires many affinity, provides few affinity.
	# tier 3: requires many affinity, provides NO affinity.
		# desired subconstellations count as t3 since they provide nothing. They're just "weak" tier 3.
	def getTier(self):
		# in theory this is static but if I manipulate the provides or requires this might change and cause unpredictable results.
		if self.requires.magnitude() == 0:
			return 0

		if self.provides.magnitude() == 0:
			return 3

		if self.requires.magnitude() == 1:
			return 1

		return 2

class Item:
	armorLocationFactor = {
		"head":.15,
		"shoulders":.15,
		"chest":.26,
		"arms":.12,
		"legs":.20,
		"feet":.12
	}

	meleeLocations = [
		"sword", 
		"axe", 
		"mace",
		"scepter",
		"dagger", 
		"twohand"
	]
	rangedLocations = [
		"pisol",
		"crossbow",
		"rifle"
	]
	weaponLocations = meleeLocations + rangedLocations

	@staticmethod
	def getByLocation(location, items):
		locItems = []
		for item in items:
			if not location or location in item.location:
				locItems += [item]
		return locItems

	@staticmethod
	def getByName(name, items):
		for item in items:
			if item.name == name:
				return item
		return 1/0

	def __init__(self, name, bonuses, location, ability=None):
		self.name = name
		self.bonuses = bonuses

		if "armor" in bonuses.keys() and location and location in Item.armorLocationFactor.keys():
			self.bonuses["armor"] = bonuses["armor"]*Item.armorLocationFactor[location]

		self.location = location
		self.ability = ability

		self.value = 0

	def __str__(self):
		return self.name

	def evaluate(self, model, location=None, verbose=False):
		if verbose:
			print self.name

		abilityBonuses = {}
		if self.ability:
			if self.ability.gc("shape") == "weapon":
				if location in Item.meleeLocations:
					self.ability.conditions["shape"] = "melee"
			self.ability.calculateEffective(model, verbose)
			self.ability.calculateDynamicBonuses(model, verbose)
			for bonus in self.ability.bonuses.keys() + self.ability.dynamicBonuses.keys():
				abilityBonuses[bonus] = self.ability.getTotalBonus(bonus)*self.ability.effective

		value = 0
		for bonus in model.bonuses.keys():
			if bonus in self.bonuses.keys():
				keyBonus = self.bonuses[bonus]
				if verbose:
					print "  ", bonus.ljust(20), str(int(keyBonus)).ljust(5), int(model.get(bonus)*keyBonus)
				value += model.get(bonus)*keyBonus
			if bonus in abilityBonuses.keys():
				value += model.get(bonus)*abilityBonuses[bonus]
				if verbose:
					print "  ", bonus.ljust(20), str(int(abilityBonuses[bonus])).ljust(5), int(model.get(bonus)*abilityBonuses[bonus])
		self.value = value
		return value

class Skill:
	skills = {}
	skillsByClass = {}

	def __init__(self, name, profession, levels, parentSkillName=None):
		self.name = name		
		self.levels = levels
		self.maxLevel = levels[0]
		self.profession = profession
		self.parentSkillName = parentSkillName
		self.childSkills = []

		Skill.skills[name] = self
		if not profession in Skill.skillsByClass:
			Skill.skillsByClass[profession] = []
		Skill.skillsByClass[profession] += [name]

		if parentSkillName:
			Skill.skills[parentSkillName].addChildSkill(self)

	def getAbility(self, level, verbose=False):
		level = min(self.maxLevel, level)
		if verbose:
			print "getAbility", self.name, level
		if level > len(self.levels):
			print self.name, "undefined for level:", level
		ability = self.levels[level].copy()
		ability.name = self.name + "(" + ability.name + ")"
		if verbose:
			print ability.bonuses
		return ability

	def addChildSkill(self, skill):
		self.childSkills += [skill]

class Character:
	verbose = False

	def __init__(self, model, baseAttributes, skills, constellations, items, stats={}):
		self.results = {}
		self.model = model
		self.baseAttributes = baseAttributes

		self.skills = {}
		for skillLevel in skills:
			skill = skillLevel.keys()[0]
			self.skills[skill] = skillLevel[skill]

		self.stats = {}
		self.level = model.stats["level"]		
		self.difficulty = model.stats["difficulty"]
		self.stats["physique"] = baseAttributes[0]
		self.stats["cunning"] = baseAttributes[1]
		self.stats["spirit"] = baseAttributes[2]
		self.stats["health"] = baseAttributes[3]
		self.stats["energy"] = baseAttributes[4]
		
		self.setMaxes()

		self.setBaseStats(stats)

		self.constellations = constellations
		self.items = items

		for item in items:
			self.process(item.bonuses, [item.ability])

		for constellation in constellations:
			for star in constellation.stars:
				self.process(star.bonuses, [star.ability])


		for skillLevel in skills:
			skill = skillLevel.keys()[0]
			if not skill in Skill.skills.keys():
				print "Missing skill definition for:", skill
				continue

			skillDef = Skill.skills[skill]
			
			if skillDef.parentSkillName:
				# if a skill has a parent then it should be processed with the parent not on it's own
				continue

			level = self.getSkillLevel(skill)
			if Character.verbose:
				print skill, self.skills[skill], "->", level

			ability = Skill.skills[skill].getAbility(level)
			if Character.verbose:
				print ability.name
			abilities = [ability]

			#augment ability with any child skills
			for childSkill in skillDef.childSkills:
				childAbility = childSkill.getAbility(self.getSkillLevel(childSkill.name))

				if Character.verbose:
					print "  childAbility:", childSkill.name, "-", childAbility.name
					print "    "+str(childAbility.bonuses)
					print

				if childAbility.gc("type") == "modifier":
					ability.augment(childAbility)
					if Character.verbose:
						print "->", str(ability.bonuses)
				elif childAbility.gc("trigger") == "parent":
					childAbility.conditions["recharge"] = ability.gc("recharge")
					abilities += [childAbility]


			self.process({}, abilities)

		self.calcOADA()
		self.calcHealth()
		self.calcEnergy()
		self.calcBonusDamage()
		self.calcRegeneration()

		self.processMetaStats()

		self.calculateDamage()
		self.calculateEffectiveHealth()

	def getSkillLevel(self, skill):
		return self.skills[skill] + self.getStat(skill) + self.getStat(Skill.skills[skill].profession)

	def setMaxes(self):
		self.maxes = {
			"attack speed":200,
			"move speed":135,
			"cast speed":200,
			"block %":100,
			"armor absorb":100,		
		}
		for resist in resists:
			self.maxes[resist] = 80

	def setBaseStats(self, stats):
		self.stats["attack speed"] = 100
		self.stats["move speed"] = 100
		self.stats["cast speed"] = 100
		self.stats["block %"] = 0
		self.stats["health/s"] = 0
		self.stats["energy/s"] = 0
		self.stats["armor absorb"] = 70

		resistBase = self.difficulty*-25
		for resist in resists:
			self.stats[resist] = resistBase
		self.stats["physical resist"] = 0 #override

		for stat in stats:
			self.addToStat(stat, stats[stat])

	def calcOADA(self):
		self.addToStat("offense", 118 + (self.level*12) + self.stats["cunning"]*.5)
		self.addToStat("defense", 118 + (self.level*12) + self.stats["physique"]*.5)

	def calcHealth(self):
		self.addToStat("health", 250 + (self.stats["physique"]-50)*2.5)

	def calcEnergy(self):
		self.addToStat("energy", 250 + (self.stats["spirit"]-50)*2)

	def calcBonusDamage(self):
		self.addToStat("physical %", self.stats["cunning"]*.416)
		self.addToStat("pierce %", self.stats["cunning"]*.40)
		for damage in physicalDurationDamage:
			self.addToStat(damage + " %", self.stats["cunning"]*.46)
		for damage in magicalDamage:
			self.addToStat(damage + " %", self.stats["spirit"]*.47)
		for damage in magicalDurationDamage:
			self.addToStat(damage + " %", self.stats["spirit"]*.5)

	def calcRegeneration(self):
		self.addToStat("base health/s", (self.stats["physique"]-50)*.04)
		self.addToStat("base energy/s", 6.5+(self.stats["spirit"]-50)*.01)
		self.addToStat("energy/s %", self.stats["spirit"]*.26)


	def process(self, bonuses, abilities, verbose=False):
		if verbose:
			print "process"
			print "  bonuses", str(bonuses)
			print "  abilities"
			for ability in abilities:
				if ability != None:
					print "   ", ability.name, ability.bonuses
		for bonus in bonuses:
			if bonus.startswith("max ") and bonus.endswith(" resist"):
				self.maxes[bonus[4:]] += bonuses[bonus]

			self.addToStat(bonus, bonuses[bonus])
		for ability in abilities:
			if ability != None:
				ability.calculateEffective(self.model)
				if verbose:
					print "effective", ability.effective
				ability.calculateDynamicBonuses(self.model)
				for bonus in ability.bonuses.keys() + ability.dynamicBonuses.keys():
					totalBonus = ability.getTotalBonus(bonus)
					if type(totalBonus) == type([]):
						self.addToStat(bonus, [totalBonus[0]*ability.effective, totalBonus[1]])
					else:
						self.addToStat(bonus, totalBonus*ability.effective)

	# stats with a % equivalent. I.e. "physique %""
	metaPercs = [
		"physique",
		"cunning",
		"spirit",
		"health",
		"health/s",
		"energy",
		"energy/s",
		"armor",
		"offense",
		"defense",
		"blocked damage",		
	]

	def processMetaStats(self):
		baseAttackSpeed = self.stats["attacks/s"]/1.9775

		for perc in Character.metaPercs:
			if perc + " %" in self.stats:
				self.stats[perc] = self.stats[perc]*self.getStatPerc(perc + " %")
				# del self.stats[perc + " %"]

		if "elemental resist" in self.stats:
			for element in elementals:
				self.addToStat(element + " resist", self.stats["elemental resist"])
			del self.stats["elemental resist"]

		if "elemental %" in self.stats:
			for element in elementals:
				self.addToStat(element + " %", self.stats["elemental %"])
			del self.stats["elemental %"]

		if "all damage %" in self.stats:
			for damage in damages:
				self.addToStat(damage + " %", self.stats["all damage %"])
			del self.stats["all damage %"]

		if "retaliation %" in self.stats:
			for damage in damages:
				self.addToStat(damage + "retaliation %", self.stats["retaliation %"])
			del self.stats["retaliation %"]

		for maxStat in self.maxes:
			self.stats[maxStat] = min(self.stats[maxStat], self.maxes[maxStat])

		self.stats["attacks/s"] = self.stats["attacks/s"]*(self.stats["attack speed"]/100.0)
		self.stats["attack speed"] = baseAttackSpeed*self.stats["attack speed"]

		self.stats["health/s"] = self.stats["base health/s"] + self.stats["health/s"]
		del self.stats["base health/s"]		
		self.stats["energy/s"] = self.stats["base energy/s"] + self.stats["energy/s"] #TODO energy/s costs are currently recorded as -energy/s so energy/s % is applied to costs (which should be) so we get a lower regen than anticipated
		del self.stats["base energy/s"]

	def calculateDamage(self, verbose=False):
		dpa = {}
		triggered = {}
		# base values
		for damage in damages:
			dpa[damage] = self.getStat(damage)
			# TODO dunno what this's for
			# self.stats["triggered "+damage] = self.getStat("triggered "+damage)
			triggered[damage] = self.getStat("triggered "+damage)

		# print triggered

		# conversions
		conversions = {}
		for fromDamage in damages:
			if fromDamage in dpa.keys() or fromDamage in triggered.keys():
				conversions[fromDamage] = {}
				totalConversion = 0
				for toDamage in damages:
					conversionKey = fromDamage + " to " + toDamage
					if conversionKey in self.stats.keys():
						if verbose:
							print "Found applicable conversion:", conversionKey
						conversions[fromDamage][toDamage] = self.stats[conversionKey]
						totalConversion += self.stats[conversionKey]

				if verbose:
					if conversions[fromDamage]:
						print fromDamage, conversions[fromDamage]

				if totalConversion > 100:
					factor = 100.0/totalConversion
					for conversion in conversions[fromDamage]:
						conversions[fromDamage][conversion] *= factor
					if conversions[fromDamage]:
						if verbose:
							print fromDamage, conversions[fromDamage]


		# for fromDamage in conversions:
		# 	if fromDamage in dpa.keys():
		# 		for toDamage in conversions[fromDamage]:
		# 			conversions[fromDamage][toDamage] = dpa[fromDamage]*(conversions[fromDamage][toDamage]/100.0)

		# for fromDamage in conversions:
		# 	if fromDamage in triggered.keys():
		# 		for toDamage in conversions[fromDamage]:
		# 			conversions[fromDamage][toDamage] = triggered[fromDamage]*(conversions[fromDamage][toDamage]/100.0)

		# print
		# for fromDamage in conversions:
		# 	for toDamage in conversions[fromDamage]:
		# 		if conversions[fromDamage][toDamage] > 0:
		# 			print fromDamage, "->", toDamage, "=", conversions[fromDamage][toDamage]

		self.convertDamage(dpa, conversions)
		self.convertDamage(triggered, conversions)


		if "armor piercing" in self.stats.keys(): # this comes after all other conversions and only applies to weapon damage
			dpa["pierce"] += dpa["physical"]*self.stats["armor piercing"]/100.0
			dpa["physical"] = dpa["physical"]*(1-self.stats["armor piercing"]/100.0)

		#scaling

		durationDamage = {}
		for damage in damages:
			if type(dpa[damage]) == type([]):
				durationDamage[damage] = dpa[damage][0]*self.getStatPerc(damage+" %")
				dpa[damage] = 0
			else:
				dpa[damage] = dpa[damage]*self.getStatPerc(damage+" %")
			triggered[damage] = triggered[damage]*self.getStatPerc(damage+" %")

		# print triggered


		#crits
		oa = self.getStat("offense")
		da = self.difficulty*150 + ((self.level+3)*20)
		critMult = getDamageForHitCrit(getPTH(oa, da), self.getStat("crit damage")/100.0)
		self.results["critical multiplier"] = critMult

		for damage in durationDamage:
			durationDamage[damage] *= critMult
		for damage in dpa:
			dpa[damage] *= critMult
		for damage in triggered:
			triggered[damage] *= critMult

		# print triggered

		triggeredDPS = sum([triggered[key] for key in triggered])

		self.results["damage per attack"] = sum([dpa[key] for key in dpa])
		triggeredDPS += self.getStat("weapon damage %")/100.0*self.results["damage per attack"]
		self.results["DPS (triggered)"] = triggeredDPS
		self.results["DPS (AA)"] = self.results["damage per attack"]*self.stats["attacks/s"]+sum([durationDamage[key] for key in durationDamage])
		self.results["DPS"] = self.results["DPS (triggered)"] + self.results["DPS (AA)"]

	def convertDamage(self, dams, conversions):
		flat = {}
		for fromDamage in conversions:
			if fromDamage in dams.keys():
				flat[fromDamage] = {}
				for toDamage in conversions[fromDamage]:
					flat[fromDamage][toDamage] = dams[fromDamage]*(conversions[fromDamage][toDamage]/100.0)

		for fromDamage in conversions:
			if fromDamage in dams.keys():
				for toDamage in conversions[fromDamage]:
					dams[fromDamage] -= flat[fromDamage][toDamage]
					if not toDamage in dams.keys():
						dams[toDamage] = 0
					dams[toDamage] += flat[fromDamage][toDamage]

	def calculateEffectiveHealth(self):
		# this one depends A LOT on what's hitting us.
		# 	lots of small hits favor armor
		#	BIG hits make armor less valuable
		#	what element are we getting hit by
		#	how fast are the hits coming (for block recovery)

		#avoid melee/avoid ranged
		meleeWeight = .5
		rangedWeight = 1-meleeWeight

		#TODO adjust melee and ranged weight for playstyle

		meleeWeight = meleeWeight * (1-self.getStat("avoid melee")/100.0)
		rangedWeight = rangedWeight * (1-self.getStat("avoid ranged")/100.0)

		damageMultiplier = meleeWeight+rangedWeight

		# print "DM avoid", damageMultiplier


		# defensive ability
		# chance to hit since defense affects all attacks
		# based at looking at some mobs in the mob db it looks like about 20 oa per level plus some base
		# adding 3 to my level as most things seem to be a bit higher than me (seems better to calculate for non-trivial content)
		oa = self.difficulty*150 + ((self.level+3)*20)
		da = self.stats["defense"]
		damageMultiplier *= getDamageForHitCrit(getPTH(oa, da))

		# print "DM defense", getDamageForHitCrit(getPTH(oa, da))

		# damage absorb %
		damageMultiplier *= 1-self.getStat("damage absorb %")

		# I'm going to say half of all hits are physical
		# the other hits are split evenly between all of the remaining attack types.
		# we don't care about flat vs duration damages as we're just trying to score resistance.

		# hit size does matter for non physical attack as well as I think shields can block any attack (they work best against )

		#armor
		#hit locations are already taken into account on an item.
		# ok I'm playing with a formula we will almost certainly need to tweak it: 1.5*(level)^1.5
		# for normal and ultimate I think I can tweak the scalar to 1 and 2.25
		# this is based on looking at a couple monsters on elite difficulty in the grim dawn db and plotting the damage for levels
		# I think I'll run armor 3 times, once for this number, double this number and quadruple this number
		# Then we'll say 5 normal hits, 3 big hits 1 giant hit is the spread

		scalar = 1		
		if self.difficulty == 0:
			scalar = 1
		elif self.difficulty == 1:
			scalar = 1.5
		elif self.difficulty == 2:
			scalar = 2.25

		hit = scalar*((self.level+5)**1.5)
		
		armorMitigation = 0
		armorMitigation += getArmorMitigation(hit, self.stats["armor"], self.stats["armor absorb"]/100.0)*5
		armorMitigation += getArmorMitigation(hit*2, self.stats["armor"], self.stats["armor absorb"]/100.0)*3
		armorMitigation += getArmorMitigation(hit*4, self.stats["armor"], self.stats["armor absorb"]/100.0)
		armorMitigation /= 9.0

		elementChance = {}
		elementChance["physical"] = .5 * armorMitigation
		elementChance["acid"] = .05
		elementChance["aether"] = .05
		elementChance["bleed"] = .05
		elementChance["fire"] = .05
		elementChance["chaos"] = .05
		elementChance["lightning"] = .05
		elementChance["cold"] = .05
		elementChance["pierce"] = .05
		elementChance["vitality"] = .05

		resistMultiplier = 0
		for element in elementChance:
			resistMultiplier += elementChance[element]*(1-self.getStat(element+" resist")/100.0)

		# print "DM resists", resistMultiplier

		damageMultiplier *= resistMultiplier


		#shield


		print "DM final", damageMultiplier
		self.results["effective health"] = (self.stats["health"]+(self.model.stats["fight length"]*self.stats["health/s"]))/damageMultiplier


	#add one to the stat in question and run another character to see the difference in values
	def testStat(self, stat):
		newCharacter = Character(self.model, self.baseAttributes, self.model.skills, self.model.constellations, self.model.items, {stat:1})
		print
		for bonus in sorted(self.results):
			print bonus.ljust(25), newCharacter.results[bonus] - self.results[bonus]

	def addToStat(self, stat, value):
		if not stat in self.stats.keys():
			self.stats[stat] = 0

		if type(self.stats[stat]) == type([]) or type(value) == type([]):
			self.stats[stat] = addDurationDamages(self.stats[stat], value)
		else:
			if stat == "armor absorb":
				value *= .7
			self.stats[stat] += value

	def getStatPerc(self, stat):
		if stat in self.stats.keys():
			return (self.stats[stat]+100)/100.0
		return 1

	def getStat(self, stat):
		if stat in self.stats.keys():
			return self.stats[stat]
		return 0

#this will "inflate" duration damages
def addDurationDamages(a, b):
	if a == 0:
		return b
	if b == 0:
		return a
	return [a[0]+b[0], max(a[1],b[1])]
def subDurationDamages(a, b):
	return [a[0]-b[0], max(a[1],b[1])]

def getPTH(oa, da):
	return 3.15*(oa/(3.5*oa+da)) + .0002275*(oa-da) + .2

def getDamageForHitCrit(pth, critDamage=0):	
	if pth <= .75: # reduced damage on hit
		return pth * (pth/.75)
	elif pth <= .90:
		return pth
	elif pth < 1:
		ctc = pth-.9
		return pth*(1-ctc) + pth*ctc*(1.1+critDamage)
	elif pth <= 1.05:
		critFactor = 1.1 + critDamage
		hd = 1 - (pth-.9)
		return hd + (pth-.9)*critFactor
	else:
		critFactor = 1.1 + critDamage
		hd = 1-(pth-.9) + .15*critFactor
		pthr = pth-1.05
		while pthr > 0:
			critFactor += .1
			hd += min(pthr, .2)*critFactor
			pthr -= .2
		return hd

def getArmorMitigation(damage, armor, armorAbsorb):
	over = max(damage-armor, 0)	
	under = min(damage, armor)
	under = under*(1-armorAbsorb)
	return (over+under)/damage

def mergeBonuses(bonusesA, bonusesB):
	bonusesC = {}
	for bonus in bonusesA:
		if bonus in bonusesB.keys():
			bonusesC[bonus] = bonusesA[bonus] + bonusesB[bonus]
		else:
			bonusesC[bonus] = bonusesA[bonus]
	for bonus in bonusesB:
		if not bonus in bonusesA.keys():
			bonusesC[bonus] = bonusesB[bonus]
	return bonusesC
