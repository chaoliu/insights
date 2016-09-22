# -*- coding: utf-8 -*-
import scrapy

import json
import MySQLdb

from community.items import TradeItem

class TradeSpider(scrapy.Spider):
    name = "trade"
    allowed_domains = ["lianjia.com"]
    start_urls = (
        'http://m.api.lianjia.com/house/chengjiao/search?channel=chengjiao&city_id=110000&limit_count=100&limit_offset=0&access_token=&utm_source=&device_id=c2245dfb-d29d-4ddb-a61f-fd72544e3640',
    )

    offset = 0
    # last = 1461513600
    # 1311
    def __init__(self, *args, **kwargs):
        self.last = int(self.getLastCursor())
        super(TradeSpider, self).__init__(*args, **kwargs)

    def getLastCursor(self):
        sql = "SELECT max(sign_timestamp) FROM chengjiao"

        db = MySQLdb.connect(host="localhost",user="reader",passwd="hh$reader",db="caravel", port=3309 )
        cursor = db.cursor()
        cursor.execute(sql)

        return cursor.fetchone()[0]


    def parse(self, response):
        more = 1
        if response.body:
            lists = json.loads(response.body)
            if lists['errno'] == 0:
                tradeItem = TradeItem()
                for item in lists['data']['list']:
                    # print item
                    if item['sign_timestamp'] > self.last:
                        for k, v in item.iteritems():
                            tradeItem[k] = v
                        yield tradeItem
                    else:
                        more = 0
                # next page
                if more:
                    self.offset += 100
                    url = 'http://m.api.lianjia.com/house/chengjiao/search?channel=chengjiao&city_id=110000&limit_count=100&limit_offset=%s&access_token=&utm_source=&device_id=c2245dfb-d29d-4ddb-a61f-fd72544e3640' % self.offset
                    yield scrapy.Request(url, callback=self.parse)

            else:
                self.logger.error('Error: %s' % response.body)
        else:
            self.logger.error('Error: response body is empty!')


#
# if __name__ == '__main__':
#
#     trade = TradeSpider()
#     print trade.last + 1
