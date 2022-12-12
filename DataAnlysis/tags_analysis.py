from database.mongo_db import query_all_video_tags, insert_many_data
from tqdm import tqdm

data = query_all_video_tags()

ans = dict((i, dict()) for i in range(1, 12))
tags_count = dict()
tags_relation_count = dict()
for tags, date in tqdm(data):
    lst = tags.split(",")
    for tag in lst:
        ans[date.month][tag] = ans[date.month].get(tag, 0) + 1
        tags_count[tag] = tags_count.get(tag, 0) + 1
    for i in range(len(lst)):
        for j in range(i):
            tags_relation_count[lst[i]] = tags_relation_count.get(lst[i], {})
            tags_relation_count[lst[i]][lst[j]] = tags_relation_count[lst[i]].get(lst[j], 0) + 1
            tags_relation_count[lst[j]] = tags_relation_count.get(lst[j], {})
            tags_relation_count[lst[j]][lst[i]] = tags_relation_count[lst[j]].get(lst[i], 0) + 1

# 统计的月份中tags出现次数
insert_many_data("month_tags", [{"month": month, "tag": tag, "count": count} for month, v in ans.items() for tag, count in v.items()])
# tags总出现次数
insert_many_data("tags_count", [{"tag": k, "count": v} for k, v in tags_count.items()])
# tag间一起出现的次数
insert_many_data("tags_relation", [{"tag1": tag1, "tag2": tag2, "count": count} for tag1, v in tags_relation_count.items() for tag2, count in v.items()])
