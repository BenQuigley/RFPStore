import os
from flask import render_template, flash, redirect, url_for, request
from werkzeug import secure_filename

from app import app, allowed_file
from app.forms import UploadForm


@app.route('/')
def landing():
    return redirect('/home')


@app.route('/home', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if request.method == 'POST':
        valid = form.validate_on_submit()
        if not valid:
            app.logger.info(f"Errors: {form.errors}")
        else:
            app.logger.info("Form submitted.")
            form_file = request.files['file']
            filename = secure_filename(form_file.filename)
            app.logger.info(f"Upload requested: {form_file}")
            if not allowed_file(filename):
                app.logger.info("Disallowed filename: {}".format(filename))
            else:
                local_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                          filename)
                app.logger.info(f"Saving file as: {local_path}")
                form.file.data.save(local_path)
    # This is a one-page web site right now.
    return render_template('home.html', title='Home',
                           form=form)
