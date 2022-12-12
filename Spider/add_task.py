import requests
import json
from database.mysql_db import do_by_sql
import datetime


params = {
    # "main_ver": "v3",
    "search_type": "video",
    "view_type": "hot_rank",
    "order": "click",
    "copy_right": -1,
    "cate_id": "201",
    "page": 2,
    "pagesize": 100,
    "jsonp": "jsonp",
    "time_from": "20220101",
    "time_to": "20220131",
    # "callback": ""
}


cates = [
    201, # 科学科普
    124, # 社科 法律 心理
    228, # 人文历史
    207, # 财经商业
    208, # 校园学习
    209, # 职业职场
    229, # 设计·创意
    122, # 野生技能协会
    95, # 数码
    230, # 软件应用
    231, # 计算机技术
    232, # 科工机械
    233 # 极客DIY
]

page_size = 100

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

data = [[i, cate, time_from, time_to] for time_from, time_to in tm for cate in cates for i in range(1, page_size+1)]
sql = """INSERT INTO `task` (`page`, `cate_id`, `time_from`, `time_to`) VALUES (%s, %s, %s, %s)"""
do_by_sql(sql, data[4:])
# print(data[2:4])