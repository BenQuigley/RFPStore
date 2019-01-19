import io
import os
import zipfile
import flask
from app.forms import UploadForm
from app import app
from factory import Store
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


def zipdir(path, ziph):
    '''
    Add a directory to a ziph.
    '''
    if not os.path.isdir(path):
        wd = os.getcwd()
        raise Exception(f"{path} is not a path in {wd}; can't make zipdir.")
    for root, dirs, files in os.walk(path):
        for fn in files:
            file_path = os.path.join(root, fn)
            app.logger.info(f"Writing {file_path}")
            ziph.write(file_path)


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
                # Store file, zip the result, and serve it back to the user.

                # Strings:
                user_filepath = os.path.join(working_dir, user_filename)
                home_name = 'index.html'
                target_path = os.path.join(working_dir, home_name)
                page_root = 'rfp-store'
                main_page_name = os.path.join(page_root, home_name)
                app.logger.info(f"Saving file as: {user_filepath}")

                form.file.data.save(user_filepath)
                s = Store(user_filepath)
                s.write_html(target_path)
                app.logger.info(f"Saving output as {target_path}.")
                zip_data = io.BytesIO()
                with zipfile.ZipFile(zip_data, 'w', zipfile.ZIP_DEFLATED) as z:
                    z.write(target_path, arcname=main_page_name)
                    zipdir(page_root, z)
                zip_data.seek(0)
                return flask.send_file(zip_data,
                                       mimetype='application/zip',
                                       as_attachment=True,
                                       attachment_filename='RFP-store.zip')

    # This is a one-page web site right now.
    return render_template('home.html', title='Home',
                           form=form)
