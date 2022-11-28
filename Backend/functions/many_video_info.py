import requests
import json
import aiohttp
import asyncio
import nest_asyncio
nest_asyncio.apply()



done = []

async def aiohttpget(vid):
    async with aiohttp.ClientSession(headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52"
        }) as session:
        async with session.get(
            url="http://api.bilibili.com/x/web-interface/view",
            params=({ "bvid": vid } if type(vid) == str and vid[0]=='B' else {"aid": vid})
        ) as resp:
            return await resp.text()

async def main_gather(ids):
    task_gets = [asyncio.create_task(
        aiohttpget(vid)) for vid in ids]  # 向上取整
    global done
    done = await asyncio.gather(*task_gets)


def get_videos_info_by_ids(ids):
    '''
    通过av号列表给出一系列视频信息
    :param aids av号列表
    :return 视频信息
    '''
    global done
    done = []
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_gather(ids))
    return [json.loads(x)["data"] for x in done]


if __name__ == "__main__":
    lst = [
        "636883435",
        "893767032",
        "BV1GK411o7CD"
    ]
    print(get_videos_info_by_ids(lst))