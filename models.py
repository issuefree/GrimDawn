import os, sys

from dataModel import *
from constellationData import *
from utils import *
from solution import *

class Model:
	# ALL_DAMAGE_PERC="all damage %"				#increases all non-retaliation damage

	# flat damage (e.g. "acid") only affects weapon attacks and skills that have a weapon component
	# perc damage increases all damage of the type by: base*(sum(all perc damage increases))
	# duration damages stack from different sources but not from the same source.
		# i.e. if you have burn damage on your weapon that does 500 damage over 5 seconds but you hit every second
		# the actual damage delivered per hit will be 100 not 500

	# ACID="acid"	
	# ACID_PERCENT="acid %"
	# POISON="poison"								
	# POISON_PERC="poison %"
	# POISON_DURATION="poison duration"

	# ELEMENTAL="elemental"							#elemental damage is delivered as 1/3 cold, 1/3 fire, 1/3 lightning
	# ELEMENTAL_PERC="elemental %"					#increases all cold,fire,lightning damage by the perc

	# COLD="cold"
	# COLD_PERC="cold %"
	# FROSTBURN="frostburn"
	# FROSTBURN_PERC="frostburn %"
	# FROSTBURN_DURATION="frostburn duration"

	# FIRE="fire"
	# FIRE_PERC="fire %"
	# BURN="burn"
	# BURN_PERC="burn %"
	# BURN_DURATION="burn duration"

	# LIGHTNING="lightning"
	# LIGHTNING_PERC="lightning %"
	# ELECTROCUTE="electrocute"
	# ELECTROCUTE_PERC="electrocute %"
	# ELECTROCUTE_DURATION="electrocute duration"

	# PHYSICAL="physical"
	# PHYSICAL_PERC="physical %"
	# INTERNAL="internal"
	# INTERNAL_PERC="internal %"
	# INTERNAL_DURATION="internal duration"

	# PIERCE="pierce"
	# PIERCE_PERC="pierce %"

	# BLEED="bleed"
	# BLEED_PERC="bleed %"
	# BLEED_DURATION="bleed duration"

	# AETHER="aether"
	# AETHER_PERC= "aether %"

	# CHAOS="chaos"
	# CHAOS_PERC="chaos %"

	# VITALITY="vitality"
	# VITALITY_PERC="vitality %"
	# VITALITY_DECAY="vitality decay"
	# VITALITY_DECAY_PERC="vitality decay %"

	# LIFE_LEECH="life leech"
	# LIFE_LEECH_PERC="life leech %"

	# TRIGGERED_ACID="triggered acid"
	# TRIGGERED_AETHER="triggered aether"
	# TRIGGERED_BLEED="triggered bleed"
	# TRIGGERED_BURN="triggered burn"
	# TRIGGERED_CHAOS="triggered chaos"
	# TRIGGERED_COLD="triggered cold"
	# TRIGGERED_ELECTROCUTE="triggered electrocute"
	# TRIGGERED_ELEMENTAL="triggered elemental"
	# TRIGGERED_FIRE="triggered fire"
	# TRIGGERED_FROSTBURN="triggered frostburn"
	# TRIGGERED_INTERNAL="triggered internal"
	# TRIGGERED_LIGHTNING="triggered lightning"
	# TRIGGERED_PHYSICAL="triggered physical"
	# TRIGGERED_PIERCE="triggered pierce"
	# TRIGGERED_POISON="triggered poison"
	# TRIGGERED_VITALITY="triggered vitality"

	# ACID_RESIST="acid resist"
	# AETHER_RESIST="aether resist"
	# BLEED_RESIST="bleed resist"

	# ARMOR="armor"
	# ARMOR_PERC="armor %"
	# ARMOR_ABSORB="armor absorb"
	# ARMOR_PHYSIQUE_REQUIREMENTS="armor physique requirements"
	# ATTACK_AS_HEALTH_PERC="attack as health %"
	# ATTACK_SPEED="attack speed"
	# ATTACK_SPEED_RETALIATION="attack speed retaliation"
	# AVOID_MELEE="avoid melee"
	# AVOID_RANGED="avoid ranged"
	# BLEED_RETALIATION="bleed retaliation"
	# BLOCK_PERC="block %"
	# BLOCKED_DAMAGE_PERC="blocked damage %"
	# CAST_SPEED="cast speed"
	# CHAOS_RESIST="chaos resist"
	# CHAOS_RETALIATION="chaos retaliation"
	# COLD_RESIST="cold resist"
	# CONSTITUTION_PERC="constitution %"
	# CRIT_DAMAGE="crit damage"
	# CUNNING="cunning"
	# CUNNING_PERC="cunning %"
	# CUNNING_RANGED_REQUIREMENTS="cunning ranged requirements"
	# DAMAGE_ABSORB="damage absorb"
	# DAMAGE_ABSORB_PERC="damage absorb %"
	# DAMAGE_BEAST_PERC="damage beast %"
	# DAMAGE_CHTHONICS_PERC="damage chthonics %"
	# DAMAGE_FROM_ARACHNIDS="damage from arachnids"
	# DAMAGE_FROM_BEASTS="damage from beasts"
	# DAMAGE_FROM_INSECTOIDS="damage from insectoids"
	# DAMAGE_FROM_UNDEAD="damage from undead"
	# DAMAGE_HUMAN_PERC="damage human %"
	# DAMAGE_REFLECT_PERC="damage reflect %"
	# DAMAGE_TO_CTHONICS="damage to cthonics"
	# DAMAGE_TO_UNDEAD="damage to undead"
	# DAMAGE_UNDEAD_PERC="damage undead %"
	# DEFENSE="defense"
	# DEFENSE_PERC="defense %"
	# DURATION="duration"
	# ELEMENTAL_RESIST="elemental resist"
	# ELEMENTAL_SHIELD="elemental shield"
	# ENERGY="energy"
	# ENERGY_PERC="energy %"
	# ENERGY_ABSORB="energy absorb"
	# ENERGY_BURN_PERC="energy burn %"
	# ENERGY_LEECH="energy leech"
	# ENERGY_LEECH_RESIST="energy leech resist"
	# ENERGY_REGENERATION="energy/s %"
	# ENERGY_PER_SEC="energy/s"
	# FIRE_RESIST="fire resist"
	# HEALTH="health"
	# HEALTH_PERC="health %"
	# HEALTH_REGENERATION="health/s %"
	# HEALTH_PER_SEC="health/s"
	# JEWELRY_SPIRIT_REQUIREMENTS="jewelry spirit requirements"
	# LIFE_LEECH_RESIST="life leech resist"
	# LIFE_LEECH_RETALIATION="life leech retaliation"
	# LIFESTEAL_PERC="lifesteal %"
	# LIGHTNING_RESIST="lightning resist"
	# MAX_ACID_RESIST="max acid resist"
	# MAX_AETHER_RESIST="max aether resist"
	# MAX_BLEED_RESIST="max bleed resist"
	# MAX_CHAOS_RESIST="max chaos resist"
	# MAX_FIRE_RESIST="max fire resist"
	# MAX_LIGHTNING_RESIST="max lightning resist"
	# MAX_PIERCE_RESIST="max pierce resist"
	# MAX_VITALITY_RESIST="max vitality resist"
	# MELEE_WEAPON_CUNNING_REQUIREMENTS="melee weapon cunning requirements"
	# MELEE_WEAPON_PHYSIQUE_REQUIREMENTS="melee weapon physique requirements"
	# MOVE_SPEED="move speed"
	# MOVE_SPEED_RETALIATION="move speed retaliation"
	# OFFENSE="offense"
	# OFFENSE_PERC="offense %"
	# PET_ACID="pet acid"
	# PET_ACID_RESIST="pet acid resist"
	# PET_AETHER_RESIST="pet aether resist"
	# PET_ALL_DAMAGE_PERC="pet all damage %"
	# PET_ATTACK_SPEED="pet attack speed"
	# PET_BLEED_RESIST="pet bleed resist"
	# PET_CHAOS_RESIST="pet chaos resist"
	# PET_CRIT_DAMAGE="pet crit damage"
	# PET_DEFENSE_PERC="pet defense %"
	# PET_ELEMENTAL_PERC="pet elemental %"
	# PET_ELEMENTAL_RESIST="pet elemental resist"
	# PET_FIRE_DAMAGE_PERC="pet fire damage %"
	# PET_HEALTH_PERC="pet health %"
	# PET_HEALTH_REGENERATION="pet health/s %"
	# PET_HEALTH_PER_SEC="pet health/s"
	# PET_LIFESTEAL_PERC="pet lifesteal %"
	# PET_LIGHTNING_DAMAGE_PERC="pet lightning damage %"
	# PET_MAX_ALL_RESIST="pet max all resist"
	# PET_OFFENSE_PERC="pet offense %"
	# PET_PHYSICAL="pet physical"
	# PET_PIERCE_RESIST="pet pierce resist"
	# PET_PIERCE_RETALIATION="pet pierce retaliation"
	# PET_POISON="pet poison"
	# PET_RETALIATION_PERC="pet retaliation %"
	# PET_TOTAL_SPEED="pet total speed"
	# PET_VITALITY_RESIST="pet vitality resist"
	# PHYSICAL_RESIST="physical resist"
	# PHYSICAL_RETALIATION="physical retaliation"
	# PHYSICAL_TO_CHAOS="physical to chaos"
	# PHYSIQUE="physique"
	# PHYSIQUE_PERC="physique %"
	# PIERCE_RESIST="pierce resist"
	# PIERCE_RETALIATION="pierce retaliation"
	# REDUCE_AETHER_RESIST="reduce aether resist"
	# REDUCE_ELEMENTAL_RESIST="reduce elemental resist"
	# REDUCE_LIGHTNING_RESIST="reduce lightning resist"
	# REDUCE_PHYSICAL_RESIST="reduce physical resist"
	# REDUCE_PIERCE_RESIST="reduce pierce resist"
	# REDUCE_DAMAGE_PERC="reduce damage %"
	# REDUCE_DEFENSE="reduce defense"
	# REDUCED_BLEED_DURATION="reduced bleed duration"
	# REDUCED_BURN_DURATION="reduced burn duration"
	# REDUCED_ELECTROCUTE_DURATION="reduced electrocute duration"
	# REDUCED_ENTRAPMENT_DURATION="reduced entrapment duration"
	# REDUCED_FREEZE="reduced freeze"
	# REDUCED_FREEZE_DURATION="reduced freeze duration"
	# REDUCED_FROSTBURN_DURATION="reduced frostburn duration"
	# REDUCED_POISON_DURATION="reduced poison duration"
	# REDUCED_STUN_DURATION="reduced stun duration"
	# REFLECTED_DAMAGE_REDUCTION="reflected damage reduction"
	# RETALIATION_PERC="retaliation %"
	# SHIELD_PHYSIQUE_REQUIREMENTS="shield physique requirements"
	# SHIELD_RECOVERY="shield recovery"
	# SKILL_COST_PERC="skill cost %"
	# SKILL_DISRUPTION_PROTECTION="skill disruption protection"
	# SLOW_MOVE="slow move"
	# SLOW_RESIST="slow resist"
	# SPIRIT="spirit"
	# SPIRIT_PERC="spirit %"
	# STUN_PERC="stun %"
	# STUN_DURATION="stun duration"
	# STUN_RETALIATION="stun retaliation"
	# TERRIFY_RETALIATION="terrify retaliation"
	# TOTAL_SPEED="total speed"
	# VITALITY_DECAY_RETALIATION="vitality decay retaliation"
	# VITALITY_RESIST="vitality resist"
	# WEAPON_DAMAGE_PERC="weapon damage %"
	# WEAPON_SPIRIT_REQUIREMENTS="weapon spirit requirements"

	def __init__(self, name, stats, bonuses, points):
		self.name = name
		self.stats = stats
		self.bonuses = bonuses
		self.points = points

	@staticmethod
	def loadModel(name):
		file = open(name.lower() + "/" + name.lower() + ".py", "r")
		exec(file.read(), locals())
		model = Model(name, locals()["stats"], locals()["weights"], locals()["devotionPoints"] )
		model.items = locals()["items"]
		model.skills = locals()["skills"]
		model.constellations = locals()["constellations"]
		model.initialize()
		return model

	def initialize(self):
		self.checkModel()
		self.filterConstellations()

		self.seedSolutions = []
		self.readSeedSolutions()

	def __str__(self):
		out = ""
		for key in sorted(self.bonuses.keys()):
			if self.get(key) > 0:
				out += key + " " + str(self.bonuses[key]) + "\n"
		return out

	def addSolution(self, solution):
		self.seedSolutions += [solution]
		self.seedSolutions = list(set(self.seedSolutions))
		self.seedSolutions.sort(key=lambda s: s.score, reverse=True)

	def saveSeedSolutions(self):
		try:
			os.mkdir(self.name.lower())
		except:
			pass

		file = open(self.name.lower()+"/solutions.py", 'w')
		out = "self.seedSolutions = [\n"
		for s in sorted(self.seedSolutions, key=lambda s: s.score, reverse=True):
			out += "  Solution("+solutionPath(s.constellations)+ " self),  # " + str(int(s.score)) + " (" + str(s.cost) + ")\n"
		out += "]"
		file.write(out)
		file.close()

	def readSeedSolutions(self):
		try:
			file = open(self.name.lower()+"/solutions.py", "r")
			lines = file.read()
			file.close()
			exec(lines)
			self.seedSolutions = sorted(list(set(self.seedSolutions)), key=lambda s:s.score, reverse=True)
			print "Reading seed solutions:"
			for s in self.seedSolutions:
				print "  " + str(s)
		except:
			pass

		self.saveSeedSolutions()


	def bonusToPercent(self, bonus):
		return (1+self.getStat(bonus)/100.0)

	def checkModel(self):
		print "Checking model..."
		print "  "+self.name

		self.stats["allAttacks/s"].sort(reverse=True)

		if not "allAttacks/s" in self.stats.keys():
			self.stats["allAttacks/s"] = [self.stats["attacks/s"]]

		# this should eventually be calculated
		if self.get("attack opportunity cost") == 0:
			self.bonuses["attack opportunity cost"] = -self.get("weapon damage %")
			print "  attack opportunity cost", self.bonuses["attack opportunity cost"]

		if not "fight length" in self.stats.keys():
			self.stats["fight length"] = 30

		self.stats["criticals/s"] = self.getStat("attacks/s")*self.getStat("crit chance")

		# /s stats can be calculated based on fight length and the value of the stat

		#1 health/s for a 30s fight is equal to... 30 health, consider the character's % regen stat
		#I'd like to perhaps give a boost to energy since it doesn't fast regen out of combat
		energyBonus = 2

		parts = ["health", "energy"]
		#calculate value of health/s and energy/s
		for part in parts:
			hps = self.get(part) * self.getStat("fight length") * self.bonusToPercent(part + "/s %")
			if part == "energy":
				hps = hps * energyBonus
			self.setCalculated(part+"/s", hps)
		
		#calculate value of health/s % and energy/s %
		#% health/s % affects ALL flat health regen EXCEPT for that gained from Physique.
		# regen from physique = (P-50)*.04

		# figure how much health/s 1 health/s % gives
		# the problem is that health/s is on the sheet as a total i.e. your health/s % is already factored in.
		# so I need to get the base value first			
		hpsP = (self.getStat("physique")-50)*.04
		hpsS = self.getStat("health/s")
		baseHps = (hpsS - hpsP)/self.bonusToPercent("health/s %")
		self.setCalculated("health/s %", baseHps*.01*self.get("health/s"))

		# physique grants health/s, health and defense so this should be accounted for
		val = 0
		val += self.get("health/s") * .04
		val += self.get("health") * 2.5
		val += self.get("defense") * .4

		self.setCalculated("physique", val)

		# cunning grants physical %, pierce %, bleed %, internal % and offense.
		val = 0
		val += self.get("physical %") * .41
		val += self.get("pierce %") * .40
		val += self.get("bleed %") * .46
		val += self.get("internal %") * .46
		val += self.get("offense") * .4

		self.setCalculated("cunning", val)

		# spirit grants fire %, burn %, cold %, frostburn %, lightning %, electrocute %, acid %, poison %, vitality %, vitality decay%, aether %, chaos %, energy and energy regen
		val = 0
		val += sum([self.get(b) for b in ["fire %", "cold %", "lightning %", "acid %", "vitality %", "aether %", "chaos %"]]) * .47
		val += sum([self.get(b) for b in ["burn %", "frostburn %", "electrocute %", "poison %", "vitality decay %"]]) * .5
		val += self.get("energy") * 2
		val += self.get("energy/s") * .01
		val += self.get("energy/s %") * .26

		self.setCalculated("spirit", val)

		# update damage % stats
		self.stats["physical %"] = self.getStat("physical %")  + self.getStat("cunning")*.41
		self.stats["pierce %"] = self.getStat("pierce %")  + self.getStat("cunning")*.41
		self.stats["bleed %"] = self.getStat("bleed %") + self.getStat("cunning")*.46
		self.stats["internal %"] = self.getStat("internal %") + self.getStat("cunning")*.46

		for dam in ["fire %", "cold %", "lightning %", "acid %", "vitality %", "aether %", "chaos %"]:
			if self.getStat(dam) > 0:
				self.stats[dam] = self.getStat(dam) + self.getStat("spirit")*.47

		for dam in ["burn %", "frostburn %", "electrocute %", "poison %", "vitality decay %"]:
			if self.getStat(dam) > 0:
				self.stats[dam] = self.getStat(dam) + self.getStat("spirit")*.5

		#check stats vs % stats
		percStats = ["physique", "cunning", "spirit", "offense", "defense", "health", "energy", "armor"]
		for stat in percStats:
			self.setCalculated(stat+" %", self.getStat(stat) * self.get(stat) / 100)

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
				# pet sheet damage only counts "all damage %" so specific types are lost here
				totalDamagePerc = (self.getStat(damage+" %")+100) + (self.getStat("pet damage %")+100)
				self.setCalculated("reduce "+damage+" resist", totalDamagePerc*.0075*self.get(damage+" %")/3.0)

		self.setCalculated("reduce resist", sum([self.get("reduce "+b) for b in resists]))

		elementals = ["fire", "cold", "lightning"]
		self.setCalculated("reduce elemental resist", sum([self.get("reduce "+b+" resist") for b in elementals]))

		# handle shorthand sets: resist	
		#resist types
		for b in resists:
			self.setIfNull(b, self.get("resist"))
			self.setIfNull("pet "+b, self.get("pet resist"))

		# elemental damage % and resist should be the sum of the individual components
		self.setCalculated("elemental %", sum([self.get(b) for b in ["cold %", "lightning %", "fire %"]]))

		# elemental resists are weird. e.g. fire resist protects against burn and elemental resist protects against fire but elemental resist does not protect against burn
		self.setCalculated("elemental resist", sum([self.get(b) for b in ["cold resist", "lightning resist", "fire resist"]]))

		# all damage should be >= all other damage bonuses (sans retaliation)
		# don't count cold, lightning, or fire as they're already aggregated under elemental
		parts = ["acid %", "aether %", "bleed %", "burn %", "chaos %", "electrocute %", "elemental %", "frostburn %", "internal %", "physical %", "pierce %", "poison %", "vitality %", "vitality decay %"]
		self.setCalculated("all damage %", sum([self.get(b) for b in parts]))

		self.setCalculated("pet all damage %", sum([self.get("pet " + b) for b in parts]))

		total = 0
		for damage in damages:
			total += (self.getStat(damage+" %")+100)*self.get(damage+" %")/100
		
		self.setCalculated("crit damage", total*self.getStat("crit chance"))

		for damage in damages:
			if damage in self.bonuses.keys():
				self.setCalculated("triggered "+damage, self.bonuses[damage]/self.getStat("attacks/s"))

		#calculate elemental damage and triggered elemental damage if not set
		self.setCalculated("elemental", sum([self.get(elemental) for elemental in elementals])/3.0)
		self.setCalculated("triggered elemental", sum([self.get("triggered " + elemental) for elemental in elementals])/3.0)

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
		for speed in ["attack speed", "cast speed", "move speed"]:
			total += self.get(speed)
		self.setCalculated("total speed", total)

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

	def calculateBonus(self, bonus, value):
		#handle flat duration damages being overwritten.
		# the value of flat damage is based on how much damage you'll deliver with it.
		# so 10 fire damage, 1 attack per second, 30 second fight you'll do 300 damage
		# assuming you keep hitting the same target until it dies
		# 10 burn damage over 2 seconds will do 5 damage on the first tick then you'll hit again and overwrite it.
		# so you'll only do 150 damage to that target with your burn damage so we would modify the burn damage to 5.
		# i.e. the slower your weapon the more valuable dot damage is.
		# this doesn't apply to triggered dot damage.
		# if your character play style is more like hit each enemy once so your dots will do the most damage then
		# this would be handled in the value of the stat.
		# skills with a weapon component will tend to mess this calculation up.
		# so if your build is based on skills with a weapon component with a significant cooldown that would be handled in the value of the stat
		if bonus in durationDamages:			
			if type(value) == type([]):
				aps = float(self.getStat("attacks/s"))
				dotDps = value[0] # the duration doesn't really matter since you're unlikely to have an attack speed less than the total duration of the dot (e.g. you won't have an aps of < .5 which is the shortest dot)
				return dotDps / aps * self.get(bonus)

		# TODO pet dot damage is hard to figure since we don't know pet attack speed (it doesn't seem very fast)
		# for now assuming pets attack real slow and deal full duration damage
		if bonus in ["pet " + dd for dd in durationDamages]:
			if type(value) == type([]):
				return self.get(bonus) * value[0]*value[1]
		return self.get(bonus)*value

	def get(self, key):
		if key in self.bonuses.keys():
			return self.bonuses[key]
		else:
			return 0
	def set(self, key, value):
		self.bonuses[key] = value

	def setCalculated(self, key, value):
		out = key + ": " 
		if not key in self.bonuses:
			self.set(key, value)
			print "  " + out + str(self.get(key))
		else:
			print "* " + out + str(self.get(key)) + " (" + str(value) + ")"

	def setIfNull(self, key, value):
		if not key in self.bonuses:
			self.set(key, value)

	def getStat(self, key):
		if key in self.stats.keys():
			return self.stats[key]
		else:
			return 0


	#bonuses
		# select the important bonuses from above and give them a value.
		# Note some bonuses will be automatically calculated if left blank (and should be unless you want to override):
		#	health/s <- health, health/s %, fight length
		#	energy/s <- energy, energy/s %, energy length

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
		# "health/s %":25,

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
