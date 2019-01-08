from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

from app import ALLOWED_EXTENSIONS


class UploadForm(FlaskForm):
    denied = 'Please upload a spreadsheet in the allowed format only.'
    filename = FileField('file name',
                         validators=[FileRequired(),
                                     FileAllowed(ALLOWED_EXTENSIONS, denied)])
    submit = SubmitField('upload')
