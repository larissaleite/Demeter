from app import app
from config import APP_STATIC

from flask import Flask, render_template, jsonify, make_response, request, flash
from flask_login import login_user, current_user, login_required
from app.models import *
from datetime import datetime

import requests
import logging

#check error Broken Pipe with requests lib
logging.getLogger('requests').setLevel(logging.CRITICAL)


headers = {
	"X-Mashape-Key": "62t27Bg1q7mshtmPnpbNVMOAVw9Tp1PkKrqjsnebv8Ph00q2x3",
	"Accept": "application/json"
}

@app.route('/', methods = ['GET'])
def index():
	if current_user.is_authenticated:
		return home()
	return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
	if request.method == 'GET':
		return render_template('profile.html', user=current_user)
	else:
		return home()

@app.route('/register', methods=['POST'])
def register():
	age = request.form['age']
	gender = request.form['gender']
	location = request.form['location']

	user = User.objects.filter(id=current_user.id).first()

	user.update(**{
		'set__age' : age,
		'set__gender': gender,
		'set__location' : location
	})

	return home()


@app.route('/home', methods=['GET'])
@login_required
def home():
	response = requests.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random?limitLicense=false&number=5", headers=headers)
	data = response.json()

	recipes = []

	for recipe in data['recipes']:
		ingredients = []

		for ingredient in recipe['extendedIngredients']:
			ingredients.append({
				'text' : str(ingredient['amount']) + " " + ingredient['unit'] + " of " + ingredient['name']
			})

		recipes.append({
			'title' : recipe['title'],
			'img' : recipe['image'],
			'instructions' : recipe['instructions'],
			'vegetarian' : recipe['vegetarian'],
			'glutenFree' : recipe['glutenFree'],
			'dairyFree' : recipe['dairyFree'],
			'ingredients' : ingredients
		})

	return render_template("home.html", recipes=recipes)
