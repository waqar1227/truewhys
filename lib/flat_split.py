"""Split long Short shots into 1.5-2.5 s cuts with alternating framings; the story clock and SFX timing are kept (from B-004 shorts, 20 Nov 2026).
from flat_split import split_long; V.build(); split_long(V)"""
import math
from flat2d import FPS, push, clamp


def _cont(fn, sh0):
    """Run a scene with the clock of the original (unsplit) shot, so its animations continue across the cut."""
    def f(g, c):
        off = c.sh["start"] - sh0["start"]
        c.sh = dict(c.sh, start=sh0["start"]); c.t += off; c.T = sh0["dur"]; c.u = clamp(c.t / c.T) if c.T > 0 else 0
        fn(g, c)
    return f


def split_long(V, maxd=2.5, keep_cam=False):
    """keep_cam=True (A-029+): the extra cuts keep the shot's own camera and only re-frame it (x1.14 / x1.07 zoom)."""
    out = []
    for sh in V.shots:
        if sh["kind"] == "end" or sh["dur"] <= maxd + 0.5:
            out.append(sh); continue
        n = math.ceil(sh["dur"] / maxd)
        edges = [round((sh["start"] + sh["dur"] * k / n) * FPS) / FPS for k in range(n + 1)]
        for k in range(n):
            part = dict(sh, start=edges[k], dur=edges[k + 1] - edges[k])
            part["sfx"] = []
            for e in sh["sfx"]:                      # each sound effect goes to the piece that contains its moment
                off, nm = e[0], e[1]
                t_abs = (V.word_t(sh["line"], *((off.split("#")[0], int(off.split("#")[1])) if "#" in off else (off, 0)))
                         if isinstance(off, str) else sh["start"] + off)
                if edges[k] <= t_abs < edges[k + 1] or (k == n - 1 and t_abs >= edges[-1]):
                    part["sfx"].append(e if isinstance(off, str) else (t_abs - edges[k],) + tuple(e[1:]))
            if k:
                part["fn"] = _cont(sh["fn"], sh)
                part["tr"] = "cut"
                part["music"] = None
                if keep_cam:
                    zk = 1.14 if k % 2 else 1.07
                    part["cam"] = (lambda cam0, zk: (lambda c: (lambda r: (r[0], r[1], r[2] * zk, r[3]))(cam0(c))))(sh["cam"], zk)
                else:
                    part["cam"] = push(1.16, 1.2, (540, 1050)) if k % 2 else push(0.96, 1.0, (540, 960))
            out.append(part)
    # keep every SFX on its own word: SFX of the first part with word anchors are fine; numeric offsets beyond the part move along
    for i, sh in enumerate(out):
        sh["id"] = f"{V.sid}_{i:02d}"
    V.shots = out
