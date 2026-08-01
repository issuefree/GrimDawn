"""Minimal reader for Grim Dawn .arz database archives.

Layout:
  header (24 bytes): u16 unknown, u16 version, u32 recTableStart, u32 recTableSize,
                     u32 recTableEntries, u32 strTableStart, u32 strTableSize
  record data:       raw deflate blobs, offsets relative to byte 24
  record table:      per entry -> u32 nameIdx, u32 typeLen + type bytes,
                     u32 offset, u32 compressedSize, u32 decompressedSize,
                     u32 unknown, u64 filetime
  string table:      u32 count, then (u32 len + bytes) * count

Each decompressed record is a stream of variables:
  u16 type (0=int 1=float 2=string 3=bool), u16 count, u32 nameIdx, count*u32 values
"""
import struct
import zlib


def lz4Decompress(src, expected):
    """LZ4 block format, pure Python.

    ARZ v3 switched from deflate to LZ4. Implemented here rather than pulling in
    the lz4 package so the extractor has no dependencies beyond the stdlib.
    Sequence: token byte (hi nibble = literal count, lo nibble = match count),
    literals, 2-byte little-endian match offset, then a back-reference copy.
    Lengths of 15 continue into extra bytes until one is not 255.
    """
    out = bytearray()
    pos = 0
    end = len(src)
    while pos < end:
        token = src[pos]
        pos += 1
        litLen = token >> 4
        if litLen == 15:
            while True:
                extra = src[pos]
                pos += 1
                litLen += extra
                if extra != 255:
                    break
        out += src[pos:pos + litLen]
        pos += litLen
        if pos >= end:
            break
        offset = src[pos] | (src[pos + 1] << 8)
        pos += 2
        matchLen = (token & 0x0F) + 4
        if (token & 0x0F) == 15:
            while True:
                extra = src[pos]
                pos += 1
                matchLen += extra
                if extra != 255:
                    break
        start = len(out) - offset
        if start < 0:
            raise ValueError("bad LZ4 match offset")
        for i in range(matchLen):      # may overlap, so copy byte by byte
            out.append(out[start + i])
    if expected is not None and len(out) != expected:
        raise ValueError("LZ4 size mismatch: got %d, expected %d" % (len(out), expected))
    return bytes(out)


class Arz:
    def __init__(self, path):
        with open(path, "rb") as handle:
            self.blob = handle.read()
        (unknown, version, recStart, recSize, recCount,
         strStart, strSize) = struct.unpack_from("<HHIIIII", self.blob, 0)
        self.version = version
        self.strings = self._readStrings(strStart)
        self.records = self._readRecordTable(recStart, recCount)

    def _readStrings(self, start):
        count, = struct.unpack_from("<I", self.blob, start)
        pos = start + 4
        out = []
        for _ in range(count):
            length, = struct.unpack_from("<I", self.blob, pos)
            pos += 4
            out.append(self.blob[pos:pos + length].decode("latin-1"))
            pos += length
        return out

    def _readRecordTable(self, start, count):
        pos = start
        records = {}
        for _ in range(count):
            nameIdx, = struct.unpack_from("<I", self.blob, pos); pos += 4
            typeLen, = struct.unpack_from("<I", self.blob, pos); pos += 4
            recType = self.blob[pos:pos + typeLen].decode("latin-1"); pos += typeLen
            offset, csize, dsize = struct.unpack_from("<III", self.blob, pos); pos += 12
            pos += 8  # filetime
            records[self.strings[nameIdx]] = (recType, offset, csize, dsize)
        return records

    def read(self, name):
        """Return {field: value} for one record path."""
        recType, offset, csize, dsize = self.records[name]
        chunk = self.blob[24 + offset: 24 + offset + csize]
        if self.version >= 3:
            raw = lz4Decompress(chunk, dsize)
        else:
            raw = zlib.decompress(chunk)
        fields = {}
        pos = 0
        while pos < len(raw):
            vtype, count, nameIdx = struct.unpack_from("<HHI", raw, pos)
            pos += 8
            values = struct.unpack_from("<%dI" % count, raw, pos)
            pos += 4 * count
            if vtype == 1:      # float
                values = struct.unpack_from("<%df" % count, raw, pos - 4 * count)
            elif vtype == 2:    # string
                values = tuple(self.strings[v] for v in values)
            elif vtype == 3:    # bool
                values = tuple(bool(v) for v in values)
            key = self.strings[nameIdx]
            fields[key] = values[0] if count == 1 else list(values)
        fields["__type__"] = recType
        return fields

    def find(self, *fragments):
        """Record paths containing every fragment (case-insensitive)."""
        frags = [f.lower() for f in fragments]
        return sorted(n for n in self.records
                      if all(f in n.lower() for f in frags))
