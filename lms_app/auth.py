# auth.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__, template_folder='templates/user')

@auth.route('/user_page')
def user_page():
    return render_template('user/user.html')

@auth.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        # Handle user login logic here
        # Example: Check username and password against the database

        username = request.form.get('username')
        password = request.form.get('password')

        # Add your authentication logic here
        # For testing purposes, assume login is successful
        if username == 'testuser' and password == 'testpassword':
            print("Login successful!")  # For debugging purposes

            # Redirect to the user profile page
            return redirect(url_for('auth.user_profile'))

        else:
            print("Login failed!")  # For debugging purposes
            # Handle unsuccessful login, show error message, etc.

    return render_template('user/user.html')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('fullName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(full_name) < 2:
            flash('Full name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, full_name=full_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.user_signup_redirect'))

    return render_template("user/user.html", user=current_user)

@auth.route('/user_profile')
def user_profile():
    return render_template('user/user_profile.html')
