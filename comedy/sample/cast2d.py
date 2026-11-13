"""Comedy cast (original): Pip the sparrow and Snap the crocodile (in his mailbox disguise).
Vector SVG groups, pivot at the feet (0, 0), facing screen-right. Same ink style as lib/cast.py."""
import math

INK = "#2A1C1E"
SW = 9


def g(body, tx=0, ty=0, sx=1, sy=1, rot=0, extra=""):
    return f'<g transform="translate({tx:.2f} {ty:.2f}) rotate({rot:.2f}) scale({sx:.3f} {sy:.3f})" {extra}>{body}</g>'


# ------------------------------------------------------------------ shared parts
def eye(cx, cy, rx, ry, expr="open", look=(0, 0), lid="#FFCF33", blink=False):
    """expr: open | happy | half | wide | teary | squint"""
    if blink or expr == "closed":
        return f'<path d="M{cx-rx} {cy} Q{cx} {cy+ry*0.6} {cx+rx} {cy}" fill="none" stroke-width="8"/>'
    if expr == "happy":
        return f'<path d="M{cx-rx} {cy+4} Q{cx} {cy-ry*1.1} {cx+rx} {cy+4}" fill="none" stroke-width="9"/>'
    if expr == "wide":
        rx, ry = rx * 1.25, ry * 1.25
    px, py = cx + look[0] * rx * 0.38, cy + look[1] * ry * 0.3
    pr = min(rx, ry) * (0.42 if expr != "wide" else 0.3)
    s = (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#FFFFFF" stroke-width="7"/>'
         f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{pr:.1f}" fill="{INK}" stroke="none"/>'
         f'<circle cx="{px+pr*0.35:.1f}" cy="{py-pr*0.4:.1f}" r="{pr*0.35:.1f}" fill="#FFFFFF" stroke="none"/>')
    if expr == "teary":
        s += (f'<circle cx="{px-pr*0.3:.1f}" cy="{py+pr*0.35:.1f}" r="{pr*0.2:.1f}" fill="#FFFFFF" stroke="none"/>'
              f'<path d="M{cx-rx*0.9} {cy+ry*0.55} Q{cx} {cy+ry*0.95} {cx+rx*0.9} {cy+ry*0.55}" fill="#9FE3FF" fill-opacity="0.85" stroke="none"/>')
    if expr in ("half", "squint"):
        top = cy - ry - 3
        cut = cy - (ry * 0.05 if expr == "half" else -ry * 0.25)
        s += (f'<path d="M{cx-rx-4} {top} L{cx+rx+4} {top} L{cx+rx+4} {cut} L{cx-rx-4} {cut} Z" fill="{lid}" stroke="none"/>'
              f'<path d="M{cx-rx*0.95} {cut} L{cx+rx*0.95} {cut}" stroke-width="8"/>')
    return s


def cupcake(candle=False, flame=0.0):
    s = ('<path d="M-38 -10 L38 -10 L28 40 L-28 40 Z" fill="#5BC0EB"/>'
         '<path d="M-20 -8 L-14 38 M0 -8 L0 38 M20 -8 L14 38" stroke-width="5" stroke="#2E8DB8"/>'
         '<path d="M-46 -8 Q-56 -34 -30 -40 Q-30 -66 0 -64 Q30 -66 30 -40 Q56 -34 46 -8 Z" fill="#FF8FB1"/>'
         '<path d="M-24 -30 Q0 -22 24 -32" fill="none" stroke-width="5" stroke="#F06292"/>')
    if candle:
        s += ('<rect x="-6" y="-112" width="12" height="50" rx="4" fill="#FFF6D8" stroke-width="6"/>'
              '<path d="M-6 -100 L6 -92 M-6 -84 L6 -76" stroke="#FF6B5B" stroke-width="5"/>')
        if flame > 0:
            f = flame
            s += (f'<circle cx="0" cy="-130" r="{34*f:.1f}" fill="#FFE27A" fill-opacity="0.35" stroke="none"/>'
                  f'<path d="M0 {-112-40*f:.1f} Q{16*f:.1f} -124 0 -114 Q{-16*f:.1f} -124 0 {-112-40*f:.1f} Z" fill="#FF9A2E" stroke-width="5"/>'
                  f'<path d="M0 {-116-22*f:.1f} Q{7*f:.1f} -122 0 -117 Q{-7*f:.1f} -122 0 {-116-22*f:.1f} Z" fill="#FFF3A0" stroke="none"/>')
    else:
        s += '<circle cx="0" cy="-70" r="13" fill="#E53950"/><path d="M2 -82 Q8 -96 18 -98" fill="none" stroke-width="5"/>'
    return s


def envelope(open_=0.0):
    s = ('<rect x="-40" y="-26" width="80" height="52" rx="5" fill="#FFFDF5"/>'
         '<path d="M-40 -24 L0 6 L40 -24" fill="none" stroke-width="6"/>'
         '<circle cx="0" cy="4" r="9" fill="#FF6B5B" stroke-width="5"/>')
    return s


# ------------------------------------------------------------------ Pip
YEL, YEL_D, BELLY, ORANGE = "#FFCF33", "#F2A93B", "#FFF1B8", "#FF9A2E"


def pip(expr="open", look=(1, 0), blink=False, front=None, back=None, back_p=0.0, poof=0.0,
        beak="closed", flame=0.0, notes=0.0, sweat=False):
    """front: 'cupcake' | 'cupcake_candle' | None (held in front wing); back: 'envelope' (back wing reaching back by back_p)."""
    p = []
    # legs + feet
    for lx in (-26, 24):
        p.append(f'<path d="M{lx} -34 L{lx} -4 M{lx} -4 L{lx+18} 0 M{lx} -4 L{lx-12} 0" stroke="{ORANGE}" stroke-width="10" fill="none"/>')
    # back wing (reaching back with the envelope)
    if back:
        ex = -70 - 150 * back_p
        ey = -128 - 30 * back_p
        p.append(f'<path d="M-40 -150 Q{(ex-40)/2:.0f} {ey-40:.0f} {ex:.0f} {ey:.0f} Q{(ex-40)/2:.0f} {ey+30:.0f} -40 -100 Z" fill="{YEL_D}"/>')
        if back == "envelope":
            p.append(g(envelope(), ex - 18, ey, rot=-12))
    # tail feathers
    p.append(f'<path d="M-92 -110 L-150 -130 L-140 -100 L-160 -84 L-96 -84 Z" fill="{YEL_D}"/>')
    if poof > 0:
        # puffed-up feather ball (after the candle gust)
        r = 104 + 70 * poof
        pts = []
        n = 22
        for i in range(n * 2):
            a = math.pi * 2 * i / (n * 2)
            rr = r * (1.0 if i % 2 == 0 else 0.86)
            pts.append(f"{rr*math.cos(a):.1f} {-128 + rr*math.sin(a)*0.92:.1f}")
        p.append(f'<path d="M{" L".join(pts)} Z" fill="{YEL}"/>')
        for i in range(10):
            a = math.pi * 2 * i / 10 + 0.3
            x0, y0 = (r * 0.55) * math.cos(a), -128 + (r * 0.5) * math.sin(a)
            p.append(f'<path d="M{x0:.0f} {y0:.0f} q{12*math.cos(a):.0f} {12*math.sin(a):.0f} {24*math.cos(a+0.4):.0f} {24*math.sin(a+0.4):.0f}" fill="none" stroke-width="5" stroke="{YEL_D}"/>')
    else:
        p.append(f'<circle cx="0" cy="-128" r="104" fill="{YEL}"/>')
        p.append(f'<ellipse cx="26" cy="-98" rx="62" ry="56" fill="{BELLY}" stroke="none"/>')
        # tuft
        p.append(f'<path d="M-6 -228 Q-30 -280 -4 -268 Q4 -300 22 -266 Q48 -284 30 -230 Z" fill="{YEL}"/>')
    # eyes (3/4 view facing right)
    lid = YEL
    p.append(eye(14, -160, 24, 30, expr, look, lid, blink))
    p.append(eye(66, -154, 21, 27, expr, look, lid, blink))
    if expr == "squint":  # one-eye twitch
        p.append('<path d="M46 -196 L84 -186" stroke-width="8"/>')
    # cheek
    p.append('<ellipse cx="84" cy="-112" rx="15" ry="9" fill="#FF9EAA" stroke="none"/>')
    # beak
    if beak == "open":
        p.append(f'<path d="M78 -140 L136 -134 L84 -122 Z" fill="{ORANGE}"/><path d="M80 -118 L124 -110 L80 -104 Z" fill="{ORANGE}"/>')
    elif beak == "flat":
        p.append(f'<path d="M80 -138 L132 -124 L80 -112 Z" fill="{ORANGE}"/><path d="M80 -124 L128 -124" stroke-width="6"/>')
    else:
        p.append(f'<path d="M80 -142 L138 -124 L80 -108 Z" fill="{ORANGE}"/>')
    # front wing + held item
    if front:
        p.append(f'<path d="M-10 -120 Q60 -130 104 -86 Q70 -66 -6 -82 Z" fill="{YEL_D}"/>')
        p.append(g(cupcake(candle=front == "cupcake_candle", flame=flame), 124, -66, 0.95, 0.95))
    else:
        p.append(f'<path d="M-30 -130 Q10 -150 30 -100 Q0 -70 -34 -86 Z" fill="{YEL_D}"/>')
    if sweat:
        p.append('<path d="M-60 -250 Q-48 -226 -60 -216 Q-72 -226 -60 -250 Z" fill="#9FE3FF" stroke-width="6"/>')
    if notes > 0:  # humming notes floating up
        for i, (nx, ny) in enumerate(((70, -300), (130, -350))):
            k = (notes + i * 0.5) % 1.0
            op = math.sin(k * math.pi)
            p.append(g('<path d="M0 0 L0 -44 L26 -52 L26 -10" fill="none" stroke-width="7"/>'
                       '<ellipse cx="-8" cy="2" rx="12" ry="9" fill="#2A1C1E"/><ellipse cx="18" cy="-8" rx="12" ry="9" fill="#2A1C1E"/>',
                       nx + 20 * math.sin(k * 6), ny - 60 * k, 0.8, 0.8, extra=f'opacity="{op:.2f}"'))
    return "".join(p)


# ------------------------------------------------------------------ Snap (crocodile in a mailbox costume)
GREEN, GREEN_D, GREEN_L = "#6CC04A", "#4E9A34", "#B7E39A"
RED, RED_D, RED_L = "#E8433A", "#B8312B", "#FF7A6E"
PURPLE = "#7E4FC9"


def croc_eyes(raise_=1.0, look=(1, 0), expr="open", blink=False, y0=-548):
    """Two eye bumps peeking over the dome. raise_ 0 = hidden behind the dome, 1 = peeking, >1 = popped (take)."""
    out = []
    lift = 70 * raise_
    for cx in (-42, 46):
        cy = y0 - lift + 40
        out.append(f'<ellipse cx="{cx}" cy="{cy+18}" rx="44" ry="40" fill="{GREEN}"/>')
        rx, ry = (26, 30) if raise_ <= 1.05 else (26 + 10 * (raise_ - 1), 30 + 14 * (raise_ - 1))
        out.append(eye(cx + 2, cy + 4, rx, ry, expr, look, GREEN, blink))
    return "".join(out)


def croc_head(expr="happy", mouth=0.0, cheeks=0.0, look=(1, 0), hat=True, blink=False):
    """Croc head popping out of the costume. Pivot = neck (0,0). Facing right."""
    p = []
    puff = 1 + 0.35 * cheeks
    # snout
    sn = 250 if expr != "blow" else 210
    p.append(f'<path d="M-90 -40 Q-110 -170 0 -180 L{sn-20} -150 Q{sn+30} -140 {sn+20} -96 Q{sn+10} -60 {sn-30} -62 '
             f'L40 -60 Q-60 -40 -90 -40 Z" fill="{GREEN}" transform="scale({puff:.3f} 1)"/>')
    # lower jaw (opens with mouth)
    jaw = 40 * mouth
    p.append(f'<path d="M-60 -50 Q40 {-40+jaw:.0f} {sn-20} {-70+jaw*1.4:.0f} Q{sn} {-50+jaw*1.4:.0f} {sn-40} {-30+jaw*1.2:.0f} Q20 {-10+jaw:.0f} -60 -10 Z" fill="{GREEN_L}"/>')
    if mouth > 0.2:
        p.append(f'<path d="M30 -60 L{sn-30} -66 L{sn-40} {-62+jaw*1.2:.0f} L40 {-56+jaw:.0f} Z" fill="#B23A48"/>')
    # smile line + teeth
    if expr in ("happy", "teary", "sheepish") and mouth < 0.2:
        p.append(f'<path d="M20 -66 Q120 -40 {sn-20} -84" fill="none" stroke-width="8"/>')
        for i in range(6):
            tx = 50 + i * 30
            ty = -58 - i * 3
            p.append(f'<path d="M{tx} {ty} l10 14 l10 -16" fill="#FFFFFF" stroke-width="5"/>')
    if expr == "blow":
        p.append(f'<ellipse cx="{sn+18}" cy="-104" rx="14" ry="18" fill="#7A2230" stroke-width="7"/>')
    # nostrils
    p.append(f'<ellipse cx="{sn-10}" cy="-150" rx="9" ry="6" fill="{INK}" stroke="none"/><ellipse cx="{sn+12}" cy="-142" rx="8" ry="5" fill="{INK}" stroke="none"/>')
    # cheek blush
    p.append(f'<ellipse cx="40" cy="-82" rx="22" ry="12" fill="#FF9EAA" stroke="none"/>')
    # eye bumps
    e = {"happy": "happy", "teary": "teary", "sheepish": "half", "inhale": "closed", "blow": "closed", "chomp": "happy", "open": "open"}[expr]
    for cx in (-20, 70):
        p.append(f'<ellipse cx="{cx}" cy="-186" rx="44" ry="40" fill="{GREEN}"/>')
        p.append(eye(cx + 2, -196, 26, 30, e, look, GREEN, blink))
    if expr == "teary":
        for cx in (-20, 70):
            p.append(f'<path d="M{cx+10} -170 Q{cx+18} -120 {cx+6} -70" fill="none" stroke="#7FD4FF" stroke-width="12" stroke-linecap="round"/>')
    # back ridges
    for i in range(4):
        p.append(f'<path d="M{-90+i*30} -150 l14 -26 l14 24" fill="{GREEN_D}" stroke-width="6"/>')
    if hat:
        p.append(f'<g transform="translate(20 -228) rotate(-8)"><rect x="-64" y="-8" width="128" height="20" rx="8" fill="{PURPLE}"/>'
                 f'<rect x="-40" y="-92" width="80" height="88" rx="8" fill="{PURPLE}"/>'
                 f'<rect x="-40" y="-36" width="80" height="16" fill="#FFCF33" stroke-width="6"/></g>')
    return "".join(p)


def box_shape(with_dome=True):
    s = f'<rect x="-150" y="-470" width="300" height="384" rx="28" fill="{RED}"/>'
    if with_dome:
        s = f'<path d="M-150 -440 Q-150 -560 0 -560 Q150 -560 150 -440 Z" fill="{RED}"/>' + s
    # side shade + highlight
    s += f'<rect x="96" y="-462" width="44" height="368" rx="18" fill="{RED_D}" stroke="none" fill-opacity="0.55"/>'
    s += f'<rect x="-128" y="-450" width="18" height="300" rx="9" fill="{RED_L}" stroke="none" fill-opacity="0.6"/>'
    # envelope icon plate (no words)
    s += ('<rect x="-62" y="-300" width="124" height="80" rx="10" fill="#FFFDF5" stroke-width="7"/>'
          '<path d="M-62 -298 L0 -252 L62 -298" fill="none" stroke-width="7"/>')
    # base band
    s += f'<rect x="-158" y="-124" width="316" height="40" rx="12" fill="{RED_D}"/>'
    return s


def mailbox_snap(eyes=1.0, look=(1, 0), eye_expr="open", blink=False, jaw=0.0, legs=(0, 0), tail=0.0, tongue=0.0,
                 dome=1.0, dome_xy=(0, 0, 0), head=0.0, head_kw=None, claw_card=None, drool=0.0):
    """dome: 1 = on; 0 = popped (then dome_xy gives its flying offset + rotation). head: 0..1 how far the croc head has risen."""
    p = []
    # tail behind
    p.append(g(f'<path d="M10 10 Q-110 50 -250 100 Q-210 60 -120 0 Q-60 -40 0 -80 Z" fill="{GREEN}"/>'
               f'<path d="M-70 -8 l-4 -30 l-24 22 M-140 32 l-4 -26 l-22 20" fill="{GREEN_D}" stroke-width="6"/>',
               -130, -150, rot=tail))
    # legs (stubby croc legs instead of a post)
    for i, lx in enumerate((-78, 78)):
        lift = legs[i]
        p.append(f'<rect x="{lx-30}" y="{-104-lift}" width="60" height="{100}" rx="22" fill="{GREEN}"/>')
        p.append(f'<path d="M{lx-26} {-6-lift} l8 12 l8 -12 l8 12 l8 -12 l8 12 l8 -12" fill="#FFFFFF" stroke-width="5"/>')
    # head rising out of the open top (drawn before the box so the box hides the neck)
    if head > 0:
        hk = head_kw or {}
        p.append(g(croc_head(**hk), 10, -300 - 140 * head))
    hinge = (-150, -349)
    ang = -38 * jaw
    if jaw > 0.001:
        # mouth interior + teeth (between the two halves)
        mo = (f'<path d="M-150 -349 L150 -349 L{-150+300*math.cos(math.radians(ang)):.1f} {-349+300*math.sin(math.radians(ang)):.1f} Z" '
              f'fill="#7A2230"/>')
        p.append(mo)
        p.append(f'<path d="M-130 -349 Q0 -330 140 -349 Q0 -362 -130 -349 Z" fill="#FF7A8A" stroke="none"/>')
        if tongue > 0:
            pass
    # lower half (clip below the slot line)
    p.append('<defs><clipPath id="lo"><rect x="-400" y="-349" width="800" height="400"/></clipPath>'
             '<clipPath id="hi"><rect x="-400" y="-800" width="800" height="451"/></clipPath></defs>')
    p.append(f'<g clip-path="url(#lo)">{box_shape(dome >= 1)}</g>')
    if jaw > 0.001:
        for i in range(7):  # lower teeth
            tx = -120 + i * 40
            p.append(f'<path d="M{tx} -349 l14 -26 l14 26 Z" fill="#FFFFFF" stroke-width="5"/>')
    upper = f'<g clip-path="url(#hi)">{box_shape(dome >= 1)}</g>'
    if dome >= 1 and head <= 0:  # eyes peek over the dome and move with the top half
        upper = croc_eyes(eyes, look, eye_expr, blink) + upper
    if jaw > 0.001:
        teeth = "".join(f'<path d="M{-120+i*40} -349 l14 26 l14 -26 Z" fill="#FFFFFF" stroke-width="5"/>' for i in range(7))
        upper = teeth + upper
    # mail slot (closed look) sits on the seam
    slot = '' if jaw > 0.05 else '<rect x="-96" y="-362" width="192" height="26" rx="12" fill="#3A1A1E" stroke-width="7"/>'
    if tongue > 0:
        slot += f'<path d="M20 -342 Q{60+50*tongue:.0f} {-330+40*tongue:.0f} {90+30*tongue:.0f} {-344+20*tongue:.0f} Q70 -348 40 -344 Z" fill="#FF6F8A" stroke-width="6"/>'
    if drool > 0:
        slot += f'<path d="M110 -340 Q118 {-330+60*drool:.0f} 110 {-320+70*drool:.0f} Q102 {-330+60*drool:.0f} 110 -340 Z" fill="#BFEFFF" stroke-width="5"/>'
    p.append(f'<g transform="rotate({ang:.2f} {hinge[0]} {hinge[1]})">{upper}</g>')
    p.append(slot)
    if dome < 1:  # flying dome
        dx, dy, dr = dome_xy
        p.append(g(f'<path d="M-150 -440 Q-150 -560 0 -560 Q150 -560 150 -440 Q0 -430 -150 -440 Z" fill="{RED}"/>'
                   f'<path d="M-120 -470 Q-110 -540 -40 -548" fill="none" stroke="{RED_L}" stroke-width="12"/>', dx, dy, rot=dr))
    if claw_card is not None:
        p.append(claw_card)
    return "".join(p)
