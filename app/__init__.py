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

ALLOWED_EXTENSIONS = set(['csv'])
UPLOAD_FOLDER = '/tmp/'

app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


'''
Function Declarations
'''

def allowed_file(filename):  # noqa
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def zipdir(path, ziph):
    '''
    Add a directory to a ziph.
    '''
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))




from app import routes  # noqa
