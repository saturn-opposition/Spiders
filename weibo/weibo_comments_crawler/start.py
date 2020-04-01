#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from scrapy import cmdline
import pymysql

import time
import random
import os
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='hjnmysqlmima0930', db='weibo_data')
cursor = conn.cursor()
cursor.execute("select id from weibo where screen_name = \'人民日报\'")
row = cursor.fetchall()
id = []
for i in range(len(row)):
    id.append(row[i][0])
print("共"+str(len(id))+"条微博")
for i in range(4093,len(id)):
    print('第'+str(i)+'条微博')
    try:
        os.system('scrapy crawl comment -a WEIBO_ID=' + id[i]+ ' -a WEIBO_MID=' +id[i])
        # cmdstr = 'scrapy crawl comment -a WEIBO_ID=' + id[i]+ ' -a WEIBO_MID=' +id[i]
        # cmdline.execute(cmdstr.split())
    except:
        time.sleep(random.randint(5,30))

print('所有微博评论爬取完毕')

