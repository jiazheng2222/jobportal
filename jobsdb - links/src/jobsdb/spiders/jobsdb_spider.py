# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import re

from jobsdb.items import JobsdbItem
from _cffi_backend import callback
from twisted.spread.pb import respond
from scrapy.http import Request
import numbers

class DmozSpider(scrapy.Spider):
    name = "jobsdb"
    allowed_domains = ["hk.jobsdb.com"]
    
    start_urls = []
    with open('lists.txt','rb') as openfile:
        for line in openfile:
            temple = line.rstrip()
            start_urls.append(temple) 

    # Get the number of each industry and generate the link list
    def parse(self,response):
        content = response.body
        self.logger.info('Top Link - Parse function called on %s', response.url)
                
        # get the number
        p_number_l = re.compile(r'id=\"firstLineCriteriaContainer\"(.*?)</em>',re.DOTALL)
        number_l = p_number_l.search(content)
        number = 0
        if number_l != None:
            p_number_r = re.compile(r'<em>(.*)')
            p_result_number = p_number_r.search(number_l.group(1))
            number = int(p_result_number.group(1))
        
        number_pages = int(number / 50) + 1
        temple = re.search(r'(.*)1$',response.url).group(1)
        
        
        for i in range(1,number_pages+1,1):
            url = temple + str(i)
            yield Request(url, callback=self.parse_industry_list)
        
    def parse_industry_list(self, response):
        self.logger.info('Parse industry: %s', response.url)
        content = response.body
                               
        # parse the content
        p_link_rough = re.compile(r'id\=\"JobListingSection\"(.*?)result-pagination',re.DOTALL)
        tmp_result = p_link_rough.findall(content)
        links_rough = tmp_result[0]
                        
        p_list = re.compile(r'id="Row(.*?)Applied</span>')
        #parse position and links together
        p_job_title = re.compile(r'job-title(.*?)</h3>')
        p_links = re.compile(r'href\=\"(.*?)\"')
        p_positions = re.compile(r'cp\d*\">(.*)</a>')
        
        p_companies_tmp = re.compile(r'CompanyAction(.*)</a>')
        p_companies = re.compile(r'\>(.*)<ins>')
        p_locations = re.compile(r'address\">(.*?)</span>')

        list = p_list.findall(links_rough)
        links = []
        positions = []
        companies = []
        locations = []
                
        for element in list:
            job_title =(p_job_title.search(element)).group(1)        
            tmp = (p_companies_tmp.search(element)).group(1)

            item = JobsdbItem()
            item['Position'] = (p_positions.search(job_title)).group(1)
            item['Company'] = (p_companies.search(tmp)).group(1)
            item['Location'] = (p_locations.search(element)).group(1)
            item['Link'] = (p_links.search(job_title)).group(1)
            yield item
    