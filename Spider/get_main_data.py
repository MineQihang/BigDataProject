import requests
import json
from database.mysql_db import do_by_sql, query_by_sql
import datetime
from time import sleep
import asyncio
import aiohttp


keys = ["tag", "id", "pubdate", "mid", "description", "title"]

done = []
PAGE_SIZE = 100
UPDATE_SIZE = 10

def get_video_list(task):
    resp = requests.get(
        url="https://s.search.bilibili.com/cate/search",
        params={
            "main_ver": "v3",
            "search_type": "video",
            "view_type": "hot_rank",
            "order": "click",
            "copy_right": -1,
            "cate_id": str(task["cate_id"]),
            "page": task["page"],
            "pagesize": PAGE_SIZE,
            "jsonp": "jsonp",
            "time_from": task["time_from"],
            "time_to": task["time_to"],
            # "callback": ""
        },
        headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52"
        }
    )
    data = json.loads(resp.text)
    result = data["result"]
    ans = [dict((k, res[k]) for k in keys) for res in result]
    for i in range(len(ans)):
        ans[i]["pubdate"] = datetime.datetime.strptime(ans[i]["pubdate"],'%Y-%m-%d %H:%M:%S')
    return ans


async def aiohttpget(x):
    aid = x["id"]
    async with aiohttp.ClientSession(headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52"
        }) as session:
        async with session.get(
            url="http://api.bilibili.com/x/web-interface/view",
            params={
                "aid": aid
            }
        ) as resp:
            return await resp.text()

async def main_gather(lst):
    task_gets = [asyncio.create_task(
        aiohttpget(x)) for x in lst]
    global done
    done = await asyncio.gather(*task_gets)


def collect_data(task):
    print("正在获取视频数据......")
    lst = get_video_list(task)
    try:
        # print(lst)
        print(f"已获取{len(lst)}条数据")
    except:
        print("网络出现了一定的问题!")
        return None
    sql = """INSERT INTO `bilibili` (`tag`, `aid`, `pubdate`, `mid`, `desc`, `title`) VALUES (%s, %s, %s, %s, %s, %s)"""
    data = [[x[y] for y in keys] for x in lst]
    flag = do_by_sql(sql, data)
    if not flag:
        print("此条数据无需更新")
        return 0
    print(f"已插入{len(lst)}条数据")
    print("正在更新视频数据......")
    gcnt = 0
    for i in range(PAGE_SIZE//UPDATE_SIZE):
        global done
        done = []
        # print([x["id"] for x in lst[i*UPDATE_SIZE:i*UPDATE_SIZE+UPDATE_SIZE]])
        asyncio.run(main_gather(lst[i*UPDATE_SIZE:i*UPDATE_SIZE+UPDATE_SIZE]))
        temp = ["duration", "view", "danmaku", "reply", "favorite", "coin", "share", "his_rank", "like"]
        res = []
        cnt = 0
        aids = []
        # print(done)
        for dt in done:
            try:
                result = json.loads(dt)["data"]
                res.append([
                    result["duration"],
                    result["stat"]["view"],
                    result["stat"]["danmaku"],
                    result["stat"]["reply"],
                    result["stat"]["favorite"],
                    result["stat"]["coin"],
                    result["stat"]["share"],
                    result["stat"]["his_rank"],
                    result["stat"]["like"],
                    result["aid"]
                ])
                aids.append(result["aid"])
            except:
                cnt += 1
        print(f"有{cnt}条数据已被拦截")
        gcnt += cnt
        if len(aids) != 0:
            sql2 = f"""UPDATE `bilibili` SET {', '.join([f'`{x}`=%s' for x in temp])} WHERE `aid`=%s;;"""
            do_by_sql(sql2, res)
            print(f"已更新{len(res)}条数据")
        print(f"[{i+1}/{PAGE_SIZE//UPDATE_SIZE}]正在进行下一次更新, 请等待...")
        sleep(2)
    return gcnt

def query_task():
    ans = query_by_sql("SELECT * FROM `task` WHERE finish=-1 limit 1")
    if len(ans) >= 1:
        return ans[0]
    else:
        return None

def flag_task(tid):
    sql = """UPDATE `task` SET `finish`=-1 WHERE id=%s"""
    do_by_sql(sql, tid)


def finish_task(tid):
    sql = """UPDATE `task` SET `finish`=-2 WHERE id=%s"""
    do_by_sql(sql, tid)

def rev_task(cnt, tid):
    sql = """UPDATE `task` SET `finish`=%s WHERE id=%s"""
    do_by_sql(sql, [cnt, tid])

def find_invalid_data():
    sql = """SELECT `aid` FROM `bilibili` WHERE view is NULL"""
    return query_by_sql(sql)

def fix_data():
    data = find_invalid_data()
    data_size = len(data)
    print(f"有{data_size}条数据等待更新...")
    gcnt = 0
    for i in range(data_size//UPDATE_SIZE):
        global done
        done = []
        # print([x["id"] for x in lst[i*UPDATE_SIZE:i*UPDATE_SIZE+UPDATE_SIZE]])
        asyncio.run(main_gather([{"id": x["aid"]} for x in data[i*UPDATE_SIZE:i*UPDATE_SIZE+UPDATE_SIZE]]))
        temp = ["duration", "view", "danmaku", "reply", "favorite", "coin", "share", "his_rank", "like"]
        res = []
        cnt = 0
        aids = []
        # print(done)
        for dt in done:
            try:
                result = json.loads(dt)["data"]
                res.append([
                    result["duration"],
                    result["stat"]["view"],
                    result["stat"]["danmaku"],
                    result["stat"]["reply"],
                    result["stat"]["favorite"],
                    result["stat"]["coin"],
                    result["stat"]["share"],
                    result["stat"]["his_rank"],
                    result["stat"]["like"],
                    result["aid"]
                ])
                aids.append(result["aid"])
            except:
                cnt += 1
        print(f"有{cnt}条数据已被拦截")
        gcnt += cnt
        if len(aids) != 0:
            sql2 = f"""UPDATE `bilibili` SET {', '.join([f'`{x}`=%s' for x in temp])} WHERE `aid`=%s;;"""
            do_by_sql(sql2, res)
            print(f"已更新{len(res)}条数据")
        print(f"[{i+1}/{data_size//UPDATE_SIZE}]正在进行下一次更新, 请等待...")
        sleep(2)
    return gcnt


if __name__ == '__main__':
    prv = -1
    # 由于数据可能被拦截，当需要重新爬取时，可以将下面置为True
    is_fix = True
    while True:
        try:
            if is_fix:
                fix_data()  # 运行fix函数对`is_finish`>0的值进行fix
            else:
                task = query_task()  # 查询任务
                if task["id"] == prv:  # 如果和上次任务一样
                    rev_task(-404, task["id"])  # 说明`task`表可能已经执行完毕, 或者有其他一些问题出现, 因此用-404标记一下task
                    continue
                prv = task["id"]  # 记录本任务为下一任务的上一个任务
                print("正在处理任务: ", task)
                flag_task(task["id"])  # 标记task为正在处理
                cnt = collect_data(task)  # 根据task收集数据, 返回的cnt表示有多少是被拦截的
                if cnt == 0:
                    finish_task(task["id"])  # 如果没有被拦截的, 该任务标注为执行完成
                else:
                    rev_task(cnt, task["id"])  # 不然就将task的`is_finish`标记为被拦截的请求个数
            print("处理完成! 请等待5秒进入下一任务")
        except:
            print("遇到了一些问题! 请排查")
        sleep(5)  # 休眠5秒避免请求过多被封IP
