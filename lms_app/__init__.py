# __init__.py
from os import path
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from .database import db


DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    # Configure the app with your database URI
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Import views and auth after db initialization to avoid circular imports
    from .views import views
    from .auth import auth

    # Register the views and auth blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/user')

    from .models import User
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('lms_app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')