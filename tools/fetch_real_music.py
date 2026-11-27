"""Download REAL-instrument background music into library/music/real/<mood>/<slug>.ogg.
/opt/c3d/bin/python tools/fetch_real_music.py
Source: Kevin MacLeod (incompetech.com), licence CC BY 4.0 -> the exact credit line (credits.json "credit") MUST go in the
video description of every video that uses the track. Chosen for acoustic instruments (no synth tracks) and avoiding the
most over-used MacLeod tracks. Processing: 48 kHz stereo, loudness -18 LUFS, max 4 min, Vorbis q3. Skips files that exist."""
import json, subprocess, urllib.request, urllib.parse, tempfile
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "library/music/real"
SR = 48000
BASE = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/"
TRACKS = {   # mood: [(title, instruments, feel)]
    "curious": [("Goblin Tinker Soldier Spy", "tuba, marimba, melodica, bass, drums", "bouncy, humorous"),
                ("Onion Capers", "piano, tuba, percussion", "bouncy, light"),
                ("Mischief Maker", "virginal, dulcimer, bass, xylophone", "bouncy, humorous"),
                ("Industrious Ferret", "lute, English horn, cellos, violas", "bouncy, grooving"),
                ("Thinking Music", "cello, viola, violin, harp", "pondering, light suspense")],
    "light": [("Cheery Monday", "piano, bass, glockenspiel", "bright, relaxed"),
              ("Teddy Bear Waltz", "flute, glockenspiel, clarinet, strings", "bright, gentle"),
              ("Glitter Blast", "glockenspiel, flutes, ukulele, bass", "bright, bouncy"),
              ("Island Meet and Greet", "steel drum, marimba, ukulele", "bright, sunny")],
    "tense": [("River of Io", "flute, clarinet, strings, percussion", "driving, suspenseful"),
              ("Mary Celeste", "tuba, bass clarinet, French horns, bass flute", "dark, intense"),
              ("Drums of the Deep", "percussion, strings", "suspense, unnerving"),
              ("Anamalie", "guitar, bass, piano, clarinets", "dark, calm tension")],
    "warm": [("Morning", "classical guitar, harp, flutes", "calm, bright"),
             ("Evening", "guitar, cello, oboe", "calm, warm"),
             ("Crinoline Dreams", "piano, violin, viola, cello, bass", "warm, bright"),
             ("Wholesome", "cello, viola, marimba, drums", "calm, grooving")],
    "upbeat": [("Fuzzball Parade", "cello, violas, drums", "bouncy, driving"),
               ("Galway", "fiddle, flute, bass, guitar, drums", "bouncy, bright"),
               ("Still Pickin", "banjo, bass, harmonica, percussion", "bouncy, grooving"),
               ("Sergio's Magic Dustbin", "tuba, marimba, clarinets, trumpet, drums", "fast, humorous")],
    "mysterious": [("Mystery Bazaar", "santur, strings, percussion", "mysterious, calm"),
                   ("Aquarium", "flute, piano, glockenspiel, strings", "mysterious, bright"),
                   ("Hard Boiled", "bass, piano, drums", "noir, grooving"),
                   ("Almost New", "piano, basses", "mysterious, calm")],
    "festive": [("Jingle Bells", "piano, flute, clarinet, horn", "bright, winter"),
                ("Winter Chimes", "piano", "calm, winter"),
                ("Nouvelle Noel", "guitar, bass, bells, piano, vibraphone", "bright, relaxed winter")],
}


def slug(t):
    return "".join(c.lower() if c.isalnum() else "_" for c in t).strip("_").replace("__", "_")


def credit(title):
    return (f'"{title}" Kevin MacLeod (incompetech.com)\nLicensed under Creative Commons: By Attribution 4.0 License\n'
            "http://creativecommons.org/licenses/by/4.0/")


def main():
    import pyloudnorm as pyln
    cj = OUT / "credits.json"
    cred = json.loads(cj.read_text()) if cj.exists() else {}
    for mood, items in TRACKS.items():
        for title, inst, feel in items:
            key = f"{mood}/{slug(title)}"
            dst = OUT / mood / f"{slug(title)}.ogg"
            if dst.exists() and key in cred:
                continue
            url = BASE + urllib.parse.quote(title + ".mp3")
            try:
                data = urllib.request.urlopen(url, timeout=120).read()
            except Exception as e:
                print("dl fail", title, type(e).__name__, flush=True); continue
            with tempfile.TemporaryDirectory() as td:
                p = Path(td) / "in.mp3"; p.write_bytes(data)
                raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ar", str(SR), "-ac", "2", "-f", "f32le", "-"],
                                     capture_output=True).stdout
            a = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()[: int(240 * SR)]
            f = int(3 * SR)
            if len(a) >= int(239 * SR):
                a[-f:] *= np.linspace(1, 0, f)[:, None]
            lufs = pyln.Meter(SR).integrated_loudness(a)
            a = np.clip(a * 10 ** ((-18 - lufs) / 20), -0.98, 0.98)
            dst.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "libvorbis",
                            "-q:a", "3", str(dst)], input=a.astype(np.float32).tobytes(), check=True)
            cred[key] = dict(file=f"{mood}/{slug(title)}.ogg", mood=mood, title=title, author="Kevin MacLeod", instruments=inst, feel=feel,
                             license="CC BY 4.0", source=url, seconds=round(len(a) / SR, 1), credit=credit(title))
            cj.write_text(json.dumps(cred, indent=1, sort_keys=True))
            print("ok", key, round(len(a) / SR), "s", flush=True)
    print("done", len(cred), "tracks")


if __name__ == "__main__":
    main()
