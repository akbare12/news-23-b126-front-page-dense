"""news-23 b126 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
Verifies the PNG header itself (signature, IHDR 1024x1024, CRCs, IEND, size bounds).
"""
import hashlib
import os
import struct
import sys
import zlib

SRC_NAME = "entry.png"
DST_NAME = "entry.png"  # output filename (kept separate: SRC_NAME may be an
# absolute test path, but the output is always a plain entry.png)
MIN_BYTES = 10_000
MAX_BYTES = 1_048_576


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def check_png(data):
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")
    # Chunk layout: signature is 8 bytes, so the first chunk header starts at
    # offset 8: 4-byte length, 4-byte type, 13-byte IHDR data, 4-byte CRC.
    # The next chunk therefore starts at offset 8 + 8 + 13 + 4 = 33.
    # (IHDR data itself spans bytes 16..29, CRC at 29..33.)
    if len(data) < 33:
        fail("file too short for IHDR")
    (length,) = struct.unpack(">I", data[8:12])
    if data[12:16] != b"IHDR" or length != 13:
        fail("first chunk must be a 13-byte IHDR")
    (w, h, depth, ctype, comp, filt, inter) = struct.unpack(">IIBBBBB", data[16:29])
    if (w, h) != (1024, 1024):
        fail(f"expected 1024x1024, got {w}x{h}")
    if depth != 8 or ctype not in (2, 6):
        fail(f"unexpected bit depth {depth} / colour type {ctype}")
    if comp != 0 or filt != 0 or inter != 0:
        fail("unexpected compression/filter/interlace method")
    if zlib.crc32(data[12:29]) & 0xFFFFFFFF != struct.unpack(">I", data[29:33])[0]:
        fail("bad IHDR CRC")
    # Walk the remaining chunks, checking CRCs; require a non-empty IDAT
    # payload and a final 0-byte IEND with nothing after it.
    pos = 33
    idat_total = 0
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated chunk header")
        (clen,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        end = pos + 8 + clen + 4
        if end > len(data):
            fail(f"truncated chunk {ctype!r}")
        crc_stored = struct.unpack(">I", data[pos + 8 + clen:end])[0]
        if zlib.crc32(data[pos + 4:pos + 8 + clen]) & 0xFFFFFFFF != crc_stored:
            fail(f"bad CRC in chunk {ctype!r}")
        if ctype == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                fail("IEND must be 0 bytes")
            if end != len(data):
                fail("trailing data after IEND")
            seen_iend = True
            break
        pos = end
    if not seen_iend:
        fail("missing IEND chunk")
    if idat_total < 1000:
        fail("IDAT payload too small")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    if os.path.isfile(out_dir_abs):
        fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    if out_dir_abs == here or out_dir_abs.startswith(here + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must be outside the repo")
    dst = os.path.join(out_dir_abs, DST_NAME)
    if os.path.abspath(dst) == os.path.abspath(src):
        fail("output would overwrite the source image")
    try:
        with open(src, "rb") as f:
            data = f.read()
    except OSError as e:
        fail(f"cannot read {src}: {e}")
    if len(data) < MIN_BYTES:
        fail(f"entry.png too small: {len(data)} bytes")
    if len(data) > MAX_BYTES:
        fail(f"entry.png too large: {len(data)} bytes")
    check_png(data)
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        fail("output differs from source after copy")
    print(f"wrote {dst} ({len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()})")


if __name__ == "__main__":
    main()
