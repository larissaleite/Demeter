from mongoengine import *
from app.models import *
from pymongo import *
import re

client = MongoClient()
db = client['demeter_v1']

#print Recipe.objects(recipe_id=20000).only("ingredients.name").as_pymongo()
#db.recipe.find({ recipe_id : 20000 }, { "ingredients.name" : 1, _id : 0 })

'''
ingredient = "banana"
title = re.compile(r'banana', re.I)
results = db.recipes.find({ "ingredients" : { "$elemMatch" : {  "name" :  ingredient } }, "title" : { "$regex" : title } })
#print results.count()
#db.recipes.find({ "ingredients" : { "$elemMatch" : {  "name" :  "apple" }}, "title" : "/.*apple.*/i" })

#results = db.analysis_rec.find({ "week_no" : 15 })
pipe = [{ "$match" : { "week_no" : 15, "country" : "France" } }, {"$group" : {"_id":"$week_day", "count":{ "$sum":1}}}]

pipe = [{ "$match" : { "type" : "Comment" } }, {"$group" : {"_id":"$month_name", "count":{ "$sum":1}}}]

results = db.analysis_rec.aggregate(pipeline=pipe)

for result in results:
    print result

print results.count()

print "\n------\n"

#print Recipe.objects(ingredients__name="onion").scalar("recipe_id")
db.recipe.find({  "ingredients" : { "$elemMatch" : {  "name" :  "onion"} }}, { recipe_id : 1, _id : 0 })

print "\n------\n"

print User.objects(id="580e0e4666b3f6140a03b957").only("preferred_ingredients.name", "restricted_ingredients.name").as_pymongo()
#db.user.find({ "_id" : ObjectId('580e0e4666b3f6140a03b957') }, { "preferred_ingredients.name" : 1, "allergies.name" : 1, _id : 0 })

print "\n------\n"

print RatingIds.objects().exclude("id")[:10].as_pymongo()

print RatingIds.objects().scalar("user_id", "recipe_id", "rating")[:10]
'''
