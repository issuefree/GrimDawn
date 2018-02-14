from dataModel import *
from constellationData import *
from itemData import *
from skillData import *
from utils import *
from models import *

from solution import *

import os

model = Model.loadModel("Lochlan")

char = Character(model, [570+200+200, 90+140+150, 170+60+150, 1120+1300, 400+600], model.skills, model.constellations, model.items)

# for bonus in sorted(char.stats):
# 	if char.stats[bonus] != 0:
# 		print bonus.ljust(25), char.stats[bonus]
print
for bonus in sorted(char.results):
	print bonus.ljust(25), char.results[bonus]

char.testStat("Soldier")

# print Skill.skills["Field Command"].getAbility(4).getBonuses(model)

# print
# print Skill.skills["Savagery"].getAbility(1).getBonuses(model)

# def addToStat(stat, value):
# 	global stats
# 	if not stat in stats.keys():
# 		stats[stat] = 0
# 	else:
# 		stats[stat] += value


# stats = {
# 	"cunning":399,
# 	"spirit":534,

# 	"physical %":628,
# 	"bleed %":386,
# 	"internal %":496,
# 	"fire %":487,
# 	"cold %":652,
# 	"lightning %":1923 + 482*.33,
# 	"acid %":298,
# 	"vitality %":298,
# 	"aether %":337,
# 	"chaos %":298,
# 	"burn %":358,
# 	"frostburn %":658,
# 	"electrocute %":1615,
# 	"poison %":298,
# 	"vitality decay %":298,
# }

# addToStat("physical %", stats["cunning"]*.416)
# addToStat("pierce %", stats["cunning"]*.40)
# for damage in physicalDurationDamage:
# 	addToStat(damage + " %", stats["cunning"]*.46)
# for damage in magicalDamage:
# 	addToStat(damage + " %", stats["spirit"]*.47)
# for damage in magicalDurationDamage:
# 	addToStat(damage + " %", stats["spirit"]*.5)

# savagery = {
# 	"aps":2.5,
# 	"physical":(1771+2406)/2,
# 	"cold":(72+90)/2,
# 	"fire":(60+75)/2,
# 	"lightning":(13676+30511)/2,
# 	"aether":49,
# 	"electrocute":(4438+6802)/2,
# 	"bleed":737
# }

# primal = {
# 	"aps":1/2.2,
# 	"physical":(3558+4585)/2,
# 	"cold":(115+144)/2,
# 	"fire":(97+120)/2,
# 	"lightning":(29540+62751)/2,
# 	"aether":79,
# 	"electrocute":(7948+9718)/2,
# 	"bleed":807
# }

# windDevil = {
# 	"aps":2,
# 	"physical":303,
# 	"electrocute":(1664+2102)/4 + 4638/2,
# 	"cold":990,
# 	"lightning":(1893+2939)/2
# }

# stormTotem = {
# 	"aps":2,
# 	"lightning":(2192+5330)/2,
# 	"electrocute":2338/2
# }

# def calcBaseDamage(attack):
# 	global stats

# 	totals = {}

# 	for stat in attack:
# 		if not stat == "aps":
# 			totals[stat] = attack[stat]*attack["aps"]/(stats[stat+" %"]+100)*100.0
# 	return totals

# # print calcBaseDamage(primal)

# totals = {}
# for attack in [savagery, primal, windDevil, stormTotem]:
# 	base = calcBaseDamage(attack)
# 	for stat in base:
# 		if not stat in totals.keys():
# 			totals[stat] = 0
# 		totals[stat] += base[stat]

# print

# for key in stats:
# 	print key.ljust(18), stats[key]

# print

# for key in totals:
# 	print key.ljust(18), totals[key]

