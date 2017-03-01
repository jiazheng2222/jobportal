# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import re

from recruit.items import recruitItem
from _cffi_backend import callback
from twisted.spread.pb import respond
from scrapy.http import Request

class DmozSpider(scrapy.Spider):
    name = "recruit"
    #allowed_domains = ["recruit.com.hk"]
    allowed_domains = ["recruit.com.hk"]
    
    start_urls = ["http://recruit.com.hk"]
    
    def parse(self,response):
        content = response.body
        self.logger.info('Top Link - Parse function called on %s', response.url)
                
        # parse the link
        p_industry_area = re.compile(r'id=\"industryView\">(.*?)</div>',re.DOTALL)
        p_li_list = re.compile(r'<li>(.*?)</li>',re.DOTALL)
        p_li_link = re.compile(r'href=\"(.*?)\">',re.DOTALL)
        p_li_industry = re.compile(r'\">(.*)</a>',re.DOTALL)
        
        #with open("links.txt",'wb') as f:
            #f.write(content)
        industry_area = p_industry_area.search(content).group(1)
        li_list = p_li_list.findall(industry_area)
        print len(li_list)
        for li in li_list:
            item = recruitItem()
            li_industry = p_li_industry.search(li)
            if li_industry != None:
                item['Industry'] = li_industry.group(1).lstrip()
            else:
                item['Industry'] = ''
            li_link = p_li_link.search(li)
            if li_link != None:
                item['Link'] = "http://www.recruit.com.hk"+li_link.group(1)
            else:
                item['Link'] = ''
                
            yield item
                    
    