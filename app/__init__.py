import logging
import sys

from flask import Flask
from datetime import datetime
from config import Config

app = Flask(__name__)

'''
Logger Settings
'''
app.logger.setLevel(logging.INFO)
app.logger.info("RFP Factory startup.")

'''
App Settings
'''
ALLOWED_EXTENSIONS = set(['txt', 'csv'])
UPLOAD_FOLDER = '/tmp/'

app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


from app import routes  # noqa
