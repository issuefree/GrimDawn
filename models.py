import os, sys

from dataModel import *
from constellationData import *
from utils import *

class Model:
	def __init__(self, name, stats, bonuses, points):
		self.name = name
		self.stats = stats
		self.bonuses = bonuses
		self.points = points

	@staticmethod
	def loadModel(name):
		file = open(name.lower() + "/" + name.lower() + ".py", "r")
		exec(file.read(), locals())
		print locals()["devotionPoints"]
		return Model(name, locals()["stats"], locals()["weights"], locals()["devotionPoints"] )

	def initialize(self, loadSeeds=True):
		self.checkModel()

		self.seedSolutions = []
		if loadSeeds:
			self.readSeedSolutions()


	def __str__(self):
		out = ""
		for key in sorted(self.bonuses.keys()):
			if self.get(key) > 0:
				out += key + " " + str(self.bonuses[key]) + "\n"
		return out

	def saveSeedSolutions(self):
		try:
			os.mkdir(self.name.lower())
		except:
			pass

		file = open(self.name.lower()+"/solutions.py", 'w')
		out = "self.seedSolutions = [\n"
		for s in sorted(self.seedSolutions, key=lambda c: evaluateSolution(c, self), reverse=True):
			out += "  "+solutionPath(s)+ "  # " + str(int(evaluateSolution(s, self))) + "\n"
		out += "]"
		file.write(out)
		file.close()

	def readSeedSolutions(self):
		try:
			file = open(self.name.lower()+"/solutions.py", "r")
			lines = file.read()
			exec(lines)
		except:
			pass

		self.saveSeedSolutions()

	def checkModel(self):
		print "Checking model..."
		print "  "+self.name

		self.stats["allAttacks/s"].sort(reverse=True)

		if self.get("attack opportunity cost") == 0:
			self.bonuses["attack opportunity cost"] = -self.get("weapon damage %")
			print "  attack opportunity cost", self.bonuses["attack opportunity cost"]

		if not "allAttacks/s" in self.stats.keys():
			self.stats["allAttacks/s"] = [self.stats["attacks/s"]]

		if not "fight length" in self.stats.keys():
			self.stats["fight length"] = 30

		self.stats["criticals/s"] = self.getStat("attacks/s")*self.getStat("crit chance")

		# /s stats can be calculated based on fight length and the value of the stat

		#1 health/s for a 30s fight is equal to... 30 health, consider the character's % regen stat
		parts = ["health", "energy"]
		for part in parts:
			hps = self.get(part) * self.getStat("fight length") * max(1, self.getStat(part+" regeneration")/100)
			if part == "energy":
				hps = hps * 2
			if self.get(part+"/s") > 0:
				print "  < "+part+"/s:", self.get(part+"/s"), "!=", hps
			else:
				print "  "+part+"/s", hps
				self.set(part+"/s", hps)

		# physique grants health/s, health and defense so this should be accounted for
		val = 0
		val += self.get("health/s") * .04
		val += self.get("health") * 3
		val += self.get("defense") * .5

		self.setIfNull("physique", val)
		print "  physique:", self.get("physique")

		# cunning grants physical %, pierce %, bleed %, internal % and offense.
		val = 0
		val += self.get("physical %") * .33
		val += self.get("pierce %") * .285
		val += self.get("bleed %") * .333
		val += self.get("internal %") * .333
		val += self.get("offense") * .5

		self.setIfNull("cunning", val)
		print "  cunning:", self.get("cunning")

		# spirit grants fire %, burn %, cold %, frostburn %, lightning %, electrocute %, acid %, poison %, vitality %, vitality decay%, aether %, chaos %, energy and energy regen
		val = 0
		val += sum([self.get(b) for b in ["fire %", "cold %", "lightning %", "acid %", "vitality %", "aether %", "chaos %"]]) * .33
		val += sum([self.get(b) for b in ["burn %", "frostburn %", "electrocute %", "poison %", "vitality decay %"]]) * .333
		val += self.get("energy") * 2
		val += self.get("energy/s") * .01

		self.setIfNull("spirit", val)
		print "  spirit:", self.get("spirit")

		# update damage % stats
		self.stats["physical %"] = self.getStat("physical %") + 100 + self.getStat("cunning")*.33
		self.stats["pierce %"] = self.getStat("pierce %") + 100 + self.getStat("cunning")*.285
		self.stats["bleed %"] = self.getStat("bleed %") + 100 + self.getStat("cunning")*.333
		self.stats["internal %"] = self.getStat("internal %") + 100 + self.getStat("cunning")*.333

		for dam in ["fire %", "cold %", "lightning %", "acid %", "vitality %", "aether %", "chaos %"]:
			if self.getStat(dam) > 0:
				self.stats[dam] = self.getStat(dam) + 100 + self.getStat("spirit")*.33

		for dam in ["burn %", "frostburn %", "electrocute %", "poison %", "vitality decay %"]:
			if self.getStat(dam) > 0:
				self.stats[dam] = self.getStat(dam) + 100 + self.getStat("spirit")*.333


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
		# Testing against dummy is giving me 7.5% increased damage for -10% resist. Using that (.0075)
		# single target debuffs need to have reduced value. Also applying resist reduction only applies to the next hit
		# setting value at 1/3
		for damage in primaryDamages:
			if self.get(damage+" %") > 0:
				self.setIfNull("reduce "+damage+" resist", self.getStat(damage+" %")*.0075*self.get(damage+" %")/3)
				print "  reduce "+damage+" resist: " + str(self.get("reduce "+damage+" resist"))

		# handle shorthand sets: resist	
		#resist types
		for b in resists:
			self.setIfNull(b, self.get("resist"))
			self.setIfNull("pet "+b, self.get("pet resist"))

			self.setIfNull("reduce "+b, self.get("reduce resist"))

		self.setIfNull("reduce resist", sum([self.get("reduce "+b) for b in resists]))

		print "  reduce resist:", self.get("reduce resist")

		elementals = ["fire", "cold", "lightning"]
		self.setIfNull("reduce elemental resist", sum([self.get("reduce "+b+" resist") for b in elementals]))
		print "  reduce elemental resist", self.get("reduce elemental resist")

		# elemental damage % and resist should be the sum of the individual components
		self.setIfNull("elemental %", sum([self.get(b) for b in ["cold %", "lightning %", "fire %"]]))
		print "  elemental %:", self.get("elemental %")

		# elemental resists are weird. e.g. fire resist protects against burn and elemental resist protects against fire but elemental resist does not protect against burn
		self.setIfNull("elemental resist", sum([self.get(b) for b in ["cold resist", "lightning resist", "fire resist"]]))
		print "  elemental resist:", self.get("elemental resist")

		# all damage should be >= all other damage bonuses (sans retaliation)
		# don't count cold, lightning, or fire as they're already aggregated under elemental
		parts = ["acid %", "aether %", "bleed %", "burn %", "chaos %", "electrocute %", "elemental %", "frostburn %", "internal %", "physical %", "pierce %", "poison %", "vitality %", "vitality decay %"]
		self.setIfNull("all damage %", sum([self.get(b) for b in parts]))
		print "  all damage %:", self.get("all damage %")

		self.setIfNull("pet all damage %", sum([self.get("pet " + b) for b in parts]))
		print "  pet all damage %:", self.get("pet all damage %")

		total = 0
		for damage in damages:
			total += self.getStat(damage+" %")*self.get(damage+" %")/100
		
		self.setIfNull("crit damage", total*self.getStat("crit chance"))
		print "  crit damage:", self.get("crit damage")

		#calculate elemental damage and triggered elemental damage if not set
		self.setIfNull("elemental", sum([self.get(elemental) for elemental in elementals])/3.0)
		print "  elemental:", self.get("elemental")
		self.setIfNull("triggered elemental", sum([self.get("triggered " + elemental) for elemental in elementals])/3.0)
		print "  triggered elemental:", self.get("triggered elemental")

		# catch all for flat damage of any type
		# triggered flat damage should be either specified manually or be equivalent to normal flat damage.
		# catch all for triggered damage of any type (no triggered damage is useless right?)		
		# retaliation types
		for damage in damages:
			# duration damage is counted for half if not specified manually
			factor = 1
			if damage in durationDamages:
				factor = .5

			self.setIfNull(damage, self.get("damage")*factor)
			self.setIfNull("pet "+damage, self.get("pet damage")*factor)

			self.setIfNull("triggered "+damage, max([self.get(damage), self.get("triggered damage")*factor]))

			self.setIfNull(damage+" retaliation", self.get("retaliation")*factor)
			self.setIfNull("pet "+damage+" retaliation", self.get("pet retaliation")*factor)
			
		total = 0
		for speed in ["attack speed", "cast speed", "move %"]:
			total += self.get(speed)
		self.setIfNull("total speed", total)

		self.filterConstellations()

	def filterConstellations(self):
		print "\n  Checking for weapon restricted constellations..."
		for c in self.getStat("blacklist"):
			if c in Constellation.constellations:
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
					print "    -", c.name, "removed <-",str(c.restricts)


	def get(self, key):
		if key in self.bonuses.keys():
			return self.bonuses[key]
		else:
			return 0
	def set(self, key, value):
		self.bonuses[key] = value

	def setIfNull(self, key, value):
		if not key in self.bonuses:
			self.set(key, value)

	def getStat(self, key):
		if key in self.stats.keys():
			return self.stats[key]
		else:
			return 0


		#"acid %":0, 
		#"acid resist":0, 
		#"aether":0, 
		#"aether %":0, 
		#"aether resist":0, 
		#"all damage %":0, 
		#"armor":0, 
		#"armor %":0, 
		#"armor absorb":0, 
		#"armor physique requirements":0, 
		#"attack as health %":0, 
		#"attack speed":0, 
		#"attack speed retaliation":0, 
		#"avoid melee":0, 
		#"avoid ranged":0, 
		#"bleed":0, 
		#"bleed %":0, 
		#"bleed duration":0, 
		#"bleed resist":0, 
		#"bleed retaliation":0, 
		#"block %":0, 
		#"blocked damage %":0, 
		#"burn":0, 
		#"burn %":0, 
		#"burn duration":0, 
		#"cast speed":0, 
		#"chaos":0, 
		#"chaos %":0, 
		#"chaos resist":0, 
		#"chaos retaliation":0, 
		#"cold":0, 
		#"cold %":0, 
		#"cold resist":0, 
		#"constitution %":0, 
		#"crit damage":0, 
		#"cunning":0, 
		#"cunning %":0, 
		#"cunning ranged requirements":0, 
		#"damage absorb":0,						**************
		#"damage absorb %":0,					**************
		#"damage beast %":0, 
		#"damage chthonics %":0, 
		#"damage from arachnids":0, 
		#"damage from beasts":0, 
		#"damage from insectoids":0, 
		#"damage from undead":0, 
		#"damage human %":0, 
		#"damage reflect %":0, 
		#"damage to cthonics":0, 
		#"damage to undead":0, 
		#"damage undead %":0, 
		#"defense":0, 
		#"defense %":0, 
		#"duration":0, 
		#"electrocute %":0, 
		#"electrocute duration":0, 
		#"elemental":0, 
		#"elemental %":0, 
		#"elemental resist":0, 
		#"elemental shield":0, 
		#"energy":0, 
		#"energy %":0, 
		#"energy absorb":0, 
		#"energy burn %":0, 
		#"energy leech":0, 
		#"energy leech resist":0, 
		#"energy regeneration":0, 
		#"energy/s":0, 
		#"fire":0, 
		#"fire %":0, 
		#"fire resist":0, 
		#"frostburn":0, 
		#"frostburn %":0, 
		#"frostburn duration":0, 
		#"health":0, 
		#"health %":0, 
		#"health regeneration":0, 
		#"health/s":0, 
		#"internal":0, 
		#"internal %":0, 
		#"internal duration":0, 
		#"jewelry spirit requirements":0, 
		#"life leach":0, 
		#"life leach %":0, 
		#"life leech":0, 
		#"life leech %":0, 
		#"life leech resist":0, 
		#"life leech retaliation":0, 
		#"lifesteal %":0, 
		#"lightning":0, 
		#"lightning %":0, 
		#"lightning resist":0, 
		#"max acid resist":0, 
		#"max aether resist":0, 
		#"max bleed resist":0, 
		#"max chaos resist":0, 
		#"max fire resist":0, 
		#"max lightning resist":0, 
		#"max pierce resist":0, 
		#"max vitality resist":0, 
		#"melee weapon cunning requirements":0, 
		#"melee weapon physique requirements":0, 
		#"move %":0, 
		#"move speed retaliation":0, 
		#"offense":0, 
		#"offense %":0, 
		#"pet acid":0, 
		#"pet acid resist":0, 
		#"pet aether resist":0, 
		#"pet all damage %":0, 
		#"pet attack speed":0, 
		#"pet bleed resist":0, 
		#"pet chaos resist":0, 
		#"pet crit damage":0, 
		#"pet defense %":0, 
		#"pet elemental %":0, 
		#"pet elemental resist":0, 
		#"pet fire damage %":0, 
		#"pet health %":0, 
		#"pet health regeneration":0, 
		#"pet health/s":0, 
		#"pet lifesteal %":0, 
		#"pet lightning damage %":0, 
		#"pet max all resist":0, 
		#"pet offense %":0, 
		#"pet physical":0, 
		#"pet pierce resist":0, 
		#"pet pierce retaliation":0, 
		#"pet poison":0, 
		#"pet retaliation %":0, 
		#"pet total speed":0, 
		#"pet vitality resist":0, 
		#"physical":0, 
		#"physical %":0, 
		#"physical resist":0, 
		#"physical retaliation":0, 
		#"physical to chaos":0, 
		#"physique":0, 
		#"physique %":0, 
		#"pierce":0, 
		#"pierce %":0, 
		#"pierce resist":0, 
		#"pierce retaliation":0, 
		#"poison":0, 
		#"poison %":0, 		
		#"poison duration":0, 
		#"reduce aether resist":0, 
		#"reduce elemental resist":0, 
		#"reduce lightning resist":0, 
		#"reduce physical resist":0, 
		#"reduce pierce resist":0, 
		#"reduce damage %":0,						****************
		#"reduce defense":0,
		#"reduced bleed duration":0, 
		#"reduced burn duration":0, 
		#"reduced electrocute duration":0, 
		#"reduced entrapment duration":0, 
		#"reduced freeze":0, 
		#"reduced freeze duration":0, 
		#"reduced frostburn duration":0, 
		#"reduced poison duration":0, 
		#"reduced stun duration":0, 
		#"reflected damage reduction":0, 
		#"retaliation %":0, 
		#"shield physique requirements":0, 
		#"shield recovery":0, 
		#"skill cost %":0, 
		#"skill disruption protection":0, 
		#"slow move":0, 
		#"slow resist":0, 
		#"spirit":0, 
		#"spirit %":0, 
		#"stun %":0, 
		#"stun duration":0, 
		#"stun retaliation":0, 
		#"terrify retaliation":0, 
		#"total speed":0, 
		#"triggered acid":0, 
		#"triggered aether":0, 
		#"triggered bleed":0, 
		#"triggered burn":0, 
		#"triggered chaos":0, 
		#"triggered cold":0, 
		#"triggered electrocute":0, 
		#"triggered elemental":0, 
		#"triggered fire":0, 
		#"triggered frostburn":0, 
		#"triggered internal":0, 
		#"triggered lightning":0, 
		#"triggered physical":0, 
		#"triggered pierce":0, 
		#"triggered poison":0, 
		#"triggered vitality":0, 
		#"vitality":0, 
		#"vitality %":0, 
		#"vitality decay":0, 
		#"vitality decay %":0, 
		#"vitality decay retaliation":0, 
		#"vitality resist":0, 
		#"weapon damage %":0, 
		#"weapon spirit requirements":0, 

	#bonuses
		# select the important bonuses from above and give them a value.
		# Note some bonuses will be automatically calculated if left blank (and should be unless you want to override):
		#	health/s <- health, health regeneration, fight length
		#	energy/s <- energy, energy regeneration, energy length

		#   physique <- health/s, health, defense
		#   cunning <- appropriate damage %, offense
		#   spirit <- appropriate damage %, energy, energy/s

		#	perc stats ["physique", "cunning", "spirit", "offense", "defense", "health", "energy", "armor"]
		#		will be calculated from your stats settings and base (non perc) values

		#   resist reductions <- appropriate damage % stat and bonus
		#	crit damage <- uses damage % stats and weights and crit chance stat

		#   elemental damage and resist <- fire/cold/lightning damage and resist  (includes pets)
		#   all damage % -< all individual damage % (includes pets)
		
		#Note there are a few shorthand notations. An individual setting will override the shorthand setting:
		#	resist <- sets a value for all resist types
		#	pet resist <- sets a value for all pet resist types
		#	reduce resist <- sets a value for all resist reductions
		#	damage <- sets a value for all on hit damage types
		#	triggered damage <- sets a value for all ability triggered damage types
		#		note that if you don't set triggered damage it gets valued at on hit damage of the same type since triggered damage is (roughly) normalized in value to on hit damage
		#   retaliation <- sets a value for all retaliation damage types
		#   pet retaliation <- sets a value for all pet retaliation damage types
	#stats
		# estimate how frequent combat events are for calculating dynamic stats and abilities
		# "attacks/s":1.75,		
		# "allAttacks/s":[
		# 	# list of attack skills that can be linked to abilities. remember to include your main attack.
		# 	1.75, #main attack (fire strike)
		# 	.5, # brutal shield slam: 3s recharge, 3 target max. Call it 2 targets and 4 seconds between = .5 aps
		# 	.4, #war cry: 7.5 s recharge, big radius, call it 3 hits = 3/7.5 = .4
		# 	.385, # markovian's advantage: 22% chance = 1.75*.22 = 
		# ],		
		# "hits/s":4,
		# "blocks/s":1.5,
		# "kills/s":1,		
		# "crit chance":.05,
		# "low healths/s":1.0/45, # total guesswork.

		# "fight length":30, # average length of a fight... this is for weighting abilities and over time effects. If you rely on wearing down opponents this should be long. If you are a glass cannon this should be small.

		# # estimated sheet stats for target level
		# "physique":900,
		# "cunning":400,
		# "spirit":450,

		# "offense":1200,
		# "defense":1400,

		# "health":7500,
		# "health regeneration":25,

		# "armor":1000,
		# "energy":2500,
		
		# # estimated damage % for target level. add whatever damages are important to your build
		# "physical %":200, # sheet % damage for important damage types.
		# "fire %":400,
		# "lightning %":200,
		# "acid %":150,

		# "retaliation %":250+100,


		# "playStyle":"tank", # playstyle for weighting constellation abilities. [ranged/shortranged/melee/tank]
		# "weapons":[
		# 	# list of weapons used for constellations that have a weapon requirement. E.g. "shield", "sword"
		# ],
		# "blacklist":[
		# 	# list of constellations that I want to manually exclude for some reason.
		# ]	
