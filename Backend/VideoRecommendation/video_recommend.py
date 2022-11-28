from jieba import lcut
from gensim.similarities import SparseMatrixSimilarity
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.corpora import MmCorpus
import numpy as np

from fastapi import APIRouter, Form
from functions.many_video_info import get_videos_info_by_ids
from basic import *

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


@router.post('/recommend-video-by-text')
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
    res = get_videos_info_by_ids([aids[x] for x in np.argsort(similarities)[-20:]])
    views = [x["stat"]["view"] for x in res]
    temp = np.argsort(views)
    index = np.argsort([0.99 * t + 0.01 * temp[t] for t in range(len(temp))])
    return successResponse(detail="返回成功", data=[res[i] for i in reversed(index)])

@router.post('/recommend-video-by-videos')
async def recommend_video_by_text(videos: str = Form("")):
    '''
    通过视频匹配视频标题获得数据
    :param videos 视频编号字符串以","为分隔符
    '''
    videos_list = videos.split(",")
    res = get_videos_info_by_ids(videos_list)
    text = [x['title'] for x in res]
    text = ' '.join(text)
    # 用词典把搜索词也转换为稀疏向量
    vector = dictionary.doc2bow(lcut(text))
    # 计算TFIDF
    tf = model[vector]
    # 计算相似度
    similarities = sparse_matrix.get_similarities(tf)
    res = get_videos_info_by_ids([aids[x] for x in np.argsort(similarities)[-20:]])
    views = [x["stat"]["view"] for x in res]
    temp = np.argsort(views)
    index = np.argsort([0.99 * t + 0.01 * temp[t] for t in range(len(temp))])
    return successResponse(detail="返回成功", data=[res[i] for i in reversed(index)])



if __name__ == "__main__":
    lst = [
        "636883435",
        "893767032",
        "BV1GK411o7CD"
    ]
    videos  = ','.join(lst)
    video_list = videos.split(",")
    res = get_videos_info_by_ids(video_list)
    text = [x['title'] for x in res]
    print(text)