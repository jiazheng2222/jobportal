# -*- coding: utf-8 -*-

# Scrapy settings for jobsdb project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

# Use scrapy crawl jobsdb --logfile yblog.txt 
# to direct the log message to file!!!!!!!!!!

BOT_NAME = 'recruit'

SPIDER_MODULES = ['recruit.spiders']
NEWSPIDER_MODULE = 'recruit.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jobsdb (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'recruit.pipelines.JobsdbPipeline': 500,
    }

DOWNLOAD_DELAY=2

#Database settings
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWD = '1234'
DB_DB = 'recruit'

