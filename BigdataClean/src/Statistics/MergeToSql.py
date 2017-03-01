import MySQLdb
import re

industry_list = []
salary_list = []
#industry_list.append('ACCOUNTING')
with open("salary-industry-templet.txt","rb") as openfile:
    for line in openfile:
        industry_list.append((line.split('|')[0]).strip())
        salary_list.append((line.split('|')[1]).strip())
    
# Fetch all the data from BigDataJob 
dbjobsdb = MySQLdb.connect(user='root', 
                    passwd='1234',
                    host='localhost',
                    db='jobsdb')
curjobsdb = dbjobsdb.cursor()

# Insert the parsed data into job schema
dbjob = MySQLdb.connect(user='root', 
                    passwd='1234',
                    host='localhost',
                    db='bigdatajob')
curjob = dbjob.cursor()

# where industry = 'TRADING'

curjobsdb.execute("SELECT * FROM bigdatajob.position  \
     order by position asc, company ")

SameFlag = False
id_pre     = ""
source_pre     = ""
position_pre     = ""
company_pre     = ""
location_pre     = ""
postdate_pre     = ""
carlvl_pre     = ""
wrkexperience_pre     = ""
education_pre     = ""
industry_pre     = ""
function_pre     = ""
salary_pre     = ""
type_pre     = ""
duty_pre     = ""
language_pre     = ""
benefits_pre     = ""
slist_pre     = ""

for row in curjobsdb.fetchall():
    id_tmp = row[0]
    source_tmp = row[1].strip()
    position_tmp = row[2].strip()
    company_tmp = row[3].strip()
    location_tmp = row[4].strip()
    postdate_tmp = row[5]
    carlvl_tmp = row[6].strip()
    wrkexperience_tmp = row[7].strip()
    education_tmp = row[8].strip()
    industry_tmp = row[9].strip()
    function_tmp = row[10].strip()
    salary_tmp = row[11].strip()
    type_tmp = row[12].strip()
    duty_tmp = row[13].strip()
    language_tmp = row[14]
    benefits_tmp = row[15]
    slist_tmp = source_tmp + " | " + str(id_tmp)
    
    print position_tmp
    
    if position_tmp.strip() == position_pre.strip() and company_tmp.strip() == company_pre.strip():
        if location_tmp != "OTHERS":
            location_pre     =    location_tmp 
        if postdate_tmp > postdate_pre:
            postdate_pre     =    postdate_tmp 
        if carlvl_tmp != "NA":
            carlvl_pre     =    carlvl_tmp 
        if wrkexperience_tmp != "NA":
            wrkexperience_pre     =    wrkexperience_tmp 
        if education_tmp != "NA":
            education_pre     =    education_tmp 
        industry_pre     =    industry_tmp 
        function_pre     =    function_tmp 
        if salary_tmp != "0 | 0":
            salary_pre     =    salary_tmp 
        if type_tmp != "":
            type_pre     =    type_tmp 
        duty_pre     =    duty_tmp 
        if language_tmp != "":
            language_pre     =    language_tmp
        if benefits_tmp != "": 
            benefits_pre     =    benefits_tmp 
        slist_pre     =   slist_pre + " | " + slist_tmp 
    else:
        # write to the database
        # Filter out the first time
        if postdate_pre != "":
            # Data Fusion:
            #
            # Salary
            if salary_pre.strip() == "0 | 0":
                # find the industry
                Find_flag = False
                for salary_index in range(0,len(industry_list),1):
                    if industry_pre.strip() in industry_list[salary_index]:
                        salary_pre = salary_list[salary_index]
                        Find_flag = True
                        break
                if Find_flag == False:
                    salary_pre = 16.88233973

            curjob.execute("INSERT INTO position \
            (Source, Position, Company, \
            Location, Postdate, CareerLvl, \
            WrkExperience, Education, Industry, \
            Function, Salary, Type, \
            Duty, Language, Benefits, \
            SList) VALUES \
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
            ('9',position_pre,company_pre,
            location_pre,postdate_pre,carlvl_pre,
            wrkexperience_pre,education_pre,industry_pre,
            function_pre,salary_pre,type_pre,duty_pre,
            language_pre,benefits_pre,slist_pre[0:101]))
            dbjob.commit()
        # save the data to the pre
        position_pre     =    position_tmp 
        company_pre     =    company_tmp 
        location_pre     =    location_tmp 
        postdate_pre     =    postdate_tmp 
        carlvl_pre     =    carlvl_tmp 
        wrkexperience_pre     =    wrkexperience_tmp 
        education_pre     =    education_tmp 
        industry_pre     =    industry_tmp 
        function_pre     =    function_tmp 
        salary_pre     =    salary_tmp 
        type_pre     =    type_tmp 
        duty_pre     =    duty_tmp 
        language_pre     =    language_tmp 
        benefits_pre     =    benefits_tmp 
        slist_pre     =   slist_tmp
        
    
        
dbjobsdb.close()
dbjob.close()