"""Comedy sample 2 cast in the TrueWhys look (egg heads from lib/cast.py), all original:
Benny (a hungry jogger with a backpack full of bread) and the Goose. Vector SVG, pivot at the feet, facing right."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from cast import HEAD, eyes_svg, brows_svg, mouth_svg, CHEEK  # noqa: E402

INK = "#2A1C1E"
SW = 10
SKIN, HAIR, HOODIE, HOODIE_D, JEANS, SHOE, PACK = "#E9B48C", "#3B2416", "#F2B33D", "#D18F22", "#2E4A7A", "#E8433A", "#2E8B8B"
BREAD, BREAD_D = "#E0A458", "#B8743A"


def g(body, tx=0, ty=0, sx=1, sy=1, rot=0, extra=""):
    return f'<g transform="translate({tx:.2f} {ty:.2f}) rotate({rot:.2f}) scale({sx:.3f} {sy:.3f})" {extra}>{body}</g>'


def limb(x, y, a1, l1, a2, l2, width, color):
    r1, r2 = math.radians(a1), math.radians(a2)
    kx, ky = x + l1 * math.sin(r1), y + l1 * math.cos(r1)
    ex, ey = kx + l2 * math.sin(r2), ky + l2 * math.cos(r2)
    d = f"M{x:.1f} {y:.1f} L{kx:.1f} {ky:.1f} L{ex:.1f} {ey:.1f}"
    s = (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{width+2*SW}" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')
    return s, (ex, ey)


def baguette(rot=0, x=0, y=0, length=200, bite=0.0):
    L = length * (1 - bite)
    s = (f'<rect x="{-L/2:.0f}" y="-22" width="{L:.0f}" height="44" rx="22" fill="{BREAD}" stroke-width="8"/>'
         + "".join(f'<path d="M{-L/2+30+i*(L-50)/3:.0f} -12 l26 22" fill="none" stroke="{BREAD_D}" stroke-width="7"/>' for i in range(3)))
    return g(s, x, y, rot=rot)


def phone_small(glow=True, w=56, h=96):
    s = f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="10" fill="#1F1B24" stroke-width="7"/>'
    s += f'<rect x="{-w/2+7}" y="{-h/2+8}" width="{w-14}" height="{h-18}" rx="5" fill="{"#BFF3FF" if glow else "#3A3550"}" stroke="none"/>'
    return s


# ------------------------------------------------------------------ Benny
def benny_head(expr="neutral", mouth="closed", eyes="open", look=(0, 0), hair_up=0.0, sweat=False):
    p = [f'<path d="{HEAD}" fill="{SKIN}"/>',
         '<path d="M-80 -232 Q-50 -256 -10 -260" fill="none" stroke="#FFFFFF" stroke-opacity="0.45" stroke-width="12"/>',
         f'<ellipse cx="-104" cy="-80" rx="26" ry="16" fill="{CHEEK}" opacity="0.8" stroke="none"/>'
         f'<ellipse cx="106" cy="-80" rx="26" ry="16" fill="{CHEEK}" opacity="0.8" stroke="none"/>',
         eyes_svg(expr, eyes, look, SKIN), brows_svg(expr), mouth_svg(expr, mouth)]
    # messy hair; spikes shoot up in the "take"
    u = 1 + 1.6 * hair_up
    p.append(f'<path d="M-152 -168 C-160 -300 150 -312 152 -168 Q126 -240 70 -238 L{86} {-238-34*u:.0f} L34 -244 L{30} {-244-46*u:.0f} '
             f'L-10 -246 L{-28} {-246-44*u:.0f} L-56 -240 L{-90} {-236-36*u:.0f} L-100 -230 Q-136 -222 -152 -168 Z" fill="{HAIR}"/>')
    if sweat:
        p.append('<path d="M150 -250 Q166 -214 150 -200 Q134 -214 150 -250 Z" fill="#9FE3FF" stroke-width="7"/>')
    return "".join(p)


def benny(legs=(10, 10, -10, 10), arms=(-10, 20, 10, 20), lean=0, bob=0, head=None, hold=None, breads=4,
          head_tilt=0, item_rot=0):
    """legs = (hipBack, kneeBack, hipFront, kneeFront) degrees (0 = straight down, + = forward);
    arms = (shoulderBack, elbowBack, shoulderFront, elbowFront). hold: 'phone' | 'baguette' | None."""
    head = head or {}
    p = []
    hb, kb, hf, kf = legs
    # back leg
    s, (ex, ey) = limb(-34, -96 + bob, hb, 52, hb - kb, 50, 46, shade_hex(JEANS, 0.8)); p.append(s)
    p.append(g(f'<path d="M-24 6 Q-26 -26 10 -24 Q46 -20 50 6 Z" fill="{shade_hex(SHOE,0.8)}"/>', ex, ey - 4, rot=-(hb - kb) * 0.4))
    upper = []
    # back arm (behind body)
    sb, eb, sf, ef = arms
    s, _ = limb(-92, -222, sb, 70, sb + eb, 64, 40, HOODIE_D); upper.append(s)
    # backpack + bread
    pk = []
    for i in range(breads):
        pk.append(baguette(-70 + i * 14, -132 + i * 10, -262 - (i % 2) * 10, 170))
    pk.append(f'<rect x="-178" y="-236" width="92" height="140" rx="26" fill="{PACK}"/>'
              f'<rect x="-170" y="-170" width="76" height="46" rx="12" fill="{shade_hex(PACK,0.8)}" stroke-width="7"/>')
    upper.append("".join(pk))
    # torso (hoodie)
    upper.append(f'<path d="M-100 -238 Q-136 -170 -118 -90 Q0 -64 118 -90 Q136 -170 100 -238 Q0 -262 -100 -238 Z" fill="{HOODIE}"/>'
                 f'<path d="M-56 -150 L56 -150 L66 -100 L-66 -100 Z" fill="{HOODIE_D}" stroke-width="7"/>'
                 f'<path d="M-84 -236 L-100 -100" fill="none" stroke="{shade_hex(PACK,0.7)}" stroke-width="16"/>'
                 f'<path d="M-20 -238 L-24 -190 M20 -238 L24 -190" fill="none" stroke-width="6"/>'
                 f'<path d="M-70 -246 Q0 -200 70 -246 Q30 -268 0 -264 Q-30 -268 -70 -246 Z" fill="{HOODIE_D}"/>')
    # head
    upper.append(g(benny_head(**head), 0, -226, rot=head_tilt))
    # front arm + held item
    s, (hx, hy) = limb(92, -222, sf, 70, sf + ef, 64, 40, HOODIE); upper.append(s)
    if hold == "phone":
        upper.append(g(phone_small(), hx + 6, hy - 40, rot=item_rot))
    elif hold == "baguette":
        upper.append(baguette(item_rot, hx, hy, 190))
    upper.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="27" fill="{SKIN}"/>')
    p.append(g("".join(upper), 0, bob, rot=lean, extra='transform-origin="0 -96"') if False else
             f'<g transform="translate(0 {bob:.1f}) rotate({lean:.1f} 0 -96)">{"".join(upper)}</g>')
    # front leg (in front of body)
    s, (ex, ey) = limb(34, -96 + bob, hf, 52, hf - kf, 50, 46, JEANS); p.insert(2, s)
    p.insert(3, g(f'<path d="M-24 6 Q-26 -26 10 -24 Q46 -20 50 6 Z" fill="{SHOE}"/>', ex, ey - 4, rot=-(hf - kf) * 0.4))
    return "".join(p)


def shade_hex(hexc, f):
    h = hexc.lstrip("#")
    r, gg, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"#{int(r*f):02X}{int(gg*f):02X}{int(b*f):02X}"


def run_pose(ph, speed=1.0, panic=True):
    s = math.sin(2 * math.pi * ph)
    c = math.cos(2 * math.pi * ph)
    A = 42 * speed
    legs = (A * s, 75 * max(0, -c) * speed + 10, -A * s, 75 * max(0, c) * speed + 10)
    arms = (-55 * s * speed, 85, 55 * s * speed, 85) if not panic else (-70 * s - 20, 40, 160 + 15 * s, 30)
    bob = -16 * abs(math.sin(2 * math.pi * ph))
    return legs, arms, bob


def walk_pose(ph):
    s = math.sin(2 * math.pi * ph); c = math.cos(2 * math.pi * ph)
    legs = (22 * s, 30 * max(0, -c) + 6, -22 * s, 30 * max(0, c) + 6)
    arms = (-25 * s, 20, 25 * s, 20)
    return legs, arms, -6 * abs(s)


# ------------------------------------------------------------------ Goose
WHITE, WING, ORANGE = "#F7F5EE", "#D5D6CE", "#FF9A2E"


def goose_eyes(expr, look, nx, ny):
    out = []
    for cx, cy in ((92 + nx, -412 + ny), (136 + nx, -410 + ny)):
        if expr in ("happy", "munch"):
            out.append(f'<path d="M{cx-15} {cy+4} Q{cx} {cy-16} {cx+15} {cy+4}" fill="none" stroke-width="8"/>')
            continue
        r = 1.25 if expr == "surprised" else 1.0
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{17*r}" ry="{22*r}" fill="#FFFFFF" stroke-width="7"/>')
        px, py = cx + 6 * look[0], cy + 5 * look[1]
        pr = 6 if expr in ("angry", "evil") else 9
        out.append(f'<circle cx="{px}" cy="{py}" r="{pr}" fill="{INK}" stroke="none"/>')
        if expr == "evil":
            out.append(f'<path d="M{cx-19} {cy-24} L{cx+19} {cy-24} L{cx+19} {cy-4} L{cx-19} {cy-4} Z" fill="{WHITE}" stroke="none"/>'
                       f'<path d="M{cx-17} {cy-4} L{cx+17} {cy-4}" stroke-width="7"/>')
    if expr in ("angry", "evil"):
        out.append(f'<path d="M{72+nx} {-446+ny} L{110+nx} {-430+ny}" stroke-width="10"/>'
                   f'<path d="M{122+nx} {-430+ny} L{158+nx} {-448+ny}" stroke-width="10"/>')
    if expr == "surprised":
        out.append(f'<path d="M{74+nx} {-448+ny} Q{92+nx} {-462+ny} {110+nx} {-448+ny}" fill="none" stroke-width="8"/>'
                   f'<path d="M{120+nx} {-448+ny} Q{138+nx} {-462+ny} {156+nx} {-448+ny}" fill="none" stroke-width="8"/>')
    return "".join(out)


def goose(ph=None, flap=0.0, nx=0, ny=0, beak=0.0, expr="angry", look=(1, 0), phone=False, bread=None, smirk=False,
          lean=0):
    """ph: run phase (None = standing). flap: wing raise (deg). bread: 0..1 bitten fraction of a baguette in the beak."""
    p = []
    # legs
    if ph is None:
        lg = ((-10, 0), (40, 0))
        bob = 0
    else:
        s = math.sin(2 * math.pi * ph)
        lg = ((-10 + 40 * s, -18 * max(0, s)), (40 - 40 * s, -18 * max(0, -s)))
        bob = -10 * abs(s)
    for (fx, fy), hx in zip(lg, (-20, 30)):
        p.append(f'<path d="M{hx} -90 L{fx+5:.0f} {fy-6:.0f}" fill="none" stroke="{INK}" stroke-width="{14+2*SW}" stroke-linecap="round"/>'
                 f'<path d="M{hx} -90 L{fx+5:.0f} {fy-6:.0f}" fill="none" stroke="{ORANGE}" stroke-width="14" stroke-linecap="round"/>'
                 f'<path d="M{fx-14:.0f} {fy:.0f} L{fx+44:.0f} {fy:.0f} L{fx+8:.0f} {fy-20:.0f} Z" fill="{ORANGE}" stroke-width="7"/>')
    b = []
    # neck (thick stroke, behind the body) + head
    nd = f"M50 -200 Q{80+nx*0.4:.0f} {-300+ny*0.4:.0f} {104+nx:.0f} {-370+ny:.0f}"
    b.append(f'<path d="{nd}" fill="none" stroke="{INK}" stroke-width="{66+2*SW}" stroke-linecap="round"/>'
             f'<path d="{nd}" fill="none" stroke="{WHITE}" stroke-width="66" stroke-linecap="round"/>')
    # tail + body
    b.append(f'<path d="M-160 -196 L-222 -236 L-196 -186 L-226 -166 L-166 -160 Z" fill="{WHITE}"/>')
    b.append(f'<path d="M-170 -190 Q-150 -256 -40 -254 Q70 -252 110 -190 Q140 -118 70 -90 Q0 -72 -90 -88 Q-166 -108 -170 -190 Z" fill="{WHITE}"/>')
    b.append(f'<path d="M-150 -170 Q-60 -110 60 -150" fill="none" stroke="{WING}" stroke-width="7"/>')
    b.append(f'<path d="M{70+nx*0.5:.0f} {-300+ny*0.5:.0f} Q{90+nx*0.8:.0f} {-350+ny*0.8:.0f} {104+nx:.0f} {-370+ny:.0f}" fill="none" stroke="{WHITE}" stroke-width="66" stroke-linecap="round"/>')
    b.append(f'<ellipse cx="{112+nx}" cy="{-404+ny}" rx="64" ry="58" fill="{WHITE}"/>')
    # beak
    bx, by = 162 + nx, -396 + ny
    if bread is not None:
        b.append(baguette(-8, bx + 70, by + 8, 200, bread))
    b.append(g(f'<path d="M0 6 L80 2 L0 26 Z" fill="{ORANGE}" stroke-width="7"/>', bx, by, rot=26 * beak))
    upper = f'<path d="M-6 -28 Q50 -20 96 2 L0 8 Z" fill="{ORANGE}" stroke-width="7"/>'
    if smirk:
        upper += '<path d="M10 2 Q36 14 60 0" fill="none" stroke-width="5"/>'
    b.append(g(upper, bx, by))
    b.append(f'<circle cx="{bx-2}" cy="{by-24}" r="13" fill="{ORANGE}" stroke-width="6"/>')
    b.append(goose_eyes(expr, look, nx, ny))
    # wing (front) + phone
    if phone:
        b.append(f'<path d="M-120 -200 Q-10 -268 112 -268 Q146 -254 132 -226 Q40 -206 -110 -150 Z" fill="{WING}"/>')
        b.append(g(phone_small(True, 64, 108), 160, -262, rot=-10))
        b.append(f'<path d="M110 -246 Q150 -250 150 -226 Q140 -206 112 -210 Z" fill="{WING}"/>')
    else:
        b.append(g(f'<path d="M0 0 Q-80 -50 -170 -10 Q-130 30 -40 40 Q-10 30 0 0 Z" fill="{WING}"/>'
                   f'<path d="M-150 0 L-100 8 M-130 18 L-80 22" fill="none" stroke-width="6"/>', 40, -196, rot=-flap))
    p.append(f'<g transform="translate(0 {bob:.1f}) rotate({lean:.1f} 0 -90)">{"".join(b)}</g>')
    return "".join(p)
