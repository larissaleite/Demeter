from mongoengine import *
from app.models import *

from app import recommender
from app import dao

users = User.objects()

for user in users:
    print user.name
    '''print "\n### FAVORITE RECIPES ###"
    for favorite_recipe in user.favorite_recipes:
        recipe = dao.get_recipe(favorite_recipe.id)
        print recipe["title"]
        print "-- Ingredients"
        for ingredient in recipe["ingredients"]:
            print "---- "+ingredient["text"]

    print "\n### FAVORITE INGREDIENTS ###"
    for ingredient in user.preferred_ingredients:
        print ingredient.name

    print "\n### RESTRICTED INGREDIENTS ###"
    for ingredient in user.restricted_ingredients:
        print ingredient.name'''

    print "\n### RATED RECIPES ###"
    user_ratings = RatingIds.objects(user_id=user.user_id).only("recipe_id", "rating")
    for user_rating in user_ratings:
        recipe_data = dao.get_recipes_from_ids([user_rating.recipe_id])

        print str(user_rating.rating) + " -- " + recipe_data[0]["title"]
        '''for ingredient in recipe_data[0]["ingredients"]:
            print "--- " + ingredient["text"]'''

    print "\n ### RECOMMENDATIONS ###"
    recommended_recipes = recommender.get_recommended_recipes_for_user(user.user_id)
    for recipe in recommended_recipes:
        print "("+str(recommended_recipes.index(recipe)+1)+") "+recipe["title"]

    print "\n ######################################### \n"
