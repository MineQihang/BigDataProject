from fastapi import APIRouter, Form
from basic import *
from functions.single_video_info import get_video_info_by_id

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

