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
    if request.method == 'POST' and form.validate_on_submit():
        app.logger.info("Form submitted.")
        flash("Upload requested.")
        filename = request.files['file']
        if filename and allowed_file(filename):
            filename = secure_filename(file.filename)
            app.logger.info(f"Saving file as: {filename}")
            form.file.data.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                filename))
        return redirect(url_for('index'))
    else:
        app.logger.info(form.validate_on_submit())
    return render_template('home.html', title='Home',
                           form=form)
