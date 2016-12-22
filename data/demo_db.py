import os, glob, json, random
from bson import ObjectId

def create_users():
	with open("/Users/larissaleite/Documents/Demeter/data/users.json") as json_data:
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

			user = User(
				city=data["City"],
				country=data["Country"],
				email=data["Email"],
				name=data["Full Name"],
				age=age,
				gender=gender,
				preferred_ingredients=preferred_ingredients,
				restricted_ingredients=restricted_ingredients,
				favorite_recipes=favorite_recipes
			)

			user.save()

def create_reviews():
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
		recipe.save()

def create_ratings():
	recipes = Recipe.objects()[:30]

	all_ingredients = set()

	for recipe in recipes:
		ingredients = Recipe.objects.filter(recipe_id=recipe.recipe_id).only("ingredients").first().ingredients

		for ingredient in ingredients:
			all_ingredients.update([ingredient.name])

	all_ingredients = list(all_ingredients)

	users = User.objects()

	for user in users:
		favorite_recipes = []
		preferred_ingredients = []
		restricted_ingredients = []

		for x in range(0,3):
			recipe = random.choice(recipes)
			ingredient_name = random.choice(all_ingredients)

			if recipe not in favorite_recipes:
				favorite_recipes.append(recipe)

			if ingredient_name not in preferred_ingredients:
				ingredient = Ingredient(
					name = ingredient_name
				)
				preferred_ingredients.append(ingredient)

		for x in range(0,3):
			ingredient_name = random.choice(all_ingredients)

			if ingredient_name not in restricted_ingredients and ingredient_name not in preferred_ingredients:
				ingredient = Ingredient(
					name = ingredient_name
				)
				restricted_ingredients.append(ingredient)

		user.update(**{
			'set__favorite_recipes' : favorite_recipes,
			'set__preferred_ingredients':preferred_ingredients,
			'set__restricted_ingredients':restricted_ingredients
		})

		rated_recipes_ids = []

		for x in range(0,5):
			recipe = random.choice(recipes)
			rating = random.uniform(3.5, 5.0)

			if recipe.recipe_id not in rated_recipes_ids:
				rated_recipes_ids.append(recipe.recipe_id)

				user_recipe_rate = RatingIds(
					user_id=user.user_id,
					recipe_id=recipe.recipe_id,
					rating=rating
				)

				user_recipe_rate.save()

def create_recipes():
	#EDAMAM
	for filename in glob.glob('/Users/larissaleite/Documents/Demeter/data/datasets/edamam/*.json'):
		with open(filename) as json_data:
			print filename
			if filename != '/Users/larissaleite/Documents/Demeter/data/datasets/edamam/edamam_recipes.json':
				data = json.load(json_data)

				for recipe_data in data['hits']:

					recipe_data = recipe_data['recipe']

					title = recipe_data['label']

					if Recipe.objects.filter(title=title).first() is None:

						summary = ""
						if 'summary' in recipe_data:
							summary = recipe_data['summary']

						recipe = Recipe(
							title=title,
							image=recipe_data['image'],
							instructions=summary,
							labels=recipe_data["healthLabels"]
						)

						for ingredient in recipe_data['ingredients']:
							full_text=ingredient['text']

							ingredient = ExtendedIngredient(
								name=ingredient['food'],
								amount=ingredient['quantity'],
								unit=ingredient['measure'],
							)

							if full_text is not None and len(full_text) < 490:
								ingredient.full_text = full_text

							recipe.ingredients.append(ingredient)

						recipe.save()

	#SPOONACULAR
	for filename in glob.glob('/Users/larissaleite/Documents/Demeter/data/datasets/spoonacular/*.json'):
		with open(filename) as json_data:
			print filename
			if filename != '/Users/larissaleite/Documents/Demeter/data/datasets/spoonacular/spoonacular_recipes.json':
				data = json.load(json_data)

				for recipe_data in data['recipes']:
					title = recipe_data['title']

					if Recipe.objects.filter(title=title).first() is None:

						instructions = recipe_data['instructions']
						if instructions is not None and len(instructions) > 499:
							instructions = ""
						#check for a better solution for instructions too big

						labels = []

						if recipe_data["vegan"] == 'true':
							labels.append("vegan")
						if recipe_data["vegetarian"] == 'true':
							labels.append("vegetarian")
						if recipe_data["glutenFree"] == 'true':
							labels.append("glutenFree")
						if recipe_data["dairyFree"] == 'true':
							labels.append("dairyFree")

						recipe = Recipe(
							title=title,
							image=recipe_data['image'],
							instructions=instructions,
							labels=labels
						)

						for ingredient in recipe_data['extendedIngredients']:
							category = ""
							if 'aisle' in ingredient:
								category = ingredient['aisle']

							ingredient = ExtendedIngredient(
								name=ingredient['name'],
								amount=ingredient['amount'],
								unit=ingredient['unit']
							)

							metaInformation = ""
							if 'metaInformation' in ingredient:
								metaInformation = ingredient['metaInformation']

							try:
								ingredient.full_text = ' '.join((str(ingredient['amount']), str(ingredient['unit']), str(metaInformation), str(ingredient['name']))).encode('utf-8').strip()

								recipe.ingredients.append(ingredient)
							except:
								continue
						recipe.save()


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

	#create_recipes()
	#create_users()
	create_ratings()
