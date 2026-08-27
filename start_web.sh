#!/bin/sh

PROJECT_DIR="/volume1/projects/vitesse-control-center"
PYTHON="/volume1/@appstore/python311/bin/python3"
LOG_FILE="$PROJECT_DIR/logs/vcc.log"

echo "Starting VCC web launcher..."
"$PYTHON" "$PROJECT_DIR/web.py" --background
STATUS=$?

echo "VCC web launcher exit status: $STATUS"
echo "Recent VCC log:"
if [ -f "$LOG_FILE" ]; then
    tail -n 12 "$LOG_FILE"
else
    echo "VCC log file was not created."
fi

exit "$STATUS"