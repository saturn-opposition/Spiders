# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class WeiboCommentPipeline(object):
    def open_spider(self, spider):
        """
        爬虫开启时会执行此方法
        :param spider:
        :return:
        """
        # self.file = open('comment.csv', 'w', encoding='gbk')
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='hjnmysqlmima0930', db='weibo_data')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            res = dict(item)
            # 为了防止评论中有英文逗号导致csv分列错误，将字符串用英文双引号包裹可以解决这种问题
            # line = '"%s","%s"' % (res['nick'], res['comment'])
            # self.file.write(line + '\n')
            row = self.cursor.execute(
                "insert into comments(wid ,user,content)values(%s, %s,%s)",
                (res['wid'],res['nick'],res['comment']))
            self.conn.commit()
            print("存入sql")
        except Exception as e:
            print(e)
        return item

    def close_spider(self, spider):
        """
        爬虫一旦关闭，就会执行此方法，关闭文件流
        :param spider:
        :return:
        """
        self.conn.close()
        # raise AttributeError
