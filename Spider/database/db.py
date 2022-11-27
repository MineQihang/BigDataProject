from config.config import *
import pymongo
from tqdm import tqdm
import numpy as np


client = pymongo.MongoClient(host=M_HOST, port=M_PORT, username=M_USER, password=M_PASSWORD)
mydb = client["bigdata"]

def insert_many_data(col_name, data):
    '''
    向数据库中插入列表数据(多条)
    :param col_name Collection名称 
    :param data list数据
    '''
    col = mydb[col_name]
    col.insert_many(data)


def insert_one_data(col_name, data):
    '''
    向数据库中插入数据
    :param col_name Collection名称 
    :param data 数据(一般是dict)
    '''
    col = mydb[col_name]
    col.insert_one(data)

def update_data():
    '''
    计算各种比率并更新到数据库中
    '''
    col = mydb["bilibili"]
    cursor = col.find({}).limit(2000000)
    col.bulk_write([pymongo.UpdateOne({"_id": item["_id"]}, {"$set": {
            "coin_rate": item["coin"] / (item["view"] + 1),
            "favorite_rate": item["favorite"] / (item["view"] + 1),
            "like_rate": item["like"] / (item["view"] + 1),
            "danmaku_rate": item["danmaku"] / (item["view"] + 1),
            "reply_rate": item["reply"] / (item["view"] + 1),
            "share_rate": item["share"] / (item["view"] + 1),
            "interact_rate": (item["reply"] + item["danmaku"]) / np.log(item["view"] + 2),
            }})for item in tqdm(cursor)])
        