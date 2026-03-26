#!/bin/bash
# Launch the free throw biomechanics viewer
cd "$(dirname "$0")"

# Generate manifest if missing
if [ ! -f visuals/manifest.json ]; then
    echo "Generating manifest..."
    python3 generate_visuals.py
fi

PORT=${1:-8000}
URL="http://localhost:$PORT/visuals/"

echo "Starting viewer at $URL"
echo "Press Ctrl+C to stop"

# Open browser (try common openers)
if command -v xdg-open &>/dev/null; then
    xdg-open "$URL" 2>/dev/null &
elif command -v open &>/dev/null; then
    open "$URL" &
elif command -v wslview &>/dev/null; then
    wslview "$URL" &
else
    echo "Open $URL in your browser"
fi

python3 -m http.server "$PORT"
