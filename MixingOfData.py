from silk import *
import copy
import datetime
import random 
import os
import math
import subprocess

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
    """
    This Class is used to mix two sources of input files (inputFile1 , inputFile2) and 
    Create output files with diffrent sampling rate
    This class takes as input :
        listWithChaningOfSamplingRate:
            This is the list of the SamplingRate of the output files, each element will create a new output file
            The elements is of the SamplingRate Class 
        inputFile1:
            Is a list files to be mixed, all elements are assusmed to have the same sampling rate, 
            (standard so is this the attack fiels)
            It is assumed that they are in stored on time with the first elemenet being the earlist file in inputFile1
        inputFile2:
            Is a list files to be mixed, all elements are assusmed to have the same sampling rate, 
            (standard so is this the normal fiels)
            It is assumed that they are in stored on time with the first elemenet being the earlist file in inputFile2
        innput:
            This is the sampling rate which the input files have. The elements are of the SamplingRate Class.
            The first element is sampling rate of the files in inputFile1,
            The second element is sampling rate of the files in inputFile2.
        outputTraniOrDetect:
            Telles the program to either save the data in detect or train folder of data/DiffrentSamplingRates/
    
    self.dicOfFileOutput ={}
    self.dicOfFileInnput ={}
    self.dictofthelistofinputfile
    self.currentTime=
    """
    def __init__(self,listWithChaningOfSamplingRate,inputFile1,inputFile2,innput,outputTraniOrDetect):
        innput= self.checkInput(innput)
        self.dicOfFileOutput ={}
        self.dicOfFileInnput ={}
        self.dictofthelistofinputfile={"tempAttack.rw":inputFile1,"tempNormal.rw":inputFile2}
        #self.openInputFiles(inputFile1,inputFile2,innput)
        self.openInputFiles(innput)
        self.checkChaningOfsamplingRate(listWithChaningOfSamplingRate,innput)
        if outputTraniOrDetect not in ["detect","train"]:
            raise ValueError("output folder not str train or detect")
        for chaningOfSamplingRate in self.dicOfFileOutput.values():
            #namOupFile= inputFile1.split("/")[-1] 
            #TODO This doesn't handle chaningOfSamplingRate with same samplingrate
            pathToFile ="/media/sf_share/data/DiffrentSamplingRates/"+outputTraniOrDetect+"/"+outputTraniOrDetect+str(chaningOfSamplingRate[0].maxpackets)
            #pathToFile ="data/DiffrentSamplingRates/"+outputTraniOrDetect+"/"+outputTraniOrDetect+str(chaningOfSamplingRate[0].maxpackets)
            if os.path.isfile(pathToFile):
                os.remove(pathToFile)
            chaningOfSamplingRate.append(silkfile_open(pathToFile, WRITE))
        self.currentTime=0
        
        self.mix()
        
        #self.closeAllFiles()

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
        the dicOfFileInnput.nextRec is the next records that have a later start time the ones that get return 
        First time the function is run, both files are read, and the one with the earlist start time is used as the currentStartTime
        the nexts time it check which of the next records have the earlist start time and uses that as currentStartTime
        After the currentStartTime is set it calleds the addNewRecWhileSameSTIME() which will find all records of both files
        these are added to temprecords and retrun
        """

        #TODO add it so that there can be more files 
        temprecords= []
        temprec=0
        """
        This only happens the first time calling this method. The earlist start time is set as self.currentTime.
        """
        if self.currentTime == 0:
            for key in self.dicOfFileInnput.keys():
                temprec=self.dicOfFileInnput[key][1].read() 
                self.dicOfFileInnput[key][0].addNextRec(temprec)
                if self.currentTime == 0:
                    self.currentTime =self.dicOfFileInnput[key][0].currentStartTime
                elif self.currentTime>self.dicOfFileInnput[key][0].currentStartTime:
                    self.currentTime =self.dicOfFileInnput[key][0].currentStartTime 
            for x in self.addNewRecWhileSameSTIME():
                temprecords.append(x)
        """
        This only happens all other times this method is called
        """
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
                        
                        temprec=self.dicOfFileInnput[key][1].read()#TODO Here I belive I can move to the next file
                        if temprec==None:
                            #firstfileAttack=self.dictofthelistofinputfile[keyoffile].pop(0)
                            #self.openNextInputFile(,key)
                            if self.openNextInputFile(key) ==False:
                                self.dicOfFileInnput[key][1].close() 
                                self.dicOfFileInnput[key][0].addNextRec(0)
                            else:
                                temprec=self.dicOfFileInnput[key][1].read() #TODO this does not handle if the next file is empty
                                self.dicOfFileInnput[key][0].addNextRec(temprec)
                        else:
                            self.dicOfFileInnput[key][0].addNextRec(temprec)
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
            innput =[SamplingRate("1:1"),SamplingRate("1:100")] 
        else:
            if len(innput) >1:
                if type(innput[1])!=SamplingRate:
                    innput[1] = SamplingRate("1:100")
            if type(innput[0])!=SamplingRate:
                innput[0] = SamplingRate("1:1")
        return innput

    def openNextInputFile(self,keytoinputfile):#openNextInputFile(self,inputFiles,keytoinputfile):
        """
        This methode closes the current ative file, then it checks if there are more files to open
        if not then retruns False
        if there are more files to read
        then it gets the first and, sorts it with self.sortFile
        and then opens the self.dicOfFileInnput with new open file and return True
        """
        
        if len(self.dictofthelistofinputfile[keytoinputfile]) ==0:
            return False
        else:
            nextfile=self.dictofthelistofinputfile[keytoinputfile].pop(0)
            if type(nextfile) != str :
                raise SyntaxError("Sorry, not valid string for the file inputFile1")
        
        self.sortFile(keytoinputfile,nextfile)
        self.dicOfFileInnput[keytoinputfile][1]= silkfile_open(keytoinputfile, READ)
        return True

    def openInputFiles(self,innput): #(self,inputFiles1,inputFiles2,innput)
        """
        This methode is run at init, and it will open the first file in list of inputFiles
        If there are no inputFiles ERROR is trhown
        Method will sort the file to a temp file, by using methode sortFile, these temps files will be remove the each time sortFile is called
        The open will be saved to self.dicOfFileInnput with the key to the temp file,
        the open files are saved in a list toghter with the correspoing SamplingRate class
        """
        if len(self.dictofthelistofinputfile["tempNormal.rw"]) ==0 and len(self.dictofthelistofinputfile["tempAttack.rw"]):
            raise ValueError("Sorry, no input files") 
        else:
            keyoffile="tempNormal.rw"
            if len(self.dictofthelistofinputfile[keyoffile]) !=0 :
                firstfileNormal=self.dictofthelistofinputfile[keyoffile].pop(0)
                if type(firstfileNormal) != str:
                    raise SyntaxError("Sorry, not valid string for the first file inputFiles2")
                #keyoffile="tempNormal.rw"
                self.sortFile(keyoffile,firstfileNormal)
                self.dicOfFileInnput[keyoffile]= [copy.copy(innput[1]),silkfile_open(keyoffile, READ)]
            else:
                self.inputFile2 = 0
            keyoffile="tempAttack.rw"
            if len(self.dictofthelistofinputfile[keyoffile]) !=0 :
                firstfileAttack=self.dictofthelistofinputfile[keyoffile].pop(0)
                if type(firstfileAttack) != str:
                    raise SyntaxError("Sorry, not valid string for the first file inputFiles1")
                keyoffile="tempAttack.rw"
                self.sortFile(keyoffile,firstfileAttack)
                self.dicOfFileInnput[keyoffile]= [copy.copy(innput[0]),silkfile_open(keyoffile, READ)]
            else:
                self.inputFile1 = 0

    def sortFile(self,fileOutput,fileInput,):
        """
        This removes the old temp file (fileOutput),
        then it sorts the silk file (fileInput) and opens it to temp file
        """
        if os.path.isfile(fileOutput):
            x=subprocess.call("rm "+fileOutput, shell=True)#tempattack.rw
        x=subprocess.call("rwsort --fields=stime --output-path="+fileOutput+" "+fileInput+"", shell=True)

    def closeInputFiles(self):
        """
        Closes the active temp files
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

        

#sa1 =SamplingRate("1:1")
#sa2 =SamplingRate("1:100")
#ca1 =SamplingRate("1:500")
#ca2 =SamplingRate("1:1000")


#MD = MixingOfData([ca2],"data/ModifiedAttackFiles/TCP_SYN_Flodd","data/SilkFilesFromSikt/TCP_SYN_Flodd",[sa1,sa2])
#MD = MixingOfData([ca1,ca2],"data/ModifiedAttackFiles/TCP_SYN_Flodd","data/SilkFilesFromSikt/TCP_SYN_Flodd",[sa1,sa2])

#MD = MixingOfData([ca1,sa2],"data/ModifiedAttackFiles/isattack","data/SilkFilesFromSikt/TCP_SYN_Flodd",[sa2,sa2])
#MD = MixingOfData([ca2],"data/ModifiedAttackFiles/TCP_SYN_Flodd0","data/SilkFilesFromSikt/TCP_SYN_Flodd",[sa1,sa2])
#listofnormal=["/media/sf_share/oslo/out/2011/01/25/out-S1_20110125.12","/media/sf_share/oslo/out/2011/01/25/out-S1_20110125.13"]
#MD = MixingOfData([ca2],["data/ModifiedAttackFiles/TCP_SYN_Flodd0"],listofnormal,[sa1,sa2],"train")
#MD = MixingOfData([ca2],"data/ModifiedAttackFiles/TCP_SYN_Flodd0","outfile.rw",[sa1,sa2])
#MD = MixingOfData([ca2],["data/ModifiedAttackFiles/TCP_SYN_Flodd0"],["outfile2.rw"],[sa1,sa2])
#MD = MixingOfData([ca2],["data/ModifiedAttackFiles/TCP_SYN_Flodd0"],["/media/sf_share/oslo/out/2011/01/25/out-S1_20110125.12"],[sa1,sa2],"train")

