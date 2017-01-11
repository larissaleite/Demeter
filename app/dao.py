from app.models import *
from bson import json_util
from bson.json_util import dumps
import json
from pymongo import *
import re

class Dao:

	def __init__(self, db):
		client = MongoClient()
		self.db = client[db]

	# USER
	def create_user(self, fb_id, name, access_token):
		user = User(
			fb_id=fb_id,
			name=name,
			fb_token=access_token
		)
		user.save()
		return user

	def get_user(self, user_id):
		user = User.objects.filter(id=user_id).first()

		user = {
			'age' : user.age,
			'gender' : user.gender,
			'location' : user.location,
			'coordinates' : user.coordinates,
			'preferred_ingredients' : user.preferred_ingredients,
			'restricted_ingredients' : user.restricted_ingredients,
			'diet_labels' : user.diet_labels,
			'favorite_cuisines' : user.favorite_cuisines,
			'favorite_recipes' : user.favorite_recipes
		}

		return user

	def get_users(self):
		return User.objects()

	def get_user_by_id(self, user_id):
		user_data = User.objects.filter(user_id=user_id).first()

		favorite_recipes = []

		for recipe in user_data.favorite_recipes:
			favorite_recipes.append(self.get_recipe_id(recipe.id))

		preferred_ingredients = []
		restricted_ingredients = []

		for ingredient in user_data.preferred_ingredients:
			preferred_ingredients.append(ingredient['name'])

		for ingredient in user_data.restricted_ingredients:
			restricted_ingredients.append(ingredient['name'])

		user = dict()

		user["preferred_ingredients"] = preferred_ingredients
		user["restricted_ingredients"] = restricted_ingredients
		user["favorite_recipes"] = favorite_recipes
		user["favorite_cuisines"] = user_data.favorite_cuisines
		user["diet_labels"] = user_data.diet_labels

		return user

	def get_user_by_fb(self, fb_id):
		user = User.objects(fb_id=fb_id).first()
		return user

	def update_user_fb_token(self, user, fb_token):
		user.update(fb_token=fb_token)
		return user

	def set_user(self, user_id, age, gender, location, coordinates, ingredients, restrictions, diet_labels, favorite_cuisines):
		preferred_ingredients = []
		restricted_ingredients = []

		for ingredient_name in ingredients:
			ingredient = Ingredient(
				name = ingredient_name
			)
			preferred_ingredients.append(ingredient)

		for ingredient_name in restrictions:
			ingredient = Ingredient(
				name = ingredient_name
			)
			restricted_ingredients.append(ingredient)

		user = User.objects.filter(id=user_id).first()

		user.update(**{
			'set__age' : age,
			'set__gender': gender,
			'set__location' : location,
			'set__coordinates' : coordinates,
			'set__preferred_ingredients':preferred_ingredients,
			'set__restricted_ingredients':restricted_ingredients,
			'set__diet_labels':diet_labels,
			'set__favorite_cuisines' : favorite_cuisines
		})

	def favorite_recipe(self, recipe_id, user_id):
		user = User.objects.filter(id=user_id).first()
		recipe = Recipe.objects.filter(id=str(recipe_id)).first()

		user.update(add_to_set__favorite_recipes=recipe)

	def unfavorite_recipe(self, recipe_id, user_id):
		user = User.objects.filter(id=user_id).first()
		recipe = Recipe.objects.filter(id=str(recipe_id)).first()

		user.update(pull__favorite_recipes=recipe)

	def get_user_favorite_recipes(self, user_id):
		favorite_recipes = self.get_user_favorite_recipes_ids(user_id)
		recipes = []

		for recipe_id in favorite_recipes:
			recipes.append(self.get_recipe(recipe_id))

		return recipes

	def get_user_favorite_recipes_ids(self, user_id):
		user = User.objects.filter(id=str(user_id)).first()
		recipe_ids = []

		for recipe in user.favorite_recipes:
			recipe_ids.append(str(recipe.id))
		return recipe_ids

	# RATING
	def get_all_ratings(self):
		return RatingIds.objects().scalar("user_id", "recipe_id", "rating")

	def get_user_ratings_ids(self, user_id):
		return RatingIds.objects(user_id=user_id).as_pymongo()

	def save_user_recipe_rating(self, user_id, recipe_id, rating):
		user = User.objects.filter(id=user_id).first()
		recipe = Recipe.objects.filter(id=str(recipe_id)).first()

		user_recipe_rate = RatingIds.objects(user_id=user.user_id, recipe_id=recipe.recipe_id).first()

		#checks if rating already exists
		if user_recipe_rate is None:

			user_recipe_rate = RatingIds(
				user_id=user.user_id,
				recipe_id=recipe.recipe_id,
				rating=rating
			)

			user_recipe_rate.save()
		else:
			user_recipe_rate.update(set__rating=rating)

	def get_recipe_ratings(self, recipe_id):
		ratings = RatingIds.objects(recipe_id=str(recipe_id)).scalar("rating")
		return ratings

	def get_user_ratings_recipe_ids(self, user_id):
		 recipe_ids = RatingIds.objects(user_id=user_id).scalar("recipe_id")
		 recipe_oids = Recipe.objects(recipe_id__in=recipe_ids).scalar("id")
		 return [str(id) for id in recipe_oids]

	# RECIPE
	def get_recipe(self, recipe_id):
		recipe = Recipe.objects.filter(id=str(recipe_id)).first()
		ratings = self.get_recipe_ratings(recipe.recipe_id)

		total_sum = 0

		for rating in ratings:
			total_sum += float(rating)
		try:
			avg_rating = "{0:.2f}".format(total_sum/float(len(ratings)))
		except:
			avg_rating = 0

		ingredients = []

		for ingredient in recipe['ingredients']:
			ingredients.append({
				'text' : str(ingredient['amount']) + " " + str(ingredient['unit']) + " " + str(ingredient['name'])
			})

		recommended_recipes = recipe['recommended_recipes'][:4]

		similar_recipes = []

		for recommended_recipe in recommended_recipes:
			similar_recipe = Recipe.objects().filter(id=recommended_recipe.id).only("title", "image", "id").as_pymongo()
			similar_recipes.append(similar_recipe[0])

		recipe = {
			'id' : recipe_id,
			'recipe_id' : recipe['recipe_id'],
			'title' : recipe['title'],
			'img' : recipe['image'],
			'labels' : recipe['labels'],
			'cuisines' : recipe['cuisines'],
			'ingredients' : ingredients,
			'rating' : avg_rating,
			'recommended_recipes' : similar_recipes
		}

		return recipe

	def get_recipe_id(self, recipe_id):
		recipe_id = Recipe.objects(id=recipe_id).scalar("recipe_id").first()
		return recipe_id

	def get_recipes_from_ids(self, recipes_ids):
		all_recipes = Recipe.objects.filter(recipe_id__in=recipes_ids)

		recipes = []

		for recipe in all_recipes:
			ingredients = []

			for ingredient in recipe['ingredients']:
				ingredients.append({
					'text' : ingredient['full_text']
				})

			recipes.append({
				'id' : recipe['id'],
				'img' : recipe['image'],
				'title' : recipe['title'],
				'labels' : recipe['labels'],
				'cuisines' : recipe['cuisines'],
				'ingredients' : ingredients
			})

		return recipes

	def get_recipes_from_oids(self, recipes_ids):
		all_recipes = Recipe.objects.filter(id__in=recipes_ids)

		recipes = []

		for recipe in all_recipes:
			ingredients = []

			for ingredient in recipe['ingredients']:
				ingredients.append({
					'text' : ingredient['full_text']
				})

			recipes.append({
				'id' : recipe['id'],
				'img' : recipe['image'],
				'title' : recipe['title'],
				'labels' : recipe['labels'],
				'cuisines' : recipe['cuisines'],
				'ingredients' : ingredients
			})

		return recipes

	def get_all_recipes_ids_per_ingredient(self, ingredient):
		return Recipe.objects(ingredients__name=ingredient).scalar("recipe_id")

	def get_recipe_reviews(self, recipe_id):
		recipe = Recipe.objects.filter(id=str(recipe_id)).first()

		reviews = recipe.reviews

		_reviews = []
		for review in reviews:
			_reviews.append({ 'id':review.id, 'text':review.text, 'user_fb_id':review.user.fb_id, 'user_id':str(review.user.id) , 'date':str(review.date) })
		return _reviews

	def save_recipe_review(self, user_id, recipe_id, text):
		user = User.objects.filter(id=user_id).first()

		review_id = ObjectId()

		review = Review(
			id = str(review_id),
			user = user,
			text = text
		)

		recipe = Recipe.objects.filter(id=str(recipe_id)).first()

		recipe.reviews.append(review)
		recipe.save()

		_reviews = []
		_reviews.append({ 'id':review.id, 'text':review.text, 'user_fb_id':review.user.fb_id, 'user_id':str(review.user.id) , 'date':str(review.date) })

	def delete_recipe_review(self, recipe_id, review_id):
		return Recipe.objects(id=str(recipe_id)).update(pull__reviews__id=str(review_id))

	def search_recipes(self, title, labels, ingredients, cuisines):
		query = {}

		if title:
			title = re.compile(title, re.I)
			query['title'] = { "$regex" : title }

		if labels:
			query['labels'] = { "$in" : labels }

		if cuisines:
			query['cuisines'] = { "$in" : cuisines }

		if ingredients:
			query['ingredients'] = { "$elemMatch" : {  "name" :  { "$in" : ingredients } } }

		results = self.db.recipe.find(query)
		print results.count()
		return dumps(results)

	def get_ingredients_labels_cuisines_recipe(self, recipe_id):
		recipe = Recipe.objects.filter(recipe_id=recipe_id).only("labels", "cuisines", "ingredients").first()

		ingredients_names = []
		for ingredient in recipe.ingredients:
			ingredients_names.append(ingredient.name)

		recipe_data = {
			'ingredients' : ingredients_names,
			'labels' : recipe.labels,
			'cuisines' : recipe.cuisines
		}

		return recipe_data

	def get_recommended_recipes(self, recipes_ids):
		recipes = Recipe.objects(id__in=recipes_ids).only("recommended_recipes")

		recommended_recipes_ids = []

		for recipe in recipes:
			for recommended_recipe in recipe.recommended_recipes:
				recommended_recipes_ids.append(str(recommended_recipe.id))

		return list(set(recommended_recipes_ids))

	# INGREDIENTS
	def get_ingredients_per_recipe_id(self, recipe_id):
		ingredients = Recipe.objects.filter(recipe_id=recipe_id).only("ingredients").first().ingredients

		ingredients_names = []
		for ingredient in ingredients:
			ingredients_names.append(ingredient.name)
		return ingredients_names

	def get_all_ingredients(self):
		return Recipe.objects.distinct(field="ingredients.name")

	def get_all_labels(self):
		return Recipe.objects.distinct(field="labels")

	def get_all_cuisines(self):
		return Recipe.objects.distinct(field="cuisines")

	def get_analysis_favorites_reviews_year(self, country):
		if country != "All":
			pipe = [{ "$match" : { "country" : country } }, {"$group" : {"_id":"$month_name", "count_fav":{ "$sum":1}}}]
		else:
			pipe = [{"$group" : {"_id":"$month_name", "count":{ "$sum":1}}}]

		results = self.db.analysis_rec.aggregate(pipeline=pipe)
		return dumps(results)
