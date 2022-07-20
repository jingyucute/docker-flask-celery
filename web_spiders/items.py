'''
Description: 
Author: jingyu
Date: 2022-07-22 18:23:58
LastEditors: Please set LastEditors
LastEditTime: 2022-07-23 16:16:09
'''
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst

def str_strip(str):
    return str.strip()

def str_to_float(str):
    result = 0
    try:
        result = float(str)
    except Exception as e:
        pass 
    return result


class DoubanTopMovieItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(str_strip),
        output_processor=TakeFirst()
    )
    directors = scrapy.Field()
    publish_year = scrapy.Field(
        # input_processor=MapCompose(int),
        output_processor=TakeFirst()
    )
    country = scrapy.Field(
        output_processor=TakeFirst()
    )
    type = scrapy.Field()
    rate = scrapy.Field(
        input_processor=MapCompose(float),
        output_processor=TakeFirst()
    )
    quote = scrapy.Field(
        input_processor=MapCompose(str_strip),
        output_processor=TakeFirst()
    )
    page = scrapy.Field(
        output_processor=TakeFirst()
    )
    crawl_time = scrapy.Field(
        output_processor=TakeFirst()
    )

    

class PyDasItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


