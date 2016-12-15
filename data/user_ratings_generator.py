def create_user_ratings():
	import os, glob, json, random
	from bson import ObjectId

	'''with open("/Users/larissaleite/Documents/Demeter/data/users.json") as json_data:
		ingredients_names = Recipe.objects.distinct(field="ingredients.name")
		recipes = Recipe.objects()

		json_data = json.load(json_data)

		for data in json_data:
			favorite_recipes = []
			preferred_ingredients = []
			restricted_ingredients = []

			for x in range(0,10):
				recipe = random.choice(recipes)
				ingredient_name = random.choice(ingredients_names)

				if recipe not in favorite_recipes:
					favorite_recipes.append(recipe)

				if ingredient_name not in preferred_ingredients:
					ingredient = Ingredient(
						name = ingredient_name
					)
					preferred_ingredients.append(ingredient)

			for x in range(0,10):
				ingredient_name = random.choice(ingredients_names)

				if ingredient_name not in restricted_ingredients and ingredient_name not in preferred_ingredients:
					ingredient = Ingredient(
						name = ingredient_name
					)
					restricted_ingredients.append(ingredient)

			age = random.uniform(13,90)
			gender = random.choice(['F', 'M'])

			location = data["City"]+","+data["Country"]

			user = User(
				location=location,
				email=data["Email"],
				name=data["Full Name"],
				age=age,
				gender=gender,
				preferred_ingredients=preferred_ingredients,
				restricted_ingredients=restricted_ingredients,
				favorite_recipes=favorite_recipes
			)

			user.save()

	#### REVIEWS ####
	recipes = Recipe.objects()
	users = User.objects()

	texts = ["Very easy to make", "Delicious", "My favorite", "Love it!", "I have tried better recipes"]

	for x in range(0,10000):
		user = random.choice(users)
		recipe = random.choice(recipes)
		text = random.choice(texts)

		review = Review(
			id=str(ObjectId()),
			user=user,
			text=text
		)

		recipe.reviews.append(review)
		recipe.save()'''

	##### RATINGS #####
	recipes = Recipe.objects().only("recipe_id")
	users = User.objects().only("user_id")

	for x in range(0,10000):
		user_id = random.choice(users).user_id
		recipe_id = random.choice(recipes).recipe_id
		rating = random.uniform(1.0, 5.0)

		user_recipe_rate = RatingIds(
			user_id=user_id,
			recipe_id=recipe_id,
			rating=rating
		)

		user_recipe_rate.save()


if __name__ == '__main__':
	if __package__ is None:
		import sys

		reload(sys)
		sys.setdefaultencoding('utf-8')

		from os import path
		sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
		from app.models import *
	else:
		from ..app.models import *

	create_user_ratings()
