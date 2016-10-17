from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user
from mongoengine import *

app = Flask(__name__)

# Configurations
app.config.from_object('config')
db = MongoEngine(app)

login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.objects.filter(id=user_id).first()

import routes
import auth
