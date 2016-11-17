from app.models import *
import os, glob, json, random, csv

recipes_csv = []

header = "recipe,vegan,vegetarian,glutenFree,dairyFree,peanutFree,fatFree,calories,rating"

recipes_csv.append(header)

recipes = Recipe.objects()

for recipe in recipes:
    name = recipe['title'].encode("utf-8")
    name = name.replace(',', '')
    row = str(name) + "," + str(recipe['vegan']) + "," + str(recipe['vegetarian']) + "," + str(recipe['glutenFree']) + "," + str(recipe['dairyFree']) + "," + str(recipe['peanutFree'])
    row += "," + str(recipe['fatFree'])  + "," + str(recipe['calories'])

    rating = random.uniform(1.0, 5.0)

    row += "," + str(rating)

    recipes_csv.append(row)

file = open(os.getcwd()+'/data/recipes.csv', 'wb')
for row in recipes_csv:
    file.write(row+"\n")
file.close()
