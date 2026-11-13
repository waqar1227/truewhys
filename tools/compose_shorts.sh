#!/bin/bash
# Compose every cut Short of an episode (resumable; skips finished ones): bash tools/compose_shorts.sh episodes/<ep>
cd "$(dirname "$0")/.."; E=$1
for d in $E/shorts/C*/; do c=$(basename $d)
  [ -f $E/shorts/$c/final.mp4 ] && continue
  COMPOSE_RESUME=$E/renders/compose_$c /opt/c3d/bin/python lib/compose.py $E --plan $E/shorts/$c/shots.json --timing $E/timing_all.json \
    --plates $E/shorts/renders/plates --w 1080 --h 1920 --workers 4 --out $E/shorts/$c/final_tmp.mp4 \
    && mv $E/shorts/$c/final_tmp.mp4 $E/shorts/$c/final.mp4 && echo "$(date -u +%H:%M) $c done"
done
echo ALLDONE
