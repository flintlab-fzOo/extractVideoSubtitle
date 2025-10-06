#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: Soop URL is required as an argument." >&2
  exit 1
fi

cd ..
uv run soop_downloader.py --username '[soopid]' --password '[sooppassword]' --url "$1"