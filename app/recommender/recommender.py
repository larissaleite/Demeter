from app.recommender.preference_engine import *
import operator

class Recommender:

    def __init__(self, dao, spark):
        self.dao = dao
        self.spark = spark

        self.preference_engine = PreferenceEngine(spark)

    def get_most_popular_recipes(self):
        all_user_recipe_rating = self.dao.get_all_ratings()
        popular_recipes_ids = self.preference_engine.get_most_popular_recipes(all_user_recipe_rating)
        popular_recipes = self.dao.get_recipes_from_ids(popular_recipes_ids)[:12]

        return popular_recipes

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

        return recommended_recipes

    def get_similar_recipes(self, recipe):
        #TODO IMPLEMENT content-based
        return self.dao.get_most_popular_recipes()

    def filter(self, user, recommended_recipes):
        restrictions = user["restricted_ingredients"]
        favorite_recipes = user["favorite_recipes"]

        print "##### BEFORE FILTERING #####"
        print recommended_recipes
        print "\n"

        filtered_recommendations = []

        #restricted_recipes = set()
        restricted_recipes = []

        for ingredient in restrictions:
            #get all recipes ids that contain these ingredients
            ingredient_recipes = self.dao.get_all_recipes_ids_per_ingredient(ingredient)
            restricted_recipes.append(ingredient_recipes)

        #restricted_recipes = list(restricted_recipes)

        filtered_recommendations = [r for r in recommended_recipes if (r not in restricted_recipes and r not in favorite_recipes)]

        print "##### AFTER FILTERING #####"
        print filtered_recommendations
        print "\n"

        return filtered_recommendations

    def boost(self, user, recommended_recipes):
        #boost recipe score by 20% for each ingredient in the user's preferred ingredients
        # TODO: also include labels

        preferred_ingredients = user["preferred_ingredients"]
        recipe_score_dict = dict()

        boosted = False

        print "#### BOOSTING #####"

        for recommended_recipe in recommended_recipes:
            recipe_score_dict[recommended_recipe] = 1

            ingredients = self.dao.get_ingredients_per_recipe_id(recommended_recipe)

            for ingredient in preferred_ingredients:
                if ingredient in ingredients:
                    boosted = True
                    print "Preferred ingredient [" + ingredient + "] in recipe [" + str(recommended_recipe)+"]"
                    recipe_score_dict[recommended_recipe] += recipe_score_dict[recommended_recipe]*0.2

        if boosted:
            sorted_recipes = sorted(recipe_score_dict.items(), key=operator.itemgetter(1), reverse=True)[:10]

            top_10_recipes = []
            for recipe in sorted_recipes:
                top_10_recipes.append(recipe[0])
        else:
            top_10_recipes = recommended_recipes[:10]

        print top_10_recipes
        print "\n"
        return top_10_recipes
