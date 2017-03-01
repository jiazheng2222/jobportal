import MySQLdb
import re

location_list = []
#industry_list.append('ACCOUNTING')
with open("Location.txt","rb") as openfile:
    for line in openfile:
        location_list.append(line.split('/')[0])
        
# Fetch all the data from BigDataJob 
dbposition = MySQLdb.connect(user='root', 
                    passwd='1234',
                    host='localhost',
                    db='bigdatajob')
curposition = dbposition.cursor()

for location_li in location_list:
    curposition.execute("SELECT * FROM position where  \
        location = '"+location_li.strip()+"' order by postdate ")

    
    cmp_list1 = curposition.fetchall()
    with open("salary_location.txt","a+") as file:
                
        count_salary = 0
        sum_salary = 0.0
        for li in cmp_list1:
            pre_salary = float(re.split(r"\|", li[11])[0])
            later_salary = float(re.split(r"\|", li[11])[1])
            if later_salary > 0.0001 and later_salary < 200.0000:
                count_salary = count_salary + 1
                average_salary = (pre_salary + later_salary)/2
                sum_salary = sum_salary + average_salary
            elif later_salary >= 200.000:
                print later_salary
        if count_salary > 0:
            file.write("['"+ location_li.strip() +"', "+str(sum_salary / count_salary) +","+  str(sum_salary / count_salary) +"],")
            file.write("\n")
            #print location_li
            #print sum_salary / count_salary
        
dbposition.close()