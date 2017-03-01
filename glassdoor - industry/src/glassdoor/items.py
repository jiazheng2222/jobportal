# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
# Datebase: test1
# Table: test

import scrapy

class glassdoorItem(scrapy.Item):
    # define the fields for your item here like:

    Industry = scrapy.Field()
    Link = scrapy.Field()
    PosNum = scrapy.Field()
    Salary = scrapy.Field()