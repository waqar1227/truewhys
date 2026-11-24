"""Write <ep>/shots.json (id, line, start, dur, line_start) from a Style F make.py, for tools/make_srt.py.
python lib/write_shots.py episodes/<ep>"""
import runpy, json, sys
from pathlib import Path
ep = Path(sys.argv[1])
sys.path.insert(0, str(Path(__file__).resolve().parent))
V = runpy.run_path(str(ep / "make.py"), run_name="shots")["V"]
out = dict(duration=V.duration, shots=[dict(id=s["id"], line=s["line"], start=s["start"], dur=s["dur"], line_start=s["line_start"]) for s in V.shots])
(ep / "shots.json").write_text(json.dumps(out, indent=1))
print(ep / "shots.json", len(out["shots"]), "shots", V.duration, "s")
