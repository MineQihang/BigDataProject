from jieba import lcut
from gensim.similarities import SparseMatrixSimilarity
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.corpora import MmCorpus
import numpy as np

from fastapi import APIRouter, Form
from functions.many_video_info import get_videos_info_by_aid

router = APIRouter(
    prefix="/video-recommend",
    tags=["video-recommend"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)



# 加载模型
print("正在加载模型...")
model = TfidfModel.load("./data/VideoTitle-TFIDF.model")
# 加载aid
print("正在加载Aid...")
aids  = [aid.strip() for aid in open("./data/VideoTitle-Aid.txt", "r").readlines()]
# 加载字典
print("正在加载字典...")
dictionary = Dictionary.load("./data/VideoTitle-Dic.dic")
# 加载语料库
print("正在加载语料库...")
corpus = MmCorpus("./data/VideoTitle-Corpus.corpus")
# 获取稀疏矩阵
print("正在计算稀疏矩阵...")
num_features = len(dictionary.token2id)
texts = model[corpus] 
sparse_matrix = SparseMatrixSimilarity(texts, num_features)


@router.post('/recommend-video')
async def recommend_video_by_text(text: str = Form("")):
    '''
    通过文本匹配视频标题获得数据
    :param text 文本
    '''
    # 用词典把搜索词也转换为稀疏向量
    vector = dictionary.doc2bow(lcut(text))
    # 计算TFIDF
    tf = model[vector]
    # 计算相似度
    similarities = sparse_matrix.get_similarities(tf)
    return get_videos_info_by_aid([aids[x] for x in np.argsort(similarities)[-20:]])


if __name__ == "__main__":
    text = "我想吃点好的"
    res = recommend_video_by_text(text)
    for i in range(res):
        print(res[i])