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

# How long a point of flat duration damage takes to deliver, in seconds. Read
# off the item records rather than guessed: every one of the 264 items carrying
# flat bleeding states three seconds, and the other six types are as close to
# unanimous - 101 of 102 for burn, 63 of 63 for internal trauma, 137 of 139 for
# poison. The game states a duration beside every flat DoT on every item; there
# was no reason for this to be a judgement call.
#
# It matters because a DoT you reapply refreshes rather than stacks, so a point
# of flat bleed delivers min(duration, your attack interval) / duration of what
# a point of flat physical delivers. At three attacks a second that is a ninth,
# where it used to be flatly halved.
DOT_SECONDS = {
	"bleed": 3.0,
	"burn": 3.0,
	"frostburn": 3.0,
	"electrocute": 3.0,
	"vitality decay": 3.0,
	"internal": 5.0,
	"poison": 5.0,
}

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

# Damage types the game will convert between. "10% of Physical Damage converted
# to Fire Damage" is one bonus named "physical to fire", and gddata writes it
# from a record's conversionInType/conversionOutType pair - these are the eleven
# names that pair can produce, so a name built from this list is one the item
# data can actually carry.
convertible = [
	"physical", "pierce", "fire", "cold", "lightning",
	"acid", "vitality", "aether", "chaos", "bleed", "elemental"
]


def conversions():
	"""Every "X to Y" bonus name, in the spelling the item data uses."""
	return ["%s to %s" % (source, target)
			for source in convertible for target in convertible if source != target]

