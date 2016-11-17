import os, glob, json, requests

def get_data_from_api():

	queries = ["beef", "pork", "chicken", "fish", "salad", "rice", "vegetable", "banana", "potato", "chocolate"]

	for query in queries:

		response = requests.get("http://api.yummly.com/v1/api/recipes?_app_id=ef9ceb39&_app_key=a4c56fdbedb1fabdd6857de6e1860605&q="+query+"&maxResult=500&start=1")

		print "Writing " +query+ " recipes to folder"

		file = open(os.getcwd()+'/data/datasets/yummly/recipes_'+query+'.json', 'wb')
		file.write(json.dumps(response.json()))
		file.close()

def insert_data_db():
	for filename in glob.glob(os.getcwd()+'/data/datasets/yummly/*.json'):
		print "Opening "+filename
		with open(filename) as json_data:
			data = json.load(json_data)

			for recipe_data in data['matches']:

				title = recipe_data['recipeName']

				if Recipe.objects.filter(title=title).first() is None:

					#default image for when there is no images
					image = "https://d30y9cdsu7xlg0.cloudfront.net/png/82540-200.png"

					if 'smallImageUrls' in recipe_data:
						if len(recipe_data['smallImageUrls']) > 0:
							image = recipe_data['smallImageUrls'][0]

					recipe = Recipe(
						title=title,
						image=image
					)

					for ingredient in recipe_data['ingredients']:

						ingredient = ExtendedIngredient(
							name=ingredient
						)

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

	#get_data_from_api()
	insert_data_db()
