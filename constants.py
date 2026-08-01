# Duration damages are carried around as [damagePerTick, ticks] pairs.
# Defined here (the leaf module) so ability, dataModel and utils all share one copy.
#this will "inflate" duration damages
def addDurationDamages(a, b):
	if a == 0:
		return b
	if b == 0:
		return a
	return [a[0]+b[0], max(a[1],b[1])]

def subDurationDamages(a, b):
	return [a[0]-b[0], max(a[1],b[1])]


damages = [
	"acid", "poison",
	"aether", 
	"bleed", 
	"fire", "burn", 
	"chaos", 
	"lightning", "electrocute", 
	"cold", "frostburn", 
	"physical", "internal",
	"pierce",
	"vitality", "vitality decay",
	"life leech",

	"elemental", 
	"all damage"
]

primaryDamages = [
	"acid",
	"aether", 
	"bleed", 
	"fire",
	"chaos", 
	"lightning",
	"elemental", 
	"cold",
	"physical",
	"pierce",
	"vitality",
	"life leech"
]

durationDamages = [
	"bleed",
	"poison",
	"burn",
	"electrocute",
	"frostburn",
	"internal",
	"vitality decay"
]

magicalDamage = [
	"acid",
	"aether",
	"fire",
	"chaos",
	"lightning",
	"cold",
	"vitality",
	"life leech"
]

magicalDurationDamage = [
	"burn",
	"frostburn",
	"electrocute",
	"poison",
	"vitality decay"
]

physicalDamage = [
	"physical",
	"pierce"
]

physicalDurationDamage = [
	"bleed",
	"internal"
]

retaliations = [
	"chaos retaliation", 
	"life leech retaliation", 
	"pierce retaliation", 
	"vitality decay retaliation", 
	"physical retaliation", 
	"bleed retaliation"
]

resists = [
	"physical resist",
	"fire resist", 
	"cold resist", 
	"lightning resist", 
	"acid resist", 
	"vitality resist", 
	"pierce resist", 
	"aether resist", 
	"chaos resist",
	"bleed resist"
]

elementals = [
	"cold",
	"fire",
	"lightning"
]

