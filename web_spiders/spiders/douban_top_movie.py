'''
Description: 
Author: jingyu
Date: 2022-07-22 18:23:58
LastEditors: Please set LastEditors
LastEditTime: 2022-07-23 16:16:51
'''

from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from web_spiders.items import DoubanTopMovieItem
import re, time


class DoubanTopMovieSpider(Spider):
    name = 'douban_top_movie'
    
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.db = None

    def start_requests(self):
        self.db.drop_table("douban_top_movies")
        base_url = "https://movie.douban.com/top250"
        start = 1
        page = 10
        for i in range(start, start+page):
            if i == 1:
                request_url = base_url
            else:
                request_url = base_url + "?start={start}&filter=".format(start=25*(i - 1))            
            print(request_url)
            yield Request(url=request_url, meta={'page': i}, callback=self.parse, errback=self.parse_err)

    
    def parse(self, response):
        movie_items = response.xpath("//ol[contains(@class, 'grid_view')]//li")
        for movie_item in movie_items:
            l = ItemLoader(item=DoubanTopMovieItem(),selector=movie_item)
            l.add_xpath('title', ".//div[contains(@class, 'info')]//div[contains(@class, 'hd')]//span[contains(@class, 'title')]/text()")
            l.add_xpath("rate", ".//div[contains(@class, 'info')]//div[contains(@class, 'bd')]//div[contains(@class, 'star')]//span[contains(@class, 'rating_num')]//text()")
            l.add_xpath('quote', ".//div[contains(@class, 'info')]//div[contains(@class, 'bd')]//p[contains(@class, 'quote')]//span//text()")
            
            infos = movie_item.xpath(".//div[contains(@class, 'info')]//div[contains(@class, 'bd')]//p[1]//text()").extract()
            length = len(infos)
            publish_year = ''
            country = ''
            type = []
            directors = []

            if length >= 1:
                data = infos[0].strip()
                index = data.find("\xa0\xa0\xa0主")
                director_data = data
                if index != -1:
                    director_data = data[0:index]

                director_data = director_data.replace("导演:", "")
                temps  = director_data.split('/')
                for direct in temps:
                    direct = direct.strip()
                    direct = re.sub('[a-zA-Z-]', '', direct)
                    directors.append(direct.strip())
            l.add_value("directors", directors)

            if length >= 2:
                datas = infos[1].strip().split('/')

                c = datas[-1]
                b = datas[-2]
                a = ','.join(datas[:-2])

                publish_year = a.strip()

                country = b.strip()

                ts = c.split(' ')
                r = []
                for t in ts:
                    r.append(t.strip())
                type = t


            l.add_value('publish_year', publish_year)       
            l.add_value('country', country)       
            l.add_value('type', type) 

            l.add_value('page', response.meta['page'])
            l.add_value('crawl_time', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))      

            yield l.load_item()

    def parse_err(self, failure):
        request = failure.request
        print("There has a error")
        