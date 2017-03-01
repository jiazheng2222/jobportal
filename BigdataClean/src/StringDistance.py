
def EditDistance(str1,str2):
    len1 = len(str1)
    len2 = len(str2)
    distance = [[0 for y in range(0,len1+1,1)] for x in range(0,len2+1,1)]
    for index in range(0,len1+1,1):
        distance[0][index] = index
    for index in range(0,len2+1,1):
        distance[index][0] = index
    
    for indey in range(1,len2+1,1):
        for index in range(1,len1+1,1):  
            dis1 = distance[indey-1][index-1]
            if str1[index-1] == str2[indey-1]:
                dis1 = dis1
            else:
                dis1 = dis1 + 1
            dis2 = distance[indey-1][index] + 1
            dis3 = distance[indey][index-1] + 1
            
            dis = dis1
            if dis2 < dis:
                dis = dis2
            if dis3 < dis:
                dis = dis3
            distance[indey][index] = dis
    
    # Special Case:
    if len1 == 0 and len2 == 0:
        return 0
    # Set the threshold to be 0.80
    threshold = 0.80
    value = 1-float(distance[len2][len1]*2)/(len1+len2)
    
    '''
    if  value > 0.75:
        print str1
        print str2
        print distance[len2][len1]
        print str(len1)+" "+str(len2)
    '''
        
    if value >= threshold:
        return 1
    else:
        return 0


def AffineGapDis(str1,str2):
    len1 = len(str1)
    len2 = len(str2)
    distance = [[0 for y in range(0,len1+1,1)] for x in range(0,len2+1,1)]
    for index in range(0,len1+1,1):
        distance[0][index] = index
    for index in range(0,len2+1,1):
        distance[index][0] = index
    
    for indey in range(1,len2+1,1):
        for index in range(1,len1+1,1):  
            dis1 = distance[indey-1][index-1]
            if str1[index-1] == str2[indey-1]:
                dis1 = dis1
            else:
                dis1 = dis1 + 1
            dis2 = distance[indey-1][index] + 1
            dis3 = distance[indey][index-1] + 1
            
            dis = dis1
            if dis2 < dis:
                dis = dis2
            if dis3 < dis:
                dis = dis3
            distance[indey][index] = dis
    
    '''
    for index in range(len2+1):
        for indey in range(len1+1):
            print distance[index][indey],
        print ''
    '''
    
    tracequeue = []
    tracequeue.append(len2)
    tracequeue.append(len1)
    
    inderow = len2
    indecol = len1
    minrow = 0
    mincol = 0
    while inderow>0 and indecol>0:
        if distance[inderow-1][indecol] <= distance[inderow][indecol-1]:
            minrow = inderow-1
            mincol = indecol
        else:
            minrow = inderow
            mincol = indecol-1
        if distance[inderow-1][indecol-1] <= distance[minrow][mincol]:
            minrow = inderow-1
            mincol = indecol-1
        tracequeue.append(minrow)
        tracequeue.append(mincol)
        inderow = minrow
        indecol = mincol
    
    # Affine Gap Formula
    # A + B*L
    # match +2
    # mismatch -1
    # first gap -2
    #       gap -1
    value = 0
    length = len(tracequeue)/2
    gapflag = False
    for index in range(len(tracequeue)-2,0,-2):
        #print tracequeue[index],tracequeue[index+1]
        #print tracequeue[index-2],tracequeue[index-1]
        if tracequeue[index]+1 == tracequeue[index-2] and tracequeue[index+1]+1 == tracequeue[index-1]:
            if distance[tracequeue[index]][tracequeue[index+1]] == distance[tracequeue[index-2]][tracequeue[index-1]]:
                value = value + 2
            else:
                value = value - 1
            gapflag = False
        else:
            if distance[tracequeue[index]][tracequeue[index+1]] != distance[tracequeue[index-2]][tracequeue[index-1]]:
                if gapflag == True:
                    value = value - 1
                else:
                    value = value -2
                gapflag = True
    
    # Set the threshold to be 0.75
    threshold = 0.75
    value = float(value)/(length)
    if value >= threshold:
        return 1
    else:
        return 0

'''  
str1 = "Audit Senior  Audit Associate"
str2 = "Audit SeniorAudit Ass"
print AffineGapDis(str1,str2)
'''