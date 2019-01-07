from flask import render_template, flash, redirect, url_for
from werkzeug import secure_filename
from app import app, allowed_file
from app.forms import UploadForm


@app.route('/')
def landing():
    return redirect('/home')


@app.route('/home', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        flash("Upload requested.")
        filename = request.files['file']
        if filename and allowed_file(filename):
            filename = secure_filename(file.filename)
            form.file.data.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                filename))
        return redirect(url_for('index'))
    return render_template('home.html', title='Home',
                           form=form)
