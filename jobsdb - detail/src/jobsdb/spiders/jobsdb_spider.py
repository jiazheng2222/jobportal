# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import re
import MySQLdb

from jobsdb.items import JobsdbItem
from _cffi_backend import callback
from twisted.spread.pb import respond
from scrapy.http import Request
from scrapy.utils.project import get_project_settings

class DmozSpider(scrapy.Spider):
    name = "jobsdb"
    allowed_domains = ["hk.jobsdb.com"]
    
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
        #cursor.execute('SELECT links FROM jobsdb.position where id=108504 ')
        cursor.execute('SELECT links FROM jobsdb.position where id between "156833" and "160000" ')
        
        rows = cursor.fetchall()
        for row in rows:
            yield self.make_requests_from_url(row[0])
        conn.close()

    def parse(self, response):
        content = response.body
        self.logger.info('Top Link - Parse function called on %s', response.url)
                           
        # get the whole content, including responsibility
        # The Temple 1:
        #     Using job-ad-contents to recognize
        p_whole_content_l = re.compile(r'class=\"job-ad-contents\"(.*)job-ad-data jobSumWrap', re.DOTALL)
        whole_content_l = p_whole_content_l.search(content)
        # The Temple 2:
        #     Using jobad-primary to recognize
        p_whole_content_tmp2 = re.compile(r'class=\"jobad-primary\">(.*)class=\"jobad-secondary\">', re.DOTALL)
        whole_content_tmp2 = p_whole_content_tmp2.search(content)
        # The Temple 3:
        #    Expired data
        p_whole_content_expired = re.compile(r'id=\"ExpiredMessagePlaceHolder\"',re.DOTALL)
        whole_content_expired = p_whole_content_expired.search(content)
        
        # The Temple 1:
        if whole_content_l != None:
            item = JobsdbItem()
            tmp = re.sub('<.*?>', '', whole_content_l.group(1))
            item['Content'] = tmp
            
            p_company_l = re.compile(r'job-ad-client-name coName\">(.*?)</',re.DOTALL)
            p_company_r = re.compile(r'>(.*)')
            company_l = p_company_l.search(content)
            company_r = p_company_r.search(company_l.group(1))
            item['Company']= company_r.group(1)
            
            # parse the content                        
            p_pstdate_l = re.compile(r'Post Date(.*?)</b>')
            p_pstdate_r = re.compile(r'->(.*)')
            p_employref_l = re.compile(r'Employer Ref(.*?)</b>')
            p_employref_r = re.compile(r'<b>(.*)')
            p_posiref_l = re.compile(r'jobsDB Ref(.*?)</b>')
            p_posiref_r = re.compile(r'<b>(.*)')
            p_title_l = re.compile(r'itemprop\=\"title\"(.*?)\<\/h1\>')
            p_title_r = re.compile(r'>(.*)')
            # Parse the whole table
            p_table      = re.compile(r'job-ad-data-table jobSum(.*)</table>',re.DOTALL)
            p_careerlvl  = re.compile(r'Career Level</th><td>(.*?)</td>')
            p_wrkexper_l = re.compile(r'Exp</th><td(.*?)</td>')
            p_wrkexper_r = re.compile(r'>(.*)')
            p_qualify_l  = re.compile(r'Qualification</th><td(.*?)</td>')
            p_qualify_r  = re.compile(r'>(.*)')
            
            p_industry_l = re.compile(r'Industry</th><td(.*?)</td>')
            p_industry_r = re.compile(r'BI">(.*?)</a>')
            
            p_function_l = re.compile(r'Job Function</th><td(.*?)</td>')
            p_function_r = re.compile(r'BF">(.*?)</a>')
            
            p_location_l = re.compile(r'jobLocation(.*?)</span>')
            p_location_r_y = re.compile(r'BL">(.*)</a>')
            p_location_r_n = re.compile(r'">(.*)')
            
            p_salary_l = re.compile(r'baseSalary">(.*?)</td>')
            p_salary_r = re.compile(r'">(.*)<ins')
            
            p_type_l = re.compile(r'employmentType(.*?)</td>')
            p_type_r = re.compile(r'">(.*)')
    
            table = (p_table.search(content)).group(1)
            pstdate_l = (p_pstdate_l.search(content)).group(1)
            item['PostDate'] = (p_pstdate_r.search(pstdate_l)).group(1)        
            
            # E.g. Employer Ref. stu052015
            parse_res = p_employref_l.search(content)
            if parse_res!= None:
                employref_l = (p_employref_l.search(content)).group(1)
                item['EmployID'] = (p_employref_r.search(employref_l)).group(1)
            else:
                item['EmployID'] = ''
            
            # E.g. jobsDB Ref. JHK100003004274837
            posiref_l = (p_posiref_l.search(content)).group(1)
            item['PositionID'] = (p_posiref_r.search(posiref_l)).group(1)
            
            # E.g. ACCOUNT MANAGERS
            title_l = (p_title_l.search(content)).group(1)
            item['Position'] = (p_title_r.search(title_l)).group(1)
            
            # E.g. Senior
            parse_res = p_careerlvl.search(table)
            if parse_res!= None:
                item['CareerLvl'] = (p_careerlvl.search(table)).group(1)
            else:
                item['CareerLvl'] = ''
                
            # E.g. 5 years
            parse_res = p_wrkexper_l.search(table)
            if parse_res != None:
                wrkexper_l = (p_wrkexper_l.search(table)).group(1)
                item['WorkExperience'] = (p_wrkexper_r.search(wrkexper_l)).group(1)
            else:
                item['WorkExperience'] = ''
                
            # E.g. Degree
            parse_res = p_qualify_l.search(table)
            if parse_res!=None:
                qualify_l = (p_qualify_l.search(table)).group(1)
                item['Qualification'] = (p_qualify_r.search(qualify_l)).group(1)
            else:
                item['Qualification'] = ''
                
            # E.g. Advertising / Public Relations / Marketing Services
            # Still need to parse
            industry_l = (p_industry_l.search(table)).group(1)
            item['Industry'] = (p_industry_r.search(industry_l)).group(1)
            
            # E.g. Marketing - Brand &#47; Product Management
            # Still need to parse
            function_l = (p_function_l.search(table)).group(1)
            item['Function'] = (p_function_r.search(function_l)).group(1)
            
            # E.g. Quarry Bay
            parse_res = p_location_l.search(table)
            if parse_res != None:
                location_l = (p_location_l.search(table)).group(1)
                if p_location_r_y.search(location_l) != None:
                    item['Location'] = (p_location_r_y.search(location_l)).group(1)
                else:
                    item['Location'] = (p_location_r_n.search(location_l)).group(1)
            else:
                item['Location'] = ''
                
            # E.g. Salary negotiable
            # Parse from the content
            parse_res = p_salary_l.search(table)
            if parse_res != None:
                salary_l = (p_salary_l.search(table)).group(1)
                item['Salary'] = (p_salary_r.search(salary_l)).group(1)
            else:
                item['Salary'] = ''
            
            parse_res = p_type_l.search(table)
            if parse_res != None:
                type_l = (p_type_l.search(table)).group(1)
                item['Type'] = (p_type_r.search(type_l)).group(1)
            else:
                item['Type'] = ''
                
            item['Links'] = response.url
            
            yield item
            
        # The Temple 2:
        #     Using jobad-primary to recognize
        elif whole_content_tmp2 != None:
            item = JobsdbItem()
            p_content_l = re.compile(r'class=\"jobad-primary-details(.*)', re.DOTALL)
            content_l = p_content_l.search(whole_content_tmp2.group(1))
            tmp = re.sub('<.*?>', '', content_l.group(1))
            item['Content'] = tmp
            
            p_company_l = re.compile(r'jobad-header-company ad-y-auto-txt1(.*?)</h2>',re.DOTALL)
            p_company_r = re.compile(r'>(.*)')
            company_l = p_company_l.search(content)
            company_r = p_company_r.search(company_l.group(1))
            item['Company']= company_r.group(1)
            
            # parse the content
            p_pstdate_l = re.compile(r'class=\"data-timestamp\"(.*?)</p>')
            p_pstdate_r = re.compile(r'->(.*)')
            pstdate_l = (p_pstdate_l.search(content)).group(1)
            item['PostDate'] = (p_pstdate_r.search(pstdate_l)).group(1)
            
            p_title_l = re.compile(r'class=\"general-pos ad-y-auto-txt2\"(.*?)</h1>')
            p_title_r = re.compile(r'>(.*)')
            # E.g. ACCOUNT MANAGERS
            title_l = (p_title_l.search(content)).group(1)
            item['Position'] = (p_title_r.search(title_l)).group(1)
            
            p_location_l = re.compile(r'class=\"loc-link\"(.*?)</a>')
            p_location_r = re.compile(r'>(.*)')
            location_l = (p_location_l.search(content)).group(1)
            item['Location'] = (p_location_r.search(location_l)).group(1)
                
            p_industry_l = re.compile(r'class=\"meta-industry-link\">(.*?)</a>')
            p_industry_r = re.compile(r'>(.*)')
            industry_l = (p_industry_l.search(content)).group(1)
            item['Industry'] = (p_industry_r.search(industry_l)).group(1)        
            
            # Parse the whole table
            #p_table = re.compile(r'class=\"primary-meta\">(.*?)class=\"jobad-primary-details\"',re.DOTALL)
            
            p_salary_l = re.compile(r'id=\"salaryTooltip\"(.*?)<ins')
            p_salary_r = re.compile(r'>(.*)')
            parse_res = p_salary_l.search(content)
            if parse_res != None:
                salary_l = (p_salary_l.search(content)).group(1)
                item['Salary'] = (p_salary_r.search(salary_l)).group(1)
            else:
                item['Salary'] = ''
                
            p_type_l = re.compile(r'itemprop=\"employmentType\"(.*?)</span>')
            p_type_r = re.compile(r'>(.*)')
            parse_res = p_type_l.search(content)
            if parse_res != None:
                type_l = (p_type_l.search(content)).group(1)
                item['Type'] = (p_type_r.search(type_l)).group(1)
            else:
                item['Type'] = ''
            
            p_careerlvl  = re.compile(r' class=\"primary-meta-lv\">(.*?)</b>')
            parse_res = p_careerlvl.search(content)
            if parse_res!= None:
                item['CareerLvl'] = (p_careerlvl.search(content)).group(1)
            else:
                item['CareerLvl'] = ''
                
            p_posiref_l = re.compile(r'class="primary-meta-item primary-meta-jdbref\">(.*?)</span>')
            p_posiref_r = re.compile(r'<b>(.*)')
            # E.g. jobsDB Ref. JHK100003004274837
            posiref_l = (p_posiref_l.search(content)).group(1)
            item['PositionID'] = (p_posiref_r.search(posiref_l)).group(1)
            
            p_function = re.compile(r'class=\"meta-jfunc-entry\"(.*?)</p>')
            # E.g. Marketing - Brand &#47; Product Management
            # Still need to parse
            function = (p_function.search(content)).group(1)
            item['Function'] = re.sub('<.*?>', '',function)                              
                            
            item['Links'] = response.url
            
            # Null element
            item['EmployID'] = ""
            item['WorkExperience'] = ""
            item['Qualification']= ""
            
            yield item            
        else:
            if whole_content_expired == None:
                with open('error_link.txt','a+') as errorlink:
                    errorlink.write(response.url)
                    errorlink.write('\n')
            
                       