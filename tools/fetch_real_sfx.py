"""Download REAL recorded sound effects + ambiences (Freesound, CC0 only) into library/sfx/real/<category>/<name>.ogg.
/opt/c3d/bin/python tools/fetch_real_sfx.py [name ...]
- API key from FREESOUND_API_KEY (sent only to freesound.org, never printed).
- Picks the best-rated, most-downloaded CC0 result that is not synthesised (skips tags/names like synth, 8bit, game, cartoon).
- Processing: 48 kHz, trim silence, SFX peak -1 dBFS (max 6 s), ambiences RMS -26 dBFS, 20-60 s, seamless loop crossfade.
- Records library/sfx/real/credits.json (+ credits.md is rebuilt by tools/real_audio_credits.py).
Re-running skips files that exist (no repeated downloads)."""
import os, sys, json, time, math, re, subprocess, urllib.request, urllib.parse, tempfile
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "library/sfx/real"
CRED = OUT / "credits.json"
SR = 48000
BAD = re.compile(r"synth|8.?bit|chiptune|retro game|video ?game|cartoon|arcade|beep|laser|generated|procedural|sci.?fi|zap|glitch|"
                 r"music|melody|loop.?beat|voice|speech|talking|scream|laugh|moan|orgasm|asmr|stinger|stab|trailer|cinematic|designed", re.I)

# name: (category, query, kind)  kind: s = short sfx, a = ambience bed
WANT = {
    # ---- foley: hands / desk / paper / cloth
    "click_mouse": ("foley", "computer mouse click", "s"), "click_pen": ("foley", "ballpoint pen click", "s"),
    "switch_light": ("foley", "light switch click", "s"), "tap_table": ("foley", "finger tap wooden table", "s"),
    "tap_glass": ("foley", "tapping glass finger", "s"), "knock_door": ("foley", "knock wooden door", "s"),
    "paper_rustle": ("foley", "paper rustle handling", "s"), "paper_crumple": ("foley", "paper crumple ball", "s"),
    "paper_tear": ("foley", "paper tear rip", "s"), "page_flip": ("foley", "book page turn", "s"),
    "book_close": ("foley", "book close slam", "s"), "cloth_rustle": ("foley", "clothes rustle movement", "s"),
    "cloth_flap": ("foley", "cloth flap sheet shake", "s"), "zipper": ("foley", "zipper jacket", "s"),
    "hand_clap": ("foley", "single hand clap", "s"), "finger_snap": ("foley", "finger snap", "s"),
    "scissors": ("foley", "scissors cutting paper", "s"), "tape_roll": ("foley", "packing tape pull", "s"),
    "cardboard_box": ("foley", "cardboard box handling", "s"), "chair_creak": ("foley", "wooden chair creak", "s"),
    "chair_slide": ("foley", "chair drag floor", "s"), "keyboard_typing": ("foley", "keyboard typing", "s"),
    "pencil_writing": ("foley", "pencil writing paper", "s"), "chalk_board": ("foley", "chalk writing blackboard", "s"),
    "rope_stretch": ("foley", "rope creak stretch", "s"), "rubber_band": ("foley", "rubber band snap", "s"),
    # ---- footsteps on several floors
    "steps_wood": ("footsteps", "footsteps wooden floor", "s"), "steps_concrete": ("footsteps", "footsteps concrete", "s"),
    "steps_gravel": ("footsteps", "footsteps gravel", "s"), "steps_grass": ("footsteps", "footsteps grass", "s"),
    "steps_tile": ("footsteps", "footsteps tiles heels", "s"), "steps_snow": ("footsteps", "footsteps snow crunch", "s"),
    "steps_stairs": ("footsteps", "footsteps stairs wooden", "s"), "steps_run": ("footsteps", "running footsteps", "s"),
    # ---- doors, drawers
    "door_open": ("doors", "door open interior", "s"), "door_close": ("doors", "door close interior", "s"),
    "door_creak": ("doors", "door creak slow", "s"), "door_slam": ("doors", "door slam", "s"),
    "drawer_open": ("doors", "drawer open wooden", "s"), "cupboard": ("doors", "cupboard door open close", "s"),
    "gate_metal": ("doors", "metal gate creak", "s"),
    # ---- glass, metal, plastic, wood
    "glass_clink": ("materials", "glass clink cheers", "s"), "glass_set_down": ("materials", "glass put down table", "s"),
    "glass_break": ("materials", "glass break smash", "s"), "metal_clang": ("materials", "metal clang hit", "s"),
    "metal_small": ("materials", "small metal object drop", "s"), "metal_scrape": ("materials", "metal scrape", "s"),
    "plastic_crinkle": ("materials", "plastic crinkle", "s"), "plastic_tap": ("materials", "plastic tap hit", "s"),
    "plastic_bag": ("materials", "plastic bag rustle", "s"), "wood_thud": ("materials", "wood thud knock", "s"),
    "wood_creak": ("materials", "wood creak", "s"), "wood_break": ("materials", "wood stick snap break", "s"),
    "stone_drop": ("materials", "stone rock drop", "s"),
    # ---- liquids
    "pour_water": ("liquids", "pouring water glass", "s"), "splash": ("liquids", "water splash", "s"),
    "drip": ("liquids", "water drip single drop", "s"), "bubbles_water": ("liquids", "water bubbles underwater blowing", "s"),
    "gulp": ("liquids", "gulp drink swallow", "s"), "fizz": ("liquids", "soda fizz carbonated", "s"),
    "boil": ("liquids", "boiling water pot", "s"), "sink_tap": ("liquids", "kitchen tap running water", "s"),
    # ---- pops, impacts
    "pop_cork": ("impacts", "cork pop bottle", "s"), "pop_balloon": ("impacts", "balloon pop", "s"),
    "pop_mouth": ("impacts", "mouth pop", "s"), "impact_soft": ("impacts", "soft impact thud body pillow", "s"),
    "impact_hard": ("impacts", "hard impact hit heavy", "s"), "box_drop": ("impacts", "box drop floor", "s"),
    "body_fall": ("impacts", "body fall floor", "s"), "punch_bag": ("impacts", "punching bag hit", "s"),
    "ball_bounce": ("impacts", "ball bounce", "s"), "slap_table": ("impacts", "hand slap table", "s"),
    # ---- real air movement
    "whoosh_stick": ("whooshes", "stick swish air", "s"), "whoosh_cloth": ("whooshes", "cloth whoosh swing", "s"),
    "whoosh_hand": ("whooshes", "hand swipe whoosh", "s"), "whoosh_fast": ("whooshes", "whoosh pass by air", "s"),
    "whoosh_rope": ("whooshes", "rope swing whoosh", "s"), "whoosh_paper": ("whooshes", "paper whoosh throw", "s"),
    # ---- everyday objects
    "bubble_wrap": ("objects", "bubble wrap pop", "s"), "kettle_boil": ("objects", "kettle boiling click", "s"),
    "kettle_whistle": ("objects", "kettle whistle", "s"), "microwave": ("objects", "microwave oven", "s"),
    "fridge_open": ("objects", "fridge door open", "s"), "cutlery": ("objects", "cutlery silverware", "s"),
    "plate_set": ("objects", "plate put down ceramic", "s"), "sizzle": ("objects", "frying pan sizzle", "s"),
    "toaster": ("objects", "toaster pop", "s"), "chop_knife": ("objects", "knife chopping vegetables board", "s"),
    "can_open": ("objects", "soda can open", "s"), "bottle_open": ("objects", "bottle cap open", "s"),
    "wrapper": ("objects", "candy wrapper crinkle", "s"), "phone_vibrate": ("objects", "phone vibrate table", "s"),
    "camera_shutter": ("objects", "camera shutter mechanical", "s"), "keys_jingle": ("objects", "keys jingle", "s"),
    "coin_drop": ("objects", "coin drop table", "s"), "coins_handful": ("objects", "coins handful", "s"),
    "clock_tick": ("objects", "clock ticking", "s"), "alarm_bell": ("objects", "alarm clock bell mechanical", "s"),
    "doorbell": ("objects", "doorbell ding dong", "s"), "cash_register": ("objects", "cash register", "s"),
    "printer": ("objects", "printer printing", "s"), "vacuum": ("objects", "vacuum cleaner", "s"),
    "hair_dryer": ("objects", "hair dryer", "s"), "washing_machine": ("objects", "washing machine", "s"),
    "spray_bottle": ("objects", "spray bottle", "s"), "ice_cubes": ("objects", "ice cubes glass", "s"),
    "bike_bell": ("objects", "bicycle bell", "s"), "umbrella": ("objects", "umbrella open", "s"),
    "typewriter": ("objects", "typewriter typing", "s"), "sewing_machine": ("objects", "sewing machine", "s"),
    "lighter": ("objects", "lighter flick", "s"), "match_strike": ("objects", "match strike", "s"),
    "scrape_ice": ("objects", "ice scraper windshield", "s"), "brush_teeth": ("objects", "brushing teeth", "s"),
    "elevator_ding": ("objects", "elevator bell ding", "s"), "shopping_cart": ("objects", "shopping cart", "s"),
    "drill": ("objects", "electric drill", "s"), "hammer_nail": ("objects", "hammer nail wood", "s"),
    "saw_hand": ("objects", "hand saw wood", "s"), "lightbulb_buzz": ("objects", "light bulb hum buzz", "s"),
    "fan": ("objects", "electric fan", "s"), "bell_small": ("objects", "small hand bell", "s"),
    # ---- vehicles
    "car_door": ("vehicles", "car door close", "s"), "car_start": ("vehicles", "car engine start", "s"),
    "car_pass": ("vehicles", "car pass by", "s"), "car_horn": ("vehicles", "car horn", "s"),
    "car_idle": ("vehicles", "car engine idle", "s"), "truck_pass": ("vehicles", "truck pass by", "s"),
    "bus_brakes": ("vehicles", "bus brakes", "s"), "train_pass": ("vehicles", "train passing", "s"),
    "plane_flyover": ("vehicles", "airplane fly over", "s"), "bicycle": ("vehicles", "bicycle riding", "s"),
    # ---- animals (real)
    "dog_bark": ("animals", "dog bark single", "s"), "cat_meow": ("animals", "cat meow", "s"),
    "birds_chirp": ("animals", "bird chirp", "s"), "cat_purr": ("animals", "cat purr", "s"),
    # ---- ambience beds
    "amb_room_quiet": ("ambience", "room tone quiet", "a"), "amb_living_room": ("ambience", "living room ambience", "a"),
    "amb_office": ("ambience", "office ambience", "a"), "amb_kitchen": ("ambience", "kitchen ambience", "a"),
    "amb_cafe": ("ambience", "cafe ambience", "a"), "amb_restaurant": ("ambience", "restaurant ambience", "a"),
    "amb_street": ("ambience", "street traffic ambience", "a"), "amb_city": ("ambience", "city ambience", "a"),
    "amb_park": ("ambience", "park ambience birds", "a"), "amb_rain_light": ("ambience", "light rain", "a"),
    "amb_rain_window": ("ambience", "rain on window", "a"), "amb_wind": ("ambience", "wind outdoor", "a"),
    "amb_crowd": ("ambience", "crowd murmur walla", "a"), "amb_school": ("ambience", "school hallway ambience", "a"),
    "amb_classroom": ("ambience", "classroom ambience", "a"), "amb_workshop": ("ambience", "workshop ambience", "a"),
    "amb_factory": ("ambience", "factory ambience machines", "a"), "amb_forest": ("ambience", "forest ambience", "a"),
    "amb_beach": ("ambience", "beach waves", "a"), "amb_night": ("ambience", "night crickets", "a"),
    "amb_airport": ("ambience", "airport terminal ambience", "a"), "amb_train": ("ambience", "train interior", "a"),
    "amb_car_inside": ("ambience", "car interior driving", "a"), "amb_supermarket": ("ambience", "supermarket ambience", "a"),
    "amb_playground": ("ambience", "playground children distant", "a"), "amb_hospital": ("ambience", "hospital ambience", "a"),
    "amb_library": ("ambience", "library ambience quiet", "a"), "amb_garden": ("ambience", "garden morning birds", "a"),
    "amb_winter": ("ambience", "winter wind snow", "a"), "amb_thunder": ("ambience", "thunderstorm", "a"),
    "amb_lab": ("ambience", "laboratory ambience hum", "a"), "amb_garage": ("ambience", "garage ambience", "a"),
    "amb_suburb": ("ambience", "suburban ambience", "a"), "amb_market": ("ambience", "outdoor market ambience", "a"),
}

# second-try queries when the first finds no clean CC0 recording
ALT = {"cloth_flap": "flapping fabric", "impact_soft": "soft thud", "whoosh_hand": "swish arm movement", "whoosh_fast": "swoosh fast",
       "whoosh_paper": "throwing paper", "alarm_bell": "alarm clock ringing", "scrape_ice": "scraping ice", "amb_rain_window": "rain window",
       "amb_lab": "lab room tone hum", "impact_hard": "heavy thud", "tape_roll": "duct tape pull",
       "rubber_band": "rubber band twang", "wood_thud": "wooden block hit", "amb_airport": "airport terminal", "metal_clang": "metal pipe hit",
       "bus_brakes": "bus air brakes", "rope_stretch": "rope tension creak", "cloth_rustle": "fabric rustle", "amb_market": "market ambience"}


def api(url, key):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": "Token " + key}), timeout=40))


def decode(path):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ar", str(SR), "-f", "f32le", "-ac", "2", "-"], capture_output=True).stdout
    return np.frombuffer(out, np.float32).reshape(-1, 2).copy()


def process(a, kind):
    mono = np.abs(a[:, 0] - a[:, 1]).max() < 1e-3 * (np.abs(a).max() + 1e-9)
    env = np.convolve(np.abs(a).max(1), np.ones(240) / 240, "same")
    pk = env.max() + 1e-9
    if kind == "s":
        on = np.where(env > pk * 10 ** (-40 / 20))[0]
        if len(on):
            a = a[max(0, on[0] - int(0.005 * SR)): on[-1] + int(0.08 * SR)]
        a = a[: int(6 * SR)]
        f = min(len(a) // 4, int(0.04 * SR)); a[-f:] *= np.linspace(1, 0, f)[:, None]
        a *= 10 ** (-1 / 20) / (np.abs(a).max() + 1e-9)
    else:
        a = a[int(0.5 * SR):] if len(a) > 25 * SR else a      # skip handling noise at the start
        a = a[: int(60 * SR)]
        x = int(min(2.0, len(a) / SR / 8) * SR)              # loop: crossfade the tail into the head
        if len(a) > 3 * x:
            head, tail = a[:x].copy(), a[-x:]
            r = np.linspace(0, 1, x)[:, None]
            a = a[:-x].copy(); a[:x] = head * np.sqrt(r) + tail * np.sqrt(1 - r)
        rms = np.sqrt((a ** 2).mean()) + 1e-9
        a *= 10 ** (-26 / 20) / rms
        a = np.clip(a, -0.95, 0.95)
    return (a[:, :1] if mono else a), mono


def save(a, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    ch = a.shape[1]
    p = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", str(ch), "-i", "-", "-c:a", "libvorbis",
                        "-q:a", "5", str(path)], input=a.astype(np.float32).tobytes())
    return p.returncode == 0


def main(only=()):
    key = os.environ.get("FREESOUND_API_KEY", "")
    if not key or key.startswith("PASTE_"):
        sys.exit("FREESOUND_API_KEY is not set")
    cred = json.loads(CRED.read_text()) if CRED.exists() else {}
    used = {v["id"] for v in cred.values()}
    for name, (cat, q, kind) in WANT.items():
        if only and name not in only:
            continue
        dst = OUT / cat / f"{name}.ogg"
        if dst.exists() and name in cred:
            continue
        dur = "[0.15 TO 12]" if kind == "s" else "[20 TO 400]"
        if os.environ.get("TW_ALT") and name in ALT:
            q = ALT[name]
        url = "https://freesound.org/apiv2/search/text/?" + urllib.parse.urlencode({
            "query": q, "filter": f'license:"Creative Commons 0" duration:{dur}', "sort": "score",
            "fields": "id,name,username,license,url,previews,duration,avg_rating,num_ratings,num_downloads,tags,samplerate,channels",
            "page_size": 25})
        try:
            r = api(url, key)
        except Exception as e:
            print("search fail", name, type(e).__name__, flush=True); time.sleep(3); continue
        res = [x for x in r.get("results", []) if "publicdomain/zero" in x["license"] and x["id"] not in used
               and not BAD.search(x["name"] + " " + " ".join(x.get("tags", [])))]
        if not res:
            print("none", name, flush=True); continue
        # relevance first (search order), then quality: downloads + rating
        best = max(enumerate(res[:12]), key=lambda ix: (math.log1p(ix[1]["num_downloads"]) + 0.6 * (ix[1]["avg_rating"] or 2.5)
                                                       * min(1, ix[1]["num_ratings"] / 3) - 0.35 * ix[0]))[1]
        try:
            data = urllib.request.urlopen(urllib.request.Request(best["previews"]["preview-hq-mp3"]), timeout=90).read()
        except Exception as e:
            print("dl fail", name, type(e).__name__, flush=True); continue
        with tempfile.TemporaryDirectory() as td:
            raw = Path(td) / "in.mp3"; raw.write_bytes(data)
            a = decode(raw)
        if len(a) < int(0.05 * SR):
            print("empty", name, flush=True); continue
        a, mono = process(a, kind)
        if not save(a, dst):
            print("encode fail", name, flush=True); continue
        cred[name] = dict(file=str(dst.relative_to(OUT)), category=cat, kind="ambience" if kind == "a" else "sfx", id=best["id"],
                          title=best["name"], author=best["username"], license="CC0 1.0", url=best["url"],
                          seconds=round(len(a) / SR, 2), channels=1 if mono else 2, query=q)
        used.add(best["id"])
        CRED.write_text(json.dumps(cred, indent=1, sort_keys=True))
        print("ok", name, "|", best["name"][:40], "|", best["username"], "|", round(len(a) / SR, 1), "s", flush=True)
        time.sleep(1.1)
    print("done", len(cred), "sounds", flush=True)


if __name__ == "__main__":
    main(set(sys.argv[1:]))
