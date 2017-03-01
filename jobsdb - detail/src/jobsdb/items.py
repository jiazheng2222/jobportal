# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
# Datebase: test1
# Table: test

import scrapy

class JobsdbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    PostDate = scrapy.Field()
    EmployID = scrapy.Field()
    PositionID = scrapy.Field()
    Position = scrapy.Field()
    CareerLvl = scrapy.Field()
    WorkExperience = scrapy.Field()
    Qualification = scrapy.Field()
    Industry = scrapy.Field()
    Function = scrapy.Field()
    Location = scrapy.Field()
    Salary = scrapy.Field()
    Type = scrapy.Field()
    Links = scrapy.Field()
    Company = scrapy.Field()
    Content = scrapy.Field()
    