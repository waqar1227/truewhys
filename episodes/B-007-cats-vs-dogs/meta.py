"""Writes upload_meta.json (long video + cut Short) with chapters taken from make.py. python episodes/B-007-cats-vs-dogs/meta.py"""
import json, subprocess, sys
from pathlib import Path
EP = Path(__file__).resolve().parent
PY = sys.executable
chap = subprocess.run([PY, str(EP / "make.py"), "chapters"], capture_output=True, text=True, check=True).stdout.strip()
AI = {"synthetic": False, "reason": "Not realistic: flat 2D cartoon (cast v2.2 + cartoon pets), generic TTS narrator imitating no real person, code-made music; "
      "no realistic people, animals, places or events (docs/ai_disclosure.md test, 25 Nov 2026)."}
long = {
 "title": "Cats vs Dogs: Who's Smarter, and Who Loves You More?",
 "description": "Your cat knows its own name. It just doesn't come. And your dog grew a new face muscle just to work on you.\n\n"
   "Cats vs dogs in 7 rounds, settled with real experiments, not opinions. Who moved in with humans first? Are dogs smarter than cats, and what happens "
   "when scientists count their brain cells? Do cats know their names? Dog nose vs cat ears. How do cats and dogs drink water (it's the same physics trick)? "
   "Puppy eyes vs the cat's purr. And the last round: do cats love their owners as much as dogs do?\n\n"
   "Chapters\n" + chap + "\n\n"
   "Sources\n• Bergström et al., \"Origins and genetic legacy of prehistoric dogs\", Science (2020); Driscoll et al., Science (2007) and PNAS (2009)\n"
   "• Jardim-Messeder, Herculano-Houzel et al., \"Dogs have the most neurons, though not the largest brain\", Frontiers in Neuroanatomy (2017)\n"
   "• Pilley & Reid, Behavioural Processes (2011); Saito et al., \"Domestic cats discriminate their names from other words\", Scientific Reports (2019)\n"
   "• Heffner, Behavioral Neuroscience (1983); Heffner & Heffner, \"Hearing range of the domestic cat\", Hearing Research (1985)\n"
   "• Reis, Jung, Aristoff & Stocker, \"How cats lap\", Science (2010); Gart, Socha, Vlachos & Jung, \"Dogs lap using acceleration-driven open pumping\", PNAS (2015)\n"
   "• Kaminski et al., \"Evolution of facial muscle anatomy in dogs\", PNAS (2019); Waller et al., PLOS ONE (2013)\n"
   "• McComb et al., \"The cry embedded within the purr\", Current Biology (2009)\n"
   "• Topál et al., J. Comparative Psychology (1998); Vitale, Behnke & Udell, \"Attachment bonds between domestic cats and humans\", Current Biology (2019)\n"
   "• Every claim checked against 2+ sources. The round points are our own playful scoring.\n\n#cats #dogs #science",
 "tags": ["cats vs dogs", "are dogs smarter than cats", "cats vs dogs intelligence", "do cats know their names", "do cats love their owners",
          "puppy eyes", "why do dogs make puppy eyes", "how do cats drink water", "how dogs drink water", "dog sense of smell", "cat hearing",
          "cat purr", "dog vs cat brain", "animal science", "pet facts", "TrueWhys"],
 "categoryId": "28", "publishAt": "2026-12-20T17:00:00Z", "playlist": "Full Stories", "video": "final/B-007.mp4",
 "pinned_comment": "Final score: dog 5, cat 4. Do you agree with the referee, or did we get a round wrong? Team Dog or Team Cat, tell us below. Which animal should face off next?",
 "ai_disclosure": AI}
(EP / "upload_meta.json").write_text(json.dumps(long, indent=1, ensure_ascii=False))
SH = {
 "C1": ("C1-puppy-eyes", "Why Dogs Make Puppy Eyes at You",
        "Dogs have a tiny muscle that lifts the inner eyebrow, and wolves mostly don't. Shelter dogs that made the face more often found homes faster.\n\n"
        "Full video (cats vs dogs, 7 rounds of real science): {LONG_URL}\n\n"
        "Sources: Kaminski et al., PNAS (2019); Waller et al., PLOS ONE (2013).\n\n#shorts #dogs #science",
        ["puppy eyes", "why do dogs make puppy eyes", "dog eyebrow muscle", "dogs vs wolves", "dog facts", "animal science", "TrueWhys"],
        "2026-12-26T18:00:00Z")}
for sid, (d, title, desc, tags, at) in SH.items():
    m = {"title": title, "description": desc, "tags": tags, "publishAt": at, "categoryId": "28", "playlist": "Shorts",
         "video": f"final/B-007-{sid}.mp4", "ai_disclosure": AI}
    (EP / "shorts" / d / "upload_meta.json").write_text(json.dumps(m, indent=1, ensure_ascii=False))
print(chap)
