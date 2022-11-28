from fastapi import APIRouter, Form
from basic import *
from database.db import query_overall_situation, query_words_count

router = APIRouter(
    prefix="/all-video",
    tags=["all-video"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post('/all-video-info')
async def all_video_info(num:int = Form(20)):
    '''
    通过视频aid或bid,获取视频基本信息
    :params aid: str av号
    :params aid: str bv号
    :return list
    '''
    data = {}

    # 播放量
    data['paly_data'] = query_overall_situation()
    data['words_count'] = query_words_count(num)


    return successResponse(detail="视频基本信息返回成功", data = data) if data != None else failResponse(detail="视频基本信息返回失败")