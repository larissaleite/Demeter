import os, glob, json

def save_unique_recipes_to_json():
	recipe_uris = []

	recipes = []

	for filename in glob.glob(os.getcwd()+'/data/datasets/edamam/*.json'):
		print "Opening "+filename
		with open(filename) as json_data:
			if filename != os.getcwd()+'/data/datasets/edamam/edamam_recipes.json':
				data = json.load(json_data)

				for recipe_data in data['hits']:
					recipe_data = recipe_data['recipe']

					uri = recipe_data['uri']

					if uri not in recipe_uris:

						title = recipe_data['label']
						recipe_uris.append(uri)

						ingredients = []

						for ingredient_data in recipe_data['ingredients']:

							ingredient = {
								'name': ingredient_data['food'],
								'amount' : ingredient_data['quantity'],
								'unit' : ingredient_data['measure']
							}

							ingredients.append(ingredient)

						recipe = {
							'title' : title,
							'ingredients': ingredients,
							'labels' : recipe_data['healthLabels'] +recipe_data['dietLabels'],
							'image' : recipe_data['image']
						}

						recipes.append(recipe)

	print len(recipes)

	file = open(os.getcwd()+'/data/datasets/edamam/edamam_recipes.json', 'wb')
	file.write(json.dumps(recipes))
	file.close()

def insert_data_db():
	for filename in glob.glob(os.getcwd()+'/data/datasets/edamam/*.json'):
		with open(filename) as json_data:
			if filename != os.getcwd()+'/data/datasets/edamam/edamam_recipes.json':
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
							calories=recipe_data['calories'],
							instructions=summary
						)

						for label in recipe_data['healthLabels']:
							if label == 'Vegan':
								recipe.vegan = True
							elif label == 'Vegetarian':
								recipe.vegetarian = True
							elif label == 'Gluten-Free':
								recipe.glutenFree = True
							elif label == 'Dairy-Free':
								recipe.dairyFree = True
							elif label == 'Peanut-Free':
								recipe.peanutFree = True
							elif label == 'Fat-Free':
								recipe.fatFree = True

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


if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
		from app.models import *
	else:
		from ..app.models import *

	save_unique_recipes_to_json()
	#insert_data_db()
