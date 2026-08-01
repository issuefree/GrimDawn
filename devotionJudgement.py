"""Hand-maintained modelling judgment for devotion procs.

Everything else about a constellation can be generated from the game files.
These two values appear nowhere in the game data:

  targets - how many enemies the proc realistically hits in play
  shape   - cone | line | circle | pbaoe | ground | melee

Keyed by ability name; regenerating constellation data must never rewrite
this file. Comments are the original reasoning, preserved verbatim.
"""

JUDGEMENT = {
	# weird shape. It hits the target and things behind it in a cone. It's pretty strong for a
	# ny kiter. Shortranged may suffer since the direction will be pretty random in aoe situat
	# ions.
	"Acid Spray":                    {"targets": 2},   # Manticore (+1 variant)
	# aoe is on target it ticks per second for duration it stacks on itself
	"Aetherfire":                    {"targets": 1.5, "shape": 'ground'},   # Imp
	"Arcane Bomb":                   {"targets": 2, "shape": 'ground'},   # Widow
	# projectiles fire in every direction. I think I'll use pbaoe shape since it's best if sur
	# rounded.
	"Blades of Wrath":               {"targets": 4, "shape": 'pbaoe'},   # Assassin (+1 variant)
	# If we assume everything has enough armor for all of the reduce armor to take effect (if 
	# they have less and we're doing physical damage they're probably dead already anyway) The
	# n if we know our flat physical we can assume 70% absorb
	"Blind Fury":                    {"targets": 2.5, "shape": 'pbaoe'},   # Oleron (+1 variant)
	# 2m radius looks like there are multiple missiles but it's not listed
	"Blizzard":                      {"targets": 3, "shape": 'ground'},   # Amatok the Spirit of Winter (+1 variant)
	# 25% on attack .5s recharge 3.5 meter radius 2 targets 4 attacks trigger, 1 attack rechar
	# ge
	"Bull Rush":                     {"targets": 2, "shape": 'pbaoe'},   # Bull
	# 3m radius cleansing effect is very hard to quantify :(
	"Cleansing Waters":              {"targets": 2, "shape": 'pbaoe'},   # Ulo the Keeper of the Waters (+1 variant)
	# says "spreads wildly among your foes" max 3 Jumps 4m. I'm going to call it 2.5 targets f
	# or now rapidly reapplying seems to prevent spreading. it doesn't seem to stack
	"Eldritch Fire":                 {"targets": 2.5},   # Solael's Witchblade
	"Elemental Storm":               {"targets": 2.5, "shape": 'ground'},   # Rhowan's Crown (+2 variants)
	# 6 projectiles 150 deg cone multi hit doesnt stack
	"Falcon Swoop":                  {"targets": 3, "shape": 'cone'},   # Falcon
	# small enough to not catch multiples.
	"Fetid Pool":                    {"targets": 1, "shape": 'ground'},   # Affliction (+1 variant)
	# 1 meter radius 7 fragments trigger creates a volcano that spits out 8 volleys of ~7 fire
	# balls about 2m there can be multiples active.
	"Fissure":                       {"targets": 2, "shape": 'ground'},   # Magi (+1 variant)
	"Fist of Vire":                  {"targets": 1.5, "shape": 'circle'},   # Vire, the Stone Matron (+1 variant)
	# 100% pass through 2 projectiles (I can't tell if each hits. I'll count like they do.)
	"Flame Torrent":                 {"targets": 3, "shape": 'pbaoe'},   # Fiend
	# this one is pretty cool. when it triggers an eye floats around me in a circle hitting th
	# ings as it goes. pretty small range it circles 5 times before disappearing
	"Guardian's Gaze":               {"targets": 7.5, "shape": 'pbaoe'},   # Eye of the Guardian
	# says it'll 10 targets but how often will that actually happen. Dropping to 5.
	"Hand of Ultos":                 {"targets": 3.5},   # Ultos, Shepherd of Storms (+1 variant)
	# 20% when attacked 4s recharge 5m radius
	"Light of Empyrion":             {"targets": 3, "shape": 'pbaoe'},   # Light of Empyrion
	# 4.5m radius
	"Maul":                          {"targets": 3, "shape": 'pbaoe'},   # Dire Bear (+1 variant)
	# 6m area 2m radius 15 meteors large area, call it 4 targets in the area each missile hits
	#  a smallish area, let's say each target gets hit 3 times let's say the burn overlaps twi
	# ce.
	"Meteor Shower":                 {"targets": 4, "shape": 'ground'},   # Ulzuin's Torch (+1 variant)
	# haven't seen this one in actions so all of these numbers are guestimates
	"Phoenix Fire":                  {"targets": 2.5, "shape": 'pbaoe'},   # Alladrah's Phoenix
	# 3 target max 8 meter radius .5s interval 12 bolts
	"Reckless Tempest":              {"targets": 3},   # Tempest (+1 variant)
	# I'm treating reduced offense like defense so don't count the targets (it's built into th
	# at conversion) reduced resist only matters when other stuff hits so reducing resist on s
	# tuff I'm not hitting doesn't count for anything. remove the multi target component (I'm 
	"Rend":                          {"targets": 3, "shape": 'circle'},   # Huntress (+1 variant)
	# untested
	"Rumor":                         {"targets": 3},   # Murmur, Mistress of Rumors (+1 variant)
	# it's a pbaoe with a decent range. It's weird for a ranged character since it triggers cl
	# ose to you regardless of what you hit. It can be put on a pet or totem so it'll pbaoe wh
	# atever they're hitting so it's still pretty decent. Still cutting this down to 2 targets
	"Scorpion Sting":                {"targets": 2, "shape": 'pbaoe'},   # Scorpion (+1 variant)
	# .5m radius
	"Spear of the Heavens":          {"targets": 1.5, "shape": 'circle'},   # Spear of the Heavens
	# 10 meter radius (huge)
	"Tainted Eruption":              {"targets": 3, "shape": 'pbaoe'},   # Abomination (+1 variant)
	"Targo's Hammer":                {"targets": 2, "shape": 'pbaoe'},   # Anvil
	# long line in direction of hitter
	"Trample":                       {"targets": 2.5, "shape": 'line'},   # Autumn Boar (+1 variant)
	# 35% on attack 12m range pretty wide line attack from me toward target with 100% pass thr
	# ough
	"Tsunami":                       {"targets": 2.5, "shape": 'line'},   # Tsunami
	# two spikes shoot out from you toward what you triggered on. They're pretty narrowly focu
	# sed and not particularly well aimed. They don't seem to hit a ton. On the fence on 1.5 -
	#  2 targets.
	"Twin Fangs":                    {"targets": 1.5, "shape": 'cone'},   # Bat
	# giving it 3 targets since it's 0 recharge I can keep a few going.
	"Wendigo's Mark":                {"targets": 3},   # Wendigo
	# 30% on attack 3 second recharge 6 second duration 3.5 meter radius ticks per second, col
	# d stacks, fostburn doesnt big radius but i'm taking a damage tick away because it's long
	#  lasting ground target
	"Whirlpool":                     {"targets": 2, "shape": 'ground'},   # Leviathan (+1 variant)
	"Will of Rattosh":               {"targets": 1},   # Rattosh, the Veilwarden
}
