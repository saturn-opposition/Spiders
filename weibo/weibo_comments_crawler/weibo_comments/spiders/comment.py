# -*- coding: utf-8 -*-
import logging

import scrapy
import json
from weibo_comments_crawler.weibo_comments.items import WeiboCommentItem

# 微博id
# WEIBO_ID = ''
# WEIBO_MID = ''
class CommentSpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = ['m.weibo.cn']
    start_urls = []
    WEIBO_ID = ''
    WEIBO_MID = ''
    def __init__(self,WEIBO_ID=None,WEIBO_MID=None, *args, **kwargs):
        print('微博id:' + WEIBO_ID)
        WEIBO_ID = int(WEIBO_ID)
        WEIBO_MID = int(WEIBO_MID)
        self.WEIBO_ID = WEIBO_ID
        self.WEIBO_MID = WEIBO_MID
        super(eval(self.__class__.__name__), self).__init__(*args, **kwargs)
        self.start_urls = ['https://m.weibo.cn/comments/hotflow?id=%d&mid=%d&max_id_type=0' % (WEIBO_ID, WEIBO_MID)]


    def start_requests(self):
            cookies = {}
            for url in self.start_urls:
                yield scrapy.Request(url=url, callback=self.parse, cookies=cookies)

    def parse(self, response):
        try:
            result = json.loads(response.text, encoding='utf-8')
        except json.decoder.JSONDecodeError:
            print('json解析失败')
            return
        data_list = result['data']['data']
        for data in data_list:
            item = WeiboCommentItem()
            item['wid'] =  self.WEIBO_ID
            item['nick'] = data['user']['screen_name']
            item['comment'] = data['text']
            yield item

            # 获取子评论
            if data['total_number'] and data['total_number'] > 0:
                child_url = 'https://m.weibo.cn/comments/hotFlowChild?cid=%s&max_id=0&max_id_type=0' % data['rootid']
                yield scrapy.Request(url=child_url, callback=self.child_parse)

        # 获取下一页
        if result['data']['max_id'] and result['data']['max_id'] > 0:
            next_url = 'https://m.weibo.cn/comments/hotflow?id=%d&mid=%d&max_id=%d&max_id_type=0' % (self.WEIBO_ID, self.WEIBO_MID, result['data']['max_id'])
            yield scrapy.Request(url=next_url, callback=self.parse)



    def child_parse(self, response):
        try:
            result = json.loads(response.text, encoding='utf-8')
        except json.decoder.JSONDecodeError:
            print('json解析失败')
            return
        data_list = result['data']
        for data in data_list:
            item = WeiboCommentItem()
            item['wid'] = self.WEIBO_ID
            item['nick'] = data['user']['screen_name']
            item['comment'] = data['text']
            yield item

        # 获取下一页
        if result['max_id'] and result['max_id'] > 0:
            next_url = 'https://m.weibo.cn/comments/hotFlowChild?cid=%s&max_id=%d&max_id_type=0' % (result['rootComment'][0]['rootid'], result['max_id'])
            yield scrapy.Request(url=next_url, callback=self.child_parse)

if __name__ == '__main__':
    cookie_str = '_T_WM=19915191835; XSRF-TOKEN=0459ac; WEIBOCN_FROM=1110006030; SUB=_2A25zUK-tDeRhGeFN4lsU9y7PyjmIHXVQujHlrDV6PUJbkdANLWygkW1NQ7-6uRZv-EHqzwl4XNmgZUUZohBGz5ry; SUHB=06ZV7w5EoTjCdy; SCF=Anze7S_q3LGw9BaFkuagiYENlakxeqNdyy7awdeNlkErl3k51ZFTTzyFg2gvjlDDPAf3D39P9NOOOhht0KJRVVs.; SSOLoginState=1582620669; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803%26uicode%3D20000174'
    cookie_params = cookie_str.split(';')
    cookies = {}
    for cookie_param in cookie_params:
        key, value = cookie_param.split('=')
        cookies[key] = value
    print(cookies)
