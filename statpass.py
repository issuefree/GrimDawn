"""Remove the stats the save agrees with, annotate the ones it does not.

A stat within 5% of what savefile.sheetOf derives is deleted: the loader fills
it in from the save, so stating it is copying out a number the code already
has. A stat further off keeps its stated value and gains a comment saying what
was derived, because that gap is worth chasing rather than hiding.
"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import models, savefile
from constants import damages

DRY = "--write" not in sys.argv
PAIR = re.compile(r'"([^"]+)"\s*:\s*(-?[\d.]+)\s*,?')
# A note this script wrote last time, so re-running refreshes it rather than
# appending a second copy. Two shapes, stripped in this order: one appended to a
# comment that was already there, then one that is the whole comment. The line
# is split on "#", so a note of its own arrives with no leading space at all -
# which is what the first attempt at this missed.
APPENDED = re.compile(r"\s{2,}derived\b.*$")
WHOLE = re.compile(r"^\s*#\s*derived\b.*$")


def statsBlock(source):
	"""(start, end) of the stats = { ... } literal, so weights are left alone."""
	match = re.search(r'^stats\s*=\s*\{', source, re.M)
	i, depth = match.end(), 1
	while depth:
		if source[i] == "{":
			depth += 1
		elif source[i] == "}":
			depth -= 1
		i += 1
	return match.end(), i - 1


def compare(name, stated):
	derived, _ = savefile.sheetOf(name)
	# The loader takes the devotions a character already has off anything the
	# model states, because the sheet was read with them on. Compare the same
	# way or every stat a constellation touches looks further out than it is.
	models.Model.removeCurrentDevotion(name, stated)
	close, off = {}, {}
	for key, value in stated.items():
		got = derived.get(key)
		if got is None or not isinstance(value, (int, float)) or not value:
			continue
		if not isinstance(got, (int, float)):
			continue
		# The sheet states damage with the multiplier already on it and the
		# save adds up flat, so they only compare once the percentage is off.
		mine = value
		if key in damages:
			mine = value / (1.0 + float(stated.get(key + " %", 0) or 0) / 100.0)
		percent = 100.0 * (got - mine) / abs(mine)
		(close if abs(percent) <= 5 else off)[key] = (got, percent)
	return close, off


def rewrite(name):
	folder = name.lower()
	path = "%s/%s.py" % (folder, folder)
	source = io.open(path, encoding="utf-8").read()

	namespace = dict(vars(models))
	exec(source, namespace)
	close, off = compare(name, namespace["stats"])
	if not close and not off:
		return None

	start, end = statsBlock(source)
	head, body, tail = source[:start], source[start:end], source[end:]

	dropped, noted, lines = [], [], []
	for line in body.split("\n"):
		code = line.split("#", 1)[0]
		comment = WHOLE.sub("", APPENDED.sub("", line[len(code):]))
		if comment.strip() in ("#", ""):
			comment = ""
		hits = list(PAIR.finditer(code))
		if not hits:
			lines.append(line)
			continue

		here, cut = [], False
		for hit in reversed(hits):                  # reversed: indices stay valid
			key = hit.group(1)
			if key in close:
				code = code[:hit.start()] + code[hit.end():]
				dropped.append("%s (derived %s)" % (key, models.fmt(close[key][0])))
				cut = True
			elif key in off:
				got, percent = off[key]
				here.append((key, models.fmt(got), percent))
				noted.append(key)
		if cut and code.strip():
			# Close up the hole a removed pair left, keeping the line's own
			# indent - two stats on a line leave a double space between the
			# survivors, or a stray one against the indent if the first went.
			indent = re.match(r"[\t ]*", line).group(0)
			code = indent + re.sub(r"[ \t]{2,}", " ", code[len(indent):].lstrip())
		if here:
			here.reverse()
			# The key is worth repeating only where the line carries more than
			# one, which is where "derived 202 -68%" would not say which.
			# One stat on the line needs no name; two do, even when only one
			# of them is off, or "derived 90 -70%" does not say which.
			label = (lambda k: k + " ") if len(hits) > 1 else (lambda k: "")
			note = "derived " + ", ".join("%s%s %+.0f%%" % (label(k), v, p)
										  for k, v, p in here)
			if comment.strip():
				comment += "  " + note
			else:
				code, comment = code.rstrip(), "  # " + note
		if not code.strip():
			if not comment.strip():
				continue                            # the line held nothing else
			code = re.match(r"\s*", line).group(0)
		elif not comment:
			code = code.rstrip()
		lines.append(code + comment)

	out = head + "\n".join(lines) + tail
	if not DRY:
		io.open(path, "w", encoding="utf-8", newline="\n").write(out)
	return dropped, noted


for name in sorted(savefile.characters()):
	if not os.path.exists("%s/%s.py" % (name.lower(), name.lower())):
		continue
	result = rewrite(name)
	if not result:
		continue
	dropped, noted = result
	print("  %-9s dropped %d, annotated %d" % (name, len(dropped), len(noted)))
	if dropped:
		print("            %s" % ", ".join(dropped))
print("\n%s" % ("DRY RUN - pass --write" if DRY else "written"))
