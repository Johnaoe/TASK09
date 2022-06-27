from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os, secrets

basedir = os.path.abspath(os.path.dirname(__file__))

apps = Flask(__name__)
apps.secret_key = secrets.token_urlsafe(32)
apps.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db?check_same_thread=False')
apps.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(apps)
Migrate(apps, db)
admin = Admin(apps)
login_manager = LoginManager(apps)
login_manager.login_view = 'register'
login_manager.login_message_category = 'info'


from mod import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))