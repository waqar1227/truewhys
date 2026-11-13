# Shorts upload — cut from "10 Pirate Myths You Still Believe (And What Was Real)"

Long video publishAt: 2026-11-14T15:00:00Z. Shorts: +1 h, then every 3 h (all within 24 h). Owner rule 6 Nov 2026.

Each Short: private + publishAt, made for kids No, altered/synthetic field left unset, playlist "Shorts".
After upload: in YouTube Studio set **Related video = the long video** on each Short (not available in the API).

| Short | publishAt (UTC) | Title | Desc chars |
|---|---|---|---|
| C1 | 2026-11-14T16:00:00Z | Pirates Never Actually Said "Arrr" #Shorts | 450 |
| C2 | 2026-11-14T19:00:00Z | Why Pirates Didn't Really Have Parrots #Shorts | 507 |
| C3 | 2026-11-14T22:00:00Z | The Real Reason Pirates Wore Eye Patches #Shorts | 516 |
| C4 | 2026-11-15T01:00:00Z | Pirates Almost Never Made Anyone Walk the Plank #Shorts | 512 |
| C5 | 2026-11-15T04:00:00Z | Why Pirates Almost Never Buried Treasure #Shorts | 477 |
| C6 | 2026-11-15T07:00:00Z | The Real Reason Pirates Flew the Skull and Crossbones #Shorts | 484 |
| C7 | 2026-11-15T10:00:00Z | Pirates Had a Bedtime #Shorts | 475 |
| C8 | 2026-11-15T13:00:00Z | Pirates Had Injury Insurance #Shorts | 488 |
| C9 | 2026-11-15T16:00:00Z | The Pirate Crew Could Fire the Captain #Shorts | 535 |
| C10 | 2026-11-15T19:00:00Z | The Women Pirates Who Escaped the Noose #Shorts | 522 |

Upload: `python lib/youtube.py upload episodes/<ep>/shorts/<CID>/final.mp4 episodes/<ep>/shorts/<CID>/upload_meta.json --long <long video id>`
