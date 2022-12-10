import scrapy

class MySpider(scrapy.Spider):
    # Spider的名字
    name = 'bilibili_spider'

    # 允许爬取的域名列表
    allowed_domains = ['bilibili.com']

    # Spider的入口URL
    start_urls = ['https://s.search.bilibili.com/cate/search']

    # 定义一个回调函数，用于处理response
    def parse(self, response):
        # 使用xpath提取页面中的数据
        title = response.xpath('//title/text()').extract_first()
        # 输出提取到的数据
        print(title)
