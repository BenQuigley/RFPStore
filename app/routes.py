from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import UploadForm


@app.route('/')
def landing():
    return redirect('/home')


@app.route('/home', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        # flash("Upload requested.")
        return redirect(url_for('index'))
    return render_template('home.html', title='Home',
                           form=form)
