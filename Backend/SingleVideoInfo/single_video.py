from fastapi import APIRouter, Form
from basic import *
from functions.single_video_info import get_video_info_by_id
from functions.sentiment_analysis import mul_sentiment_analysis
from functions.word_segment import WordSegmenter

from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizer
from transformers import AutoTokenizer, AutoModelForTokenClassification

import re
import torch

sentiment_tokenizer=BertTokenizer.from_pretrained('IDEA-CCNL/Erlangshen-MegatronBert-1.3B-Sentiment')
sentiment_model=AutoModelForSequenceClassification.from_pretrained('IDEA-CCNL/Erlangshen-MegatronBert-1.3B-Sentiment')

ws_tokenizer = AutoTokenizer.from_pretrained("ckiplab/albert-base-chinese-ws")
ws_model = AutoModelForTokenClassification.from_pretrained("ckiplab/albert-base-chinese-ws")

print("load bert model success!")

router = APIRouter(
    prefix="/single-video",
    tags=["single-video"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post('/basic-info')
async def basic_info(video_id: str = Form("")):
    '''
    通过视频aid或bid,获取视频基本信息
    :params aid: str av号
    :params aid: str bv号
    :return list
    '''
    data = {}

    if video_id == "":
        return failResponse(detail="视频aid或bid未输入")

    info_data = get_video_info_by_id(bid = video_id) if video_id.startswith("BV") else get_video_info_by_id(aid = video_id)

    data['bvid'] = info_data['bvid']
    data['aid'] = info_data['aid']
    data['pic'] = info_data['pic']
    data['title'] = info_data['title']
    data['desc'] = info_data['desc']
    # url
    if video_id.startswith("BV") or video_id.startswith("av"):
        url = f"https://www.bilibili.com/video/{video_id}"
    else:
        url = f"https://www.bilibili.com/video/av{video_id}"
    data['url'] = url

    # owner
    data['owner'] = info_data['owner']

    # data
    data['stat'] = info_data['stat']
    data['stat']['like_rate'] = info_data['stat']['like']/info_data['stat']['view']
    data['stat']['coin_rate'] = info_data['stat']['coin']/info_data['stat']['view']
    data['stat']['favorite_rate'] = info_data['stat']['favorite']/info_data['stat']['view']

    # TODO: rate所占百分比, spark调数据库

    # honor
    if 'honor' in info_data['honor_reply'].keys():
        data['honor'] = info_data['honor_reply']['honor']

    return successResponse(detail="视频基本信息返回成功", data = data) if data != None else failResponse(detail="视频基本信息返回失败")

@router.post('/replies-word-data')
async def replies_word_data(video_id: str = Form("")):
    '''
    通过视频aid或bid,获取视频评论,并进行词频统计
    :params aid: str av号
    :params aid: str bv号
    :return list
    '''

    data = {}

    info_data = get_video_info_by_id(bid = video_id) if video_id.startswith("BV") else get_video_info_by_id(aid = video_id)
    
    # load stop word
    stop_word_path = "./functions/stop_words.txt"
    stop_word_list = []
    with open(stop_word_path, encoding='utf-8') as f:
        stop_word = f.read()
    stop_word_list = stop_word.split('\n')

    ws = WordSegmenter(model = ws_model,tokenizer = ws_tokenizer,device = torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    words = ' '.join(info_data['replies']).lower()

    words = ws.segment([words])

    word_data = {}

    for word in words[0]:
        if word not in stop_word_list and len(word) > 1: # 非停用词并且非单字
            tmp_word = re.findall(r'[\u4e00-\u9fa5]+',word)
            if len(tmp_word)== 1:
                if tmp_word[0] not in word_data.keys():
                    word_data[tmp_word[0]] = 0
                word_data[tmp_word[0]] += 1

    # data['words'] = words

    # 排序
    word_data = sorted(word_data.items(), key=lambda x: x[1], reverse = True)

    data['word_data'] = word_data

    return successResponse(detail="视频评论词频统计返回成功", data = data) if data != None else failResponse(detail="视频评论词频统计返回失败")

@router.post('/replies-sentiment')
async def replies_sentiment(video_id: str = Form("")):
    '''
    通过视频aid或bid,获取视频评论,并进行情感分析
    :params aid: str av号
    :params aid: str bv号
    :return list
    '''
    data = {}

    if video_id == "":
        return failResponse(detail="视频aid或bid未输入")

    info_data = get_video_info_by_id(bid = video_id) if video_id.startswith("BV") else get_video_info_by_id(aid = video_id)
    
    sentiment = mul_sentiment_analysis(info_data['replies'], sentiment_tokenizer, sentiment_model)

    data["sentiment"] = sentiment

    data["pos_num"] = sentiment.count("positive")
    data["neg_num"] = sentiment.count("negative")

    data["pos_rate"] = data["pos_num"]/len(data["sentiment"])
    data["neg_rate"] = data["neg_num"]/len(data["sentiment"])

    return successResponse(detail="视频评论情感分析返回成功", data = data) if data != None else failResponse(detail="视频评论情感分析返回失败")
