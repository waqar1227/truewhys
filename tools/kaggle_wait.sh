#!/bin/bash
# One background waiter: polls Kaggle kernels every 10 min, downloads each finished kernel's output.
# usage: tools/kaggle_wait.sh <kernel>=<out_dir> ...   (exits when the first kernel in the list finishes, or all if ALL=1)
K="/opt/c3d/bin/python tools/kaggle_px.py"
while true; do
  for kv in "$@"; do k=${kv%%=*}; d=${kv#*=}; [ -f "$d/.fetched_$k" ] && continue
    s=$($K kernels status anam318/truewhys-render-$k 2>&1 | tail -1)
    case "$s" in *COMPLETE*|*ERROR*|*CANCEL*) mkdir -p "$d"; $K kernels output anam318/truewhys-render-$k -p "$d" >/dev/null 2>&1
      touch "$d/.fetched_$k"; echo "$(date -u +%H:%M) $k: $s"; [ -z "$ALL" ] && exit 0;; esac
  done
  left=0; for kv in "$@"; do k=${kv%%=*}; d=${kv#*=}; [ -f "$d/.fetched_$k" ] || left=1; done; [ $left = 0 ] && exit 0
  sleep 600
done
