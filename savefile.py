"""Read what the game's own save files say about your characters.

A player.gdc is obfuscated rather than encrypted: the first word is a seed,
XORed with 0x55555555, and from it a 256-entry table is built by rotating right
one bit and multiplying by 39916801. Every value read is XORed with a running
key, and the key is then advanced by XORing in table[b] for each *ciphertext*
byte consumed. Nothing is secret; it just cannot be read out of order, because
the key depends on everything read before it.

What works here is the header, which is every character's name, mastery
combination and level. What does not is the body - see NOTES.md. The header is
worth having on its own: it is the one place a level cannot go stale, and the
class tag says which masteries a build is made of, which is the first thing you
need before naming its main attack.
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
	"""name, masteries and level, or None if this is not a save we understand."""
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
	return {"name": name, "level": level, "hardcore": bool(hardcore),
			"classTag": tag, "masteries": masteriesOf(tag)}


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
	print("\n  %-12s %5s  %-28s %s" % ("character", "level", "masteries", "model says"))
	for name in sorted(found):
		header = found[name]
		stated = _modelLevel(name)
		note = "-" if stated is None else ("%d" % stated)
		if stated is not None and stated != header["level"]:
			note += "   <- stale"
		print("  %-12s %5d  %-28s %s"
			  % (name, header["level"], ", ".join(header["masteries"]) or "?", note))


def _modelLevel(name):
	"""The level the model file states, if there is a model file."""
	path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
						name.lower(), name.lower() + ".py")
	if not os.path.exists(path):
		return None
	import re
	match = re.search(r'"level"\s*:\s*(\d+)', open(path, encoding="utf-8").read())
	return int(match.group(1)) if match else None


if __name__ == "__main__":
	show()
