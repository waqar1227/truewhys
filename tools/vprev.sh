#!/bin/bash
# usage: vprev.sh CID  -> /tmp/claude-0/vsheet_CID.png
cd /home/user/truewhys; E=${EP:-episodes/B-001-animal-trials}; C=$1; P=/tmp/claude-0/vst_$C; O=/tmp/claude-0/vc_$C
rm -f $P/*.png 2>/dev/null; mkdir -p $P $O
/opt/c3d/bin/python lib/render_bg.py $E/shorts/$C/shots.json $P --stills --w 540 --h 960 --samples 24 > $P.log 2>&1
ids=$(python3 -c "import json;print(' '.join(s['id'] for s in json.load(open('$E/shorts/$C/shots.json'))['shots']))")
for s in $ids; do /opt/c3d/bin/python lib/compose.py $E --plates $P --plan $E/shorts/$C/shots.json --timing $E/shorts/timing.json --w 540 --h 960 --still $s:0.6 --out $O/$s.png >/dev/null 2>&1; done
/opt/c3d/bin/python - <<P
from PIL import Image,ImageDraw
ids="$ids".split(); n=len(ids); cols=8; rows=(n+cols-1)//cols
W=Image.new('RGB',(270*cols,480*rows))
for i,s in enumerate(ids):
    im=Image.open('$O/'+s+'.png').resize((270,480)); ImageDraw.Draw(im).text((4,4),s,fill=(255,255,0)); W.paste(im,((i%cols)*270,(i//cols)*480))
W.save('/tmp/claude-0/vsheet_$C.png')
P
echo done $C
