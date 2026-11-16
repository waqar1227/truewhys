#!/bin/bash
# Build + push the flat Kaggle dataset and kernel for one Style R episode.
# usage: tools/kaggle_style_r.sh a016 episodes/A-016-onion-tears '{"w":1080,"h":1920,"samples":64,"step":1,"mblur":true}' <mpfb.zip>
set -e; ID=$1; EP=$2; JOB=$3; ZIP=$4
K="/opt/c3d/bin/python tools/kaggle_px.py"
D=/tmp/kds_$ID; KD=/tmp/kk_$ID; rm -rf $D $KD; mkdir -p $D $KD
cp lib/style_r/sr_*.py lib/camera.py $EP/scene.py $EP/shots.json $D/; cp $ZIP $D/mpfb.zip; echo "$JOB" > $D/job.json
echo "{\"title\": \"truewhys-ep-$ID\", \"id\": \"anam318/truewhys-ep-$ID\", \"licenses\": [{\"name\": \"CC0-1.0\"}]}" > $D/dataset-metadata.json
if $K datasets status anam318/truewhys-ep-$ID >/dev/null 2>&1; then $K datasets version -p $D -m "update $(date -u +%F_%H%M)" -r zip; else $K datasets create -p $D -r zip; fi
cp notebooks/kaggle_jobs/style_r/render.py $KD/render.py
echo "{\"id\": \"anam318/truewhys-render-$ID\", \"title\": \"truewhys-render-$ID\", \"code_file\": \"render.py\", \"language\": \"python\", \"kernel_type\": \"script\", \"is_private\": true, \"enable_gpu\": true, \"enable_internet\": true, \"dataset_sources\": [\"anam318/truewhys-ep-$ID\"], \"competition_sources\": [], \"kernel_sources\": []}" > $KD/kernel-metadata.json
echo "dataset pushed; kernel dir $KD (push after the dataset is ready: $K kernels push -p $KD --accelerator NvidiaTeslaT4)"
