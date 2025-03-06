from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models import User
from app.forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)  
            return redirect(url_for('main.index')) 
        else:
            flash('Неверные имя пользователя или пароль', 'error')

    return render_template('auth/login.html', form=form)


@login_required  
@auth.route('/logout')
def logout():
    logout_user()  
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)

        user = User(
            username=form.username.data,
            password=hashed_password,
            email=form.email.data
        )
    	
        db.session.add(user)
        db.session.commit()

        login_user(user)

        return redirect(url_for('main.index'))

    return render_template('auth/register.html', form=form)