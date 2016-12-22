from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
import json

class PreferenceEngine():

	def __init__(self, spark):
		self.spark = spark

	def build_model(self, ratings):
		# Load model
		try:
			#REMOVE!!
			saved_model = ALS.train(ratings, rank, numIterations)
			#saved_model = MatrixFactorizationModel.load(self.spark, "target/tmp/myCollaborativeFilter")
			return saved_model
		except:
			# Load and parse the data

			# Build the recommendation model using Alternating Least Squares
			rank = 5
			numIterations = 10
			model = ALS.train(ratings, rank, numIterations)

			#evaluate_model(model, ratings)

			# Save model
			#model.save(self.spark, "target/tmp/myCollaborativeFilter")

			return model

	def evaluate_model(self, model, ratings):
		# Evaluate the model on training data
		testdata = ratings.map(lambda p: (p[0], p[1]))
		predictions = model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2]))
		ratesAndPreds = ratings.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
		MSE = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
		print("Mean Squared Error = " + str(MSE))

	def get_recommended_recipes_for_user(self, all_user_recipe_rating, user_id):
		ratings_RDD = self.spark.parallelize(all_user_recipe_rating)

		ratings = ratings_RDD.map(lambda row: Rating(int(row[0]), int(row[1]), float(row[1])))

		model = self.build_model(ratings)

		user_rated_recipes = ratings.filter(lambda rating: rating[0]==user_id).map(lambda x: str(x[1]))
		user_unrated_recipes_ids = ratings.map(lambda x: str(x[1])).distinct().subtract(user_rated_recipes)
		user_unrated_recipes = user_unrated_recipes_ids.map(lambda x: (user_id, x)).distinct()

		print "\n RATED"
		print user_rated_recipes.collect()

		print "\n UNRATED"
		print user_unrated_recipes_ids.collect()

		predictions = model.predictAll(user_unrated_recipes).collect()
		recommendations = sorted(predictions, key=lambda x: x[2], reverse=True)[:100]

		#print "\nRECOMMENDATIONS\n"

		products = self.spark.parallelize(recommendations).map(lambda x: x.product).collect()
		#print products
		#print "##########################"

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
