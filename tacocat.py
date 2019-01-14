from flask import (Flask, render_template,
                   flash, redirect, url_for, g)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user,
                         login_required, logout_user, current_user)

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'


app = Flask(__name__)

app.secret_key = '234802834lsslfwiy324;ljas9-8wrkjb348612r3987t345kjnt3487i'

login_manager = LoginManager()

login_manager.init_app(app)


@app.before_request
def before_request():
    """connect to database before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    g.db.close()
    return response


# This callback is used to reload the
# user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None


@app.route('/register', methods=["GET", "POST"])
def register():
    form = forms.Register()
    if form.validate_on_submit():
        flash('awesome you are registered now create a taco', "success")
        models.User.create_user(
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.Login()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash('oops that email or password does not match our records',category='error')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('you are logged in', category='success')
                return redirect(url_for('index'))
            else:
                flash(flash('oops that email or password does not match our records',category='error'))
    return render_template('login.html', form=form)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    flash('you have been logged out', category='success')
    return redirect(url_for('index'))


@app.route('/taco', methods=['GET', 'POST'])
@login_required
def taco():
    form = forms.TacoOrder()
    if form.validate_on_submit():
        try:
            models.Taco.create_taco(
                user=g.user._get_current_object(),
                protein=form.protein.data,
                shell=form.shell.data,
                cheese=form.cheese.data,
                extras=form.extras.data
           )
        except ValueError:
            flash("looks like we could not produce a taco", category='error')
        else:
            flash('you created a taco', category='success')
            return redirect(url_for('index'))
    return render_template('taco.html', form=form)


@app.route('/', methods=['GET'])
def index():
    tacos = models.Taco.select()
    return render_template('index.html', tacos=tacos)


if __name__ == '__main__':
    models.initialize()
    app.run(PORT, HOST, DEBUG)
