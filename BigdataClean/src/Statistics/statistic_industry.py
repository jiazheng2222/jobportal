import MySQLdb
import re

industry_list = []
#industry_list.append('ACCOUNTING')
with open("Industry.txt","rb") as openfile:
    for line in openfile:
        industry_list.append(line.split('/')[0])
        
# Fetch all the data from BigDataJob 
dbposition = MySQLdb.connect(user='root', 
                    passwd='1234',
                    host='localhost',
                    db='bigdatajob')
curposition = dbposition.cursor()

for industry_li in industry_list:
    curposition.execute("SELECT * FROM position where  \
        industry = '"+industry_li+"' order by postdate ")
    
    cmp_list1 = curposition.fetchall()
    with open("salary.txt","a+") as file:
                
        count_salary = 0
        sum_salary = 0.0
        for li in cmp_list1:
            pre_salary = float(re.split(r"\|", li[11])[0])
            later_salary = float(re.split(r"\|", li[11])[1])
            if later_salary > 0.0001 and later_salary < 200.0000:
                count_salary = count_salary + 1
                average_salary = (pre_salary + later_salary)/2
                sum_salary = sum_salary + average_salary
        if count_salary > 0:
            file.write(industry_li)
            file.write(" " + str(sum_salary / count_salary)+ "\n")
            #print industry_li
            #print sum_salary / count_salary
        
    
dbposition.close()