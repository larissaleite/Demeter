from app.recommender.preference_engine import * 
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating

class Recommender:

    def __init__(self, dao, spark):
        self.dao = dao
        self.spark = spark

        self.preference_engine = PreferenceEngine(spark)

    def get_recommended_recipes_for_user(self, user_id):
        all_user_recipe_rating = self.dao.get_all_ratings()

        total_recommendations = 15

        recommended_recipes = self.preference_engine.get_recommended_recipes_for_user(all_user_recipe_rating, user_id, total_recommendations)

        # from the 100, filter and boost to provide the best 10
        '''user = self.dao.get_user(user_id)

        filtered_recommended_recipes = filter(user, recommended_recipes)
        boosted_recommended_recipes = boost(user, filtered_recommended_recipes)

        recommended_recipes = filtered_recommended_recipes'''

        return recommended_recipes[10:]

    def get_similar_recipes(self, recipe):
        # TO IMPLEMENT
        return self.dao.get_most_popular_recipes()

    def filter(self, user, recommended_recipes):
        restrictions = user.allergies
        #how to do that efficiently? -> should be ok since there shouldn't be that many restricted ingredients
        filtered_recommendations = []

        restricted_recipes = []

        for ingredient in restrictions:
            #get all recipes ids that contain these ingredients
            # TODO: implement method in DAO
            ingredient_recipes = dao.get_all_recipes_per_ingredient(ingredient)
            # TODO: insert in restricted recipes (avoid repetition) => set or dictionary?
            restricted_recipes.append(ingredient_recipes)

        unique_restricted_recipes = set(restricted_recipes)

        for recommended_recipe in recommended_recipes:
            if recommended_recipe not in restricted_recipes:
                filtered_recommendations.append(recommended_recipe)

        return filtered_recommendations

    def boost(self, user, recommended_recipes):
        #boost recipe score by 20% for each ingredient in the user's preferred ingredients
        # TODO: also include labels

        preferred_ingredients = user.preferred_ingredients

        for recommended_recipe in recommended_recipes:
            ingredients = dao.get_ingredients_per_recipe
            for ingredient in ingredients:
                if ingredient in preferred_ingredients:
                    recommended_recipe.score += recommended_recipe.score*0.2

        # TODO: re-order
        return recommended_recipes
