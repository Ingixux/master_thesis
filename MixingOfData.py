from silk import *
import copy
import datetime
import random 
import os
import math

class TempRecords:
    def __init__(self,rec,samplingUsedToCollect,keyToFile):
        #self.rec=copy.copy(rec)
        self.rec=rec
        self.stime = self.rec.stime
        self.totalPackets = self.rec.packets *samplingUsedToCollect
        self.duration = self.rec.duration
        self.packetsUsed = 0
        self.packetsWeight = 0
        self.packetToWrite = 0
        self.currentetime= self.rec.stime
        self.bytes= rec.bytes *samplingUsedToCollect
        self.keyToFile=keyToFile

    def getPacketsLeft(self):
        return self.totalPackets - self.packetsUsed
    
    def increasePacketsUsed(self, packets,timeNow):
        self.packetsUsed += packets
        self.packetsWeight += packets
        self.currentetime=timeNow

    def setPacketsWeightZero(self,overPackets):
        if self.packetsUsed>=self.totalPackets:
            self.packetsWeight=overPackets
        else:
            self.packetsWeight=overPackets

    def checkEnd(self):
        if self.packetsUsed>=self.totalPackets:
            return True
        else:
            return False
        
    def increasePacketToWrite(self):
        self.packetToWrite+=1

    def endOfFlow(self,timeNow):
        if self.packetToWrite ==0:
            return 0
        else:
            self.rec.packets = self.packetToWrite
            self.rec.bytes =(self.bytes // self.totalPackets) * self.packetToWrite 
            self.rec.duration = (timeNow - self.rec.stime)
            return self.rec

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
            pathToFile ="data/DiffrentSamplingRates/"+namOupFile+str(chaningOfSamplingRate[0].maxpackets)
            if os.path.isfile(pathToFile):
                os.remove(pathToFile)
            chaningOfSamplingRate.append(silkfile_open(pathToFile, WRITE))
        self.currentTime=0
        
        self.mix()
        
        self.closeAllFiles()

    def mix(self):
        records =1
        while records>0:
            newNext=self.getNextRecord()
            nextstime= self.findLowestNextRecStime()
            for samplingRateFiles in self.dicOfFileOutput.values():
                if len(newNext) != 0:
                    for tempRecords in newNext:
                        samplingRateFiles[0].listOfCurrenttempRecords.append(copy.copy(tempRecords))
                    countpackets =0
                    longerflows=0
                    #TODO somthing must be added here, so that records here don't get remove if there isn't enugh, in the current time, but they are completet
                    for tempRecords in samplingRateFiles[0].listOfCurrenttempRecords:
                        packetToUseNow=0
                        if nextstime - tempRecords.currentetime <= tempRecords.duration:
                            packetToUseNow =tempRecords.getPacketsLeft()
                            tempRecords.increasePacketsUsed(packetToUseNow,tempRecords.currentetime)
                        countpackets +=packetToUseNow
                    for tempRecords in samplingRateFiles[0].listOfCurrenttempRecords:
                        longerflows+=1
                        diffrentInStartTime =0
                        packetToUseNow=0
                        dDBDIST = 0 #dDBDIST=durationDivivedByDiffrentInStartTime
                        if nextstime ==datetime.datetime.max:
                            packetToUseNow =tempRecords.getPacketsLeft()
                        else:
                            diffrentInStartTime = nextstime- tempRecords.currentetime
                            dDBDIST = math.floor(tempRecords.duration / diffrentInStartTime)  
                            if dDBDIST<1:
                                packetToUseNow =tempRecords.getPacketsLeft()
                            else:
                                packetToUseNow =int(tempRecords.getPacketsLeft() // dDBDIST)
                        tempRecords.increasePacketsUsed(packetToUseNow,nextstime)
                        
                        countpackets +=packetToUseNow
                    overMax,timesover=samplingRateFiles[0].addPackets(countpackets)
                    if overMax:
                        theWeights =[]
                        recordsToUse =[]
                        setWeightStart =(samplingRateFiles[0].countpackets) //longerflows
                        extraSetWeightStart=(samplingRateFiles[0].countpackets) % longerflows
                        x=0
                        for tempRecords in samplingRateFiles[0].listOfCurrenttempRecords: #TODO need to handle if there are more packets than sample rate
                            if tempRecords.checkEnd() == False:
                                tempsetWeightStart = copy.copy(setWeightStart)
                                if x<extraSetWeightStart:
                                    tempsetWeightStart+=1
                                    x+=1
                                theWeights.append(tempRecords.packetsWeight-tempsetWeightStart)
                                tempRecords.setPacketsWeightZero(tempsetWeightStart)
                            else:
                                theWeights.append(tempRecords.packetsWeight)
                            recordsToUse.append(tempRecords)
                        incressWrite=random.choices(recordsToUse, weights=theWeights, k=timesover) #create the
                        for tempRecords in incressWrite:
                            tempRecords.increasePacketToWrite()
                    self.writeAndDelTemprecdors(samplingRateFiles)
                else:
                    self.writeAndDelTemprecdors(samplingRateFiles)
                    records =0

    def writeAndDelTemprecdors(self,samplingRateFiles):
        tempDelList =[]
        for tempRecords in samplingRateFiles[0].listOfCurrenttempRecords:
            if tempRecords.checkEnd():
                recToWrtie= tempRecords.endOfFlow(self.currentTime)
                if recToWrtie!=0:
                    samplingRateFiles[1].write(recToWrtie)
                tempDelList.append(tempRecords)
        for tempRecords in tempDelList:
            samplingRateFiles[0].listOfCurrenttempRecords.remove(tempRecords)    
            del tempRecords

    def findLowestNextRecStime(self):
        tempkey=0
        for key in self.dicOfFileInnput.keys():
            if tempkey== 0:
                    tempkey=key
            elif self.dicOfFileInnput[tempkey][0].currentStartTime>self.dicOfFileInnput[key][0].currentStartTime:
                    tempkey=key
        return self.dicOfFileInnput[tempkey][0].currentStartTime

    def getNextRecord(self):
        """
        Gathers all the next records with the same start time, and retruns them in a list
        the dicOfFileInnput.nextRec is the next record that have a later strat time 
        First time the function is run, both files are read, else the one with the earlist start time is read  
        """
        temprecords= []
        temprec=0
        if self.currentTime == 0:
            for key in self.dicOfFileInnput.keys():
                temprec=self.dicOfFileInnput[key][1].read() # TODO check what happen if the file stops
                self.dicOfFileInnput[key][0].addNextRec(temprec)
                if self.currentTime == 0:
                    self.currentTime =self.dicOfFileInnput[key][0].currentStartTime
                elif self.currentTime>self.dicOfFileInnput[key][0].currentStartTime:
                    self.currentTime =self.dicOfFileInnput[key][0].currentStartTime 
        for x in self.addNewRecWhileSameSTIME():
            temprecords.append(x)
        if temprec==0:
            tempkey=0
            for key in self.dicOfFileInnput.keys():
                if tempkey== 0:
                    tempkey=key
                elif self.dicOfFileInnput[tempkey][0].currentStartTime>self.dicOfFileInnput[key][0].currentStartTime:
                    tempkey=key
            if self.dicOfFileInnput[tempkey][0].currentStartTime != datetime.datetime.max:
                self.currentTime =self.dicOfFileInnput[tempkey][0].currentStartTime
            for x in self.addNewRecWhileSameSTIME():
                temprecords.append(x)
        return temprecords
                 
    def addNewRecWhileSameSTIME(self):
        temprecords =[]
        for key in self.dicOfFileInnput.keys():
            record = self.dicOfFileInnput[key][0].getNextRecord()
            if record !=0:
                while record.stime ==self.currentTime:
                    if self.currentTime==self.dicOfFileInnput[key][0].currentStartTime:
                        temprecords.append(TempRecords(record,self.dicOfFileInnput[key][0].maxpackets,key))
                        temprec=self.dicOfFileInnput[key][1].read()
                        if temprec != None:
                            self.dicOfFileInnput[key][0].addNextRec(temprec)
                        else:
                            self.dicOfFileInnput[key][0].addNextRec(0)
                    record = self.dicOfFileInnput[key][0].getNextRecord()
                    if record==0:
                        break
        return temprecords
    
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
                self.dicOfFileOutput[SamplingRateTochange.samplingRate][0].inputFile1SamplingRate= innput[0].maxpackets
                if len(innput) == 2:
                    self.dicOfFileOutput[SamplingRateTochange.samplingRate][0].inputFile2SamplingRate= innput[1].maxpackets

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
        if len(inputFile2) !=0 :
            self.dicOfFileInnput[inputFile2]= [innput[1],silkfile_open(inputFile2, READ)]
        else:
            self.inputFile2 = 0
        
    def closeInputFiles(self):
        """
        closes innput files
        """
        for set in self.dicOfFileInnput.values():
            set[1].close() 

class ChaningOfSamplingRate:
    def __init__(self,changeTosamplingRate):
        self.maxpackets = changeTosamplingRate.maxpackets
        self.inputFile1SamplingRate = 0
        self.inputFile2SamplingRate = 0
        self.listOfCurrenttempRecords =[]
        self.countpackets =0

    def checkIfOverMax(self):
        if self.countpackets>=self.maxpackets:
            return True
        else:
            return False

    def addPackets(self,newPackets): 
        if newPackets>self.maxpackets:
            timesover= (newPackets +self.countpackets)//self.maxpackets
            newPackets = newPackets- self.maxpackets*timesover
            self.countpackets+=newPackets
            self.checkIfOverMax()
            return True,timesover 
        else:
            self.countpackets+=newPackets
            isover = self.checkIfOverMax()
            if isover:
                self.countpackets= self.countpackets-self.maxpackets
                return isover, 1
            else: 
                return isover, 0 

class SamplingRate:
    def __init__(self,samplingRate):
        self.initCheckSamplingRate(samplingRate)
        self.currentStartTime=0
        self.nextRec=0

    def getNextRecord(self):
        return self.nextRec

    def addNextRec(self,nextRec):
        self.nextRec=nextRec
        if nextRec ==0:
            self.currentStartTime= datetime.datetime.max
        else:
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

        

sa1 =SamplingRate("1:1")
sa2 =SamplingRate("1:100")
ca1 =SamplingRate("1:500")
ca2 =SamplingRate("1:1000")


#MD = MixingOfData([ca2],"data/ModifiedAttackFiles/TCP_SYN_Flodd","data/SilkFilesFromSikt/TCP_SYN_Flodd",[sa1,sa2])
MD = MixingOfData([ca1,ca2],"data/ModifiedAttackFiles/TCP_SYN_Flodd","data/SilkFilesFromSikt/TCP_SYN_Flodd",[sa1,sa2])

