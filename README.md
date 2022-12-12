# BigDataProject
基于大数据的学习视频数据分析与个性化推荐：以B站2022年知识/科技区视频数据作为分析对象。

对于以下几个部分更详细的文档详见目录下的README文件和项目报告。

## 数据爬取

本部分对应`Spider`文件夹。

使用`Aiohttp`实现异步分布式爬虫。

## 视频分析

本部分对应`DataAnalysis`文件夹。

使用`Hadoop+Spark`对总体数据进行大数据分析。

## 后端部署

本部分对应`Backend`文件夹。

其中主要包括单视频分析（评论情感分析等），视频推荐等。

## 前端部署

本部分对应`Visualization`文件夹。

使用`Vue+Element+ECharts`实现数据可视化。

