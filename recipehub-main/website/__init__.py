from flask import Flask, g
from flask_login import LoginManager
import pandas as pd
import json, os
from flask_sqlalchemy import SQLAlchemy
from .models import User
from .database import db

def create_app():
    app = Flask(__name__, static_folder='static')
    DEVELOPMENT = True
    app.secret_key = 'sdfsdgasdg32y35dfujesf42geasca8fg2vnuwfrg'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{"database.db"}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    return app


