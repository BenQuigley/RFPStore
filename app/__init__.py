import logging
import os
import sys

from config import Config
from datetime import datetime
from flask import Flask

app = Flask(__name__)

'''
Logger Settings
'''

app.logger.setLevel(logging.INFO)
app.logger.info("RFP Factory startup.")

'''
App Settings
'''

ALLOWED_EXTENSIONS = set(['csv'])
UPLOAD_FOLDER = '/tmp/'

app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import routes  # noqa
