from config.config import M_USER, M_PASSWORD, M_HOST, M_PORT
from database.mysql_db import query_by_sql, do_by_sql
import pymongo

def get_mysql_data():
    sql = """SELECT * FROM `bilibili` WHERE `view` is not NULL"""
    return query_by_sql(sql)


def insert_data_into_mongo(client, data):
    db = client.admin
    db.authenticate(M_USER, M_PASSWORD, mechanism='SCRAM-SHA-1')
    mydb = client["bigdata"]
    mycol = mydb["bilibili"]
    for i in range(len(data)):
        data[i]["_id"] = data[i]["aid"]
    x = mycol.insert_many(data)
    # print(x.inserted_ids)


if __name__ == "__main__":
    myclient = pymongo.MongoClient(M_HOST, M_PORT)
    data = get_mysql_data()
    insert_data_into_mongo(myclient, data)
