# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
# Datebase: test1
# Table: test

import scrapy

class JiujikItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    Position = scrapy.Field()
    Company = scrapy.Field()
    Location = scrapy.Field()
    Link = scrapy.Field()
    industry = scrapy.Field()
    wrklvl = scrapy.Field()
    experience = scrapy.Field()
    salary = scrapy.Field()
    degree = scrapy.Field()
    type = scrapy.Field()
    postdate = scrapy.Field()