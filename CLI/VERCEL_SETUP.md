# Vercel Deployment Structure

This folder is now configured for deployment on Vercel with CLI as the root directory.

## Key Changes Made:

### 1. **Folder Structure**
```
CLI/
├── api/                          # Vercel serverless functions entry point
│   ├── __init__.py
│   └── index.py                  # WSGI app entry point for Vercel
├── app/                          # Flask application
│   ├── __init__.py
│   └── app.py                    # Main Flask app
├── templates/                    # Flask templates (newly created)
│   └── index.html               # HTML template
├── static/                       # Static assets (newly created)
│   ├── styles.css
│   └── app.js
├── chain_of_events/              # Game logic modules
├── pol_2_stat/
├── generaliser/
├── random_event_gen/
├── vercel.json                   # Vercel configuration
├── requirements.txt              # Python dependencies
└── .gitignore                    # Git ignore rules
```

### 2. **Fixed Imports**
- Changed from full path imports (`stavanger_app.web.CLI.chain_of_events...`)
- Now uses relative imports: `from chain_of_events.coe_logic import ...`
- This works because all code runs from the CLI directory as the root

### 3. **Files Created/Moved**
- ✅ `templates/index.html` - Flask template moved from CLI root
- ✅ `static/styles.css` - CSS moved from CLI root
- ✅ `static/app.js` - JavaScript moved from CLI root
- ✅ `api/index.py` - WSGI entry point for Vercel
- ✅ `vercel.json` - Vercel build configuration
- ✅ `requirements.txt` - Python dependencies

### 4. **Python Packaging**
- Added `__init__.py` files to all Python packages:
  - `app/__init__.py`
  - `chain_of_events/__init__.py`
  - `chain_of_events/events/__init__.py`
  - `pol_2_stat/__init__.py`
  - `generaliser/__init__.py`
  - `random_event_gen/__init__.py`
  - `api/__init__.py`

### 5. **Vercel Configuration**
The `vercel.json` is configured to:
- Use the Python runtime via `@vercel/python`
- Route all requests to `api/index.py`
- Serve static files automatically

### 6. **Entry Point**
`api/index.py` imports the Flask app and exports it as `app` for Vercel to use as the WSGI application.

## Deployment Checklist

Before deploying to Vercel:

1. ✅ Folder structure organized with CLI as root
2. ✅ Templates moved to `templates/` folder  
3. ✅ Static files moved to `static/` folder
4. ✅ Imports updated to use relative paths
5. ✅ Python packages initialized with `__init__.py`
6. ✅ `vercel.json` configured correctly
7. ✅ `requirements.txt` lists dependencies
8. ⚠️ TODO: Verify all dependencies in requirements.txt are correct
9. ⚠️ TODO: Test Flask app locally before deploying

## Deployment Options

This project is configured to work on multiple platforms:

- **Vercel**: Use `api/index.py` (serverless)
- **PythonAnywhere**: Use `pythonanywhere_wsgi.py` (see `PYTHONANYWHERE_SETUP.md`)
- **Local**: Use Flask directly (see below)

See `PYTHONANYWHERE_SETUP.md` for detailed PythonAnywhere setup instructions.

## Local Testing

To test locally:

```bash
cd CLI
pip install -r requirements.txt
python app/app.py
```

Or use Flask directly:
```bash
cd CLI
export FLASK_APP=app/app.py
flask run
```

## Notes

- The app will run on `http://localhost:5000` locally
- Vercel will automatically handle routing and WSGI conversion
- Static files in the `static/` folder are served by Vercel automatically
- The `templates/` folder is used by Flask for `render_template()`
