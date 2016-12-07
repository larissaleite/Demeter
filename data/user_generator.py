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
        
    import os, glob, json, random, csv

    ratings_csv = []

    for x in range(0,10000):
        user_id += 1

        recipe_id = int(random.uniform(1,5000))

        '''positive_rating = random.uniform(4.0, 5.0)
        neutral_rating = random.uniform(2.5, 3.9)
        negative_rating = random.uniform(1.0, 2.4)'''

        rating = random.uniform(1.0, 5.0)

        ratings_csv.append(str(user_id)+","+str(recipe_id)+","+str(rating))

    file = open(os.getcwd()+'/app/ratings.csv', 'wb')
    for row in ratings_csv:
        file.write(row+"\n")
    file.close()
