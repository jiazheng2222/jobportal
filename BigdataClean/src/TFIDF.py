
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize tf idf
corpus = []
num = 50000
index = 0

filter_list = []
with open('position_filter_list.txt','r') as filter:
    for item in filter:
        filter_list.append(re.sub(r'\n', '', item))
        
with open('trainin_position_all.txt', 'r') as train_pos:
    for item in train_pos:
        if index > num:
            break
        index = index + 1
        item = re.sub('["&\+\,\!_\[\]\.\~]', ' ', item)
        corpus.append(item)
        
tfidf_transformer = TfidfVectorizer(analyzer='word',stop_words=filter_list)

def InitialTFIDF():
    X_train_tfidf = tfidf_transformer.fit_transform(corpus)
    

def IFIDFDist(str1, str2):
    tfidf_result = tfidf_transformer.fit_transform([str1,str2])
    tfidf_array = tfidf_result.toarray()
    
    #print tfidf_array
    dt1 = np.array(tfidf_array[0]).reshape((1, -1))
    dt2 = np.array(tfidf_array[1]).reshape((1, -1))
    similarity = cosine_similarity(dt1, dt2)
    #similarity = cosine_similarity(tfidf_array[0], tfidf_array[1])
    #print "similarity "+str(similarity[0])

    if similarity > 0.75:
        return 1
    else:
        return 0

    #print tfidf_transformer.idf_
    #print X_train_tfidf.shape
'''
InitialTFIDF()
str1 = "Responsible Officer 9  Sole or Non sole    PRC Financial Group"
str2 = "Debt Capital Markets Manager  DCM    PRC based Bank"
IFIDFDist(str1,str2)
'''