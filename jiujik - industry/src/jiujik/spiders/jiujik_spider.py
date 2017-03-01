# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import re

from jiujik.items import JiujikItem

class DmozSpider(scrapy.Spider):
    name = "jiujik"
    allowed_domains = ["www.jiujik.com"]
    start_urls = [
        "http://www.jiujik.com/"
        ]

    def parse(self,response):
        print "Current Link is ",response.url  
        content = response.body
                
        # parse the link
        p_link_block = re.compile(r'class=\"row list\"(.*?)<script>',re.DOTALL)
        link_block = (p_link_block.search(content)).group(1)
        
        p_li = re.compile(r'<li>(.*?)</li>')
        p_links = re.compile(r'href=\"(.*)\">')
        p_names = re.compile(r'>(.*)</a>')

        li_list = p_li.findall(link_block)

        for element in li_list:
            
            item = JiujikItem()
            item['Name'] = (p_names.search(element)).group(1)
            item['Link'] = (p_links.search(element)).group(1)
            yield item
