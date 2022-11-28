import json
import aiohttp
import asyncio
import nest_asyncio
nest_asyncio.apply()


done = []

async def aiohttpget(url, params):
    '''
    发起异步请求并返回数据文本
    :param url 
    :param params 请求参数
    '''
    async with aiohttp.ClientSession(headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52"
        }) as session:
        async with session.get(
            url=url,
            params=params
        ) as resp:
            return await resp.text()

async def main_gather(configs):
    '''
    根据(url, params)同步发出请求
    :param configs [(url, params)]
    '''
    task_gets = [asyncio.create_task(aiohttpget(url, params)) for (url, params) in configs]  # 向上取整
    global done
    done = await asyncio.gather(*task_gets)


def send_get_requests(configs):
    '''
    通过av号列表给出一系列视频信息
    :param aids av号列表
    :return 视频信息
    '''
    global done
    done = []
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_gather(configs))
    return [json.loads(x) for x in done]
