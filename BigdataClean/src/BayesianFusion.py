from cmath import log, exp

alpha = 0.1
beta = 1 - 2*alpha
copy_ratio = 0.8
totalnumber = 50


def BayesianFusion(Accuracy,WordAccuracy,sameflag):
    #source accuracy
    AS = Accuracy
    #word accuracy
    #same flag to label the difference value between two source
    
    Copy_Data_All_Item = 0
    index = 0
    for WA in WordAccuracy:
        if sameflag[index] == 1:
        # Same value
            Copy_Data_Item = log((1-copy_ratio)+
                    copy_ratio*((WA*AS+(1-WA)*(1-AS))
                    /(WA*AS*AS+(1-WA)*(1-AS)*(1-AS)/totalnumber)))
        # Different value
        else:
            Copy_Data_Item = log(1-copy_ratio)
        Copy_Data_All_Item = Copy_Data_All_Item + Copy_Data_Item
        index = index + 1
    #print Copy_Data_All_Item 
    return (1/(1+alpha/beta*(exp(Copy_Data_All_Item)*2))).real*100
     
    
'''
AS = 0.2
WordAccuracy = [0.01,0.95,0.015,0.015,0.5]
sameflag = [1,1,1,1,0]
print BayesianFusion(AS,WordAccuracy,sameflag)
'''
AS = 0.81298
WordAccuracy = [0.0764,0.1341,0.1965,0.0119,0.1211,0.1565,0.1468,0.0868,0.0488,0.4525,0.2605,0.0868]
sameflag = [1,1,1,1,1,1,1,1,1,1,1,1]
print BayesianFusion(AS,WordAccuracy,sameflag)
