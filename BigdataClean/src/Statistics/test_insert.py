import re

industry_list = []
salary_list = []
#industry_list.append('ACCOUNTING')
with open("salary-industry-templet.txt","rb") as openfile:
    for line in openfile:
        industry_list.append((line.split('|')[0]).strip())
        salary_list.append((line.split('|')[1]).strip())
        
# find the industry
industry_pre = "TRADING"
for salary_index in range(0,len(industry_list),1):
    if industry_pre.strip() in industry_list[salary_index]:
        print salary_list[salary_index]
        break
