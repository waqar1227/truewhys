"""List or extract chosen entries of a remote stored/deflated zip using HTTP range requests (no full download)."""
import sys, struct, zlib, subprocess, os, json, re
URL = sys.argv[1]; SIZE = int(sys.argv[2]); mode = sys.argv[3]
def rng(a, b):
    return subprocess.run(["curl", "-s", "-m", "300", "-A", "Mozilla/5.0", "-r", f"{a}-{b}", URL], capture_output=True).stdout
tail = rng(SIZE - 70000, SIZE - 1)
i = tail.rfind(b"PK\x05\x06")
_, _, _, _, n, cdsize, cdoff, _ = struct.unpack("<IHHHHIIH", tail[i:i + 22])
cd = rng(cdoff, cdoff + cdsize - 1)
ents = []; p = 0
while p < len(cd) and cd[p:p + 4] == b"PK\x01\x02":
    meth = struct.unpack("<H", cd[p + 10:p + 12])[0]; csz, usz = struct.unpack("<II", cd[p + 20:p + 28])
    fl, el, cl = struct.unpack("<HHH", cd[p + 28:p + 34]); off = struct.unpack("<I", cd[p + 42:p + 46])[0]
    name = cd[p + 46:p + 46 + fl].decode("utf8", "replace"); ents.append((name, meth, csz, usz, off)); p += 46 + fl + el + cl
if mode == "ls":
    for e in ents: print(e[3], e[0])
else:
    pat = re.compile(sys.argv[4]); out = sys.argv[5]
    for name, meth, csz, usz, off in ents:
        if name.endswith("/") or not pat.search(name): continue
        h = rng(off, off + 29); fl, el = struct.unpack("<HH", h[26:30])
        data = rng(off + 30 + fl + el, off + 30 + fl + el + csz - 1) if csz else b""
        if meth == 8: data = zlib.decompress(data, -15)
        dst = os.path.join(out, name); os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, "wb").write(data)
        print(len(data), name)
