from app.recommender.preference_engine import *
import operator

class Recommender:

    def __init__(self, dao, spark):
        self.dao = dao
        self.spark = spark

        self.preference_engine = PreferenceEngine(spark)

    def get_most_popular_recipes(self):
        #try:
        all_user_recipe_rating = self.dao.get_all_ratings()
        popular_recipes_ids = self.preference_engine.get_most_popular_recipes(all_user_recipe_rating)
        popular_recipes = self.dao.get_recipes_from_ids(popular_recipes_ids)[:12]

        #print popular_recipes
        return popular_recipes
        #except:
        #    return []

    def get_recommended_recipes_for_user(self, user_id):
        #try:
        all_user_recipe_rating = self.dao.get_all_ratings()

        user_ratings = self.dao.get_user_ratings_ids(user_id)

        if len(user_ratings) == 0:
            recommended_recipes_ids = self.preference_engine.get_most_popular_recipes(all_user_recipe_rating)
        else:
            recommended_recipes_ids = self.preference_engine.get_recommended_recipes_for_user(all_user_recipe_rating, user_id)

        # from the 100, filter and boost to provide the best 10

        user = self.dao.get_user_by_id(user_id)

        filtered_recommended_recipes_ids = self.filter(user, recommended_recipes_ids)
        boosted_recommended_recipes_ids = self.boost(user, filtered_recommended_recipes_ids)

        recommended_recipes = self.dao.get_recipes_from_ids(boosted_recommended_recipes_ids)

        #print recommended_recipes
        return recommended_recipes
        #except:
        #    return []

    def get_similar_recipes(self, recipe):
        #TODO IMPLEMENT content-based
        return self.dao.get_most_popular_recipes()

    def filter(self, user, recommended_recipes):
        restrictions = user.restricted_ingredients
        favorite_recipes = user.favorite_recipes

        print recommended_recipes[:10]

        filtered_recommendations = []

        restricted_recipes = set()

        for ingredient in restrictions:
            #get all recipes ids that contain these ingredients
            ingredient_recipes = self.dao.get_all_recipes_ids_per_ingredient(ingredient)
            restricted_recipes.update(ingredient_recipes)

        restricted_recipes = list(restricted_recipes)

        #check if order is being kept based on initial scores
        filtered_recommendations = [r for r in recommended_recipes if r not in restricted_recipes and r not in favorite_recipes]

        print filtered_recommendations[:10]

        return filtered_recommendations

    def boost(self, user, recommended_recipes):
        #boost recipe score by 20% for each ingredient in the user's preferred ingredients
        # TODO: also include labels

        preferred_ingredients = user.preferred_ingredients
        recipe_score_dict = dict()

        for recommended_recipe in recommended_recipes:
            recipe_score_dict[recommended_recipe] = 1
            #check if it's necessay to keep getting from the db all the time; see if the query can be done differently
            ingredients = self.dao.get_ingredients_per_recipe_id(recommended_recipe)
            for ingredient in preferred_ingredients:
                if ingredient in ingredients:
                    recipe_score_dict[recommended_recipe] += recipe_score_dict[recommended_recipe]*0.2

        sorted_recipes = sorted(recipe_score_dict.items(), key=operator.itemgetter(1), reverse=True)[:12]

        top_10_recipes = []
        for recipe in sorted_recipes:
            top_10_recipes.append(recipe[0])

        return top_10_recipes
