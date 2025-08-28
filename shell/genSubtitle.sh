#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: YouTube URL or VideoId is required as an argument." >&2
  exit 1
fi

cd ..
PYTHONIOENCODING=utf-8 uv run extractVideoSubtitle.py --summary --youtube "$1" > ./logs/summary.log