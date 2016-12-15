from mongoengine import *
from app.models import *

print Recipe.objects(recipe_id=20000).only("ingredients.name").as_pymongo()
#db.recipe.find({ recipe_id : 20000 }, { "ingredients.name" : 1, _id : 0 })

print "\n------\n"

print Recipe.objects(ingredients__name="onion").scalar("recipe_id")
#db.recipe.find({  "ingredients" : { "$elemMatch" : {  "name" :  "onion"} }}, { recipe_id : 1, _id : 0 })

print "\n------\n"

print User.objects(id="580e0e4666b3f6140a03b957").only("preferred_ingredients.name", "allergies.name").as_pymongo()
#db.user.find({ "_id" : ObjectId('580e0e4666b3f6140a03b957') }, { "preferred_ingredients.name" : 1, "allergies.name" : 1, _id : 0 })

print "\n------\n"

print RatingTest.objects().exclude("id")[:10].as_pymongo()
