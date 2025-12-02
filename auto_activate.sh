#!/bin/bash
# auto_activate.sh — auto-activates or creates user-defined virtual environment

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_NAME="test_myenv"    # 👈 your custom venv name here
VENV_PATH="$PROJECT_DIR/$VENV_NAME"

if [ -d "$VENV_PATH" ]; then
    source "$VENV_PATH/bin/activate"
    echo "✅ Activated virtual environment: $VENV_NAME"
else
    echo "⚠️ Virtual environment '$VENV_NAME' not found. Creating one..."
    python3 -m venv "$VENV_PATH"
    source "$VENV_PATH/bin/activate"
    echo "✅ Created and activated '$VENV_NAME'."
    pip install -r "$PROJECT_DIR/requirements.txt"
fi
