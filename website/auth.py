from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_required, login_user, logout_user, current_user, login_manager

auth = Blueprint('auth', __name__)

@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not (email and password):
            flash('Email and password are required.', category='error')
            return redirect(url_for('auth.sign_in'))

        user = User.query.filter_by(email=email).first()
        if user:
            if password and check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("sign_in.html", user=current_user)
            # flash('Signed in successfully', category='success')

@auth.route('/sign-out')
@login_required
def sign_out():
    logout_user()
    flash('You have been signed out.', category='info')
    return redirect(url_for('auth.sign_in'))
    

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if not (email and first_name and password1 and password2):
            flash('All fields are required.', category='error')
            return redirect(url_for('auth.sign_up'))

        if len(email) < 4:
            flash('Email must be at least 4 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be at least 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already exists.', category='error')
            else:
                new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created successfully. You are now signed in.', category='success')
                return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
