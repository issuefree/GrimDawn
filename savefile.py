"""Read what the game's own save files say about your characters.

A player.gdc is obfuscated rather than encrypted: the first word is a seed,
XORed with 0x55555555, and from it a 256-entry table is built by rotating right
one bit and multiplying by 39916801. Every value read is XORed with a running
key, and the key is then advanced by XORing in table[b] for each *ciphertext*
byte consumed. Nothing is secret; it just cannot be read out of order, because
the key depends on everything read before it.

The header reads every character's name, mastery combination and level. The body
now opens too: what had stalled it was four fields between the header and the
first block that nothing was reading - a byte, an int read without advancing the
key, the data version, and a sixteen-byte uid. With those consumed the blocks
fall out with the right types and lengths and a zero trailer on each, which is
the check that the key is still in step.

The blocks are read as far as the skills, which is what there was to get: the
ranks you have spent points on, the attributes and base health before gear, and
the total devotion earned.

    python savefile.py            every character, against what its model says
    python savefile.py Gwyr       his skills, in the syntax a rotation wants
    python savefile.py Gwyr gear  what he is wearing, and what is in it

Nothing can be skipped, because the key advances on every ciphertext byte
consumed - and nothing can be walked blindly either, because a nested block
declares its length and a length is read *without* advancing the key. So the
inventory and the stash are opened properly at their block boundaries and their
contents consumed byte by byte: no item is interpreted, which is deliberate,
since the item record is the part of this format that keeps changing shape.

Every block checks itself against its own declared end. Landing on the promised
byte with a zero after it is not something a wrong field order does by accident,
which is what makes the rest of it trustworthy.
"""
import os
import struct

# Where the game keeps them. GRIM_DAWN_SAVE overrides, the way GRIM_DAWN_DIR
# does for the game's own data.
SAVE = os.environ.get(
	"GRIM_DAWN_SAVE",
	os.path.join(os.path.expanduser("~"), "Documents", "My Games", "Grim Dawn",
				 "save", "main"))

# tagSkillClassName<NN><MM> names the two masteries, in the order the game
# numbers them - the same numbering skillgen walks as records/skills/playerclassNN.
MASTERIES = {
	1: "Soldier", 2: "Demolitionist", 3: "Occultist", 4: "Nightblade",
	5: "Arcanist", 6: "Shaman", 7: "Inquisitor", 8: "Necromancer",
	9: "Oathkeeper", 10: "Berserker",
}


class Reader(object):
	"""Sequential reader over one obfuscated save."""

	def __init__(self, data):
		self.d = data
		seed = struct.unpack_from("<I", data, 0)[0] ^ 0x55555555
		self.table = []
		k = seed
		for _ in range(256):
			k = ((k >> 1) | (k << 31)) & 0xFFFFFFFF
			k = (k * 39916801) & 0xFFFFFFFF
			self.table.append(k)
		self.key = seed
		self.pos = 4

	def u32(self, update=True):
		raw = self.d[self.pos:self.pos + 4]
		value = struct.unpack("<I", raw)[0] ^ self.key
		if update:
			for b in raw:
				self.key ^= self.table[b]
		self.pos += 4
		return value

	def u8(self):
		b = self.d[self.pos]
		value = b ^ (self.key & 0xFF)
		self.key ^= self.table[b]
		self.pos += 1
		return value

	def string(self):
		return "".join(chr(self.u8()) for _ in range(self.u32()))

	def wstring(self):
		"""Two bytes a character; the length counts characters, not bytes."""
		return "".join(chr(self.u8() | (self.u8() << 8)) for _ in range(self.u32()))


def readHeader(path):
	"""name, masteries and level, or None if this is not a save we understand.

	Returns the reader alongside, positioned at the first block, so a caller
	that wants the body does not have to decode the header a second time - and
	could not, since the key state is what it is.
	"""
	with open(path, "rb") as handle:
		data = handle.read()
	reader = Reader(data)
	if reader.u32() != 0x58434447:
		return None
	reader.u32()                       # format version, 2 for every save here
	name = reader.wstring()
	reader.u8()                        # sex, which nothing scores
	tag = reader.string()
	level = reader.u32()
	hardcore = reader.u8()

	# The four fields that had the body looking like noise. The middle one is
	# read without advancing the key, which is the format's way of marking a
	# length or a version it does not want folded into the cipher state - the
	# same treatment every block length gets below.
	reader.u8()                        # 7 on these saves, 3 on older ones
	reader.u32(update=False)           # always 0
	dataVersion = reader.u32()         # 8
	uid = bytes(reader.u8() for _ in range(16))

	return {"name": name, "level": level, "hardcore": bool(hardcore),
			"classTag": tag, "masteries": masteriesOf(tag),
			"dataVersion": dataVersion, "uid": uid,
			"reader": reader, "data": data}


def blocks(header):
	"""Walk the file's blocks, yielding (type, start, length) for each.

	Stops at the first block it cannot walk, which is the third - a block's own
	bytes can be consumed without understanding them, but not one that contains
	a nested length. readCharacter goes further by opening those properly.
	"""
	reader, data = header["reader"], header["data"]
	while reader.pos < len(data) - 8:
		start = reader.pos
		kind = reader.u32()
		length = reader.u32(update=False)
		end = reader.pos + length
		if length <= 0 or end > len(data):
			return
		while reader.pos < end:
			reader.u8()
		if reader.u32(update=False) != 0:
			return                     # trailer is not zero, so the key is out
		yield kind, start, length


# Block 2 is the same forty-eight bytes on every save: a version and eleven
# fields. The three that matter are total devotion, which is the one number
# kieri and lachesis could not be modelled without, and the attributes and base
# health, which are what you have before gear - and base health is what a
# "+% Health" bonus multiplies and is on no character sheet at all. lochlan's
# reads 1070 against the 1070 he read off the game by hand.
ATTRIBUTES = ["level", "experience", "attribute points", "skill points",
			  "devotion points", "total devotion",
			  "physique", "cunning", "spirit", "health", "energy"]
FLOATS = {"physique", "cunning", "spirit", "health", "energy"}


def readAttributes(header):
	"""The attribute block, or None if the walk does not reach it.

	Block 1 is character info and is walked past rather than read: it is a
	different length on every character and nothing in it is wanted yet. It
	cannot be skipped, only consumed, because the key advances on every byte.
	"""
	import struct
	walker = blocks(header)
	try:
		next(walker)                       # block 1, consumed to keep the key
	except StopIteration:
		return None
	reader, data = header["reader"], header["data"]
	if reader.pos >= len(data) - 8:
		return None
	reader.u32()                           # block type, 2
	length = reader.u32(update=False)
	end = reader.pos + length
	reader.u32()                           # block version
	out = {}
	for name in ATTRIBUTES:
		if reader.pos >= end - 3:
			break
		value = reader.u32()
		if name in FLOATS:
			value = struct.unpack("<f", struct.pack("<I", value))[0]
		out[name] = value
	return out


def _blockStart(reader, expect=None):
	"""(type, end). The length is read without advancing the key, as the format
	has it - that is the whole reason a block cannot be walked blindly."""
	kind = reader.u32()
	length = reader.u32(update=False)
	if expect is not None and kind != expect:
		raise ValueError("expected block %d, found %d" % (expect, kind))
	return kind, reader.pos + length


def _blockEnd(reader, end):
	"""The check that the parse of a block was exactly right.

	Landing on the byte the length promised, with a zero after it, is not
	something a wrong field order does by accident - which is why every block
	below is trusted once it passes.
	"""
	if reader.pos != end:
		raise ValueError("block ended at %d, expected %d" % (reader.pos, end))
	if reader.u32(update=False) != 0:
		raise ValueError("block trailer is not zero")


def _list(reader, element):
	return [element(reader) for _ in range(reader.u32())]


def _item(reader, version=11):
	"""One item: what it is, what rolled on it and what is socketed into it.

	Eight strings and six numbers, of which the names are the part worth having.
	The seeds decide which affix values rolled and the records carry only the
	ranges, so a seed without the game's own roller says nothing.
	"""
	base = reader.string()
	prefix = reader.string()
	suffix = reader.string()
	reader.string(); reader.string()                # modifier, transmute
	reader.u32()                                    # seed
	component = reader.string()
	reader.string()                                 # relic bonus
	reader.u32()                                    # component seed
	augment = reader.string()
	# Four in inventory version 4, eight in 11. Two of these characters have not
	# been loaded since that changed and are still on the short one.
	for _ in range(8 if version >= 11 else 4):
		reader.u32()
	return {"base": base, "prefix": prefix, "suffix": suffix,
			"component": component, "augment": augment}


def _equipped(reader, version=11):
	item = _item(reader, version)
	reader.u8()                                     # attached
	return item


def _uids(reader, count):
	for _ in range(count):
		for _ in range(reader.u32()):
			for _ in range(16):
				reader.u8()


def _skill(reader, version=8):
	"""One entry of the skills block: a record path and what you have in it.

	Twenty-eight bytes after the name in these saves, where a version-5
	reference lists twenty-seven - one more byte among the unknowns. The count
	is what matters, because landing anywhere else puts the next name out and
	the whole list with it.
	"""
	name = reader.string()
	level = reader.u32()
	reader.u8()                                     # enabled
	devotionLevel = reader.u32()
	reader.u32()                                    # experience
	reader.u32()                                    # active
	reader.u8(); reader.u8()                        # two unknowns
	if version >= 8:
		reader.u8()                                 # and a third, added since
	reader.string(); reader.string()                # autocast skill and controller
	return {"record": name, "level": level, "devotionLevel": devotionLevel}


def _itemSkill(reader):
	"""A skill something grants you, and what is bound to it.

	Four strings and nothing else. The middle two are the interesting part: they
	are the devotion proc bound to this skill and the controller that decides
	when it fires, which is the binding the optimiser spends its whole time
	choosing and has never been able to read back.
	"""
	record = reader.string()
	bound = reader.string()
	controller = reader.string()
	# What granted it, and how it is spelled depends on what that was. A
	# component puts an int in front of the path - armitage's Brutal Shield Slam
	# comes off compa_reinforcedshell and does - where a transformation does not;
	# fenris's Feral Claws comes off werewolf1 and goes straight to the path. So
	# the path is looked for rather than assumed to be next.
	mark, key = reader.pos, reader.key
	source = reader.string()
	if not source.startswith("records/"):
		reader.pos, reader.key = mark, key
		reader.u32()
		source = reader.string()
	return {"record": record, "boundSkill": bound,
			"controller": controller, "source": source}


def readCharacter(path):
	"""Everything up to and including the skills, or as far as it gets.

	The blocks have to be read in order and in full: the key advances on every
	ciphertext byte, so nothing can be skipped, and a length is read without
	advancing it, so nothing can be walked blindly either. Each block checks
	itself against its own declared end.
	"""
	header = readHeader(path)
	if not header:
		return None
	reader = header["reader"]

	_, end = _blockStart(reader, 1)                 # character info
	while reader.pos < end:
		reader.u8()
	_blockEnd(reader, end)

	_, end = _blockStart(reader, 2)                 # attributes
	reader.u32()                                    # version
	import struct
	for name in ATTRIBUTES:
		value = reader.u32()
		header[name] = (struct.unpack("<f", struct.pack("<I", value))[0]
						if name in FLOATS else value)
	_blockEnd(reader, end)

	# The inventory and the stash are read for position only. Nothing here scores
	# an item, and the item record has changed shape between game versions - it
	# grew four fields since the reference this was written against, and two
	# characters carry something that is a different shape again. So the bytes
	# are consumed rather than interpreted.
	#
	# That is safe exactly as far as the nested blocks: a sack and a stash tab
	# each declare their own length, and a length is read without advancing the
	# key, so those have to be opened properly. Inside one there are only items,
	# which carry no lengths, so consuming them byte by byte keeps the key right
	# whatever shape they are.
	_, end = _blockStart(reader, 3)                 # inventory
	version = reader.u32()
	header["equipped"] = []
	if reader.u8():
		bags = reader.u32()
		reader.u32(); reader.u32()                  # focused, selected
		for _ in range(bags):
			# The bags are loot and are consumed, not read. Whatever odd thing
			# is sitting in one cannot break the parse that way, and two of
			# these characters carry something the item layout below does not
			# describe.
			_, sackEnd = _blockStart(reader)
			while reader.pos < sackEnd:
				reader.u8()
			_blockEnd(reader, sackEnd)
		# What you are wearing, which is the part worth having: twelve slots,
		# then two weapon sets of two. Attempted, and consumed if it does not
		# land on the block's own end, so a shape we have not seen costs the
		# gear and not the skills.
		mark, key = reader.pos, reader.key
		try:
			reader.u8()                             # use alternate
			worn = [_equipped(reader, version) for _ in range(12)]
			reader.u8()
			worn += [_equipped(reader, version) for _ in range(2)]
			reader.u8()
			worn += [_equipped(reader, version) for _ in range(2)]
			if reader.pos != end:
				raise ValueError("equipment did not land on the block end")
			header["equipped"] = [w for w in worn if w["base"]]
		except Exception:
			reader.pos, reader.key = mark, key
	while reader.pos < end:
		reader.u8()
	_blockEnd(reader, end)

	_, end = _blockStart(reader, 4)                 # stash
	reader.u32()                                    # version
	for _ in range(reader.u32()):
		_, tabEnd = _blockStart(reader)
		while reader.pos < tabEnd:
			reader.u8()
		_blockEnd(reader, tabEnd)
	while reader.pos < end:
		reader.u8()
	_blockEnd(reader, end)

	for kind, groups in ((5, 3), (6, 3), (7, 3), (17, 6)):
		_, end = _blockStart(reader, kind)
		reader.u32()                                # version
		_uids(reader, groups)
		if kind == 5:
			for _ in range(3):                      # where you respawn, per difficulty
				for _ in range(16):
					reader.u8()
		_blockEnd(reader, end)

	_, end = _blockStart(reader, 8)                 # skills
	# Two versions in play across these saves: 8 on most, 6 on two of them, and
	# the record is a byte shorter in 6. Getting it wrong does not misread one
	# skill, it puts the next name out and every skill after it with it.
	version = reader.u32()
	header["skills"] = _list(reader, lambda r: _skill(r, version))
	# Masteries allowed, the two reclamation counts, and a fourth this version
	# adds. Reading three and a trailing int instead balances the books whenever
	# the item-skill list is empty, which is why it looked right on the seven
	# characters who carry no item skill and wrong on the four who do.
	reader.u32(); reader.u32(); reader.u32()        # masteries allowed, two reclamations

	# What follows is the skills something else grants you and what is bound to
	# each. It is worth having - the middle two strings of an entry are the
	# devotion proc bound to that skill and the controller that fires it, which
	# is the binding this whole program exists to choose - but its shape varies
	# between characters in a way four saves were not enough to pin down.
	#
	# So it is attempted, and where it does not come out exactly on the block's
	# own end the bytes are consumed instead. The ranks above are the point and
	# they are already read; this is the part that can be missing without
	# costing anything. The block still has to end where it said it would.
	mark, key = reader.pos, reader.key
	try:
		granted = _list(reader, _itemSkill) + _list(reader, _itemSkill)
		if reader.pos != end:
			raise ValueError("item skills did not land on the block end")
		header["itemSkills"] = granted
	except Exception:
		reader.pos, reader.key = mark, key
		header["itemSkills"] = []
		while reader.pos < end:
			reader.u8()
	_blockEnd(reader, end)
	return header


def masteriesOf(tag):
	"""["Soldier", "Demolitionist"] from tagSkillClassName0102."""
	digits = tag[len("tagSkillClassName"):] if tag.startswith("tagSkillClassName") else ""
	out = []
	for i in range(0, len(digits) - 1, 2):
		name = MASTERIES.get(int(digits[i:i + 2]))
		if name:
			out.append(name)
	return out


def characters(root=None):
	"""Every character the save folder holds, by name."""
	root = root or SAVE
	out = {}
	if not os.path.isdir(root):
		return out
	for folder in sorted(os.listdir(root)):
		path = os.path.join(root, folder, "player.gdc")
		if not os.path.exists(path):
			continue
		try:
			header = readHeader(path)
		except Exception:
			continue
		if header and header["name"] not in out:
			header["path"] = path
			out[header["name"]] = header
	return out


def show(root=None):
	"""Print what the saves say, against what the model files say."""
	found = characters(root)
	if not found:
		print("  no saves under %s - set GRIM_DAWN_SAVE" % (root or SAVE))
		return
	print("\n  %-11s %5s %6s %5s %5s %5s %8s  %s"
		  % ("character", "level", "devot", "phys", "cunn", "spir", "base hp",
			 "masteries"))
	for name in sorted(found):
		header = readHeader(found[name]["path"])
		if not header:
			continue
		try:
			attributes = readAttributes(header) or {}
		except Exception:
			attributes = {}
		stale = []
		for label, mine, key in (("level", header["level"], "level"),
								 ("devotionPoints", attributes.get("total devotion"),
								  "devotionPoints")):
			stated = _modelStat(name, key)
			if stated is not None and mine is not None and stated != mine:
				stale.append("%s %g" % (label, stated))
		stale = ("   <- model says " + ", ".join(stale)) if stale else ""
		print("  %-11s %5d %6s %5s %5s %5s %8s  %s%s"
			  % (name, header["level"],
				 _num(attributes.get("total devotion")),
				 _num(attributes.get("physique")), _num(attributes.get("cunning")),
				 _num(attributes.get("spirit")), _num(attributes.get("health")),
				 ", ".join(header["masteries"]) or "?", stale))
	print("\n  devot is total devotion earned. The attributes and base health are\n"
		  "  what you have before gear, which is what a \"+%\" of each multiplies -\n"
		  "  and base health is on no character sheet at all.")


def skillsOf(name, root=None):
	"""[(skill name, points spent)] for one character, biggest first.

	The save stores record paths; the names come from the same place skillgen
	takes them, which is the first record in the chain that has one. Points
	spent, not the rank the skill screen shows - that is this plus whatever your
	gear grants, which is what "+skills" in a model is for.
	"""
	from gddata import Database, procRecords
	found = characters(root)
	if name not in found:
		return []
	character = readCharacter(found[name]["path"])
	db = Database()
	out = []
	for entry in character["skills"]:
		if not entry["level"]:
			continue
		record = db.read(entry["record"])
		if not record:
			continue
		label = next((db.name(r) for r in procRecords(record, db) if db.name(r)), "")
		if label:
			out.append((label, entry["level"]))
	return sorted(out, key=lambda row: (-row[1], row[0]))


def gearOf(name, root=None):
	"""[(item name, component, augment)] for what a character is wearing.

	The names come from the game's own records, the way skillgen takes a skill's
	name. A prefix and a suffix are recorded too, but they are tags rather than
	rolled values - the record carries the range and the seed picks from it - so
	only what the piece is, and what is socketed into it, is reported.
	"""
	from gddata import Database
	found = characters(root)
	if name not in found:
		return []
	character = readCharacter(found[name]["path"])
	db = Database()

	def label(path):
		record = db.read(path) if path else None
		return (db.name(record) if record else "") or (
			path.split("/")[-1][:-4] if path else "")

	out = []
	for worn in character["equipped"]:
		out.append((label(worn["base"]), label(worn["component"]),
					label(worn["augment"])))
	return out


def showGear(name, root=None):
	"""Print what a character is wearing, with what is socketed into it."""
	rows = gearOf(name, root)
	if not rows:
		print("  nothing read for %r" % name)
		return
	print("\n  %s is wearing %d pieces:\n" % (name, len(rows)))
	for piece, component, augment in rows:
		extra = ", ".join(x for x in (component, augment) if x)
		print("     %-42s %s" % (piece[:42], extra))


def sheetOf(name, root=None):
	"""What the gear adds up to, in the vocabulary a model states.

	Not the character sheet, and the difference is large. Against lochlan's own
	numbers this lands for the resistances, the conversion and the added ranks
	and falls short everywhere else - physique 298 against 763, health 2108
	against 10178 - because three things contribute that are not read here: a
	mastery bar grants attributes, so do skills, and an item's prefix and suffix
	roll their values from a seed against a range the record only bounds.
	Armor comes out about four times over, which is a bug rather than a gap.

	Every worn piece, plus whatever is socketed into it, read through the same
	extraction itemgen uses to build itemData - so a bonus is spelled here the
	way a model spells it. Attributes and health start from the save's own base
	rather than from zero, because those are the two the character has before
	any of this.

	Returns (stats, missing): what could be worked out, and the names of what
	could not.
	"""
	from gddata import Database
	from itemgen import itemBonuses
	found = characters(root)
	if name not in found:
		return {}, []
	character = readCharacter(found[name]["path"])
	db = Database()

	import skillData                    # noqa: F401 - registers the skills
	from dataModel import Skill
	skillNames = set(Skill.skills)

	gear = {}
	for worn in character["equipped"]:
		for path in (worn["base"], worn["component"], worn["augment"]):
			record = db.read(path) if path else None
			if not record:
				continue
			for bonus, value in itemBonuses(record, db).items():
				if isinstance(value, list):
					continue                # a duration pair; the model reads
											# those off the skill, not the item
				gear[bonus] = gear.get(bonus, 0) + value

	stats = {}
	for attribute in ("physique", "cunning", "spirit"):
		stats[attribute] = round(character[attribute] + gear.get(attribute, 0))
	# Health and energy are the base times what the gear multiplies, and the
	# percentage is stated as well because a model needs both: the total to
	# price a point of health against, and the percentage to know what another
	# point of "+% Health" would multiply.
	for pool in ("health", "energy"):
		percent = gear.get(pool + " %", 0)
		stats[pool] = round((character[pool] + gear.get(pool, 0)) * (1 + percent / 100.0))
		if percent:
			stats[pool + " %"] = round(percent)
	for bonus, value in sorted(gear.items()):
		if bonus in stats or bonus in ("physique", "cunning", "spirit"):
			continue
		if bonus.endswith(" resist") or bonus.startswith("max "):
			stats[bonus] = round(value)
		elif bonus in ("armor", "armor %", "offense", "defense", "health/s",
					   "energy/s", "attack speed", "move speed", "cast speed"):
			stats[bonus] = round(value, 2)
		elif bonus.endswith(" skills") or bonus == "all skills" or bonus in skillNames:
			# "+2 Shaman skills" and "+2 Blade Arc" are both ranks your gear
			# adds, which is what the "+skills" field states - not stats of
			# their own, which is where they were landing.
			stats.setdefault("+skills", {})
			key = ("all" if bonus == "all skills"
				   else bonus[:-len(" skills")].title() if bonus.endswith(" skills")
				   else bonus)
			stats["+skills"][key] = stats["+skills"].get(key, 0) + round(value)
		else:
			stats[bonus] = round(value, 2)

	# Offensive and defensive ability have a base from level and attributes that
	# the save does not carry and the records do not state, so only the gear's
	# share of them is known.
	missing = [n for n in ("offense", "defense") if n in stats]
	return stats, missing


def showSheet(name, root=None):
	"""Print the sheet the gear implies, as a model would state it."""
	stats, partial = sheetOf(name, root)
	if not stats:
		print("  nothing read for %r" % name)
		return
	print("\n  %s, from the save:\n" % name)
	for key in sorted(stats):
		value = stats[key]
		if isinstance(value, dict):
			print('     "%s": %s,' % (key, "{" + ", ".join(
				'"%s": %d' % kv for kv in sorted(value.items())) + "}"))
		else:
			print('     "%s": %s,' % (key, value))
	print("\n  This is what the gear gives, not the character sheet. Against\n"
		  "  lochlan's own numbers it lands for the resistances, the conversion\n"
		  "  and the added ranks, and falls short everywhere else - physique 298\n"
		  "  against 763, health 2108 against 10178 - because a mastery bar and\n"
		  "  a skill both grant attributes and an item's prefix and suffix roll\n"
		  "  from a seed, and none of the three is read. Armor comes out about\n"
		  "  four times over, which is a bug rather than a gap.\n\n"
		  "  So: take the resistances, the conversions and \"+skills\" from here.\n"
		  "  %s and the rest still come off the sheet."
		  % " and ".join(partial or ["Nothing"]).capitalize())


def showSkills(name, root=None):
	"""Print one character's skills as a rotation would state them."""
	rows = skillsOf(name, root)
	if not rows:
		print("  nothing read for %r" % name)
		return
	print("\n  %s - %d skills with points in them:\n" % (name, len(rows)))
	for label, level in rows:
		print('     ("%s", %d),' % (label, level))
	print("\n  Points spent, not the rank the skill screen shows. Gear on top of\n"
		  "  these is what \"+skills\" in a model states.")


def _num(value):
	return "-" if value is None else "%g" % round(value)


def _modelStat(name, key):
	"""What the model file states for one number, if there is a model file.

	"level" is a stats key and "devotionPoints" a bare assignment, so both
	spellings are tried rather than two functions written.
	"""
	path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
						name.lower(), name.lower() + ".py")
	if not os.path.exists(path):
		return None
	import re
	text = open(path, encoding="utf-8").read()
	match = (re.search(r'"%s"\s*:\s*(\d+)' % key, text)
			 or re.search(r'^%s\s*=\s*(\d+)' % key, text, re.M))
	return int(match.group(1)) if match else None


if __name__ == "__main__":
	import sys
	if len(sys.argv) > 2 and sys.argv[2] == "gear":
		showGear(sys.argv[1])
	elif len(sys.argv) > 2 and sys.argv[2] == "stats":
		showSheet(sys.argv[1])
	elif len(sys.argv) > 1:
		showSkills(sys.argv[1])
	else:
		show()
