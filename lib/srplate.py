"""Lay rendered Style R frames (renders/<shot>/f_####.png) into a flat2d.Video shot: plate(rdir, name) -> fn(g, c).
The nearest rendered frame at or before the current one is shown, so animatics rendered every Nth frame play as holds."""
from pathlib import Path
from flat2d import FPS, W, H

_cache = {}


def plate(rdir, name, fallback="#14213D"):
    rdir = Path(rdir)
    def fn(g, c):
        import cairocffi as cairo
        from PIL import Image
        files = _cache.get(name)
        if files is None:
            files = sorted(list((rdir / name).glob("f_*.png")) + list((rdir / name).glob("f_*.jpg"))); _cache[name] = files
        if not files:
            g.fill_all(fallback); g.text(name, W / 2, H / 2, 70, "#FFFFFF"); return
        fr = int(c.t * FPS)
        nums = [int(f.stem[2:]) for f in files]
        k = max([i for i, n in enumerate(nums) if n <= fr] or [0])
        key = (name, nums[k])
        if key not in _cache:
            im = Image.open(files[k]).convert("RGB").resize((W, H), Image.LANCZOS).convert("RGBA")
            r, g_, b, a = im.split(); im = Image.merge("RGBA", (b, g_, r, a))
            surf = cairo.ImageSurface.create_for_data(bytearray(im.tobytes()), cairo.FORMAT_ARGB32, W, H, W * 4)
            for kk in [x for x in _cache if isinstance(x, tuple) and x[0] == name and x != key]:
                del _cache[kk]
            _cache[key] = surf
        cc = g.c; cc.save(); cc.identity_matrix(); cc.set_source_surface(_cache[key], 0, 0); cc.paint(); cc.restore()
    return fn
