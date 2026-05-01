# ============================================================================
# PythonAnywhere WSGI Configuration File
# ============================================================================
# Place this file at: /var/www/yourusername_pythonanywhere_com_wsgi.py
# (PythonAnywhere will generate the filename based on your username/domain)
#
# Instructions:
# 1. Log in to PythonAnywhere
# 2. Go to Web tab
# 3. Add a new web app
# 4. Choose "Flask"
# 5. Copy this entire file's content into the WSGI configuration
# 6. Update the 'path' variable below with your actual path
# 7. Reload the web app
#
# ============================================================================

import sys
import os

# IMPORTANT: Update this path to match your PythonAnywhere directory structure
# Format: /home/yourusername/path/to/stavanger_app/web/CLI
path = '/home/yourusername/stavanger_app/web/CLI'

if path not in sys.path:
    sys.path.insert(0, path)

# Change to the CLI directory so relative imports work
os.chdir(path)

# Import the Flask app from app/app.py
from app.app import create_app

# Create the Flask application
app = create_app()

# PythonAnywhere will use 'app' as the WSGI callable
