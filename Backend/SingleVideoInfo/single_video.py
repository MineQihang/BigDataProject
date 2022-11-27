from fastapi import APIRouter, Form
from basic import *
from functions.single_video_info import get_video_info_by_id
from functions.sentiment_analysis import mul_sentiment_analysis

from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizer

tokenizer=BertTokenizer.from_pretrained('IDEA-CCNL/Erlangshen-MegatronBert-1.3B-Sentiment')
model=AutoModelForSequenceClassification.from_pretrained('IDEA-CCNL/Erlangshen-MegatronBert-1.3B-Sentiment')
print("load success!!!")

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
    ...

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
    
    sentiment = mul_sentiment_analysis(info_data['replies'], tokenizer, model)

    print(sentiment)

    data["sentiment"] = sentiment

    data["pos_num"] = sentiment.count("positive")
    data["neg_num"] = sentiment.count("negative")

    data["pos_rate"] = data["pos_num"]/len(data["sentiment"])
    data["neg_rate"] = data["neg_num"]/len(data["sentiment"])

    return successResponse(detail="视频基本信息返回成功", data = data) if data != None else failResponse(detail="视频基本信息返回失败")
