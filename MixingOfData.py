#from silk import *


""" 
count the total number of packets, inside of the time space the attack is being mix inn,
The number of real packets have to be mdultiplied with 100, add the number of total attack packets and normal packets, 
and remove 1/100 of pactkes and other info so that it looks like it was sampeled with 1/100 (myby it is here the change of sampling rates happens)

multiple attack files needs to be possible

5000 packets -> attack

450 * 100 = 45000 -> normal  

50000

5000/50000 = 10%

45000/50000= 90 %


1/100
500 packets in new 
450 packets of normal 
50 packets of attack

1/1000
50 packets in new  
45 packets of normal 
5 packets of attack

1/10000
5 packets in new  
4 packets of normal 
1 packets of attack


When mixing move through the time and add a packtet when you get to the sampling rate
"""

class MixingOfData:
    def __init__(self,listWithChaningOfSamplingRate,inputFile1,inputFile2,innput=[100,1]):
        if len(innput) >2 or type(innput) != list:
            innput ==[100,1]
        else:
            if len(innput) >1:
                if type(innput[1])!=int:
                    innput[1] = 1
            if type(innput[0])!=int:
                innput[0] = 100
        self.dicOfFileOutput ={}
        if len(inputFile1) ==0:
            raise ValueError("Sorry, no input for inputFile1") 
        else:
            if len(inputFile2) !=0:
                if type(inputFile2) != str:
                    raise SyntaxError("Sorry, not valid string for the file inputFile2")
            if type(inputFile1) != str :
                raise SyntaxError("Sorry, not valid string for the file inputFile1") 
        self.inputFile1 = inputFile1
        if len(inputFile2) ==0 :
            self.inputFile2 = 0
        else:
            self.inputFile2 = inputFile2
        
        #for x in range(0, len(listWithChaningOfSamplingRate)):
        #    self.dicOfFileOutput["ModifiedAttackFiles/"+attack+str(x)]= [silkfile_open("data/ModifiedAttackFiles/"+attack+str(x), WRITE),listWithChaningOfSamplingRate[x]]



class ChaningOfSamplingRate:
    def __init__(self):
        pass
        


innput="sa"
if type(innput) == str:
    print("hei")