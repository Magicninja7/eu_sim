# PythonAnywhere Setup Guide

## Step-by-Step Setup on PythonAnywhere

### 1. Upload Your Code
- Create a new bash console on PythonAnywhere
- Clone or upload your stavanger_app to your home directory
- Path should be: `/home/yourusername/stavanger_app/web/CLI`

### 2. Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 stavanger_app
pip install flask==3.0.0 werkzeug==3.0.0
```

### 3. Configure the Web App
1. Go to **Web** tab on PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose **Manual configuration**
4. Select **Python 3.10** (or your preferred version)
5. Click **Next**

### 4. Set Up WSGI File
1. PythonAnywhere generates a WSGI file at: `/var/www/yourusername_pythonanywhere_com_wsgi.py`
2. Open that file and replace its contents with the content from `pythonanywhere_wsgi.py` in this directory
3. **Important**: Update the `path` variable to your actual path:
   ```python
   path = '/home/yourusername/stavanger_app/web/CLI'
   ```

### 5. Configure Static Files
In the Web app settings:

1. Go to **Static files** section
2. Add a mapping:
   - **URL**: `/static/`
   - **Directory**: `/home/yourusername/stavanger_app/web/CLI/static`

3. Add another mapping for templates if needed:
   - **URL**: `/templates/`
   - **Directory**: `/home/yourusername/stavanger_app/web/CLI/templates`

### 6. Configure Virtual Environment
In the Web app settings:
- Set **Virtualenv path** to: `/home/yourusername/.virtualenvs/stavanger_app`

### 7. Reload
Click the **Reload** button (big green button at the top of the Web tab)

### 8. Test
Visit: `https://yourusername.pythonanywhere.com`

## Troubleshooting

### Import Errors
If you get import errors, check:
1. Virtual environment is activated
2. All dependencies are installed: `pip list`
3. Path in WSGI file is correct
4. All `__init__.py` files exist in your packages

### Static Files Not Loading
1. Verify static files mapping is correct
2. Check that `/static/styles.css` and `/static/app.js` exist
3. Reload the web app after making changes

### Module Not Found
This usually means the path in the WSGI file is wrong. It should point to the CLI directory:
```python
path = '/home/yourusername/stavanger_app/web/CLI'
```

### Permissions Error
Run in bash console:
```bash
chmod 755 /home/yourusername/stavanger_app
chmod 755 /home/yourusername/stavanger_app/web
chmod 755 /home/yourusername/stavanger_app/web/CLI
```

## Environment Variables
If you need to set environment variables (like `FLASK_ENV`):

In the WSGI file, add before creating the app:
```python
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_DEBUG'] = '0'
```

## Key Differences from Vercel

| Feature | Vercel | PythonAnywhere |
|---------|--------|----------------|
| Entry Point | `api/index.py` | WSGI file |
| Static Files | Auto-served | Manual mapping |
| Environment | Serverless | Always-on |
| Python Version | Auto-managed | User selects |
| Console Access | Limited | Full bash console |

## File Structure Check

Your project should have this structure for PythonAnywhere:

```
/home/yourusername/stavanger_app/web/CLI/
├── app/
│   ├── __init__.py
│   └── app.py
├── templates/
│   └── index.html
├── static/
│   ├── styles.css
│   └── app.js
├── chain_of_events/
├── pol_2_stat/
├── generaliser/
├── random_event_gen/
├── requirements.txt
└── pythonanywhere_wsgi.py (this file)
```

## Full Requirements.txt
Make sure your `requirements.txt` includes all dependencies:

```
flask==3.0.0
werkzeug==3.0.0
```

Add any other imports your `app.py` uses (e.g., if you import pandas, numpy, etc.)
