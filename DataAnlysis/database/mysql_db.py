import json
import pymysql
from config.config import HOST, USER, PASSWORD, DATABASE, PORT
from pymysql.constants import CLIENT
from datetime import datetime
import time
import sys



def query_by_sql(sql: str, args=None):
    '''
    通过sql进行查询数据
    @params: sql: str 要执行查询的sql语句, args: 需要传入的查询参数
    @return: list 返回查询到的数据
    '''
    db = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE, client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    data = None
    try:
        cursor.execute(sql, args)
        data = cursor.fetchall()
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        cursor.close()
        db.close()
        return data

def do_by_sql(sql: str, args=None):
    '''
    使用sql进行数据插入或删除或修改
    @params: sql: str 要执行操作的sql语句, args: 需要传入的查询参数
    @return: bool 是否成功执行
    '''
    db = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE, client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    flag = False
    try:
        if type(args) == list and len(args) > 0 and type(args[0]) == list:
            cursor.executemany(sql, args)
        else:
            cursor.execute(sql, args)
        db.commit()
        flag = True
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        cursor.close()
        db.close()
        return flag
    