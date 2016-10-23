from app.models import *
import os, glob, json

for filename in glob.glob(os.getcwd()+'/data/*.json'):
	with open(filename) as json_data:
		data = json.load(json_data)

		for recipe_data in data['hits']:

			recipe_data = recipe_data['recipe']

			summary = ""
			if 'summary' in recipe_data:
				summary = recipe_data['summary']

			recipe = Recipe(
				title=recipe_data['label'],
				image=recipe_data['image'],
				calories=recipe_data['calories'],
				instructions=summary
			)

			for label in recipe_data['healthLabels']:
				if label == 'vegan':
					recipe.vegan = True
				elif label == 'vegetarian':
					recipe.vegetarian = True
				elif label == 'gluten-free':
					recipe.glutenFree = True
				elif label == 'dairy-free':
					recipe.dairyFree = True
				elif label == 'peanut-free':
					recipe.peanutFree = True
				elif label == 'fat-free':
					recipe.fatFree = True

			for ingredient in recipe_data['ingredients']:
				ingredient = ExtendedIngredient(
					name=ingredient['food'],
					amount=ingredient['quantity'],
					unit=ingredient['measure'],
					full_text=ingredient['text']
				)
				recipe.ingredients.append(ingredient)

			recipe.save()
