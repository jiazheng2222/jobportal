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

    PostDate = scrapy.Field()
    PositionID = scrapy.Field()
    Position = scrapy.Field()
    Company = scrapy.Field()
    Content = scrapy.Field()
    Industry = scrapy.Field()
    Function = scrapy.Field()
    JobLvl = scrapy.Field()
    MinCareerLvl = scrapy.Field()
    WorkExperience = scrapy.Field()
    Salary = scrapy.Field()
    Location = scrapy.Field()
    Benefits = scrapy.Field()
    Links = scrapy.Field()
        
    