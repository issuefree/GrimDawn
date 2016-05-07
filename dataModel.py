import re
import copy
from operator import *
from time import time

import traceback

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

    # returns true if either affinity has value in any category
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

		self.star = None

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
		if self.triggerTime == -1:
			self.effective = 0
			return

		targets = max(1, self.gc("targets"))
		if self.gc("type") == "buff":
			self.effective = self.getUpTime(model)*targets
			# print "buff uptime:", self.getUpTime(model)
		elif self.gc("type") == "attack":

			if self.gc("shape") == "???":
				print "    Shape unknown for", self.name

			# normalized around 2 attacks per second. If I use actual attack speed we get inverse calculated value to actual value. 
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
					targets = targets * .25
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
				self.bonuses["attack opportunity cost"] = 100
				if self.gc("recharge") == 0:
					self.conditions["recharge"] = 1

			self.effective = self.getNumTriggers(model)/(2.0*model.getStat("fight length"))*targets

			# print "nt", self.getNumTriggers(model)

			interval = self.triggerTime+self.gc("recharge")
			for dam in durationDamages:
				if "triggered "+dam in self.bonuses.keys():
					if type(self.gb("triggered "+dam)) == type([]):
						damage, ticks = self.bonuses["triggered "+dam]
						if ticks < interval:
							self.bonuses["triggered "+dam] = damage*ticks
						else:
							self.bonuses["triggered "+dam] = damage*interval

			if "duration" in self.bonuses.keys():
				self.setDebuffValue(model)

		elif self.gc("type") == "shield":
			self.effective = self.getNumTriggers(model)
		elif self.gc("type") == "heal":
			# we're counting half effectiveness due to overheal
			self.effective = self.getNumTriggers(model)*.5

			if "duration" in self.bonuses.keys():
				self.setDebuffValue(model)

		elif self.gc("type") == "summon":
			self.effective = self.getUpTime(model)

	def setDebuffValue(self, model):
		#find duration based elements (for attacks that include a debuff component)
		targets = max(1, self.gc("targets"))
		upTime = self.getUpTime(model)
		# print "up", upTime
		durationBonuses = self.bonuses["duration"]
		for bonus in durationBonuses.keys():
			self.bonuses[bonus] = durationBonuses[bonus]*upTime/self.effective*targets
			if bonus in ["triggered "+damage for damage in damages]:
				self.bonuses[bonus] = self.bonuses[bonus] / 2
		del self.bonuses["duration"]

	def calculateTriggerTime(self, model):
		if self.gc("trigger") == "manual":
			return 0
		triggerFrequency = model.getStat(self.gc("trigger")+"s/s")
		if triggerFrequency == 0:
			self.triggerTime = -1
			return
		self.triggerTime = 1.0/triggerFrequency * 1.0/self.gc("chance")
		# print "tt", self.triggerTime

	#uptime is a percent so we'll use a scalar of fight length to get an average across multiple fights
	def getUpTime(self, model):
		up = 0.0
		fightLen = model.getStat("fight length")*5
		fightRemaining = fightLen - self.triggerTime		
		while fightRemaining >= 0:
			up += min(max(self.gc("duration"), self.gc("lifespan")), fightRemaining)
			fightRemaining -= max(self.gc("duration"), self.gc("recharge") + self.triggerTime) 
		return up/fightLen

	#average over a number of fights
	def getNumTriggers(self, model):
		numFights = 5.0
		triggers = 0
		fightRemaining = model.getStat("fight length")*numFights - self.triggerTime
		while fightRemaining >= 0:
			triggers += 1
			fightRemaining -= self.gc("recharge") + self.triggerTime

		triggers = max(triggers, 1) # this will usually catch low health events which don't happen often. We'll calculate stats as if they happen once a fight.

		return triggers/numFights

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
						print "    " +self.name+" requires a defined " + dam + " _stat_ in the model."
						model.stats[dam] = .01
					else:
						self.bonuses[dam] = self.gb(dam) + (model.getStat(dam) * self.gb("weapon damage %")/100.0 + self.gb(dam)) * self.gb(dam+" %")/100.0

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
					model.stats["pet all damage %"] = .01
				else:
					self.bonuses["triggered "+dam] = self.gb("triggered "+dam) + self.gb("pet "+dam)*model.getStat("pet all damage %")/100

	def calculateValue(self, model):
		self.calculateEffective(model)
		# print "Effective %:", self.name, self.effective

		self.calculateDynamicBonuses(model)
		
		modelFactor = 1
		self.name
		if self.name in model.bonuses.keys():
			modelFactor = model.get(self.name)

		for bonus in self.bonuses.keys():
			self.star.bonuses[bonus] = self.bonuses[bonus]*self.effective * modelFactor
		self.star.bonuses[self.name] = 1

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

		self.value = None
		self.apsValue = []

		self.redundancies = []
		self.conflicts = []

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
			if apsIndex == 0 or not self.hasAttackTrigger():
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
			for i in range(len(model.getStat("allAttacks/s"))-1, -1, -1 ):
				apsModel = copy.deepcopy(model)
				apsModel.stats["attacks/s"] = apsModel.stats["allAttacks/s"][i]
				for star in self.stars:
					star.reset()
					self.apsValue[i] += star.evaluate(apsModel)
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
			if location in item.location:
				locItems += [item]
		return locItems

	def __init__(self, name, bonuses, location, ability=None):
		self.name = name
		self.bonuses = bonuses
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
				print location
				if location in Item.meleeLocations:
					self.ability.conditions["shape"] = "melee"
			self.ability.calculateEffective(model)
			self.ability.calculateDynamicBonuses(model)
			for bonus in self.ability.bonuses.keys():
				abilityBonuses[bonus] = self.ability.bonuses[bonus]*self.ability.effective

		value = 0
		for bonus in model.bonuses.keys():
			if bonus in self.bonuses.keys():
				keyBonus = self.bonuses[bonus]
				if bonus == "armor" and location:
					try:					
						keyBonus = self.bonuses["armor"]*Item.armorLocationFactor[location]
					except:
						pass
				if verbose:
					print "  ", bonus.ljust(20), str(int(keyBonus)).ljust(5), int(model.get(bonus)*keyBonus)
				value += model.get(bonus)*keyBonus
			if bonus in abilityBonuses.keys():
				value += model.get(bonus)*abilityBonuses[bonus]
				if verbose:
					print "  ", bonus.ljust(20), str(int(abilityBonuses[bonus])).ljust(5), int(model.get(bonus)*abilityBonuses[bonus])
		self.value = value
		return value

