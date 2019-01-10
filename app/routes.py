import os
import zipfile

from flask import (
        flash,
        redirect,
        render_template,
        request,
        send_from_directory,
        url_for,
)
from werkzeug import secure_filename

from app import app, allowed_file
from app.forms import UploadForm
from factory import Store


@app.route('/')
def landing():
    return redirect('/home')


@app.route('/home', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    file_ready = None
    if request.method == 'POST':
        valid = form.validate_on_submit()
        if not valid:
            app.logger.info(f"Errors: {form.errors}")
        else:
            app.logger.info("Form submitted.")
            working_dir = app.config['UPLOAD_FOLDER']
            form_file = request.files['file']
            filename = secure_filename(form_file.filename)
            app.logger.info(f"Upload requested: {form_file}")
            if not allowed_file(filename):
                app.logger.info("Disallowed filename: {}".format(filename))
            else:
                local_path = os.path.join(working_dir,
                                          filename)
                app.logger.info(f"Saving file as: {local_path}")
                form.file.data.save(local_path)
                s = Store(local_path)
                target_path = os.path.join(working_dir,
                                           'index.html')
                s.write_html(target_path)
                return send_from_directory(directory=working_dir,
                                           filename='index.html',
                                           as_attachment=True)

    # This is a one-page web site right now.
    return render_template('home.html', title='Home',
                           form=form)
