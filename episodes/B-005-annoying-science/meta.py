"""Writes upload_meta.json (long video + cut Shorts) with chapters taken from make.py. python episodes/B-005-annoying-science/meta.py"""
import json, subprocess, sys
from pathlib import Path
EP = Path(__file__).resolve().parent
PY = sys.executable
chap = subprocess.run([PY, str(EP / "make.py"), "chapters"], capture_output=True, text=True, check=True).stdout.strip()
AI = {"synthetic": False, "reason": "Not realistic: flat 2D cartoon (cast v2.2), generic TTS narrator imitating no real person, code-made music; "
      "no realistic people, places or events (docs/ai_disclosure.md test, 22 Nov 2026)."}
long = {
 "title": "Why Toast Lands Butter-Side Down, Shoelaces Untie and Earbuds Tangle",
 "description": "Your toast landing butter-side down isn't bad luck. A physicist worked out the real culprit: the height of your kitchen table.\n\n"
   "Seven everyday annoyances, seven real experiments. Why do shoelaces come undone even when you tie them tight? Why do earbuds come out of your "
   "pocket in a knot? Why does dry spaghetti never snap into just two pieces? Why does the shower curtain creep in and stick to your legs? Why does "
   "spilled coffee dry as a ring, and why do the last cereal loops in your bowl clump together? Scientists measured every one of them, with treadmills, "
   "spinning boxes and two weeks of computer time.\n\nChapters\n" + chap + "\n\n"
   "Sources\n• R. A. J. Matthews, \"Tumbling toast, Murphy's Law and the fundamental constants\", European Journal of Physics (1995)\n"
   "• Daily-Diamond, Gregg & O'Reilly, \"The roles of impact and inertia in the failure of a shoelace knot\", Proc. Royal Society A (2017); UC Berkeley News\n"
   "• Raymer & Smith, \"Spontaneous knotting of an agitated string\", PNAS (2007)\n"
   "• Audoly & Neukirch, Physical Review Letters (2005); Heisser et al., PNAS (2018); MIT News\n"
   "• Scientific American (2001): David Schmidt on why the shower curtain moves toward the water\n"
   "• Deegan et al., Nature (1997); Yunker et al., Nature (2011)\n"
   "• Vella & Mahadevan, \"The 'Cheerios effect'\", American Journal of Physics (2005)\n"
   "• Every claim checked against 2+ sources\n\n#science #physics #everydayscience",
 "tags": ["why toast lands butter side down", "buttered toast physics", "why shoelaces come untied", "shoelace knot science",
          "why earbuds tangle", "why headphones tangle", "spaghetti breaks in three", "spaghetti break in two", "shower curtain effect",
          "why shower curtain blows in", "coffee ring effect", "cheerios effect", "everyday science", "physics explained", "science of annoying things", "TrueWhys"],
 "categoryId": "28", "publishAt": "2026-12-07T17:00:00Z", "playlist": "Full Stories", "video": "final/B-005.mp4",
 "pinned_comment": "Which one will you test first? Ours: the spaghetti twist (it really works, but you need patience). Which everyday annoyance should we explain next?",
 "ai_disclosure": AI}
(EP / "upload_meta.json").write_text(json.dumps(long, indent=1, ensure_ascii=False))
SH = {
 "C1": ("C1-toast", "Why Toast Always Lands Butter-Side Down",
        "It's not bad luck: from a normal table, falling toast only has time for half a turn, so the buttered side ends up on the bottom.\n\n"
        "Full video (7 everyday annoyances explained) on our channel: \"Why Toast Lands Butter-Side Down, Shoelaces Untie and Earbuds Tangle\".\n\n"
        "Sources: R. A. J. Matthews, European Journal of Physics (1995); Bacon et al., American Journal of Physics (2001).\n\n#shorts #science #physics",
        ["why toast lands butter side down", "buttered toast", "toast physics", "murphy's law", "physics facts", "everyday science", "TrueWhys"],
        "2026-12-08T18:00:00Z"),
 "C2": ("C2-spaghetti", "Why You Can't Snap Spaghetti in Two",
        "Dry spaghetti almost always breaks into 3 or more pieces: the first snap sends a bending wave down each half. In 2018 an MIT team found the fix.\n\n"
        "Full video (7 everyday annoyances explained) on our channel: \"Why Toast Lands Butter-Side Down, Shoelaces Untie and Earbuds Tangle\".\n\n"
        "Sources: Audoly & Neukirch, Physical Review Letters (2005); Heisser et al., PNAS (2018); MIT News.\n\n#shorts #science #physics",
        ["spaghetti break in two", "why spaghetti breaks into three", "spaghetti physics", "MIT spaghetti", "feynman spaghetti", "everyday science", "TrueWhys"],
        "2026-12-10T18:00:00Z")}
for sid, (d, title, desc, tags, at) in SH.items():
    m = {"title": title, "description": desc, "tags": tags, "publishAt": at, "categoryId": "28", "playlist": "Shorts",
         "video": f"final/B-005-{sid}.mp4", "ai_disclosure": AI}
    (EP / "shorts" / d / "upload_meta.json").write_text(json.dumps(m, indent=1, ensure_ascii=False))
print(chap)
