import os, glob, json, random, csv

ratings_csv = []

for x in range(0,1000):
    user_id = int(random.uniform(1,100))
    recipe_id = int(random.uniform(1,5000))
    rating = random.uniform(1.0, 5.0)

    ratings_csv.append(str(user_id)+","+str(recipe_id)+","+str(rating))

file = open(os.getcwd()+'/app/ratings.csv', 'wb')
for row in ratings_csv:
    file.write(row+"\n")
file.close()
