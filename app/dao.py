from app.models import *

class Dao:

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
			#'diet_labels' : user.diet_labels,
			'favorite_recipes' : user.favorite_recipes
		}

		return user

	def get_user_by_id(self, user_id):
		user = User.objects.filter(user_id=user_id).first()

		favorite_recipes = []

		for recipe in user.favorite_recipes:
			favorite_recipes.append(self.get_recipe_id(recipe.id)[0])

		preferred_ingredients = []
		restricted_ingredients = []

		for ingredient in user.preferred_ingredients:
			preferred_ingredients.append(ingredient['name'])

		for ingredient in user.restricted_ingredients:
			restricted_ingredients.append(ingredient['name'])

		user.preferred_ingredients = preferred_ingredients
		user.restricted_ingredients = restricted_ingredients
		user.favorite_recipes = favorite_recipes

		return user

	def get_user_by_fb(self, fb_id):
		user = User.objects(fb_id=fb_id).first()
		return user

	def update_user_fb_token(self, user, fb_token):
		user.update(fb_token=fb_token)
		return user

	def set_user(self, user_id, age, gender, location, coordinates, ingredients, restrictions, diet_labels):
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
			'set__restricted_ingredients':restricted_ingredients
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
		return RatingIds.objects().as_pymongo()

	def get_user_ratings(self, user_id):
		user = User.objects.filter(id=str(user_id)).first()
		ratings = Rating.objects.filter(user=user)

		user_recipes_rating = dict()

		for rating in ratings:
			if str(rating.recipe.id) not in user_recipes_rating:
				user_recipes_rating[str(rating.recipe.id)] = rating.rating

		return user_recipes_rating

	def get_user_ratings_ids(self, user_id):
		return RatingIds.objects(user_id=user_id).as_pymongo()

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

	def get_recipe_ratings(self, recipe_id):
		ratings = RatingIds.objects(recipe_id=str(recipe_id)).scalar("rating")
		return ratings

	# RECIPE
	def get_recipe(self, recipe_id):
		recipe = Recipe.objects.filter(id=str(recipe_id)).first()
		ratings = self.get_recipe_ratings(recipe.recipe_id)

		total_sum = 0

		for rating in ratings:
			total_sum += float(rating)

		avg_rating = "{0:.2f}".format(total_sum/float(len(ratings)))

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
			'ingredients' : ingredients,
			'rating' : avg_rating
		}

		return recipe

	def get_recipe_id(self, recipe_id):
		return Recipe.objects(id=recipe_id).scalar("recipe_id")

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
				'vegetarian' : recipe['vegetarian'],
				'glutenFree' : recipe['glutenFree'],
				'dairyFree' : recipe['dairyFree'],
				'ingredients' : ingredients,
				'instructions' : recipe['instructions']
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

	# INGREDIENTS
	def get_ingredients_per_recipe_id(self, recipe_id):
		ingredients = Recipe.objects.filter(recipe_id=recipe_id).only("ingredients").first().ingredients

		ingredients_names = []
		for ingredient in ingredients:
			ingredients_names.append(ingredient.name)
		return ingredients_names

	def get_all_ingredients(self):
		return Recipe.objects.distinct(field="ingredients.name")
