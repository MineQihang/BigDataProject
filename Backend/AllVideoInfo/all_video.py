from fastapi import APIRouter, Form
from basic import *
from database.db import query_overall_situation, query_words_count, query_tags_count_by_word, query_tag_count_change, query_tags_count_in_month, query_tags_relation

router = APIRouter(
    prefix="/all-video",
    tags=["all-video"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post('/all-video-info')
async def all_video_info(num:int = Form(20)):
    '''
    查看总体情况,标题词频
    :params num: int 标题词频个数
    :return list
    '''
    data = {}
    # 播放量
    data['play_data'] = query_overall_situation()
    data['words_count'] = query_words_count(num) # 词云使用
    # 饼状图占比
    rate_data = {}
    for x in data['play_data']:
        if x['fq']+'-'+x['cate'] not in rate_data.keys():
            rate_data[x['fq']+'-'+x['cate']] = 0
        rate_data[x['fq']+'-'+x['cate']] += x['num']
    # 折线图data,每个月份各个分区视频发布量
    line_data = {}
    for x in data['play_data']:
        if x['month'] not in line_data.keys():
            line_data[x['month']] = {}
        line_data[x['month']][x['fq']+'-'+x['cate']] = x['num']

    data['rate_data'] = rate_data
    data['line_data'] = line_data

    return successResponse(detail="视频基本信息返回成功", data = data) if data != None else failResponse(detail="视频基本信息返回失败")

@router.post('/tags-count-by-word')
async def tags_count_by_word(word:str=Form(""), num:int = Form(20)):
    '''
    用词语检索出相关的num个词tags
    :param word 一个词 **传入word=""即可实现查询所有tag中前num个**
    :return tag列表 如["1", "2"] 
    '''
    data = {}
    data['tags_count_by_word'] = query_tags_count_by_word(word, num)
    return successResponse(detail="视频基本信息返回成功", data = data) if data != None else failResponse(detail="视频基本信息返回失败")

@router.post('/tags-count-change')
async def tags_count_change(tag:str=Form("")):
    '''
    一个tag每个月份的变化
    :param tag
    :return [(month, count), ...]
    '''
    data = {}
    data['tags_count_change'] = query_tag_count_change(tag)

    return successResponse(detail="视频基本信息返回成功", data = data) if data != None else failResponse(detail="视频基本信息返回失败")

@router.post('/tags-count-in-month')
async def tags_count_in_month(month:int=Form(None), num=Form(10)):
    '''
    :param month 不指定就是返回所有月份的数据, 指定了就是那个月的排名前num的tag
    :param num 要看前多少个
    :return {1: [(tag, count), ...], 2:[], ...}
    '''
    data = {}
    data['tags_count_in_month'] = query_tags_count_in_month(month, num)

    return successResponse(detail="视频基本信息返回成功", data = data) if data != None else failResponse(detail="视频基本信息返回失败")

@router.post('/tags-relation')
async def tags_relation(tags:str = Form()):
    '''
    根据tags返回关联度关系
    :param tags list 比如 知识分享官,打卡挑战,学习
    :return 三元组 [(index_1, index_2, relation_rate), ...]
    '''
    data = {}
    tags = tags.split(",")
    # print(tags)
    data['tags_relation'] = query_tags_relation(tags)

    return successResponse(detail="视频基本信息返回成功", data = data) if data != None else failResponse(detail="视频基本信息返回失败")



