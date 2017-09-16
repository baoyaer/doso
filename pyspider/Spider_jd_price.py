#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-09-12 20:20:39
# Project: jd_price
import pymongo
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = { 'headers': { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
        }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://search.jd.com/search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC%E7%94%B5%E8%84%91&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.his.0.0&wtype=1&ev=exprice_10000gt%5E&uc=0#J_searchWrap', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        print response.doc('a[href*="item.jd.com"]').items()
        for each in response.doc('a[href*="item.jd.com"]').items():
            href = each.attr.href
            self.crawl(href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        if "item.jd.com/" in response.url:
            return {
                "url": response.url,
                "commid": self.__parse_jdcommid__(response.url),
                "title": response.doc('title').text(),
            }

    def __parse_jdcommid__(self, str):
        str_1 = "item.jd.com/"
        str_2 = ".html"
        begin = str.find(str_1)
        end = str.find(str_2)
        if begin == -1 or end == -1:
            return ""
        else:
            return str[begin + str_1.__len__():end]

    def on_result(self, result):
        if not result:
                return
        #BaseHandler.on_result(self, result)
        client = pymongo.MongoClient(host='10.243.10.231', port=27017)
        db = client['pyspider_projectdb']
        coll = db['website']
        # 保证商品信息唯一
        commid = result['commid']
        data = {
            'title': result['title'],
            'commid': commid,
            'url': result['url'],
        }

        data_id = coll.update({"commid": commid}, {"$set": data}, {"upsert": True})
        print(data_id)
