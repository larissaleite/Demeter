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
            data = self.spark.textFile("/Users/larissaleite/Documents/Demeter/app/ratings_test.csv") #use ratings after!
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
        model = self.build_model(all_user_recipe_rating)

        data = self.spark.textFile("/Users/larissaleite/Documents/Demeter/app/ratings_test.csv") #use ratings after!
        ratings = data.map(lambda l: l.split(','))\
            .map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2])))

        all_recipes_ids = []

        #TODO: get from the database
        for x in range(1,51):
            all_recipes_ids.append(x)

        all_recipes_ids = self.spark.parallelize(all_recipes_ids)

        rated_recipes_ids = ratings.filter(lambda rating: rating[0]==user_id).map(lambda x: int(x[1])).distinct().collect()

        all_recipes_ids = data.map(lambda l: l.split(',')).map(lambda y: int(y[1])).distinct().collect()
        candidates = self.spark.parallelize([r for r in all_recipes_ids if r not in rated_recipes_ids])
        #to transform in an array and print, just put .collect() after

        predictions = model.predictAll(candidates.map(lambda x: (user_id, x))).collect()
        recommendations = sorted(predictions, key=lambda x: x[2], reverse=True)[:10]

        print "\nRECOMMENDATIONS\n"

        print str(recommendations)+"\n"
        return recommendations
