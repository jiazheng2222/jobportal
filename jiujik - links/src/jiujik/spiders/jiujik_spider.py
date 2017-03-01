# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import re

from jiujik.items import JiujikItem
from _cffi_backend import callback
from twisted.spread.pb import respond
from scrapy.http import Request
import numbers

class DmozSpider(scrapy.Spider):
    name = "jiujik"
    allowed_domains = ["myjobs.jiujik.com"]
    
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
        p_number_l = re.compile(r'id=\"search_navi\">(.*?)</em>',re.DOTALL)
        number_l = p_number_l.search(content)
        number = 0
        if number_l != None:
            p_number_r = re.compile(r'<em>(.*)')
            p_result_number = p_number_r.search(number_l.group(1))
            number = int(p_result_number.group(1))
                    
        number_pages = int(number / 15) + 1
        temple = response.url+"/"
        
        yield Request(response.url, callback=self.parse_industry_list,)
        for i in range(2,number_pages+1,1):
            url = temple + str(i)
            yield Request(url, callback=self.parse_industry_list)
        
    def parse_industry_list(self, response):
        self.logger.info('Parse industry: %s', response.url)
        content = response.body
                               
        # parse the content
        p_link_table = re.compile(r'<tbody class=\"job_list\">(.*?)</table>',re.DOTALL)
        links_table = (p_link_table.search(content)).group(1)
        p_list = re.compile(r'<tr(.*?)</tr>',re.DOTALL)
        #parse position and links together
        p_td = re.compile(r'<td(.*?)</td>', re.DOTALL)
        p_job_title_block = re.compile(r'class=\"job_title\">(.*?)</a>',re.DOTALL)
        p_positions = re.compile(r'>(.*)',re.DOTALL)
        p_links = re.compile(r'href=\'(.*?)\'',re.DOTALL)
        
        p_companies = re.compile(r'\'>(.*)</a>',re.DOTALL)
        p_location = re.compile(r'<span (.*?)<', re.DOTALL)

        list_all = p_list.findall(links_table)

    
        for element in list_all:
            job_title_exist = p_job_title_block.search(element)
            if job_title_exist == None:
                continue
             
            job_title_block =(p_job_title_block.search(element)).group(1)
            positions = (p_positions.search(job_title_block)).group(1)
            links = (p_links.search(job_title_block)).group(1)
                
            td_list = p_td.findall(element)
                            
            company = p_companies.search(td_list[2])
            industry = re.search(r'>(.*)',td_list[3])
            wrklvl = re.search(r'>(.*)',td_list[4])
            experience = re.search(r'>(.*)',td_list[5])
            salary = re.search(r'>(.*)',td_list[6])
            degree = re.search(r'>(.*)',td_list[7])
            type = re.search(r'>(.*)',td_list[8])
            postdate = re.search(r'<td>(.*)',td_list[9])
            location_tmp = (p_location.search(td_list[9])).group(1)
            location = location_tmp.strip()
            
            item = JiujikItem()
            item['Position'] = positions
            if company != None:
                item['Company'] = company.group(1)
            else:
                item['Company'] = "--"
            item['Link'] = "http://myjobs.jiujik.com"+links
            item['Location'] = location
            item['industry'] = industry.group(1)
            item['wrklvl'] = wrklvl.group(1)
            item['experience'] = experience.group(1)
            item['salary'] = salary.group(1)
            item['degree'] = degree.group(1)
            item['type'] = type.group(1)
            item['postdate'] = postdate.group(1)
            yield item
