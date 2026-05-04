import sys
import os
from pathlib import Path
from threading import Thread

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.chdir(ROOT)

from app.app import create_app, day_update

application = create_app()

day_thread = Thread(target=day_update, daemon=True)
day_thread.start()
