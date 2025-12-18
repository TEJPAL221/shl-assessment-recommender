import sys
import os

# Make project root importable
sys.path.append(os.path.abspath("."))

from backend.app.main import app

# Hugging Face looks for a variable named `app`
# This exposes FastAPI directly
