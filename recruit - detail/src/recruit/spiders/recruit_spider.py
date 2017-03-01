# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import re
import MySQLdb

from recruit.items import recruitItem
from _cffi_backend import callback
from twisted.spread.pb import respond
from scrapy.http import Request
from scrapy import FormRequest
from scrapy.utils.project import get_project_settings

class DmozSpider(scrapy.Spider):
    name = "recruit"
    allowed_domains = ["recruit.com.hk"]
    
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
        
        cursor.execute('SELECT joborder, position FROM recruit.position where id between "34001" and "35000" ')
        #cursor.execute('SELECT joborder, position FROM recruit.position where id = "33812" ')
        
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
        #     Using jobDetail_job_detail_div to recognize
        p_whole_content_l = re.compile(r'id=\"jobDetail_job_detail_div\"(.*)id=\"job_summary\"', re.DOTALL)
        whole_content_l = p_whole_content_l.search(content)
        # The Temple 2: (No use now)
        #    Expired data
        p_whole_content_expired = re.compile(r'id=\"ExpiredMessagePlaceHolder\"',re.DOTALL)
        whole_content_expired = p_whole_content_expired.search(content)
        
        # The Temple 1:
        if whole_content_l != None:
            item = recruitItem()
            tmp = re.sub('<.*?>', '', whole_content_l.group(1))
            item['Content'] = tmp
            
            p_company_l = re.compile(r'id=\"jobDetail_companyNameLabel\"(.*?)</',re.DOTALL)
            p_company_r = re.compile(r'>(.*)')
            company_l = p_company_l.search(content)
            company_r = p_company_r.search(company_l.group(1))
            item['Company']= company_r.group(1)
            
            # parse the content                        
            p_pstdate_l = re.compile(r'id=\"jobDetail_postDateLabel\"(.*?)</')
            p_pstdate_r = re.compile(r'>(.*)')

            p_posiref_l = re.compile(r'id=\"jobDetail_jobOrderLabel\"(.*?)</')
            p_posiref_r = re.compile(r'>(.*)')
            
            p_title_l = re.compile(r'id=\"jobDetail_jobTitleLab\"(.*?)</')
            p_title_r = re.compile(r'>(.*)')
            
            p_industry_l = re.compile(r'id=\"jobDetail_jobIndustryLabel\"(.*?)</')
            p_industry_r = re.compile(r'>(.*)')
            
            # I just pick up the first function
            p_function_l = re.compile(r'id=\"jobDetail_jobCatFunc1Link\"(.*?)</')
            p_function_r = re.compile(r'>(.*)')
            
            p_joblvl  = re.compile(r'id=\"jobDetail_jobPosLvlLabel\">(.*?)</')
            
            p_mincareerlvl  = re.compile(r'id=\"jobDetail_eduLevelLabel\">(.*?)</')
            
            p_wrkexper_l = re.compile(r'id="jobDetail_workExpLabel"(.*?)</')
            p_wrkexper_r = re.compile(r'>(.*)')
            
            p_salary_l = re.compile(r'id=\"jobDetail_salaryLabel\">(.*?)</')
            p_salary_r = re.compile(r'id=\"jobDetail_salaryUnitLab\">(.*?)</')
            
            p_location_l = re.compile(r'id=\"jobDetail_locationLabel\"(.*?)</')
            p_location_r = re.compile(r'\'>(.*)')
            
            p_benefits_l = re.compile(r'id=\"jobDetail_BenefitsPanel\"(.*?)</ul>',re.DOTALL)
            p_benefits_r = re.compile(r'class=\"jobad_summText\">(.*)', re.DOTALL)
            # add a remove
            
            pstdate_l = (p_pstdate_l.search(content)).group(1)
            item['PostDate'] = (p_pstdate_r.search(pstdate_l)).group(1)        
            
            # E.g. jobsDB Ref. JHK100003004274837
            posiref_l = (p_posiref_l.search(content)).group(1)
            item['PositionID'] = (p_posiref_r.search(posiref_l)).group(1)
            
            # E.g. ACCOUNT MANAGERS
            title_l = (p_title_l.search(content)).group(1)
            item['Position'] = (p_title_r.search(title_l)).group(1)
            
            # E.g. Advertising / Public Relations / Marketing Services
            industry_l = (p_industry_l.search(content)).group(1)
            item['Industry'] = (p_industry_r.search(industry_l)).group(1)
            
            # E.g. Marketing - Brand &#47; Product Management
            function_l = (p_function_l.search(content)).group(1)
            item['Function'] = (p_function_r.search(function_l)).group(1)
            
            parse_res = p_joblvl.search(content)
            if parse_res!= None:
                item['JobLvl'] = parse_res.group(1)
            else:
                item['JobLvl'] = ''
             
            parse_res = p_mincareerlvl.search(content)
            if parse_res!= None:
                item['MinCareerLvl'] = parse_res.group(1)
            else:
                item['MinCareerLvl'] = ''
                
            wrkexper_l = (p_wrkexper_l.search(content)).group(1)
            item['WorkExperience'] = (p_wrkexper_r.search(wrkexper_l)).group(1)
                
            salary_l_c1 = ""
            salary_l_c2 = ""
            parse_res = p_salary_r.search(content)
            if parse_res != None:
                salary_l_c1 = (p_salary_l.search(content)).group(1)
                salary_l_c2 = (p_salary_r.search(content)).group(1)
                item['Salary'] = salary_l_c1 +' | '+ salary_l_c2
            else:
                item['Salary'] = "--"
                
            # E.g. Quarry Bay
            parse_res = p_location_l.search(content)
            if parse_res != None:
                location_l = (p_location_l.search(content)).group(1)
                item['Location'] = (p_location_r.search(location_l)).group(1)
            else:
                item['Location'] = ''  
                
            parse_res = p_benefits_l.search(content)
            if parse_res!=None:
                benefits_l = (p_benefits_l.search(content)).group(1)
                benefits_r = (p_benefits_r.search(benefits_l)).group(1)
                benefits_p1 = re.sub('<.*?>', '',benefits_r)
                item['Benefits'] = re.sub('[\\r\\n]', '',benefits_p1)
            else:
                item['Benefits'] = ''
                
            item['Links'] = response.url
            
            yield item
        else:
            if whole_content_expired == None:
                with open('error_link.txt','a+') as errorlink:
                    errorlink.write(response.url)
                    errorlink.write('\n')
 