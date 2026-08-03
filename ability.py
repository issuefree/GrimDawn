import copy
import math
from itertools import chain
from constants import *
import devotionderive

class Ability:
	minTriggerTime = .25  # there are gaps between skills etc
	# What a bare default attack swings for, and the fallback when a character
	# has not said what its own main attack is worth.
	weaponSwing = 100

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
		# set by resolveTiming: the cooldown after the character's reduction, and
		# the whole gap from one firing to the next
		self.rechargeTime = 0
		self.interval = 0
		# how long one cast keeps working; set by resolveDerived
		self.payloadSeconds = 0
		# damage this cast adds itself, and the percentages and durations it adds
		# for itself, none of which is on the character sheet; set by resolveDerived
		self.swingFlat, self.swingBoost, self.swingDuration = {}, {}, {}
		# enemies one cast lands on, after shape and playStyle - only meaningful
		# for the attack types, and kept so a report can name the two factors
		# behind `effective` separately
		self.targets = 1
		self.derived = False # set by resolveDerived on first evaluation

		self.star = None

	def copy(self):
		return Ability(self.name, copy.deepcopy(self.conditions), copy.deepcopy(self.bonuses))

	def gc(self, key):
		if key in self.conditions:
			return self.conditions[key]
		else:
			return 0

	def gb(self, key):
		if key in self.bonuses:
			return self.bonuses[key]
		else:
			return 0

	def mergeBonuses(self, bonusesA, bonusesB):
		bonusesC = {}
		for bonus in bonusesA:
			if bonus in bonusesB:
				bonusesC[bonus] = bonusesA[bonus] + bonusesB[bonus]
			else:
				bonusesC[bonus] = bonusesA[bonus]
		for bonus in bonusesB:
			if not bonus in bonusesA:
				bonusesC[bonus] = bonusesB[bonus]
		return bonusesC

	def getTotalBonuses(self):
		return self.mergeBonuses(self.bonuses, self.dynamicBonuses)

	def getTotalBonus(self, key):
		value = 0
		if key in self.bonuses:
			if type(self.bonuses[key]) == type([]) and value == 0:
				value = self.bonuses[key]
			else:
				# print(self.name)
				# print(self.bonuses)
				# print(key)
				# print(value)
				value += self.bonuses[key]
		if key in self.dynamicBonuses:
			if type(self.dynamicBonuses[key]) == type([]) and value == 0:
				value = self.dynamicBonuses[key]
			else:
				value += self.dynamicBonuses[key]
		return value

	def resolveDerived(self, model):
		"""Fill in shape, targets and duration scaling from the raw game geometry.

		Generated constellation data carries the skill's class and geometry
		rather than a hand-picked shape and target count, so those are worked
		out here - by rule, identically for identical geometry. Abilities that
		still state shape or targets explicitly keep what they state.

		Runs once per ability. Enemy density is a property of the character, so
		this assumes one model per process, which is how the tools drive it.
		"""
		if self.derived:
			return
		self.derived = True

		# How long one cast keeps working: its own stated duration and any
		# damage over time it lays down. Read here rather than in resolveTiming
		# because the duration loop below collapses a [dps, seconds] pair into a
		# scalar, and resolveTiming runs again on every re-evaluation.
		self.payloadSeconds = max([float(self.gc("duration") or 0)]
								  + [float(value[1]) for value in self.bonuses.values()
									 if isinstance(value, list) and len(value) == 2])

		# What this cast puts on the target beyond the weapon damage it scales,
		# captured here for the same reason: the duration loop below turns a
		# [dps, seconds] pair into a scalar and resolveTiming runs again on
		# every re-evaluation. A generated ability names its damage "triggered
		# x"; a mastery skill out of skillData names it plainly.
		self.swingFlat, self.swingBoost, self.swingDuration = {}, {}, {}
		for bonus, value in self.bonuses.items():
			name = bonus[len("triggered "):] if bonus.startswith("triggered ") else bonus
			if name in damages:
				self.swingFlat[name] = value
			elif name.endswith(" %") and name[:-2] in damages:
				self.swingBoost[name[:-2]] = self.swingBoost.get(name[:-2], 0) + value
			elif name.endswith(" duration") and name[:-9] in damages:
				self.swingDuration[name[:-9]] = self.swingDuration.get(name[:-9], 0) + value

		if not self.gc("skillClass"):
			return

		skillClass = self.gc("skillClass")
		if "shape" not in self.conditions:
			self.conditions["shape"] = devotionderive.shapeFor(skillClass)
		# Some projectiles are worth less at the range you fight at than at the
		# range they were built for. Applied to the damage rather than to
		# targets: it is each hit that lands softer, not fewer of them.
		falloff = devotionderive.damageScale(self.gc("damageBands"),
											 model.getStat("playStyle"))
		if falloff != 1:
			for key in list(self.bonuses):
				if ((key.startswith("triggered ") or key == "weapon damage %")
						and not isinstance(self.bonuses[key], dict)):
					value = self.bonuses[key]
					self.bonuses[key] = ([round(value[0] * falloff, 2), value[1]]
										 if isinstance(value, list)
										 else round(value * falloff, 2))

		# A proc's damage is stated per application. How many applications one
		# enemy actually takes depends on the shape and is decided in one place.
		scale = devotionderive.durationScale(self.gc("duration"), self.gc("shape"))
		if scale > 1:
			for key in list(self.bonuses):
				if key.startswith("triggered ") and not isinstance(self.bonuses[key], (list, dict)):
					self.bonuses[key] = round(self.bonuses[key] * scale, 2)

		# A summon's bonuses are what one creature does in one hit. What it adds
		# up to over a lifespan is the pet's own attack speed and the walk to its
		# target, both of which are judgement and so are worked out in
		# devotionderive rather than baked into the data.
		if self.gc("petMode"):
			hits = devotionderive.summonHits(self.gc("lifespan"), self.gc("petAttackSpeed"),
											 self.gc("petMode"), self.gc("petMelee"))
			lifespan = float(self.gc("lifespan") or 0)
			interval = lifespan / hits
			# Everything else is charged per second: an attack proc's damage is
			# per trigger and its effective is triggers per second. A summon's
			# effective is how many are standing, so its damage has to be per
			# second too - what one creature deals over its whole life, divided
			# by how long that life is. Charging the lifetime total against the
			# standing count made Revenant's skeletons worth twenty times what
			# they are.
			perSecond = hits / lifespan if lifespan else hits
			for key in list(self.bonuses):
				value = self.bonuses[key]
				if key == "duration":
					upTime = devotionderive.summonDebuffUpTime(hits, self.gc("lifespan"))
					# a debuff refreshed by each swing does not stack with itself,
					# so it scales with how much of the time it is up, not with
					# how many times it landed
					for debuff in list(value):
						value[debuff] = round(value[debuff] * upTime, 2)
				elif isinstance(value, list):
					# same refresh rule as an attack proc's DoT, but the interval
					# is the pet's own swing rather than the proc's recharge
					damage, ticks = value
					self.bonuses[key] = round(damage * min(ticks, interval or ticks) * perSecond, 2)
				elif key.startswith("triggered "):
					self.bonuses[key] = round(value * perSecond, 2)

	def calculateEffective(self, model, verbose=False):
		self.resolveDerived(model)
		self.calculateTriggerTime(model, verbose)
		if self.triggerTime == -1:
			self.effective = 0
			if "duration" in self.bonuses:
				del self.bonuses["duration"]
			return

		self.resolveTiming(model)

		if self.gc("type") == "buff":
			self.effective = self.getUpTime(model)*max(1, self.derivedTargets(model))
			# print("buff uptime:", self.getUpTime(model))
		if self.gc("type") == "attack" or self.gc("type") == "wps" or self.gc("type") == "aar":

			if self.gc("shape") == "???":
				print("    Shape unknown for", self.name)

			targets = self.effectiveTargets(model)

			if self.gc("trigger") == "manual":
				# one swing given up per cast, however many the cast hits - the
				# divide cancels the targets that effective multiplies back in.
				# A skill with no cooldown used to be handed a one second one
				# here; resolveTiming floors the interval at the attack rate
				# instead, which is the thing that actually limits pressing it.
				#
				# And the swing is charged across everything it would have hit.
				# Both sides of the trade are area effects or neither is: a cast
				# that lands on four was being credited on four while the attack
				# it displaced was charged on one, so any build whose own attack
				# cleaves read every granted skill as free area damage.
				self.bonuses["attack opportunity cost"] = (
					self.mainAttackPercent(model)
					* model.mainAttackTargets() / targets)

			self.targets = targets
			self.effective = self.getNumTriggers(model, verbose)*targets/model.getStat("fight length")

			if verbose:
				print("nt", self.getNumTriggers(model))
				print("effective", self.effective)

			if "duration" in self.bonuses:
				self.setDebuffValue(targets, model)
			# TODO I've removed damage % modifiers from attack abilities as these are only supposed to affect the attack itself not all damage.
			# this needs to be fixed and this can be removed
			for damage in damages:
				if damage+" %" in self.bonuses:
					del self.bonuses[damage+" %"]


			for dam in durationDamages:
				if "triggered "+dam in self.bonuses:
					if type(self.gb("triggered "+dam)) == type([]):
						damage, ticks = self.bonuses["triggered "+dam]
						# a longer bleed is more bleed, but only as far as the
						# next cast: activeSeconds takes it against the interval
						self.bonuses["triggered "+dam] = damage*self.activeSeconds(
							ticks * model.durationScale(dam))

		if self.gc("type") == "shield":
			self.effective = self.getNumTriggers(model)
		if self.gc("type") == "heal":
			# we're counting half effectiveness due to overheal
			self.effective = self.getNumTriggers(model)*.5

			if "duration" in self.bonuses:
				self.setDebuffValue(max(1, self.gc("targets")), model)

		if self.gc("type") == "summon":
			self.effective = self.getUpTime(model)

		if "duration" in self.bonuses:
			# Whatever setDebuffValue did not claim. A buff or a summon is
			# already charged for how much of the fight it is up, and that is
			# the same window its debuff component is on the enemy, so these
			# fold in as ordinary bonuses rather than being scaled again.
			for bonus, value in self.bonuses.pop("duration").items():
				self.bonuses[bonus] = self.gb(bonus) + value

	def effectiveTargets(self, model):
		"""Enemies one cast lands on, after shape, playStyle and the two caps.

		Split out from calculateEffective because it is asked twice now: once
		for the cast being scored, and once for the attack that cast displaces.
		Measuring those two different ways is what made an area skill look like
		free damage.
		"""
		targets = max(1, self.derivedTargets(model))
		# Read rather than gc("shape"): resolveDerived fills that in, and the
		# main attack is asked for its targets without ever being scored. Only
		# where there is a class to read it from, the same condition
		# resolveDerived applies - a hand-written ability with neither keeps the
		# nothing it had rather than being handed a circle.
		shape = self.gc("shape") or (self.gc("skillClass")
									 and devotionderive.shapeFor(self.gc("skillClass")))

		if model.getStat("playStyle") == "ranged":
			# Characters who try to keep enemies as far away as possible. Often kiting.
			# Optimal range 10+ yards
			# Ground target abilities will often miss due to mobility.
			# Circle is strong due to it hitting the point of the enemy spear where most enemies will clump.
			# Cone/line abilities may not hit many enemies due to long range.
			# pbaoe abilities may be of limited value
			if shape == "cone" or shape == "line":
				targets = targets * .75
			elif shape == "ground":
				targets = targets * .5
			elif shape == "circle":
				pass
			elif shape == "pbaoe":
				targets = targets * .125
			elif shape == "melee":
				targets = targets * .05

		elif model.getStat("playStyle") == "shortranged":
			# Characters who have short ranged abilities and try to keep monsters from hittim him but kiting is minimal and mostly for the purposes of clumping.
			# 	Low mobility and close range tend to make crowd control common. Lots of slows and stuns.
			# Optimal range 5-10 yards
			# Ground target abilities are strong due to clumping and funneling.
			# Circle is strong due to clumping and funneling.
			# Cone/line abilities should have the desired effect.
			# pbaoe abilities aren't ideal if they're very short ranged.
			if shape == "cone" or shape == "line":
				pass
			elif shape == "ground":
				targets = targets * 1.25
			elif shape == "circle":
				targets = targets * 1.25
			elif shape == "pbaoe":
				targets = targets * .75
			elif shape == "melee":
				targets = targets * .1

		elif model.getStat("playStyle") == "melee":
			# Characters who engage in melee but aim to kill fast and minimize getting surrounded or take a beating.
			# Optimal range is melee but not surrounded.
			# Ground target abilities are strong due to melee range and not getting surrounded. 
			#	Mobility is required so value may be somewhat limited.
			# Circle is strong due to clumping.
			# Cone/Line abilities are ideal due to keeping enemies close but on one side.
			# pbaoe abilities are strong but not ideal due to trying not to get surrounded.
			if shape == "cone" or shape == "line":
				targets = targets * 1.33
			elif shape == "ground":
				pass
			elif shape == "circle":
				targets = targets * 1.25
			elif shape == "pbaoe":
				pass
			elif shape == "melee":
				pass

		elif model.getStat("playStyle") == "tank":
			# Characters who run into the fray and try to take hits. Often retaliation based.
			# Optimal range is all enemies up close and personal.
			# Ground target abilities are strong due to low mobility and enemy gathering. Not ideal as surrounding can spread them out.
			# Circle is strong due to clumping and gathering.
			# Cone/Line abilities are decent but similar to ground target, enemies can be spread in a lot of directions.
			# pbaoe are ideal.
			if shape == "cone" or shape == "line":
				pass
			elif shape == "ground":
				pass
			elif shape == "circle":
				pass
			elif shape == "pbaoe":
				targets = targets * 1.5
			elif shape == "melee":
				pass

		# Two ceilings, and the playStyle adjustment above has to live under
		# both rather than on top of them.
		#
		# MAX_TARGETS is the bound on how many enemies one proc realistically
		# hits. Applying it in targetsFor and then multiplying by 1.5 for a
		# tank's pbaoe put Tainted Eruption, Blind Fury and Reckless Tempest on
		# six enemies apiece against a stated ceiling of four.
		#
		# And a count of enemies is not a ceiling on the geometry, it is a
		# ceiling on the room: against one enemy nothing hits more than one.
		# That cap used to be applied inside derivedTargets, so a melee
		# character's 1.25 for a circle put every area skill on 1.25 enemies in
		# the boss column - and it never reached an ability that states its own
		# targets at all, which walked past the count entirely.
		limit = model.getStat("enemies") or devotionderive.MAX_TARGETS
		return min(targets, devotionderive.MAX_TARGETS, limit)

	def derivedTargets(self, model):
		"""How many enemies one cast lands on, before the playStyle adjustment.

		Worked out per evaluation rather than cached into conditions the way it
		used to be. It is a property of the character as much as of the skill -
		it reads enemy density - and caching it meant a model could only ever be
		asked about one kind of fight, because resolveDerived runs once and
		changing the density afterwards had no effect. Being able to score the
		same build against a boss and against a pack is the whole point of
		asking.

		Geometry and density only: how many the shape covers in a room that
		thick. What the room actually holds is effectiveTargets' cap, so that
		an ability which states its own targets is bound by it too.

		An ability that states targets outright keeps what it states.
		"""
		if "targets" in self.conditions:
			return self.conditions["targets"]
		if self.gc("type") not in ("attack", "wps", "aar"):
			return 0
		geometry = {k: self.gc(k) for k in
					("radius", "projectiles", "sparkMaxNumber", "waveDistance",
					 "waveStartWidth", "waveEndWidth") if self.gc(k)}
		targets = devotionderive.targetsFor(
			self.gc("skillClass"), geometry.get("radius", 0), geometry.get("projectiles", 0),
			model.getStat("enemy density") or None, geometry)
		# Density says how thickly they stand, not how many there are, and for a
		# chain or a volley it says nothing at all - those hit a fixed number of
		# separate targets however sparse the room.
		return targets

	def resolveTiming(self, model):
		"""Seconds from one firing to the next, and how much of that is cooldown.

		Three things decide it and none of them used to be in one place.

		The cooldown is the game's, less whatever the character's gear takes off
		it. Grim Dawn's "% Reduced Skill Cooldown" is on some fifteen hundred
		item records and nothing here read it, so a build wearing 30% of it was
		scored as though every cooldown were full length - on this skill and on
		every devotion proc with a recharge.

		Then the gap: a proc waits for its trigger, and a skill you press waits
		on you noticing it is ready, which is what minTriggerTime stands in for.

		Then two floors, for a skill you press. You cannot press it more often
		than you can swing, whatever its cooldown says.

		And unless it beats the attack it interrupts, you would not press it
		every swing. A skill carrying at least as much weapon damage as your own
		main attack is worth swinging with instead; one carrying less is a cast
		you fit in, and casting it again before its own payload expires
		refreshes something already running while costing another whole swing.
		So a skill below your main attack repeats no faster than its payload
		lasts - Poison Bomb is 12% weapon damage and a four second cloud.

		What counts as "your main attack" is mainAttackPercent, and it matters:
		against a bare 100% swing Decapitate's 145% looks like an upgrade worth
		spamming, and against a real mastery attack it is not. Each side is
		taken across the enemies it reaches, for the same reason the opportunity
		cost is: a 60% nova landing on four beats a 150% swing landing on one,
		and you would press it every time it came up.
		"""
		reduction = min(90.0, float(model.getStat("reduce cooldown") or 0)) / 100.0
		self.rechargeTime = self.gc("recharge") * (1.0 - reduction)
		interval = self.rechargeTime + self.triggerTime
		if self.gc("trigger") == "manual":
			rate = float(model.getStat("attacks/s") or 0)
			if rate:
				interval = max(interval, 1.0 / rate)
			# Both sides measured the same way. This used to hold the skill's
			# bare weapon damage percentage against a main attack figure that
			# had the main attack's own damage counted into it, so a skill
			# carrying little weapon damage and a lot of its own lost a
			# comparison it should have won.
			mine = model.swingPercent(self.gb("weapon damage %"), self.swingFlat,
									  self.swingBoost, self.swingDuration)
			if (mine * self.effectiveTargets(model)
					< self.mainAttackPercent(model) * model.mainAttackTargets()):
				interval = max(interval, self.payloadSeconds)
			interval = max(interval, self.energyInterval(model))
		self.interval = interval

	def mainAttackPercent(self, model):
		"""Weapon damage of the attack a cast interrupts.

		Pressing a button costs you the attack you would otherwise have made,
		and that attack is whatever your build actually swings with - a mastery
		skill with points in it, not a bare default attack. This was hardcoded
		at 100, which is the bare swing, and it decided two things at once: what
		a cast gives up, and whether a granted skill is good enough to be your
		attack instead. Both were being asked against the wrong opponent.

		Set stats["main attack %"] to what the first entry of allAttacks/s
		swings for. Left unset it falls back to a plain 100, which flatters any
		component skill that carries more.
		"""
		return float(model.getStat("main attack %") or 0) or Ability.weaponSwing

	def energyInterval(self, model):
		"""Seconds between casts that the character can actually pay for.

		The last thing that stops you pressing a button, and the one that was
		missing: Amber's nova costs 55 energy, and spamming it three times a
		second is 165 a second against eight a second of regeneration. Nothing
		checked, so it came out the best component in the slot by double.

		What a fight affords is the regeneration plus the pool, since you may end
		a fight empty - less whatever the rest of the build has already spoken
		for. That subtraction is the point: items are scored one at a time, so
		without it every candidate is handed the whole pool and told it may have
		all of it, and a dozen skills each priced as sole owner of the energy
		all read as affordable when only one of them is. The model works out
		what your main attack costs and takes it off; anything else your
		rotation burns is "energy committed/s", because nothing here can know it.

		A skill that costs nothing is unconstrained.
		"""
		cost = -self.gb("energy")
		if cost <= 0:
			return 0.0
		budget = model.spareEnergy()
		return cost / budget if budget > 0 else float("inf")

	def activeSeconds(self, ticks):
		"""Seconds of a DoT that actually land, per application.

		A DoT reapplied by its own proc refreshes rather than stacking, so one
		application is worth however long it runs before the next one truncates
		it - dps * that, charged once per cast.

		The obvious form is min(duration, interval), and that is what this used
		to be. It over-counts, because the interval is not a fixed number: the
		proc waits a geometric number of attacks, so some gaps run long and lose
		the tail of the DoT while short ones cannot make it back. min() is
		concave, so feeding it the mean interval always reads high - simulated
		against the model's own Poisson assumption it ran 15-30% over on Bull
		Rush, Rend and any proc whose duration is near its interval.

		Taking the expectation properly, with the interval as the cooldown plus
		an exponential wait of mean triggerTime:

			E[min(D, I)] = recharge + triggerTime * (1 - exp(-(D-recharge)/triggerTime))

		which matches simulation to three decimals on every case tried, and
		still collapses to the right answers at the edges - a duration shorter
		than the cooldown lands whole, and a very long one tends to the full
		interval.
		"""
		# the settled part of the interval - cooldown, plus anything the action
		# rate floor added - against the part that is a wait for the trigger
		fixed = max(0.0, self.interval - self.triggerTime)
		if ticks <= fixed:
			return ticks
		if self.triggerTime <= 0:
			# fires on every opportunity, so the interval is just the cooldown
			return min(ticks, fixed) or ticks
		return fixed + self.triggerTime * (1.0 - math.exp(-(ticks - fixed) / self.triggerTime))

	def describe(self):
		"""What this ability's `effective` means, in the units it is actually in.

		`effective` is not one quantity. For an attack it is applications a
		second summed over everything the cast lands on; for a summon it is how
		many are standing; for a shield or a heal it is how many times it fires
		in a fight; only for a buff is it a share of the fight. Printing all of
		them as "hits a second" or as a percentage read plausibly and was wrong
		four times out of five - Arcane Barrier reported "up 640% of the fight".

		An attack is given as its two factors rather than their product, because
		which one is large is the useful part: a slow proc across a pack and a
		fast one on a single target multiply out the same.
		"""
		kind = self.gc("type")
		if kind == "summon":
			return "%.1f standing at once" % self.effective
		if kind in ("attack", "wps", "aar"):
			casts = self.effective / self.targets if self.targets else 0.0
			return "%.2f casts/s x %.1f targets" % (casts, self.targets)
		if kind in ("shield", "heal"):
			return "%.1f times a fight" % self.effective
		return "up %.0f%% of the fight" % min(100, 100 * self.effective)

	def setDebuffValue(self, targets, model, verbose=False):
		#find duration based elements (for attacks that include a debuff component)
		upTime = self.getUpTime(model)
		if verbose:
			print("setDebuffValue", self.name)
			print("  upTime", upTime)
			print("  effective", self.effective)
		durationBonuses = self.bonuses["duration"]
		for bonus in durationBonuses:
			value = durationBonuses[bonus]
			if type(value) == type([]):
				damage, ticks = value
				value = damage*self.activeSeconds(ticks * model.durationScale(bonus))
			self.bonuses[bonus] = value*self.effective
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
		if self.gc("type") == "wps" or self.gc("type") == "aar":
			triggerFrequency = model.getStat("attacks/s")
		else:
			triggerFrequency = model.getStat(self.gc("trigger")+"s/s")
		if triggerFrequency == 0:
			self.triggerTime = -1
			return
		
		self.triggerTime = 1.0/triggerFrequency * 1.0/self.gc("chance")
		# print("tt", self.triggerTime)

	#uptime is a percent so we'll use a scalar of fight length to get an average across multiple fights
	def getUpTime(self, model):
		if self.gc("trigger") == "toggle" or self.gc("trigger") == "passive":
			return 1
		up = 0.0
		fightLen = model.getStat("fight length")*5
		fightRemaining = fightLen - self.triggerTime		
		while fightRemaining >= 0:
			up += min(max(self.gc("duration"), self.gc("lifespan")), fightRemaining)
			fightRemaining -= max(self.gc("duration"), self.interval)
		return up/fightLen

	#average over a number of fights
	def getNumTriggers(self, model, verbose=False):
		numFights = 10.0
		triggers = 0
		fightRemaining = model.getStat("fight length")*numFights - self.triggerTime		
		while fightRemaining >= 0:
			triggers += 1
			fightRemaining -= self.interval

		triggers = max(triggers, 1) # this will usually catch low health events which don't happen often. We'll calculate stats as if they happen once a fight.

		if verbose:
			print(self.name, "getNumTriggers")
			print("   recharge", self.rechargeTime)
			print("   interval", self.interval)
			print("   triggerTime", self.triggerTime)
			print("   fight length", model.stats["fight length"])
			print("   total triggers", triggers)
			print("   nt", triggers/numFights)

		return triggers/numFights

	def calculateDynamicBonuses(self, model, verbose=False):
		self.dynamicBonuses = {}
		if "attack as health %" in self.bonuses:
			totalDamage = 0
			for dam in damages:
				if "triggered "+dam in self.bonuses:
					totalDamage += self.bonuses["triggered "+dam]*(model.getStat(dam+" %")+100)/100.0
			totalDamage = totalDamage*self.bonuses["attack as health %"]/100.0
			# count as half due to overheal
			if "health" in self.bonuses:				
				self.dynamicBonuses["health"] += totalDamage
			else:
				self.dynamicBonuses["health"] = totalDamage


		if self.gc("type") == "attack":
			for dam in damages:
				# % damage depends on a weapon component and a flat damage component to be meaningful
				# technically it could depend on a triggered component of the spell as well but I don't think that scenario exists.
				# actually I think only targo's hammer is an attack ability with a %damage increase.
				if dam+" %" in self.bonuses:
					if model.getStat(dam) <= 0:
						print("    " +self.name+" requires a defined " + dam + " _stat_ in the model.")
					else:
						self.dynamicBonuses[dam] = (model.getStat(dam) * self.gb("weapon damage %")/100.0 + self.gb(dam)) * self.gb(dam+" %")/100.0

		if self.gc("type") == "wps":
			# A weapon pool skill substitutes for the swing it replaces, so it
			# gives up what that swing was worth. One swing, on one enemy,
			# however many the replacement hits - so this is divided by targets
			# for the same reason the manual opportunity cost is: every bonus is
			# multiplied by effective, and effective carries the target count.
			# Left flat, a wps that hits four enemies paid four attacks for one.
			#
			# And the swing it takes the place of is your main attack, not a bare
			# default one. A pool skill rolls on whatever you are swinging with,
			# so a 130% proc is only an upgrade against something worth less -
			# and against however many that swing would have reached, which is
			# the same trade the manual opportunity cost prices.
			self.dynamicBonuses["weapon damage %"] = (
				-self.mainAttackPercent(model) * model.mainAttackTargets()
				/ max(1, self.targets))

		# armor reduction is like + physical damage that isn't affected by %damage
		if self.gb("reduce armor") > 0:
			if model.getStat("physical %") <= 0:
				print("    " +self.name+" requires a defined stat for physical %.")
			else:
				self.dynamicBonuses["physical"] = self.gb("reduce armor")*.7 / (model.getStat("physical %")/100.0)

	def getBonuses(self, model):
		bonuses = {}
		self.calculateEffective(model)
		# print("Effective %:", self.name, self.effective)

		self.calculateDynamicBonuses(model)

		# if the ability has been manually valued in the model
		modelFactor = 1
		if self.name in model.bonuses:
			modelFactor = model.get(self.name)

		for bonus in chain(self.bonuses.keys(), self.dynamicBonuses.keys()):
			total = self.getTotalBonus(bonus)
			if type(total) == type([]):
				total = [total[0]*self.effective*modelFactor, total[1]]
			else:
				total = total*self.effective * modelFactor
			bonuses[bonus] = total
		return bonuses


	def calculateValue(self, model):
		self.calculateEffective(model)
		# print("Effective %:", self.name, self.effective)

		self.calculateDynamicBonuses(model)
		
		# if the ability has been manually valued in the model
		modelFactor = 1
		if self.name in model.bonuses:
			modelFactor = model.get(self.name)

		for bonus in chain(self.bonuses.keys(), self.dynamicBonuses.keys()):
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
		if "ability damage %" in ability.bonuses:
			for damage in damages+["weapon damage %"]:
				if damage in self.bonuses:
					if type(self.bonuses[damage]) == type([]):						
						self.bonuses[damage] = [self.bonuses[damage][0]*(1+ability.bonuses["ability damage %"]/100.0), self.bonuses[damage][1]]
					else:
						self.bonuses[damage] *= 1+ability.bonuses["ability damage %"]/100.0
			del ability.bonuses["ability damage %"]
		for bonus in ability.bonuses:
			if type(ability.bonuses[bonus]) == type([]):
				if bonus in self.bonuses:					
					self.bonuses[bonus] = addDurationDamages(self.bonuses[bonus], ability.bonuses[bonus])
				else:
					self.bonuses[bonus] = ability.bonuses[bonus]
			elif type(ability.bonuses[bonus]) == type({}):
				if bonus in self.bonuses:
					self.bonuses[bonus] = self.mergeBonuses(self.bonuses[bonus], ability.bonuses[bonus])
				else:
					self.bonuses[bonus] = ability.bonuses[bonus]
			else:
				if verbose:
					print(bonus, self.gb(bonus))
				self.bonuses[bonus] = self.gb(bonus) + ability.bonuses[bonus]

