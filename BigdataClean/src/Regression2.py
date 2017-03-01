import re
import numpy as np
import statsmodels.api as sm

y = []
x = []
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
            
            for it in range(1,13,1):
                item_set.append(int(items[it].strip()))
            train.append(item_set) 
            y.append(int(items[15].strip()))

for index in range(0,12,1):
    item_x = []
    for indey in range(0,len(train),1):
        item_x.append(train[indey][index])
    x.append(item_x)

def reg_m(y, x):
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    #results = sm.OLS(formula='x12 ~ x1 + x2 + x3 -1 ', data=).fit()
    results = sm.OLS(y, X).fit()
    return results

'''
def reg_m(y, x):
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()
    return results
'''
    
print reg_m(y, x).summary()

