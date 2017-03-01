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
from scrapy import FormRequest

class DmozSpider(scrapy.Spider):
    name = "recruit"
    #allowed_domains = ["recruit.com.hk"]
    allowed_domains = ["recruit.com.hk"]
    
    page_location = 0
    event_value_index = 1 
    
    start_urls = []
    with open('links.txt','rb') as openfile:
        for line in openfile:
            temple = line.rstrip()
            start_urls.append(temple)                
    
    def parse(self,response):
        content = response.body
        self.logger.info('Top Link: %s', response.url)
        
        #p_file_name = re.compile(r'industry=(.*)')
        #file_name = (p_file_name.search(response.url)).group(1) + ".html"
        #with open(file_name,'wb') as f:
        #    f.write(content)
        
        p_number_position = re.compile(r'jobCountLab\">(.*?)</span>')
        number_position_tmp = p_number_position.search(content)
        if number_position_tmp != None:
            number_position = (number_position_tmp.group(1)).replace(",","")
        else:
            number_position = 0
                
        p_content_table = re.compile(r'jobs-table(.*?)</table>',re.DOTALL)
        p_content_tbody = re.compile(r'</thead>(.*)',re.DOTALL)
        content_table = p_content_table.search(content)
        content_tbody = p_content_tbody.search(content_table.group(1))
        
        # For id="__EVENTVALIDATION" and id="__VIEWSTATE"
        p_viewstate_l = re.compile(r'id=\"__VIEWSTATE\"(.*?)</div>',re.DOTALL)
        p_viewstate_r = re.compile(r'value=\"(.*?)\"',re.DOTALL)
        p_eventvalidation_l = re.compile(r'id=\"__EVENTVALIDATION\"(.*?)</div>',re.DOTALL)
        p_eventvalidation_r = re.compile(r'value=\"(.*?)\"',re.DOTALL)
        viewstate_l = p_viewstate_l.search(content)
        viewstate = (p_viewstate_r.search(viewstate_l.group(1))).group(1)
        eventvalidation_l = p_eventvalidation_l.search(content)
        eventvalidation = (p_eventvalidation_r.search(eventvalidation_l.group(1))).group(1)
        
        p_tr_list = re.compile(r'<tr(.*?)</tr>',re.DOTALL)
        p_td_title_col = re.compile(r'title-company-col(.*)</a>',re.DOTALL)
        # title & company exist in title_col & link
        p_td_joborder = re.compile(r'href=\"(.*?)\"', re.DOTALL)
        p_td_title_l = re.compile(r'title(.*?)</a>',re.DOTALL)
        p_td_title_r = re.compile(r'\">(.*)',re.DOTALL)
        p_td_company = re.compile(r'\"company\">(.*)',re.DOTALL)
        p_td_edu_col = re.compile(r'edu-col\">(.*?)</td>',re.DOTALL)
        p_td_salary_col = re.compile(r'salary-col\">(.*?)</td>',re.DOTALL)
        p_td_exp_col = re.compile(r'exp-col\">(.*?)</td>',re.DOTALL)
        p_td_post_col = re.compile(r'post-date-col\">(.*?)</td>',re.DOTALL)
        
        
        #with open('content_table.txt','wb') as f:
        tr_list = p_tr_list.findall(content_tbody.group(1))
        for li in tr_list:
            td_title_col = p_td_title_col.search(li)
            if td_title_col != None:
                #f.write(li)
                td_joborder = p_td_joborder.search(td_title_col.group(1))
                td_title_l = p_td_title_l.search(td_title_col.group(1))
                td_title = p_td_title_r.search(td_title_l.group(1))
                td_company = p_td_company.search(td_title_col.group(1))
                
                item = recruitItem()
                item['Joborder'] = "http://recruit.com.hk"+str(td_joborder.group(1))
                item['Position'] = td_title.group(1)
                item['Company'] = td_company.group(1)
                td_edu_col = p_td_edu_col.search(li)
                item['Education']  = td_edu_col.group(1)
                td_salary_col = p_td_salary_col.search(li)
                item['Salary'] = td_salary_col.group(1)
                td_exp_col = p_td_exp_col.search(li)
                item['Experience'] = td_exp_col.group(1)
                td_post_col = p_td_post_col.search(li)
                item['Postdate'] = td_post_col.group(1)
                print item['Joborder']
                
                yield item

        postdata = {
        '__EVENTARGUMENT':'',
'__EVENTTARGET':'pagerBottom$ctl01$ctl01',
'__VIEWSTATE':viewstate,
'__EVENTVALIDATION':eventvalidation,
'__LASTFOCUS':'',
'agencyFilterTxt':'N',
'filterTypeTxt':'N',
'isAdvanceSearchTxt':'N',
'isEmployerSearchTxt':'N',
'itemCnt':'25',
'pageJobCnt':'',
'pageTxt':'',
'recruitHeader$ActivityShortcutBar1$siteTypeHidden':'',
'recruitJobSearch$careerLvlSearchHidden':'',
'recruitJobSearch$eduLvlSearchHidden':'',
'recruitJobSearch$empTermSearchHidden':'',
'recruitJobSearch$jobCatSearchHidden':'',
'recruitJobSearch$jobFuncSearchHidden':'',
'recruitJobSearch$keywordSearchTypeSearchHidden':'B',
'recruitJobSearch$keywordTxt':'',
'recruitJobSearch$lastKeyword':'',
'recruitJobSearch$locationSearchHidden':'',
'recruitJobSearch$salarySearchHidden':'',
'recruitJobSearch$salaryTypeSearchHidden':'M',
'recruitJobSearch$searchPath':'I',
'recruitJobSearch$yearExpSearchHidden':'',
'searchBy':'B',
'searchPath':'I',
'selectedJobOrder':'',
'sortByDDL':'POST_DATE',
'sortDirection':'DESC',
'sortExpression':'POST_DATE',
'sortFieldTxt':'',
'startIndex':'0',
'totalCnt':'2098'
        }
        
        if int(number_position) > 0:
            yield FormRequest(url=response.url,method='POST',formdata=postdata,callback=self.after_load)
        #yield FormRequest.from_response(response,formdata=postdata,callback=self.after_load,dont_click = True,dont_filter=True)

    def after_load(self,response):
        content = response.body
        self.logger.info('Lower Link %s', response.url)
                
        # parse the link
        file_name = str(self.page_location) + '.html'
        self.page_location = self.page_location + 1
        #print self.page_location,'\n\n'
        
        #with open(file_name,'wb') as f:
        #    f.write(content)
        
        p_content_table = re.compile(r'jobs-table(.*?)</table>',re.DOTALL)
        p_content_tbody = re.compile(r'</thead>(.*)',re.DOTALL)
        content_table = p_content_table.search(content)
        
        if content_table == None:
            return
        
        content_tbody = p_content_tbody.search(content_table.group(1))
        
        if content_tbody == None:
            return
        
        # For id="__EVENTVALIDATION" and id="__VIEWSTATE"
        p_viewstate_l = re.compile(r'id=\"__VIEWSTATE\"(.*?)</div>',re.DOTALL)
        p_viewstate_r = re.compile(r'value=\"(.*?)\"',re.DOTALL)
        p_eventvalidation_l = re.compile(r'id=\"__EVENTVALIDATION\"(.*?)</div>',re.DOTALL)
        p_eventvalidation_r = re.compile(r'value=\"(.*?)\"',re.DOTALL)
        viewstate_l = p_viewstate_l.search(content)
                
        viewstate = (p_viewstate_r.search(viewstate_l.group(1))).group(1)
        eventvalidation_l = p_eventvalidation_l.search(content)
        eventvalidation = (p_eventvalidation_r.search(eventvalidation_l.group(1))).group(1)
    
        p_tr_list = re.compile(r'<tr(.*?)</tr>',re.DOTALL)
        #p_tr_break = re.compile(r'job-list-adv(.*)')
        p_td_title_col = re.compile(r'title-company-col(.*)</a>',re.DOTALL)
        # title & company exist in title_col
        p_td_title_l = re.compile(r'title(.*?)</a>',re.DOTALL)
        p_td_title_r = re.compile(r'\">(.*)',re.DOTALL)
        p_td_joborder = re.compile(r'href=\"(.*?)\"', re.DOTALL)
        p_td_company = re.compile(r'\"company\">(.*)',re.DOTALL)
        p_td_edu_col = re.compile(r'edu-col\">(.*?)</td>',re.DOTALL)
        p_td_salary_col = re.compile(r'salary-col\">(.*?)</td>',re.DOTALL)
        p_td_exp_col = re.compile(r'exp-col\">(.*?)</td>',re.DOTALL)
        p_td_post_col = re.compile(r'post-date-col\">(.*?)</td>',re.DOTALL)
        
        #with open('content_table.txt','wb') as f:
        tr_list = p_tr_list.findall(content_tbody.group(1))
        for li in tr_list:
            td_title_col = p_td_title_col.search(li)
            if td_title_col != None:
                #f.write(li)
                td_joborder = p_td_joborder.search(td_title_col.group(1))
                td_title_l = p_td_title_l.search(td_title_col.group(1))
                td_title = p_td_title_r.search(td_title_l.group(1))
                td_company = p_td_company.search(td_title_col.group(1))
                
                item = recruitItem()
                item['Joborder'] = "http://recruit.com.hk"+str(td_joborder.group(1))
                item['Position'] = td_title.group(1)
                item['Company'] = td_company.group(1)
                td_edu_col = p_td_edu_col.search(li)
                item['Education']  = td_edu_col.group(1)
                td_salary_col = p_td_salary_col.search(li)
                item['Salary'] = td_salary_col.group(1)
                td_exp_col = p_td_exp_col.search(li)
                item['Experience'] = td_exp_col.group(1)
                td_post_col = p_td_post_col.search(li)
                item['Postdate'] = td_post_col.group(1)
                
                yield item
    
        postdata = {
        '__EVENTTARGET':'pagerBottom$ctl02$ctl00',
'__EVENTARGUMENT':'',
'__LASTFOCUS':'',
'__VIEWSTATE':viewstate,
'__EVENTVALIDATION':eventvalidation,
'recruitHeader$ActivityShortcutBar1$siteTypeHidden':'',
'sortByDDL':'POST_DATE',
'searchBy':'B',
'recruitJobSearch$keywordTxt':'',
'recruitJobSearch$keywordSearchTypeSearchHidden':'B',
'recruitJobSearch$jobCatSearchHidden':'',
'recruitJobSearch$jobFuncSearchHidden':'',
'recruitJobSearch$eduLvlSearchHidden':'',
'recruitJobSearch$yearExpSearchHidden':'',
'recruitJobSearch$empTermSearchHidden':'',
'recruitJobSearch$careerLvlSearchHidden':'',
'recruitJobSearch$locationSearchHidden':'',
'recruitJobSearch$salaryTypeSearchHidden':'M',
'recruitJobSearch$salarySearchHidden':'',
'recruitJobSearch$searchPath':'I',
'recruitJobSearch$lastKeyword':'',
'sortExpression':'POST_DATE',
'sortDirection':'DESC',
'sortFieldTxt':'',
'searchPath':'I',
'agencyFilterTxt':'N',
'isAdvanceSearchTxt':'N',
'isEmployerSearchTxt':'N',
'filterTypeTxt':'N',
'selectedJobOrder':'',
'pageTxt':'',
'startIndex':'0',
'itemCnt':'25',
'totalCnt':'209',
'pageJobCnt':''
        
        }
        
        yield FormRequest(url=response.url,method='POST',formdata=postdata,callback=self.after_load,dont_filter=True)
        #yield FormRequest.from_response(response,formdata=postdata,callback=self.after_load,dont_click = True,dont_filter=True)
    