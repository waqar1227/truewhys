#!/bin/bash
# Rebuild the flat Kaggle dataset for B-009 plates from the repo (run from the repo root).
set -e
D=notebooks/kaggle_jobs/b009/dataset
cp lib/sets.py lib/sets9.py episodes/B-009-flight-secrets/plates.py $D/
