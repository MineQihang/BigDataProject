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

