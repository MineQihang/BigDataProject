from database.db import insert_many_data
from request.request import send_get_requests
from time import sleep

cates = [
    (201, 0, "科学科普", "知识区"), # 科学科普
    (124, 0, "社科 法律 心理", "知识区"), # 社科 法律 心理
    (228, 0, "人文历史", "知识区"), # 人文历史
    (207, 0, "财经商业", "知识区"), # 财经商业
    (208, 0, "校园学习", "知识区"), # 校园学习
    (209, 0, "职业职场", "知识区"), # 职业职场
    (229, 0, "设计·创意", "知识区"), # 设计·创意
    (122, 0, "野生技能协会", "知识区"), # 野生技能协会
    (95, 1, "数码", "科技区"),  # 数码
    (230, 1, "软件应用", "科技区"), # 软件应用
    (231, 1, "计算机技术", "科技区"), # 计算机技术
    (232, 1, "科工机械", "科技区"), # 科工机械
    (233, 1, "极客DIY", "科技区")  # 极客DIY
]

tm = [
    ("20220101", "20220131"),
    ("20220201", "20220228"),
    ("20220301", "20220331"),
    ("20220401", "20220430"),
    ("20220501", "20220531"),
    ("20220601", "20220630"),
    ("20220701", "20220731"),
    ("20220801", "20220831"),
    ("20220901", "20220930"),
    ("20221001", "20221031"),
    ("20221101", "20221120")
]

url = "https://s.search.bilibili.com/cate/search"


def get_data():
    '''
    爬取每个分区2022年的所有视频数
    '''
    res = []
    for (cate_id, fq_id, cate, fq) in cates:
        print(f"正在爬取[{fq} - {cate}]数据...")
        params = []
        for (time_from, time_to) in tm:
            params.append({
                "main_ver": "v3",
                "search_type": "video",
                "view_type": "hot_rank",
                "order": "click",
                "copy_right": -1,
                "cate_id": cate_id,
                "page": 1,
                "pagesize": 10,
                "jsonp": "jsonp",
                "time_from": time_from,
                "time_to": time_to,
            })
        data = send_get_requests([(url, param) for param in params])
        for i in range(len(data)):
            res.append({
                "cate_id": cate_id,
                "fq_id": fq_id,
                "cate": cate,
                "fq": fq,
                "month": int(tm[i][0][4:6]),
                "num": data[i]["numResults"],
            })
        sleep(5)
    return res


if __name__ == "__main__":
    res = get_data()
    print(res)
    insert_many_data("overall", res)