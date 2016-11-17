import os, glob, json, requests

def get_data_from_api():

	for x in range(1,35):
		response = requests.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random?limitLicense=false&number=100",
		  headers={
			"X-Mashape-Key": "62t27Bg1q7mshtmPnpbNVMOAVw9Tp1PkKrqjsnebv8Ph00q2x3",
			"Accept": "application/json"
		  }
		)

		total = x*100
		print "Writing " +str(total)+ " recipes to folder"

		file = open(os.getcwd()+'/data/datasets/spoonacular/recipes'+str(x)+'.json', 'wb')
		file.write(json.dumps(response.json()))
		file.close()

def insert_data_db():
	for filename in glob.glob(os.getcwd()+'/data/datasets/spoonacular/*.json'):
		print "Opening "+filename
		with open(filename) as json_data:
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

					if recipe["vegan"] == 'true':
						recipe.vegan = True
					if recipe["vegetarian"] == 'true':
						recipe.vegetarian = True
					if recipe["glutenFree"] == 'true':
						recipe.glutenFree = True
					if recipe["dairyFree"] == 'true':
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
