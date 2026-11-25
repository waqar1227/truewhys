"""TrueWhys cast v2 (owner-approved direction D3, 15 Nov 2026; audit report §6.1).

Older, drier proportions than cast v1 (lib/cast.py): head ~1/3 of body height, smaller eyes with lids and
brows, a nose, no rosy cheeks, neck + shoulders, mitten hands with a thumb, deadpan default expression.
Same brand rules: thick dark ink outline, flat colours + one shade, our skin tones and palette.
Not Rick's Clips (white round heads, stick limbs) and not Ink Explainer (messy-hair stick people).

Units: feet at y=0, head top at about y=-600. figure_svg() returns an SVG group; png() renders it.
python lib/cast2.py <out.png>  -> model sheet: 6 cast + Wy, full body + expression row
"""
import math
import io, sys
import cairosvg
from PIL import Image

INK = "#22181B"
SW = 9


def shade(hexc, f):
    h = hexc.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    if f < 1:
        r, g, b = (int(c * f) for c in (r, g, b))
    else:
        r, g, b = (int(c + (255 - c) * (f - 1)) for c in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"


# role = hat/uniform + one prop (audit: role by hat, uniform and one prop)
CAST = {
    "wy":       dict(name="Wy", skin="#F6D5BC", iris="#5B3A29", face="round", hair="curl", hair_c="#5B3A29", top="#FF6B5B", top2="#FFF4E0",
                     legs="#24476B", shoes=INK, badge=True, jaw=0.0, prop=None),
    "captain":  dict(name="Captain", skin="#EBC09E", iris="#3E6A8C", face="square", hair="tricorn", hair_c="#1E1A24", top="#8E2430", top2="#E8C46A",
                     legs="#2A2A38", shoes=INK, beard="#3A2416", coat=True, jaw=0.3, prop="spyglass"),
    "doctor":   dict(name="Doctor", skin="#C99470", iris="#4A2E1E", face="long", hair="bun", hair_c="#1E1A24", top="#F4F1EA", top2="#3E7CB1",
                     legs="#2E3B52", shoes="#3A2618", coat=True, glasses=True, jaw=0.0, prop="clipboard", female=True),
    "worker":   dict(name="Worker", skin="#E9BC98", iris="#5E7A4A", face="square", hair="hood", hair_c="#6E6650", top="#8A6A44", top2="#C9A27A",
                     legs="#4A3A2C", shoes="#2A1A10", stubble=True, apron="#7A5236", jaw=0.4, prop="shovel"),
    "guard":    dict(name="Guard", skin="#F2CFB2", iris="#5B7A9C", face="long", hair="helmet", hair_c="#9AA3AD", top="#2F4F6F", top2="#C9A23A",
                     legs="#3A3A44", shoes=INK, moustache="#5B3A29", jaw=0.5, prop="spear"),
    "noble":    dict(name="Noble", skin="#F8DFCC", iris="#3E8E7A", face="long", hair="crown_long", hair_c="#7A3E1E", top="#5B3A8C", top2="#FFC93C",
                     legs="#5B3A8C", shoes=INK, gown=True, jaw=0.0, prop="scroll", female=True),
    # added 15 Nov 2026 (same v2.1 rules) for Victorian stories
    "bobby":    dict(name="Constable", skin="#EFC6A6", iris="#4A6A8C", face="long", hair="custodian", hair_c="#1F2A44", top="#1F2A44", top2="#C9CED6",
                     legs="#1A2236", shoes=INK, moustache="#5B3A29", jaw=0.4, prop=None, buttons=True),
    "gent":     dict(name="Gentleman", skin="#F3D0B5", iris="#5B3A29", face="square", hair="tophat", hair_c="#22181B", top="#3A3046", top2="#F4F1EA",
                     legs="#4A4A55", shoes=INK, beard="#7A5236", coat=True, jaw=0.3, prop=None),
    "prof":     dict(name="Professor", skin="#F1CDB0", iris="#4A6A5C", face="round", hair="bald", hair_c="#C9CED6", top="#7A5A3A", top2="#F4F1EA",
                     legs="#4A3A2C", shoes=INK, beard="#D8DCE0", glasses=True, coat=True, jaw=0.0, prop=None),
    "modern":   dict(name="Everyman", skin="#D8A580", iris="#4A2E1E", face="round", hair="short", hair_c="#22181B", top="#3E8E5E", top2="#2A2A38",
                     legs="#3A4A66", shoes="#F4F1EA", hoodie=True, jaw=0.2, prop="phone"),
    # added 19 Nov 2026 for B-004 "shapes" (same v2.1 rules: role by hat, uniform and one prop)
    "clipper":  dict(name="Clipper", skin="#E9BC98", iris="#4A3A2C", face="square", hair="flatcap", hair_c="#6E6650", top="#6E5A44", top2="#C9A27A",
                     legs="#3A3026", shoes="#2A1A10", stubble=True, jaw=0.4, prop=None),
    "newton":   dict(name="Newton", skin="#F3D0B5", iris="#4A5A6A", face="long", hair="periwig", hair_c="#E6E1D6", top="#6E2A30", top2="#F4F1EA",
                     legs="#3A2A2A", shoes=INK, coat=True, jaw=0.2, prop=None),
    "chaloner": dict(name="Chaloner", skin="#EFC6A6", iris="#5B3A29", face="square", hair="tricorn", hair_c="#22181B", top="#4E6A3A", top2="#E8C46A",
                     legs="#2A2A38", shoes=INK, coat=True, moustache="#3A2416", jaw=0.3, prop=None),
    "engineer": dict(name="Engineer", skin="#F1CDB0", iris="#3E5A7A", face="square", hair="fedora", hair_c="#7A6A5A", top="#4A5A7A", top2="#F4F1EA",
                     legs="#3A3A44", shoes=INK, glasses=True, jaw=0.3, prop=None),
    "sewer":    dict(name="Sewer worker", skin="#C99470", iris="#4A2E1E", face="round", hair="hardhat", hair_c="#FFC93C", top="#FF8A3D", top2="#E6E6E6",
                     legs="#2E3B52", shoes="#2A1A10", jaw=0.2, prop=None, buttons=True),
    "knight":   dict(name="Margaret", skin="#F6D5BC", iris="#4A6A5C", face="long", hair="bun", hair_c="#5B3A29", top="#2F5F6A", top2="#F4F1EA",
                     legs="#2F5F6A", shoes=INK, gown=True, jaw=0.0, prop=None, female=True),
    "annan":    dict(name="Annan", skin="#EBC09E", iris="#3E3E3E", face="square", hair="tophat", hair_c="#22181B", top="#4A4A55", top2="#F4F1EA",
                     legs="#3A3A44", shoes=INK, moustache="#22181B", coat=True, jaw=0.5, prop=None),
    "painter":  dict(name="Painter", skin="#F3D0B5", iris="#5B3A29", face="round", hair="bald", hair_c="#B8B0A6", top="#2F3A4F", top2="#F4F1EA",
                     legs="#2F3A4F", shoes=INK, beard="#C9C2B8", coat=True, jaw=0.0, prop=None),
    "gillette": dict(name="Salesman", skin="#EFC6A6", iris="#3E6A8C", face="long", hair="short", hair_c="#3A2416", top="#5A4A3A", top2="#F4F1EA",
                     legs="#4A3A2C", shoes=INK, moustache="#3A2416", coat=True, jaw=0.3, prop=None),
    "baker":    dict(name="Baker", skin="#D8A580", iris="#4A2E1E", face="round", hair="chef", hair_c="#22181B", top="#FFFFFF", top2="#FF6B5B",
                     legs="#3A3A44", shoes=INK, apron="#F4F1EA", jaw=0.2, prop=None, female=True),
    # added 22 Nov 2026 for B-005 "annoying science" (same v2.1 rules)
    "physicist": dict(name="Physicist", skin="#C68E6A", iris="#3A2A1E", face="square", hair="short", hair_c="#1E1A24", top="#F4F1EA", top2="#3E8E7A",
                     legs="#2E3B52", shoes=INK, glasses=True, coat=True, jaw=0.3, prop=None),
    "runner":   dict(name="Runner", skin="#F1CDB0", iris="#3E6A5C", face="round", hair="bun", hair_c="#7A3E1E", top="#FF6B5B", top2="#FFC93C",
                     legs="#24476B", shoes="#F4F1EA", jaw=0.0, prop=None, female=True),
    # added 24 Nov 2026 for B-006 "brain glitches" (same v2.1 rules)
    "mira":     dict(name="Mira", skin="#E9BC98", iris="#3E5A4A", face="long", hair="bun", hair_c="#3A2416", top="#2F8FA0", top2="#FFF4E0",
                     legs="#2A2A38", shoes="#F4F1EA", jaw=0.0, prop="phone", female=True),
    "student":  dict(name="Student", skin="#F3D0B5", iris="#5B3A29", face="round", hair="short", hair_c="#7A3E1E", top="#FFC93C", top2="#2A2A38",
                     legs="#2E3B52", shoes=INK, hoodie=True, jaw=0.1, prop=None),
    # added 24 Nov 2026 for A-026 (same v2.1 rules: role by clothes; winter hat/scarf drawn by lib/flat_winter.py)
    "friend":   dict(name="Friend", skin="#8D5A3C", iris="#3A2A1E", face="long", hair="bun", hair_c="#1E1A24", top="#3E7CB1", top2="#FFF4E0",
                     legs="#2A2A38", shoes="#F4F1EA", jaw=0.0, prop=None, female=True, hoodie=True),
    "herder":   dict(name="Herder", skin="#E3B48E", iris="#3E5A7A", face="square", hair="hood", hair_c="#2F4F6F", top="#2F4F6F", top2="#FFC93C",
                     legs="#3A3026", shoes="#2A1A10", stubble=True, jaw=0.4, prop=None, buttons=True),
    # added 25 Nov 2026 for B-007 "cats vs dogs" (same v2.1 rules)
    "lena":     dict(name="Lena", skin="#F1C9A8", iris="#3E6A5C", face="round", hair="bun", hair_c="#B5532A", top="#6FA34A", top2="#FFF4E0",
                     legs="#3A4A6A", shoes="#F4F1EA", jaw=0.0, prop=None, female=True, hoodie=True),
    "vet":      dict(name="Researcher", skin="#B57A55", iris="#3A2A1E", face="square", hair="short", hair_c="#1E1A24", top="#F4F1EA", top2="#E07A3A",
                     legs="#2A3A4A", shoes=INK, jaw=0.2, prop=None, buttons=True),
}

# expressions: eyelid height (0 = fully open, 1 = closed), brow shapes (left, right) as (inner_dy, outer_dy), mouth
EXPR = {
    "deadpan":    dict(lid=0.45, brow=((0, 0), (0, 0)), mouth="flat"),
    "smug":       dict(lid=0.55, brow=((4, -2), (-14, -6)), mouth="smirk"),
    "suspicious": dict(lid=0.6, brow=((10, 0), (-10, -4)), mouth="side", look=(-1, 0)),
    "shocked":    dict(lid=0.0, brow=((-16, -12), (-16, -12)), mouth="o", pupil=0.7),
    "bored":      dict(lid=0.7, brow=((2, 4), (2, 4)), mouth="flat_down"),
    "smile":      dict(lid=0.35, brow=((-3, -5), (-3, -5)), mouth="smile"),   # B-007: gentle closed smile
    "angry":      dict(lid=0.35, brow=((14, -6), (14, -6)), mouth="grit"),
}


def _head(s, e, view="front"):
    """view "3q": three-quarter turn towards screen right (features shift right, far eye narrower, near ear hidden)."""
    """Head centred at (0,-505): slightly tall rounded box with a jaw; ~190 units tall incl. hair."""
    skin = s["skin"]; jaw = s.get("jaw", 0.2); fem = s.get("female")
    face = s.get("face", "round")
    w = (62 if fem else 66) + {"round": 6, "square": 4, "long": -4}[face]
    jaw = {"round": 0.0, "square": 0.9, "long": 0.4}[face] if "jaw" not in s or face != "round" else jaw
    p = []
    # back hair / hood
    hc = s["hair_c"]
    if s["hair"] == "hood":
        p.append(f'<path d="M-92 -430 Q-104 -560 0 -600 Q104 -560 92 -430 Q60 -410 0 -412 Q-60 -410 -92 -430 Z" fill="{hc}"/>')
    if s["hair"] == "periwig":   # 1690s long curled wig (B-004): falls past the shoulders
        p.append(f'<path d="M-96 -470 Q-112 -600 0 -606 Q112 -600 96 -470 Q112 -400 92 -360 Q60 -346 40 -372 L-40 -372 Q-60 -346 -92 -360 Q-112 -400 -96 -470 Z" fill="{hc}"/>')
        for sd in (-1, 1):
            for yy in (-470, -430, -392):
                p.append(f'<path d="M{sd*96} {yy} Q{sd*112} {yy+18} {sd*94} {yy+34}" fill="none" stroke="{shade(hc, 0.8)}" stroke-width="5"/>')
    if s["hair"] in ("bun", "crown_long"):
        p.append(f'<path d="M-80 -470 Q-96 -590 0 -598 Q96 -590 80 -470 Q86 -400 60 -380 L-60 -380 Q-86 -400 -80 -470 Z" fill="{hc}"/>')
    # neck
    p.append(f'<path d="M-24 -440 L-26 -400 L26 -400 L24 -440 Z" fill="{shade(skin, 0.86)}"/>')
    # face: rounded top, squarer jaw for jaw>0
    jx = w - 10 * jaw
    p.append(f'<path d="M-{w} -520 Q-{w} -588 0 -590 Q{w} -588 {w} -520 L{w} -480 Q{jx} -430 0 -424 Q-{jx} -430 -{w} -480 Z" fill="{skin}"/>')
    # ear
    for sd in ((-1,) if view == "3q" else (-1, 1)):
        p.append(f'<path d="M{sd*(w-4)} -514 Q{sd*(w+18)} -514 {sd*(w+14)} -490 Q{sd*(w+8)} -478 {sd*(w-2)} -482" fill="{skin}"/>'
                 f'<path d="M{sd*(w+2)} -506 Q{sd*(w+10)} -500 {sd*(w+4)} -490" fill="none" stroke-width="4"/>')
    if s.get("stubble"):
        p.append(f'<path d="M-{w-4} -486 Q-{jx-6} -434 0 -430 Q{jx-6} -434 {w-4} -486 Q30 -458 0 -462 Q-30 -458 -{w-4} -486 Z" fill="{shade(skin, 0.8)}" stroke="none"/>')
    fi = len(p)
    # eyes (small, with lids)
    lid = e.get("lid", 0.45); lx, ly = e.get("look", (0, 0)); pr = 6.5 * e.get("pupil", 1.0)
    for i, cx in enumerate((-26, 26)):
        cy, rx, ry = -515, 13, 11
        if view == "3q" and i == 1:              # the eye on the turning side foreshortens
            rx = 10.0
        p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#FFFFFF" stroke-width="5"/>')
        ix, iy = cx + 4*lx, cy + 1 + 2*ly
        p.append(f'<circle cx="{ix}" cy="{iy}" r="{pr}" fill="{s.get("iris", "#5B3A29")}" stroke="none"/>'
                 f'<circle cx="{ix}" cy="{iy}" r="{pr*0.45:.1f}" fill="{INK}" stroke="none"/>'
                 f'<circle cx="{ix+2.5}" cy="{iy-2.5}" r="1.8" fill="#FFFFFF" stroke="none"/>')
        if lid > 0.01:
            ly0 = cy - ry - 2 + (2 * ry + 2) * lid
            p.append(f'<path d="M{cx-rx-3} {cy-ry-4} L{cx+rx+3} {cy-ry-4} L{cx+rx+3} {ly0} L{cx-rx-3} {ly0} Z" fill="{skin}" stroke="none"/>')
            p.append(f'<path d="M{cx-rx-1} {ly0} L{cx+rx+1} {ly0}" stroke-width="5"/>')
            p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke-width="5"/>')
        (di, do) = e["brow"][i]
        inner, outer = (cx + 12, cx - 16) if i == 0 else (cx - 12, cx + 16)
        p.append(f'<path d="M{outer} {-540 + do} L{inner} {-540 + di}" fill="none" stroke-width="9"/>')
    if s.get("glasses"):
        p.append('<rect x="-45" y="-532" width="38" height="32" rx="9" fill="none" stroke-width="6"/>'
                 '<rect x="7" y="-532" width="38" height="32" rx="9" fill="none" stroke-width="6"/><path d="M-7 -518 L7 -518" stroke-width="6"/>')
    # nose
    p.append(f'<path d="M0 -510 L7 -488 Q2 -482 -6 -484" fill="none" stroke-width="5"/>'
             f'<path d="M-9 -488 Q-12 -483 -7 -481" fill="none" stroke-width="4"/>'
             f'<path d="M1 -506 L6 -490 L1 -490 Z" fill="{shade(skin, 0.88)}" stroke="none"/>')
    # beard / moustache
    if s.get("beard"):
        b = s["beard"]
        beard_svg = f'<path d="M-{w} -486 Q-{jx} -412 0 -404 Q{jx} -412 {w} -486 Q40 -468 22 -470 Q0 -462 -22 -470 Q-40 -468 -{w} -486 Z" fill="{b}"/>'
        if view != "3q":
            p.append(beard_svg)
    if s.get("moustache"):
        p.append(f'<path d="M-26 -470 Q-12 -480 0 -472 Q12 -480 26 -470 Q12 -464 0 -468 Q-12 -464 -26 -470 Z" fill="{s["moustache"]}"/>')
    # mouth
    m = e["mouth"]
    M = {"flat": "M-14 -458 L14 -458", "flat_down": "M-14 -455 Q0 -460 14 -455", "smirk": "M-12 -458 Q8 -456 18 -466",
         "side": "M-6 -458 L16 -460", "grit": "M-16 -462 L16 -462 L14 -450 L-14 -450 Z",
         "smile": "M-15 -461 Q0 -449 15 -461"}
    if m == "o":
        p.append('<ellipse cx="0" cy="-456" rx="9" ry="12" fill="#6E2430" stroke-width="6"/>')
    elif m == "grit":
        p.append(f'<path d="{M[m]}" fill="#FFFFFF" stroke-width="6"/><path d="M-15 -456 L15 -456" stroke-width="3"/>')
    else:
        p.append(f'<path d="{M[m]}" fill="none" stroke-width="6"/>')
        if not (s.get("beard") or s.get("moustache")):
            p.append(f'<path d="M-9 -451 Q0 -446 9 -451" fill="none" stroke="{shade(skin, 0.78)}" stroke-width="5"/>')
    if view == "3q":
        bs = [beard_svg] if s.get("beard") else []
        p[fi:] = bs + [f'<g transform="translate(12,0)">' + "".join(p[fi:]) + '</g>']
    # front hair / hats
    h = s["hair"]
    if h == "curl":   # Wy: short brown hair + the question-mark curl
        p.append(f'<path d="M-{w} -528 Q-{w} -600 0 -600 Q{w} -600 {w} -528 Q40 -566 0 -566 Q-40 -566 -{w} -528 Z" fill="{hc}"/>')
        p.append(f'<path d="M-6 -600 Q-6 -650 26 -648 Q56 -644 46 -618 Q38 -600 18 -606" fill="none" stroke="{hc}" stroke-width="14"/>'
                 f'<path d="M-6 -600 Q-6 -650 26 -648 Q56 -644 46 -618 Q38 -600 18 -606" fill="none" stroke-width="4"/>')
    elif h == "short":
        p.append(f'<path d="M-{w} -522 Q-{w+4} -604 0 -602 Q{w+4} -604 {w} -522 Q50 -572 10 -568 Q-40 -572 -{w} -522 Z" fill="{hc}"/>')
    elif h == "tricorn":
        p.append(f'<path d="M-112 -556 Q0 -536 112 -556 Q86 -600 50 -598 Q30 -640 0 -640 Q-30 -640 -50 -598 Q-86 -600 -112 -556 Z" fill="{hc}"/>'
                 f'<path d="M-104 -560 Q0 -542 104 -560" fill="none" stroke="{s["top2"]}" stroke-width="7"/>')
    elif h == "bun":
        p.append(f'<path d="M-{w} -520 Q-{w} -604 0 -604 Q{w} -604 {w} -520 Q30 -566 -10 -560 Q-50 -556 -{w} -520 Z" fill="{hc}"/>'
                 f'<circle cx="0" cy="-616" r="26" fill="{hc}"/>')
    elif h == "hood":
        p.append(f'<path d="M-{w+6} -500 Q-{w+10} -606 0 -606 Q{w+10} -606 {w+6} -500 Q{w-4} -560 0 -568 Q-{w-4} -560 -{w+6} -500 Z" fill="{hc}"/>')
    elif h == "helmet":
        p.append(f'<path d="M-{w+12} -536 Q-{w+8} -626 0 -628 Q{w+8} -626 {w+12} -536 Z" fill="{hc}"/>'
                 f'<path d="M-{w+22} -536 L{w+22} -536" stroke-width="14"/><path d="M0 -628 L0 -540" stroke="{shade(hc, 0.75)}" stroke-width="10"/>')
    elif h == "crown_long":
        p.append(f'<path d="M-{w} -520 Q-{w} -606 0 -606 Q{w} -606 {w} -520 Q20 -576 0 -566 Q-20 -576 -{w} -520 Z" fill="{hc}"/>'
                 f'<path d="M-44 -592 L-50 -636 L-24 -612 L0 -646 L24 -612 L50 -636 L44 -592 Z" fill="{s["top2"]}"/>')
    elif h == "custodian":   # Victorian police helmet: tall dome, badge
        p.append(f'<path d="M-{w+8} -540 Q-{w+4} -600 -40 -650 Q0 -700 40 -650 Q{w+4} -600 {w+8} -540 Z" fill="{hc}"/>'
                 f'<path d="M-{w+18} -540 L{w+18} -540" stroke-width="12"/><circle cx="0" cy="-690" r="9" fill="#C9CED6"/>'
                 f'<path d="M0 -620 L12 -598 L0 -576 L-12 -598 Z" fill="#C9CED6" stroke-width="4"/>')
    elif h == "bald":       # bald crown with grey side hair
        for sd in (-1, 1):
            p.append(f'<path d="M{sd*w} -500 Q{sd*(w+6)} -560 {sd*(w-24)} -572 Q{sd*(w-14)} -540 {sd*(w-6)} -500 Z" fill="{hc}"/>')
        p.append(f'<path d="M-30 -578 Q0 -586 30 -578" fill="none" stroke="#FFFFFF" stroke-width="6" opacity="0.5"/>')
    elif h == "tophat":
        p.append(f'<path d="M-{w} -528 Q-{w+4} -600 0 -602 Q{w+4} -600 {w} -528 Q40 -566 0 -566 Q-40 -566 -{w} -528 Z" fill="#7A5236"/>'
                 f'<rect x="-60" y="-720" width="120" height="150" rx="8" fill="{hc}"/><path d="M-92 -570 L92 -570" stroke-width="16"/>'
                 f'<rect x="-60" y="-610" width="120" height="20" fill="#8E2430" stroke-width="5"/>')
    elif h == "periwig":
        p.append(f'<path d="M-{w+8} -500 Q-{w+12} -612 0 -612 Q{w+12} -612 {w+8} -500 Q{w-6} -572 0 -572 Q-{w-6} -572 -{w+8} -500 Z" fill="{hc}"/>'
                 f'<path d="M-40 -590 Q-30 -606 -14 -594 M8 -598 Q20 -612 34 -598" fill="none" stroke="{shade(hc, 0.8)}" stroke-width="5"/>')
    elif h == "fedora":     # 1920s hat with a band
        p.append(f'<path d="M-{w} -528 Q-{w+4} -590 0 -592 Q{w+4} -590 {w} -528 Q40 -560 0 -560 Q-40 -560 -{w} -528 Z" fill="#5B3A29"/>'
                 f'<path d="M-62 -584 Q-60 -654 -20 -646 Q0 -632 20 -646 Q60 -654 62 -584 Z" fill="{hc}"/>'
                 f'<rect x="-62" y="-600" width="124" height="18" fill="#22181B" stroke-width="4"/><path d="M-104 -582 Q0 -570 104 -582" stroke-width="14"/>')
    elif h == "hardhat":
        p.append(f'<path d="M-{w+10} -540 Q-{w+6} -640 0 -642 Q{w+6} -640 {w+10} -540 Z" fill="{hc}"/>'
                 f'<path d="M-{w+26} -540 L{w+26} -540" stroke-width="16"/><path d="M-{w+24} -540 L{w+24} -540" stroke="{hc}" stroke-width="8"/>'
                 f'<path d="M0 -640 L0 -548" stroke="{shade(hc, 0.8)}" stroke-width="12"/>')
    elif h == "chef":
        p.append(f'<path d="M-{w} -528 Q-{w+4} -590 0 -592 Q{w+4} -590 {w} -528 Q40 -560 0 -560 Q-40 -560 -{w} -528 Z" fill="{hc}"/>'
                 f'<path d="M-64 -572 L-64 -620 Q-100 -640 -80 -680 Q-60 -712 -20 -694 Q0 -730 30 -706 Q70 -716 82 -680 Q96 -640 64 -620 L64 -572 Z" fill="#FFFFFF"/>'
                 f'<path d="M-64 -596 L64 -596" stroke="#DCE6EA" stroke-width="6"/>')
    elif h == "flatcap":
        p.append(f'<path d="M-{w} -524 Q-{w+4} -590 0 -592 Q{w+4} -590 {w} -524 Q40 -556 0 -556 Q-40 -556 -{w} -524 Z" fill="#5B4636"/>'
                 f'<path d="M-{w+6} -548 Q-{w+2} -620 0 -618 Q{w+20} -616 {w+34} -560 Q20 -544 -{w+6} -548 Z" fill="{hc}"/>')
    if h in ("short", "curl", "bun", "crown_long"):
        dk = shade(hc, 0.72 if hc not in ("#22181B", "#1E1A24") else 1.6)
        p.append(f'<path d="M-30 -592 Q-20 -574 -36 -560 M6 -598 Q14 -580 2 -566 M36 -590 Q46 -574 36 -560" fill="none" stroke="{dk}" stroke-width="4"/>')
    return "".join(p)


HEAD_K = 0.8  # v2.1: head scaled about the neck so it is ~1/4 of body height (owner: "closer to human")


def _head_scaled(s, e, view="front"):
    return f'<g transform="translate(0,-404) scale({HEAD_K}) translate(0,404)">{_head(s, e, view)}</g>'


def _body(s):
    top, t2, lg, sh = s["top"], s["top2"], s["legs"], s["shoes"]
    fem = s.get("female")
    p = []
    # legs + shoes
    if not s.get("gown"):
        p.append(f'<path d="M-46 -210 L-50 -14 L-14 -14 L-6 -190 L6 -190 L14 -14 L50 -14 L46 -210 Z" fill="{lg}"/>')
        p.append(f'<path d="M-58 0 Q-60 -26 -30 -24 L-12 -24 L-12 0 Z" fill="{sh}"/><path d="M58 0 Q60 -26 30 -24 L12 -24 L12 0 Z" fill="{sh}"/>')
    # torso with shoulders (trapezoid), slightly narrower for female characters
    sw, hw = (82, 58) if fem else (92, 62)
    if s.get("gown"):
        p.append(f'<path d="M-{sw} -390 Q-{sw+6} -330 -{hw} -260 L-110 -8 Q0 6 110 -8 L{hw} -260 Q{sw+6} -330 {sw} -390 Q0 -408 -{sw} -390 Z" fill="{top}"/>')
        p.append(f'<path d="M-{hw} -262 Q0 -246 {hw} -262" fill="none" stroke="{t2}" stroke-width="12"/>')
    else:
        p.append(f'<path d="M-{sw} -390 Q-{sw+6} -330 -{hw} -200 L{hw} -200 Q{sw+6} -330 {sw} -390 Q0 -408 -{sw} -390 Z" fill="{top}"/>')
    if s.get("coat"):   # long open coat (captain, doctor)
        p.append(f'<path d="M-{sw} -390 Q-{sw+8} -260 -{hw+14} -120 L-14 -120 L-10 -392 Z" fill="{top}"/>'
                 f'<path d="M{sw} -390 Q{sw+8} -260 {hw+14} -120 L14 -120 L10 -392 Z" fill="{top}"/>'
                 f'<path d="M-10 -392 L0 -300 L10 -392 Z" fill="{t2}"/>')
    if s.get("hoodie"):
        p.append(f'<path d="M-50 -394 Q0 -360 50 -394" fill="none" stroke="{shade(top, 0.7)}" stroke-width="14"/>'
                 f'<path d="M-48 -260 L48 -260 L44 -216 L-44 -216 Z" fill="{shade(top, 0.85)}" stroke-width="6"/>')
    if s.get("apron"):
        p.append(f'<path d="M-46 -330 L46 -330 L54 -150 L-54 -150 Z" fill="{s["apron"]}" stroke-width="7"/>')
    if not (s.get("coat") or s.get("hoodie") or s.get("gown")):
        p.append(f'<path d="M-24 -398 L0 -360 L24 -398" fill="{t2}" stroke-width="6"/>')
        p.append(f'<path d="M-{hw} -214 L{hw} -214" stroke="{shade(lg, 0.7)}" stroke-width="14"/>')
    if s.get("buttons"):
        for yy in (-370, -330, -290, -250):
            p.append(f'<circle cx="0" cy="{yy}" r="7" fill="{t2}" stroke-width="3"/>')
    if s.get("badge"):
        p.append('<circle cx="44" cy="-330" r="17" fill="#FFC93C" stroke-width="6"/><path d="M36 -330 L42 -324 L53 -337" fill="none" stroke-width="6"/>')
    return "".join(p)


# arm poses (v2.2): elbow + hand offsets from the shoulder for the SCREEN-RIGHT arm (side +1); mirrored for side -1.
# Poses can be blended: pose = (name_a, name_b, u) gives a smooth in-between (char2/pose_at use this for gradual moves).
ARM = {
    "down":    ((14, 86), (20, 172)),
    "hold":    ((22, 92), (-12, 112)),
    "hip":     ((60, 84), (12, 146)),
    "point":   ((72, 22), (150, 2)),
    "up":      ((56, -60), (66, -176)),
    "wave":    ((70, 20), (78, -110)),
    "shrug":   ((64, 70), (118, 30)),
    "explain": ((40, 88), (104, 88)),
    "count":   ((44, 90), (36, -6)),
    "think":   ((40, 100), (-70, -26)),
    "reach_r": ((80, 34), (170, 39)),
    "reach_l": ((-80, 34), (-170, 39)),
}
PALM = {"wave", "shrug", "explain", "up"}          # open hand facing out


def _arm_pts(side, pose):
    if isinstance(pose, (tuple, list)):
        (ea, ha), (eb, hb) = ARM[pose[0]], ARM[pose[1]]
        u = pose[2]; u = u * u * (3 - 2 * u)
        e = (ea[0] + (eb[0] - ea[0]) * u, ea[1] + (eb[1] - ea[1]) * u); h = (ha[0] + (hb[0] - ha[0]) * u, ha[1] + (hb[1] - ha[1]) * u)
        name = pose[1] if u > 0.5 else pose[0]
    else:
        if pose == "reach_l" and side > 0:        # far arm crosses the body (same targets as v2.1)
            e, h = (-46, 124), (-232, 54)
        elif pose == "reach_r" and side < 0:
            e, h = (46, 124), (232, 54)
        else:
            e, h = ARM.get(pose, ARM["down"])
        name = pose
    if pose in ("reach_l", "reach_r") or (isinstance(pose, (tuple, list)) and set(pose[:2]) & {"reach_l", "reach_r"}):
        return (e[0], e[1]), (h[0], h[1]), name          # these are screen-space, not mirrored
    return (side * e[0], e[1]), (side * h[0], h[1]), name


def _arm(s, side, pose):
    """side -1 = screen left. Smooth bent sleeve (shoulder -> elbow -> wrist) + a hand turned along the forearm."""
    sx = side * (74 if s.get("female") else 82)
    sleeve, skin = s["top"], s["skin"]
    sy = -384
    (ex, ey), (hx, hy), name = _arm_pts(side, pose)
    ex, ey, hx, hy = sx + ex, sy + ey, sx + hx, sy + hy
    sx, sy = sx - side * 10, sy + 8                                    # sleeve starts inside the shoulder line (no bulge)
    cx, cy = 2 * ex - (sx + hx) / 2, 2 * ey - (sy + hy) / 2           # control point so the curve passes through the elbow
    path = f"M{sx} {sy} Q{cx:.1f} {cy:.1f} {hx:.1f} {hy:.1f}"
    W = 34
    p = [f'<path d="{path}" fill="none" stroke-width="{W + 2 * SW}"/>',
         f'<path d="{path}" fill="none" stroke="{sleeve}" stroke-width="{W}"/>']
    # forearm direction -> hand rotation (hand drawn pointing +y in local space)
    fx, fy = hx - ex, hy - ey
    ang = math.degrees(math.atan2(fy, fx)) - 90
    palm = name in PALM
    hand = (f'<path d="M-17 -4 Q-20 34 0 36 Q20 34 17 -4 Q0 -12 -17 -4 Z" fill="{skin}"/>'
            f'<path d="M{-side*15} 4 Q{-side*31} 8 {-side*23} 22" fill="{skin}" stroke-width="5"/>')
    hand += ('<path d="M-8 14 L-8 32 M0 15 L0 34 M8 14 L8 31" fill="none" stroke-width="3.5"/>' if not palm else
             f'<path d="M-6 16 Q0 22 6 16" fill="none" stroke="{shade(skin, 0.75)}" stroke-width="4"/>')
    if name == "count":
        hand += f'<path d="M-4 -2 L-6 -40 Q0 -48 6 -40 L6 -2 Z" fill="{skin}"/>'
    p.append(f'<g transform="translate({hx:.1f},{hy:.1f}) rotate({ang:.1f})">{hand}</g>')
    p.append(f'<path d="M{hx - 18:.1f} {hy:.1f} L{hx + 18:.1f} {hy:.1f}" transform="rotate({ang:.1f} {hx:.1f} {hy:.1f})" stroke="{shade(sleeve, 0.7)}" stroke-width="6"/>')
    return "".join(p), (hx, hy + 12)


def _prop(name, at):
    x, y = at
    P = {
        "spyglass": f'<rect x="{x-6}" y="{y-60}" width="22" height="80" rx="6" fill="#C9A23A" transform="rotate(-20 {x} {y})"/>'
                    f'<rect x="{x-9}" y="{y-66}" width="28" height="18" rx="5" fill="#7A5236" transform="rotate(-20 {x} {y})"/>',
        "clipboard": f'<rect x="{x-30}" y="{y-56}" width="60" height="78" rx="6" fill="#B07A4A"/>'
                     f'<rect x="{x-22}" y="{y-44}" width="44" height="58" fill="#FFFFFF" stroke-width="5"/>'
                     f'<path d="M{x-14} {y-30} L{x+14} {y-30} M{x-14} {y-16} L{x+10} {y-16} M{x-14} {y-2} L{x+12} {y-2}" stroke-width="4"/>',
        "shovel": f'<path d="M{x} {y-150} L{x} {y+150}" stroke="#7A5236" stroke-width="12"/><path d="M{x} {y-150} L{x} {y+150}" stroke-width="3"/>'
                  f'<path d="M{x-26} {y+150} L{x+26} {y+150} L{x+20} {y+210} Q{x} {y+226} {x-20} {y+210} Z" fill="#9AA3AD"/>',
        "spear": f'<path d="M{x} {y-260} L{x} {y+200}" stroke="#7A5236" stroke-width="10"/><path d="M{x} {y-260} L{x} {y+200}" stroke-width="3"/>'
                 f'<path d="M{x} {y-320} L{x+16} {y-262} L{x-16} {y-262} Z" fill="#C8CED6"/>',
        "scroll": f'<rect x="{x-38}" y="{y-14}" width="76" height="30" rx="6" fill="#F3E2BC"/>'
                  f'<circle cx="{x-38}" cy="{y+1}" r="15" fill="#E6CF9E"/><circle cx="{x+38}" cy="{y+1}" r="15" fill="#E6CF9E"/>',
        "phone": f'<rect x="{x-14}" y="{y-40}" width="28" height="50" rx="6" fill="#22181B"/><rect x="{x-9}" y="{y-34}" width="18" height="36" rx="3" fill="#7FC8E8" stroke="none"/>',
    }
    return P.get(name, "")


def figure_svg(cid, expr="deadpan", pose_l="down", pose_r="hold", prop=True, view="front"):
    """view "3q" = three-quarter turn to screen right (flip the drawing to face left): the far (screen-left) arm goes behind the body."""
    s = CAST[cid]; e = EXPR[expr]
    if not prop:
        s = dict(s, prop=None)
    al, _ = _arm(s, -1, pose_l)
    ar, hand = _arm(s, 1, pose_r)
    prop = _prop(s["prop"], hand) if s.get("prop") else ""
    back = prop if s.get("prop") in ("shovel", "spear") else ""
    front = "" if back else prop
    if view == "3q":                             # turned to screen right: the screen-right arm is the far arm (behind the body)
        return back + ar + front + f'<g transform="translate(5,0) scale(0.93,1)">{_body(s)}</g>' + _head_scaled(s, e, view) + al
    return back + _body(s) + al + _head_scaled(s, e) + ar + front


def png(svg_body, vb, scale=1.0, bg=None):
    x0, y0, w, h = vb
    rect = f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {w} {h}" width="{w}" height="{h}">{rect}'
           f'<g stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round">{svg_body}</g></svg>')
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), scale=scale))).convert("RGBA")


def model_sheet(out):
    from PIL import ImageDraw, ImageFont
    order = ["wy", "captain", "doctor", "worker", "guard", "noble", "modern"]
    cw, W = 300, 300 * 7
    sheet = Image.new("RGBA", (W, 1300), "#F3EBDD")
    d = ImageDraw.Draw(sheet)
    try:
        f = ImageFont.truetype("library/fonts/LilitaOne-Regular.ttf", 34); f2 = ImageFont.truetype("library/fonts/LilitaOne-Regular.ttf", 22)
    except OSError:
        f = f2 = ImageFont.load_default()
    d.text((24, 16), "TrueWhys cast v2.1 — sample sheet (owner feedback: fairer skin, closer to human)", fill="#22181B", font=f)
    for i, cid in enumerate(order):
        im = png(figure_svg(cid, "deadpan", "down", "hold"), (-150, -680, 300, 700), 1.0)
        sheet.alpha_composite(im, (i * cw, 60))
        d.text((i * cw + 20, 760), CAST[cid]["name"], fill="#22181B", font=f2)
    d.text((24, 800), "Expressions (deadpan default; emotion spikes on the key word)", fill="#22181B", font=f2)
    exprs = ["deadpan", "smug", "suspicious", "shocked", "bored", "angry"]
    for j, ex in enumerate(exprs):
        d.text((60 + j * 345, 840), ex, fill="#22181B", font=f2)
        for k, cid in enumerate(["captain", "doctor", "modern"]):
            im = png(_head(CAST[cid], EXPR[ex]), (-115, -660, 230, 250), 0.62)
            sheet.alpha_composite(im, (20 + j * 345 + (k % 3) * 108, 875 + (k % 2) * 0))
    # heights guide: Wy v1 vs v2 proportions note
    d.text((24, 1180), "v2.1: head ~1/4 of height, coloured eyes with lids + brows, shaped nose, ears, lips, varied face shapes, hair strands, fingers.",
           fill="#5B3A29", font=f2)
    d.text((24, 1220), "Role by hat + outfit + one prop. Thick ink outline, flat colours, our palette. Wy keeps his curl, coral shirt and yellow check badge.",
           fill="#5B3A29", font=f2)
    sheet.convert("RGB").save(out, quality=92)


if __name__ == "__main__":
    model_sheet(sys.argv[1] if len(sys.argv) > 1 else "library/cast/cast_v2_sheet.jpg")
