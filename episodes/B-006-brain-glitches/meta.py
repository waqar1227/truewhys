"""Writes upload_meta.json (long video + cut Short) with chapters taken from make.py. python episodes/B-006-brain-glitches/meta.py"""
import json, subprocess, sys
from pathlib import Path
EP = Path(__file__).resolve().parent
PY = sys.executable
chap = subprocess.run([PY, str(EP / "make.py"), "chapters"], capture_output=True, text=True, check=True).stdout.strip()
AI = {"synthetic": False, "reason": "Not realistic: flat 2D cartoon (cast v2.2), generic TTS narrator imitating no real person, code-made music; "
      "no realistic people, places or events (docs/ai_disclosure.md test, 24 Nov 2026)."}
long = {
 "title": "Why You Forget Why You Walked Into a Room, Songs Get Stuck and Déjà Vu Happens",
 "description": "You walk into a room and forget why you came in. Scientists think the doorway itself is part of the reason.\n\n"
   "Seven everyday brain glitches, seven real experiments. Why do songs get stuck in your head, and why does chewing gum help? Why can a word be on the "
   "tip of your tongue? How do you hear your own name across a noisy room? Why do you see faces in power sockets and clouds? Why do you feel your phone "
   "buzz when nobody called? And what is déjà vu, really? Each glitch turns out to be a shortcut your brain uses every day, working a little too hard.\n\n"
   "Chapters\n" + chap + "\n\n"
   "Sources\n• Radvansky, Krawietz & Tamplin, \"Walking through doorways causes forgetting\", Q. J. Exp. Psychology (2011); McFadyen et al., BMC Psychology (2021)\n"
   "• Liikkanen, Psychology of Music (2012); Jakubowski et al., Psychology of Aesthetics, Creativity and the Arts (2016); Beaman et al., University of Reading (2015)\n"
   "• Brown & McNeill, \"The tip of the tongue phenomenon\", J. Verbal Learning & Verbal Behavior (1966)\n"
   "• Cherry, J. Acoustical Society of America (1953); Moray, Q. J. Exp. Psychology (1959); Wood & Cowan, J. Exp. Psychology (1995)\n"
   "• Hadjikhani et al., NeuroReport (2009); Wardle et al., Nature Communications (2020)\n"
   "• Rothberg et al., BMJ (2010); Drouin et al., Computers in Human Behavior (2012)\n"
   "• Brown, Psychological Bulletin (2003); Cleary et al., Consciousness and Cognition (2012); Urquhart, O'Connor et al., University of St Andrews (2016)\n"
   "• Every claim checked against 2+ sources\n\n#psychology #brain #science",
 "tags": ["why do i forget why i walked into a room", "doorway effect", "why songs get stuck in your head", "earworm", "tip of the tongue",
          "cocktail party effect", "why do i hear my name", "pareidolia", "seeing faces in objects", "phantom vibration", "phone buzzing when it didn't",
          "what causes deja vu", "deja vu explained", "brain glitches", "psychology explained", "TrueWhys"],
 "categoryId": "28", "publishAt": "2026-12-13T17:00:00Z", "playlist": "Full Stories", "video": "final/B-006.mp4",
 "pinned_comment": "Which glitch happens to you the most? Ours is the doorway one (we forgot why we opened this comment box). Which everyday brain mystery should we explain next?",
 "ai_disclosure": AI}
(EP / "upload_meta.json").write_text(json.dumps(long, indent=1, ensure_ascii=False))
SH = {
 "C1": ("C1-phantom", "Why You Feel Your Phone Buzz When It Didn't",
        "That phantom buzz in your pocket is common: 68% of staff in a hospital survey and 89% of students in another study felt it. "
        "Your brain is waiting for the buzz, so it plays it safe.\n\n"
        "Full video (7 everyday brain glitches explained): {LONG_URL}\n\n"
        "Sources: Rothberg et al., BMJ (2010); Drouin et al., Computers in Human Behavior (2012).\n\n#shorts #psychology #brain",
        ["phantom vibration", "phone buzzing when it didn't", "phantom vibration syndrome", "why do i feel my phone vibrate", "brain facts", "psychology", "TrueWhys"],
        "2026-12-17T18:00:00Z")}
for sid, (d, title, desc, tags, at) in SH.items():
    m = {"title": title, "description": desc, "tags": tags, "publishAt": at, "categoryId": "28", "playlist": "Shorts",
         "video": f"final/B-006-{sid}.mp4", "ai_disclosure": AI}
    (EP / "shorts" / d / "upload_meta.json").write_text(json.dumps(m, indent=1, ensure_ascii=False))
print(chap)
