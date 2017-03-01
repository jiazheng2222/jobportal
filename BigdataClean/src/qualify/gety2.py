import re

count = 149
matched = 0
unmatched = 0

with open('log.txt','rb') as file:
    for item in file:
        if (item.split(',')[14]).strip() == 'y' :
            matched = matched + 1
            xx = (item.split(',')[12]).strip()
            yy = (item.split(',')[13]).strip()
            if xx != yy:            
                print xx+","+yy
        count = count + 1
        #else:
        #    unmatched = unmatched + 1
            
print count
#print matched
#print unmatched