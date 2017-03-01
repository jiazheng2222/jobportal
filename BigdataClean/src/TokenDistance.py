import re
from cmath import log

# For each word: w in string A has a weight:
#           v(w) = log (tf+1)*log(idf)
#           tf: the number of times that w appears 
#                in the Field
#           idf: the relative number of the times 
#                appears in the Databse
#                = |D|/Nw
#                |D|: size of the database
#                Nw : number of records in the database D

# Similarity: string A1,A2
#                       sum(vA1(w)*vA2(w))
#            Sim(A1,A2)=--------------------
#                            |A1|*|A2|

# Step1:
# Initialize the words weight


# Step2:
# Use the module to check the data

def WDis(str1,str2):
    p_split = re.compile(r' ')
    data_str1 = p_split.split(str1)
    data_str2 = p_split.split(str2)
    
    vector1 = []
    vector1_num = []
    vector2 = []
    vector2_num = []
#    calc the vA1(w) and vA2(w)
#    v(w) = log (tf+1)*log(idf)
#    Str1
    for i in range(0,len(data_str1),1):
        search_flag = False
        for j in range(0,len(vector1),1):
            if data_str1[i].strip(' ') == vector1[j].strip(' '):
                vector1_num[j] = vector1_num[j] + 1
                search_flag = True
        if search_flag == False:
            vector1.append(data_str1[i])
            vector1_num.append(1)

#    Str2
    for i in range(0,len(data_str2),1):
        search_flag = False
        for j in range(0,len(vector2),1):
            if data_str2[i].strip(' ') == vector2[j].strip(' '):
                vector2_num[j] = vector2_num[j] + 1
                search_flag = True
        if search_flag == False:
            vector2.append(data_str2[i])
            vector2_num.append(1)

#    Similarity
    sum = 0
    for i in range(0,len(vector1),1):
        # replace 3
        v1 = log(vector1_num[i]+1)/log(10)
        v2 = 0
        for j in range(0,len(vector2),1):
            if vector1[i].strip(' ') == vector2[j].strip(' '):
                v2 = log(vector2_num[j]+1)/log(10)
                break
        sum = sum + v1*v2
    #print sum
    # Set the threshold to be 0.75
    threshold = 0.75
    value = sum/(len(vector1)*len(vector2))*100
    
    if value >= threshold:
        return 1 
    else:
        return 0


'''
str1 = "AUDIT SENIOR Starting from HK$22.5K  SEMI SENIOR Starting from HK$16.5K"
str2 = "AUDIT SEMI SENIOR  AUDIT JUNIOR"
print WDis(str1,str2)
'''

def AtomicDis(str1,str2):
    p_split = re.compile(r' ')
    arr1 = p_split.split(str1)
    arr2 = p_split.split(str2)
    
    if '' in arr1:
        arr1.remove('')
    if '' in arr2:
        arr2.remove('')
    
    arr1.sort()
    arr2.sort()
    
    if len(arr1) == 0 or len(arr2) == 0:
        return 0
    
    SimilarFlag = True
    if len(arr1) > len(arr2):
        for index in range(0,len(arr2),1):
            if arr1[index] != arr2[index]:
                SimilarFlag = False
                break
    else:
        for index in range(0,len(arr1),1):
            if arr1[index] != arr2[index]:
                SimilarFlag = False
                break
    
    if SimilarFlag:
        return 1
    else:
        return 0
        

'''
str1 = "Audit Senior  Audi Associate"
str2 = "Audit Audit Associate Senior"
print AtomicDis(str1,str2)
'''