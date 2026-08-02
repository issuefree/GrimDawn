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


def evalItemMods(location, itemType):
	items = Item.getByLocation(location, itemType)
	for item in items:
		item.evaluate(model, location)
		# print(item.name.ljust(20), item.value)
	items.sort(key=lambda i: i.value, reverse=True)
	for item in items:
		if item.value > 0:
			print(item.evaluate(model, location, True))

def evalItems(itemList, slot=None):
	"""Side by side for Items you already have in hand, best first.

	compareGear takes names and finds them; this takes the objects, for
	something built here that the game has no record of.
	"""
	items = [equipment[i] if isinstance(i, str) else i for i in itemList]
	where = [slot or (i.location if isinstance(i.location, str)
					  else (i.location[0] if i.location else "")) for i in items]
	scored = sorted(((item.evaluate(model, w), item, w) for item, w in zip(items, where)),
					reverse=True, key=lambda row: row[0])
	columns = [(item, {b: model.get(b) * (v[0] if isinstance(v, list) else v)
					   for b, v in item.bonuses.items() if model.get(b)})
			   for _, item, _ in scored]
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
	underneath with the share of the fight they are up for.
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
				print("  %-24s %s up %.0f%% of the fight"
					  % (c.name[:24], star.ability.name, 100 * star.ability.effective))


# compareGear("thundertouch", "everliving grove")
# bestInSlot("ring")
# bestInSlot("head", components)
# bestAugments()
# evalCon(falcon, huntressRend)
# evalSol([xA, xC, owl, vulture, jackal, revenant])
# compareGear("bloodreaper's cleaver", "bloodreaper's claw", "duelist's sabre", "pit master's axe", "gorefeast")
compareGear("Briarthorn Band", "band of black ice", "blackwatch seal", "reddan memento ring")