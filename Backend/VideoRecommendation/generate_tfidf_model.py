import pymongo
from tqdm import tqdm
from jieba import lcut
from gensim.similarities import SparseMatrixSimilarity
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim import corpora
import numpy as np
from config.config import *

client = pymongo.MongoClient(host=M_HOST, port=M_PORT, username=M_USER, password=M_PASSWORD)
mydb = client["bigdata"]
mycol = mydb["bilibili"]
cursor = mycol.find({}, {"title": 1, "aid": 1, "desc": 1}).limit(1500000)
data = [(x["aid"], lcut(x["title"])) for x in tqdm(cursor)]

aids = [x[0] for x in data]
texts = [x[1] for x in data]

# 基于文本集建立词典，并获得词典特征数
dictionary = Dictionary(texts)
num_features = len(dictionary.token2id)
# 基于词典，将分词列表集转换成稀疏向量集，称作语料库
corpus = [dictionary.doc2bow(text) for text in texts]
# 创建TF-IDF模型，传入语料库来训练
tfidf = TfidfModel(corpus)
# 此处将语料库用作被检索文本
tf_texts = tfidf[corpus] 
# 相似度计算
sparse_matrix = SparseMatrixSimilarity(tf_texts, num_features)

# 保存模型
tfidf.save("VideoTitle-TFIDF.model")
# 保存字典
dictionary.save("VideoTitle-Dic.dic")
# 保存语料库
corpora.MmCorpus.serialize("./VideoTitle-Corpus.corpus", corpus)
# 保存aid
with open("VideoTitle-Aid.txt", "w") as fin:
    fin.writelines([str(aid)+"\n" for aid in aids])
