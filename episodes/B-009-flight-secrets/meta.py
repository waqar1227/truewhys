"""Writes upload_meta.json (long video + cut Short) with chapters taken from make.py. python episodes/B-009-flight-secrets/meta.py"""
import json, subprocess, sys
from pathlib import Path
EP = Path(__file__).resolve().parent
PY = sys.executable
chap = subprocess.run([PY, str(EP / "make.py"), "chapters"], capture_output=True, text=True, check=True).stdout.strip()
AI = {"synthetic": False, "reason": "Not realistic: flat 2D cartoon (cast v2.2, generic plane in our colours), generic TTS narrator imitating no real person, "
      "code-made music; no realistic people, places or events, no real footage (docs/ai_disclosure.md test, 26 Nov 2026)."}
long = {
 "title": "Why Planes Dim the Lights to Land (and 6 More Flight Secrets) ✈️",
 "description": "Right before some planes land at night, the crew switches the cabin lights off. On purpose. And it's not to help you sleep.\n\n"
   "One flight, from the gate to the runway, and the real reason behind 7 strange things planes make you do: why you always board on the left side, "
   "why you need airplane mode, why your seat has to be upright for takeoff and landing (the 90-second rule), what the tiny hole in the plane window is for, "
   "why airplane food tastes bland (and why everyone orders tomato juice), why you put your own oxygen mask on first, and why the cabin lights go dim for landing.\n\n"
   "Chapters\n" + chap + "\n\n"
   "Sources\n• Cabin lights and window shades: Time (2016); Fortune (2016); AFAR; IATA guidance\n"
   "• Boarding on the left: AFAR; Scripps News; Jalopnik\n"
   "• Airplane mode: FCC rule 91-399 (1991), 47 CFR 22.925; US DOT; UK CAA (2000) study; Popular Science\n"
   "• 90-second evacuation rule: 14 CFR 25.803 + Appendix J; A380 test, Hamburg, 26 March 2006 (NBC News, FlightGlobal, Flight Safety Foundation)\n"
   "• Window breather hole: Mental Floss; AFAR; Fortune; Gizmodo\n"
   "• Taste in the air: Fraunhofer IBP study for Lufthansa (2010); Spence, Int. J. Gastronomy & Food Science (2017); Cornell University (2015); Lufthansa Group newsroom\n"
   "• Oxygen masks and hypoxia: FAA \"Hypoxia\" guidance; time of useful consciousness tables (FAA, AOPA); ATSB report AR-2008-075\n"
   "• Accidents by phase of flight: Boeing Statistical Summary; Flight Safety Foundation\n"
   "• Every claim checked against 2+ sources. Not safety training: always follow your crew's briefing.\n\n#planes #aviation #science",
 "tags": ["why do planes dim the lights for landing", "why window shades up for landing", "airplane mode", "why do you need airplane mode",
          "airplane window hole", "why is there a hole in airplane windows", "why does plane food taste bland", "tomato juice on planes",
          "put your own oxygen mask on first", "time of useful consciousness", "90 second evacuation rule", "why board planes on the left",
          "seat upright for landing", "flight secrets", "aviation facts", "plane facts", "TrueWhys"],
 "categoryId": "28", "publishAt": "2027-01-02T17:00:00Z", "playlist": "Full Stories", "video": "final/B-009.mp4",
 "pinned_comment": "Which of the 7 surprised you most: the left door, airplane mode, the 90 seconds, the tiny hole, the bland food, mask first, or the dark cabin? And what strange plane rule should we explain next?",
 "ai_disclosure": AI}
(EP / "upload_meta.json").write_text(json.dumps(long, indent=1, ensure_ascii=False))
SH = {
 "C1": ("C1-mask-first", "Why You Put Your Own Oxygen Mask On First ✈️",
        "At 35,000 feet, a loss of cabin pressure can leave you only 30 seconds to a minute of clear thinking, and you often don't feel it coming. "
        "That's why the crew says: your own mask first, then help others.\n\n"
        "Full video (7 strange things on every flight, explained): {LONG_URL}\n\n"
        "Sources: FAA hypoxia guidance; time of useful consciousness tables (FAA, AOPA). Not safety training: always follow your crew's briefing.\n\n#shorts #planes #aviation",
        ["oxygen mask", "put your own oxygen mask on first", "time of useful consciousness", "hypoxia", "plane facts", "aviation facts", "TrueWhys"],
        "2027-01-07T18:00:00Z")}
for sid, (d, title, desc, tags, at) in SH.items():
    m = {"title": title, "description": desc, "tags": tags, "publishAt": at, "categoryId": "28", "playlist": "Shorts",
         "video": f"final/B-009-{sid}.mp4", "ai_disclosure": AI}
    (EP / "shorts" / d / "upload_meta.json").write_text(json.dumps(m, indent=1, ensure_ascii=False))
print(chap)
