import os, glob, json, requests

def get_data_from_api():

	for x in range(250,300):
		response = requests.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random?limitLicense=false&number=100",
		  headers={
			"X-Mashape-Key": "gRoA2rL1xLmshqs60gDOU8iUfjfMp1lu0uyjsn4vA0zVyylWN0",
			"Accept": "application/json"
		  }
		)

		total = x*100
		print "Writing " +str(total)+ " recipes to folder"

		file = open(os.getcwd()+'/data/datasets/spoonacular/recipes'+str(x)+'.json', 'wb')
		file.write(json.dumps(response.json()))
		file.close()

def save_unique_recipes_to_json():
	recipe_ids = []

	recipes = []

	for filename in glob.glob(os.getcwd()+'/data/datasets/spoonacular/*.json'):
		print "Opening "+filename
		with open(filename) as json_data:
			data = json.load(json_data)

			for recipe_data in data['recipes']:
				id = recipe_data['id']

				if id not in recipe_ids:
					title = recipe_data['title']
					recipe_ids.append(recipe_ids)

					ingredients = []

					for ingredient_data in recipe_data['extendedIngredients']:
						category = ""
						if 'aisle' in ingredient_data:
							category = ingredient_data['aisle']

						ingredient = {
							'name': ingredient_data['name'],
							'amount' : ingredient_data['amount'],
							'unit' : ingredient_data['unit'],
							'category' : category
						}

						ingredients.append(ingredient)

					recipe = {
						'title' : title,
						'vegan': recipe_data["vegan"],
						'vegetarian': recipe_data["vegetarian"],
						'glutenFree': recipe_data["glutenFree"],
						'dairyFree': recipe_data["dairyFree"],
						'ingredients': ingredients,
						'cuisines': recipe_data["cuisines"]
					}

					recipes.append(recipe)

	print len(recipes)

	file = open(os.getcwd()+'/data/datasets/spoonacular/spoonacular_recipes.json', 'wb')
	file.write(json.dumps(recipes))
	file.close()

def insert_data_db():
	for filename in glob.glob(os.getcwd()+'/data/datasets/spoonacular/*.json'):
		with open(filename) as json_data:
			if filename != os.getcwd()+'/data/datasets/spoonacular/spoonacular_recipes.json':
				data = json.load(json_data)

				for recipe_data in data['recipes']:
					title = recipe_data['title']

					if Recipe.objects.filter(title=title).first() is None:

						instructions = recipe_data['instructions']
						if instructions is not None and len(instructions) > 499:
							instructions = ""
						#check for a better solution for instructions too big

						recipe = Recipe(
							title=title,
							image=recipe_data['image'],
							instructions=instructions
						)

						if recipe_data["vegan"] == 'true':
							recipe.vegan = True
						if recipe_data["vegetarian"] == 'true':
							recipe.vegetarian = True
						if recipe_data["glutenFree"] == 'true':
							recipe.glutenFree = True
						if recipe_data["dairyFree"] == 'true':
							recipe.dairyFree = True
						#no fat free or peanut free

						for ingredient in recipe_data['extendedIngredients']:
							category = ""
							if 'aisle' in ingredient:
								category = ingredient['aisle']

							ingredient = ExtendedIngredient(
								name=ingredient['name'],
								amount=ingredient['amount'],
								unit=ingredient['unit'],
								category=category
							)

							metaInformation = ""
							if 'metaInformation' in ingredient:
								metaInformation = ingredient['metaInformation']

							ingredient.full_text = str(ingredient['amount']) + " " + str(ingredient['unit']) + " " + str(metaInformation) + " " + str(ingredient['name'])

							recipe.ingredients.append(ingredient)

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

	#get_data_from_api()
	insert_data_db()
	#save_unique_recipes_to_json()
