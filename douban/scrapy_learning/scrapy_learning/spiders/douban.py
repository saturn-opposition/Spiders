# -*- coding: utf-8 -*-
import scrapy
from scrapy_learning.items import ScrapyLearningItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['www.douban.com']
    start_urls = ['https://www.douban.com/group/explore?start=0']

    def parse(self, response):
        channels = response.xpath('//div[@class=\'channel-item\']')
        for c in channels:
           heading = c.xpath('.//h3/a/text()').get()
           content = c.xpath('.//p/text()').get()
           source = c.xpath('.//span[@class=\'from\']/a/text()').get()
           item = ScrapyLearningItem(heading=heading,content=content,source=source)
           yield item
        next_url = response.xpath('//div[@class=\'paginator\']//span[@class=\'next\']/a/@href').get()
        if not next_url:
            return
        else:
            next_url = 'https://www.douban.com/group/explore'+ next_url
            yield scrapy.Request(next_url,callback=self.parse)
