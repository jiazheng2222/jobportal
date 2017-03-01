from itertools import count

count = 0
matched = 0
unmatched = 0

with open('log.txt','rb') as file:
    for item in file:
        count = count + 1
        if (item.split(' ')[2]).strip() == 'y' :
            matched = matched + 1
            with open('match.txt','a+') as matchfile:
                matchfile.write("'"+(item.split(' ')[0]).strip() + 
                                "','"+ (item.split(' ')[1]).strip()+"',\n")
        else:
            unmatched = unmatched + 1
            
print count
print matched
print unmatched