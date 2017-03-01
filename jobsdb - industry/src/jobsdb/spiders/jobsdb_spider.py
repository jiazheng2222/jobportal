# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import re

from jobsdb.items import JobsdbItem

class DmozSpider(scrapy.Spider):
    name = "jobsdb"
    allowed_domains = ["hk.jobsdb.com"]
    start_urls = [
        "http://hk.jobsdb.com/hk/en/browse"
        ]

    def parse(self,response):
        content = response.body
                
        # parse the link
        p_link_rough = re.compile(r'Job by industry</h3>(.*?)</div>',re.DOTALL)
        tmp_result = p_link_rough.findall(content)
        links_rough = tmp_result[0]
        
        p_list = re.compile(r'<a class(.*?)</a>')
        p_links = re.compile(r'href\=\"(.*?)\">')
        p_names = re.compile(r'">(.*)')

        list = []        
        list = p_list.findall(links_rough)
        names = []

        for element in list:
            #links.append((p_links.search(element)).group(1))
            names.append((p_names.search(element)).group(1))
            
            item = JobsdbItem()
            item['Name'] = (p_names.search(element)).group(1)
            item['Link'] = (p_links.search(element)).group(1)

            yield item
