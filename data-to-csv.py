from app.models import *
import os, glob, json, random, csv

recipes_csv = []

header = "recipe,vegan,vegetarian,glutenFree,dairyFree,peanutFree,fatFree,calories,rating"

recipes_csv.append(header)

recipes = Recipe.objects()

count = 1

for recipe in recipes:

    row = str(count) + "," + str(recipe['vegan']) + "," + str(recipe['vegetarian']) + "," + str(recipe['glutenFree']) + "," + str(recipe['dairyFree']) + "," + str(recipe['peanutFree'])
    row += "," + str(recipe['fatFree'])  + "," + str(recipe['calories'])

    rating = random.uniform(1.0, 5.0)

    row += "," + str(rating)

    recipes_csv.append(row)

    count += 1

file = open(os.getcwd()+'/data/recipes.csv', 'wb')
for row in recipes_csv:
    file.write(row+"\n")
file.close()
