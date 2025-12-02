import yaml
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import logging
from backend.extra_api import router as extra_router
from backend.auth_api import router as auth_router

# Get project root (one level above frontend folder)
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(PROJECT_DIR, "config.yml")

# Universal logger setup
LOG_DIR = os.path.join(PROJECT_DIR, "log")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_FILE = os.path.join(LOG_DIR, "backend.log")

logger = logging.getLogger("backend_logger")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

ch = logging.StreamHandler()
ch.setFormatter(formatter)
fh = logging.FileHandler(LOG_FILE)
fh.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(ch)
    logger.addHandler(fh)

# Load config
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)
    logger.info("Loaded configuration from %s", CONFIG_PATH)

backend_config = config["backend"]
logger.info("Backend config: %s", backend_config)

app = FastAPI()
logger.info("FastAPI app created.")

# Include extra APIs
app.include_router(auth_router)
app.include_router(extra_router)


# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/greet")
def greet(name: str = Query(...)):
    logger.info("Greet endpoint called with name=%s", name)
    return {"message": f"Hello, {name}!"}

@app.get("/api/square")
def square(number: int = Query(...)):
    logger.info("Square endpoint called with number=%d", number)
    return {"result": number ** 2}

if __name__ == "__main__":
    logger.info("Starting backend server at %s:%s", backend_config["host"], backend_config["port"])
    uvicorn.run("main:app", host=backend_config["host"], port=backend_config["port"], reload=True)
