from silk import *
import copy
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
    #TODO add the possiblety to remove files that exits, when oping to write
    """
    The class assumes that the two files inputFile1 and inputFile2 are sorted on time
    """
    def __init__(self,listWithChaningOfSamplingRate,inputFile1,inputFile2,innput):
        innput= self.checkInput(innput)
        self.dicOfFileOutput ={}
        self.dicOfFileInnput ={}
        self.openInputFiles(inputFile1,inputFile2,innput)
        self.checkChaningOfsamplingRate(listWithChaningOfSamplingRate,innput)
        for chaningOfSamplingRate in self.dicOfFileOutput.values():
            namOupFile= inputFile1.split("/")[-1] 
            chaningOfSamplingRate.append(silkfile_open("data/DiffrentSamplingRates/"+namOupFile+chaningOfSamplingRate[0].changeTosamplingRate.samplingRate, WRITE))
        self.currentTime=0
        self.mix()
        
        self.closeAllFiles()

    def mix(self):
        #TODO add the mixing
        if len(self.dicOfFileInnput.keys)==1:
            pass

        #when mixing, for each time the max is reach save temp of all record that arrive until max is reach again. save the temp in a list in a dic, so that it can be erased based on the chaning
        tempRecordList=[] 

    def readNextRecs(self):
        temprec=0
        if self.currentTime == 0:
            for key in self.dicOfFileInnput.keys():
                self.dicOfFileInnput[key][0].addNextRec(self.dicOfFileInnput[key][1].read())
                if self.currentTime == 0:
                    self.currentTime =self.dicOfFileInnput[key][0].currentStartTime
                    #temprec=self.dicOfFileInnput[key][0].nextRec
                elif self.currentTime==self.dicOfFileInnput[key][0].currentStartTime:
                    #TODO also add this record dic of temps
                    pass   
                elif self.currentTime>self.dicOfFileInnput[key][0].currentStartTime:
                    self.currentTime =self.dicOfFileInnput[key][0].currentStartTime  
                    #temprec= self.dicOfFileInnput[key][0].nextRec         
            #TODO add the temo record to dic of temps
        #TODO also add this record dic of temps   
        temprec =self.addNewRecWhileSameSTIME()
        if temprec==0: 
            tempkey=0
            for key in self.dicOfFileInnput.keys():
                if tempkey== 0:
                    tempkey=key
                elif self.dicOfFileInnput[tempkey][0].currentStartTime>self.dicOfFileInnput[key][0].currentStartTime:
                    tempkey=key
            temp =self.dicOfFileInnput[tempkey][1].read()
            self.dicOfFileInnput[tempkey][0].addNextRec(temp)
            #TODO also add this record dic of temps          
            temprec =self.addNewRecWhileSameSTIME()

    def addNewRecWhileSameSTIME(self):
        temp = 0
        while self.checkIfOverCurrent == False:
            for key in self.dicOfFileInnput.keys():
                if self.currentTime==self.dicOfFileInnput[key][0].currentStartTime:
                    temp =self.dicOfFileInnput[key][1].read()
                    if temp == None:
                        break
                    else:
                        self.dicOfFileInnput[key][0].addNextRec(temp)
                        #TODO also add this record dic of temps
            #get all record of the same start time
        return temp
        
        



    def checkIfOverCurrent(self):
        allAreOver = True
        for key in self.dicOfFileInnput.keys():
            if self.currentTime==self.dicOfFileInnput[key][0].currentStartTime:
                allAreOver =False
        return allAreOver

    def checkChaningOfsamplingRate(self,listWithChaningOfSamplingRate,innput):
        for SamplingRateTochange in listWithChaningOfSamplingRate:
            if type(SamplingRateTochange)!= SamplingRate:
                raise ValueError("listWithChaningOfSamplingRate dose not contain SamplingRate objects")
            for inn in innput:
                if SamplingRateTochange.maxpackets < inn.maxpackets:
                    raise ValueError("the sampling rate to change to can't be lower than the sampling rate of the to input file")
            if not SamplingRateTochange.samplingRate in self.dicOfFileOutput.keys():
                self.dicOfFileOutput[SamplingRateTochange.samplingRate]=[ChaningOfSamplingRate(SamplingRateTochange)]
                self.dicOfFileOutput[SamplingRateTochange.samplingRate][0].inputFile1SamplingRate= copy.deepcopy(innput[0])
                if len(innput) == 2:
                    self.dicOfFileOutput[SamplingRateTochange.samplingRate][0].inputFile2SamplingRate= copy.deepcopy(innput[1])

    def closeAllFiles(self):
        """
        closes all files
        """
        self.closeOutputFiles()
        self.closeInputFiles()

    def closeOutputFiles(self):
        """
        closes output files
        """
        for set in self.dicOfFileOutput.values():
            set[1].close()      

    def checkInput(self,innput):
        if len(innput) >2 or type(innput) != list:
            innput ==[SamplingRate("1:100"),SamplingRate("1:1")] 
        else:
            if len(innput) >1:
                if type(innput[1])!=SamplingRate:
                    innput[1] = SamplingRate("1:1")
            if type(innput[0])!=SamplingRate:
                innput[0] = SamplingRate("1:100")
        return innput

    def openInputFiles(self,inputFile1,inputFile2,innput):
        if len(inputFile1) ==0:
            raise ValueError("Sorry, no input for inputFile1") 
        else:
            if len(inputFile2) !=0:
                if type(inputFile2) != str:
                    raise SyntaxError("Sorry, not valid string for the file inputFile2")
            if type(inputFile1) != str :
                raise SyntaxError("Sorry, not valid string for the file inputFile1") 
        
        self.dicOfFileInnput[inputFile1]= [innput[0],silkfile_open(inputFile1, READ)]
        if len(inputFile2) ==0 :
            self.inputFile2 = 0
        else:
            self.dicOfFileInnput[inputFile1]= [innput[1],silkfile_open(inputFile2, READ)]
        
    def closeInputFiles(self):
        """
        closes innput files
        """
        for set in self.dicOfFileInnput.values():
            set[1].close() 

class ChaningOfSamplingRate:
    def __init__(self,changeTosamplingRate):
        self.changeTosamplingRate = changeTosamplingRate
        self.inputFile1SamplingRate = 0
        self.inputFile2SamplingRate = 0

    def addPackets(self,newPackets):
        return self.changeTosamplingRate.addPackets(newPackets)

class SamplingRate:
    def __init__(self,samplingRate):
        self.initCheckSamplingRate(samplingRate)
        self.currentStartTime=0
        self.nextRec=0

    def getTotalPacketsInFlow(self, packets):
        return self.maxpackets * packets

    def addNextRec(self,nextRec):
        self.nextRec=nextRec
        self.currentStartTime=self.nextRec.stime

    def initCheckSamplingRate(self,samplingRate):
        self.samplingRate = samplingRate
        if type(samplingRate)!= str:
            raise ValueError("Sorry, sampling rate is not string")
        checkstring=samplingRate.split(":")
        if len(checkstring) != 2:
            raise ValueError("Sorry, input of sampling rate should be like 'int:int'")
        try:
            int(checkstring[0])
            int(checkstring[1])
        except:
            raise ValueError("Sorry, input of sampling rate should be like 'int:int'")
        if int(checkstring[0]) > int(checkstring[1]):
            raise ValueError("Sorry, sampling rate 'int1:int2', int1 has to be smaller than int2 ")
        elif int(checkstring[0]) !=1:
            raise ValueError("Sorry, sampling rate 'int1:int2', int1 has to be 1")
        self.maxpackets = int(checkstring[1])
        self.samplingRate = "1OF"+str(self.maxpackets)
        self.countpackets =0

    def checkIfOverMax(self):
        if self.countpackets>=self.maxpackets:
            self.countpackets= self.countpackets-self.maxpackets
            return True
        else:
            return False
        
    def addPackets(self,newPackets):
        if newPackets>self.maxpackets:
            timesover= newPackets//self.maxpackets
            newPackets = newPackets- self.maxpackets*timesover
            self.countpackets+=newPackets
            if self.checkIfOverMax() == True:
                return timesover+1, True
            else:
                return timesover, False
        else:
            self.countpackets+=newPackets
            return 1, self.checkIfOverMax()
        

sa1 =SamplingRate("1:1")
sa2 =SamplingRate("1:100")
ca1 =SamplingRate("1:500")
ca2 =SamplingRate("1:1000")

MD = MixingOfData([ca1,ca2],"data/ModifiedAttackFiles/TCP_SYN_Flodd","data/SilkFilesFromSikt/TCP_SYN_Flodd",[sa1,sa2])

