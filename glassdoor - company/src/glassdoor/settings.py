# -*- coding: utf-8 -*-

# Scrapy settings for glassdoor project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

# Use scrapy crawl glassdoor --logfile yblog.txt 
# to direct the log message to file!!!!!!!!!!

BOT_NAME = 'glassdoor'

SPIDER_MODULES = ['glassdoor.spiders']
NEWSPIDER_MODULE = 'glassdoor.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'glassdoor (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'glassdoor.pipelines.glassdoorPipeline': 500,
    }
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6'
#Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0
#"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
#"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
#"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    

DOWNLOAD_DELAY=2

#Database settings
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWD = '1234'
DB_DB = 'glassdoor'
DB_DB_JOBSDB = 'jobsdb'
DB_DB_RECRUIT = 'recruit'

