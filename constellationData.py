import re
from operator import *

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
		for bonus in model.keys():
			if bonus in self.bonuses.keys():
				value += model[bonus]*self.bonuses[bonus]
		return value

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

falcon = Constellation("Falcon", "1a", "3a 3e")
a = Star(falcon, [], {"physical %":15})
b = Star(falcon, a, {"bleed %":24})
c = Star(falcon, b, {"cunning":15})
d = Star(falcon, c, {"physical %":24})
e = Star(falcon, d, {"Falcon Swoop":True})

shepherd = Constellation("Shepherd's Crook", "1a", "5a")
a = Star(shepherd, [], {"health":40})
b = Star(shepherd, a, {"cunning":10, "health":40})
c = Star(shepherd, b, {"elemental resist":10})
d = Star(shepherd, c, {"health %":3})
e = Star(shepherd, d, {"Shepherd's Call":True})

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

owl = Constellation("Owl", "1a", "5a")
a = Star(owl, [], {"spirit":10})
b = Star(owl, a, {"elemental resist":8, "skill cost %":-5})
c = Star(owl, b, {"burn %":30, "electrocute %":30, "frostburn %":30})
d = Star(owl, b, {"elemental %":24})

harpy = Constellation("Harpy", "1a", "5a")
a = Star(harpy, [], {"pierce %":15, "cold %":15})
b = Star(harpy, a, {"cunning":10})
c = Star(harpy, b, {"bleed resist":10, "offense":15})
d = Star(harpy, b, {"pierce":(3+7)/2, "pierce %":24, "cold %":24})

throne = Constellation("Empty Throne", "1a", "5a")
a = Star(throne, [], {"reduced stun":15})
b = Star(throne, a, {"pierce resist":8})
c = Star(throne, b, {"???":False})
d = Star(throne, b, {"???":False})

wolverine = Constellation("Wolverine", "1a", "6a")
a = Star(wolverine, [], {"defense":15})
b = Star(wolverine, a, {"pierce retaliation":30})
c = Star(wolverine, b, {"defense":18})
d = Star(wolverine, c, {"???":False})
e = Star(wolverine, c, {"defense %":3})

crab = Constellation("Crab", "6a 4o", "3a")
a = Star(crab, [], {"constitution %":15, "physique":20})
b = Star(crab, a, {"elemental %":30, "internal %":70})
c = Star(crab, b, {"Elemental Barrier":True})
d = Star(crab, c, {"pierce resist":18, "defense":10})
e = Star(crab, d, {"elemental %":40, "elemental resist":15})

scepter = Constellation("Rhowan's Scepter", "6a 4o", "3a 2o")
a = Star(scepter, [], {"defense":15})
b = Star(scepter, a, {"health %":6})
c = Star(scepter, b, {"physical %":50})
d = Star(scepter, c, {"internal %":80})
e = Star(scepter, b, {"defense":18})
f = Star(scepter, e, {"physical":(8+12)/2,"stun %":5})

boar = Constellation("Autumn Boar", "4a 3o 4p", "3a")
a = Star(boar, [], {"physique":10, "cunning":10})
b = Star(boar, a, {"pierce resist":15, "physique":10})
c = Star(boar, b, {"physique %":5})
d = Star(boar, c, {"physical resist":4, "fire resist":20})
e = Star(boar, c, {"???":False})
f = Star(boar, e, {"???":False})
g = Star(boar, e, {"Trample":True})

scythe = Constellation("Harvestman's Scythe", "3a 3o 5p", "3a 3p")
a = Star(scythe, [], {"energy/s":2})
b = Star(scythe, a, {"health/s":12})
c = Star(scythe, b, {"physique %":4, "constitution %":20})
d = Star(scythe, c, {"health regeneration":20})
e = Star(scythe, d, {"energy regeneration":20})
f = Star(scythe, e, {"cunning %":4, "spirit %":4})

crown = Constellation("Rhowan's Crown", "4a 6e", "1a 1e")
a = Star(crown, [], {"elemental %":30, "elemental":(6+9)/2})
b = Star(crown, a, {"spirit":20})
c = Star(crown, b, {"Elemental Storm":True})
d = Star(crown, c, {"elemental resist":18})
e = Star(crown, d, {"elemental %":40, "burn %":60, "electrocute %":60, "frostburn %":60})

huntress = Constellation("Huntress", "4a 3c 4e", "1a 1e")
a = Star(huntress, [], {"offense":15})
b = Star(huntress, a, {"pierce %":35})
c = Star(huntress, b, {"bleed %":60})
d = Star(huntress, c, {"pierce resist":8, "damage beast %":15, "health":100})
e = Star(huntress, c, {"offense %":3})
f = Star(huntress, e, {"bleed":10*3, "bleed %":50})
g = Star(huntress, e, {"Rend":True})

leviathan = Constellation("Leviathan", "13a 13e")
a = Star(leviathan, [], {"cold":8, "cold %":80})
b = Star(leviathan, a, {"health %":5, "physique":25})
c = Star(leviathan, b, {"defense":26, "energy regeneration":20})
d = Star(leviathan, c, {"pierce resist":20, "cold resist":20})
e = Star(leviathan, d, {"cold":(12+16)/2, "cold %":100})
f = Star(leviathan, d, {"frostburn":25*3, "frostburn %":100})
g = Star(leviathan, d, {"Whirlpool":True})

oleron = Constellation("Oleron", "20a 7o")
a = Star(oleron, [], {"physique":20, "cunning":20, "health":100})
b = Star(oleron, a, {"physical %":80, "internal %":80})
c = Star(oleron, b, {"pierce resist":20, "bleed resist":10, "offense":30})
d = Star(oleron, c, {"physical resist":4, "health":200})
e = Star(oleron, d, {"physical":(9+18)/2, "physical %":100})
f = Star(oleron, d, {"offense":15, "internal":25*5, "internal %":100})
g = Star(oleron, d, {"Blind Fury":True})

tortoise = Constellation("Tortoise", "1o", "2o 3p")
a = Star(tortoise, [], {"defense":10, "health":25})
b = Star(tortoise, a, {"defense":12})
c = Star(tortoise, b, {"defense":12, "health":100})
d = Star(tortoise, c, {"health %":4, "defense":10, "armor %":4})
e = Star(tortoise, c, {"Turtle Shell":True})

blade = Constellation("Assassin's Blade", "1o", "3a 2o")
a = Star(blade, [], {"pierce %":15})
b = Star(blade, a, {"offense":12})
c = Star(blade, a, {"bleed %":15, "pierce %":15})
d = Star(blade, c, {"bleed %":30})
e = Star(blade, d, {"Assassin's Mark":True})

lion = Constellation("Lion", "1o", "3o")
a = Star(lion, [], {"health %":4, "defense":8})
b = Star(lion, a, {"spirit":10, "health":100})
c = Star(lion, b, {"all damage %":15})

crane = Constellation("Crane", "1o", "5o")
a = Star(crane, [], {"physique":8, "spirit":8})
b = Star(crane, a, {"poison resist":12})
c = Star(crane, b, {"all damage %":15})
d = Star(crane, c, {"vitality resist":8})
e = Star(crane, d, {"elemental resist":10})

panther = Constellation("Panther", "1o", "2o 3p")
a = Star(panther, [], {"offense":12})
b = Star(panther, a, {"cunning":8, "spirit":8})
c = Star(panther, b, {"all damage %":15, "energy regeneration":10})
d = Star(panther, c, {"offense":20})

dryad = Constellation("Dryad", "1o", "3o")
a = Star(dryad, [], {"poison resist":10, "energy":200})
b = Star(dryad, a, {"energy/s":1, "health":80})
c = Star(dryad, b, {"???":False})
d = Star(dryad, c, {"spirit %":5})
e = Star(dryad, d, {"Dryad's Blessing":True})

shieldmaiden = Constellation("Shieldmaiden", "4o 6p", "2o 3p")
a = Star(shieldmaiden, [], {"block %":4})
b = Star(shieldmaiden, a, {"armor absorb":5})
c = Star(shieldmaiden, b, {"???":False})
d = Star(shieldmaiden, c, {"???":False})
e = Star(shieldmaiden, b, {"reduced stun":25})
f = Star(shieldmaiden, e, {"shield recovery":15, "stun retaliation":15})

scales = Constellation("Scales of Ulcama", "8o", "2o")
a = Star(scales, [], {"health":250, "energy":300})
b = Star(scales, a, {"health/s":6, "health regeneration":10})
c = Star(scales, b, {"health %":6})
d = Star(scales, c, {"energy regeneration":10, "energy/s":2})
e = Star(scales, b, {"all damage %":30})
f = Star(scales, e, {"Tip the Scales":True})

assassin = Constellation("Assassin", "6a 4o", "1a 1o")
a = Star(assassin, [], {"pierce %":30})
b = Star(assassin, a, {"cunning":15})
c = Star(assassin, b, {"offense":18, "defense":10})
d = Star(assassin, b, {"bleed resist":8, "cunning %":5})
e = Star(assassin, d, {"defense":12, "poison resist":8, "damage human %":15})
f = Star(assassin, d, {"pierce":6, "pierce %":40})
g = Star(assassin, f, {"Blades of Wrath":True})

blades = Constellation("Blades of Nadaan", "10a", "3a 2o")
a = Star(blades, [], {"avoid melee":2, "avoid ranged":2})
b = Star(blades, a, {"pierce %":40})
c = Star(blades, b, {"pierce %":50})
d = Star(blades, b, {"attack speed":5})
e = Star(blades, b, {"attack speed":5})
f = Star(blades, b, {"???":False})

targo = Constellation("Targo the Builder", "4o 6p", "1o")
a = Star(targo, [], {"defense":15})
b = Star(targo, a, {"health %":5})
c = Star(targo, b, {"armor %":5})
d = Star(targo, b, {"health %":5})
e = Star(targo, d, {"defense":20, "health":200})
f = Star(targo, d, {"armor %":5})
g = Star(targo, f, {"Shield Wall":True})

obelisk = Constellation("Obelisk of Menhir", "8o 15p")
a = Star(obelisk, [], {"armor %":7})
b = Star(obelisk, a, {"defense":30, "armor":150})
c = Star(obelisk, b, {"???":False})
d = Star(obelisk, a, {"defense %":5, "defense":25})
e = Star(obelisk, d, {"block %":5})
f = Star(obelisk, e, {"reduced stun":30, "reduced freeze":30, "armor %":4})
g = Star(obelisk, f, {"Stone Form":True})

soldier = Constellation("Unknown Soldier", "15a 8o")
a = Star(soldier, [], {"offense":15, "pierce %":60})
b = Star(soldier, a, {"bleed":18*3, "bleed %":80})
c = Star(soldier, b, {"lifesteal %":3, "attack speed":5, "health":150})
d = Star(soldier, b, {"bleed %":80, "pierce %":80})
e = Star(soldier, d, {"health %":4, "offense":40})
f = Star(soldier, e, {"pierce":15, "crit damage":10})
g = Star(soldier, f, {"Living Shadow":True})

scorpion = Constellation("Scorpion", "1e", "5e")
a = Star(scorpion, [], {"offense":12})
b = Star(scorpion, a, {"poison %":24})
c = Star(scorpion, b, {"offense":18})
d = Star(scorpion, c, {"acid %":15, "poison %":30})
e = Star(scorpion, c, {"Scorpion Sting":True})

eye = Constellation("Eye of the Guaridan", "1e", "3a 3e")
a = Star(eye, [], {"acid %":15, "poison %":15})
b = Star(eye, a, {"chaos %":15})
c = Star(eye, b, {"chaos %":15, "poison %":15})
d = Star(eye, c, {"poison %":30})
e = Star(eye, d, {"Guardian's Gaze":True})

bat = Constellation("Bat", "1e", "2c 3e")
a = Star(bat, [], {"vitality %":15, "bleed %":15})
b = Star(bat, a, {"???":False})
c = Star(bat, b, {"vitality %":24, "bleed %":30})
d = Star(bat, c, {"life leech":30, "lifesteal %":3})
e = Star(bat, d, {"Twin Fangs":True})

spider = Constellation("Spider", "1e", "6e")
a = Star(spider, [], {"cunning":10, "spirit":10})
b = Star(spider, a, {"offense":10})
c = Star(spider, a, {"offense":15, "defense":10})
d = Star(spider, a, {"cunning %":3, "spirit %":3})
e = Star(spider, a, {"cast speed":3})

raven = Constellation("Raven", "1e", "5e")
a = Star(raven, [], {"spirit":8})
b = Star(raven, a, {"energy/s":1, "spirit":10})
c = Star(raven, b, {"offense":15})
d = Star(raven, b, {"all damage %":15})

fox = Constellation("Fox", "1e", "5e")
a = Star(fox, [], {"cunning":10})
b = Star(fox, a, {"bleed":8*3, "bleed %":24})
c = Star(fox, b, {"bleed resist":8, "cunning":15})
d = Star(fox, c, {"bleed":12*3, "bleed %":45})

light = Constellation("Scholar's Light", "1e", "4e")
a = Star(light, [], {"fire %":15})
b = Star(light, a, {"elemental resist":8, "physique":10})
c = Star(light, b, {"elemental %":24, "elemental":6, "energy/s":1.5})

hawk = Constellation("Hawk", "1e", "3e")
a = Star(hawk, [], {"offense":15})
b = Star(hawk, a, {"crit damage":8})
c = Star(hawk, b, {"offense %":3})

witchblade = Constellation("Solael's Witchblade", "4c 6e", "1c 1e")
a = Star(witchblade, [], {"chaos %":40})
b = Star(witchblade, a, {"offense":10, "spirit":10})
c = Star(witchblade, b, {"energy burn %":10, "chaos %":30})
d = Star(witchblade, c, {"fire %":50, "chaos %":50, "fire resist":15})
e = Star(witchblade, d, {"Eldritch Fire":True})

bonds = Constellation("Bysmiel's Bonds", "4c 6e", "3e")
a = Star(bonds, [], {"offense":15})
b = Star(bonds, a, {"cast speed":5})
c = Star(bonds, b, {"vitality resist":15})
d = Star(bonds, c, {"all damage %":30})
e = Star(bonds, d, {"Bysmiel's Command":True})

magi = Constellation("Magi", "10e", "3e")
a = Star(magi, [], {"fire %":40, "burn %":50})
b = Star(magi, a, {"elemental resist":8})
c = Star(magi, b, {"fire resist":25})
d = Star(magi, c, {"cast speed":5, "burn %":60})
e = Star(magi, c, {"fire":(6+8)/2, "fire %":40})
f = Star(magi, c, {"burn":12*3, "burn %":30})
g = Star(magi, f, {"Fissure":True})

berserker = Constellation("Berserker", "5a 5e", "2c 3e")
a = Star(berserker, [], {"offense":15})
b = Star(berserker, a, {"physical %":50})
c = Star(berserker, b, {"offense":25})
d = Star(berserker, a, {"bleed %":80, "lifesteal %":3})
e = Star(berserker, d, {"bleed %":100*.15, "crit damage":5})
f = Star(berserker, f, {"pierce resist":10})

lantern = Constellation("Oklaine's Lantern", "10e", "3e 2o")
a = Star(lantern, [], {"energy regeneration":15})
b = Star(lantern, a, {"offense":25})
c = Star(lantern, b, {"offense":15, "crit damage":5})
d = Star(lantern, c, {"all damage %":50})
e = Star(lantern, d, {"cast speed":5, "attack speed":5, "energy/s":2})

behemoth = Constellation("Behemoth", "3c 4e 4p", "2c 3e")
a = Star(behemoth, [], {"health/s":10})
b = Star(behemoth, a, {"health":300})
c = Star(behemoth, b, {"health/s":15, "constitution %":25})
d = Star(behemoth, b, {"health %":4})
e = Star(behemoth, b, {"health regeneration":10})
f = Star(behemoth, b, {"Giant's Blood":True})

affliction = Constellation("Affliction", "4a 3c 4e", "1a 1e")
a = Star(affliction, [], {"vitality %":40, "poison %":40})
b = Star(affliction, a, {"spirit":15})
c = Star(affliction, b, {"Fetid Pool":True})
d = Star(affliction, c, {"offense":18, "defense":10})
e = Star(affliction, d, {"crit damage":10})
f = Star(affliction, c, {"vitality":(8+15)/2, "poison resist":10})
g = Star(affliction, f, {"offense %":3, "vitality %":50, "acid %":50})

manticore = Constellation("Manticore", "4c 6e", "1a 1e")
a = Star(manticore, [], {"offense":15})
b = Star(manticore, a, {"acid %":50, "poison %":50})
c = Star(manticore, b, {"health %":4})
d = Star(manticore, c, {"offense":10, "poison resist":25})
e = Star(manticore, c, {"poison":8*5, "acid %":40, "poison %":40})
f = Star(manticore, e, {"Acid Spray":True})

abomination = Constellation("Abomination", "8c 18e")
a = Star(abomination, [], {"chaos %":80, "poison %":80})
b = Star(abomination, a, {"vitality %":80, "acid %":80})
c = Star(abomination, b, {"offense":40, "poison resist":20})
d = Star(abomination, c, {"offense":20, "chaos %":80, "health":150})
e = Star(abomination, d, {"Abominable Might":True})
f = Star(abomination, c, {"offense":20, "poison %":80, "health":150})
g = Star(abomination, f, {"acid %":100, "poison %":100})
h = Star(abomination, g, {"Tainted Eruption":True})

sage = Constellation("Blind Sage", "10a 18e")
a = Star(sage, [], {"offense":15, "spirit":25})
b = Star(sage, a, {"offense":15, "elemental %":80})
c = Star(sage, b, {"crit damage":10, "skill disruption protection":30})
d = Star(sage, c, {"cold resist":20, "cold %":100, "frostburn %":100})
e = Star(sage, c, {"lightning %":100, "electrocute %":100})
f = Star(sage, c, {"fire %":100, "burn %":100, "fire resist":20})
g = Star(sage, f, {"Elemental Seeker":True})

wolf = Constellation("Mogdrogen the Wolf", "15a 12e")
a = Star(wolf, [], {"offense":35})
b = Star(wolf, a, {"bleed %":80})
c = Star(wolf, b, {"vitality resist":20})
d = Star(wolf, c, {"bleed":25*5, "bleed %":80})
e = Star(wolf, d, {"bleed resist":15, "elemental resist":15})
f = Star(wolf, e, {"Howl of Mogdrogen":True})

rat = Constellation("Rat", "1c", "2c 3e")
a = Star(rat, [], {"cunning":8, "spirit":8})
b = Star(rat, a, {"poison":8*5, "poison %":24})
c = Star(rat, b, {"poison resist":10, "cunning":15, "spirit":15})
d = Star(rat, c, {"poison":12*5, "poison %":20})

ghoul = Constellation("Ghoul", "1c", "3c")
a = Star(ghoul, [], {"physique":10})
b = Star(ghoul, a, {"health/s":6, "life leech":15*2})
c = Star(ghoul, b, {"physique":10, "spirit":10})
d = Star(ghoul, b, {"health regeneration":15, "lifesteal %":4})
e = Star(ghoul, d, {"Ghoulish Hunger":True})

jackal = Constellation("Jackal", "1c", "3c")
a = Star(jackal, [], {"???":False})
b = Star(jackal, a, {"offense":12, "attack speed":6})
c = Star(jackal, b, {"all damage %":15})

fiend = Constellation("Fiend", "1c", "3c 3e")
a = Star(fiend, [], {"fire %":15, "chaos %":15})
b = Star(fiend, a, {"spirit":10})
c = Star(fiend, b, {"???":False}) # MISSING BONUS
d = Star(fiend, c, {"fire %":24, "chaos %":24})
e = Star(fiend, d, {"Flame Torrent":True})

viper = Constellation("Viper", "1c", "2c 3p")
a = Star(viper, [], {"spirit":10})
b = Star(viper, a, {"energy absorb":10, "energy leech":18*2*.15})
c = Star(viper, b, {"vitality resist":10})
d = Star(viper, c, {"offense %":3})

vulture = Constellation("Vulture", "1c", "5c")
a = Star(vulture, [], {"cunning":10})
b = Star(vulture, a, {"bleed resist":15})
c = Star(vulture, b, {"life leech":15*2})
d = Star(vulture, b, {"cunning %":5})
e = Star(vulture, b, {"vitality resist":15, "life leech":50})

wendigo = Constellation("Wendigo", "4c 6p", "2c")
a = Star(wendigo, [], {"vitality %":40})
b = Star(wendigo, a, {"spirit":15, "health":100})
c = Star(wendigo, b, {"cast speed":5, "vitality resist":10})
d = Star(wendigo, c, {"health %":5})
e = Star(wendigo, d, {"vitality %":50, "life leech":50})
f = Star(wendigo, e, {"Wendigo's Mark":True})

hydra = Constellation("Hydra", "3a 3c 5e", "2c 3e")
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
g = Star(chariot, f, {"Wayward Soul":True})

revenant = Constellation("Revenant", "8c", "1c 1p")
a = Star(revenant, [], {"energy leech":20*2*.1, "lifesteal %":3})
b = Star(revenant, a, {"health %":3})
c = Star(revenant, b, {"vitality resist":20})
d = Star(revenant, c, {"energy absorb":15, "lifesteal %":6})
e = Star(revenant, d, {"damage undead %":15, "attack speed":6})
f = Star(revenant, e, {"Raise the Dead":True})

torch = Constellation("Ulzuin's Torch", "8c 15e")
a = Star(torch, [], {"offense":20, "fire %":80})
b = Star(torch, a, {"offense %":5})
c = Star(torch, b, {"move %":5, "crit damage":10})
d = Star(torch, c, {"fire %":100, "fire resist":20})
e = Star(torch, d, {"burn":25*3, "burn %":100})
f = Star(torch, c, {"burn %":100})
g = Star(torch, f, {"Meteor Shower":True})

god = Constellation("Dying God", "8c 15p")
a = Star(god, [], {"offense":20, "vitality %":80})
b = Star(god, a, {"offense":20, "chaos":80})
c = Star(god, b, {"offense %":3, "spirit":25})
d = Star(god, c, {"offense":45})
e = Star(god, d, {"vitality %":100, "chaos %":100})
f = Star(god, e, {"chaos":(5+24)/2})
g = Star(god, f, {"Hungering Void":True})

imp = Constellation("Imp", "1p", "3e 3p")
a = Star(imp, [], {"fire %":15, "aether %":15})
b = Star(imp, a, {"spirit":10})
c = Star(imp, b, {"???":False})
d = Star(imp, c, {"fire %":24, "aether %":24})
e = Star(imp, d, {"Aetherfire":True})

tsunami = Constellation("Tsunami", "1p", "5p")
a = Star(tsunami, [], {"lightning %": 15, "cold %":15})
b = Star(tsunami, a, {"spirit":10})
c = Star(tsunami, b, {"electrocute %":40, "frostburn %":40})
d = Star(tsunami, c, {"lightning %":24, "cold %":24})
e = Star(tsunami, d, {"Tsunami":True})

gallows = Constellation("Gallows", "1p", "5p")
a = Star(gallows, [], {"vitality %":15})
b = Star(gallows, a, {"???":False})
c = Star(gallows, b, {"vitality resist":10})
d = Star(gallows, c, {"vitality":6, "vitality %":24, "chaos %":24})

lizard = Constellation("Lizard", "1p", "4p")
a = Star(lizard, [], {"health/s":6, "constitution %":15})
b = Star(lizard, a, {"health/s":10, "health":50})
c = Star(lizard, b, {"constitution %":15, "health regeneration":15})

guide = Constellation("Sailor's Guide", "1p", "5p")
a = Star(guide, [], {"physique":10})
b = Star(guide, a, {"reduced freeze":15, "slow resist":15})
c = Star(guide, b, {"move %":5, "physique":10})
d = Star(guide, b, {"cold resist":15})

bull = Constellation("Bull", "1p", "2o 3p")
a = Star(bull, [], {"physique":10})
b = Star(bull, a, {"internal %":24})
c = Star(bull, b, {"stun %":8})
d = Star(bull, c, {"internal":12*5, "armor physique requirements":-10})
e = Star(bull, d, {"Bull Rush":True})

wraith = Constellation("Wraith", "1p", "3a 3p")
a = Star(wraith, [], {"aether %":15, "lightning %":15})
b = Star(wraith, a, {"spirit":10})
c = Star(wraith, a, {"energy absorb":15, "offense":10})
d = Star(wraith, a, {"aether":4, "aether %":24, "lightning":(1+7)/2, "lightning %":24})

eel = Constellation("Eel", "1p", "5p")
a = Star(eel, [], {"defense":10, "avoid melee":2})
b = Star(eel, a, {"defense":10, "avoid ranged":2})
c = Star(eel, b, {"pierce resist":10, "defense":10})

hound = Constellation("Hound", "1p", "4p")
a = Star(hound, [], {"physique":10})
b = Star(hound, a, {"armor %":2, "pierce retaliation":30})
c = Star(hound, b, {"armor %":2, "physique":15})

messenger = Constellation("Messenger of War", "3a 7p", "2c 3p")
a = Star(messenger, [], {"pierce retaliation":90})
b = Star(messenger, a, {"move %":5, "physique":10})
c = Star(messenger, b, {"armor":50})
d = Star(messenger, c, {"armor %":6, "pierce retaliation":120})
e = Star(messenger, b, {"pierce resist":15, "damage reflect":25})
f = Star(messenger, e, {"Messenger of War":True})

tempest = Constellation("Tempest", "5a 5p", "1e 1p")
a = Star(tempest, [], {"lightning %":40})
b = Star(tempest, a, {"lightning":(1-24)/2})
c = Star(tempest, b, {"lightning %":50, "electrocute %":50})
d = Star(tempest, c, {"offense":10})
e = Star(tempest, d, {"move %":3, "lightning %":200*.3})
f = Star(tempest, d, {"offense":15, "electrocute %":50})
g = Star(tempest, f, {"Reckless Tempest":True})

widow = Constellation("Widow", "6e 4p", "3p")
a = Star(widow, [], {"aether %":40})
b = Star(widow, a, {"offense":18})
c = Star(widow, b, {"aether %":30, "spirit":10})
d = Star(widow, c, {"vitality resist":8})
e = Star(widow, d, {"aether %":50, "lightning %":50})
f = Star(widow, e, {"Arcane Bomb":True})

kraken = Constellation("Kraken", "5e 5p", "2c 3p")
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
f = Star(winter, b, {"offense":15, "frostburn %":30})
g = Star(winter, f, {"Blizzard":True})

bear = Constellation("Dire Bear", "5a 5p", "1a 1p")
a = Star(bear, [], {"physical %":40})
b = Star(bear, a, {"physique":10, "cunning":10})
c = Star(bear, b, {"constitution %":15, "attack speed":5})
d = Star(bear, c, {"reduced stun":15, "reduced freeze":15, "health %":5})
e = Star(bear, [], {"physical %":50, "internal %":50})
f = Star(bear, d, {"Maul":True})

ulo = Constellation("Ulo the Keeper of the Waters", "4o 6p", "2o 3p")
a = Star(ulo, [], {"elemental resist":10})
b = Star(ulo, a, {"???":False})
c = Star(ulo, b, {"poison resist":15})
d = Star(ulo, b, {"???":False})
e = Star(ulo, b, {"Cleansing Waters":True})

watcher = Constellation("Solemn Watcher", "10p", "2o 3p")
a = Star(watcher, [], {"physique":10})
b = Star(watcher, a, {"cold resist":25})
c = Star(watcher, b, {"pierce resist":18})
d = Star(watcher, c, {"defense":30, "physique %":3})
e = Star(watcher, d, {"defense %":5})

hourglass = Constellation("Aeon's Hourglass", "8c 18p")
a = Star(hourglass, [], {"physique":30, "cunning":30, "spirit":30})
b = Star(hourglass, a, {"defense":25})
c = Star(hourglass, b, {"slow resist":50})
d = Star(hourglass, c, {"defense":35, "vitality resist":15})
e = Star(hourglass, d, {"avoid melee":6, "avoid ranged":6})
f = Star(hourglass, e, {"Time Stop":True})

spear = Constellation("Spear of the Heavens", "7c 20p")
a = Star(spear, [], {"offense":20, "lightning %":80})
b = Star(spear, a, {"offense":20, "aether %":80})
c = Star(spear, b, {"offense %":5})
d = Star(spear, c, {"crit damage":10})
e = Star(spear, d, {"aether %":100, "lightning %":100})
f = Star(spear, e, {"Spear of the Heavens":True})

tree = Constellation("Tree of Life", "7o 20p")
a = Star(tree, [], {"health %":5})
b = Star(tree, a, {"health/s":20})
c = Star(tree, b, {"health %":8})
d = Star(tree, b, {"health/s":15, "defense":30})
e = Star(tree, d, {"health %":4, "health regeneration":20})
f = Star(tree, d, {"Healing Rain":True})

empyrion = Constellation("Light of Empyrion", "8o 18p")
a = Star(empyrion, [], {"elemental resist":10})
b = Star(empyrion, a, {"fire":(8+14)/2})
c = Star(empyrion, b, {"???":False})
d = Star(empyrion, c, {"vitality resist":15})
e = Star(empyrion, d, {"elemental resist":15})
f = Star(empyrion, e, {"fire %":80, "damage chthonics %":10})
g = Star(empyrion, f, {"Light of Empyrion":True})