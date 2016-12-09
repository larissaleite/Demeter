def generate_user_ratings():
    import os, glob, json, random, csv

    recipes = Recipe.objects().only("recipe_id")

    ratings_csv = []

    for x in range(0,100000):
        user_id = int(random.uniform(1,10000))
        recipe_id = random.choice(recipes).recipe_id
        rating = random.uniform(1.0, 5.0)

        line = str(user_id)+","+str(recipe_id)+","+str(rating)
        #print line
        ratings_csv.append(line)

    print "creating ratings file"
    file = open(os.getcwd()+'/app/ratings.csv', 'wb')
    for row in ratings_csv:
        file.write(row+"\n")
    file.close()
    print "finished"

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

        generate_user_ratings()
