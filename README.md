# BigDataProject
基于大数据的学习视频数据分析与个性化推荐：以B站2022年知识/科技区视频数据作为分析对象

## 分布式爬取bilibili知识区和科技区视频数据

目的：B站推荐不够个性化，每个用户推荐相同，仅根据单个视频推荐，无法根据多个视频进行推荐

数据内容：

| 数据库键名 | 意义         | 备注       |
| ---------- | ------------ | ---------- |
| aid        | av号         | 主键       |
| title      | 视频标题     |            |
| tag        | 视频tags     | 逗号分隔符 |
| pubdate    | 视频上传时间 |            |
| desc       | 视频简介     |            |
| duration   | 视频长度     | 单位为秒   |
| mid        | UP主UID      |            |
| view       | 播放量       |            |
| danmaku    | 弹幕条数     |            |
| reply      | 评论条数     |            |
| favorite   | 收藏人数     |            |
| coin       | 投币数       |            |
| share      | 分享数       |            |
| his_rank   | 历史最高排名 |            |
| like       | 获赞次数     |            |



- 视频标题 ok
- 视频简介 ok
- 播放数 ok
- 点赞数
- 投币数
- 收藏数
- 分享数
- 评论数
- 弹幕数 ok
- tags ok
- 相关视频推荐 not
- 作者 
- aid ok
- 发布时间 ok

## 视频分析

各个年份月份视频发布量，播放量

分析视频互动率（评论数，弹幕数）

投币点赞比例

分析热门知识或科技领域，趋势

分析视频整体评价（输入bv号，返回整体评价）

## 个性化推荐

相关算法：？

## 通过文字推荐

根据一段描述，个性化推荐相关视频

## 通过视频推荐

根据一个或多个bv号，个性化推荐相关视频
