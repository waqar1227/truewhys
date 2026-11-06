"""TrueWhys cast: original vector cutout puppets (SVG -> PNG via cairosvg).

Each character is drawn in layers so the compositor can animate them:
  body  (legs, torso, clothes)   pivot: feet (0,0)
  armL / armR                    pivot: shoulder, angle 0 = hanging down
  head  (face, hair, hat)        pivot: neck (0,0) = bottom of head
Units: 1 unit ~ 1 px at scale 1. A standard adult is ~560 units tall (feet to head top).
Design language (ours, see library/cast/cast.md): wide egg heads, big oval eyes with
highlights, eyebrows, rosy cheeks, bean bodies, thick ink outline.
"""
import io, math, functools
from PIL import Image
import cairosvg

INK = "#2A1C1E"
SW = 11  # outline width
EYE_W = "#FFFFFF"
CHEEK = "#F2918A"

HEAD = "M0 -274 C100 -274 152 -212 152 -140 C152 -60 88 0 0 0 C-88 0 -152 -60 -152 -140 C-152 -212 -100 -274 0 -274 Z"

# ---------------------------------------------------------------- characters
CHARS = {
    "wy":      dict(skin="#F4C6A0", hair="curl", hair_c="#5B3A29", top="#FF6B5B", collar="#FFF4E0",
                    legs="#24476B", shoes=INK, badge=True, hx=1.0),
    "judge":   dict(skin="#E9B48C", hair="judge_cap", hair_c="#1E1A24", top="#B3262E", collar="#FFF4E0",
                    robe=True, beard="#F2EEE6", fur="#FFF4E0", hx=1.08),
    "lawyer":  dict(skin="#D79C72", hair="lawyer_cap", hair_c="#1E1A24", top="#20243A", collar="#FFFFFF",
                    robe=True, bands=True, hair2="#3B2416", hx=0.96),
    "bishop":  dict(skin="#F0C9A8", hair="mitre", hair_c="#FFF4E0", top="#6E3A8C", collar="#FFC93C",
                    robe=True, trim="#FFC93C", hx=1.0),
    "crier":   dict(skin="#C98E66", hair="feather_cap", hair_c="#0F6B78", top="#2E6FA7", collar="#FFC93C",
                    legs="#5B3A29", shoes=INK, belt="#FFC93C", hx=1.0),
    "mother":  dict(skin="#F2C09A", hair="coif", hair_c="#FFF4E0", top="#3E8E5E", collar="#FFF4E0",
                    robe=True, apron="#FFF4E0", hx=0.98),
    "farmer":  dict(skin="#B97A55", hair="straw_hat", hair_c="#E8C46A", top="#8A5A3B", collar="#C9A27A",
                    legs="#4A3A2C", shoes="#3A2618", belt="#5B3A29", stubble=True, hx=1.04),
    "monk":    dict(skin="#E6B08A", hair="tonsure", hair_c="#6B4A32", top="#7A5236", collar="#7A5236",
                    robe=True, belt="#E8D5A8", hx=1.0),
    "magistrate": dict(skin="#DDA77E", hair="fur_hat", hair_c="#4A2F22", top="#1F5C8C", collar="#FFF4E0",
                    robe=True, fur="#7A5236", hx=1.06),
}
VILLAGER_TOPS = ["#3E8E5E", "#B3262E", "#2E6FA7", "#8A5A3B", "#C76A2B", "#6E3A8C", "#4F6D3A", "#9C4F67"]
VILLAGER_SKINS = ["#F2C09A", "#D79C72", "#B97A55", "#8D5A3C", "#E9B48C", "#C98E66"]
VILLAGER_HAIR = [("coif", "#FFF4E0"), ("hood", "#7A5236"), ("bowl", "#3B2416"), ("straw_hat", "#E8C46A"),
                 ("bald", None), ("bun", "#6B4A32"), ("hood", "#3E5A7A"), ("bowl", "#C98A3A")]


def villager(i):
    h, hc = VILLAGER_HAIR[i % len(VILLAGER_HAIR)]
    return dict(skin=VILLAGER_SKINS[(i * 5 + 1) % len(VILLAGER_SKINS)], hair=h, hair_c=hc or "#3B2416",
                top=VILLAGER_TOPS[(i * 3) % len(VILLAGER_TOPS)], collar="#FFF4E0",
                legs=["#4A3A2C", "#24476B", "#5B3A29"][i % 3], shoes=INK, robe=(i % 2 == 0),
                hx=0.94 + 0.04 * (i % 4))


def spec(cid):
    if cid.startswith("villager"):
        return villager(int(cid[8:] or 0))
    return CHARS[cid]


def _svg(body, vb):
    x0, y0, x1, y1 = vb
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1-x0} {y1-y0}" '
            f'width="{x1-x0}" height="{y1-y0}">'
            f'<g stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round">{body}</g></svg>')


def _png(svg, scale):
    data = cairosvg.svg2png(bytestring=svg.encode(), scale=scale)
    return Image.open(io.BytesIO(data)).convert("RGBA")


def shade(hexc, f):
    h = hexc.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    if f < 1:
        r, g, b = (int(c * f) for c in (r, g, b))
    else:
        r, g, b = (int(c + (255 - c) * (f - 1)) for c in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"

# ---------------------------------------------------------------- head parts

def eyes_svg(expr, eyes, look, skin):
    lx, ly = look
    out = []
    for side, cx in ((-1, -58), (1, 62)):
        cy = -146
        if eyes == "closed" or expr == "happy_closed":
            out.append(f'<path d="M{cx-34} {cy+4} Q{cx} {cy+30} {cx+34} {cy+4}" fill="none" stroke-width="10"/>')
            continue
        ry = 46 if expr != "surprised" else 52
        rx = 34 if expr != "surprised" else 37
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{EYE_W}" stroke-width="9"/>')
        pr = 20 if expr != "surprised" else 15
        px, py = cx + 9 * lx, cy + 10 * ly - 4
        out.append(f'<circle cx="{px}" cy="{py}" r="{pr}" fill="{INK}" stroke="none"/>')
        out.append(f'<circle cx="{px+7}" cy="{py-9}" r="7" fill="#FFFFFF" stroke="none"/>')
        out.append(f'<circle cx="{px-6}" cy="{py+8}" r="3" fill="#FFFFFF" stroke="none"/>')
        lid = None
        if eyes == "half" or expr in ("smug", "tired"):
            lid = cy - 6
        elif expr in ("angry",):
            lid = cy - 22
        if lid is not None:
            # upper lid: skin cap over the eye, with a lash line
            tilt = (-12 * side) if expr == "angry" else 0
            out.append(f'<path d="M{cx-rx-6} {lid - tilt} L{cx+rx+6} {lid + tilt} L{cx+rx+6} {cy-ry-8} '
                       f'L{cx-rx-6} {cy-ry-8} Z" fill="{skin}" stroke="none"/>')
            out.append(f'<path d="M{cx-rx+2} {lid - tilt*0.8} L{cx+rx-2} {lid + tilt*0.8}" stroke-width="9"/>')
            out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke-width="9"/>')
    return "".join(out)


def brows_svg(expr):
    # left brow (screen left) and right brow paths per expression
    B = {
        "neutral":   ("M-92 -206 Q-62 -228 -30 -214", "M32 -216 Q64 -232 94 -210"),
        "happy":     ("M-92 -214 Q-62 -238 -30 -222", "M32 -224 Q64 -240 94 -216"),
        "surprised": ("M-94 -226 Q-62 -254 -28 -236", "M30 -238 Q64 -258 96 -228"),
        "worried":   ("M-92 -206 Q-60 -214 -30 -232", "M32 -232 Q64 -214 94 -206"),
        "angry":     ("M-92 -222 Q-60 -214 -28 -196", "M30 -196 Q64 -214 94 -222"),
        "smug":      ("M-92 -206 Q-62 -222 -30 -212", "M32 -230 Q64 -250 94 -226"),
        "sad":       ("M-92 -204 Q-60 -210 -30 -228", "M32 -228 Q64 -210 94 -204"),
        "tired":     ("M-92 -204 Q-62 -214 -30 -208", "M32 -208 Q64 -214 94 -204"),
    }
    a, b = B.get(expr, B["neutral"])
    return f'<path d="{a}" fill="none" stroke-width="11"/><path d="{b}" fill="none" stroke-width="11"/>'


def mouth_svg(expr, mouth):
    """mouth: closed/small/open/wide (talking shapes) shaped by the expression."""
    dark, tongue = "#8A2734", "#E8707A"
    frown = expr in ("worried", "sad", "angry")
    if expr == "surprised" and mouth == "closed":
        mouth = "small"
    if mouth == "closed":
        if frown:
            return '<path d="M-26 -58 Q0 -76 26 -58" fill="none" stroke-width="10"/>'
        if expr == "smug":
            return '<path d="M-24 -66 Q6 -50 32 -74" fill="none" stroke-width="10"/>'
        return '<path d="M-30 -70 Q0 -46 30 -70" fill="none" stroke-width="10"/>'
    if mouth == "small":
        if expr == "surprised":
            return f'<ellipse cx="0" cy="-62" rx="15" ry="19" fill="{dark}" stroke-width="9"/>'
        return (f'<path d="M-22 -70 Q0 -42 22 -70 Q0 -62 -22 -70 Z" fill="{dark}" stroke-width="9"/>')
    if mouth == "open":
        top = -76 if not frown else -66
        return (f'<path d="M-30 {top} Q0 -30 30 {top} Q0 {top+10} -30 {top} Z" fill="{dark}" stroke-width="9"/>'
                f'<path d="M-14 -46 Q0 -38 14 -46" fill="{tongue}" stroke="none"/>')
    # wide
    return (f'<path d="M-36 -80 Q0 -20 36 -80 Q0 -70 -36 -80 Z" fill="{dark}" stroke-width="9"/>'
            f'<path d="M-18 -40 Q0 -30 18 -40" fill="{tongue}" stroke="none"/>'
            f'<path d="M-28 -77 Q0 -71 28 -77 L26 -70 Q0 -66 -26 -70 Z" fill="#FFFFFF" stroke="none"/>')


def hair_back(s):
    h, c = s["hair"], s["hair_c"]
    if h == "coif":
        return f'<path d="M-170 -150 C-176 -300 176 -300 170 -150 L176 -10 L-176 -10 Z" fill="{c}"/>'
    if h == "hood":
        return f'<path d="M-176 -140 C-180 -320 180 -320 176 -140 L190 10 L-190 10 Z" fill="{c}"/>'
    if h == "bun":
        return f'<circle cx="0" cy="-292" r="44" fill="{c}"/>'
    return ""


def hair_front(s):
    h, c = s["hair"], s["hair_c"]
    if h == "curl":  # Wy's question-mark curl (from the logo)
        d = "M-60 -298 C-60 -364 68 -370 68 -306 C68 -268 14 -268 8 -222"
        return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="40"/>'
                f'<path d="{d}" fill="none" stroke="{c}" stroke-width="22"/>')
    if h == "judge_cap":
        return (f'<path d="M-118 -236 L-112 -300 Q0 -330 112 -300 L118 -236 Q0 -262 -118 -236 Z" fill="{c}"/>'
                f'<path d="M-118 -236 Q0 -262 118 -236" fill="none" stroke="#FFC93C" stroke-width="9"/>')
    if h == "lawyer_cap":
        return (f'<path d="M-126 -232 Q-140 -300 -60 -312 Q0 -322 60 -312 Q140 -300 126 -232 Q0 -258 -126 -232 Z" fill="{c}"/>'
                f'<path d="M-150 -168 Q-160 -224 -124 -236" fill="none" stroke="{s.get("hair2", INK)}" stroke-width="22"/>'
                f'<path d="M150 -168 Q160 -224 124 -236" fill="none" stroke="{s.get("hair2", INK)}" stroke-width="22"/>')
    if h == "mitre":
        return (f'<path d="M-104 -238 L-92 -360 Q-40 -420 0 -452 Q40 -420 92 -360 L104 -238 Q0 -262 -104 -238 Z" fill="{c}"/>'
                f'<path d="M0 -448 L0 -248 M-40 -330 L40 -330" fill="none" stroke="{s["trim"]}" stroke-width="13"/>'
                f'<path d="M-104 -238 Q0 -262 104 -238" fill="none" stroke="{s["trim"]}" stroke-width="12"/>')
    if h == "feather_cap":
        return (f'<path d="M-130 -232 Q-120 -306 0 -312 Q120 -306 140 -240 Q0 -262 -130 -232 Z" fill="{c}"/>'
                f'<path d="M60 -296 Q150 -380 190 -330 Q140 -326 92 -282 Z" fill="#FFC93C"/>')
    if h == "coif":
        return (f'<path d="M-148 -150 C-150 -296 150 -296 148 -150 Q120 -236 0 -244 Q-120 -236 -148 -150 Z" fill="{c}"/>')
    if h == "hood":
        return (f'<path d="M-152 -140 C-156 -300 156 -300 152 -140 Q126 -244 0 -252 Q-126 -244 -152 -140 Z" fill="{c}"/>')
    if h == "straw_hat":
        return (f'<ellipse cx="0" cy="-236" rx="196" ry="38" fill="{c}"/>'
                f'<path d="M-96 -240 Q-92 -318 0 -322 Q92 -318 96 -240 Z" fill="{c}"/>'
                f'<path d="M-94 -258 Q0 -272 94 -258" fill="none" stroke="#B3262E" stroke-width="12"/>')
    if h == "tonsure":
        return (f'<path d="M-150 -150 Q-150 -232 -96 -250 Q-80 -214 -56 -236 L-60 -200 Q-120 -200 -150 -150 Z" fill="{c}"/>'
                f'<path d="M150 -150 Q150 -232 96 -250 Q80 -214 56 -236 L60 -200 Q120 -200 150 -150 Z" fill="{c}"/>')
    if h == "fur_hat":
        return (f'<path d="M-140 -228 Q-150 -330 0 -336 Q150 -330 140 -228 Q0 -252 -140 -228 Z" fill="{c}"/>'
                f'<path d="M-146 -226 Q0 -260 146 -226" fill="none" stroke="{shade(c, 0.7)}" stroke-width="24"/>')
    if h == "bowl":
        return (f'<path d="M-152 -150 C-160 -290 160 -290 152 -150 Q130 -210 60 -214 L40 -190 L20 -214 Q-110 -216 -152 -150 Z" fill="{c}"/>')
    if h == "bun":
        return (f'<path d="M-150 -150 C-150 -296 150 -296 150 -150 Q120 -232 0 -238 Q-120 -232 -150 -150 Z" fill="{c}"/>')
    return ""


@functools.lru_cache(maxsize=4096)
def head_img(cid, expr="neutral", mouth="closed", eyes="open", look=(0, 0), scale=1.0):
    s = spec(cid)
    hx = s.get("hx", 1.0)
    skin = s["skin"]
    parts = [hair_back(s)]
    parts.append(f'<g transform="scale({hx},1)"><path d="{HEAD}" fill="{skin}"/>'
                 f'<path d="M-80 -232 Q-50 -256 -10 -260" fill="none" stroke="#FFFFFF" stroke-opacity="0.45" stroke-width="12"/></g>')
    if s.get("stubble"):
        parts.append(f'<path d="M-118 -70 Q0 30 118 -70 Q60 -10 0 -12 Q-60 -10 -118 -70 Z" fill="{shade(skin, 0.82)}" stroke="none"/>')
    parts.append(f'<ellipse cx="-104" cy="-80" rx="26" ry="16" fill="{CHEEK}" opacity="0.8" stroke="none"/>'
                 f'<ellipse cx="106" cy="-80" rx="26" ry="16" fill="{CHEEK}" opacity="0.8" stroke="none"/>')
    parts.append(eyes_svg(expr, eyes, look, skin))
    parts.append(brows_svg(expr))
    if s.get("beard"):
        parts.append(f'<path d="M-120 -96 Q-110 40 0 70 Q110 40 120 -96 Q90 -40 40 -44 Q0 -30 -40 -44 Q-90 -40 -120 -96 Z" fill="{s["beard"]}"/>')
        parts.append(f'<path d="M-52 -96 Q-20 -112 0 -98 Q20 -112 52 -96 Q30 -84 0 -90 Q-30 -84 -52 -96 Z" fill="{s["beard"]}"/>')
    parts.append(mouth_svg(expr, mouth))
    parts.append(hair_front(s))
    return _png(_svg("".join(parts), (-215, -470, 215, 90)), scale), (215, 470)  # image, pivot (px at scale 1)


@functools.lru_cache(maxsize=256)
def body_img(cid, scale=1.0):
    s = spec(cid)
    p = []
    top, collar = s["top"], s["collar"]
    if s.get("robe"):
        p.append(f'<ellipse cx="-44" cy="-6" rx="40" ry="20" fill="{s.get("shoes", INK)}"/>'
                 f'<ellipse cx="44" cy="-6" rx="40" ry="20" fill="{s.get("shoes", INK)}"/>')
        p.append(f'<path d="M-104 -238 Q-150 -120 -150 -22 Q0 -4 150 -22 Q150 -120 104 -238 Q0 -262 -104 -238 Z" fill="{top}"/>')
        if s.get("fur"):
            p.append(f'<path d="M-150 -22 Q0 -4 150 -22 L148 -50 Q0 -32 -148 -50 Z" fill="{s["fur"]}" stroke-width="8"/>')
        if s.get("trim"):
            p.append(f'<path d="M0 -240 L0 -14" fill="none" stroke="{s["trim"]}" stroke-width="22"/>'
                     f'<path d="M0 -240 L0 -14" fill="none" stroke-width="3"/>')
        if s.get("apron"):
            p.append(f'<path d="M-70 -150 L70 -150 L84 -30 Q0 -20 -84 -30 Z" fill="{s["apron"]}" stroke-width="8"/>')
        if s.get("belt"):
            p.append(f'<path d="M-122 -132 Q0 -112 122 -132" fill="none" stroke="{s["belt"]}" stroke-width="16"/>')
    else:
        lg = s.get("legs", "#24476B")
        p.append(f'<rect x="-66" y="-90" width="50" height="86" rx="20" fill="{lg}"/>'
                 f'<rect x="16" y="-90" width="50" height="86" rx="20" fill="{lg}"/>')
        p.append(f'<path d="M-78 -2 Q-80 -34 -40 -30 Q-8 -28 -10 -2 Z" fill="{s.get("shoes", INK)}"/>'
                 f'<path d="M78 -2 Q80 -34 40 -30 Q8 -28 10 -2 Z" fill="{s.get("shoes", INK)}"/>')
        p.append(f'<path d="M-100 -238 Q-136 -170 -118 -90 Q0 -64 118 -90 Q136 -170 100 -238 Q0 -262 -100 -238 Z" fill="{top}"/>')
        if s.get("belt"):
            p.append(f'<path d="M-120 -104 Q0 -84 120 -104" fill="none" stroke="{s["belt"]}" stroke-width="16"/>')
    # collar
    if s.get("fur"):
        p.append(f'<path d="M-108 -236 Q0 -170 108 -236 Q60 -266 0 -262 Q-60 -266 -108 -236 Z" fill="{s["fur"]}"/>')
    else:
        p.append(f'<path d="M-44 -246 L0 -206 L44 -246" fill="{collar}" stroke-width="9"/>')
    if s.get("bands"):
        p.append('<path d="M-16 -212 L-22 -150 L-2 -150 L0 -206 L2 -150 L22 -150 L16 -212 Z" fill="#FFFFFF" stroke-width="7"/>')
    if s.get("badge"):
        p.append('<circle cx="62" cy="-150" r="26" fill="#FFC93C" stroke-width="7"/>'
                 '<path d="M50 -150 L59 -141 L75 -160" fill="none" stroke-width="7"/>')
    return _png(_svg("".join(p), (-170, -280, 170, 30)), scale), (170, 280)


@functools.lru_cache(maxsize=256)
def arm_img(cid, scale=1.0, hold=None):
    """Arm hanging down from pivot (0,0). Hand at (0, 150)."""
    s = spec(cid)
    sleeve = s["top"]
    p = [f'<path d="M-24 0 L-22 120 Q0 140 22 120 L24 0 Q0 -14 -24 0 Z" fill="{sleeve}"/>']
    if s.get("fur") or s.get("robe"):
        p.append(f'<path d="M-30 96 L-26 132 Q0 146 26 132 L30 96 Q0 108 -30 96 Z" fill="{s.get("fur") or shade(sleeve, 0.8)}" stroke-width="8"/>')
    p.append(f'<circle cx="0" cy="152" r="25" fill="{s["skin"]}"/>')
    if hold:
        p.append(prop_svg(hold, at=(0, 160)))
    return _png(_svg("".join(p), (-300, -300, 300, 300)), scale), (300, 300)

# ---------------------------------------------------------------- props held / placed

def prop_svg(name, at=(0, 0)):
    x, y = at
    if name == "gavel":
        return (f'<g transform="translate({x},{y}) rotate(-20)">'
                f'<rect x="-7" y="-10" width="14" height="110" rx="6" fill="#8A5A3B"/>'
                f'<rect x="-46" y="-40" width="92" height="44" rx="12" fill="#5B3A29"/></g>')
    if name == "scroll":
        return (f'<g transform="translate({x},{y})"><rect x="-60" y="-20" width="120" height="150" fill="#F3E2BC"/>'
                f'<path d="M-40 10 H40 M-40 40 H40 M-40 70 H24 M-40 100 H34" stroke="#A8865A" stroke-width="7"/>'
                f'<rect x="-72" y="-34" width="144" height="26" rx="13" fill="#E3C78F"/>'
                f'<rect x="-72" y="122" width="144" height="26" rx="13" fill="#E3C78F"/></g>')
    if name == "quill":
        return (f'<g transform="translate({x},{y}) rotate(25)"><path d="M0 0 Q30 -80 10 -150 Q-30 -80 0 0 Z" fill="#FFF4E0"/></g>')
    if name == "staff":
        return (f'<g transform="translate({x},{y})"><rect x="-8" y="-240" width="16" height="420" rx="8" fill="#8A5A3B"/>'
                f'<path d="M0 -240 Q-60 -260 -50 -320 Q-10 -350 20 -310" fill="none" stroke="#FFC93C" stroke-width="16"/></g>')
    if name == "torch":
        return (f'<g transform="translate({x},{y})"><rect x="-9" y="-120" width="18" height="190" rx="8" fill="#6B4A32"/>'
                f'<path d="M0 -230 Q50 -170 30 -126 Q0 -110 -30 -126 Q-50 -170 0 -230 Z" fill="#FFB238"/>'
                f'<path d="M0 -190 Q24 -156 14 -134 Q0 -126 -14 -134 Q-24 -156 0 -190 Z" fill="#FFF0A0" stroke="none"/></g>')
    if name == "coin":
        return (f'<g transform="translate({x},{y})"><circle r="30" fill="#FFC93C"/>'
                f'<circle r="18" fill="none" stroke="#C9921E" stroke-width="6"/></g>')
    if name == "egg":
        return (f'<g transform="translate({x},{y})"><path d="M0 -60 C34 -60 46 -10 46 14 C46 44 24 60 0 60 C-24 60 -46 44 -46 14 C-46 -10 -34 -60 0 -60 Z" fill="#FFF4E0"/>'
                f'<path d="M-20 -30 Q-10 -44 4 -46" fill="none" stroke="#FFFFFF" stroke-width="8"/></g>')
    if name == "gloves":
        g = ('<path d="M-40 60 L-44 -10 Q-44 -36 -30 -36 L-30 -60 Q-22 -72 -14 -60 L-12 -70 Q-2 -82 6 -68 L8 -64 Q18 -74 24 -60 '
             'L24 -20 Q36 -34 44 -24 Q50 -14 30 20 L26 60 Z" fill="#F3E2BC"/>'
             '<path d="M-44 44 L28 44" stroke="#C9A27A" stroke-width="10"/>')
        return (f'<g transform="translate({x},{y})"><g transform="translate(-34,0) rotate(-12)">{g}</g>'
                f'<g transform="translate(34,0) rotate(12) scale(-1,1)">{g}</g></g>')
    if name == "sack":
        return (f'<g transform="translate({x},{y})"><path d="M-70 60 Q-90 -30 -30 -60 L-40 -84 Q0 -96 40 -84 L30 -60 Q90 -30 70 60 Q0 80 -70 60 Z" fill="#D8B27A"/>'
                f'<path d="M-36 -64 Q0 -54 36 -64" fill="none" stroke-width="9"/>'
                f'<text x="0" y="30" font-family="Lilita One" font-size="70" text-anchor="middle" fill="{INK}" stroke="none">1/10</text></g>')
    if name == "painting":  # church fresco of the Falaise execution (our own drawing)
        return (f'<g transform="translate({x},{y})"><rect x="-150" y="-110" width="300" height="220" rx="6" fill="#C9921E"/>'
                f'<rect x="-130" y="-90" width="260" height="180" fill="#E9D9B4" stroke-width="6"/>'
                f'<rect x="-130" y="30" width="260" height="60" fill="#B9A88E" stroke="none"/>'
                f'<rect x="-50" y="0" width="100" height="40" fill="#A0703F" stroke-width="5"/>'
                f'<ellipse cx="0" cy="-12" rx="34" ry="22" fill="#F7A8B8" stroke-width="5"/>'
                f'<path d="M-22 -30 L22 -30 L28 0 L-28 0 Z" fill="#2E6FA7" stroke-width="5"/>'
                f'<circle cx="28" cy="-24" r="14" fill="#F7A8B8" stroke-width="5"/>'
                + "".join(f'<circle cx="{cx}" cy="58" r="13" fill="#{c}" stroke-width="4"/><rect x="{cx-12}" y="66" width="24" height="24" fill="#{c}" stroke-width="4"/>'
                          for cx, c in [(-100, "3E8E5E"), (-72, "B3262E"), (66, "8A5A3B"), (96, "2E6FA7")])
                + '<path d="M-130 -90 L-40 -90 L-130 -20 Z" fill="#FFF4E0" opacity="0.4" stroke="none"/></g>')
    if name == "barley":
        return (f'<g transform="translate({x},{y})">' + "".join(
            f'<g transform="rotate({a})"><path d="M0 0 L0 -150" stroke="#C99A2E" stroke-width="7"/>'
            f'<path d="M0 -150 Q-14 -190 0 -230 Q14 -190 0 -150 Z" fill="#E8C46A" stroke-width="6"/></g>'
            for a in (-18, 0, 18)) + '</g>')
    return ""


def prop_img(name, scale=1.0):
    return _png(_svg(prop_svg(name), (-160, -360, 160, 200)), scale), (160, 360)

# ---------------------------------------------------------------- animals (single layer + blink/mouth variants)

@functools.lru_cache(maxsize=1024)
def animal_img(kind, expr="neutral", mouth="closed", eyes="open", outfit=None, scale=1.0):
    """Animals face 3/4 to screen-right. Pivot at feet centre. Returns (img, pivot)."""
    p = []
    def eye(cx, cy, r=24, look=(1, 0)):
        if eyes == "closed":
            return f'<path d="M{cx-r} {cy} Q{cx} {cy+r*0.8} {cx+r} {cy}" fill="none" stroke-width="9"/>'
        rr = r * (1.15 if expr == "surprised" else 1)
        e = (f'<ellipse cx="{cx}" cy="{cy}" rx="{rr*0.8}" ry="{rr}" fill="#FFFFFF" stroke-width="8"/>'
             f'<circle cx="{cx+5*look[0]}" cy="{cy+2}" r="{rr*0.45}" fill="{INK}" stroke="none"/>'
             f'<circle cx="{cx+5*look[0]+5}" cy="{cy-6}" r="{rr*0.17}" fill="#FFFFFF" stroke="none"/>')
        if eyes == "half" or expr in ("smug", "sly"):
            e += f'<path d="M{cx-rr} {cy-4} L{cx+rr} {cy-4} L{cx+rr} {cy-rr-6} L{cx-rr} {cy-rr-6} Z" fill="{lidc}" stroke="none"/>'
            e += f'<path d="M{cx-rr*0.8} {cy-4} L{cx+rr*0.8} {cy-4}" stroke-width="8"/>'
        return e
    def brow(cx, cy, w=26):
        if expr == "worried":
            return f'<path d="M{cx-w} {cy+4} Q{cx} {cy-2} {cx+w} {cy-12}" fill="none" stroke-width="9"/>'
        if expr in ("angry", "sly"):
            return f'<path d="M{cx-w} {cy-10} Q{cx} {cy} {cx+w} {cy+8}" fill="none" stroke-width="9"/>'
        if expr == "surprised":
            return f'<path d="M{cx-w} {cy-6} Q{cx} {cy-22} {cx+w} {cy-6}" fill="none" stroke-width="9"/>'
        return ""
    if kind == "pig":
        pink, lidc = "#F7A8B8", "#F7A8B8"
        p.append(f'<path d="M-168 -170 Q-200 -200 -186 -150" fill="none" stroke="{INK}" stroke-width="10"/>')  # tail
        for lx in (-110, -60, 50, 100):
            p.append(f'<rect x="{lx-20}" y="-70" width="40" height="70" rx="16" fill="{shade(pink,0.9)}"/>')
            p.append(f'<rect x="{lx-20}" y="-18" width="40" height="18" rx="6" fill="#8A5A5A"/>')
        p.append(f'<ellipse cx="-20" cy="-150" rx="160" ry="104" fill="{pink}"/>')
        if outfit == "clothes":
            p.append('<path d="M-150 -196 Q-20 -250 110 -196 L130 -90 Q-20 -40 -170 -90 Z" fill="#2E6FA7"/>'
                     '<path d="M-26 -236 L-26 -60" stroke-width="7"/>'
                     '<circle cx="-8" cy="-180" r="7" fill="#FFC93C"/><circle cx="-8" cy="-140" r="7" fill="#FFC93C"/>'
                     '<circle cx="-8" cy="-100" r="7" fill="#FFC93C"/>'
                     '<path d="M-60 -236 Q-26 -206 6 -236" fill="#FFF4E0" stroke-width="8"/>')
        p.append(f'<ellipse cx="120" cy="-220" rx="96" ry="86" fill="{pink}"/>')
        p.append(f'<path d="M60 -290 L44 -350 L100 -300 Z" fill="{shade(pink,0.85)}"/>'
                 f'<path d="M150 -296 L176 -356 L190 -282 Z" fill="{shade(pink,0.85)}"/>')
        if outfit == "clothes":
            p.append('<path d="M40 -284 Q120 -340 200 -284 Q120 -300 40 -284 Z" fill="#5B3A29"/>'
                     '<path d="M70 -296 Q120 -360 170 -296 Z" fill="#5B3A29"/>')
        p.append(eye(100, -236, 20) + eye(160, -236, 20))
        p.append(brow(100, -268, 20) + brow(162, -268, 20))
        p.append(f'<ellipse cx="190" cy="-190" rx="40" ry="30" fill="#F28CA2"/>'
                 f'<ellipse cx="178" cy="-190" rx="7" ry="10" fill="{INK}" stroke="none"/>'
                 f'<ellipse cx="202" cy="-190" rx="7" ry="10" fill="{INK}" stroke="none"/>')
        p.append(f'<ellipse cx="72" cy="-188" rx="18" ry="11" fill="{CHEEK}" stroke="none"/>')
        m = {"closed": "M120 -160 Q140 -150 160 -162", "small": "M120 -160 Q140 -140 160 -162 Z",
             "open": "M118 -162 Q140 -128 162 -164 Z", "wide": "M116 -164 Q140 -120 164 -166 Z"}[mouth]
        frown = expr in ("worried", "sad")
        if mouth == "closed" and frown:
            m = "M120 -152 Q140 -164 160 -152"
        p.append(f'<path d="{m}" fill="{"none" if mouth=="closed" else "#8A2734"}" stroke-width="8"/>')
        vb = (-230, -400, 260, 20)
    elif kind == "rat":
        fur, lidc = "#9AA0A8", "#9AA0A8"
        p.append(f'<path d="M-50 -30 Q-170 -10 -190 -90 Q-200 -140 -160 -150" fill="none" stroke="{INK}" stroke-width="22"/>'
                 f'<path d="M-50 -30 Q-170 -10 -190 -90 Q-200 -140 -160 -150" fill="none" stroke="#E8A0A8" stroke-width="10"/>')
        p.append(f'<ellipse cx="-40" cy="-12" rx="30" ry="14" fill="#E8A0A8"/><ellipse cx="40" cy="-12" rx="30" ry="14" fill="#E8A0A8"/>')
        p.append(f'<path d="M-70 -20 Q-90 -160 0 -170 Q90 -160 70 -20 Q0 -4 -70 -20 Z" fill="{fur}"/>')
        p.append(f'<path d="M-36 -40 Q-40 -120 0 -124 Q40 -120 36 -40 Q0 -30 -36 -40 Z" fill="#D6D9DE" stroke="none"/>')
        p.append(f'<circle cx="-70" cy="-262" r="46" fill="{fur}"/><circle cx="-70" cy="-262" r="26" fill="#E8A0A8" stroke="none"/>'
                 f'<circle cx="80" cy="-262" r="46" fill="{fur}"/><circle cx="80" cy="-262" r="26" fill="#E8A0A8" stroke="none"/>')
        p.append(f'<path d="M-80 -190 Q-90 -270 0 -272 Q90 -270 80 -190 Q60 -140 0 -136 Q-60 -140 -80 -190 Z" fill="{fur}"/>')
        p.append(f'<path d="M-30 -160 Q0 -120 30 -160 Q0 -170 -30 -160 Z" fill="#D6D9DE" stroke="none"/>')
        p.append(eye(-30, -214, 18, (0, 0)) + eye(30, -214, 18, (0, 0)) + brow(-30, -244, 16) + brow(32, -244, 16))
        p.append(f'<ellipse cx="0" cy="-168" rx="14" ry="10" fill="#E8708A"/>')
        p.append('<path d="M-12 -150 Q0 -140 12 -150" fill="none" stroke-width="7"/>'
                 '<rect x="-9" y="-150" width="18" height="16" rx="3" fill="#FFFFFF" stroke-width="5"/>')
        p.append('<path d="M-20 -168 L-80 -178 M-20 -162 L-78 -156 M20 -168 L80 -178 M20 -162 L78 -156" stroke-width="4"/>')
        if outfit == "scroll":
            p.append(prop_svg("scroll", at=(60, -120)).replace('translate(60,-120)', 'translate(60,-120) scale(0.5)'))
        vb = (-230, -330, 150, 20)
    elif kind == "cat":
        fur, lidc = "#F0A04B", "#F0A04B"
        p.append(f'<path d="M80 -20 Q190 -10 170 -120 Q160 -170 200 -190" fill="none" stroke="{INK}" stroke-width="36"/>'
                 f'<path d="M80 -20 Q190 -10 170 -120 Q160 -170 200 -190" fill="none" stroke="{fur}" stroke-width="20"/>')
        p.append(f'<path d="M-100 -10 Q-120 -170 0 -180 Q120 -170 100 -10 Q0 6 -100 -10 Z" fill="{fur}"/>')
        p.append(f'<path d="M-40 -10 Q-40 -110 0 -112 Q40 -110 40 -10 Z" fill="#FFF4E0" stroke="none"/>')
        p.append(f'<path d="M-110 -250 L-120 -370 L-40 -320 Z" fill="{fur}"/><path d="M110 -250 L120 -370 L40 -320 Z" fill="{fur}"/>')
        p.append(f'<ellipse cx="0" cy="-260" rx="124" ry="100" fill="{fur}"/>')
        p.append('<path d="M-40 -350 L-30 -310 M0 -358 L0 -316 M40 -350 L30 -310" stroke="#C9762E" stroke-width="12"/>')
        p.append(eye(-48, -270, 26) + eye(48, -270, 26))
        p.append(brow(-48, -306, 24) + brow(48, -306, 24))
        p.append(f'<path d="M-12 -224 L12 -224 L0 -210 Z" fill="#E8708A" stroke-width="6"/>'
                 '<path d="M0 -210 Q-14 -194 -30 -204 M0 -210 Q14 -194 30 -204" fill="none" stroke-width="7"/>'
                 '<path d="M-40 -220 L-130 -232 M-40 -212 L-128 -206 M40 -220 L130 -232 M40 -212 L128 -206" stroke-width="4"/>')
        vb = (-200, -400, 240, 20)
    elif kind == "rooster":
        lidc = "#FFFFFF"
        p.append('<path d="M-60 -40 L-60 0 M-80 0 L-40 0 M40 -40 L40 0 M20 0 L60 0" stroke="#E8A03A" stroke-width="14"/>')
        for i, c in enumerate(("#2E6B4E", "#B3262E", "#1F4E6B")):
            p.append(f'<path d="M-90 -150 Q{-230+20*i} {-300+40*i} {-150+30*i} {-110+20*i} Z" fill="{c}"/>')
        p.append('<ellipse cx="-10" cy="-120" rx="110" ry="86" fill="#FFF8EE"/>')
        p.append('<path d="M-60 -130 Q-10 -60 50 -120" fill="none" stroke="#E8DCC8" stroke-width="10"/>')
        p.append('<path d="M40 -170 Q30 -280 100 -300 Q160 -290 150 -220 Q140 -170 80 -150 Z" fill="#FFF8EE"/>')
        p.append('<path d="M80 -300 Q70 -350 100 -340 Q110 -370 130 -344 Q150 -360 154 -326 Q170 -320 150 -296 Z" fill="#E8333A"/>')
        p.append('<path d="M150 -262 L196 -248 L150 -232 Z" fill="#FFB238"/>')
        p.append('<path d="M146 -232 Q160 -196 136 -196 Q124 -210 140 -232 Z" fill="#E8333A"/>')
        p.append(eye(118, -262, 15))
        p.append(brow(118, -284, 14))
        if mouth != "closed":
            p.append('<path d="M150 -248 L190 -232 L150 -236 Z" fill="#8A2734" stroke-width="5"/>')
        vb = (-240, -390, 220, 20)
    elif kind == "weevil":
        g, lidc = "#5FBF5A", "#5FBF5A"
        for lx in (-70, -10, 50):
            p.append(f'<path d="M{lx} -50 L{lx-20} 0" stroke-width="12"/>')
        p.append(f'<ellipse cx="-20" cy="-90" rx="100" ry="70" fill="{g}"/>')
        p.append(f'<path d="M-20 -158 L-20 -22" stroke="{shade(g,0.7)}" stroke-width="7"/>'
                 '<path d="M-80 -120 Q-60 -150 -30 -152" fill="none" stroke="#C8F0B0" stroke-width="10"/>')
        p.append(f'<circle cx="90" cy="-120" r="52" fill="{g}"/>')
        p.append(f'<path d="M130 -110 Q190 -90 230 -40" fill="none" stroke="{INK}" stroke-width="26"/>'
                 f'<path d="M130 -110 Q190 -90 230 -40" fill="none" stroke="{shade(g,0.85)}" stroke-width="12"/>')
        p.append('<path d="M180 -86 L200 -150 L236 -170 M160 -94 L160 -160 L190 -190" fill="none" stroke-width="7"/>')
        p.append(eye(84, -132, 20) + eye(118, -134, 17) + brow(86, -160, 18) + brow(120, -160, 15))
        vb = (-150, -230, 270, 20)
    elif kind == "basilisk":
        lidc = "#3E8E5E"
        p.append('<path d="M-260 -40 Q-160 -160 -40 -80 Q60 -10 120 -120" fill="none" stroke="#2A1C1E" stroke-width="80"/>'
                 '<path d="M-260 -40 Q-160 -160 -40 -80 Q60 -10 120 -120" fill="none" stroke="#3E8E5E" stroke-width="58"/>')
        p.append('<path d="M-200 -110 L-180 -160 L-160 -112 M-110 -116 L-90 -170 L-70 -104" fill="#E8333A"/>')
        p.append('<path d="M60 -150 Q60 -260 150 -270 Q230 -260 220 -180 Q200 -130 120 -120 Z" fill="#3E8E5E"/>')
        p.append('<path d="M120 -266 Q110 -330 150 -316 Q166 -346 186 -310 Q214 -320 210 -280 Z" fill="#E8333A"/>')
        p.append('<path d="M214 -220 L270 -196 L212 -186 Z" fill="#FFB238"/>')
        p.append('<circle cx="170" cy="-220" r="22" fill="#FFF06A"/><ellipse cx="170" cy="-220" rx="6" ry="16" fill="#2A1C1E" stroke="none"/>')
        vb = (-320, -360, 300, 40)
    elif kind in ("dog", "bull", "horse"):
        col = {"dog": "#C98A4B", "bull": "#6B4A3A", "horse": "#A8703F"}[kind]
        lidc = col
        L = {"dog": 1.0, "bull": 1.35, "horse": 1.3}[kind]
        for lx in (-110, -60, 50, 100):
            hh = 90 if kind == "dog" else 120
            p.append(f'<rect x="{lx*L-18}" y="{-hh}" width="36" height="{hh}" rx="14" fill="{shade(col,0.9)}"/>')
            p.append(f'<rect x="{lx*L-18}" y="-16" width="36" height="16" rx="5" fill="{INK}"/>')
        if kind == "horse":
            p.append(f'<path d="M{-150*L} -200 Q{-210*L} -150 {-190*L} -60" fill="none" stroke="{INK}" stroke-width="34"/>'
                     f'<path d="M{-150*L} -200 Q{-210*L} -150 {-190*L} -60" fill="none" stroke="#5B3A29" stroke-width="20"/>')
        else:
            p.append(f'<path d="M{-150*L} -180 Q{-200*L} -230 {-180*L} -260" fill="none" stroke="{INK}" stroke-width="22"/>'
                     f'<path d="M{-150*L} -180 Q{-200*L} -230 {-180*L} -260" fill="none" stroke="{col}" stroke-width="10"/>')
        p.append(f'<ellipse cx="-10" cy="-170" rx="{150*L}" ry="{80 if kind=="dog" else 95}" fill="{col}"/>')
        if kind == "bull":
            p.append('<path d="M60 -250 Q20 -320 70 -330 M190 -250 Q240 -320 190 -330" fill="none" stroke="#FFF4E0" stroke-width="22"/>')
        hx_, hy_ = (130, -250) if kind != "horse" else (170, -310)
        if kind == "horse":
            p.append(f'<path d="M90 -200 L140 -300 L200 -290 L150 -180 Z" fill="{col}"/>'
                     '<path d="M120 -300 Q90 -230 70 -190" fill="none" stroke="#5B3A29" stroke-width="22"/>')
        p.append(f'<ellipse cx="{hx_}" cy="{hy_}" rx="80" ry="72" fill="{col}"/>')
        if kind == "dog":
            p.append(f'<path d="M70 -290 Q40 -260 60 -200 Q90 -240 96 -290 Z" fill="{shade(col,0.7)}"/>'
                     f'<path d="M190 -290 Q220 -260 200 -200 Q170 -240 164 -290 Z" fill="{shade(col,0.7)}"/>')
        else:
            p.append(f'<path d="M{hx_-50} {hy_-60} L{hx_-60} {hy_-110} L{hx_-20} {hy_-70} Z" fill="{col}"/>'
                     f'<path d="M{hx_+40} {hy_-60} L{hx_+60} {hy_-110} L{hx_+15} {hy_-72} Z" fill="{col}"/>')
        p.append(eye(hx_ - 25, hy_ - 12, 17) + eye(hx_ + 25, hy_ - 12, 17) + brow(hx_ - 25, hy_ - 38, 16) + brow(hx_ + 27, hy_ - 38, 16))
        p.append(f'<ellipse cx="{hx_+5}" cy="{hy_+38}" rx="46" ry="30" fill="{shade(col,1.35)}"/>'
                 f'<ellipse cx="{hx_-8}" cy="{hy_+30}" rx="7" ry="6" fill="{INK}" stroke="none"/>'
                 f'<ellipse cx="{hx_+18}" cy="{hy_+30}" rx="7" ry="6" fill="{INK}" stroke="none"/>')
        if kind == "dog":
            p.append(f'<path d="M{hx_-10} {hy_+52} Q{hx_+5} {hy_+70} {hx_+22} {hy_+52}" fill="#E8707A" stroke-width="7"/>')
        vb = (-280, -420, 290, 20)
    elif kind == "locust":
        g, lidc = "#9CB84A", "#9CB84A"
        p.append('<path d="M-40 -40 L-110 -110 L-150 0 M20 -40 L-20 -120 L-60 0" fill="none" stroke-width="10"/>')
        p.append(f'<ellipse cx="-40" cy="-70" rx="120" ry="40" fill="{g}"/>')
        p.append('<path d="M-130 -90 Q-40 -150 60 -96 Q-40 -110 -130 -90 Z" fill="#D8E8A0" opacity="0.9"/>')
        p.append(f'<circle cx="90" cy="-84" r="40" fill="{g}"/>')
        p.append('<path d="M100 -120 Q150 -190 200 -200 M86 -122 Q110 -200 150 -220" fill="none" stroke-width="6"/>')
        p.append(eye(98, -92, 17) + brow(98, -116, 15))
        vb = (-200, -240, 230, 20)
    s = _svg("".join(p), vb)
    return _png(s, scale), (-vb[0], -vb[1])


if __name__ == "__main__":
    # contact sheet for checking the cast
    import sys
    sheet = Image.new("RGBA", (2600, 1500), "#0F6B78")
    x = 40
    for i, cid in enumerate(list(CHARS) + ["villager1", "villager2", "villager3"]):
        b, bp = body_img(cid, 0.5)
        h, hp = head_img(cid, ["happy", "surprised", "worried", "smug", "angry", "neutral"][i % 6], ["open", "small", "closed", "wide"][i % 4], scale=0.5)
        a, ap = arm_img(cid, 0.5)
        fx, fy = x + 90, 700
        sheet.alpha_composite(b, (int(fx - bp[0] * 0.5), int(fy - bp[1] * 0.5)))
        sheet.alpha_composite(a.rotate(-25, center=(ap[0] * .5, ap[1] * .5)), (int(fx - 50 - ap[0] * .5), int(fy - 115 - ap[1] * .5)))
        sheet.alpha_composite(a.rotate(140, center=(ap[0] * .5, ap[1] * .5)), (int(fx + 50 - ap[0] * .5), int(fy - 115 - ap[1] * .5)))
        sheet.alpha_composite(h, (int(fx - hp[0] * .5), int(fy - 120 - hp[1] * .5)))
        x += 200
    x = 60
    for k, ex in [("pig", "neutral"), ("pig", "worried"), ("rat", "sly"), ("cat", "sly"), ("rooster", "surprised"), ("weevil", "neutral"), ("basilisk", "angry")]:
        im, pv = animal_img(k, ex, "open" if k == "rat" else "closed", outfit="clothes" if ex == "worried" else None, scale=0.6)
        sheet.alpha_composite(im, (x, 1400 - im.height))
        x += im.width + 30
    sheet.save(sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/cast_sheet.png")
