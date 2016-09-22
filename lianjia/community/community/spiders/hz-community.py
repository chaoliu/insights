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

#uid 1811044508146 数据重复

class HzCommunitySpider(scrapy.Spider):
    name = "hzcommunity"
    allowed_domains = ["lianjia.com"]

    def start_requests(self):
        url = 'http://hz.lianjia.com/xiaoqu/'
        return [ scrapy.Request(url, callback=self._parseArea) ]

    def parse(self, response):
        for sel in response.xpath('/html/body/div[4]/div[1]/ul/li'):
            item = CommunityItem()
            uid = sel.xpath('a/@href').re("/xiaoqu/(\d+)/")
            item['uid']  = '' if len(uid)==0 else uid[0]

            name = sel.css('div.title > a::text').extract()

            item['name'] = '' if len(name)==0 else name[0]
            item['area'] = sel.css('div.positionInfo > a.district::text').extract()[0]
            item['district'] = sel.css('div.positionInfo > a.bizcircle::text').extract()[0]


            #
            if len(sel.css('div.tagList > span')) > 1:
                subway = sel.css('div.tagList > span:nth-child(2)::text').re('\D*(\d*)%s(.*)' % '号线'.decode('utf-8'))
            else:
                subway = sel.css('div.tagList > span::text').re('\D*(\d*)%s(.*)' % '号线'.decode('utf-8'))

                # school ?
            #
            item['subway'] = '' if len(subway) == 0 else subway[0]
            item['station'] = '' if len(subway) == 0 else subway[1]
            #


            time = sel.css('.positionInfo::text')[1].re('(\d+).*')
            #
            item['time'] = '' if len(time) == 0 else time[0]
            # item['buildingType'] = sel.css('.con::text')[0].extract()
            #
            # #
            item['count'] = sel.css('div.sellCount > a > span::text').extract()[0]
            #
            price = sel.css('div.totalPrice > span::text').extract()
            #
            item['price'] = '' if len(price) == 0 else price[0]

            item['volume'] = sel.css('div.houseInfo > a::text')[0].re('90.*(\d+).*')[0]

            yield item

        # next page
        page = response.css('.page-box::attr(page-data)').extract()[0]
        page = json.loads(page)

        if page['curPage'] < page['totalPage']:
            next = page['curPage'] + 1
            replace_reg = re.compile(r'\d+')
            url = replace_reg.sub(str(next), response.url)
            # url = 'http://bj.lianjia.com/xiaoqu/dongcheng/pg' + str(next)
            # print url
            yield scrapy.Request(url, callback=self.parse)


    def _parseArea(self,response):
        areas = response.xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div/a/@href').re('/xiaoqu/\w+')

        base = 'http://hz.lianjia.com'
        for area in areas:
            url = base + area + '/pg1/'
            # print url
            # url = "http://hz.lianjia.com/xiaoqu/pg1"
            yield scrapy.Request(url, callback=self.parse)
            #
            # break
