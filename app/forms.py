from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

from app import ALLOWED_EXTENSIONS


class UploadForm(FlaskForm):
    denied = 'Please upload a spreadsheet in the allowed format only.'
    validators = [FileRequired()]
    file = FileField('file', validators=validators)
    submit = SubmitField('upload')
