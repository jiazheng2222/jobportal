import MySQLdb
import re
import PositionItem
from ParseSalary import ParseSalary

# Fetch the Location list from "Location.txt"
location_list = []
with open('Location.txt','rb') as openfile:
    for line in openfile:
        location_list.append(line.rstrip())
location_list_matched = []
with open('Location_matched2.txt','rb') as openfile:
    for line in openfile:
        location_list_matched.append(line.strip())

# Fetch the month list from "Month.txt"
month_slist = []
month_nlist = []
with open('Month.txt','rb') as openfile:
        for line in openfile:
            month_slist.append(line.rstrip())
for index in range(1,10,1):
    month_nlist.append('0'+str(index))
month_nlist.append('10')
month_nlist.append('11')
month_nlist.append('12')
            
# Fetch the industry list from "Industry.txt"
# Store it in a union set
industry_list = []
with open('Industry.txt','rb') as openfile:
        for line in openfile:
            industry_list.append(line.rstrip())

# Fetch the function list from "Function.txt"
function_list = []
with open('Function.txt','rb') as openfile:
        for line in openfile:
            function_list.append(line.rstrip())
            
# Fetch the work experience list from "Experience.txt"        
wrkexperience_list = []        
with open('Experience.txt','rb') as openfile:        
    for line in openfile:        
        wrkexperience_list.append(line.strip())        
        
# Fetch the career lvl list from "Level.txt"        
careerlvl_list = []        
with open('Level.txt','rb') as openfile:        
    for line in openfile:        
        careerlvl_list.append(line.strip())        
                
# Fetch the education list from "Education.txt"        
education_list = []        
with open('Education.txt','rb') as openfile:        
    for line in openfile:        
        education_list.append(line.strip())

# Check whether the string contains Chinese characters or not
def chinese_character(inputstring):
    iconvcontent = inputstring
    #zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    zhPattern = re.compile(u'\?')
    match = zhPattern.search(iconvcontent)
    res = False
    if match:
        res = True
    return res

# Convert the time format from 01-Jan-16 to 2016-01-01
def convert_time(postdate):
    datearray = postdate.split('/')
    dateyear = datearray[2]
    datemonth = datearray[1]
    dateday = datearray[0]
    return dateyear+'-'+datemonth+'-'+dateday


# Fetch all the data from jiujik
dbjiujik = MySQLdb.connect(user='root', 
                    passwd='1234',
                    host='localhost',
                    db='jiujik')
curjiujik = dbjiujik.cursor()

# Insert the parsed data into job schema
dbjob = MySQLdb.connect(user='root', 
                    passwd='1234',
                    host='localhost',
                    db='bigdatajob')
curjob = dbjob.cursor()

curjiujik.execute("SELECT * FROM jiujik.positiondetail  ")

for row in curjiujik.fetchall():
    postdate_tmp = row[1].strip()
    position_tmp = row[3].strip()
    company_tmp = row[4].strip()
    industry_tmp = row[5].strip()
    function_tmp = row[6].strip()
    carlvl_tmp = row[7].strip()
    language_tmp = row[8].strip()
    wrkexperience_tmp = row[9].strip()
    type_tmp = row[10].strip()
    qualification_tmp = row[11].strip()    
    salary_tmp = row[12].strip()
    location_tmp = row[13].strip()
    benefits_tmp = row[14].strip()
    duty_tmp = row[16]    

    # Filter the chinese information
    flag_chinese = chinese_character(position_tmp)
    if flag_chinese == True:
        continue

# Step1: parse the data
# parse locates
# identifies
# and isolates individual data elements in the source fields

#
# parse position
#
#
#
#    
    # Save tmp_salaryduration for step3 use
    position_tmp_salaryduartion = position_tmp
# 1. Remove symbol
    position_tmp = re.sub('&#[0-9]+;', ' ', position_tmp)
    position_tmp = re.sub('[\:\/\-()$\.\|\,\~\*]', ' ', position_tmp)
    position_tmp = re.sub('<.*?>', '', position_tmp)
    position_tmp = re.sub('\?', '', position_tmp)
    position_tmp = re.sub('&[a-zA-Z0-9];', ' ', position_tmp)
    position_tmp = position_tmp.upper()
    
    
# 2. Filter out the salary and work duration
#   a. parse salary
    p_salary_in_position = re.compile(r'$[0-9]+[kK]')
    if p_salary_in_position.search(position_tmp_salaryduartion) != None:
        p_salary_in_position1 = re.compile(r'$(.*)K')
        salary_in_position1 = p_salary_in_position1.search(position_tmp_salaryduartion)
        if salary_in_position1 != None:
            salary_tmp = salary_in_position1.group(1) + 'K'

#        b. parse work duration
    p_duration_in_position = re.compile(r'(.*)Day')
    duration_in_position = p_duration_in_position.search(position_tmp_salaryduartion)
    if duration_in_position != None:
        workduration_tmp = duration_in_position.group(1)

#
# parse postdate
#
#
#
#  
    postdate_tmp = re.sub('post on ', '', postdate_tmp)
    
#
# parse ParseCompany1
#
#
#
#   
    company_tmp = re.sub('[\:\/\-()$\.\,\?]', ' ', company_tmp)
    company_tmp = re.sub('&[a-zA-Z0-9];', ' ', company_tmp)
    company_tmp = re.sub('[\?\&]', '', company_tmp)
#
# parse function
#
#
#
#   
    function_tmp = re.sub('\(.*\)', '', function_tmp)
    function_tmp = re.sub(r'<br/>', ' ', function_tmp)
    function_tmp = re.sub('/', ' ', function_tmp)
    function_tmp = re.sub('&[0-9a-zA-Z]+;', ' ', function_tmp)
    function_tmp = re.sub('>', '', function_tmp)

# Parse salary
#
#
#
#
#  filter the characters after negotiable/provided
    salary_tmp = salary_tmp.upper()
    if "NEGOTIABLE" in salary_tmp:
        salary_tmp = "NA"
    if "PROVIDED" in salary_tmp:
        salary_tmp = "NA" 
    if salary_tmp == "":
        salary_tmp = "NA"
    if salary_tmp == "BASE SALARY + HIGH COMMISSION":
        salary_tmp = "NA"
    salary_tmp = ParseSalary(salary_tmp)
#
#
# NLP to deal with the data
#
#

    

    
# Step2: Data transformation
# convert the data from one data type to another type
#
#
#
#
# 1. PostDate to the standard format 2016-02-01
    postdate_tmp = convert_time(postdate_tmp)

# Step3: Data standardization
# standardizing the information in that field to a specific format
# 1. covert the qualification to the stadnardizing version
    if qualification_tmp == '--':
        qualification_tmp = ""

# 2. covert the salary to the stadnardizing version
    if '--' in salary_tmp :
        salary_tmp = ""
    if 'Month' in salary_tmp :
        split_tmp = salary_tmp.split()
        salary_tmp = split_tmp[0]
    if 'Hour' in salary_tmp :
        split_tmp = salary_tmp.split()
        salary_tmp = split_tmp[0]+' | Hour'
        
# 3. covert the experience to the stadnardizing version
#    try to find the first number
    wrk_loc = re.search("\d", wrkexperience_tmp)
    if wrk_loc != None:
        wrk_num = wrkexperience_tmp[wrk_loc.start()]
        if wrkexperience_tmp[wrk_loc.start()+1].isdigit():
            wrk_num = wrk_num + wrkexperience_tmp[wrk_loc.start()+1]
        wrkexperience_tmp = wrk_num
    else:
        wrkexperience_tmp = "NA"
        
# 4. PostDate to the standard format 2016-02-01
    if ('hr' in postdate_tmp) or ('min' in postdate_tmp):
        postdate_tmp = '2016-04-04'

# 5. covert the location to the standardizing version
#    standard location list in the Location.txt
#    Remove 'area'
#    'Not Specified' -> 'Others'
    location_tmp = (re.sub('\(.*\)', '', location_tmp)).strip()
    if location_tmp == '' or location_tmp == 'N/A':
        location_tmp = 'NA'
    else:
        location_tmp = location_tmp.upper()
        location_tmp = location_tmp.replace('AREA', '')
        location_tmp = location_tmp.replace('DISTRICT', '')
        # get the first location
        p_location_first = re.compile(r'(.*)\,')
        location_first = p_location_first.search(location_tmp)
        if location_first != None:
            location_tmp = (location_first.group(1)).strip()
        location_flag = False
        for item in location_list:
            if item in location_tmp:
                location_tmp = item
                location_flag = True
                break
        
        location_tmp = location_tmp.strip()
        # Special Cases            
        for item in location_list_matched:
            if location_tmp in item:
                location_tmp = (item.split('/')[0]).strip()
                location_flag = True
                break
            
        if location_flag == False:
            print "No Location Founded!",location_tmp

# 6. Industry: get the top level
    industry_tmp = re.sub(r'-', '/', industry_tmp)
    p_industry_top_lvl = re.compile(r'(.*?)/')
    if p_industry_top_lvl.search(industry_tmp) != None:
        industry_tmp = ((p_industry_top_lvl.search(industry_tmp)).group(1)).rstrip()
    industry_tmp = industry_tmp.upper()

# 7. convert the industry to the standard format
    industry_flag = False
    for item in industry_list:
        if industry_tmp in item:
            industry_tmp  = (re.search(r'(.*?)/',item)).group(1)
            industry_flag = True
            break

    if industry_flag == False:
        print "No Industry Founded!",industry_tmp
    
# 9. convert the function to the standard format
#   replace the symbol for easy parse
    function_tmp.replace('(',' ')
    function_tmp.replace(',',' ')
    function_tmp.replace(' ',' ')
    function_tmp.replace('&#47;',' ')
    function_tmp.replace('&#38;',' ')
    function_tmp = function_tmp.upper()
#    select the first one as the function
    p_function_first = re.compile(r'\/')
    p_function_data_list = re.compile(r' ')
    function_data_list = p_function_data_list.split(function_tmp)
    function_data_list = filter(None, function_data_list)
    function_tmp = ""
    function_flag = False
    for function_data_li in function_data_list:
        for item in function_list:
            if function_data_li in item:
                function_first = p_function_first.split(item)
                if function_first[0] not in function_tmp:
                    if function_flag == False:
                        function_tmp = function_first[0]
                    else:
                        function_tmp = function_tmp + " / " +function_first[0]
                function_flag = True
                break
    if function_flag == False:
        function_tmp = "Others"

# 10. convert the Level to the standard format
    if 'N/A' in carlvl_tmp or carlvl_tmp == '':
        carlvl_tmp = "NA"
    else:        
        for item in careerlvl_list:
            if carlvl_tmp in item:
                carlvl_tmp = re.split(r'\/', item)[0]
                break
            
# 11. convert the Education to the standard format
#     get the first one
    if 'N/A' in qualification_tmp or qualification_tmp == '':
        qualification_tmp = "NA"
    else:
        p_education = re.search(r'(.*?)/', qualification_tmp)
        if p_education != None:
            qualification_tmp = (p_education.group(1)).strip()
        qualification_tmp = qualification_tmp.upper()
        for item in education_list:
            if qualification_tmp in item:
                qualification_tmp = re.split(r'\/', item)[0]
                break
            
# 12. convert the Type to the standard format
    type_tmp = re.sub(r'\,', '/', type_tmp)
    
# 13. convert the Salary to the standard format
    salary_tmp = re.sub('&#[0-9]+;', ' ', salary_tmp)

# 14. replace the symbol , to |
    benefits_tmp = re.sub('\,', '|', benefits_tmp)
    
# 15. replace the symbol , to |
    language_tmp = re.sub('\,', '|', language_tmp)


    position_tmp=position_tmp.strip()
    company_tmp=company_tmp.strip()
    location_tmp=location_tmp.strip()
    postdate_tmp=postdate_tmp.strip()
    carlvl_tmp=carlvl_tmp.strip()
    wrkexperience_tmp=wrkexperience_tmp.strip()
    qualification_tmp=qualification_tmp.strip()
    industry_tmp=industry_tmp.strip()
    function_tmp=function_tmp.strip()
    salary_tmp=salary_tmp.strip()
    type_tmp=type_tmp.strip()
    duty_tmp=duty_tmp.strip()
    benefits_tmp=benefits_tmp.strip()
    language_tmp=language_tmp.strip()
        
    
    curjob.execute("INSERT INTO position \
    (Source, Position, Company, \
    Location, Postdate, CareerLvl, \
    WrkExperience, Education, Industry, \
    Function, Salary, Type, Duty, Language, Benefits) VALUES \
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
    ('2',position_tmp,company_tmp,
    location_tmp,postdate_tmp,carlvl_tmp,
    wrkexperience_tmp,qualification_tmp,industry_tmp,
    function_tmp,salary_tmp,type_tmp,duty_tmp,
    language_tmp,benefits_tmp))
    
    dbjob.commit()


    

dbjiujik.close()
dbjob.close()




