from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
import json

class PreferenceEngine():

	def __init__(self, spark):
		self.spark = spark

	def build_model(self, ratings):
		# Load model
		try:
			saved_model = MatrixFactorizationModel.load(self.spark, "target/tmp/myCollaborativeFilter")
			return saved_model
		except:
			# Load and parse the data

			# Build the recommendation model using Alternating Least Squares
			rank = 5
			numIterations = 10
			model = ALS.train(ratings, rank, numIterations)

			#evaluate_model(model, ratings)

			# Cache
			#model.userFeatures().cache()
			#model.productFeatures().cache()

			# Save model
			#model.save(self.spark, "target/tmp/myCollaborativeFilter")

			return model

	def get_recommended_recipes_for_user(self, all_user_recipe_rating, user_id):
		ratings_RDD = self.spark.parallelize(all_user_recipe_rating)

		ratings = ratings_RDD.map(lambda row: Rating(int(row[0]), int(row[1]), float(row[1])))

		model = self.build_model(ratings)

		user_rated_recipes = ratings.filter(lambda rating: rating[0]==user_id).map(lambda x: str(x[1]))
		user_unrated_recipes_ids = ratings.map(lambda x: str(x[1])).distinct().subtract(user_rated_recipes)
		user_unrated_recipes = user_unrated_recipes_ids.map(lambda x: (user_id, x)).distinct()

		predictions = model.predictAll(user_unrated_recipes).collect()

		recommendations = sorted(predictions, key=lambda x: x[2], reverse=True)[:100]

		products = self.spark.parallelize(recommendations).map(lambda x: x.product).collect()

		return products

	def get_most_popular_recipes(self, all_user_recipe_rating):
		ratings_RDD = self.spark.parallelize(all_user_recipe_rating)

		ratings = ratings_RDD.map(lambda row: Rating(int(row[0]), int(row[1]), float(row[1])))

		# From ratings with tuples of (UserID, RecipeID, Rating) create an RDD with tuples of the (RecipeID, iterable of Ratings for that RecipeID)
		recipeIDsWithRatingsRDD = (ratings
								  .map(lambda (userid, recipeid, rating): (recipeid, rating))
								  .combineByKey(lambda value: (value, 1),
								  lambda x, value: (x[0] + value, x[1] + 1),
								  lambda x, y: (x[0] + y[0], x[1] + y[1])))

		averageByKey = recipeIDsWithRatingsRDD.map(lambda (label, (value_sum, count)): (label, value_sum / count))
		sorted_recipes = sorted(averageByKey.collect(), key=lambda x: x[1], reverse=True)

		top_10_recipes = []
		for recipe in sorted_recipes:
			top_10_recipes.append(recipe[0])

		return top_10_recipes
