from app.recommender.preference_engine import *
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
import operator

class Recommender:

    def __init__(self, dao, spark):
        self.dao = dao
        self.spark = spark

        self.preference_engine = PreferenceEngine(spark)

    def get_recommended_recipes_for_user(self, user_id):
        all_user_recipe_rating = self.dao.get_all_ratings()

        total_recommendations = 15

        recommended_recipes_ids = self.preference_engine.get_recommended_recipes_for_user(all_user_recipe_rating, user_id, total_recommendations)

        #self.preference_engine.get_most_popular_recipes(all_user_recipe_rating,total_recommendations)

        # from the 100, filter and boost to provide the best 10
        user = self.dao.get_user("580e0e4666b3f6140a03b957")

        '''filtered_recommended_recipes = filter(user, recommended_recipes)
        boosted_recommended_recipes = boost(user, filtered_recommended_recipes)

        recommended_recipes = filtered_recommended_recipes'''

        filtered_recommended_recipes = self.filter(recommended_recipes_ids)
        recommended_recipes = self.dao.get_recipes_from_ids(recommended_recipes_ids)

        self.boost(user, recommended_recipes_ids)

        return recommended_recipes[:10]

    def get_similar_recipes(self, recipe):
        #TODO IMPLEMENT content-based
        return self.dao.get_most_popular_recipes()

    def filter(self, recommended_recipes):
        # TODO: exclude favorites; get favorites ids
        restrictions = user['restrictions']
        favorites = user['favorite_recipes']
        #restrictions = ["sugar", "salt", "butter"]

        #how to do that efficiently? -> should be ok since there shouldn't be that many restricted ingredients
        filtered_recommendations = []

        restricted_recipes = set()

        for ingredient in restrictions:
            #get all recipes ids that contain these ingredients
            ingredient_recipes = self.dao.get_all_recipes_ids_per_ingredient(ingredient)
            restricted_recipes.update(ingredient_recipes)

        restricted_recipes = list(restricted_recipes)

        #check if order is being kept based on initial scores
        filtered_recommendations = [r for r in recommended_recipes if r not in restricted_recipes]

        return filtered_recommendations

    def boost(self, user, recommended_recipes):
        #boost recipe score by 20% for each ingredient in the user's preferred ingredients
        # TODO: also include labels

        preferred_ingredients = user['ingredients']
        print preferred_ingredients
        recipe_score_dict = dict()

        for recommended_recipe in recommended_recipes:
            recipe_score_dict[recommended_recipe] = 1
            #check if it's necessay to keep getting from the db all the time; see if the query can be done differently
            ingredients = self.dao.get_ingredients_per_recipe_id(recommended_recipe)
            for ingredient in preferred_ingredients:
                if ingredient.name in ingredients:
                    recipe_score_dict[recommended_recipe] += recipe_score_dict[recommended_recipe]*0.2

        sorted_recipes = sorted(recipe_score_dict.items(), key=operator.itemgetter(1), reverse=True)[:10]

        top_10_recipes = []
        for recipe in sorted_recipes:
            top_10_recipes.append(recipe[0])

        return top_10_recipes
