# views.py
from flask import Blueprint, render_template, redirect, url_for
from .auth import auth  # Import the auth blueprint

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/user_login_redirect')
def user_login_redirect():
    return redirect(url_for('auth.user_page'))

@views.route('/user_signup_redirect')
def user_signup_redirect():
    return redirect(url_for('auth.user_page'))
