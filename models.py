import os
from dataModel import *
from constellationData import *
from utils import *


class Model:	
	def __init__(self, name, bonuses, stats):
		self.name = name
		self.bonuses = bonuses
		self.stats = stats


	def initialize(self):
		self.checkModel()

		self.seedSolutions = []
		self.readSeedSolutions()


	def __str__(self):
		out = ""
		for key in sorted(self.bonuses.keys()):
			if self.get(key) > 0:
				out += key + " " + str(self.bonuses[key]) + "\n"
		return out

	def saveSeedSolutions(self):
		try:
			os.mkdir(self.name)
		except:
			pass

		file = open(self.name+"/solutions.py", 'w')
		out = "self.seedSolutions = [\n"
		for s in sorted(self.seedSolutions, key=lambda c: evaluateSolution(c, self), reverse=True):
			out += "  "+solutionPath(s)+ "  # " + str(int(evaluateSolution(s, self))) + "\n"
		out += "]"
		file.write(out)
		file.close()

	def readSeedSolutions(self):
		try:
			file = open(self.name+"/solutions.py", "r")
			lines = file.read()
			exec(lines)
		except:
			pass

		self.saveSeedSolutions()

	def checkModel(self):
		print "Checking model..."
		print "  "+self.name

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
		val += sum([self.get(b) for b in ["fire %", "cold %", "lightning %", "acid %", "vitality %", "aether %", "chaos %"]]) * .33
		val += sum([self.get(b) for b in ["burn %", "frostburn %", "electrocute %", "poison %", "vitality decay %"]]) * .333
		val += self.get("energy") * 2
		val += self.get("energy/s") * .01

		self.set("spirit", max(self.get("spirit"), val))
		print "  Spirit:", self.get("spirit")

		# update damage % stats
		self.stats["physical %"] = self.getStat("physical %") + 100 + self.getStat("cunning")*.33
		self.stats["pierce %"] = self.getStat("pierce %") + 100 + self.getStat("cunning")*.285
		self.stats["bleed %"] = self.getStat("bleed %") + 100 + self.getStat("cunning")*.333
		self.stats["internal %"] = self.getStat("internal %") + 100 + self.getStat("cunning")*.333

		for dam in ["fire %", "cold %", "lightning %", "acid %", "vitality %", "aether %", "chaos %"]:
			self.stats[dam] = self.getStat(dam) + 100 + self.getStat("spirit")*.33

		for dam in ["burn %", "frostburn %", "electrocute %", "poison %", "vitality decay %"]:
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
				self.set("reduce "+damage+" resist", max(self.get("reduce "+damage+" resist"), self.getStat(damage+" %")*.0075*self.get(damage+" %")/3))
				print "  reduce "+damage+" resist: " + str(self.get("reduce "+damage+" resist")/3)

		# handle shorthand sets: resist	
		#resist types
		for b in resists:
			self.set(b, max(self.get(b), self.get("resist")))
			self.set("pet "+b, max(self.get("pet "+b), self.get("pet resist")))

			self.set("reduce "+b, max(self.get("reduce "+b), self.get("reduce resist")))
		self.set("reduce resist", max(self.get("reduce resist"), sum([self.get("reduce "+b) for b in resists])))
		print "  reduce resist:", self.get("reduce resist")

		elementals = ["fire", "cold", "lightning"]
		self.set("reduce elemental resist", max(self.get("reduce elemental resist"), sum([self.get("reduce "+b+" resist") for b in elementals])))
		print "  reduce elemental resist", self.get("reduce elemental resist")

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

		total = 0
		for damage in damages:
			total += self.getStat(damage+" %")*self.get(damage+" %")/100
		
		self.set("crit damage", max(self.get("crit damage"), total*self.getStat("crit chance")))
		print "  crit damage:", self.get("crit damage")

		# catch all for flat damage of any type
		# triggered flat damage should be either specified manually or be equivalent to normal flat damage.
		# catch all for triggered damage of any type (no triggered damage is useless right?)		
		# retaliation types
		for damage in damages:
			# duration damage is counted for half if not specified manually
			factor = 1
			if damage in durationDamages:
				factor = .5

			self.set(damage, max(self.get(damage), self.get("damage")*factor))
			self.set("pet "+damage, max(self.get("pet "+damage), self.get("pet damage")*factor))

			self.set("triggered "+damage, max([self.get("triggered "+damage), self.get(damage), self.get("triggered damage")*factor]))

			self.set(damage+" retaliation", max(self.get(damage+" retaliation"), self.get("retaliation")*factor))
			self.set("pet "+damage+" retaliation", max(self.get("pet "+damage+" retaliation"), self.get("pet retaliation")*factor))
			


		#nothing grants total speed

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


lachesis = Model(
	"lachesis",
	{
		"offense":17.5, 
		"cast speed":25,
		"defense":7.5,
		"armor":3.5, 
		# armor absorb is good vs lots of little hits. This char regens fast with lots of little enemies so there's not much value
		"armor absorb":10,
		"health":.6,
		"energy":.25,
		"avoid melee":10, "avoid ranged":15,
		"resist":7.5,

		"pet attack speed":5,
		"pet total speed":8,
		"pet offense":5,
		"pet offense %":50,
		"pet lifesteal %":2,
		"pet all damage %":7.5,
		"pet damage":10,
		"pet defense %":1,
		"pet resist":1.5,
		"pet health %":5,
		"pet health/s":1,
		"pet retaliation":1, "pet retaliaion %":3,

		"vitality %":25,
		"chaos %":7.5,

		"triggered vitality":30, "triggered vitality decay":10,
		"triggered chaos":10,
		"triggered life leech":3,
		"triggered damage":1,
		
		"weapon damage %":1,
		"slow move":7,
		"stun %":10
	},

	{
		"attacks/s":3.5,
		"allAttacks/s":[
			3.5, # sigil
			2.5, # lightning totem
			2.5, # grasping roots
			1,   # pets/locust
			1,   # pets/locust
			1,   # pets/locust
		],
		"hits/s":.5,
		"blocks/s":0,
		"kills/s":1.5,
		"crit chance":.075,
		"low healths/s":1.0/30, # total guesswork.

		"physique":650,
		"cunning":400,
		"spirit":650,

		"offense":1250,
		"defense":1000,

		"health":5500,
		"armor":400,
		"energy":3000,

		"vitality %":900, "vitality decay %":200,
		"chaos %":350,

		"pet all damage %":150,

		"fight length":30,

		"playStyle":"shortranged",
		"weapons":["offhand"],
		"blacklist":[
			sage, 			#seems cool but there's nothing but the ability
			wolf,			#relatively low value for the requirements
			soldier,			#relatively low value for the requirements
			tree, spear,
			falcon, hammer, owl, harpy, throne, wolverine, blade # don't need these. crook will supply all I need.
		]
	}
)


armitage = Model(
	"armitage",
	{
		"attack speed":10,
		"cast speed":7.5,
		
		"energy":.2, # "energy %": ,
		"energy absorb": 15,
		# "energy regeneration": ,
		# "energy/s": ,

		"health": .66, # "health %": ,
		# "health regeneration": 5,
		# "health/s": 5,

		"armor": 5-1.5, 
		"armor absorb": 20-15,
		
		"defense": 1-.5, # "defense %": ,
		"resist": 15-10,
		"physical resist":35,
		"pierce resist":25-15,
		"aether reist":25,
		"acid resist":10,
		"chaos resist":20,
		"bleed resist":15,

		"block %": 100,
		"blocked damage %":50-10,
		"shield recovery":75,

		"offense": 10, # "offense %": ,

		"damage":1,
		"physical": 7.5, "triggered physical":5, "physical %": 7.5,
		"fire":12.5, "triggered fire":10, "fire %": 15,
		"burn":7.5, "triggered burn":5, "burn %": 5, "burn duration":5,
		"lightning": 5, "triggered lightning":2.5, "lightning %":5,
		"elemental": 2.5, # "elemental %": 20,


		"weapon damage %":7.5,

		# "crit damage": ,
		"damage reflect %": 35,
		"retaliation":7, 
		"retaliation %":17,
		
		"stun %":-1,

		"lifesteal %":20,
		"move %": 10,

		"Acid Spray":.75,
	},

	{
		"attacks/s":1.75,
		"allAttacks/s":[
			1.75, #main attack (fire strike)
			.75, # thermite mine / mortar
			.5, # brutal shield slam: 3s recharge, 3 target max. Call it 2 targets and 4 seconds between = .5 aps
			.4, #war cry: 7.5 s recharge, big radius, call it 3 hits = 3/7.5 = .4
			.385, # markovian's advantage: 22% chance = 1.75*.22 = 
		],
		"hits/s":4,
		"blocks/s":1.5,
		"kills/s":1,
		"crit chance":.08,
		"low healths/s":1.0/120, # total guesswork.

		"physique":1200,
		"cunning":400,
		"spirit":600,

		"offense":1750,
		"defense":1750,

		"health":8500,
		"health regeneration":200,

		"armor":2500,
		"energy":2500,

		"physical %":300, "physical":800,
		"fire %":750, "fire":2000,
		"burn %":450, "burn":400,
		"lightning %":400, "lightning":850,

		"retaliation %":550+100,

		"fight length":45,

		"playStyle":"tank",
		"weapons":["shield"],
		"blacklist":[
			# manticore, manticoreAcidSpray# I'm not sure it makes sense in this build. Not many attacks to bind it to and the stats on the constellation aren't that good.
		]
	}
)
  # [xC, viper, hound, xO, dryad, targoShieldWall, shieldmaiden, xA, anvil, messenger, xE, raven, behemothGiantsBlood, crown],  # 39417
#  [xC, viper, hound, xO, lion, targoShieldWall, xA, anvil, messenger, xE, light, behemothGiantsBlood, raven, crown, magiFissure],  # 38500
testModel = Model(
	"testModel",
	{
		"attack speed":10,
		"cast speed":7.5,
		
		"energy": .2, # "energy %": ,
		"energy absorb": 1,
		# "energy regeneration": ,
		# "energy/s": ,

		"health": .66, # "health %": ,
		"health regeneration": 5,
		# "health/s": 5,

		"armor": 3, # "armor %": ,
		"armor absorb": 10,
		
		"defense": 0.5, # "defense %": ,
		"resist": 15,
		#"elemental resist": 12.5,
		"physical resist":35,
		"pierce resist":25,

		"block %": 75,
		"blocked damage %":50,
		"shield recovery":35,

		"offense": 4, # "offense %": ,

		"damage":1,
		"physical": 4, "physical %": 5,
		"fire":5, "fire %": 10,
		"lightning": 2, "lightning %": 5,
		"elemental": 2, # "elemental %": 20,
		"burn": 2, "burn %": 5, "burn duration": 1,

		"triggered fire":10,
		"triggered lightning":4,
		"triggered physical":2,

		"weapon damage %":7.5,

		# "crit damage": ,
		"damage reflect %": 20,
		"retaliation":3.5, 
		"retaliation %": 20,
		
		"stun %":-1,

		# "lifesteal %": ,
		"move %": 10,
	},

	{
		"attacks/s":1.75,
		"hits/s":4,
		"blocks/s":1.5,
		"kills/s":1,
		"crit chance":.05,
		"low healths/s":1.0/45, # total guesswork.

		"physique":900,
		"cunning":400,
		"spirit":450,

		"offense":1200,
		"defense":1400,

		"health":7500,
		"health regeneration":25,

		"armor":1000,
		"energy":2500,

		"physical %":200,
		"fire %":400,
		"lightning %":200,
		"acid %":150,

		"retaliation %":250+100,

		"fight length":45,

		"playStyle":"tank",
		"weapons":["shield"],
		"blacklist":[xE, wolverine, owl, ghoul, eye, crane, blade, guide, falcon, spider, bat, throne, shepherd, vulture, rat, raven
		]
	}
)

lochlan = Model(
	"Lochlan",
	{
		"armor":2, "armor absorb":10,
		"attack speed":20,
		"avoid melee":20, "avoid ranged":15,
		"cast speed":10,
		# "crit damage":20,
		"defense":7.5,
		
		"energy":.75,
		"health":.75,
		"lifesteal %":20,

		"offense":15,

		"elemental":5,
		"electrocute":12.5, "electrocute %":7.5, "electrocute duration":2.5,
		"physical":15, "physical %":10,
		"lightning":20, "lightning %":20,
		"bleed %":2.5,
		"cold %":2.5,
		"fire %":2.5,

		"weapon damage %":20, 

		"resist":2.5,
		"physical resist":5,

		"stun %":10,
		"stun duration":5,

		"move %":5,

	},
	#stats
	{
		# estimate how frequent combat events are for calculating dynamic stats and abilities
		"attacks/s":1.5,
		"hits/s":1.5,
		"blocks/s":0,
		"kills/s":1.5,	
		"crit chance":.1,
		"low healths/s":1.0/15, # total guesswork.

		"fight length":20, # average length of a fight... this is for weighting abilities and over time effects. If you rely on wearing down opponents this should be long. If you are a glass cannon this should be small.

		# estimated sheet stats for target level
		"physique":500,
		"cunning":250,
		"spirit":350,

		"offense":1000,
		"defense":1000,

		"health":5000,
		"health regeneration":20,

		"armor":500,
		"energy":1250,
		
		# estimated damage % for target level. add whatever damages are important to your build
		"physical %":200,
		"lightning %":250,

		"playStyle":"melee", # playstyle for weighting constellation abilities. [ranged/shortranged/melee/tank]
		"weapons":[
			"twohand"
		],
		"blacklist":[
			# list of constellations that I want to manually exclude for some reason.
		]	
	}
)

kieri = Model(
	"Kieri",
	{
		"armor":.25,
		"attack speed":40, 
		"cast speed":10, 
		
		"offense":20, 

		"avoid melee":5, "avoid ranged":7.5, 
		"defense":5, 

		"resist":3,
		"physical resist":5, 

		"health":.66, 
		"energy":.5, 

		"damage":1,
		"physical":10, "physical %":15, 
		#"pierce":0, "pierce %":0, 
		"burn":5, "burn %":5, "burn duration":2.5, "triggered burn":7.5,
		"fire":15, "fire %":20, 
		"lightning":3, "lightning %":5, 
		"chaos %":1, 
		"pierce %":1.5,
		"elemental":5, 

		"lifesteal %":15, 

		"move %":20, 

		"slow move":10, 
		"stun %":50, "stun duration":10, 

		"weapon damage %":25, 
	},
	#stats
	{
		# estimate how frequent combat events are for calculating dynamic stats and abilities
		"attacks/s":3,		
		"hits/s":.25,
		"blocks/s":0,
		"kills/s":1.5,		
		"crit chance":.15,
		"low healths/s":1.0/45, # total guesswork.

		"fight length":20, # average length of a fight... this is for weighting abilities and over time effects. If you rely on wearing down opponents this should be long. If you are a glass cannon this should be small.

		# estimated sheet stats for target level
		"physique":450,
		"cunning":450,
		"spirit":450,

		"offense":1200,
		"defense":900,

		"health":3500,
		"health regeneration":10,

		"armor":250,
		"energy":2000,
		
		# estimated damage % for target level. add whatever damages are important to your build
		"physical %":150,
		"fire %":400, "burn %":200,
		"lightning %":250, "electrocute %":100,
		"pierce":100,
		"chaos":100,

		"playStyle":"ranged", # playstyle for weighting constellation abilities. [ranged/shortranged/melee/tank]
		"weapons":[
			"ranged"
		],
		"blacklist":[
			# list of constellations that I want to manually exclude for some reason.
		]	
	}
)

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

newModel = Model(
	#name
	"newModel",
	#bonuses
	{
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
	},
	#stats
	{
		# estimate how frequent combat events are for calculating dynamic stats and abilities
		"attacks/s":1.75,		
		"allAttacks/s":[
			# list of attack skills that can be linked to abilities. remember to include your main attack.
			1.75, #main attack (fire strike)
			.5, # brutal shield slam: 3s recharge, 3 target max. Call it 2 targets and 4 seconds between = .5 aps
			.4, #war cry: 7.5 s recharge, big radius, call it 3 hits = 3/7.5 = .4
			.385, # markovian's advantage: 22% chance = 1.75*.22 = 
		],		
		"hits/s":4,
		"blocks/s":1.5,
		"kills/s":1,		
		"crit chance":.05,
		"low healths/s":1.0/45, # total guesswork.

		"fight length":30, # average length of a fight... this is for weighting abilities and over time effects. If you rely on wearing down opponents this should be long. If you are a glass cannon this should be small.

		# estimated sheet stats for target level
		"physique":900,
		"cunning":400,
		"spirit":450,

		"offense":1200,
		"defense":1400,

		"health":7500,
		"health regeneration":25,

		"armor":1000,
		"energy":2500,
		
		# estimated damage % for target level. add whatever damages are important to your build
		"physical %":200, # sheet % damage for important damage types.
		"fire %":400,
		"lightning %":200,
		"acid %":150,

		"retaliation %":250+100,


		"playStyle":"tank", # playstyle for weighting constellation abilities. [ranged/shortranged/melee/tank]
		"weapons":[
			# list of weapons used for constellations that have a weapon requirement. E.g. "shield", "sword"
		],
		"blacklist":[
			# list of constellations that I want to manually exclude for some reason.
		]	
	}
)