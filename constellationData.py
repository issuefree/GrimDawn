import re
from operator import *

class Model:
	def __init__(self, bonuses, stats):
		self.bonuses = bonuses
		self.stats = stats

		self.checkModel()

	def __str__(self):
		out = ""
		for key in sorted(self.bonuses.keys()):
			if self.get(key) > 0:
				out += key + " " + str(self.bonuses[key]) + "\n"
		return out

	def checkModel(self):
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

		# physique grants health/s, health and defense so this should be accounted for
		val = 0
		val += self.get("health/s") * .04
		val += self.get("health") * 3
		val += self.get("defense") * .5

		self.set("physique", max(self.get("physique"), val))

		# cunning grants physical %, pierce %, bleed %, internal % and offense.
		val = 0
		val += self.get("physical %") * .33
		val += self.get("pierce %") * .285
		val += self.get("bleed %") * .333
		val += self.get("internal %") * .333
		val += self.get("offense") * .5

		self.set("cunning", max(self.get("cunning"), val))

		# spirit grants fire %, burn %, cold %, frostburn %, lightning %, electrocute %, acid %, poison %, vitality %, vitality decay%, aether %, chaos %, energy and energy regen
		val = 0
		val += sum([self.get(b) for b in ["elemental %", "acid %", "vitality %", "aether %", "chaos %"]]) * .33
		val += sum([self.get(b) for b in ["burn %", "frostburn %", "electrocute %", "poison %", "vitality decay %"]]) * .333
		val += self.get("energy") * 2
		val += self.get("energy/s") * .01

		self.set("spirit", max(self.get("spirit"), val))
		#check stats vs % stats
		percStats = ["physique", "cunning", "spirit", "offense", "defense", "health", "armor"]
		for stat in percStats:
			self.set(stat+" %", self.getStat(stat) * self.get(stat) / 100)
			print stat + " %: " + str(self.get(stat+" %"))

		#check resist reduction
		# I'm assuming 25% resistance for the purposes of calculating value.
		# at that resistance each point of resist reduction resulst in 1.33% more overall damage.
		# if we have +400% vitality damage (500% total) a 1 percent reduction in resist is worth
		# 500*.0133 vitality % or 6.65 %
		for damage in primaryDamages:
			if self.get(damage+" %") > 0:
				self.set("reduce "+damage+" resist", self.getStat(damage+" %")*.0133*self.get(damage+" %"))
				print "reduce "+damage+" resist: " + str(self.get("reduce "+damage+" resist"))

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
			"acid resist", 
			"vitality resist", 
			"pierce resist", 
			"aether resist", 
			"chaos resist",
			"bleed resist"
		]
		for b in resists:
			self.set(b, max(self.get(b), self.get("resist")))
			self.set("pet "+b, max(self.get("pet "+b), self.get("pet resist")))

			self.set("reduce "+b, max(self.get("reduce "+b), self.get("reduce resist")))
		for b in resists:
			self.set("reduce resist", max(self.get("reduce resist"), self.get("reduce "+b)))


		# elemental damage % and resist should be the sum of the individual components
		self.set("elemental %", max(self.get("elemental %"), sum([self.get(b) for b in ["cold %", "lightning %", "fire %"]])))

		# elemental resists are weird. e.g. fire resist protects against burn and elemental resist protects against fire but elemental resist does not protect against burn
		self.set("elemental resist", max(self.get("elemental resist"), sum([self.get(b) for b in ["cold resist", "lightning resist", "fire resist"]])))

		# all damage should be >= all other damage bonuses (sans retaliation)
		# don't count cold, lightning, or fire as they're already aggregated under elemental
		parts = ["acid %", "aether %", "bleed %", "burn %", "chaos %", "electrocute %", "elemental %", "frostburn %", "internal %", "physical %", "pierce %", "poison %", "vitality %", "vitality decay %"]
		self.set("all damage %", max(self.get("all damage %"), sum([self.get(b) for b in parts])))

		# catch all for flat damage of any type
		# triggered flat damage should be either specified manually or be equivalent to normal flat damage.
		# catch all for triggered damage of any type (no triggered damage is useless right?)		
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
		for damage in damages:
			self.set(damage, max(self.get(damage), self.get("damage")))
			# pet flat damage?
			self.set("triggered "+damage, max([self.get("triggered "+damage), self.get(damage), self.get("triggered damage")]))

		#nothing grants total speed

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
		self.ascendant = 0
		self.chaos = 0
		self.eldritch = 0
		self.order = 0
		self.primordial = 0

		if type(ascendant) == type(""):
			m = re.search("(\d+)+a", ascendant)
			if m:
				self.ascendant = int(m.group(1))

			m = re.search("(\d+)+c", ascendant)
			if m:
				self.chaos = int(m.group(1))

			m = re.search("(\d+)+e", ascendant)
			if m:
				self.eldritch = int(m.group(1))

			m = re.search("(\d+)+o", ascendant)
			if m:
				self.order = int(m.group(1))

			m = re.search("(\d+)+p", ascendant)
			if m:
				self.primordial = int(m.group(1))
		else:
			self.ascendant = ascendant
			self.chaos = chaos
			self.eldritch = eldritch
			self.order = order
			self.primordial = primordial

	def magnitude(self):
		return self.ascendant + self.chaos + self.eldritch + self.order + self.primordial

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

class Ability:
	def __init__(self, name, star):
		self.name = name
		self.star = star

		self.type = None

		self.trigger = None #[attack,hit,block]
		self.triggerChance = 0
		self.recharge = 0
		self.duration = 0		
		self.targets = 0

	def calculateInterval(self, model):
		triggerFrequency = model.getStat(self.trigger+"s/s")
		#if something has a 33% chance to activate then on average 1 in 3 triggers will activate it.
		triggerFrequency * self.triggerChance

	def evaluate(self, model):
		self.calculateEffective(model)

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

		self.constellation.addStar(self)

	def __str__(self):
		return self.constellation.name + "." + str(self.constellation.stars.index(self))

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
		value = 0
		for bonus in model.bonuses.keys():
			if bonus in self.bonuses.keys():
				value += model.get(bonus)*self.bonuses[bonus]
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

	def addAbility(self, name, perc, bonuses):
		self.name = name
		self.bonuses[name] = 1
		for bonus in bonuses.keys():
			self.bonuses[bonus] = bonuses[bonus]*perc
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

		self.stars = []
		self.abilities = []
		self.value = 0

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
		self.value = 0
		for star in self.stars:
			self.value += star.evaluate(model)

		return self.value

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

	# ignore this
	# we'll use 75% chance of triggering for our timing
	# 1-((1-.15)^x) = .75 -> log_.25(1-.15) = 8.5 attacks to trigger after cooldown, 4 attacks in the cooldown

falcon = Constellation("Falcon", "1a", "3a 3e")
a = Star(falcon, [], {"physical %":15})
b = Star(falcon, a, {"bleed %":24})
c = Star(falcon, b, {"cunning":15})
d = Star(falcon, c, {"physical %":24})
e = Star(falcon, d, {"Falcon Swoop":True})
# 6 projectiles
# 100% chance to pierce (assume pierce means on average 2 hits)
# I'm guestimating I'll get 4 hits per.
# 15 % on attack
# 1 second recharge
# we'll use an arbitrary .5 seconds per attack for an auto attacker
# 1/.15 = 6.66 so 1 in 6.66 attacks will trigger
# add the 2 from the recharge for 1 in 8.66
# 1/8.66 * 4 = .46
e.addAbility("Falcon Swoop", .46, {"weapon damage %":65, "triggered bleed":125})

shepherd = Constellation("Shepherd's Crook", "1a", "5a")
a = Star(shepherd, [], {"health":40, "pet health %":8})
b = Star(shepherd, a, {"cunning":10, "health":40})
c = Star(shepherd, b, {"elemental resist":10, "pet elemental resist":15})
d = Star(shepherd, c, {"health %":3, "pet health %":5, "pet defense %":5})
e = Star(shepherd, d, {})
# 4 second uptime, 6 second recharge 25% trigger on attack. Estimating 50% uptime.
e.addAbility("Shepherd's Call", .5, {"offense":70, "pet all damage %": 190, "pet crit damage":25, "pet retaliation %":250})

hammer = Constellation("Hammer", "1a", "4a")
a = Star(hammer, [], {"physical %":15})
b = Star(hammer, a, {"defense":8, "internal %":30})
c = Star(hammer, b, {"physical %":15, "internal %":30})

anvil = Constellation("Anvil", "1a", "5a")
a = Star(anvil, [], {"defense":10})
b = Star(anvil, a, {"physique":10})
c = Star(anvil, b, {"armor absorb":3})
d = Star(anvil, c, {"defense":15, "constitution %":20})
e = Star(anvil, d, {"Targo's Hammer":True})
# 25% chance on block
# estimating .75 seconds per block
#	working no our default .5 seconds per attack so a block is .666 as valuable as an attack
# described as a close AoE so we'll assume ~3 hits# 
# 3 * .25 * .66
e.addAbility("Targo's Hammer", .495, {"stun %":50, "weapon damage %":92, "physical":100, "internal %":.92*145})

owl = Constellation("Owl", "1a", "5a")
a = Star(owl, [], {"spirit":10})
b = Star(owl, a, {"elemental resist":8, "skill cost %":-5})
c = Star(owl, b, {"burn %":30, "electrocute %":30, "frostburn %":30})
d = Star(owl, b, {"elemental %":24, "reflected damage reduction":15})

harpy = Constellation("Harpy", "1a", "5a")
a = Star(harpy, [], {"pierce %":15, "cold %":15})
b = Star(harpy, a, {"cunning":10})
c = Star(harpy, b, {"bleed resist":10, "offense":15})
d = Star(harpy, b, {"pierce":(3+7)/2, "pierce %":24, "cold %":24})

throne = Constellation("Empty Throne", "1a", "5a")
a = Star(throne, [], {"reduced stun duration":15})
b = Star(throne, a, {"pierce resist":8, "pet pierce resist":8})
c = Star(throne, b, {"chaos resist":8, "pet chaos resist":8})
d = Star(throne, b, {"aether resist":8, "pet aether resist":8})

wolverine = Constellation("Wolverine", "1a", "6a")
a = Star(wolverine, [], {"defense":15, "pet pierce resist":10})
b = Star(wolverine, a, {"pierce retaliation":30, "retaliation %":20, "pet pierce retaliation":50})
c = Star(wolverine, b, {"defense":18, "pet bleed resist":25})
d = Star(wolverine, c, {"retaliation %":35, "pet retaliation %":50})
e = Star(wolverine, c, {"defense %":3, "melee weapon physique requirements":-10, "melee weapon cunning requirements":-10, "pet defense %":5})

crab = Constellation("Crab", "6a 4o", "3a")
a = Star(crab, [], {"constitution %":15, "physique":20})
b = Star(crab, a, {"elemental %":30, "internal %":70})
c = Star(crab, b, {"Elemental Barrier":True})
d = Star(crab, c, {"pierce resist":18, "defense":10})
e = Star(crab, d, {"elemental %":40, "elemental resist":15})

scepter = Constellation("Rhowan's Scepter (requires mace)", "6a 4o", "3a 2o")
a = Star(scepter, [], {"defense":15})
b = Star(scepter, a, {"health %":6})
c = Star(scepter, b, {"physical %":50})
d = Star(scepter, c, {"internal %":80})
e = Star(scepter, b, {"defense":18})
f = Star(scepter, e, {"physical":(8+12)/2,"stun %":5, "stun duration":10})

boar = Constellation("Autumn Boar", "4a 3o 4p", "3a")
a = Star(boar, [], {"physique":10, "cunning":10})
b = Star(boar, a, {"pierce resist":15, "physique":10})
c = Star(boar, b, {"physique %":5})
d = Star(boar, c, {"physical resist":4, "fire resist":20})
e = Star(boar, c, {"stun duration":10, "physical retaliation":150})
f = Star(boar, e, {"bleed retaliation":2100*.1})
g = Star(boar, e, {})
# 25% on block
# ~.75 seconds per block (.5 s per attack)
# 1 second recharge
# description sounds like a frontal cone so we'll go with 2 targets avg
# 1 in 4 blocks will trigger .55/.75 = .66 so 1 in ~6 attack equivalents + 2 from the recharge
# 1/8*2 = .25
g.addAbility("Trample", .25, {"stun %":100, "weapon damage %":80, "internal":404})

scythe = Constellation("Harvestman's Scythe", "3a 3o 5p", "3a 3p")
a = Star(scythe, [], {"energy/s":2})
b = Star(scythe, a, {"health/s":12})
c = Star(scythe, b, {"physique %":4, "constitution %":20})
d = Star(scythe, c, {"health regeneration":20})
e = Star(scythe, d, {"energy regeneration":20})
f = Star(scythe, e, {"cunning %":4, "spirit %":4})

crown = Constellation("Rhowan's Crown", "4a 6e", "1a 1e")
a = Star(crown, [], {"elemental %":30, "elemental":(6+9)/2})
b = Star(crown, a, {"spirit":20, "pet elemental %":40})
c = Star(crown, b, {"Elemental Storm":True})
d = Star(crown, c, {"elemental resist":18, "pet elemental resist":10})
e = Star(crown, d, {"elemental %":40, "burn %":60, "electrocute %":60, "frostburn %":60, "chaos resist":8})

huntress = Constellation("Huntress", "4a 3c 4e", "1a 1e")
a = Star(huntress, [], {"offense":15})
b = Star(huntress, a, {"pierce %":35})
c = Star(huntress, b, {"bleed %":60})
d = Star(huntress, c, {"pierce resist":8, "damage beast %":15, "health":100})
e = Star(huntress, c, {"offense %":3, "pet offense %":5})
f = Star(huntress, e, {"bleed":30, "bleed %":50, "bleed duration":20})
g = Star(huntress, e, {})
# 20% on attack, 5 second duration, no recharge
# calling it .9
# no stat for reducing opponent offense so we'll call it defense

# the bleed damage is high and long and the apply rate is very high but it's also AoE.
# using the .5 per attack the 307 bleed per second is worth ~150 per hit.
# assuming 3 targets that's 450 per hit but I the damage may spread across hits as I hit different targets...
# call hit 500
g.addAbility("Rend", .9, {"defense":125, "reduce bleed resist":33, "triggered bleed":500})

leviathan = Constellation("Leviathan", "13a 13e")
a = Star(leviathan, [], {"cold":8, "cold %":80})
b = Star(leviathan, a, {"health %":5, "physique":25})
c = Star(leviathan, b, {"defense":26, "energy regeneration":20, "energy %":10})
d = Star(leviathan, c, {"pierce resist":20, "cold resist":20})
e = Star(leviathan, d, {"cold":(12+16)/2, "cold %":100})
f = Star(leviathan, d, {"frostburn":25*3, "frostburn %":100})
g = Star(leviathan, d, {})
# 30% on attack
# 3 second recharge
# 6 second duration
# 3.5 meter radius
# decent sized aoe probably 2 targets, it lasts and hits stuff that walks in (I assume) so call it another .5
g.addAbility("Whirlpool", .3*2.5, {"cold":322, "frostburn":266, "slow move":35})

oleron = Constellation("Oleron", "20a 7o")
a = Star(oleron, [], {"physique":20, "cunning":20, "health":100})
b = Star(oleron, a, {"physical %":80, "internal %":80})
c = Star(oleron, b, {"pierce resist":20, "bleed resist":10, "offense":30})
d = Star(oleron, c, {"physical resist":4, "health":200})
e = Star(oleron, d, {"physical":(9+18)/2, "physical %":100})
f = Star(oleron, d, {"offense":15, "internal":25*5, "internal %":100, "max pierce resist":2})
g = Star(oleron, d, {})
# 100% on critical (hrm, call it 15%)
# 1 second recharge
# 1/(1/.15+4) ~= .1
# 5 meter pbaoe for 3 targets
g.addAbility("Blind Fury", .1*3, {"weapon damage %":85, "internal":324, "bleed":324, "slow attack":25, "reduce armor":275})

tortoise = Constellation("Tortoise", "1o", "2o 3p")
a = Star(tortoise, [], {"defense":10, "health":25})
b = Star(tortoise, a, {"defense":12, "shield physique requirements":-10})
c = Star(tortoise, b, {"defense":12, "health":100})
d = Star(tortoise, c, {"health %":4, "defense":10, "armor %":4})
e = Star(tortoise, c, {})
# 100% chance at 40% health
# 30 second recharge
# I'll probably only hit 40% health once per fight on a 30 second cooldown
e.addAbility("Turtle Shell", 1, {"health":2700})

blade = Constellation("Assassin's Blade", "1o", "3a 2o")
a = Star(blade, [], {"pierce %":15})
b = Star(blade, a, {"offense":12})
c = Star(blade, a, {"bleed %":15, "pierce %":15})
d = Star(blade, c, {"bleed %":30})
e = Star(blade, d, {})
#100% on crit: ~15% on attack
#15 second duration, so on big targets we'll have nearly 100% uptime. for small stuff it doesn't matter.
#call it 66%?
e.addAbility("Assassin's Mark", .66, {"reduce physical resist":33, "reduce pierce resist":33})

lion = Constellation("Lion", "1o", "3o")
a = Star(lion, [], {"health %":4, "defense":8, "pet health %":3})
b = Star(lion, a, {"spirit":10, "health":100})
c = Star(lion, b, {"all damage %":15, "pet all damage %":12})

crane = Constellation("Crane", "1o", "5o")
a = Star(crane, [], {"physique":8, "spirit":8})
b = Star(crane, a, {"acid resist":12})
c = Star(crane, b, {"all damage %":15, "weapon spirit requirements":-10})
d = Star(crane, c, {"vitality resist":8})
e = Star(crane, d, {"elemental resist":10})

panther = Constellation("Panther", "1o", "2o 3p")
a = Star(panther, [], {"offense":12, "pet offense %":2})
b = Star(panther, a, {"cunning":8, "spirit":8, "pet all damage %":15})
c = Star(panther, b, {"all damage %":15, "energy regeneration":10, "pet offense %":3})
d = Star(panther, c, {"offense":20, "pet crit damage":5})

dryad = Constellation("Dryad", "1o", "3o")
a = Star(dryad, [], {"acid resist":10, "energy":200})
b = Star(dryad, a, {"energy/s":1, "health":80})
c = Star(dryad, b, {"reduced poison duration":20, "reduced bleed duration":20})
d = Star(dryad, c, {"spirit %":5, "jewelry spirit requirements":-10})
e = Star(dryad, d, {})
#33% on attack
#4 second recharge
#8%+350 health restored
# how long is a fight? call it... 30 seconds.
# 1 in 3 attacks triggers it, .5 seconds per attack = 1.5 seconds + 4 seconds recharge = 5.5 seconds. Will trigger ~5 times per fight.
# lets say half of them aren't used because we're near full health
e.addAbility("Dryad's Blessing", 2.5, {"health %":8, "health":350, "reduced poison duration":30, "reduced bleed duration":30})

shieldmaiden = Constellation("Shieldmaiden (requires shield)", "4o 6p", "2o 3p")
a = Star(shieldmaiden, [], {"block %":4})
b = Star(shieldmaiden, a, {"armor absorb":5})
c = Star(shieldmaiden, b, {"blocked damage %":18})
d = Star(shieldmaiden, c, {"retaliation %":50})
e = Star(shieldmaiden, b, {"reduced stun duration":25, "blocked damage %":15})
f = Star(shieldmaiden, e, {"shield recovery":15, "stun retaliation":15})

scales = Constellation("Scales of Ulcama", "8o", "2o")
a = Star(scales, [], {"health":250, "energy":300})
b = Star(scales, a, {"health/s":6, "health regeneration":10})
c = Star(scales, b, {"health %":6})
d = Star(scales, c, {"energy regeneration":10, "energy/s":2})
e = Star(scales, b, {"all damage %":30})
f = Star(scales, e, {})
# assuming single target
# 20% when hit
# 1.5 s recharge
# I have no idea how to handle the 135% attack damage converted to health
# assume I get hit 2 times a second so 2.5 seconds + 1.5 seconds = 4 seconds between
# normalizing to .5 s per attack = 1/8
# let's say I get... 300 health per, it triggers 3 times in a fight that's 900 health in a fight.
# multiply by 8 since it's not weapon attack adjusted
f.addAbility("Tip the Scales", 1.0/8, {"triggered vitality":170, "energy leech":320, "health":900*8})

assassin = Constellation("Assassin", "6a 4o", "1a 1o")
a = Star(assassin, [], {"pierce %":30})
b = Star(assassin, a, {"cunning":15})
c = Star(assassin, b, {"offense":18, "defense":10})
d = Star(assassin, b, {"bleed resist":8, "cunning %":5})
e = Star(assassin, d, {"defense":12, "acid resist":8, "damage human %":15})
f = Star(assassin, d, {"pierce":6, "pierce %":40})
g = Star(assassin, f, {})
#100% on crit: ~15% on hit
#18 projectiles
#100% pass through
# call it 6 hits
# 4 attacks for recharge, ~6 attacks between hits = .1
g.addAbility("Blades of Wrath", .1*6, {"triggered pierce":168, "weapon damage %":25})

blades = Constellation("Blades of Nadaan (requires sword)", "10a", "3a 2o")
a = Star(blades, [], {"avoid melee":2, "avoid ranged":2})
b = Star(blades, a, {"pierce %":40})
c = Star(blades, b, {"pierce %":50})
d = Star(blades, b, {"attack speed":5})
e = Star(blades, b, {"attack speed":5})
f = Star(blades, b, {"armor piercing %":100})

targo = Constellation("Targo the Builder", "4o 6p", "1o")
a = Star(targo, [], {"defense":15})
b = Star(targo, a, {"health %":5})
c = Star(targo, b, {"armor %":5})
d = Star(targo, b, {"health %":5})
e = Star(targo, d, {"defense":20, "health":300})
f = Star(targo, d, {"armor %":5, "blocked damage %":20})
g = Star(targo, f, {})
#33% on attack (1.5 s to trigger)
#8 second recharge
#5 second duration
#9.5 seconds
g.addAbility("Shield Wall", 5/9.5, {"damage reflect %":125, "blocked damage %":125, "armor %":30})

obelisk = Constellation("Obelisk of Menhir", "8o 15p")
a = Star(obelisk, [], {"armor %":7})
b = Star(obelisk, a, {"defense":30, "armor":150})
c = Star(obelisk, b, {"retaliation %":100})
d = Star(obelisk, a, {"defense %":5, "defense":25})
e = Star(obelisk, d, {"block %":5, "blocked damage %":30})
f = Star(obelisk, e, {"reduced stun duration":30, "reduced freeze duration":30, "armor %":4, "max pierce resist":3})
g = Star(obelisk, f, {})
#15% on block (1/.15/.75*.5) = 4.44 seconds to trigger
#12 second recharge
#8 second duration
#8/16.4
g.addAbility("Stone Form", 8/16.4, {"armor %":50, "armor absorb":20, "pierce resist":50, "reduced poison duration":50, "reduced bleed duration":50, "retaliation %":70})

soldier = Constellation("Unknown Soldier", "15a 8o")
a = Star(soldier, [], {"offense":15, "pierce %":60})
b = Star(soldier, a, {"bleed":21*3, "bleed %":80})
c = Star(soldier, b, {"lifesteal %":3, "attack speed":5, "health":150})
d = Star(soldier, b, {"bleed %":80, "pierce %":80})
e = Star(soldier, d, {"health %":4, "offense":40})
f = Star(soldier, e, {"pierce":20, "crit damage":10})
g = Star(soldier, f, {})
#100% on crit: 15% on attack
#6 second recharge
#3 summon limit
#20 second lifespan
# even more guessworky than most others...
# 2 attacks. shadow strike and shadow blades.
# I'm assuming strike is an engage and blades is the normal attack
# lets assume 1 strike and 5 normal attacks in a lifespan
# 3.3 s to trigger 6 second recharge means 2.5 lifespans in a 30 second fight.
g.addAbility("Living Shadow", 2.5, {"triggered bleed":35+(48*2*5), "triggered physical":68.5+45.5*5})

scorpion = Constellation("Scorpion", "1e", "5e")
a = Star(scorpion, [], {"offense":12})
b = Star(scorpion, a, {"poison %":24})
c = Star(scorpion, b, {"offense":18})
d = Star(scorpion, c, {"acid %":15, "poison %":30})
e = Star(scorpion, c, {})
#25% on attack
#1.5 s recharge
#6 projectiles
#100% passthrough
# 4 hits
# reduced defense will count as offense
# 3 attack recharge, 4 attack trigger = 1/7
e.addAbility("Scorpion Sting", 1.0/7, {"offense":140, "triggered poison":320, "weapon damage %":30})

eye = Constellation("Eye of the Guaridan", "1e", "3a 3e")
a = Star(eye, [], {"acid %":15, "poison %":15})
b = Star(eye, a, {"chaos %":15})
c = Star(eye, b, {"chaos %":15, "poison %":15})
d = Star(eye, c, {"poison %":30})
e = Star(eye, d, {})
#15% on attack
#.5 s recharge
#100% pass through
#6.6 attacks to trigger 1 attack cooldown
e.addAbility("Guardian's Gaze", 1/7.6, {"weapon damage %":18, "triggered chaos":78, "triggered poison":156})

bat = Constellation("Bat", "1e", "2c 3e")
a = Star(bat, [], {"vitality %":15, "bleed %":15})
b = Star(bat, a, {"vitality decay":166*.15})
c = Star(bat, b, {"vitality %":24, "bleed %":30})
d = Star(bat, c, {"life leech %":30, "lifesteal %":3})
e = Star(bat, d, {})
#20% on attack
#1 second recharge
#2 projectiles
#70% pass through
# call it 2.5 hits on average
#2 attacks recharge and 5 attacks trigger
# 3.5 seconds between ~= 8 hits per fight. ~250 damage = 125 heal per hit = 1000 health per fight
e.addAbility("Twin Fangs", 2.5/7, {"weapon damage":25, "triggered pierce":116, "triggered vitality":111, "health":1000})

spider = Constellation("Spider", "1e", "6e")
a = Star(spider, [], {"cunning":10, "spirit":10})
b = Star(spider, a, {"offense":10, "chaos resist":8})
c = Star(spider, a, {"offense":15, "defense":10, "damage from insectoids":-12, "damage from arachnids":-12})
d = Star(spider, a, {"cunning %":3, "spirit %":3})
e = Star(spider, a, {"cast speed":3, "attack speed retaliation":20, "move speed retaliation":20})

raven = Constellation("Raven", "1e", "5e")
a = Star(raven, [], {"spirit":8, "pet all damage %":15})
b = Star(raven, a, {"energy/s":1, "spirit":10})
c = Star(raven, b, {"offense":15, "pet offense %":5})
d = Star(raven, b, {"all damage %":15, "pet lightning damage %":60})

fox = Constellation("Fox", "1e", "5e")
a = Star(fox, [], {"cunning":10})
b = Star(fox, a, {"bleed":10*3, "bleed %":24})
c = Star(fox, b, {"bleed resist":8, "cunning":15})
d = Star(fox, c, {"bleed":14*3, "bleed %":45})

light = Constellation("Scholar's Light", "1e", "4e")
a = Star(light, [], {"fire %":15})
b = Star(light, a, {"elemental resist":8, "physique":10})
c = Star(light, b, {"elemental %":24, "elemental":8, "energy/s":1.5})

hawk = Constellation("Hawk", "1e", "3e")
a = Star(hawk, [], {"offense":15})
b = Star(hawk, a, {"crit damage":8})
c = Star(hawk, b, {"offense %":3, "cunning ranged requirements":-10})

witchblade = Constellation("Solael's Witchblade", "4c 6e", "1c 1e")
a = Star(witchblade, [], {"chaos %":40})
b = Star(witchblade, a, {"offense":10, "spirit":15})
c = Star(witchblade, b, {"energy burn %":10, "chaos %":30})
d = Star(witchblade, c, {"fire %":50, "chaos %":50, "fire resist":15})
e = Star(witchblade, d, {})
#15% on attack
#4 second duration
# says "spreads wildly among your foes" so there's probably some aoe component but we're treating it as single target
e.addAbility("Eldritch Fire", 1/6.6, {"triggered fire":102, "triggered chaos":102, "slow move":33, "reduce fire resist":20, "reduce chaos resist":20})

bonds = Constellation("Bysmiel's Bonds", "4c 6e", "3e")
a = Star(bonds, [], {"offense":15, "pet all damage %":30})
b = Star(bonds, a, {"cast speed":5, "pet total speed":8})
c = Star(bonds, b, {"vitality resist":15, "pet vitality resist":20})
d = Star(bonds, c, {"all damage %":30, "pet all damage %":40, "pet health %":8})
e = Star(bonds, d, {})
#20% on attack
#30 second recharge
#20 second lifespan
#1 lifespan per fight
# ~7.5 attacks per lifespan
# this guy scales with pet damage so I'm not sure how to handle it
# there's a scale factor we need to account for somehow at some point
e.addAbility("Bysmiel's Command", 7.5, {"triggered physical":26.5, "triggered acid":38.5})

magi = Constellation("Magi", "10e", "3e")
a = Star(magi, [], {"fire %":40, "burn %":50})
b = Star(magi, a, {"elemental resist":8})
c = Star(magi, b, {"fire resist":25})
d = Star(magi, c, {"cast speed":5, "burn %":60})
e = Star(magi, c, {"fire":(6+8)/2, "fire %":40})
f = Star(magi, c, {"burn":12*3, "burn %":30, "burn duration":30})
g = Star(magi, f, {})
#15% on attack
#1.5 s recharge
#5 second duration
# 1 meter radius
#7 fragments
# call it 4 targets
# 3 attacks recharge 6.66 attacks trigger
g.addAbility("Fissure", 4/9.6, {"triggered fire":116, "triggered burn":264, "stun %":1.5})

berserker = Constellation("Berserker (requires axe)", "5a 5e", "2c 3e")
a = Star(berserker, [], {"offense":15})
b = Star(berserker, a, {"physical %":50})
c = Star(berserker, b, {"offense":25})
d = Star(berserker, a, {"bleed %":80, "lifesteal %":3})
e = Star(berserker, d, {"bleed %":100*.15, "bleed duration":100*.15, "crit damage":5})
f = Star(berserker, f, {"pierce resist":10, "reduced bleed duration":20})

lantern = Constellation("Oklaine's Lantern (requires scepter, dagger or caster off-hand)", "10e", "3e 2o")
a = Star(lantern, [], {"energy regeneration":15})
b = Star(lantern, a, {"offense":25})
c = Star(lantern, b, {"offense":15, "crit damage":5})
d = Star(lantern, c, {"all damage %":50, "reduced entrapment duration":25})
e = Star(lantern, d, {"cast speed":5, "attack speed":5, "energy/s":2})

behemoth = Constellation("Behemoth", "3c 4e 4p", "2c 3e")
a = Star(behemoth, [], {"health/s":10})
b = Star(behemoth, a, {"health":300, "pet health %":5})
c = Star(behemoth, b, {"health/s":15, "constitution %":25})
d = Star(behemoth, b, {"health %":4})
e = Star(behemoth, b, {"health regeneration":10, "pet health regeneration":20})
f = Star(behemoth, b, {})
#15 % when hit
#30s recharge
#10s duration
# will trigger once per 30s fight but will probably overheal
f.addAbility("Giant's Blood", .75, {"health%":20, "health":1000, "health/s":240})

affliction = Constellation("Affliction", "4a 3c 4e", "1a 1e")
a = Star(affliction, [], {"vitality %":40, "poison %":40})
b = Star(affliction, a, {"spirit":15, "vitality decay retaliation":600, })
c = Star(affliction, b, {"Fetid Pool":True})
#33% when hit
#2 second recharge
#6 second duration
# 3 meter radius
# 2 targets
# 4 hits recharge, 3.33 hits trigger
c.addAbility("Fetid Pool", 2/7.33, {"triggered vitality":128, "triggered poison":136, "slow move":25})
d = Star(affliction, c, {"offense":18, "defense":10})
e = Star(affliction, d, {"crit damage":10, "vitality decay retaliation":720})
f = Star(affliction, c, {"vitality":(11+21)/2, "acid resist":10})
g = Star(affliction, f, {"offense %":3, "vitality %":50, "acid %":50})

manticore = Constellation("Manticore", "4c 6e", "1a 1e")
a = Star(manticore, [], {"offense":15})
b = Star(manticore, a, {"acid %":50, "poison %":50})
c = Star(manticore, b, {"health %":4})
d = Star(manticore, c, {"offense":10, "acid resist":25})
e = Star(manticore, c, {"poison":8*5, "acid %":40, "poison %":40})
f = Star(manticore, e, {})
#15% on attack
#1 second recharge
#4 meter range
#call it 1.5 targets
#2 attack recharge 6.66 attack trigger
f.addAbility("Acid Spray", 1.5/8.66, {"triggered acid":148, "triggered poison":180, "reduce armor":250, "reduce resist":30})

abomination = Constellation("Abomination", "8c 18e")
a = Star(abomination, [], {"chaos %":80, "poison %":80})
b = Star(abomination, a, {"vitality %":80, "acid %":80})
c = Star(abomination, b, {"offense":40, "acid resist":20, "max acid resist":3})
d = Star(abomination, c, {"offense":20, "chaos %":80, "health":150})
e = Star(abomination, d, {})
#100% on enemy death
#18 s recharge
#12 s duration
#hard to say how long to kill an enemy. seems pretty darn quick mostly. Call it a second.
e.addAbility("Abominable Might", 12.0/19, {"chaos":336.5, "chaos %":230, "health %":20, "physical to chaos":50})
f = Star(abomination, c, {"offense":20, "poison %":80, "health":150})
g = Star(abomination, f, {"acid %":100, "poison %":100})
h = Star(abomination, g, {})
#15% on attack
#3 second recharge
#6 attacks recharge, 6.66 attacks trigger
# 10 meter radius
# call it 4 targets
h.addAbility("Tainted Eruption", 4/12.66, {"triggered poison":1320, "stun %":100})

sage = Constellation("Blind Sage", "10a 18e")
a = Star(sage, [], {"offense":15, "spirit":25})
b = Star(sage, a, {"offense":15, "elemental %":80})
c = Star(sage, b, {"crit damage":10, "skill disruption protection":30})
d = Star(sage, c, {"cold resist":20, "cold %":100, "frostburn %":100})
e = Star(sage, c, {"lightning %":100, "electrocute %":100, "lightning resist":20})
f = Star(sage, c, {"fire %":100, "burn %":100, "fire resist":20})
g = Star(sage, f, {})
#100% on attack
# 1.5 second recharge
# 5 s lifespan
# call it 2 attacks and a detonate each hitting 2 targets
# 4 attacks per
g.addAbility("Elemental Seeker", 1.0/4, {"triggered elemental":60*2*2+132*2, "stun %":100})

wolf = Constellation("Mogdrogen the Wolf", "15a 12e")
a = Star(wolf, [], {"offense":35, "pet offense %":5})
b = Star(wolf, a, {"bleed %":80, "pet all damage %":30})
c = Star(wolf, b, {"vitality resist":20, "pet total speed":6})
d = Star(wolf, c, {"bleed":25*5, "bleed %":80})
e = Star(wolf, d, {"bleed resist":15, "elemental resist":15, "max bleed resist":3, "pet all damage %":80})
f = Star(wolf, e, {})
#20% on attack
#15 s recharge
#10 s duration
# 5 attack trigger = 2.5 s
f.addAbility("Howl of Mogdrogen", 10/17.5, {"triggered bleed":396, "bleed %":200, "offense":120*.38, "attack speed":15, "pet offense %":15, "pet total speed":35})

rat = Constellation("Rat", "1c", "2c 3e")
a = Star(rat, [], {"cunning":8, "spirit":8})
b = Star(rat, a, {"poison":8*5, "poison %":24})
c = Star(rat, b, {"acid resist":10, "cunning":15, "spirit":15})
d = Star(rat, c, {"poison":12*5, "poison %":20, "poison duration":30})

ghoul = Constellation("Ghoul", "1c", "3c")
a = Star(ghoul, [], {"physique":10})
b = Star(ghoul, a, {"health/s":6, "life leech":15*2})
c = Star(ghoul, b, {"physique":10, "spirit":10})
d = Star(ghoul, b, {"health regeneration":15, "lifesteal %":4})
e = Star(ghoul, d, {})
# 100% at 33% health
# 30s recharge
# 6s duration
# lets say we hit 33% 1 / 3 fights
e.addAbility("Ghoulish Hunger", 6.0/30/3, {"life leach":442, "life leach %":135, "lifesteal %":60, "attack speed":20})

jackal = Constellation("Jackal", "1c", "3c")
a = Star(jackal, [], {"energy %":6, "pet health %":3})
b = Star(jackal, a, {"offense":12, "attack speed":6})
c = Star(jackal, b, {"all damage %":15, "pet attack speed":5})

fiend = Constellation("Fiend", "1c", "3c 3e")
a = Star(fiend, [], {"fire %":15, "chaos %":15})
b = Star(fiend, a, {"spirit":10, "pet fire damage %":25})
c = Star(fiend, b, {"chaos resist":8})
d = Star(fiend, c, {"fire %":24, "chaos %":24, "pet fire damage %":40})
e = Star(fiend, d, {})
#25% on attack
#.5 s recharge
#100% pass through
# 2 projectiles
# 2.5 targets
# 1 attack recharge, 4 attack trigger
e.addAbility("Flame Torrent", 2.5/5, {"weaopn damage %":35, "triggered fire":132, "triggered chaos":56, "triggered burn":504})

viper = Constellation("Viper", "1c", "2c 3p")
a = Star(viper, [], {"spirit":10})
b = Star(viper, a, {"energy absorb":10, "energy leech":18*2*.15})
c = Star(viper, b, {"vitality resist":10})
d = Star(viper, c, {"offense %":3, "reduce elemental resist":20})

vulture = Constellation("Vulture", "1c", "5c")
a = Star(vulture, [], {"cunning":10})
b = Star(vulture, a, {"bleed resist":15})
c = Star(vulture, b, {"life leech":15*2, "life leech resist":30})
d = Star(vulture, b, {"cunning %":5})
e = Star(vulture, b, {"vitality resist":15, "life leech %":50})

wendigo = Constellation("Wendigo", "4c 6p", "2c")
a = Star(wendigo, [], {"vitality %":40, "vitality decay %":40})
b = Star(wendigo, a, {"spirit":15, "health":100})
c = Star(wendigo, b, {"cast speed":5, "vitality resist":10})
d = Star(wendigo, c, {"health %":5, "damage from beasts":-10})
e = Star(wendigo, d, {"vitality %":50, "vitality decay %":50, "life leech %":50})
f = Star(wendigo, e, {})
# 25% on attack
# 8s duration
# I have no idea how this one works. I'm guessing vitality damage per second for the duration.
f.addAbility("Wendigo's Mark", .5, {"triggered vitality":186, "health":186*.9})

hydra = Constellation("Hydra (requires ranged)", "3a 3c 5e", "2c 3e")
a = Star(hydra, [], {"offense":15})
b = Star(hydra, a, {"all damage %":15})
c = Star(hydra, b, {"pierce %": 40})
d = Star(hydra, b, {"offense":20})
e = Star(hydra, d, {"offense %":3, "slow resist":20})
f = Star(hydra, b, {"all damage %":35})

chariot = Constellation("Chariot of the Dead", "5a 5e", "2c 3e")
a = Star(chariot, [], {"cunning":15})
b = Star(chariot, a, {"offense":15})
c = Star(chariot, b, {"cunning":20})
d = Star(chariot, c, {"vitality resist":10})
e = Star(chariot, c, {"offense":25})
f = Star(chariot, e, {"offense %":3, "offense":10})
g = Star(chariot, f, {})
# 100% when hit by critical: ??? .15% when hit
#18 s recharge
#7 s duration
#6.66 s to trigger so 7/24.66
g.addAbility("Wayward Soul", 7/24.66, {"health %":10, "health":1300, "defense":120})

revenant = Constellation("Revenant", "8c", "1c 1p")
a = Star(revenant, [], {"energy leech":20*2*.1, "lifesteal %":3})
b = Star(revenant, a, {"health %":3, "damage from undead":-10})
c = Star(revenant, b, {"vitality resist":20, "pet vitality resist":15})
d = Star(revenant, c, {"energy absorb":15, "lifesteal %":6})
e = Star(revenant, d, {"damage undead %":15, "attack speed":6, "pet lifesteal %":5})
f = Star(revenant, e, {})
#100% on enemy death
#3 s recharge
#5 summon limit
# 25 s lifespan
# 10 attacks per summon (1/2.5s)
#scales with pet bonuses which I don't have an answer for
# 1-26 = 10
# 5-30 = 10
# 9-34 = 8
# 13-38 = 6
# 17-42 = 5
f.addAbility("Raise the Dead", 39, {"triggered physical":18, "slow move":.25})

torch = Constellation("Ulzuin's Torch", "8c 15e")
a = Star(torch, [], {"offense":20, "fire %":80})
b = Star(torch, a, {"offense %":5, "chaos resist":15})
c = Star(torch, b, {"move %":5, "crit damage":10})
d = Star(torch, c, {"fire %":100, "fire resist":20})
e = Star(torch, d, {"burn":25*3, "burn %":100, "max fire resist":3})
f = Star(torch, c, {"burn %":100, "burn duration":100})
g = Star(torch, f, {})
#30% on attack
#3.5s recharge
#3 s duration
#6m area
#2m radius
#15 meteors
#call it 15 hits...
# 3.3 attacks trigger, 7 attacks recharge
g.addAbility("Meteor Shower", 15/10.3, {"triggered fire":90, "triggered physical":90, "triggered burn":164/2})

god = Constellation("Dying God", "8c 15p")
a = Star(god, [], {"offense":20, "vitality %":80})
b = Star(god, a, {"offense":20, "chaos %":80})
c = Star(god, b, {"offense %":3, "spirit":25, "pet all damage %":30, "pet attack speed":5})
d = Star(god, c, {"offense":45, "chaos resist":15})
e = Star(god, d, {"vitality %":100, "chaos %":100})
f = Star(god, e, {"chaos":(5+24)/2, "pet all damage %":60, "pet crit damage":10})
g = Star(god, f, {})
#100% on attack
#30s recharge
#20s duration
#12 meter radius
g.addAbility("Hungering Void", 20.0/31, {"health/s":-275, "crit damage":30, "vitality %":215, "chaos%":215, "total speed":8, "chaos retaliation":485, "terrify retaliation":55, "pet all damage %":150, "pet crit damage":20, "stun %":10, "slow move":30*.45})

imp = Constellation("Imp", "1p", "3e 3p")
a = Star(imp, [], {"fire %":15, "aether %":15})
b = Star(imp, a, {"spirit":10})
c = Star(imp, b, {"aether resist":8})
d = Star(imp, c, {"fire %":24, "aether %":24})
e = Star(imp, d, {})
#15% on attack
#3s duration
#2.5 radius
#1.5 targets
e.addAbility("Aetherfire", 1.5/6.66, {"trigered fire":50, "triggered aether":125, "stun %":33})

tsunami = Constellation("Tsunami", "1p", "5p")
a = Star(tsunami, [], {"lightning %": 15, "cold %":15})
b = Star(tsunami, a, {"spirit":10})
c = Star(tsunami, b, {"electrocute %":40, "frostburn %":40})
d = Star(tsunami, c, {"lightning %":24, "cold %":24})
e = Star(tsunami, d, {})
#35% on attack
#1.5s recharge
#12m range
# call it 2 targets
#2.85 attacks trigger, 3 attacks recharge
e.addAbility("Tsunami", 2/5.85, {"weapon damage %":32, "triggered cold":115, "triggered lightning":51})

gallows = Constellation("Gallows", "1p", "5p")
a = Star(gallows, [], {"vitality %":15})
b = Star(gallows, a, {"life leech retaliation":100*.15})
c = Star(gallows, b, {"vitality resist":10})
d = Star(gallows, c, {"vitality":7, "vitality %":24, "chaos %":24})

lizard = Constellation("Lizard", "1p", "4p")
a = Star(lizard, [], {"health/s":6, "constitution %":15})
b = Star(lizard, a, {"health/s":10, "health":50})
c = Star(lizard, b, {"constitution %":15, "health regeneration":15})

guide = Constellation("Sailor's Guide", "1p", "5p")
a = Star(guide, [], {"physique":10})
b = Star(guide, a, {"reduced freeze":15, "slow resist":15})
c = Star(guide, b, {"move %":5, "physique":10})
d = Star(guide, b, {"cold resist":15, "lightning resist":15})

bull = Constellation("Bull", "1p", "2o 3p")
a = Star(bull, [], {"physique":10})
b = Star(bull, a, {"internal %":24, "internal duration":20})
c = Star(bull, b, {"stun %":8, "stun duration":10})
d = Star(bull, c, {"internal":12*5, "armor physique requirements":-10})
e = Star(bull, d, {})
#25% on attack
#.5s recharge
#3.5 meter radius
# 2 targets
# 4 attacks trigger, 1 attack recharge
e.addAbility("Bull Rush", 2.0/5, {"weapon damage %":45, "triggered physical":114, "triggered internal":250})

wraith = Constellation("Wraith", "1p", "3a 3p")
a = Star(wraith, [], {"aether %":15, "lightning %":15})
b = Star(wraith, a, {"spirit":10, "aether resist":8})
c = Star(wraith, a, {"energy absorb":15, "offense":10})
d = Star(wraith, a, {"aether":4, "aether %":24, "lightning":(1+7)/2, "lightning %":24})

eel = Constellation("Eel", "1p", "5p")
a = Star(eel, [], {"defense":10, "avoid melee":2})
b = Star(eel, a, {"defense":10, "avoid ranged":2})
c = Star(eel, b, {"pierce resist":10, "defense":10})

hound = Constellation("Hound", "1p", "4p")
a = Star(hound, [], {"physique":10, "pet health %":4})
b = Star(hound, a, {"armor %":2, "pierce retaliation":30, "retaliation %":20})
c = Star(hound, b, {"armor %":2, "physique":15, "retaliation %":30, "pet retaliation %":30})

messenger = Constellation("Messenger of War", "3a 7p", "2c 3p")
a = Star(messenger, [], {"pierce retaliation":90, "retaliation %":30})
b = Star(messenger, a, {"move %":5, "physique":10})
c = Star(messenger, b, {"armor":50, "retaliation %":50})
d = Star(messenger, c, {"armor %":6, "pierce retaliation":120})
e = Star(messenger, b, {"pierce resist":15, "damage reflect %":25})
f = Star(messenger, e, {})
# 20% when hit
# 15s recharge
# 8s duration
f.addAbility("Messenger of War", 8/17.5, {"move speed":30, "slow resist":70, "pierce retaliation":2400, "retaliation %":200})

tempest = Constellation("Tempest", "5a 5p", "1e 1p")
a = Star(tempest, [], {"lightning %":40})
b = Star(tempest, a, {"lightning":(1-24)/2})
c = Star(tempest, b, {"lightning %":50, "electrocute %":50})
d = Star(tempest, c, {"offense":10, "lightning resist":25})
e = Star(tempest, d, {"move %":3, "lightning %":200*.3})
f = Star(tempest, d, {"offense":15, "electrocute %":50, "electrocute duration":30})
g = Star(tempest, f, {})
#100% on critical: 15% on attack
#10s recharge
#6s duration
# 3 target max
# 8 meter radius
# .5s interval
# 36/26.66
g.addAbility("Reckless Tempest", 12*3/26.66, {"triggered lightning":113.5, "triggered, electrocute":256/2, "stun %":20})

widow = Constellation("Widow", "6e 4p", "3p")
a = Star(widow, [], {"aether %":40})
b = Star(widow, a, {"offense":18, "energy %":5})
c = Star(widow, b, {"aether %":30, "spirit":10})
d = Star(widow, c, {"vitality resist":8, "aether resist":18})
e = Star(widow, d, {"aether %":50, "lightning %":50})
f = Star(widow, e, {})
#25% on attack
#2s recharge
# 2 targets
# 4 attack to trigger 4 to recharge
f.addAbility("Arcane Bomb", 2.0/8, {"triggered lightning":40, "triggered aether":40, "defense":35, "reduce lightning resist":5, "reduce aether resist":5})

kraken = Constellation("Kraken (requires two-hand)", "5e 5p", "2c 3p")
a = Star(kraken, [], {"all damage %":35})
b = Star(kraken, a, {"physical %":40, "attack speed":10})
c = Star(kraken, a, {"physical %":40, "attack speed":10})
d = Star(kraken, a, {"all damage %":50, "move %":5})
e = Star(kraken, a, {"all damage %":35, "crit damage":15})

winter = Constellation("Amatok the Spirit of Winter", "4e 6p", "1e 1p")
a = Star(winter, [], {"cold %":40})
b = Star(winter, a, {"health %":3, "defense":15})
c = Star(winter, b, {"cold resist":25, "offense":10})
d = Star(winter, b, {"cold %":50, "frostburn %":50})
e = Star(winter, d, {"frostburn":12*3, "frostburn %":70})
f = Star(winter, b, {"offense":15, "frostburn %":30, "frostburn duration":30})
g = Star(winter, f, {})
#100% on crit: 15% on attack
#3.5s recharge
#1.5m radius
#6.66 attacks to trigger, 7 attacks to recharge
#looks like there are multiple missiles but it's not listed
g.addAbility("Blizzard", 4.0/13.66, {"weapon damage %":10, "triggered cold":165.5, "triggered frostburn":164, "stun %":36, "slow move":54})

bear = Constellation("Dire Bear", "5a 5p", "1a 1p")
a = Star(bear, [], {"physical %":40})
b = Star(bear, a, {"physique":10, "cunning":10})
c = Star(bear, b, {"constitution %":15, "attack speed":5})
d = Star(bear, c, {"reduced stun duration":15, "reduced freeze duration":15, "health %":5})
e = Star(bear, [], {"physical %":50, "internal %":50})
f = Star(bear, d, {})
#15% on attack
#1s recharge
#4m radius
#2 targets
f.addAbility("Maul", 2.0/8.66, {"weapon damage %":75, "triggered physical":161.5, "stun %":100})

ulo = Constellation("Ulo the Keeper of the Waters", "4o 6p", "2o 3p")
a = Star(ulo, [], {"elemental resist":10, "pet elemental resist":10})
b = Star(ulo, a, {"life leech resist":30, "energy leech resist":30})
c = Star(ulo, b, {"acid resist":15, "pet acid resist":15})
d = Star(ulo, b, {"chaos resist":10, "pet chaos resist":10})
e = Star(ulo, b, {})
# 100% on attack
#22s recharge
#1s duration (actually 8)
#3m radius
#2 targets
# 44 attacks recharge, 1 attack trigger
e.addAbility("Cleansing Waters", 8.0/45, {"slow move":40})

watcher = Constellation("Solemn Watcher", "10p", "2o 3p")
a = Star(watcher, [], {"physique":15})
b = Star(watcher, a, {"cold resist":25})
c = Star(watcher, b, {"pierce resist":18})
d = Star(watcher, c, {"defense":30, "physique %":3})
e = Star(watcher, d, {"defense %":5, "reflected damage reduction":20})

hourglass = Constellation("Aeon's Hourglass", "8c 18p")
a = Star(hourglass, [], {"physique":30, "cunning":30, "spirit":30})
b = Star(hourglass, a, {"defense":25, "reduced burn duration":20, "reduced frostburn duration":20, "reduced electrocute duration":20})
c = Star(hourglass, b, {"slow resist":50, "aether resist":20})
d = Star(hourglass, c, {"defense":35, "vitality resist":15, "max vitality resist":4})
e = Star(hourglass, d, {"avoid melee":6, "avoid ranged":6, "reduced entrapment duration":30, "reflected damage reduction":25})
f = Star(hourglass, e, {})
#30 chance when hit
#3s recharge
#3m radius
# 3.33 for trigger, 6 for recharge
# 1.5 targets
f.addAbility("Time Stop", 1.5/9.33, {"stun %":100, "slow move":70})

spear = Constellation("Spear of the Heavens", "7c 20p")
a = Star(spear, [], {"offense":20, "lightning %":80})
b = Star(spear, a, {"offense":20, "aether %":80})
c = Star(spear, b, {"offense %":5, "aether resist":15})
d = Star(spear, c, {"crit damage":10, "lightning resist":20})
e = Star(spear, d, {"aether %":100, "lightning %":100, "max lightning resist":3})
f = Star(spear, e, {})
#50% when hit
#1s recharge
#.5m radius
#2 for recharge, 2 for trigger
f.addAbility("Spear of the Heavens", 1.0/4, {"triggered lightning":162, "triggered aether":176, "stun %":100})

tree = Constellation("Tree of Life", "7o 20p")
a = Star(tree, [], {"health %":5, "pet health %":5})
b = Star(tree, a, {"health/s":20, "pet health regeneration":20})
c = Star(tree, b, {"health %":8, "pet health %":5})
d = Star(tree, b, {"health/s":15, "defense":30, "pet health regeneration":20})
e = Star(tree, d, {"health %":4, "health regeneration":20, "pet health/s":50})
f = Star(tree, d, {})
#25% when hit
#12s recharge
#8s 2 per
f.addAbility("Healing Rain", 16.0/28, {"health/s":100, "energy/s":10, "health regeneration":50, "energy regeneration":50, "health%":10*2, "health":550*2})

empyrion = Constellation("Light of Empyrion", "8o 18p")
a = Star(empyrion, [], {"elemental resist":10, "pet elemental resist":10}) #not quite right but close enough
b = Star(empyrion, a, {"fire %":80, "damage chthonics %":10})
c = Star(empyrion, b, {"elemental resist":15, "pet elemental resist":15})
d = Star(empyrion, c, {"vitality resist":15, "pet vitality resist":15})
e = Star(empyrion, d, {"aether resist":15, "chaos resist":15, "pet aether resist":15, "pet chaos resist":15})
b = Star(empyrion, a, {"fire":(8+14)/2, "max aether resist":3, "max chaos resist":3, "pet max all resist":5})
g = Star(empyrion, f, {})
#20% when attacked
#4s recharge
#5m radius
# 2 targets
# 8 recharge, 5 triggerd
g.addAbility("Light of Empyrion", 2.0/13, {"weapon damage %":35, "triggered fire":226, "triggered burn":204, "stun %":50, "reduce armor":225, "damage to undead":50, "damage to cthonics":50})