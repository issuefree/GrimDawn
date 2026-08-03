import sys
from dataModel import *
from constellationData import *
from itemData import *
from utils import *
from models import *

from solution import *

import os

model = Model.loadModel("Morena")

# getBestConstellations/getHighestScoring/getMostEfficient used to run here and
# print the whole ranked list on every start. Nothing below reads any of it -
# it was there to watch the branch-and-bound prune, and that search is gone.
# Call them by hand if you want the ranking:
#     printRanking()

print("------------------------------")


def printRanking(threshold=0):
	"""Every constellation ranked by value and by value per star."""
	ranks = [(c.evaluate(model), c.evaluate(model) / len(c.stars), c)
			 for c in Constellation.constellations]
	print("\n  %-42s %8s %8s" % ("", "score", "/star"))
	for score, perStar, c in sorted(ranks, reverse=True, key=lambda r: r[0]):
		if score > threshold:
			print("  %-42s %8d %8d" % (c.name, score, perStar))

def evalSol(solution):
	# print(getSolutionCost(solution))

	cost = 0
	score = 0
	for c in solution:
		cost += len(c.stars)
		score += c.evaluate(model)
		print(c.name.ljust(33), str(int(c.evaluate(model))).ljust(5), cost)
	print("Total score: ", score)

	if not isGoodSolution(solution):
		print("FAIL")

def printSol(sol):
	bonuses = getBonuses(sol, model)
	calculatedBonuses = []
	for bonus in bonuses:
		value = bonuses[bonus]
		if not type(value) == type([]):
			value = int(value)
		calculatedBonuses.append([bonus, value, int(evaluateBonuses(model, {bonus:bonuses[bonus]}))])
	calculatedBonuses.sort(key = lambda b: b[2], reverse=True)
	for bonus in calculatedBonuses:
		print(bonus[0].ljust(25), str(bonus[1]).ljust(8), str(bonus[2]))

def diffSols(sola, solb):
	print(sola.score, "->", solb.score)
	bonusesa = getBonuses(sola.constellations, model)
	bonusesb = getBonuses(solb.constellations, model)

	bonusesT = {}
	for bonus in bonusesa:
		bonusesT[bonus] = bonusesa[bonus]
	for bonus in bonusesb:
		if bonus in bonusesT.keys():
			if type(bonusesT[bonus]) == type([]):
				bonusesT[bonus] = subDurationDamages(bonusesT[bonus], bonusesb[bonus])
			else:
				bonusesT[bonus] -= bonusesb[bonus]
		else:
			if type(bonusesb[bonus]) == type([]):
				bonusesT[bonus] = [-bonusesb[bonus][0], bonusesb[bonus][1]]
			else:
				bonusesT[bonus] = -bonusesb[bonus]
	calculatedBonuses = []
	for bonus in bonusesT:
		value = bonusesT[bonus]
		if not type(value) == type([]):
			value = int(value)
		calculatedBonuses.append([bonus, value, int(evaluateBonuses(model, {bonus:bonusesT[bonus]}))])
	calculatedBonuses.sort(key = lambda b: b[2], reverse=True)
	for bonus in calculatedBonuses:
		if bonus[2] != 0:
			print(bonus[0].ljust(25), str(bonus[1]).ljust(8), str(bonus[2]))


def compareGear(*names):
	"""Which of these pieces is best for this character, and why.

	Takes names, not Item literals - anything the game has can be named,
	whether or not it is listed in equipmentWanted.py:

		compareGear("thundertouch", "everliving grove")

	Matching ignores case and punctuation and falls back to a substring, so
	part of a name is enough. Prints a row per bonus, a total, and the margin.
	"""
	import gearcompare
	gearcompare.compare(model, names)


def dumpGear(*names):
	"""Print pieces as Item literals, ready to paste into a python file.

		dumpGear("thundertouch", "everliving grove")

	Useful for tinkering with a piece you do not own yet, or for pinning one
	down so it stops changing under you when the game is patched.
	"""
	import gearcompare
	gearcompare.source(names)


def bestInSlot(slot, pool=None, count=3):
	"""The best few things this character could put in one slot.

	pool defaults to augments; pass components or equipment.values() for those.

		bestInSlot("ring")
		bestInSlot("head", components)
	"""
	items = Item.getByLocation(slot, list(pool if pool is not None else augments))
	ranked = sorted(((item.evaluate(model, slot), item) for item in items),
					key=lambda row: row[0], reverse=True)
	print("\n  Best in %s:" % slot)
	for value, item in ranked[:count]:
		if value > 0:
			print("    %-42s %d" % (item.name, value))
	if not ranked or ranked[0][0] <= 0:
		print("    - nothing this character scores")


def bestAugments(count=3):
	"""The top augments for every slot at once, as the solver prints them."""
	import devotion
	devotion.showAugments(model, count)


def evalItemMods(slot, pool=None, count=8, detail=4, level=None):
	"""Everything that fits one slot, ranked, and where each one's value is.

		evalItemMods("medal")
		evalItemMods("axe", augments)
		evalItemMods("axe", level=0)      # everything, whatever the level

	pool defaults to components. count is how many items to list, detail how
	many bonus lines each. A cost - the attack a granted skill gives up - is
	always shown whether or not it makes the cut, since it is the reason an
	item scores less than its stats suggest.

	level defaults to the model's own, because a list topped by things you
	cannot wear is a list you have to read past. Pass a number to ask about a
	level you are planning for, or 0 for everything.

	This used to hand verbose=True to evaluate, which printed an ability's
	trigger arithmetic in the middle of the table and then a bare float on the
	end of it. The breakdown comes from the same function gearcompare prints,
	so a row here and a row there agree.
	"""
	from gearcompare import bonusWorth
	items = Item.getByLocation(slot, list(pool if pool is not None else components))

	if level is None:
		level = model.getStat("level")
	hidden = 0
	if level:
		usable = [i for i in items if i.level <= level]
		hidden = len(items) - len(usable)
		items = usable

	# Against one enemy as well, because a ranking on packs alone is misleading
	# in the one direction that matters: an area skill multiplies by everything
	# it touches, so it climbs over a single-target item that beats it in the
	# fight you actually die in. The x column is how much of a piece is clear
	# speed, and a 1.0 is a piece nothing can take away from you.
	was = model.stats.get("enemies")
	model.stats["enemies"] = 1
	boss = {item.name: item.evaluate(model, slot) for item in items}
	if was is None:
		model.stats.pop("enemies", None)
	else:
		model.stats["enemies"] = was

	ranked = [(item.evaluate(model, slot), item) for item in items]
	ranked = sorted(((v, i) for v, i in ranked if v > 0), reverse=True, key=lambda r: r[0])
	if not ranked:
		print("\n  Nothing this character scores in %s." % slot)
		return

	print("\n  %s, best first%s:"
		  % (slot, "" if not level else " (level %g%s)"
			 % (level, ", %d above it hidden" % hidden if hidden else "")))
	print("    %-36s %4s %8s %8s %6s" % ("", "lvl", "pack", "boss", "x"))
	for value, item in ranked[:count]:
		one = boss.get(item.name, value)
		print("    %-36s %4d %8d %8d %6.2f"
			  % (item.name[:36], item.level, value, one, (value / one) if one else 0))
		named = set(item.bonuses)
		if item.ability and item.abilityCounted:
			named |= set(item.ability.bonuses)
		rows = sorted(((bonusWorth(item, b, model), b) for b in named
					   if abs(bonusWorth(item, b, model)) >= 1), reverse=True)
		shown = rows[:detail] + [row for row in rows[detail:] if row[0] < 0]
		for worth, bonus in shown:
			print("       %-37s %8d" % (bonus[:37], worth))
		rest = sum(worth for worth, _ in rows[detail:] if worth > 0)
		if rest:
			print("       %-37s %8d" % ("... everything else", rest))
		if item.ability and not item.abilityCounted:
			print("       %-37s %8s" % ("(%s not worth using)" % item.ability.name[:24], "-"))

def evalItems(itemList, slot=None):
	"""Side by side for Items, best first, by name or as objects.

		evalItems("vicious spikes")
		evalItems(["vicious spikes", "bloody whetstone"])
		evalItems([myOwnItem], "axe")

	One item or several, named or handed over as objects, so this and
	compareGear differ only in how they lay the answer out. It used to take a
	list of objects and look a string up in `equipment` by exact key, which
	failed two ways at once on a bare name: a string is a list of its own
	characters, so evalItems("vicious spikes") asked for an item called "v",
	and Vicious Spikes is a component, which is not in `equipment` under any
	spelling. Names now go through the same resolver compareGear uses - every
	pool, punctuation and case ignored, falling back to the game's own database
	for anything the data files have not got.
	"""
	if isinstance(itemList, str) or isinstance(itemList, Item):
		itemList = [itemList]
	import gearcompare
	names = [i for i in itemList if isinstance(i, str)]
	found, missing = gearcompare.resolve(names) if names else ([], [])
	for name in missing:
		print("  no item found called %r" % name)
	# resolve returns what it found in its own order - data files first, then
	# anything it had to build from the database - and that is fine here,
	# because the columns get sorted by score and slot is one value for all of
	# them. Nothing downstream depends on the order these arrive in.
	items = [i for i in itemList if not isinstance(i, str)] + found
	if not items:
		return

	where = [slot or (i.location if isinstance(i.location, str)
					  else (i.location[0] if i.location else "")) for i in items]
	scored = sorted(((item.evaluate(model, w), item, w) for item, w in zip(items, where)),
					reverse=True, key=lambda row: row[0])
	# same row arithmetic gearcompare prints, so the two agree and neither keeps
	# its own copy of what a bonus is worth. A granted skill's bonuses are part
	# of the total, so they are part of the rows too - left out, a column did
	# not add up to the figure printed under it.
	from gearcompare import bonusWorth
	columns = []
	for _, item, _ in scored:
		named = set(item.bonuses)
		if item.ability and item.abilityCounted:
			named |= set(item.ability.bonuses)
		columns.append((item, {b: bonusWorth(item, b, model)
							   for b in named if bonusWorth(item, b, model)}))
	bonuses = {b for _, worth in columns for b in worth}
	rows = [(b, [worth.get(b, 0) for _, worth in columns])
			for b in sorted(bonuses, key=lambda b: -max(w.get(b, 0) for _, w in columns))]
	sideBySide([item.name for item, _ in columns], rows,
			   [("slot", [w for _, _, w in scored]),
				("TOTAL", [value for value, _, _ in scored])], width=18)



def sideBySide(headers, rows, footers=(), label=24, width=14):
	"""One column per thing, one row per bonus, biggest contribution first."""
	width = max(width, max((len(h) for h in headers), default=width))
	print("\n  %-*s %s" % (label, "", "  ".join("%*s" % (width, h) for h in headers)))
	print("  %-*s %s" % (label, "", "  ".join("%*s" % (width, "-" * len(h)) for h in headers)))
	for name, values in rows:
		print("  %-*s %s" % (label, name[:label],
							 "  ".join("%*s" % (width, _cell(v)) for v in values)))
	for name, values in footers:
		print("  %-*s %s" % (label, name[:label],
							 "  ".join("%*s" % (width, _cell(v)) for v in values)))


def _cell(value):
	if value == 0:
		return "-"
	return "%d" % value if isinstance(value, float) else str(value)


def evalCon(*constellations):
	"""What each constellation is worth to this character, and where from.

		evalCon(falcon)
		evalCon(falcon, owl)

	Bonuses either one gives are listed together so the difference is one row
	to read. Procs are folded in the way scoring folds them, and named
	underneath with how often each one lands, in its own units.
	"""
	columns = []
	for c in constellations:
		c.evaluate(model)      # scoring an ability writes its share into the stars
		worth = {}
		for star in c.stars:
			for bonus, value in star.bonuses.items():
				if bonus in model.bonuses:
					worth[bonus] = worth.get(bonus, 0) + model.calculateBonus(bonus, value)
		columns.append((c, {b: v for b, v in worth.items() if v}))

	names = [c.name for c, _ in columns]
	bonuses = {b for _, worth in columns for b in worth}
	rows = [(b, [worth.get(b, 0) for _, worth in columns])
			for b in sorted(bonuses, key=lambda b: -max(w.get(b, 0) for _, w in columns))]
	footers = [("TOTAL", [c.evaluate(model) for c, _ in columns]),
			   ("stars", [len(c.stars) for c, _ in columns]),
			   ("per star", [c.evaluate(model) / len(c.stars) for c, _ in columns])]
	sideBySide(names, rows, footers)

	for c, _ in columns:
		for star in c.stars:
			if star.ability:
				print("  %-24s %-22s %s"
					  % (c.name[:24], star.ability.name[:22], star.ability.describe()))


# compareGear("thundertouch", "everliving grove")
# bestInSlot("ring")
# bestInSlot("head", components)
# bestAugments()
# evalCon(falcon, huntressRend)
# evalSol([xA, xC, owl, vulture, jackal, revenant])
# compareGear("bloodreaper's cleaver", "bloodreaper's claw", "duelist's sabre", "pit master's axe", "gorefeast")
# compareGear("Briarthorn Band", "band of black ice", "blackwatch seal", "reddan memento ring")
# evalCon(tsunami, assassin)
evalItemMods("medal", components)
# dumpGear("vicious spikes")
evalItems("vicious spikes")