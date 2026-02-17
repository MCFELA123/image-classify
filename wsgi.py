"""
WSGI entry point for Render deployment
"""
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the app from backend
from backend.app import app

if __name__ == "__main__":
    app.run()
