"""Writes upload_meta.json (long video + cut Short) with chapters taken from make.py. python episodes/B-008-accidental-inventions/meta.py"""
import json, subprocess, sys
from pathlib import Path
EP = Path(__file__).resolve().parent
PY = sys.executable
chap = subprocess.run([PY, str(EP / "make.py"), "chapters"], capture_output=True, text=True, check=True).stdout.strip()
AI = {"synthetic": False, "reason": "Not realistic: flat 2D cartoon (cast v2.2 stand-ins, code-drawn props and sets), generic TTS narrator imitating no real person, "
      "code-made music; no realistic people, places or events and no real person shown saying or doing anything (docs/ai_disclosure.md test, 26 Nov 2026)."}
SRC = ("Sources\n"
       "• Microwave: APS News \"October 8, 1945: First patent for microwave cooking\" (2015); IEEE Spectrum \"A Brief History of the Microwave Oven\"; Lemelson-MIT \"Percy Spencer\"\n"
       "• Slinky: Encyclopedia of Greater Philadelphia \"Slinky\"; Smithsonian Magazine \"The Accidental Invention of the Slinky\"; PBS American Experience\n"
       "• Velcro: WIPO \"From a Mountain Walk to 2,100 Patents: The Velcro IP Story\"; Lemelson-MIT \"George de Mestral\"\n"
       "• Super glue: Lemelson-MIT \"Harry Coover\"; Popular Science \"How a shot at making better gunsights became Super Glue instead\"\n"
       "• PTFE / non-stick: Science History Institute \"Roy J. Plunkett\"; APS News \"April 1938: Discovery of Teflon\" (2021)\n"
       "• Safety glass: McGill Office for Science and Society; American Ceramic Society Bulletin \"The evolution and importance of car windshields\"\n"
       "• Penicillin: Science History Institute \"Alexander Fleming\" and \"Howard Walter Florey and Ernst Boris Chain\"; University of Oxford \"Penicillin: the Oxford story\"; "
       "American Chemical Society, National Historic Chemical Landmark \"Discovery and Development of Penicillin\"\n"
       "• Every claim checked against 2+ sources; where accounts differ (the candy-bar story, exact dates) we say so or leave the detail out.")
long = {
 "title": "How 7 Everyday Things Were Invented by Accident",
 "description": "In 1945, an engineer's candy bar melted in his pocket, and nothing near him was hot. That sticky pocket is why there's a microwave in your kitchen.\n\n"
   "7 everyday inventions nobody meant to make, counted down from the smallest accident to the one that changed the world: a spring that walked off a shelf "
   "(the Slinky), burrs on a dog (Velcro), a glue that was too sticky and thrown away for 9 years (super glue), a gas cylinder that looked empty "
   "(non-stick pans), a flask that broke but didn't shatter (safety glass), the melted candy bar (the microwave oven), and the dirty dish that "
   "saved millions of lives (penicillin).\n\n"
   "Chapters\n" + chap + "\n\n" + SRC + "\n\n#inventions #history #science",
 "tags": ["invented by accident", "accidental inventions", "inventions by accident", "how was the microwave invented", "microwave invention",
          "who invented velcro", "how was super glue invented", "slinky invention", "teflon discovery", "non-stick pan history",
          "safety glass invention", "how was penicillin discovered", "alexander fleming penicillin", "history of inventions",
          "everyday inventions", "science history", "TrueWhys"],
 "categoryId": "28", "publishAt": "2026-12-27T17:00:00Z", "playlist": "Full Stories", "video": "final/B-008.mp4",
 "pinned_comment": "Which accident surprised you most: the walking spring, the burrs, the too-sticky glue, the 'empty' can, the flask, the candy bar or the dirty dish? "
                   "And which everyday invention should we explain next?",
 "ai_disclosure": AI}
(EP / "upload_meta.json").write_text(json.dumps(long, indent=1, ensure_ascii=False))
SH = {
 "C1": ("C1-microwave", "How a Melted Candy Bar Invented the Microwave 🍫",
        "In 1945 an engineer's candy bar melted in his pocket next to a radar tube. Popcorn popped, an egg exploded, and the first microwave oven "
        "was almost 6 feet tall.\n\nFull video (7 everyday things invented by accident): {LONG_URL}\n\n"
        "Sources: APS News (2015); IEEE Spectrum \"A Brief History of the Microwave Oven\"; Lemelson-MIT \"Percy Spencer\".\n\n#shorts #inventions #science",
        ["microwave invention", "how was the microwave invented", "percy spencer", "invented by accident", "accidental inventions", "science history", "TrueWhys"],
        "2027-01-05T18:00:00Z")}
for sid, (d, title, desc, tags, at) in SH.items():
    m = {"title": title, "description": desc, "tags": tags, "publishAt": at, "categoryId": "28", "playlist": "Shorts",
         "video": f"final/B-008-{sid}.mp4", "ai_disclosure": AI}
    (EP / "shorts" / d / "upload_meta.json").write_text(json.dumps(m, indent=1, ensure_ascii=False))
print(chap)
