from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                #user looged in
                login_user(user, remember=True)
                flash('Logged in!', 'success')
                return redirect(url_for('views.dashboard'))
            else:
                #wrong password
                flash('Incorect Password!', 'error')
                pass
        else:
            # user not exist!
            flash('User Not Exists!', 'error')
            pass

    return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/signup', methods=["GET", "POST"])
def signup():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        balance = request.form.get('balance')

        #Add data validation
        user = User.query.filter_by(email=email).first()
        if user:
            #Email is already exist!
            flash('Email is already exist', 'error')
            return render_template("signup.html")
        elif len(password) < 6:
            #Check Password
            flash('Password is to short!', 'error')
        elif first_name == "":
            #Check name
            flash('Enter Name', 'error')


        user = User(email=email,
                    password=generate_password_hash(password, method='sha256'),
                    first_name=first_name,
                    balance=balance)

        db.session.add(user)
        db.session.commit()

        flash('Account created!', 'success')
        return redirect(url_for('views.dashboard'))

    return render_template("signup.html")