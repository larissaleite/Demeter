from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName('demeter').setMaster("spark://Larissas-MacBook-Pro.local:7077")
sc = SparkContext(conf=conf)

'''raw_text = sc.textFile('/Users/larissaleite/Documents/Demeter/app/pg100.txt', 4)

print "------PRINTING FILE"
print "---------"+str(raw_text.count())
# check whether the data was loaded properly:
print u'first line of raw_text:\t "{}"'.format(raw_text.first())
print u'total number of lines:\t {}'.format(raw_text.count())
'''

import pymongo_spark
pymongo_spark.activate()

mongo_rdd = sc.mongoRDD('mongodb://localhost:27017/demeter.recipe')
print(mongo_rdd.first())
