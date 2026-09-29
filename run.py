# run.py

import os

from app import app

if __name__ == '__main__':
    # Bind to loopback by default to avoid exposing the dev server publicly.
    # Set FLASK_HOST explicitly (e.g. inside a container) if external
    # access is required.
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", "5000"))
    app.run(host=host, port=port)

