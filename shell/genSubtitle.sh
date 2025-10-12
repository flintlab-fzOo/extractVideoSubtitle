#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: YouTube URL or VideoId is required as an argument." >&2
  exit 1
fi

cd ..

QUALITY_OPTION=""
if [ -n "$2" ]; then
  QUALITY_OPTION="--quality $2"
fi

PYTHONIOENCODING=utf-8 uv run extractVideoSubtitle.py --summary --youtube "$1" $QUALITY_OPTION > ./logs/summary.log