# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import re
import MySQLdb

from jiujik.items import jiujikItem
from _cffi_backend import callback
from twisted.spread.pb import respond
from scrapy.http import Request
from scrapy import FormRequest
from scrapy.utils.project import get_project_settings

class DmozSpider(scrapy.Spider):
    name = "jiujik"
    allowed_domains = ["myjobs.jiujik.com"]
    
    def start_requests(self):
        SETTINGS = get_project_settings()
        conn = MySQLdb.connect(                
                db = SETTINGS['DB_DB'],
                user = SETTINGS['DB_USER'],
                passwd = SETTINGS['DB_PASSWD'],
                host = SETTINGS['DB_HOST'],
                port = SETTINGS['DB_PORT'],
                charset = 'utf8',
                use_unicode = False
                )
        cursor = conn.cursor()
        
        cursor.execute('SELECT link, position FROM jiujik.position where id between "7781" and "7881" ')
        
        rows = cursor.fetchall()
        for row in rows:
            # Don't deal with chinese position
            try:
                row[1].decode('ascii')
            except UnicodeDecodeError:
                continue
            else:
                yield self.make_requests_from_url(row[0])
        conn.close()
        
    def parse(self, response):
        content = response.body
        self.logger.info('Top Link - Parse function called on %s', response.url)
                           
        # get the whole content, including responsibility
        # The Temple 1:
        #     Using desc to recognize
        p_whole_content_l = re.compile(r'class=\"desc\">(.*)class=\"replyinfo\">', re.DOTALL)
        whole_content_l = p_whole_content_l.search(content)
        # The Temple 2: (No use now)
        #    Expired data
        p_whole_content_expired = re.compile(r'id=\"ExpiredMessagePlaceHolder\"',re.DOTALL)
        whole_content_expired = p_whole_content_expired.search(content)
        
        # The Temple 1:
        if whole_content_l != None:
            item = jiujikItem()
            tmp = re.sub('<.*?>', '', whole_content_l.group(1))
            item['Content'] = tmp
            
            p_company_l = re.compile(r'class=\"company\">(.*?)</',re.DOTALL)
            p_company_r = re.compile(r'>(.*)')
            company_l = p_company_l.search(content)
            company_r = p_company_r.search(company_l.group(1))
            item['Company']= company_r.group(1)
            
            # parse the content
            p_title_l = re.compile(r'class=\"job_title\"(.*?)</')
            p_title_r = re.compile(r'>(.*)')
            
            title_l = (p_title_l.search(content)).group(1)
            item['Position'] = (p_title_r.search(title_l)).group(1)
            
            p_pstdate_l = re.compile(r'class=\"post_on\"(.*?)</')
            p_pstdate_r = re.compile(r'>(.*)')
            
            pstdate_l = (p_pstdate_l.search(content)).group(1)
            item['PostDate'] = (p_pstdate_r.search(pstdate_l)).group(1)  

            p_posiref_l = re.compile(r'class=\"ref_no\"(.*?)</')
            p_posiref_r = re.compile(r'>(.*)')
            
            posiref_l = (p_posiref_l.search(content)).group(1)
            item['PositionID'] = (p_posiref_r.search(posiref_l)).group(1)
            
            
            # Table content
            p_table_l = re.compile(r'<table(.*)</table>', re.DOTALL)
            table_content = (p_table_l.search(content)).group(1)
                        
            p_joblvl_l  = re.compile(r'<th >job level</th>(.*?)</td>',re.DOTALL)
            p_joblvl_r  = re.compile(r'>(.*)',re.DOTALL)
            
            parse_res = p_joblvl_l.search(table_content)
            if parse_res!= None:
                item['JobLvl'] = (p_joblvl_r.search(parse_res.group(1))).group(1)
            else:
                item['JobLvl'] = ''
            
            p_wrkexper_l = re.compile(r'<th >yr\(s\) of exp</th>(.*?)</td>',re.DOTALL)
            p_wrkexper_r = re.compile(r'>(.*)',re.DOTALL)
            
            parse_res = p_wrkexper_l.search(table_content)
            if parse_res!= None:
                item['WorkExperience'] = (p_wrkexper_r.search(parse_res.group(1))).group(1)
            else:
                item['WorkExperience'] = ''
            
            p_qualification_l = re.compile(r'<th >qualification</th>(.*?)</td>',re.DOTALL)
            p_qualification_r = re.compile(r'>(.*)',re.DOTALL)
            
            parse_res = p_qualification_l.search(table_content)
            if parse_res!= None:
                item['Qualification'] = (p_qualification_r.search(parse_res.group(1))).group(1)
            else:
                item['Qualification'] = ''
            
            p_industry_l = re.compile(r'<th >industry</th>(.*?)</td>',re.DOTALL)
            p_industry_r = re.compile(r'>(.*)',re.DOTALL)
            
            parse_res = p_industry_l.search(table_content)
            if parse_res!= None:
                item['Industry'] = (p_industry_r.search(parse_res.group(1))).group(1)
            else:
                item['Industry'] = ''
            
            p_function_l = re.compile(r'<th>job function</th>(.*?)</td>',re.DOTALL)
            p_function_r = re.compile(r'>(.*)',re.DOTALL)
            
            parse_res = p_function_l.search(table_content)
            if parse_res!= None:
                item['Function'] = (p_function_r.search(parse_res.group(1))).group(1)
            else:
                item['Function'] = ''
            
            p_language_l  = re.compile(r'<th>Language</th>(.*?)</td>',re.DOTALL)
            p_language_r  = re.compile(r'>(.*)',re.DOTALL)
            
            parse_res = p_language_l.search(table_content)
            if parse_res!= None:
                item['Language'] = (p_language_r.search(parse_res.group(1))).group(1)
            else:
                item['Language'] = ''
            
            p_location_l = re.compile(r'<th>location</th>(.*?)</td>',re.DOTALL)
            p_location_r = re.compile(r'>(.*)',re.DOTALL)
            
            parse_res = p_location_l.search(table_content)
            if parse_res!= None:
                item['Location'] = (p_location_r.search(parse_res.group(1))).group(1)
            else:
                item['Location'] = ''
            
            p_salary_l = re.compile(r'<th >salary</th>(.*?)</td>',re.DOTALL)
            p_salary_r = re.compile(r'>(.*)',re.DOTALL)
            
            parse_res = p_salary_l.search(table_content)
            if parse_res!= None:
                item['Salary'] = (p_salary_r.search(parse_res.group(1))).group(1)
            else:
                item['Salary'] = ''
            
            p_type_l = re.compile(r'<th>employment type</th>(.*?)</td>',re.DOTALL)
            p_type_r = re.compile(r'>(.*)', re.DOTALL)
            
            parse_res = p_type_l.search(table_content)
            if parse_res!= None:
                item['Type'] = (p_type_r.search(parse_res.group(1))).group(1)
            else:
                item['Type'] = ''
            
            p_benefit_l = re.compile(r'<th>Benefits</th>(.*?)</td>',re.DOTALL)
            p_benefit_r = re.compile(r'>(.*)', re.DOTALL)
            
            parse_res = p_benefit_l.search(table_content)
            if parse_res!= None:
                item['Benefits'] = (p_benefit_r.search(parse_res.group(1))).group(1)
            else:
                item['Benefits'] = ''
                            
            item['Links'] = response.url
            
            yield item
        else:
            if whole_content_expired == None:
                with open('error_link.txt','a+') as errorlink:
                    errorlink.write(response.url)
                    errorlink.write('\n')
 