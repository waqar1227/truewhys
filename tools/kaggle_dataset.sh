#!/bin/bash
# Rebuild an episode's flat Kaggle dataset folder and push a new version.
# usage: tools/kaggle_dataset.sh b002 episodes/B-002-worst-jobs   (needs notebooks/kaggle_jobs/<id>/dataset/{dataset-metadata.json,job_*.json})
set -e; ID=$1; EP=$2; D=/tmp/kds_$ID; rm -rf $D; mkdir -p $D
cp notebooks/kaggle_jobs/$ID/dataset/* $D/
cp lib/render_bg.py lib/sets.py lib/sets2.py lib/camera.py $D/
cp $EP/shots.json $D/shots.json
[ -f $EP/shorts/all_shots.json ] && cp $EP/shorts/all_shots.json $D/shorts_shots.json
/opt/c3d/bin/kaggle datasets version -p $D -m "update $(date -u +%F)"
