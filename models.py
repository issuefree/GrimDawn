from dataModel import *
from constellationData import *
from utils import *

class Model:	
	def __init__(self, name, bonuses, stats):
		self.name = name
		self.bonuses = bonuses
		self.stats = stats

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
		file = open(self.name+"/solutions.py", "r")
		lines = file.read()
		exec(lines)

		self.saveSeedSolutions()

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
		for c in self.getStat("blacklist"):
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
		"hits/s":1.5,
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
