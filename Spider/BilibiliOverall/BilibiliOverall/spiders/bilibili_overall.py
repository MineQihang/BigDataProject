import scrapy


class BilibiliOverallSpider(scrapy.Spider):
    name = 'bilibili_overall'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://www.bilibili.com/v/knowledge/business/#/all/click/0/1/2022-12-03,2022-12-10']

    def parse(self, response):
        print(response.text)
        raw_text = response.xpath('//div[@class="page-total"]/span/text()').extract_first()
        print(raw_text)
        num = raw_text.split(" ")
        print(num)
