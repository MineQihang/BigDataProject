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
    data = []
    for x in col.find({}):
        del x['_id']
        data.append(x)
    return data


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


def query_tags_count_by_word(word:str="", num=10):
    '''
    用词语检索出相关的num个词tags
    :param word 一个词 **传入word=""即可实现查询所有tag中前num个**
    :return tag列表 如["1", "2"] 
    '''
    col = mydb["tags_count"]
    res = col.find({"tag": {"$regex": word}}).sort("count", -1).limit(num)
    return [(x["tag"], x["count"]) for x in res]


def query_tag_count_change(tag=""):
    '''
    一个tag每个月份的变化
    :param tag
    :return [(month, count), ...]
    '''
    col = mydb["month_tags"]
    res = col.find({"tag": tag}).sort("month")
    return [(x["month"], x["count"]) for x in res]


def query_tags_count_in_month(month=None, num=10):
    '''
    :param month 不指定就是返回所有月份的数据, 指定了就是那个月的排名前num的tag
    :param num 要看前多少个
    :return {1: [(tag, count), ...], 2:[], ...}
    '''
    col = mydb["month_tags"]
    if month != None:
        res = col.find({"month": month}).sort("count", -1).limit(num)
        return [(x["tag"], x["count"]) for x in res]
    else:
        res = col.aggregate([{
            "$facet": dict((str(month), [ { "$match": { "month":month } }, {"$sort" : {"count": -1}}, { "$limit": num } ]) for month in range(1, 12))
        }]) 
        return dict((int(month), [(x["tag"], x["count"]) for x in mp]) for temp in res for month, mp in temp.items())
        

def query_tags_relation(tags):
    '''
    根据tags返回关联度关系
    :param tags list 比如["知识分享官", "打卡挑战", "学习" ...]
    :return 三元组 [(index_1, index_2, relation_rate), ...]
    '''
    col = mydb["tags_relation"]
    col_tags = mydb["tags_count"]
    try:
        ans = []
        tags_count = [col_tags.find_one({"tag": tags[i]})["count"] for i in range(len(tags))]
        for i in range(len(tags)):
            temp = []
            for j in range(i):
                res = col.find_one({"tag1": tags[i], "tag2": tags[j]})
                temp.append(res.get("count", 0) if res else 0)
            ans.extend([(i, j, 2 * temp[j] / (tags_count[i] + tags_count[j])) for j in range(len(temp))])
            ans.extend([(j, i, 2 * temp[j] / (tags_count[i] + tags_count[j])) for j in range(len(temp))])
        return ans
    except:
        raise Exception("tag不在数据库中")