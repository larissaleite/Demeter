from app.models import *

class Dao:

	# USER
	def create_user(self, fb_id, first_name, last_name, access_token):
		user = User(
			fb_id=fb_id,
			first_name=first_name,
			last_name=last_name,
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
			'ingredients' : user.preferred_ingredients,
			'restrictions' : user.allergies,
			'diet_labels' : user.diet_labels
		}

		return user

	def get_user_by_fb(self, fb_id):
		user = User.objects(fb_id=fb_id).first()
		return user

	def update_user_fb_token(self, user, fb_token):
		user.update(fb_token=fb_token)
		return user

	def set_user(self, user_id, age, gender, location, coordinates, ingredients, restrictions, diet_labels):
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

		user = User.objects.filter(id=user_id).first()

		user.update(**{
			'set__age' : age,
			'set__gender': gender,
			'set__location' : location,
			'set__coordinates' : coordinates,
			'set__preferred_ingredients':preferred_ingredients,
			'set__allergies':ingredient_restrictions,
			'set__diet_labels':diet_labels
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
		user = User.objects.filter(id=str(user_id)).first()
		_user_favorite_recipes = user.favorite_recipes

		user_favorite_recipes = []

		#try to do it direct in the query, to get only the ids
		for recipe in _user_favorite_recipes:
			if str(recipe.id) not in user_favorite_recipes:
				user_favorite_recipes.append(str(recipe.id))

		return user_favorite_recipes

	# RATING
	def get_all_ratings(self):
		return Rating.objects()

	def get_user_ratings(self, user_id):
		user = User.objects.filter(id=str(user_id)).first()
		ratings = Rating.objects.filter(user=user)

		user_recipes_rating = dict()

		for rating in ratings:
			if str(rating.recipe.id) not in user_recipes_rating:
				user_recipes_rating[str(rating.recipe.id)] = rating.rating

		return user_recipes_rating

	def save_user_recipe_rating(self, user_id, recipe_id, rating):
		user = User.objects.filter(id=user_id).first()
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

	# RECIPE
	def get_recipe(self, recipe_id):
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

		return recipe

	def get_most_popular_recipes(self):
		#still needs to be implemented
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

		return recipes

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

	# INGREDIENTS
	def get_all_ingredients(self):
		return Recipe.objects.distinct(field="ingredients.name")
