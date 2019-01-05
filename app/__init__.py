import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

from flask import Flask
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
