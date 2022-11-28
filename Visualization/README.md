# 前端功能

## 数据展示页面

数据库：

- 每个月的视频发布量->柱状图展示：某地区蒸发量和降水量  【爬】【ok】

- 每个月份，tag的视频数->动态折线图展示：动态折线图  【算】
- {词：频数}->标题词云【已有】
- 优质视频，宝藏视频【算：播放量】
- tag之间的关联程度【算】
- 热门视频与热门tag->关系图【】

动态数据：

- 用户输入bv号，可视化展现视频数据（播放数、点赞数（超过数据库内XX%视频）、互动率），视频评价

## 推荐

- 根据描述推荐：返回前五条视频数据（封面，bv号，链接）
- 根据视频推荐（前端传多个bv号）：返回前五条视频数据（封面，bv号，链接）







# 项目前端页面

技术栈为：Vite + Vue3 + ElementUI + ECharts









下面是实验过程，并非需要用户操作，仅仅只是为了记录！

## 项目构建

先初始化一个vue3项目：

![image-20221125144213582](https://qihang-1306873228.cos.ap-chongqing.myqcloud.com/imgs/image-20221125144213582.png)

安装elementUI：

```bash
npm install element-plus --save
```

使用elementUI地自动导入功能，参考[快速开始 | Element Plus (element-plus.org)](https://element-plus.org/zh-CN/guide/quickstart.html#按需导入)。

安装Echarts：

```bash
npm install echarts --save
```



