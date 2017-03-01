# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import re
import json
import MySQLdb

from glassdoor.items import glassdoorItem
from _cffi_backend import callback
from twisted.spread.pb import respond
from scrapy.http import Request, FormRequest
from scrapy.utils.project import get_project_settings

class DmozSpider(scrapy.Spider):
    name = "glassdoor"
    allowed_domains = ["glassdoor.com"]
        
    def start_requests(self):
        SETTINGS = get_project_settings()
        
        # jobsdb
        conn_jobsdb = MySQLdb.connect(                
                db = SETTINGS['DB_DB_JOBSDB'],
                user = SETTINGS['DB_USER'],
                passwd = SETTINGS['DB_PASSWD'],
                host = SETTINGS['DB_HOST'],
                port = SETTINGS['DB_PORT'],
                charset = 'utf8',
                use_unicode = False
                )
        cursor_jobsdb = conn_jobsdb.cursor()
        cursor_jobsdb.execute('SELECT distinct(Company) FROM jobsdb.position ')
        #cursor_jobsdb.execute('SELECT distinct(Company) FROM jobsdb.position where id = "156896" ')
        
        rows_jobsdb = cursor_jobsdb.fetchall()
        cursor_jobsdb.close()
        
        # recruit
        conn_recruit = MySQLdb.connect(                
                db = SETTINGS['DB_DB_RECRUIT'],
                user = SETTINGS['DB_USER'],
                passwd = SETTINGS['DB_PASSWD'],
                host = SETTINGS['DB_HOST'],
                port = SETTINGS['DB_PORT'],
                charset = 'utf8',
                use_unicode = False
                )
        cursor_recruit = conn_recruit.cursor()
        cursor_recruit.execute('SELECT distinct(Company) FROM recruit.position ')
        #cursor_recruit.execute('SELECT distinct(Company) FROM recruit.position where id = "156896" ')
        
        rows_recruit = cursor_recruit.fetchall()
        cursor_recruit.close()
        
        temple_l = 'http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=55571&t.k=dq1mX87IgI&action=employers&q='
        temple_r = '&userip=192.168.43.42&useragent=Mozilla/%2F4.0'
        
        for row in rows_jobsdb:
            query = re.sub('&#[0-9]+;', '', row[0])
            if query != "--":
                yield self.make_requests_from_url(temple_l + query + temple_r)
                
        for row in rows_recruit:
            query = re.sub('&#[0-9]+;', '', row[0])
            if query != "--":
                yield self.make_requests_from_url(temple_l + query + temple_r)
        
    def parse(self,response):
        content = response.body
        self.logger.info('Top Link - Parse function called on %s', response.url)
             
        parsed_json = json.loads(content)
        content_parsed = parsed_json['response']

        for index in range(0,len(content_parsed['employers']),1):
            item = glassdoorItem()
            item['GSId'] = str(content_parsed['employers'][index]['id'])
            item['Name'] = str(content_parsed['employers'][index]['name'])
            item['Website'] = str(content_parsed['employers'][index]['website'])
            item['AllRating'] = str(content_parsed['employers'][index]['overallRating'])
            item['LogoAddress'] = str(content_parsed['employers'][index]['squareLogo'])
            item['Industry'] = str(content_parsed['employers'][index]['industry'])
            if 'sectorName' in content_parsed['employers'][index]:
                item['SectorName'] = str(content_parsed['employers'][index]['sectorName'])
            else:
                item['SectorName'] = ''
            if 'industryName' in content_parsed['employers'][index]:
                item['IndustryName'] = str(content_parsed['employers'][index]['industryName'])
            else:
                item['IndustryName'] = ''

            if 'ceo' in content_parsed['employers'][index]:
                item['CeoName'] = str(content_parsed['employers'][index]['ceo']['name'])
                item['CeoTitle'] = str(content_parsed['employers'][index]['ceo']['title'])
            else:
                item['CeoName'] = ''
                item['CeoTitle'] = ''
            
            yield item

