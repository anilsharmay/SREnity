"""
Simple configuration for notebook - just the backend path
"""
from pathlib import Path

# Get backend directory relative to this config file
# Config is in backend/notebooks/config.py, so backend is parent
BACKEND_DIR = Path(__file__).parent.parent

# Logs directory relative to backend
LOGS_DIR = BACKEND_DIR / "data" / "logs"




