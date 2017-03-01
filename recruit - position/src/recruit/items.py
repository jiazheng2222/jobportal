# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
# Datebase: test1
# Table: test

import scrapy

class recruitItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    Position = scrapy.Field()
    Company = scrapy.Field()
    Education = scrapy.Field()
    Salary = scrapy.Field()
    Experience = scrapy.Field()
    Postdate = scrapy.Field()
    Joborder = scrapy.Field()