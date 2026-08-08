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

What is not done is the inside of most blocks. A block cannot be skipped, because
the key advances on every ciphertext byte consumed, and it cannot be walked
blindly either: a block that contains items contains their lengths, and a length
is read *without* advancing the key, so consuming those four bytes as data puts
the key out. Every block has to be parsed field by field or not at all. See
NOTES.md for what that leaves.
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

	Stops at the first block it cannot walk. A block's own bytes can be consumed
	without understanding them - the key advances the same either way - but not
	one that contains a nested length, because a length is read without
	advancing the key and consuming those four bytes as data breaks it. On these
	saves that is the third block, which is where the items live.
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
	show()
