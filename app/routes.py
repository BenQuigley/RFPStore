import io
import os
import flask
from app.forms import UploadForm
from app import app
from app import factory
from flask import (
        flash,
        redirect,
        render_template,
        request,
        send_from_directory,
        url_for,
)
from werkzeug import secure_filename


def allowed_extension(filename):
    allowed = ('csv')
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed


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
            user_filename = secure_filename(form_file.filename)
            app.logger.info(f"Upload requested: {form_file}")
            if not allowed_extension(user_filename):
                app.logger.info(f"Disallowed filename: {user_filename}")
            else:

                # Then a CSV file has been uploaded. Save it, create an RFP
                # Store file, and serve it back to the user.

                # Strings:
                user_filepath = os.path.join(working_dir, user_filename)
                home_name = 'RFP-store.html'
                target_path = os.path.join(working_dir, home_name)
                page_root = 'rfp-store'
                main_page_name = os.path.join(page_root, home_name)
                app.logger.info(f"Saving file as: {user_filepath}")

                form.file.data.save(user_filepath)
                s = factory.Store(user_filepath)
                s.write_html(target_path)
                app.logger.info(f"Saving output as {target_path}.")
                return flask.send_file(target_path,
                                       mimetype='application/html',
                                       as_attachment=True,
                                       attachment_filename=home_name)

    # This is a one-page web site right now.
    return render_template('home.html', title='Home',
                           form=form)
