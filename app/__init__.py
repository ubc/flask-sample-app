import logging
import os
import platform
from logging.handlers import RotatingFileHandler

from flask import Flask

app = Flask(__name__)

log_dir = os.path.join(os.path.expanduser("~"), ".flask_sample_app")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "flask_sample_app.log")

file_handler = RotatingFileHandler(log_file, maxBytes=1_048_576, backupCount=5)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s [%(name)s] %(message)s"
))
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

app.logger.info(
    "Application starting — host=%s, platform=%s, log_file=%s",
    platform.node(), platform.system(), log_file,
)

from app import routes
