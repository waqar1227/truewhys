"""Helpers for standalone Short plans (episodes/A-<NNN>-<slug>/plan.py), vertical 1080x1920, Style T.
A plan.py imports this, declares shots with S(...) (one or more per script line, `part` splits a line),
then calls finish(EP, title). Cameras are authored for 9:16 directly (no re-aim): lens ~22-35.
The last shot is the Wy end card (outro line O1: "Follow for more true whys.").
Durations come from timing.json (lib/voice.py Kokoro draft or lib/voice_gemini.py final).
"""
import json, copy
from pathlib import Path

SHOTS = []
GAP = 0.22          # Shorts are tight: small gap between lines
END_DUR = 2.4


def M(pos, tgt, lens):
    return {"pos": list(pos), "tgt": list(tgt), "lens": lens}


def push(m, amt=0.12, dz=0.0, lens_mult=1.0):
    p, t = m["pos"], m["tgt"]
    b = {"pos": [p[i] + (t[i] - p[i]) * amt + (dz if i == 2 else 0) for i in range(3)], "tgt": list(t), "lens": m["lens"] * lens_mult}
    return {"from": copy.deepcopy(m), "to": b, "ease": "inout"}


def pull(m, amt=0.12):
    c = push(m, amt)
    return {"from": c["to"], "to": c["from"], "ease": "inout"}


def pan(m, dx=1.0, dy=0.0, dz=0.0):
    b = {"pos": [m["pos"][0] + dx, m["pos"][1] + dy, m["pos"][2] + dz], "tgt": [m["tgt"][0] + dx, m["tgt"][1] + dy, m["tgt"][2] + dz], "lens": m["lens"]}
    return {"from": copy.deepcopy(m), "to": b, "ease": "inout"}


def crane(m, dz=1.0, dtz=0.0):
    b = copy.deepcopy(m); b["pos"][2] += dz; b["tgt"][2] += dtz
    return {"from": copy.deepcopy(m), "to": b, "ease": "inout"}


def shake(m, amt=0.08, amp=0.03):
    c = push(m, amt); c["shake"] = amp
    return c


def A(c, at, h=1.5, face="R", expr="neutral", arms="down", **kw):
    d = dict(c=c, at=list(at), h=h, face=face, expr=expr, arms=arms)
    d.update(kw)
    return d


def S(line, kind="3d", set=None, cam=None, chars=(), part=None, **kw):
    st, var = (set.split(":") + ["day"])[:2] if set else (None, None)
    sh = dict(line=line, kind=kind, set=st, variant=var, cam=cam, chars=list(chars), part=part)
    sh.update(kw)
    SHOTS.append(sh)


def finish(ep, title, short_id=None):
    ep = Path(ep)
    T = {t["id"]: t for t in json.loads((ep / "timing.json").read_text())}
    out, t, k, prev = [], 0.0, 0, None
    sid = short_id or ep.name[:5]
    for sh in SHOTS:
        L = T[sh["line"]]
        p0, p1 = sh["part"] or (0, 1)
        gap = GAP + (0.18 if L["text"].rstrip().endswith(("?", "...")) else 0)
        full = L["dur"] + gap
        if sh["line"] != prev:
            line_start = t; prev = sh["line"]
        s0, s1 = line_start + full * p0, line_start + full * p1
        if k == 0:  # hook: starts at 0, words begin at 0.12 s
            line_start = 0.0
        out.append(dict(sh, id=f"{sid}_{k:02d}", start=round(s0, 3), dur=round(s1 - s0, 3), chapter=0, line_start=round(line_start + (0.12 if k == 0 else 0), 3)))
        if p1 >= 0.999:
            t = line_start + full
        k += 1
    o = T["O1"]
    out.append(dict(id=f"{sid}_END", kind="end", line="O1", start=round(t, 3), line_start=round(t + 0.12, 3), dur=max(END_DUR, o["dur"] + 0.5),
                    chapter=None, chars=[], sfx=[[0, "ding", 0.5]], music=None, set=None))
    t += out[-1]["dur"]
    plan = dict(fps=30, resolution=[1080, 1920], style="T", episode=sid, short=sid, title=title, duration=round(t, 2), vertical=True, shots=out)
    (ep / "shots.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False))
    print(f"{sid}: {len(out)} shots, {t:.1f} s")
    return plan
