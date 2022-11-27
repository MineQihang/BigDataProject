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


def query_exceed_rate(indexes):
    '''
    计算超过数据库中多少视频
    :param indexes 需要从哪些方面和对应的值，例如{"view": 120}
    :return dict 结果{col: data}，例如{'view': 0.91}
    '''
    col = mydb["bilibili"]
    sum_num = col.count_documents({})
    return dict((index, 1 - col.count_documents({index: {"$gt": value}}) / sum_num) for (index, value) in indexes.items())

def query_words_count(num):
    '''
    查询数据库标题词频
    :param num 需要多少
    :return {词: 词频, ...}
    '''
    col = mydb["result"]
    return dict((x["_1"], x["_2"]) for x in col.find({}).limit(num).sort("_2", -1))