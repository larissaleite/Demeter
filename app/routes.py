from app import app
from config import APP_STATIC

from flask import Flask, render_template, jsonify, make_response, request, flash
from flask_login import login_user, current_user, login_required
from datetime import datetime
from bson import ObjectId, json_util

from app import dao
from app import recommender
from app import  user_favorite_recipes, user_recipes_rating

@app.route('/', methods = ['GET'])
def index():
	if current_user.is_authenticated:
		return home()
	return render_template('index.html')

@app.route('/home', methods=['GET'])
@login_required
def home():
	global user_favorite_recipes
	global user_recipes_rating

	if not user_favorite_recipes:
		user_favorite_recipes = dao.get_user_favorite_recipes_ids(current_user.id)

	if not user_recipes_rating:
		user_recipes_rating = dao.get_user_ratings_ids(current_user.user_id)

	print user_favorite_recipes
	print user_recipes_rating

	popular_recipes = recommender.get_most_popular_recipes()
	recommended_recipes = recommender.get_recommended_recipes_for_user(current_user.user_id)
	favorite_recipes = dao.get_user_favorite_recipes(current_user.id)

	return render_template("home.html", popular_recipes=popular_recipes, recommended_recipes=recommended_recipes, favorite_recipes=favorite_recipes)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	if request.method == 'GET':
		return render_template('profile.html', user=current_user)
	else:
		age = request.json['age']
		gender = request.json['gender']
		location = request.json['location']
		coordinates = request.json['coordinates']
		restricted_ingredients = request.json['restricted_ingredients']
		preferred_ingredients = request.json['preferred_ingredients']
		diet_labels = request.json['diet_labels']
		favorite_cuisines = request.json['favorite_cuisines']

		dao.set_user(current_user.id, age, gender, location, coordinates, preferred_ingredients, restricted_ingredients, diet_labels, favorite_cuisines)

		return home()

@app.route('/search', methods=['GET', 'POST'])
def search_recipes():
	if request.method == 'GET':
		return render_template('search.html')
	else:
		if 'title' in request.json:
			title = request.json['title']
		else:
			title = None

		if 'labels' in request.json:
			labels = request.json['labels']
		else:
			labels = None

		if 'ingredients' in request.json:
			ingredients = request.json['ingredients']
		else:
			ingredients = None

		if 'cuisines' in request.json:
			cuisines = request.json['cuisines']
		else:
			cuisines = None

		recipes = dao.search_recipes(title, labels, ingredients, cuisines)
		return recipes

@app.route('/recipe/<recipe_id>', methods=['GET'])
@login_required
def get_recipe(recipe_id):
	recipe = dao.get_recipe(recipe_id)

	is_favorite_recipe = False
	rating = 0

	if recipe_id in user_favorite_recipes:
		is_favorite_recipe = True

	if recipe['recipe_id'] in user_recipes_rating:
		rating = user_recipes_rating[str(recipe['recipe_id'])]

	user_recipe_data = {
		'is_favorite_recipe' : is_favorite_recipe,
		'rating' : rating
	}

	return render_template("recipe.html", recipe=recipe, user_data=user_recipe_data)

@app.route('/rating/new', methods=['POST'])
@login_required
def rate_recipe():
	recipe_id = request.json['recipe_id']
	rating = int(request.json['rating'])

	dao.save_user_recipe_rating(current_user.id, recipe_id, rating)

	user_recipes_rating[str(recipe_id)] = rating

	return "Rating added to recipes"

@app.route('/favorite/new', methods=['POST'])
@login_required
def favorite_recipe():
	recipe_id = request.json['recipe_id']

	dao.favorite_recipe(recipe_id, current_user.id)

	if recipe_id not in user_favorite_recipes:
		user_favorite_recipes.append(recipe_id)

	return "Recipe added to favorites"

@app.route('/favorite/delete', methods = ['POST'])
@login_required
def unfavorite_recipe():
	recipe_id = request.json['recipe_id']

	dao.unfavorite_recipe(recipe_id, current_user.id)

	user_favorite_recipes.remove(str(recipe_id))

	return "Unfavorited!"

@app.route('/recipe/reviews', methods = ['GET'])
@login_required
def get_recipe_reviews():
	recipe_id = request.args["recipe_id"]
	reviews = dao.get_recipe_reviews(recipe_id)

	return json_util.dumps({ 'reviews' : reviews })

@app.route('/recipe/review/new', methods = ['POST'])
@login_required
def save_recipe_reviews():
	recipe_id = request.json["recipe_id"]
	review_text = request.json["review"]

	reviews = dao.save_recipe_review(current_user.id, recipe_id, review_text)

	return json_util.dumps({ 'reviews' : reviews })

@app.route('/recipe/review/delete', methods = ['POST'])
@login_required
def delete_review():
	recipe_id = request.json["recipe_id"]
	review_id = request.json["review_id"]

	recipe = dao.delete_recipe_review(recipe_id, review_id)

	return jsonify( { 'recipe': recipe } )

@app.route('/user', methods=['GET'])
@login_required
def get_user():
	user = dao.get_user(current_user.id)
	return jsonify(user=user)

@app.route('/comments_favorites_year', methods=['GET'])
def get_comments_favorites_year():
	country = request.args["country"]

	response = dao.get_analysis_favorites_reviews_year(country)
	return response

@app.route('/recommender', methods=['GET'])
def recommender_demo():
	return render_template('recommender_demo.html')

@app.route('/api/ingredients', methods=['GET'])
def get_ingredients():
	all_ingredients = dao.get_all_ingredients()
	return jsonify( { 'all_ingredients': all_ingredients } )

@app.route('/api/labels', methods=['GET'])
def get_labels():
	all_labels = dao.get_all_labels()
	return jsonify( { 'all_labels': all_labels } )

@app.route('/api/cuisines', methods=['GET'])
def get_cuisines():
	all_cuisines = dao.get_all_cuisines()
	return jsonify( { 'all_cuisines': all_cuisines } )

@app.route('/template_select', methods = ['GET'])
def get_template_select():
	return render_template('template_select.html')

@app.route('/analysis', methods= ['GET'])
def get_dashboard():
	return render_template('dashboard2.html')
