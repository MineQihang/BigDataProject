from config.config import *
import pymongo


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

def query_overall_situation():
    '''
    查看总体情况
    返回结果示例:
    [{'_id': ObjectId('63831bff7a14a2170e89853c'), 'cate_id': 201, 'fq_id': 0, 'cate': '科学科普', 'fq': '知识区', 'month': 1, 'num': 79711} ...]
    一个元素的重要组成结构为(cate: 小分区名, fq: 大分区名, month: 月份, num: 这个月视频的数量)
    '''
    col = mydb["overall"]
    return list(col.find({}))