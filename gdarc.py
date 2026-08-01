"""Minimal reader for Grim Dawn .arc resource archives.

The .arz databases name things by tag - an item record says its name is
tagCompB018Name and nothing more. The strings those tags stand for live in
Text_EN.arc, so reading item and skill names means reading one of these.

Layout:
  header (28 bytes): 4s magic "ARC\\0", u32 version, u32 fileCount,
                     u32 chunkCount, u32 chunkTableSize, u32 stringTableSize,
                     u32 chunkTableOffset
  file data:         lz4 chunks, each listed in the chunk table
  chunk table:       per chunk -> u32 offset, u32 compressedSize, u32 size
  string table:      file names, concatenated, indexed by offset and length
  file table:        per file -> u32 type, u32 offset, u32 compressedSize,
                     u32 size, u32 hash, u64 filetime, u32 chunks,
                     u32 firstChunk, u32 nameLength, u32 nameOffset

A file is stored as one or more chunks; a chunk whose compressed size equals
its decompressed size is stored as-is rather than compressed.
"""
import struct

from gdarz import lz4Decompress

HEADER = struct.Struct("<4s6I")
CHUNK = struct.Struct("<III")
ENTRY = struct.Struct("<IIIIIQIIII")


class Arc:
    def __init__(self, path):
        with open(path, "rb") as handle:
            self.blob = handle.read()
        magic, version, fileCount, chunkCount, chunkTableSize, stringTableSize, chunkTableOffset = \
            HEADER.unpack_from(self.blob, 0)
        if magic != b"ARC\0":
            raise ValueError("%s is not an .arc archive" % path)
        self.version = version
        self.chunks = [CHUNK.unpack_from(self.blob, chunkTableOffset + i * CHUNK.size)
                       for i in range(chunkCount)]
        stringStart = chunkTableOffset + chunkTableSize
        strings = self.blob[stringStart:stringStart + stringTableSize]
        self.files = {}
        entryStart = stringStart + stringTableSize
        for i in range(fileCount):
            entry = ENTRY.unpack_from(self.blob, entryStart + i * ENTRY.size)
            nameLength, nameOffset = entry[8], entry[9]
            name = strings[nameOffset:nameOffset + nameLength].decode("latin-1")
            self.files[name] = entry

    def read(self, name):
        """Return one stored file's bytes."""
        entry = self.files[name]
        chunks, firstChunk = entry[6], entry[7]
        out = bytearray()
        for index in range(firstChunk, firstChunk + chunks):
            offset, compressed, size = self.chunks[index]
            raw = self.blob[offset:offset + compressed]
            out += raw if compressed == size else lz4Decompress(raw, size)
        return bytes(out)


def readTags(path, subjects=()):
    """{tag: text} from every tag file in one archive.

    subjects narrows it to the files worth decompressing - "items" pulls the
    item names rather than the megabyte of story text beside them. Each
    expansion names its own files, so the base game's tags_items.txt is
    tagsgdx1_items.txt in the first expansion and so on. Colour codes (^k and
    friends) are stripped; they are display markup, no part of a name.
    """
    arc = Arc(path)
    out = {}
    for name in arc.files:
        if not name.startswith("tags") or not name.endswith(".txt"):
            continue
        if subjects and not any(name.endswith("_%s.txt" % s) for s in subjects):
            continue
        for line in arc.read(name).decode("utf-8-sig", "replace").splitlines():
            tag, _, text = line.partition("=")
            if not _ or line.startswith("//"):
                continue
            while len(text) > 1 and text[0] == "^":
                text = text[2:]
            out[tag.strip()] = text.strip()
    return out
