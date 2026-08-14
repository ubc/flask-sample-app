# run.py
import os

from app import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001)) # Default to 5000 if PORT env var is not set
    app.run(host='0.0.0.0', port=port)
