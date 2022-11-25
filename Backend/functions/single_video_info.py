import requests
import json
import aiohttp
import asyncio
import nest_asyncio
nest_asyncio.apply()


PAGE_SIZE = 20  # 一次获取多少评论

done = []

async def aiohttpget(aid, page):
    async with aiohttp.ClientSession(headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52"
        }) as session:
        async with session.get(
            url="https://api.bilibili.com/x/v2/reply/main",
            params={
                "mode": 3,  # 热度排序
                "oid": aid,  # av号
                "next": page,  # 第几页 每次20条
                "type": 1   # 默认
            }
        ) as resp:
            return await resp.text()

async def main_gather(data_size, aid):
    task_gets = [asyncio.create_task(
        aiohttpget(aid, page)) for page in range(1, 1+(data_size + PAGE_SIZE - 1)//PAGE_SIZE)]  # 向上取整
    global done
    done = await asyncio.gather(*task_gets)


def get_basic_info_by_id(aid=None, bid=None, full=True):
    resp = requests.get(
        url="http://api.bilibili.com/x/web-interface/view",
        params={
            "aid": aid,
            "bvid": bid
        })
    try:
        data = json.loads(resp.text)["data"]
        needed_data = ["aid", "title", "desc", "stat"]
        return dict((x, data[x]) for x in needed_data) if not full else data
    except:
        raise Exception("获取视频基本信息错误")

def get_replies_info_by_aid(aid, data_size=100):
    '''
    :param aid av号
    :param data_size 获取多少条评论
    '''
    global done
    done = []
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_gather(data_size, aid))
    ans = []
    for data in done:
        replies = json.loads(data)["data"]["replies"]
        ans.extend([reply["content"]["message"] for reply in replies])
    return ans


def get_video_info_by_id(aid=None, bid=None):
    '''
    通过av号或者bv号给出视频信息
    :param aid av号 如12345或者av12345
    :param bid bv号 如1rK411d7qG或者BV1rK411d7qG, 注意区分大小写
    :return 视频信息
    '''
    if aid == None and bid == None:
        raise Exception("请给出aid或者bid的其中一种")
    aid = aid.lower().strip("av") if type(aid) == str else aid
    info = get_basic_info_by_id(aid, bid)
    try:
        aid = info["aid"]
        info["replies"] = get_replies_info_by_aid(aid=aid)
        return info
    except:
        raise("获取评论错误")
