# BigDataProject项目后端
基于大数据的学习视频数据分析与个性化推荐：以B站2022年知识/科技区视频数据作为分析对象
## 运行命令

`uvicorn main:app --port=5000 --host=0.0.0.0`

环境要求：`python>=3.8，aiohttp>=3.8.3，pymongo>=3.9.0，uvicorn>= 0.18.3，fastapi>=0.85.1，torch>=1.13，transformers>=4.24`

## 整体结构

```
│  basic.py
│  main.py
│  README.md
│
├─AllVideoInfo
│      all_video.py
│
├─database
│      db.py
│
├─functions
│      many_video_info.py
│      sentiment_analysis.py
│      single_video_info.py
│      stop_words.txt
│      word_segment.py
│
├─request
│      request.py
│
├─SingleVideoInfo
│      single_video.py
│
└─VideoRecommendation
        README.md
        video_recommend.py
```


| 代码文件 | 功能 |
| -------- | ---- |
|     `basic.py`     |   提供成功响应和失败响应两个class   |
|     `main.py`     |   后端启动程序   |
|    `all_video.py`      |   负责整体视频数据分析的相关请求   |
|    `db.py`      |   负责数据库的相关操作   |
|     `many_video_info.py`     |   多个视频相关数据获取   |
|     `sentiment_analysis.py`     |   评论情感分析   |
|    `single_video_info.py`      |   单个视频数据获取   |
|     `word_segment.py`     |   评论分词   |
|     `single_video.py`     |  单个视频数据分析    |
|     `video_recommend.py`     |   视频推荐   |

