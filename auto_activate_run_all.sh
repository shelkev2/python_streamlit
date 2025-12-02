

#!/bin/bash
# auto_activate_run_all.sh — activate venv, run FastAPI backend & Streamlit frontend

# --- Step 0: Move to project root (directory of this script) ---
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR" || exit

# --- Step 1: Activate or create virtual environment ---
VENV_NAME="test_myenv"    # your custom venv name
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

# --- Step 2: Define backend & frontend ---
BACKEND_MODULE="backend.main:app"   # note the :app at the end
FRONTEND_FILE="frontend/app.py"

# --- Step 3: Run FastAPI backend in background ---
echo "🚀 Starting FastAPI backend..."
uvicorn "$BACKEND_MODULE" --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!
echo "🆔 Backend PID: $BACKEND_PID"

# --- Step 4: Run Streamlit frontend ---
echo "🚀 Starting Streamlit frontend..."
streamlit run "$FRONTEND_FILE"

# --- Step 5: Stop backend when Streamlit exits ---
echo "🛑 Stopping FastAPI backend..."
kill "$BACKEND_PID"
echo "✅ Backend stopped."
