from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating

class PreferenceEngine():

	def __init__(self, spark):
		self.spark = spark

	def build_model(self, all_user_recipe_rating):
		# Load model
		try:
			saved_model = MatrixFactorizationModel.load(self.spark, "target/tmp/myCollaborativeFilter")
			return saved_model
		except:
			# Load and parse the data
			data = self.spark.textFile("/Users/larissaleite/Documents/Demeter/app/ratings.csv") #use ratings after!
			ratings = data.map(lambda l: l.split(','))\
				.map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2])))

			# Build the recommendation model using Alternating Least Squares
			rank = 5
			numIterations = 10
			model = ALS.train(ratings, rank, numIterations)

			#evaluate_model(model, ratings)

			# Save model
			#model.save(sc, "target/tmp/myCollaborativeFilter")

			return model

	def evaluate_model(self, model, ratings):
		# Evaluate the model on training data
		testdata = ratings.map(lambda p: (p[0], p[1]))
		predictions = model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2]))
		ratesAndPreds = ratings.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
		MSE = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
		print("Mean Squared Error = " + str(MSE))

	def get_recommended_recipes_for_user(self, all_user_recipe_rating, user_id, total_recommendations):
		'''model = self.build_model(all_user_recipe_rating)

		data = self.spark.textFile("/Users/larissaleite/Documents/Demeter/app/ratings.csv") #use ratings after!
		ratings = data.map(lambda l: l.split(','))\
			.map(lambda l: Rating(int(l[0]), str(l[1]), float(l[2])))

		#rated_recipes_ids = ratings.filter(lambda rating: rating[0]==user_id).map(lambda x: str(x[1])).distinct().collect()
		unrated_recipes_ids = ratings.filter(lambda rating: not rating[0]==user_id).map(lambda x: str(x[1])).distinct()#.collect()
		#candidates = self.spark.parallelize([r for r in unrated_recipes_ids if r not in rated_recipes_ids])
		#to transform in an array and print, just put .collect() after

		predictions = model.predictAll(unrated_recipes_ids.map(lambda x: (user_id, x))).collect()
		recommendations = sorted(predictions, key=lambda x: x[2], reverse=True)[:100]

		print "\nRECOMMENDATIONS\n"

		print str(recommendations)+"\n"
		products = self.spark.parallelize(recommendations).map(lambda x: x.product).collect()
		print products
		return products'''
		recommendations = [14867, 19572, 15578, 10291, 18994, 15756, 14451, 16070, 8413, 14631, 21162, 12971, 12016, 13946, 14818, 14973, 16402, 19501, 14939, 8939, 9087, 13183, 19470, 7900, 11025, 9548, 8612, 9569, 15763, 16349, 16460, 7971, 7791, 20532, 8414, 9878, 17722, 6346, 9516, 15040, 9482, 17351, 6352, 20661, 19172, 15546, 7580, 11156, 15906, 14576, 13819, 8882, 6367, 20777, 16906, 20282, 7780, 13173, 16055, 16777, 14272, 21874, 16178, 6929, 11264, 6920, 17431, 15973, 6212, 7985, 19953, 20471, 9628, 17048, 12352, 9499, 17563, 6688, 15824, 18766, 8336, 20457, 6891, 8723, 11416, 9164, 21133, 17929, 15010, 8928, 5930, 9168, 10379, 18905, 21044, 6571, 9539, 18774, 18898, 14242]
		return recommendations

	def get_most_popular_recipes(self, all_user_recipe_rating, total_recommendations):
		data = self.spark.textFile("/Users/larissaleite/Documents/Demeter/app/ratings.csv") #use ratings after!
		ratings = data.map(lambda l: l.split(','))\
			.map(lambda l: Rating(int(l[0]), str(l[1]), float(l[2])))

		# From ratings with tuples of (UserID, RecipeID, Rating) create an RDD with tuples of the (RecipeID, iterable of Ratings for that RecipeID)
		recipeIDsWithRatingsRDD = (ratings
								  .map(lambda (userid, recipeid, rating): (recipeid, rating))#.groupByKey())
								  .combineByKey(lambda value: (value, 1),
								  lambda x, value: (x[0] + value, x[1] + 1),
								  lambda x, y: (x[0] + y[0], x[1] + y[1])))

		averageByKey = recipeIDsWithRatingsRDD.map(lambda (label, (value_sum, count)): (label, value_sum / count))
		print sorted(averageByKey.collect(), key=lambda x: x[1], reverse=True)[:10]
