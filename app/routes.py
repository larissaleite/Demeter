from app import app
from config import APP_STATIC

from flask import Flask, render_template, jsonify, make_response, request, flash
from flask_login import login_user, current_user, login_required
from app.models import *
from datetime import datetime

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

	all_recipes = Recipe.objects[:10]

	recipes = []

	for recipe in all_recipes:
		ingredients = []

		for ingredient in recipe['ingredients']:
			ingredients.append({
				'text' : ingredient['full_text']
			})

		recipes.append({
			'title' : recipe['title'],
			'img' : recipe['image'],
			'instructions' : recipe['instructions'],
			'vegetarian' : recipe['vegetarian'],
			'glutenFree' : recipe['glutenFree'],
			'dairyFree' : recipe['dairyFree'],
			'fatFree' : recipe['fatFree'],
			'peanutFree' : recipe['peanutFree'],
			'calories' : recipe['calories'],
			'ingredients' : ingredients
		})

	return render_template("home.html", recipes=recipes)
