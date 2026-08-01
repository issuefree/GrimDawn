"""Which named equipment itemData.py should carry.

There are some eight thousand gear records and nothing in the data says
which of them matter to a character - that is the one judgement about
items worth making by hand. Add a name here and it appears in itemData.py
on the next  python devotion.py --regenerate  with its current stats.

Names are as the game shows them, Empowered and Mythical prefixes included.
"""
WANTED = [
	"Beastcaller's Shroud",
	'Black Scourge',
	'Death Omen',
	'Empowered Bramblewood Amulet',
	"Empowered Stormcaller's Gem",
	'Lifegiver Signet',
	"Necrolord's Shroud",
	'Pendant of the Royal Crown',
	'Rhowari Lifecaller',
	'Rhowari Void Seal',
	'Seal of the Royal Crown',
	'The Peerless Eye of Beronath',
]

# set bonuses, named "<set> (<pieces worn>)"
WANTED_SETS = [
	"Beastcaller's Regalia (2)",
	"Beastcaller's Regalia (3)",
	"Beastcaller's Regalia (4)",
	'Royal Exuberance (2)',
	'Royal Exuberance (3)',
]
