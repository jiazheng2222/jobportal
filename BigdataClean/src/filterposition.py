
import re

with open('trainin_position_all.txt','r') as file:
    with open('position_filter.txt','w') as filter:
        for item in file:
            item = re.sub('["&\+\,\!_\[\]\.\~]', ' ', item)
            str_tmp = re.split(r' ', item)
            if '' in str_tmp:
                str_tmp.remove('')
            for it in str_tmp:
                filter.write(it+'\n')
                

            