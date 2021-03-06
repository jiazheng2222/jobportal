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

    GSId = scrapy.Field()
    Name = scrapy.Field()
    Website = scrapy.Field()
    AllRating = scrapy.Field()
    LogoAddress = scrapy.Field()
    Industry = scrapy.Field()
    SectorName = scrapy.Field()
    IndustryName = scrapy.Field()
    CeoName = scrapy.Field()
    CeoTitle = scrapy.Field()
