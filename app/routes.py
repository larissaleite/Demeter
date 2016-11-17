from app import app
from config import APP_STATIC

from flask import Flask, render_template, jsonify, make_response, request, flash
from flask_login import login_user, current_user, login_required
from app.models import *
from datetime import datetime
from bson import ObjectId, json_util

user_favorite_recipes = []
user_recipes_rating = dict()

@app.route('/', methods = ['GET'])
def index():
	if current_user.is_authenticated:
		return home()
	return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	if request.method == 'GET':
		return render_template('profile.html', user=current_user)
	else:
		return home()

@app.route('/register', methods=['POST'])
def register():
	age = request.json['age']
	gender = request.json['gender']
	location = request.json['location']
	coordinates = request.json['coordinates']
	restrictions = request.json['restrictions']
	ingredients = request.json['ingredients']
	diet_labels = request.json['diet_labels']

	preferred_ingredients = []
	ingredient_restrictions = []

	for ingredient_name in ingredients:
		ingredient = Ingredient(
			name = ingredient_name
		)
		preferred_ingredients.append(ingredient)

	for ingredient_name in restrictions:
		ingredient = Ingredient(
			name = ingredient_name
		)
		ingredient_restrictions.append(ingredient)

	user = User.objects.filter(id=current_user.id).first()

	user.update(**{
		'set__age' : age,
		'set__gender': gender,
		'set__location' : location,
		'set__coordinates' : coordinates,
		'set__preferred_ingredients':preferred_ingredients,
		'set__allergies':ingredient_restrictions,
		'set__diet_labels':diet_labels
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
			'id' : recipe['id'],
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

	user = User.objects.filter(id=str(current_user.id)).first()
	_user_favorite_recipes = user.favorite_recipes

	#try to do it direct in the query, to get only the ids
	for recipe in _user_favorite_recipes:
		if str(recipe.id) not in user_favorite_recipes:
			user_favorite_recipes.append(str(recipe.id))

	ratings = Rating.objects.filter(user=user)
	for rating in ratings:
		if str(rating.recipe.id) not in user_recipes_rating:
			user_recipes_rating[str(rating.recipe.id)] = rating.rating

	print user_favorite_recipes
	print user_recipes_rating

	return render_template("home.html", recipes=recipes)

@app.route('/recipe/<recipe_id>', methods=['GET'])
@login_required
def get_recipe(recipe_id):

	recipe = Recipe.objects.filter(id=str(recipe_id)).first()

	ingredients = []

	for ingredient in recipe['ingredients']:
		ingredients.append({
			'text' : ingredient['full_text']
		})

	recipe = {
		'id' : recipe_id,
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
	}

	all_recipes = Recipe.objects[:4]

	similar_recipes = []

	for similar_recipe in all_recipes:

		similar_recipes.append({
			'id' : similar_recipe['id'],
			'title' : similar_recipe['title'],
			'img' : similar_recipe['image'],
			'instructions' : similar_recipe['instructions'],
			'vegetarian' : similar_recipe['vegetarian'],
			'glutenFree' : similar_recipe['glutenFree'],
			'dairyFree' : similar_recipe['dairyFree'],
			'fatFree' : similar_recipe['fatFree'],
			'peanutFree' : similar_recipe['peanutFree'],
			'calories' : similar_recipe['calories']
		})

	is_favorite_recipe = False
	rating = 0

	if recipe_id in user_favorite_recipes:
		is_favorite_recipe = True

	if recipe_id in user_recipes_rating:
		rating = user_recipes_rating[str(recipe_id)]

	user_data = {
		'is_favorite_recipe' : is_favorite_recipe,
		'rating' : rating
	}

	return render_template("recipe.html", recipe=recipe, similar_recipes=similar_recipes, user_data=user_data)

@app.route('/rating/new', methods=['POST'])
@login_required
def rate_recipe():
	recipe_id = request.json['recipe_id']
	rating = int(request.json['rating'])

	user = User.objects.filter(id=current_user.id).first()
	recipe = Recipe.objects.filter(id=str(recipe_id)).first()

	user_recipe_rate = Rating.objects(user=user, recipe=recipe).first()

	#checks if rating already exists
	if user_recipe_rate is None:

		user_recipe_rate = Rating(
			user=user,
			recipe=recipe,
			rating=rating
		)

		user_recipe_rate.save()
	else:
		user_recipe_rate.update(set__rating=rating)

	user_recipes_rating[str(recipe_id)] = rating
	print user_recipes_rating

	return "Rating added to recipes"

@app.route('/favorite/new', methods=['POST'])
@login_required
def favorite_recipe():
	recipe_id = request.json['recipe_id']

	user = User.objects.filter(id=current_user.id).first()
	recipe = Recipe.objects.filter(id=str(recipe_id)).first()

	user.update(add_to_set__favorite_recipes=recipe)

	if recipe_id not in user_favorite_recipes:
		user_favorite_recipes.append(recipe_id)

	return "Recipe added to favorites"

@app.route('/favorite/delete', methods = ['POST'])
@login_required
def unfavorite_recipe():
	recipe_id = request.json['recipe_id']

	user = User.objects.filter(id=current_user.id).first()
	recipe = Recipe.objects.filter(id=str(recipe_id)).first()

	user.update(pull__favorite_recipes=recipe)

	user_favorite_recipes.remove(str(recipe_id))
	print user_favorite_recipes

	return "Unfavorited!"

@app.route('/api/recipe/reviews', methods = ['GET'])
@login_required
def get_recipe_reviews():
	recipe_id = request.args["recipe_id"]

	recipe = Recipe.objects.filter(id=str(recipe_id)).first()

	reviews = recipe.reviews

	_reviews = []
	for review in reviews:
		_reviews.append({ 'id':review.id, 'text':review.text, 'user_fb_id':review.user.fb_id, 'user_id':str(review.user.id) , 'date':str(review.date) })

	return json_util.dumps({ 'reviews' : _reviews })

@app.route('/api/recipe/review/new', methods = ['POST'])
@login_required
def save_recipe_reviews():
	recipe_id = request.json["recipe_id"]
	review_text = request.json["review"]

	user = User.objects.filter(id=current_user.id).first()

	review_id = ObjectId()

	review = Review(
		id = str(review_id),
		user = user,
		text = review_text
	)

	recipe = Recipe.objects.filter(id=str(recipe_id)).first()

	recipe.reviews.append(review)
	recipe.save()

	_reviews = []
	_reviews.append({ 'id':review.id, 'text':review.text, 'user_fb_id':review.user.fb_id, 'user_id':str(review.user.id) , 'date':str(review.date) })

	return json_util.dumps({ 'reviews' : _reviews })

@app.route('/api/recipe/review/delete', methods = ['POST'])
@login_required
def delete_review():
	recipe_id = request.json["recipe_id"]
	review_id = request.json["review_id"]

	recipe = Recipe.objects(id=str(recipe_id)).update(pull__reviews__id=str(review_id))

	return jsonify( { 'recipe': recipe } )

@app.route('/api/user', methods=['GET'])
def get_user():
	user = User.objects.filter(id=current_user.id).first()

	user = {
		'age' : user.age,
		'gender' : user.gender,
		'location' : user.location,
		'coordinates' : user.coordinates,
		'ingredients' : user.preferred_ingredients,
		'restrictions' : user.allergies,
		'diet_labels' : user.diet_labels
	}

	return jsonify(user=user)

@app.route('/api/ingredients', methods=['GET'])
def get_ingredients():
	all_ingredients = Recipe.objects.distinct(field="ingredients.name")

	return jsonify( { 'all_ingredients': all_ingredients } )

@app.route('/template_select', methods = ['GET'])
def get_template_select():
	return render_template('template_select.html')

@app.route('/template_pagination', methods = ['GET'])
def get_template_pagination():
	return render_template('dirPagination.tpl.html')
