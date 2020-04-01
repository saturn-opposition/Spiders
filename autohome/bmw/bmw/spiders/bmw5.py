# -*- coding: utf-8 -*-
import scrapy
from bmw.items import BmwItem

class Bmw5Spider(scrapy.Spider):
    name = 'bmw5'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html#pvareaid=3454438']

    def parse(self, response):
        uiboxes = response.xpath('//div[@class=\'uibox\']')[1:]
        for box in uiboxes:
            category = box.xpath('.//div[@class=\'uibox-title\']/a/text()').get()
            urls = box.xpath('.//ul/li/a/img/@src').getall()
            new_urls = []
            for url in urls:
                url = 'https:' + url
                new_urls.append(url)
                item = BmwItem(category=category,image_urls=new_urls)
                yield item

