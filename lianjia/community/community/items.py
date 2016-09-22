# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CommunityItem(scrapy.Item):
    # define the fields for your item here like:
    uid = scrapy.Field()  # 链家id
    name = scrapy.Field()  # 小区名字
    area = scrapy.Field()  # 城区（东城，西城...）
    district = scrapy.Field()  # 商圈
    subway = scrapy.Field()  # 地铁
    station = scrapy.Field()  # 站点
    #
    time = scrapy.Field()  # 建筑年代
    buildingType = scrapy.Field()  # 建筑类型

    count = scrapy.Field()  # 在售套数
    price = scrapy.Field()  # 成交均价
    volume = scrapy.Field()  # 30天成交量


class TradeItem(scrapy.Item):
    bizcircle_id = scrapy.Field()
    community_id = scrapy.Field()
    house_code = scrapy.Field()
    title = scrapy.Field()
    kv_house_type = scrapy.Field()
    cover_pic = scrapy.Field()
    frame_id = scrapy.Field()
    blueprint_hall_num = scrapy.Field()
    blueprint_bedroom_num = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    unit_price = scrapy.Field()
    sign_date = scrapy.Field()
    sign_timestamp = scrapy.Field()
    sign_source = scrapy.Field()
    orientation = scrapy.Field()
    floor_state = scrapy.Field()
    building_finish_year = scrapy.Field()
    decoration = scrapy.Field()
    building_type = scrapy.Field()
