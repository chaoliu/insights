# -*- coding: utf-8 -*-
import scrapy
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class MainSpider(scrapy.Spider):
    nextPage = 1
    name = "main"
    allowed_domains = ["https://licai.lianjia.com"]
    start_urls = (
        'https://licai.lianjia.com/index/sort?sortType=0&page=1&num=10&t=6NpCwdF5',
    )

    def parse(self, response):

        if not response.body:
            self.log('body is empty: ' % self.nextPage, level=logging.ERROR)
        else:
            result = json.loads(response.body.decode('utf-8'))

            # print result
            
            lists = result['data']

            for item in lists:
                yield item
                # yield item

        if self.nextPage <= 3:
            self.nextPage += 1
            url = "https://licai.lianjia.com/index/sort?sortType=0&page=%s&num=10&t=6NpCwdF5" % self.nextPage
            yield scrapy.Request(url, callback=self.parse)