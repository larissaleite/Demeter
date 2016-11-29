from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating

class Recommender:

    def __init__(self, dao, spark):
        self.dao = dao
        self.spark = spark

    def check_spark(self):
        print "------LOADING FILE"
        raw_text = self.spark.textFile('/Users/larissaleite/Documents/Demeter/app/pg100.txt', 4)

        print "------PRINTING FILE"
        print "---------"+str(raw_text.count())
        # check whether the data was loaded properly:
        print u'first line of raw_text:\t "{}"'.format(raw_text.first())
        print u'total number of lines:\t {}'.format(raw_text.count())

    def get_recommended_recipes(self):
        # Load and parse the data
        data = self.spark.textFile("/Users/larissaleite/Documents/Demeter/app/ratings.csv")
        ratings = data.map(lambda l: l.split(','))\
            .map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2])))

        # Build the recommendation model using Alternating Least Squares
        rank = 10
        numIterations = 10
        model = ALS.train(ratings, rank, numIterations)

        # Evaluate the model on training data
        testdata = ratings.map(lambda p: (p[0], p[1]))
        predictions = model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2]))
        ratesAndPreds = ratings.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
        MSE = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
        print("Mean Squared Error = " + str(MSE))

        print str(predictions.take(10))

        # Save and load model
        #model.save(sc, "target/tmp/myCollaborativeFilter")
        #sameModel = MatrixFactorizationModel.load(sc, "target/tmp/myCollaborativeFilter")

        print "RECOMMENDATIONS\n"
        print str(model.recommendProducts(50,10))

    def get_similar_recipes(self, recipe):
        return self.dao.get_most_popular_recipes()
