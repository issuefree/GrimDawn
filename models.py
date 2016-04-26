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
				self.set("reduce "+damage+" resist", max(self.get("reduce "+damage+" resist"), self.getStat(damage+" %")*.0075*self.get(damage+" %")))
				print "  reduce "+damage+" resist: " + str(self.get("reduce "+damage+" resist"))

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
			# pet flat damage?

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


nyx = Model(
	"nyx",
	{
		"spirit":12.5, 
		"offense":20, 
		"crit damage":5,
		"vitality %":20,
		"chaos %":7.5,
		"cast speed":5,
		"defense":6,
		"armor":3.5, 
		# armor absorb is good vs lots of little hits. This char regens fast with lots of little enemies so there's not much value
		"armor absorb":2,
		"health":.6, "health/s":0,
		"energy":.2, "energy/s":5,
		"avoid melee":10, "avoid ranged":15,
		"resist":7.5,

		"pet attack speed":5,
		"pet total speed":8,
		"pet offense":5,
		"pet offense %":50,
		"pet lifesteal %":2,
		"pet all damage %":7.5,
		"pet defense %":1,
		"pet resist":1.5,
		"pet health %":5,
		"pet health/s":1,
		"pet retaliation":1, "pet retaliaion %":3,

		"triggered vitality":30, "triggered vitality decay":10,
		"triggered chaos":10,
		"triggered fire":3,
		"triggered life leech":3,
		"triggered damage":1,
		
		"weapon damage %":1,
		"slow move":7,
		"stun %":10
	},

	{
		"attacks/s":5,
		"hits/s":1,
		"blocks/s":0,
		"kills/s":1,
		"crit chance":.12,
		"low healths/s":1.0/30, # total guesswork.

		"physique":650,
		"cunning":400,
		"spirit":650,

		"offense":1500,
		"defense":1000,

		"health":5000,
		"armor":450,
		"energy":2500,

		"vitality %":750+350,
		"chaos %":350+350,

		"pet all damage %":200,

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
		
		"energy": .1, # "energy %": ,
		"energy absorb": 5,
		# "energy regeneration": ,
		# "energy/s": ,

		"health": .55, # "health %": ,
		"health regeneration": 5,
		# "health/s": 5,

		"armor": 3.5, # "armor %": ,
		"armor absorb": 20,
		
		"defense": 1, # "defense %": ,
		"resist": 15,
		#"elemental resist": 12.5,
		"physical resist":35,
		"pierce resist":25,

		"block %": 100,
		"blocked damage %":50,
		"shield recovery":75,

		"offense": 10, # "offense %": ,

		"damage":1,
		"physical": 4, "physical %": 7.5,
		"fire":5, "fire %": 12.5,
		"lightning": 2, "lightning %": 5,
		"elemental": 2, # "elemental %": 20,
		"burn": 2, "burn %": 6, "burn duration":5,

		"triggered fire":7.5,
		"triggered burn":5,

		"reduce fire resist":80,

		"weapon damage %":7.5,

		# "crit damage": ,
		"damage reflect %": 25,
		"retaliation":7.5, 
		"retaliation %": 17.5,
		
		"stun %":-1,

		# "lifesteal %": ,
		"move %": 10,

		"Acid Spray":.75,
	},

	{
		"attacks/s":1.75,
		"allAttacks/s":[
			1.75, #main attack (fire strike)
			1, # thermite mine / mortar
			.5, # brutal shield slam: 3s recharge, 3 target max. Call it 2 targets and 4 seconds between = .5 aps
			.4, #war cry: 7.5 s recharge, big radius, call it 3 hits = 3/7.5 = .4
			.385, # markovian's advantage: 22% chance = 1.75*.22 = 
		],
		"hits/s":4,
		"blocks/s":1.5,
		"kills/s":1,
		"crit chance":.05,
		"low healths/s":1.0/45, # total guesswork.

		"physique":900,
		"cunning":400,
		"spirit":450,

		"offense":1500,
		"defense":1500,

		"health":10000,
		"health regeneration":100,

		"armor":1250,
		"energy":2500,

		"physical %":250+150+100,
		"fire %":500+175+100,
		"lightning %":300+175+100,
		"acid %":100+175+100,

		"retaliation %":350+100,

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
		"allAttacks/s":[
			1.75, #main attack (fire strike)
			.5, # brutal shield slam: 3s recharge, 3 target max. Call it 2 targets and 4 seconds between = .5 aps
			.4, #war cry: 7.5 s recharge, big radius, call it 3 hits = 3/7.5 = .4
			.385, # markovian's advantage: 22% chance = 1.75*.22 = 
			0,0,0,0,0
		],

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

		"physical %":200+150+100,
		"fire %":400+175+100,
		"lightning %":200+175+100,
		"acid %":150+175+100,

		"retaliation %":250+100,

		"fight length":45,

		"playStyle":"tank",
		"weapons":["shield"],
		"blacklist":[xE, wolverine, owl, ghoul, eye, crane, blade, guide, falcon, spider, bat, throne, shepherd, vulture, rat, raven
		]
	}
)


  # Elemental Barrier
  # Targo's Hammer
  # acid %
  # acid resist
  # aether
  # aether %
  # aether resist
  # all damage %
  # armor
  # armor %
  # armor absorb
  # armor physique requirements
  # attack speed
  # attack speed retaliation
  # avoid melee
  # avoid ranged
  # bleed
  # bleed %
  # bleed duration
  # bleed resist
  # bleed retaliation
  # block %
  # blocked damage %
  # burn
  # burn %
  # burn duration
  # cast speed
  # chaos
  # chaos %
  # chaos resist
  # cold
  # cold %
  # cold resist
  # constitution %
  # crit damage
  # cunning
  # cunning %
  # cunning ranged requirements
  # damage beast %
  # damage chthonics %
  # damage from arachnids
  # damage from beasts
  # damage from insectoids
  # damage from undead
  # damage human %
  # damage reflect %
  # damage undead %
  # defense
  # defense %
  # electrocute %
  # electrocute duration
  # elemental
  # elemental %
  # elemental resist
  # energy
  # energy %
  # energy absorb
  # energy burn %
  # energy leech
  # energy leech resist
  # energy regeneration
  # energy/s
  # fire
  # fire %
  # fire resist
  # frostburn
  # frostburn %
  # frostburn duration
  # health
  # health %
  # health regeneration
  # health/s
  # internal
  # internal %
  # internal duration
  # jewelry spirit requirements
  # life leech
  # life leech %
  # life leech resist
  # life leech retaliation
  # lifesteal %
  # lightning
  # lightning %
  # lightning resist
  # max acid resist
  # max aether resist
  # max bleed resist
  # max chaos resist
  # max fire resist
  # max lightning resist
  # max pierce resist
  # max vitality resist
  # melee weapon cunning requirements
  # melee weapon physique requirements
  # move %
  # move speed retaliation
  # offense
  # offense %
  # pet acid resist
  # pet aether resist
  # pet all damage %
  # pet attack speed
  # pet bleed resist
  # pet chaos resist
  # pet crit damage
  # pet defense %
  # pet elemental %
  # pet elemental resist
  # pet fire damage %
  # pet health %
  # pet health regeneration
  # pet health/s
  # pet lifesteal %
  # pet lightning damage %
  # pet max all resist
  # pet offense %
  # pet pierce resist
  # pet pierce retaliation
  # pet retaliation %
  # pet total speed
  # pet vitality resist
  # physical
  # physical %
  # physical resist
  # physical retaliation
  # physique
  # physique %
  # pierce
  # pierce %
  # pierce resist
  # pierce retaliation
  # poison
  # poison %
  # poison duration
  # reduce elemental resist
  # reduced bleed duration
  # reduced burn duration
  # reduced electrocute duration
  # reduced entrapment duration
  # reduced freeze
  # reduced freeze duration
  # reduced frostburn duration
  # reduced poison duration
  # reduced stun duration
  # reflected damage reduction
  # retaliation %
  # shield physique requirements
  # shield recovery
  # skill cost %
  # skill disruption protection
  # slow resist
  # spirit
  # spirit %
  # stun %
  # stun duration
  # stun retaliation
  # vitality
  # vitality %
  # vitality decay
  # vitality decay %
  # vitality decay retaliation
  # vitality resist
  # weapon spirit requirements

newModel = Model(
	#name
	"newModel",
	#bonuses
	{
	
	},
	#stats
	{
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

		"physique":900,
		"cunning":400,
		"spirit":450,

		"offense":1200,
		"defense":1400,

		"health":7500,
		"health regeneration":25,

		"armor":1000,
		"energy":2500,

		"physical %":200+150+100, # sheet % damage for important damage types.
		"fire %":400+175+100,
		"lightning %":200+175+100,
		"acid %":150+175+100,

		"retaliation %":250+100,

		"fight length":45, # average length of a fight... this is for weighting abilities and over time effects. If you rely on wearing down opponents this should be long. If you are a glass cannon this should be small.

		"playStyle":"tank", # playstyle for weighting constellation abilities. [ranged/shortranged/melee/tank]
		"weapons":[
			# list of weapons used for constellations that have a weapon requirement. E.g. "shield", "sword"
		],
		"blacklist":[
			# list of constellations that I want to manually exclude for some reason.
		]	
	}
	)