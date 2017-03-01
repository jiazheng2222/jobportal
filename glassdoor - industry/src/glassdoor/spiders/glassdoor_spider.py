# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import re
import json

from glassdoor.items import glassdoorItem
from _cffi_backend import callback
from twisted.spread.pb import respond
from scrapy.http import Request, FormRequest

class DmozSpider(scrapy.Spider):
    name = "glassdoor"
    allowed_domains = ["glassdoor.com"]
    
    start_urls = ["https://www.glassdoor.com/index.htm"]
    
    #start_urls = []
    #start_urls.append("https://www.glassdoor.com/Job/public-relations-jobs-SRCH_KO0,16.htm")
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,cookies={
                                'ARPNTS' :'191211712.36895.0000',
' gdId' :'9aca0301-c27b-4e05-9ffc-09a0388cef93',
' __utma' :'88367261.1359524526.1444112040.1456117357.1456120543.20',
' optimizelySegments' :'%7B%22203410388%22%3A%22referral%22%2C%22205068319%22%3A%22ff%22%2C%22205072306%22%3A%22false%22%7D',
' optimizelyEndUserId' :'oeu1444112041341r0.07885076386898926',
' optimizelyBuckets' :'%7B%7D',
' _ga' :'GA1.2.1359524526.1444112040',
' __ar_v4' :'TTR273FZT5BTPAZS7GPAI4%3A20160211%3A1%7CY425ZXNYUJFP5KUDBXHENG%3A20160211%3A67%7CETX7GD4DFZFVREUYC2AJK3%3A20160211%3A68%7CUHTYLV6APJBAREEHGMJYXJ%3A20160211%3A68',
' __qca' :'P0-169315631-1444112042828',
' uc' :'8F0D0CFA50133D96DAB3D34ABA1B8733A2E05B20936C3416DD880AADB4DDE1F7D89FC485869D5421F5616CEAA1A59A9F87A00184D20608C5D98730C490799C18D736DB6CD026B9F9967366846165BE3A112590DA3879599729AD6D8D10777073B49086EA2AD696D08408283AAE277D3001288EBCA930B9E2D08052C263276A3A18F5C59AB02FE73D5FFB74084D4A00E8AEEFC6DF5CAC41BCE6EAB934971C770A52B6178747EDEF3F',
' __utmv' :'88367261.|4=GDSegment=Job-Searcher=1',
' __gads' :'ID=7003a5e4e31d31f6:T=1444215206:S=ALNI_MbyClgFa29COCg77AjeGnzpSz1PeQ',
' D_SID' :'175.159.102.24:s7rfgpBqQXENPjlJdvWGBxljNJ5bqtEiT4XdYLh5uzw',
' D_PID' :'7E87B955-84EB-3578-A991-B8948732DC33',
' D_IID' :'95ED3DE9-2A6E-3BFC-AB4D-6C1F4F32F5A5',
' D_UID' :'EEA8BCD7-3D5C-3A54-AB00-4AD91B18C34F',
' D_HID' :'hRyky9CrTdyhzQ1FJr7AsbcoPu4TFYhlYFqx3GsJANA',
' __utma' :'249728464.1359524526.1444112040.1455089168.1455089168.1',
' RT' :'sl=2&ss=1456120541460&tt=5426&obo=0&sh=1456120555908%3D2%3A0%3A5426%2C1456120544434%3D1%3A0%3A2971&dm=glassdoor.com&si=fb51ef47-5cfb-44ca-b5bd-42839cb9f7ab&bcn=%2F%2F36fb68c2.mpstat.us%2F&nu=https%3A%2F%2Fwww.glassdoor.com%2FJob%2Fbusiness-administration-jobs-SRCH_KO0%2C23.htm&cl=1456120793698&r=https%3A%2F%2Fwww.glassdoor.com%2Findex.htm&ul=1456120894753',
' rs' :'"sc.keyword%3Dsoftware+engineer%26locT%3D%26locId%3D0%26locKeyword%3D:sc.keyword%3Dpublic+relations%26locT%3D%26locId%3D0%26locKeyword%3D:sc.keyword%3Dbusiness+administration%26locT%3D%26locId%3D0%26locKeyword%3D:sc.keyword%3Dibm%26locT%3D%26locId%3D0%26locKeyword%3D:sc.keyword%3D%26locT%3DC%26locId%3D2309313%26locKeyword%3DKowloon:sc.keyword%3Dtest%26locT%3DC%26locId%3D2309313%26locKeyword%3DKowloon"',
' mp_5d4806b773713d93bd344cf2365e6df0_mixpanel' :'%7B%22distinct_id%22%3A%20%2215041f26d84397-0b9a38d787dc24-45504331-144000-15041f26d8547c%22%2C%22%24initial_referrer%22%3A%20%22http%3A%2F%2Fwww.glassdoor.com%22%2C%22%24initial_referring_domain%22%3A%20%22www.glassdoor.com%22%7D',
' ht' :'%7B%22quantcast%22%3A%5B%22D%22%5D%2C%22bizo%22%3A%5B%5D%7D',
' __utmz' :'88367261.1456113375.18.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
' JSESSIONID' :'9B7C74F9EBBA5E7D35A1B5D863A92789',
' __utmb' :'88367261.3.9.1456205270',
' __utmc' :'88367261',
' __utmt' :'1',
' _dc_gtm_UA-2595786-1' :'1',
' _gat_UA-2595786-1' :'1'
})
    
    def parse(self,response):
        content = response.body

        p_ul = re.compile(r'<ul class=\'undecorated(.*?)</ul>', re.DOTALL)
        p_li = re.compile(r'<li(.*?)</li>', re.DOTALL)
        p_list_content = re.compile(r'<p class=\'tightVert\'>(.*?)</p>')
        p_list_attribute = re.compile(r'class=\'tightVert minor\'>(.*?)</')
        p_list_name = re.compile(r'>(.*)</a>')
        p_list_link = re.compile(r'<a href=(\'|\")(.*)(\'|\")>')
        temple = "https://www.glassdoor.com"
        
        ul_list = p_ul.findall(content)
        for ul_item in ul_list:
            li_list = p_li.findall(ul_item)
            for li_item in li_list: 
                item = glassdoorItem()
                list_content = p_list_content.findall(li_item)
                list_attribute = p_list_attribute.findall(li_item)
                item['Industry'] = (p_list_name.search(list_content[0])).group(1)
                item['Link'] = temple+(p_list_link.search(list_content[0])).group(2).strip() 
                item['PosNum'] = list_attribute[0]
                item['Salary'] = list_attribute[1]
                    
                yield item

    