# Record Linkage

import MySQLdb
import re
import PositionItem
import DecisionTree
import sys
import json
import nltk
from datetime import datetime
from dateutil.relativedelta import relativedelta
from StringDistance import AffineGapDis,EditDistance
from TokenDistance import AtomicDis
from TFIDF import IFIDFDist,InitialTFIDF
from ctypes.wintypes import DOUBLE
from BayesianFusion import BayesianFusion 

industry_list = []
#industry_list.append('ACCOUNTING')
with open('Industry.txt','rb') as openfile:
    for line in openfile:
        industry_list.append(line.split('/')[0])

similarity = [0]*16
# the number of attributes (remove first 2)
num = 12
# the records that have been merged
merge_record = []

# Initial the Bayesian Module
item_name = []
first_line_flag = True
p_training = re.compile(r',')
train = []
with open("Training.csv","r") as training:
    for item in training:
        if first_line_flag == True:
            item_name = p_training.split(item)
            item_name[15] = item_name[15].strip()
            first_line_flag = False
        else:
            items = p_training.split(item)
            item_set = []
            
            for it in items:
                item_set.append(int(it.strip()))
                
            dict_tmp = dict(zip(item_name[1:13], item_set[1:13]))
            if item_set[15] == 1:
                train.append((dict_tmp,'y'))
            else:
                train.append((dict_tmp,'x'))
                
classifier = nltk.classify.NaiveBayesClassifier.train(train) 
#print classifier.show_most_informative_features()

'''
# Initial the Decision Tree
# Trainning data
training_datafile = "Training.csv"
dt = DecisionTree.DecisionTree(
              training_datafile = training_datafile,
              csv_class_column_index = 15,
              csv_columns_for_features = [1,2,3,4,5,6,7,8,9,10,11,12],
              entropy_threshold = 0.01,
              max_depth_desired = 8,
              symbolic_to_numeric_cardinality_threshold = 1,
   )

dt.get_training_data()
dt.calculate_first_order_probabilities()
dt.calculate_class_priors()
root_node = dt.construct_decision_tree_classifier()
root_node.display_decision_tree("   ")
'''
''

# Fetch all the data from BigDataJob 
dbposition = MySQLdb.connect(user='root', 
                    passwd='1234',
                    host='localhost',
                    db='bigdatajob')
curposition = dbposition.cursor()
# Search and match all the data from BigDataJob 
dbposition_match = MySQLdb.connect(user='root', 
                    passwd='1234',
                    host='localhost',
                    db='bigdatajob')
curposition_match = dbposition_match.cursor()
# Insert into BigDataJob 
dbposition_insert = MySQLdb.connect(user='root', 
                    passwd='1234',
                    host='localhost',
                    db='bigdatajob')
curposition_insert = dbposition_insert.cursor()

for industry_li in industry_list:
    curposition.execute("SELECT * FROM company where source = '1' and \
        industry = '"+industry_li+"' order by postdate ")
    # copy the data to array cmp_tmp
    cmp_list1 = curposition.fetchall()

    block_sql = "SELECT * FROM bigdatajob.company \
        where source = '3' and industry = '"+industry_li+"' \
          order by postdate "
    curposition_match.execute(block_sql)
    cmp_list3 = curposition_match.fetchall()
   
    block_sql2 = "SELECT * FROM bigdatajob.company \
        where source = '2' and industry = '"+industry_li+"' \
          order by postdate "
    curposition_match.execute(block_sql2)
    cmp_list2 = curposition_match.fetchall()
    
    # merge sort the data by their postdate
    index_3 = index_2 = 0
    rowsarr = []
    while index_3 < len(cmp_list3) and index_2 < len(cmp_list2) :
        if  cmp_list3[index_3][5] < cmp_list2[index_2][5]:
            rowsarr.append(cmp_list3[index_3])
            index_3 = index_3 + 1
        else:
            rowsarr.append(cmp_list2[index_2])
            index_2 = index_2 + 1
    # check which one break firstly
    if index_3 == len(cmp_list3) - 1:
        for index_tmp in range(index_2,len(cmp_list2),1):
            rowsarr.append(cmp_list2[index_tmp])
    elif index_2 == len(cmp_list2) - 1:
        for index_tmp in range(index_3,len(cmp_list3),1):
            rowsarr.append(cmp_list3[index_tmp])
    
    # start to scan all the data in list 1
    for row in cmp_list1:
        sourcex = str(row[0])
        position_tmp = row[2].strip()
        company_tmp = row[3].strip()
        location_tmp = row[4].strip()
        postdate_tmp = row[5]
        carlvl_tmp = row[6].strip()
        wrkexperience_tmp = row[7].strip()
        qualification_tmp = row[8].strip()
        industry_tmp = row[9].strip()
        function_tmp = row[10].strip()
        salary_tmp = row[11].strip()
        type_tmp = row[12].strip()    
        duty_tmp = row[13].strip() 
    
        date_object = postdate_tmp
        seven_date_rel = relativedelta(days=7)
        postdate_range_l = date_object - seven_date_rel
        postdate_range_r = date_object + seven_date_rel    
        
        # Blocking to reduce the comparison  
        #         use industry as block
        #         use date to sort searching date
        #         sort by ParseCompany1
        # block searching: 
        
        # Binary search to locate the first data
        index_l = 0
        index_r = len(rowsarr)
        index_mid = (index_l + index_r)/2
        while index_l < index_r :
            if postdate_range_l < rowsarr[index_mid][5]:
                index_r = index_mid - 1
            else:
                index_l = index_mid + 1
            index_mid = (index_l + index_r)/2
              
        # Start to scan from the index_l
        for index in range(index_l,len(rowsarr),1):            
            row_match = rowsarr[index]
            
            sourcey = str(row_match[0])
            position_match = row_match[2].strip()
            postdate_match = row_match[5]     
            
            company_match = row_match[3].strip()
            location_match = row_match[4].strip()
            carlvl_match = row_match[6].strip()
            wrkexperience_match = row_match[7].strip()
            qualification_match = row_match[8].strip()
            industry_match = row_match[9].strip()
            function_match = row_match[10].strip()
            salary_match = row_match[11].strip()
            type_match = row_match[12].strip()    
            duty_match = row_match[13].strip() 
            if postdate_range_r < postdate_match:
                break
                        
    # Starting to compare two records
    # Similarity Metrics
    # 1. Edit string
            #SimilarityEditDis = EditDistance(position_tmp,position_match)
    # 2. Affine Gap
            #SimilarityEditDis = AffineGapDis(position_tmp,position_match)  
    # 3. TokenDistance
            #SimilarityEditDis = WDis(position_tmp,position_match)
    # 4. Tf-idf Distance (Only for position)
                        
            # Position
            #similarity[2] = EditDistance(position_tmp,position_match)
            #similarity[2] = AffineGapDis(position_tmp,position_match)
            #similarity[2] = AtomicDis(position_tmp,position_match)
            similarity[2] = IFIDFDist(position_tmp,position_match)
            
            
            # Company
            similarity[3] = EditDistance(company_tmp,company_match)
            #similarity[3] = AffineGapDis(company_tmp,company_match)
            #similarity[3] = AtomicDis(company_tmp,company_match)
            
            # Location
            if location_tmp == location_match:
                similarity[4] = 1
            else:
                similarity[4] = 0
            # Postdate: must be 1
            similarity[5] = 1
            # career level: ignore it
            if carlvl_tmp == carlvl_match:
                similarity[6] = 1
            else:
                similarity[6] = 0
            # work experience: ignore it
            if wrkexperience_tmp == wrkexperience_match:
                similarity[7] = 1
            else:
                similarity[7] = 0
            # qualification: ignore it
            if qualification_tmp == qualification_match:
                similarity[8] = 1
            else:
                similarity[8] = 0
            # industry: must be 1
            similarity[9] = 1
            # function: check the list
            #     get the tmp list
            function_tmp_list = re.split(r'/', function_tmp)
            #     get the match list
            function_match_list = re.split(r'/', function_match)
            function_flag = False
            for tmp_it in function_tmp_list:
                for match_it in function_match_list:
                    if tmp_it.strip() == match_it.strip():
                        function_flag = True
                        break  
            if function_flag == True:     
                similarity[10] = 1
            else:
                similarity[10] = 0
            # salary: ignore it
            similarity[11] = 0
            # type: ignore it
            if type_tmp == type_match:
                similarity[12] = 1
            else:
                similarity[12] = 0
            # duty
            #similarity[13] = EditDistance(duty_tmp, duty_match)
            #similarity[13] = AffineGapDis(duty_tmp, duty_match)
            #similarity[13] = AtomicDis(duty_tmp, duty_match)
            similarity[13] = 1
                                     
    
    # Duplicate Detection
            merge_flag = False
    # 1. Bayes
            dict_test = dict(zip(item_name[1:13], similarity[1:13]))
            #pdist = classifier.prob_classify(dict_test)
            #print('%.4f %.4f' % (pdist.prob('x'), pdist.prob('y')))
            print sourcex+" "+sourcey+" ",
            bayes_result = classifier.classify(dict_test)
            print bayes_result
            with open('log.txt','a+') as logfile:
                logfile.write(sourcex+" "+sourcey+" "+bayes_result+"\n")
            if bayes_result == 'y':
                merge_flag = True
            
            
    # 2. Decistion Tree to classify
            '''
            test_sample  = ['position = '+str(similarity[1]),
                    'ParseCompany1 = '+str(similarity[2]),
                    'location = '+str(similarity[3]),
                    'postdate = '+str(similarity[4]),
                    'careerlvl = '+str(similarity[5]),
                    'wrkexperience = '+str(similarity[6]),
                    'education = '+str(similarity[7]),
                    'industry = '+str(similarity[8]),
                    'function = '+str(similarity[9]),
                    'salary = '+str(similarity[10]),
                    'type = '+str(similarity[11]),
                    'content = '+str(similarity[12])
                    ]
            classification = dt.classify(root_node, test_sample)                
            result_1 = float((re.search(r'\'result=1\': \'(.*?)\'', str(classification))).group(1))
            result_0 = float((re.search(r'\'result=0\': \'(.*?)\'', str(classification))).group(1))
            if result_1 > result_0 :
                merge_flag = True
            print classification
            '''             
    
            if merge_flag == True :                
                curposition_insert.execute("INSERT INTO company \
                (Source, Company, Location, Industry) VALUES \
                (%s, %s, %s, %s);",
                ('9',company_tmp,
                location_tmp,industry_tmp))
                # Execute the commission to write data
                dbposition_insert.commit()   
       

dbposition_insert.close()
dbposition_match.close()
dbposition.close()

