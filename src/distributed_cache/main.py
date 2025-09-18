from fastapi.staticfiles import StaticFiles
import os

# Import the app from api.py
from .api import app

# Get the absolute path to the frontend directory
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")

# Mount the static files directory
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")
