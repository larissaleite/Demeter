from app.recommender.preference_engine import *
import operator
from random import shuffle

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

	def get_similar_recipes_for_user(self, user):
		rated_recipes = self.dao.get_user_ratings_recipe_ids(user.user_id)
		favorite_recipes = self.dao.get_user_favorite_recipes_ids(user.id)

		recipes_user_likes = list(set(rated_recipes).union(favorite_recipes))

		content_recommended_recipes = self.dao.get_recommended_recipes(recipes_user_likes)

		similar_recipes = [r for r in content_recommended_recipes if r not in recipes_user_likes]

		shuffle(similar_recipes)

		recommended_recipes = self.dao.get_recipes_from_oids(similar_recipes[:12])

		return recommended_recipes

	def get_recommended_recipes_for_user(self, user_id):
		all_user_recipe_rating = self.dao.get_all_ratings()

		user_ratings = self.dao.get_user_ratings_ids(user_id)

		if len(user_ratings) == 0:
			recommended_recipes_ids = self.preference_engine.get_most_popular_recipes(all_user_recipe_rating)
		else:
			recommended_recipes_ids = self.preference_engine.get_recommended_recipes_for_user(all_user_recipe_rating, user_id)

		# from the 100, filter and boost to provide the best 12

		user = self.dao.get_user_by_id(user_id)

		filtered_recommended_recipes_ids = self.filter(user, recommended_recipes_ids)
		boosted_recommended_recipes_ids = self.boost(user, filtered_recommended_recipes_ids)

		recommended_recipes = self.dao.get_recipes_from_ids(boosted_recommended_recipes_ids)

		return recommended_recipes

	def filter(self, user, recommended_recipes):
		restrictions = user["restricted_ingredients"]
		favorite_recipes = user["favorite_recipes"]

		filtered_recommendations = []

		restricted_recipes = []

		for ingredient in restrictions:
			#get all recipes ids that contain these ingredients
			ingredient_recipes = self.dao.get_all_recipes_ids_per_ingredient(ingredient)
			restricted_recipes.append(ingredient_recipes)

		filtered_recommendations = [r for r in recommended_recipes if (r not in restricted_recipes and r not in favorite_recipes)]

		return filtered_recommendations

	def boost(self, user, recommended_recipes):
		preferred_ingredients = user["preferred_ingredients"]
		favorite_cuisines = user["favorite_cuisines"]
		diet_labels = user["diet_labels"]

		recipe_score_dict = dict()

		boosted = False

		for recommended_recipe in recommended_recipes:
			recipe_score_dict[recommended_recipe] = 1

			recipe_data = self.dao.get_ingredients_labels_cuisines_recipe(recommended_recipe)

			ingredients = recipe_data['ingredients']
			cuisines = recipe_data['cuisines']
			labels = recipe_data['labels']

			for ingredient in preferred_ingredients:
				if ingredient in ingredients:
					boosted = True
					recipe_score_dict[recommended_recipe] += recipe_score_dict[recommended_recipe]*0.2

			for cuisine in favorite_cuisines:
				if cuisine in cuisines:
					boosted = True
					recipe_score_dict[recommended_recipe] += recipe_score_dict[recommended_recipe]*0.2

			for label in diet_labels:
				if label in labels:
					boosted = True
					recipe_score_dict[recommended_recipe] += recipe_score_dict[recommended_recipe]*0.2

		if boosted:
			sorted_recipes = sorted(recipe_score_dict.items(), key=operator.itemgetter(1), reverse=True)[:12]

			top_12_recipes = []
			for recipe in sorted_recipes:
				top_12_recipes.append(recipe[0])
		else:
			top_12_recipes = recommended_recipes[:12]

		return top_12_recipes
