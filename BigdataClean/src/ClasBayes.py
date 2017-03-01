import re
from TrainingData import *
# Use the bayes Decision Rule
class ClasBayes:
    # Here are the criteria:
    #   Similarity 1: <0.5    0
    #                 0.5-0.7 1
    #                 >0.7    2
    P1Lvl1 = 0.5
    P1Lvl2 = 0.7
    #   Similarity 2: <0.6    0
    #                 >=0.6   1
    P2Lvl1 = 0.6
    
    Number_field = 2
    
    # Training Module Data
    # Initialize the Bayes module
    TNum = 0
    FNum = 0
    ta0 = ta1 = ta2 = 0
    tb0 = tb1 = 0
    fa0 = fa1 = fa2 = 0
    fb0 = fb1 = 0
    data = []
    
    def __init__(self):
        
        
        training_data_input = []
        training_data = []
        with open('Training.txt','rb') as training:
            for line in training:
                training_data_input.append(line)
                
        for index in range(0,len(training_data_input),1):
            p_data = re.compile(r' ')
            self.data = p_data.split(training_data_input[index].rstrip())
            
            p1 = p2 = 0
            cls = ''
            if self.data[2] == 'T':
                self.TNum = self.TNum + 1
                cls = 'T'
                
                if float(self.data[0]) < self.P1Lvl1:
                    p1 = 0
                    self.ta0 = self.ta0 + 1
                elif float(self.data[0]) < self.P1Lvl2:
                    p1 = 1
                    self.ta1 = self.ta1 + 1
                else:
                    p1 = 2
                    self.ta2 = self.ta2 + 1
                
                if float(self.data[1]) < self.P2Lvl1:
                    p2 = 0
                    self.tb0 = self.tb0 + 1
                else:
                    p2 = 1
                    self.tb1 = self.tb1 + 1
            else:
                self.FNum = self.FNum + 1
                cls = 'F'
                
                if float(self.data[0]) < self.P1Lvl1:
                    p1 = 0
                    self.fa0 = self.fa0 + 1
                elif float(self.data[0]) < self.P1Lvl2:
                    p1 = 1
                    self.fa1 = self.fa1 + 1
                else:
                    p1 = 2
                    self.fa2 = self.fa2 + 1
                
                if float(self.data[1]) < self.P2Lvl1:
                    p2 = 0
                    self.fb0 = self.fb0 + 1
                else:
                    p2 = 1
                    self.fb1 = self.fb1 + 1
                    
            data_tmp = TrainingData(p1,p2,cls)
            training_data.append(data_tmp)
        
    def Classify(self, similarity):
        # Use the module
        # P(T|a=x,b=y)/P(F|a=x,b=y)
        #   P(T)*P(a=x,b=y|T)     P(T)*P(a=x|T)*P(b=y|T)
        # = -----------------  =  ----------------------
        #   P(F)*P(a=x,b=y|F)     P(F)*P(a=x|F)*P(b=y|F)
        #                        tax*tby/TNum
        #                     =  -----------------------
        #                        fax*fby/FNum
        
        # Test Set
        a = similarity[0]
        b = similarity[1]
        tax = tby = 0
        fax = fby = 0
        
        if float(a) < self.P1Lvl1:
            tax = self.ta0
            fax = self.fa0
        elif float(self.data[0]) < self.P1Lvl2:
            tax = self.ta1
            fax = self.fa1
        else:
            tax = self.ta2
            fax = self.fa2
        
        if float(self.data[1]) < self.P2Lvl1:
            tby = self.tb0
            fby = self.fb0
        else:
            tby = self.tb1
            fby = self.fb1
        
        result = (tax*tby/self.TNum)/(fax*fby/self.FNum)
        return str(result)
    
    