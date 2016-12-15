def generate_user_ratings():
    import os, glob, json, random, csv

    '''recipes = Recipe.objects().only("recipe_id")
    users = User.objects()

    for x in range(0,100):
        user = random.choice(users)
        recipe_id = random.choice(recipes).recipe_id
        rating = random.uniform(1.0, 5.0)

        user_recipe_rate = RatingTest(
            user=user,
            recipe_id=recipe_id,
            rating=rating
        )

        user_recipe_rate.save()'''

    ratings_csv = []
    ratings = RatingIds.objects()

    for _rating in ratings:
        line = str(_rating.user_id)+","+str(_rating.recipe_id)+","+str(_rating.rating)
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
