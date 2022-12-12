# 爬虫

本项目实现了两种方式爬虫。

- **Aiohttp + MySQL伪分布式爬虫**：由于集群电脑数量不够，且需要爬取的数据量巨大，再加之B站有强大的反爬机制，所以需要更多的电脑(IP)来爬取。因此一种方便的部署方式是十分必要的，采用这种方式能很快速地在其他电脑上运行爬取任务。
  - 主要任务：爬取2022年1月1日到2022年11月20日哔哩哔哩知识区和科技区的所有子分区下按热度排序前100页的**详细视频数据**。
- **Scapy + MongoDB分布式爬虫**：主流的分布式数据爬取方法。这种方式对于反爬机制比较弱的API，爬取效果很不错。
  - 主要任务：爬取2022年1月1日到2022年11月20日哔哩哔哩知识区和科技区的所有子分区下**视频数量**。

> **注意：**运行前请一定要在`config`文件夹下创建`config.py`并在里面填写数据库相关信息，下面是一个示例
>
> ```
> # Mysql
> HOST="..."  # 数据库host
> PORT=...  # 数据库端口
> USER="..."  # 数据库用户名
> PASSWORD="..."  # 数据库密码
> DATABASE="..."  # 数据库名称
> 
> # MongoDB
> M_HOST="..."  # 数据库host
> M_PORT=...  # 数据库端口
> M_USER="..."  # 数据库用户 
> M_PASSWORD="..."  # 数据库密码
> ```

## Aiohttp + MySQL 伪分布式爬虫

通过使用`aiohttp`配合`asyncio`同时发起多次请求，快速获取大量数据。再使用`pymysql`将数据保存到MySQL中。

### 基本步骤

1. 运行`add_task.py`向task表内插入任务，表项定义如下：

   | 表项名称  | 类型 | 说明                                                         |
   | --------- | ---- | ------------------------------------------------------------ |
   | id        | int  | 主键，唯一标识一个task                                       |
   | page      | int  | 爬取第几页                                                   |
   | cate_id   | int  | B站小分区id                                                  |
   | time_from | text | 爬取数据的开始时间                                           |
   | time_to   | text | 爬取数据的结束时间                                           |
   | finish    | int  | 完成的标记。`0`表示未处理，`-1`表示正在处理，`-2`表示处理完成，`x`(x>0)表示在爬取过程中有x条数据被拦截了 |

2. 运行`get_main_data.py`获取上文提到的所有数据（限定时间内的所有视频信息等），表项定义如下：

   | 表项名称 | 类型     | 说明                 |
   | -------- | -------- | -------------------- |
   | aid      | bigint   | av号，主键           |
   | title    | text     | 视频标题             |
   | tag      | text     | 视频tags，逗号分隔符 |
   | pubdate  | datetime | 视频上传时间         |
   | desc     | longtext | 视频简介             |
   | duration | bigint   | 视频长度，单位为秒   |
   | mid      | bigint   | UP主UID              |
   | view     | int      | 播放量               |
   | danmaku  | int      | 弹幕条数             |
   | reply    | int      | 评论条数             |
   | favorite | int      | 收藏人数             |
   | coin     | int      | 投币数               |
   | share    | int      | 分享数               |
   | his_rank | bigint   | 历史最高排名         |
   | like     | int      | 获赞次数             |

   这里的`get_main_data.py`可以轻松地在不在集群中的其他电脑上运行（部署非常方便）。

3. 数据库迁移

   由于项目后期发现在大数据量下MySQL数据库增删改查速度很慢，效率低下，因此后期我们将MySQL数据库上的数据迁移到MongoDB。

   运行`mysql2mongo.py`即可将`msql`的`bilibili`数据表迁移至`mongo`数据库中。



## Scrapy + MongoDB 分布式爬虫

进入`BilibiliOverall`运行`scrapy crawl bilibili_overall`即可。







