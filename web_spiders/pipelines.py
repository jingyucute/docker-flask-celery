'''
Description: 
Author: jingyu
Date: 2022-07-22 18:23:58
LastEditors: Please set LastEditors
LastEditTime: 2022-07-23 15:47:31
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from web_spiders.items import DoubanTopMovieItem
from py_toolkits.db import MongoDB
import base_config

class PyDasPipeline:

    def open_spider(self, spider):
    #    print('open spider', spider)
    #    print(spider.name == "douban_top_movie")
        if spider.name == "douban_top_movie":
            spider.db = MongoDB(**{
                "host": base_config.MONGO_HOST,
                "port": base_config.MONGO_PORT,
                "user": base_config.MONGO_USER,
                "passwd": base_config.MONGO_PASSWORD,
                "db": base_config.MONGO_DB
            })

    def close_spider(self, spider):
       if spider.name == "douban_top_movie":
            print("scrapy over ")

    def process_item(self, item, spider):
        if isinstance(item, DoubanTopMovieItem):
            save_item = dict(item)
            spider.db.insert("douban_top_movies", save_item)
            # print("douban_top_movie item", dict(item))
        # return item
