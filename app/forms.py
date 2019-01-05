from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    form = StringField('file name', validators=DataRequired)
    submit = SubmitField('Upload')
