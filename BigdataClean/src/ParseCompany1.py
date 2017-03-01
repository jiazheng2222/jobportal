# select the data from the position TABLE
# SELECT company, location, industry FROM bigdatajob.position 
# Parse the data from bigdatajob

import MySQLdb
import re

# Fetch all the data from bigdatajob 
dbjobsdb = MySQLdb.connect(user='root', 
                    passwd='1234',
                    host='localhost',
                    db='bigdatajob')
curjobsdb = dbjobsdb.cursor()

# Insert the parsed data into job schema
dbjob = MySQLdb.connect(user='root', 
                    passwd='1234',
                    host='localhost',
                    db='bigdatajob')
curjob = dbjob.cursor()

curjobsdb.execute("SELECT source, company, location, industry FROM bigdatajob.position ")

for row in curjobsdb.fetchall():
    source_tmp = row[0].rstrip()
    company_tmp = row[1].rstrip()
    location_tmp = row[2].rstrip()
    industry_tmp = row[3].rstrip()     

#curjob.execute("INSERT INTO position (Source, Position, Company, Location, Postdate, CareerLvl, WrkExperience, Education, Industry, Function, Salary, Type, Duty) VALUES ('1', 'po', 'com', 'loc', 'time', 'lvl', 'xyear', 'edu', 'ind', 'func', 'sala', 'typ', 'dut');")
    curjob.execute("INSERT INTO company \
    (Source, Company, Location, Industry) VALUES \
    (%s, %s, %s, %s);",
    (source_tmp,company_tmp,
    location_tmp,industry_tmp))
    dbjob.commit()



dbjobsdb.close()
dbjob.close()





