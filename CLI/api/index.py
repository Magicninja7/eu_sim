import sys
from pathlib import Path

# Add parent directory to path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import and create the Flask app
from app.app import create_app

app = create_app()

# For serverless function export
