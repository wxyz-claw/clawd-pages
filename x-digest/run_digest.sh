#!/bin/bash
set -e

# Directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "Step 1: Processing digest..."
python3 process_digest.py

echo "Step 2: Rendering latest digest to index.html..."
python3 render.py --input digest.json --output index.html

# Get today's date in YYYY-MM-DD format
TODAY=$(date +%Y-%m-%d)
FILENAME="${TODAY}.html"

echo "Step 3: Archiving to ${FILENAME}..."
cp index.html "$FILENAME"

echo "Step 4: Updating archive index..."
python3 update_archive.py

echo "Done! Latest digest is at index.html and archived at ${FILENAME}."
