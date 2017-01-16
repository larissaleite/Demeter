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
dao = Dao('demeter_demo')
recommender = Recommender(dao, sc)

#initializing lists to hold user information
#app.config['user_favorite_recipes'+str(user.user_id)] = []
#app.config['user_recipes_rating'+str(user.user_id)] = dict()

#initializing flask's login manager
login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User

#setting logged in user
@login_manager.user_loader
def load_user(user_id):
	user = User.objects.filter(id=user_id).first()

	global initial_load

	#if not app.config['user_favorite_recipes'+str(user.user_id)]:
	app.config['user_favorite_recipes'+str(user.user_id)] = dao.get_user_favorite_recipes_ids(user.id)

	#if not app.config['user_recipes_rating'+str(user.user_id)]:
	app.config['user_recipes_rating'+str(user.user_id)] = dao.get_user_dict_ratings_ids(user.user_id)

	return user

import routes
import auth
