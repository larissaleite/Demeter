import os, glob, json

if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
		from app.models import *
	else:
		from ..app.models import *

for filename in glob.glob(os.getcwd()+'/data/datasets/edamam/*.json'):
	with open(filename) as json_data:
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
