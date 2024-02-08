from silk import *
import copy
import datetime
import random 
import os
import math
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

class TempRecords:
    def __init__(self,rec,samplingUsedToCollect,keyToFile):
        #self.rec=copy.deepcopy(rec)
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
        self.lastTime=False
        self.end=False

    def getPacketsLeft(self):
        return self.totalPackets - self.packetsUsed
    
    def increasePacketsUsed(self, packets,timeNow):
        self.packetsUsed += packets
        self.packetsWeight += packets
        self.currentetime=timeNow
        if self.packetsUsed>=self.totalPackets:
            pass
        else:
            pass


    def decreasePacketsUsed(self, packets):
        self.packetsUsed -= packets
    

    def setPacketsWeightZero(self,overPackets):
        if self.lastTime == True:
            self.end == True
        elif self.packetsUsed>=self.totalPackets:
            self.lastTime = True
            self.packetsWeight=overPackets
        else:
            self.packetsWeight=overPackets

    def checkEnd(self):
        return self.end
        if self.end:
        #if self.lastTime == True:
            return True
        else:
            return False
    
    def findDifInTime(self):
        pass

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
        #TODO add the mixing
        #if len(self.dicOfFileInnput.keys)==1:
        #    pass

        #when mixing, for each time the max is reach save temp of all record that arrive until max is reach again. save the temp in a list in a dic, so that it can be erased based on the chaning#
        records =1
        while records>0:
            newNext=self.getNextRecord()
            nextstime= self.findLowestNextRecStime()
            for samplingRateFiles in self.dicOfFileOutput.values():
                if len(newNext) != 0:
                    for tempRecords in newNext:
                        samplingRateFiles[0].listOfCurrenttempRecords.append(copy.copy(tempRecords))
                    #for record in records:
                    #    samplingRateFiles.listOfCurrenttempRecords.append(TempRecords(record,))
                    #for tempRecords in samplingRateFiles.listOfCurrenttempRecords:
                    countpackets =0
                    for tempRecords in samplingRateFiles[0].listOfCurrenttempRecords:
                        diffrentInStartTime =0
                        packetToUseNow=0
                        dDBDIST = 0 #dDBDIST=durationDivivedByDiffrentInStartTime
                        if nextstime - tempRecords.currentetime < tempRecords.duration:
                            packetToUseNow =tempRecords.getPacketsLeft()
                            tempRecords.increasePacketsUsed(packetToUseNow,tempRecords.currentetime)
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
                    print()
                    print(countpackets)
                    print(timesover)
                    print(overMax)
                    print("smapling "+str(samplingRateFiles[0].maxpackets))
                    if overMax:
                        theWeights =[]
                        recordsToUse =[]
                        setWeightStart =(samplingRateFiles[0].countpackets) // len(samplingRateFiles[0].listOfCurrenttempRecords)
                        extraSetWeightStart=(samplingRateFiles[0].countpackets) % len(samplingRateFiles[0].listOfCurrenttempRecords)
                        #print(setWeightStart*len(samplingRateFiles[0].listOfCurrenttempRecords))
                        #print(extraSetWeightStart)
                        x=0
                        for tempRecords in samplingRateFiles[0].listOfCurrenttempRecords: #TODO need to handle if there are more packets than sample rate
                            tempsetWeightStart = copy.copy(setWeightStart)
                            if x<extraSetWeightStart:
                                tempsetWeightStart+=1
                                x+=1
                            #print(x+setWeightStart)
                            #tempRecords.decreasePacketsUsed(tempsetWeightStart)
                            theWeights.append(tempRecords.packetsWeight-tempsetWeightStart)
                            tempRecords.setPacketsWeightZero(tempsetWeightStart)
                            #theWeights.append(tempRecords.packetsWeight-tempsetWeightStart)
                            recordsToUse.append(tempRecords)
                        incressWrite=random.choices(recordsToUse, weights=theWeights, k=timesover) #create the

                        #print(len(incressWrite))
                        #print("smapling "+str(samplingRateFiles[0].maxpackets))
                        #print()
                        #print(samplingRateFiles[0].maxpackets) 
                        #print()
                        for tempRecords in incressWrite:
                            #timeToWrtie= nextstime
                            #if nextstime == datetime.datetime.max:
                            #    timeToWrtie = self.currentTime
                            tempRecords.increasePacketToWrite()
                            #tempRecords.increasePacketToWrite(timeToWrtie)
                    #listToDel=[]
                    for tempRecords2 in samplingRateFiles[0].listOfCurrenttempRecords:
                        #for tempRecords2 in incressWrite:
                        #    if tempRecords == tempRecords2:
                        #        tempRecords.increasePacketToWrite()
                        
                        #print(tempRecords2.checkEnd())
                        if tempRecords2.checkEnd():
                            #TODO write the record
                            recToWrtie= tempRecords2.endOfFlow(self.currentTime)
                            if recToWrtie!=0:
                                samplingRateFiles[1].write(recToWrtie)
                            samplingRateFiles[0].listOfCurrenttempRecords.remove(tempRecords2)    
                            del tempRecords2
                            #listToDel.append(tempRecords)
                    #for tempRecords in listToDel:
                    #        samplingRateFiles[0].listOfCurrenttempRecords.remove(tempRecords)
                    #        del tempRecords
                        #TODO check if record is being remove
                else:
                    for tempRecords in samplingRateFiles[0].listOfCurrenttempRecords:
                        #TODO write the record
                        recToWrtie= tempRecords.endOfFlow(self.currentTime)
                        if recToWrtie!=0:
                            samplingRateFiles[1].write(recToWrtie)
                        samplingRateFiles[0].listOfCurrenttempRecords.remove(tempRecords)
                        del tempRecords
                        records =0


                    
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
        # will the first record, the first time it is run
        if self.currentTime == 0:
            for key in self.dicOfFileInnput.keys():
                temprec=self.dicOfFileInnput[key][1].read()
                self.dicOfFileInnput[key][0].addNextRec(temprec)
                #self.dicOfFileInnput[key][0].currentStartTime =temprec.stime
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
            #print(self.dicOfFileInnput[key][0].getNextRecord())
            #print(self.currentTime)
            record = self.dicOfFileInnput[key][0].getNextRecord()
            if record !=0:
                while record.stime ==self.currentTime:
                    if self.currentTime==self.dicOfFileInnput[key][0].currentStartTime:
                        #temprecords.append(record)
                        temprecords.append(TempRecords(record,self.dicOfFileInnput[key][0].maxpackets,key))
                        temprec=self.dicOfFileInnput[key][1].read()
                        if temprec != None:
                            self.dicOfFileInnput[key][0].addNextRec(temprec)
                            #self.dicOfFileInnput[key][0].currentStartTime =temprec.stime
                        else:
                            self.dicOfFileInnput[key][0].addNextRec(0)
                            #self.dicOfFileInnput[key][0].currentStartTime =datetime.datetime.max
                    record = self.dicOfFileInnput[key][0].getNextRecord()
                    if record==0:
                        break
        return temprecords

    """
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
            temprec =self.addNewRecWhileSameSTIME()
        return False
        """
    
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
                #self.dicOfFileOutput[SamplingRateTochange.samplingRate][0].inputFile1SamplingRate= copy.deepcopy(innput[0])
                self.dicOfFileOutput[SamplingRateTochange.samplingRate][0].inputFile1SamplingRate= innput[0].maxpackets
                if len(innput) == 2:
                    #self.dicOfFileOutput[SamplingRateTochange.samplingRate][0].inputFile2SamplingRate= copy.deepcopy(innput[1])
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
        #self.changeTosamplingRate = changeTosamplingRate.maxpackets
        self.maxpackets = changeTosamplingRate.maxpackets
        self.inputFile1SamplingRate = 0
        self.inputFile2SamplingRate = 0
        self.listOfCurrenttempRecords =[]
        self.countpackets =0

    def checkIfOverMax(self):
        if self.countpackets>=self.maxpackets:
            self.countpackets= self.countpackets-self.maxpackets
            return True
        else:
            return False
        
    def addToListOfCurrenttempRecords(self, tempRecords):    
        self.listOfCurrenttempRecords.append(copy.deepcopy(tempRecords))


    def addPackets(self,newPackets): #TODO Wrong!!!!!!!
        if newPackets>self.maxpackets:
            timesover= newPackets//self.maxpackets
            newPackets = newPackets- self.maxpackets*timesover
            self.countpackets+=newPackets
            self.checkIfOverMax()
            return True,timesover+1 
        else:
            self.countpackets+=newPackets
            isover = self.checkIfOverMax()
            if isover:
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

    def getTotalPacketsInFlow(self, packets):
        return self.maxpackets * packets

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

