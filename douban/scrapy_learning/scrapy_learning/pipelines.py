# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

# class ScrapyLearningPipeline(object):
#     def __init__(self):
#         self.fp = open("doubantiezi.csv",'w',encoding='utf-8',newline='')
#         header_a = ['标题','内容','来源']
#         self.csvwriter = csv.writer(self.fp)
#         self.csvwriter.writerow(header_a)
#     def open_spider(self,spider):
#         print("开始爬取")
#     def process_item(self, item, spider):
#         head = item['heading']
#         content = item['content']
#         source = item['source']
#         self.csvwriter.writerow([head,content,source])
#         return item
#     def close_spider(self,spider):
#         self.fp.close()
#         print("爬取结束")

from scrapy.exporters import CsvItemExporter,JsonLinesItemExporter,JsonItemExporter
from scrapy.exporters import JsonItemExporter
class ScrapyLearningPipeline(object):
    def __init__(self):
        self.fp = open("doubantiezi.csv",'wb')
        self.exporter = CsvItemExporter(self.fp,encoding='utf-8')
        self.exporter.start_exporting()
    def open_spider(self,spider):
        print("开始爬取")
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        print("爬取结束")