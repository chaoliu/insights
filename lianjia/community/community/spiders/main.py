# -*- coding: utf-8 -*-
import scrapy

import re
import json
import time
import urllib

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from community.items import CommunityItem


class MainSpider(scrapy.Spider):
    name = "main"
    allowed_domains = ["lianjia.com"]

    def start_requests(self):
        url = 'http://bj.lianjia.com/xiaoqu/'
        return [ scrapy.Request(url, callback=self._parseArea) ]

    def parse(self, response):
        for sel in response.xpath('//*[@id="house-lst"]/li'):
            item = CommunityItem()
            uid = sel.xpath('div[2]/h2/a/@href').re("/xiaoqu/(\d+)/")
            item['uid']  = '' if len(uid)==0 else uid[0]

            # print item['uid']
            name = sel.xpath('div[2]/h2/a/text()').extract()
            item['name'] = '' if len(name)==0 else name[0]
            item['area'] = sel.xpath('div[2]/div[1]/div[2]/div/a[1]/text()').extract()[0]
            item['district'] = sel.xpath('div[2]/div[1]/div[2]/div/a[2]/text()').extract()[0]

            subway = sel.css('.fang-subway-ex span::text').re('\D*(\d*)%s(.*)' % '号线'.decode('utf-8'))

            # print subway
            item['subway'] = '' if len(subway) == 0 else subway[0]
            item['station'] = '' if len(subway) == 0 else subway[1]

            time = sel.css('.con::text')[1].re('(\d+).*')

            item['time'] = '' if len(time) == 0 else time[0]
            item['buildingType'] = sel.css('.con::text')[0].extract()

            #
            item['count'] = sel.css('.square .num::text').extract()[0]

            price = sel.css('.price .num::text').extract()

            item['price'] = '' if len(price) == 0 else price[0]
            item['volume'] = sel.css('.laisuzhou::text')[0].re('30.*(\d+).*')[0]
            yield item

        # next page
        page = response.css('.page-box::attr(page-data)').extract()[0]
        page = json.loads(page)

        if page['curPage'] <= page['totalPage']:
            next = page['curPage'] + 1
            replace_reg = re.compile(r'\d+')
            url = replace_reg.sub(str(next), response.url)
            # url = 'http://bj.lianjia.com/xiaoqu/dongcheng/pg' + str(next)
            # print url
            yield scrapy.Request(url, callback=self.parse)


    def _parseArea(self,response):
        areas = response.xpath('//*[@id="filter-options"]/dl[1]/dd/div[1]/a/@href').re('/xiaoqu/\w+')

        base = 'http://bj.lianjia.com'
        for area in areas:
            url = base + area + '/pg1/'
            # print url
            yield scrapy.Request(url, callback=self.parse)
            #
            # break
