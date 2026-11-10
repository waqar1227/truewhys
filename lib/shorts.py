"""Build vertical Short plans (1080x1920) cut from a long video, re-composed (not cropped).

python lib/shorts.py episodes/<ep>            -> episodes/<ep>/shorts/<CID>/shots.json for every Short,
                                                 plus episodes/<ep>/shorts/all_shots.json (one plan for the Kaggle render)
Each Short = hook shot (new narration line) + the long video's shots for the chosen lines (re-timed back to back)
+ a 2.6 s Wy end card with the outro line. Every 3D camera is re-aimed for 9:16: same position and tilt,
longer lens (LENS_K), turned towards the main actor so the subject fills the tall frame.
"""
import sys, os, json, math, copy
from pathlib import Path
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import camera

LENS_K = 1.75  # 9:16 frame then shows ~57% of the landscape width and ~1.0x its height
VW, VH = 1080, 1920
SUBJ_Y = 0.43
END_DUR = 2.6
SUBJ_H = 0.36   # main subject height as a share of the vertical frame
ZOOM_MAX, ZOOM_MIN = 1.6, 0.7
ANIMALS = {"pig", "bull", "rat", "weevil", "rooster", "hen", "dog", "cat", "horse", "mouse", "locust", "toad", "sheep", "goat", "cow", "polar_bear", "seal", "fish"}  # wider than tall


def est_words(text):
    return len(text.split()) / 2.7 + 0.35


def fake_timing(lid, text):
    """Even word timing, used only until the real hook voice exists (previews)."""
    ws = text.split(); t = 0.0; out = []
    for w in ws:
        d = 0.18 + 0.055 * len(w)
        out.append(dict(w=w, s=round(t, 3), e=round(t + d, 3))); t += d + 0.06
    return dict(id=lid, text=text, dur=round(t + 0.2, 3), words=out, estimated=True)


def reaim(cam, chars, W=1920, H=1080):
    """Turn the camera (both keys) towards the main actor(s) and lengthen the lens for 9:16."""
    cam = copy.deepcopy(cam)
    if not chars:
        for k in ("from", "to"):
            if cam.get(k):
                cam[k]["lens"] = round(cam[k]["lens"] * LENS_K, 2)
        return cam
    pos, tgt, lens = camera.cam_at(cam, 0.5)
    best = []
    for a in chars:
        x, y, z, ppm = camera.project(a["at"], pos, tgt, lens, W, H)
        if z < 0.3 or x < -0.1 * W or x > 1.1 * W:
            continue
        w = a.get("h", 1.4) * ppm * (2.2 if a.get("talk") else 1.0) * (1.4 if a.get("main") else 1.0) \
            * (1.6 if (a.get("hold_r") or a.get("hold") or a.get("gest")) else 1.0)  # the one doing the action
        best.append((w, x, a))
    if not best:
        best = [(1, W / 2, chars[0])]
    best.sort(key=lambda b: -b[0])
    px = best[0][1]
    half = W * 0.5 / LENS_K * 1.15  # neighbours this close join the group; the zoom below then fits the group
    group = [b for b in best if abs(b[1] - px) < half]
    wsum = sum(b[0] for b in group)
    aim = np.array([sum(b[0] * np.array(b[2]["at"][:2], float) for b in group) / wsum])[0]
    # body centre of the group: we tilt so it sits at SUBJ_Y of the frame height (captions live lower, at 0.68)
    zc = sum(b[0] * (b[2]["at"][2] + b[2].get("h", 1.4) * 0.5) for b in group) / wsum
    # adaptive zoom (from the first key): the main subject fills ~36% of the frame height, and the group fits the width
    k = 1.0
    c0 = cam.get("from")
    if c0:
        p = np.array(c0["pos"], float); t = np.array(c0["tgt"], float)
        hdir = aim - p[:2]
        if np.linalg.norm(hdir) > 0.3:
            R0 = float(np.linalg.norm(t - p)); pitch0 = math.asin(max(-1, min(1, (t - p)[2] / R0)))
            hdir = hdir / np.linalg.norm(hdir)
            t2 = p + R0 * np.array([hdir[0] * math.cos(pitch0), hdir[1] * math.cos(pitch0), math.sin(pitch0)])
            lv = c0["lens"] * LENS_K
            pr = [(camera.project(b[2]["at"], p, t2, lv, VW, VH), b[2].get("h", 1.4), b[2].get("c", "")) for b in group]
            pr = [(x, ppm, h, 0.8 if c.rstrip("0123456789") in ANIMALS else 0.38) for (x, y, z, ppm), h, c in pr if z > 0.3]
            if pr:
                frac = max(ppm * h for x, ppm, h, wf in pr) / VH
                spread = max(x + ppm * h * wf for x, ppm, h, wf in pr) - min(x - ppm * h * wf for x, ppm, h, wf in pr)
                k = min(ZOOM_MAX, SUBJ_H / frac) if frac < SUBJ_H - 0.02 else 1.0
                k = max(ZOOM_MIN, min(k, 0.86 * VW / max(spread, 1)))
                if any(wf > 0.5 for x, ppm, h, wf in pr):  # animals are drawn behind their anchor: keep room for the body
                    k = min(k, 1.2)
    for key in ("from", "to"):
        c = cam.get(key)
        if not c:
            continue
        p = np.array(c["pos"], float); t = np.array(c["tgt"], float)
        d = t - p; R = float(np.linalg.norm(d))
        pitch = math.asin(max(-1, min(1, d[2] / R)))
        h = aim - p[:2]
        hn = np.linalg.norm(h)
        if hn < 0.3:
            continue
        h /= hn
        lens_v = c["lens"] * LENS_K * k
        fpx = lens_v / camera.SENSOR * VW
        dist = float(np.linalg.norm(aim - p[:2]))
        elev = math.atan2(zc - p[2], dist)
        want = elev - math.atan((0.5 - SUBJ_Y) * VH / fpx)
        pitch = max(pitch - 0.35, min(pitch + 0.35, want))  # stay close to the director's original tilt
        nt = p + R * np.array([h[0] * math.cos(pitch), h[1] * math.cos(pitch), math.sin(pitch)])
        c["tgt"] = [round(float(v), 3) for v in nt]
        c["lens"] = round(lens_v, 2)
    return cam


def pick_hook(sel, want=None):
    """The hook opens on the strongest image: the given shot, else the 3D shot with the biggest subject."""
    d3 = [s for s in sel if s["kind"] == "3d"]
    if want:
        for s in d3:
            if s["id"] == want:
                return s
    def size(s):
        pos, tgt, lens = camera.cam_at(s["cam"], 0.5)
        best = 0
        for a in s.get("chars", []):
            x, y, z, ppm = camera.project(a["at"], pos, tgt, lens, 1920, 1080)
            if z > 0.3 and 0.2 * 1920 < x < 0.8 * 1920:
                best = max(best, a.get("h", 1.4) * ppm)
        return best * (0.4 if s.get("set") == "study" else 1.0)  # the story's own subject beats Wy at his desk
    return max(d3, key=size)


def build(ep):
    ep = Path(ep)
    plan = json.loads((ep / "shots.json").read_text())
    cfg = json.loads((ep / "shorts.json").read_text())
    timing = {t["id"]: t for t in json.loads((ep / "timing.json").read_text())}
    if (ep / "timing_hooks.json").exists():  # real hook/outro voice (lib/voice_gemini.py <ep> shorts)
        timing.update({t["id"]: t for t in json.loads((ep / "timing_hooks.json").read_text())})
    extra = {}
    for c in cfg["shorts"]:
        for ln in (c["hook"], cfg["outro"]):
            wav = ep / f"audio/lines/{ln['id']}.wav"
            if ln["id"] not in timing:
                extra[ln["id"]] = fake_timing(ln["id"], ln["text"])
    out_all = []
    root = ep / "shorts"; root.mkdir(exist_ok=True)
    for c in cfg["shorts"]:
        cid = c["id"]
        sel = [s for s in plan["shots"] if s.get("line") in set(c["lines"])]
        sel.sort(key=lambda s: s["start"])
        shots = []
        t = 0.0
        # ---- hook: the first 3D shot of the Short, slow push-in, new line
        first3d = pick_hook(sel, c.get("hook_shot"))
        hk = c["hook"]
        ht = timing.get(hk["id"]) or extra[hk["id"]]
        h = copy.deepcopy(first3d)
        cm = h["cam"]
        a = cm["from"]; p = np.array(a["pos"]); g = np.array(a["tgt"])
        cm["to"] = dict(pos=[round(float(v), 3) for v in p + (g - p) * 0.10], tgt=a["tgt"], lens=a["lens"]); cm["ease"] = "inout"
        cm.pop("orbit", None)
        h.update(id=f"{cid}_H", line=hk["id"], start=0.0, line_start=0.15, dur=round(ht["dur"] + 0.45, 3), music=first3d.get("music") or "mystery",
                 sfx=[[0, "whoosh_soft", 0.5]] + [x for x in first3d.get("sfx", []) if x[1] in ("crowd_murmur", "wind", "birds", "fire", "insects")])
        h.pop("pop", None); h.pop("tag", None)
        if c.get("hook_pop"):  # big hook words on screen from ~0.1 s (format rule: hook visible by 0.5 s)
            h["pop"] = [[0.02, c["hook_pop"], 1.45]]
        for a in h.get("chars", []):  # optional stronger face for the opening frame
            if a.get("c") in c.get("hook_expr", {}):
                a["expr"] = c["hook_expr"][a["c"]]
        shots.append(h); t = h["dur"]
        # ---- body: line blocks back to back
        lines_in = []
        for s in sel:
            if s["line"] not in lines_in:
                lines_in.append(s["line"])
        for ln in lines_in:
            blk = [s for s in sel if s["line"] == ln]
            ls = min(s["start"] for s in blk)
            le = max(s["start"] + s["dur"] for s in blk)
            off = t - ls
            for s in blk:
                n = copy.deepcopy(s)
                n["id"] = f"{cid}_{s['id']}"
                n["start"] = round(s["start"] + off, 3)
                n["line_start"] = round(s["line_start"] + off, 3)
                n["src"] = s["id"]
                if n.get("tag") and n["tag"].upper().startswith("IDEA"):  # "IDEA 2: MONEY" -> "MONEY" (no numbering out of context)
                    n["tag"] = n["tag"].split(":", 1)[-1].strip()
                shots.append(n)
            t = round(le + off, 3)
        shots[1]["music"] = shots[1].get("music") or h["music"]
        # ---- end card
        o = cfg["outro"]
        shots.append(dict(id=f"{cid}_END", kind="end", line=o["id"], start=t, line_start=round(t + 0.15, 3), dur=END_DUR, chapter=None,
                          sfx=[[0, "ding", 0.5]], music=None))
        t += END_DUR
        for s in shots:
            if s["kind"] == "3d":
                s["cam"] = reaim(s["cam"], s.get("chars", []))
        p = dict(fps=plan.get("fps", 30), resolution=[VW, VH], style=plan.get("style"), episode=plan.get("episode"), short=cid,
                 title=c["title"], duration=round(t, 3), vertical=True, shots=shots)
        (root / cid).mkdir(exist_ok=True)
        (root / cid / "shots.json").write_text(json.dumps(p, indent=1))
        out_all += [s for s in shots if s["kind"] == "3d"]
        print(f"{cid}: {t:5.1f}s  {len(shots)} shots  {c['title']}")
    tt = dict(timing); tt.update(extra)
    (root / "timing.json").write_text(json.dumps(list(tt.values()), indent=1))
    (root / "all_shots.json").write_text(json.dumps(dict(fps=plan.get("fps", 30), duration=0, shots=out_all), indent=1))
    print("estimated (no voice yet):", sorted(extra))


if __name__ == "__main__":
    build(sys.argv[1])
