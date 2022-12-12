from pyspark import SparkConf, SQLContext, SparkContext
from pyspark.sql import SparkSession
from config.config import M_HOST, M_PORT, M_USER, M_PASSWORD
import jieba


spark = SparkSession \
    .builder \
    .appName("TitleWordsAnalysis") \
    .master("spark://master:7077") \
    .config("spark.mongodb.read.connection.uri", f"mongodb://{M_USER}:{M_PASSWORD}@{M_HOST}:{M_PORT}/bigdata.bilibili?authSource=admin&authMechanism=SCRAM-SHA-1") \
    .config("spark.mongodb.write.connection.uri", f"mongodb://{M_USER}:{M_PASSWORD}@{M_HOST}:{M_PORT}/bigdata.result?authSource=admin&authMechanism=SCRAM-SHA-1") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector:10.0.5") \
    .config("spark.rpc.message.maxSize", 1024) \
    .getOrCreate()

def process_string(string):
    return string.replace(" ", "").replace("\n", "").replace("\t", "")

def get_stop_words(filepath):
    stopwords = spark.textFile(filepath).collect()
    stopwords = [x.strip() for x in stopwords]
    return stopwords

print("正在加载数据库...")
df = spark.read.format("mongodb").load()
# df = spark.createDataFrame(df)
print("数据库加载成功！\n正在执行Title数据预处理和分词...")
string = df.select("title").rdd.map(lambda x: x[0]).reduce(lambda x, y : x + y)
string = process_string(string)
words_list = jieba.lcut(string)

print("正在进行MapReduce统计结果...")
wordsRdd = spark.sparkContext.parallelize(words_list)
stop_words = get_stop_words("/project/stop_words.txt")
resRdd = wordsRdd.filter(lambda word: word not in stop_words) \
                    .filter(lambda word: len(word) > 1) \
                    .map(lambda word: (word, 1)) \
                    .reduceByKey(lambda a, b: a + b) \
                    .sortBy(ascending=False, numPartitions=None, keyfunc=lambda x: x[1])
resDF = resRdd.toDF()
print("MapReduce结束！\n正在保存结果...")
resDF.write.format("mongodb").mode("append").save()
print("结果保存成功")