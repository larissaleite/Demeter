import os

#importing and initilizing spark
from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName('demeter').setMaster("spark://Larissas-MacBook-Pro.local:7077")
sc = SparkContext(conf=conf)

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user
from mongoengine import *

from app.dao import *

from app.recommender.recommender import *

#instatiating app
app = Flask(__name__)

# Configurations
app.config.from_object('config')
db = MongoEngine(app)

#creating DAO and Recommender objects
dao = Dao('demeter_v1')
recommender = Recommender(dao, sc)

#initializing lists to hold user information
user_favorite_recipes = []
user_recipes_rating = dict()

#initializing flask's login manager
login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User

#setting logged in user
@login_manager.user_loader
def load_user(user_id):
    return User.objects.filter(id=user_id).first()

import routes
import auth
