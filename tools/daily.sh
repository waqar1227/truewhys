#!/bin/bash
# Daily growth data (deterministic, no AI): channel analytics + competitor snapshot.
# Works in a light session too: uses /opt/c3d/bin/python if present, else system python3 (+ pip yt-dlp).
# Writes research/stats/<date>.{json,md} and research/competitors/<date>.{json,md}; the daily report entry
# in research/daily_report.md then only needs the short analysis (template: research/report_template.md).
cd "$(dirname "$0")/.."
P=/opt/c3d/bin/python; [ -x $P ] || P=python3
[ -x /opt/c3d/bin/yt-dlp ] || command -v yt-dlp >/dev/null || $P -m pip install -q yt-dlp
$P lib/yt_stats.py 28 > /dev/null && echo "stats: research/stats/$(date -u +%F).md"
$P lib/competitors.py > /dev/null && echo "competitors: research/competitors/$(date -u +%F).md"
