import numpy as np
import pickle as pickle
import os
from RandomforestDetection import RandomforestDetection
from Threshold import Threshold
from silk import *
import datetime
import copy

class TraningOfClassification:
    #TODO decide who I want to handle training and testing from same file adn diffrentfiles
    def __init__(self, listOfTrainingClasses,listOfPathToSilkFiles):
        #self.listOfTrainingClasses=listOfTrainingClasses
        self.listOfPathToSilkFiles=listOfPathToSilkFiles
        self.dicOfFileOutput ={}
        data=[]
        for TrainingClasses in listOfTrainingClasses:
            self.dicOfFileOutput[TrainingClasses.name]= [TrainingClasses,data]
        #self.dicOfFileInnput ={}
        #for inputFiles in listOfPathToSilkFiles:
        #    self.dicOfFileInnput[inputFiles]= [???,silkfile_open(inputFiles, READ)]
        
        #self.train()
        

    def makeTraingData(self):
        self.createfilesToSaveTo()
        self.getDataFromSilkFile("train")

    def doDetectionOnData(self,data,trainingClasses):
        #print(data)
        toSave=[]
        if trainingClasses[0].typeOfFeatures =="threshold":
            #print(data)
            toSave=trainingClasses[0].detect(data,data["isAtttack"])#TODO add the isattack feature
        else:
            toPredict=[]
            toPredict.append(data)
            darecta=np.array(toPredict, dtype=object)
            Features=darecta[:,2:-1]
            labels=darecta[:,-1]
            #print(Features)
            #print(labels)
            toSave=trainingClasses[0].detect(Features,labels[0])
    
        print(toSave)
        #TODO save toSave in a file

    def detect(self):
        self.getDataFromSilkFile("detect")

    def train(self):
        for trainingClasses in self.dicOfFileOutput.values():
            trainingClasses[0].train()



    def saveDataTofile(self,file,data,trainingClasses):
        #print(data)
        if trainingClasses[0].typeOfFeatures =="threshold":
            result = data.items()
            fdate= list(result)
            data=np.array(fdate, dtype=object)
            
        #print(data)
        data=np.array(data, dtype=object)
        #print(data)
        np.save(trainingClasses[2],data)

    def createfilesToSaveTo(self):
        for file in self.listOfPathToSilkFiles:
            nameoffile=file.split("/")[-1]
            for trainingClasses in self.dicOfFileOutput.values():
                trainingClasses.append(open("data/Classifiers/"+nameoffile+trainingClasses[0].name+".npy", "wb"))
                trainingClasses[0].filepathOfInput="data/Classifiers/"+nameoffile+trainingClasses[0].name+".npy"
                trainingClasses[0].filepathOfClassifier="data/Classifiers/"+nameoffile+trainingClasses[0].name+".pkl"

    def getDataFromSilkFile(self,detectortrain):
        for file in self.listOfPathToSilkFiles:
            infile = silkfile_open(file, READ)
            self.setDataToZero()
            for rec in infile:  #TODO Handle that when No rec are for a sliding window time
                for trainingClasses in self.dicOfFileOutput.values():
                    #newData=[rec.stime,rec.etime]
                    dataToHandle=[]
                    if trainingClasses[0].typeOfFeatures =="fields":
                        dataToHandle= self.createNetlfowFeilds(rec)
                    elif trainingClasses[0].typeOfFeatures in ["entropy","combined","threshold"]:
                        dataToHandle=self.createNetlfowEntropy(rec,trainingClasses[0])
                    #print(dataToHandle)
                    if detectortrain=="train" and len(dataToHandle)>0:
                        #print(dataToHandle)
                        if trainingClasses[0].typeOfFeatures =="fields":
                            self.saveDataTofile(file,dataToHandle,trainingClasses)
                        elif trainingClasses[0].typeOfFeatures in ["entropy","combined"]:
                            for rec1 in dataToHandle:
                                self.saveDataTofile(file,rec1,trainingClasses)
                        elif trainingClasses[0].typeOfFeatures =="threshold":
                            self.saveDataTofile(file,trainingClasses[0].entropy.getcurrentvaules(),trainingClasses) 
                            #self.saveDataTofile(file,trainingClasses[0].entropy.findThreasholds(False),trainingClasses) 
                    elif detectortrain=="detect" and len(dataToHandle)>0:
                        if trainingClasses[0].typeOfFeatures =="fields":
                            self.doDetectionOnData(dataToHandle,trainingClasses)
                        elif trainingClasses[0].typeOfFeatures in ["entropy","combined"]:
                            for rec1 in dataToHandle:
                                self.doDetectionOnData(rec1,trainingClasses)
                        elif trainingClasses[0].typeOfFeatures in ["threshold"]:
                            self.doDetectionOnData(trainingClasses[0].entropy.findThreasholds(False),trainingClasses)
            for trainingClasses in self.dicOfFileOutput.values(): #TODO this does only acuount for the vaules in [-1],needs to add the vaule to all in the rec
                if trainingClasses[0].typeOfFeatures in ["entropy","combined","threshold"]:
                    toadd=trainingClasses[0].entropy.doCalculation()
                    if trainingClasses[0].typeOfFeatures =="threshold":
                        if detectortrain=="train":
                            self.saveDataTofile(file,trainingClasses[0].entropy.getcurrentvaules(),trainingClasses)
                            #self.saveDataTofile(file,trainingClasses[0].entropy.findThreasholds(True),trainingClasses)
                        elif detectortrain=="detect":
                            self.doDetectionOnData(trainingClasses[0].entropy.findThreasholds(True),trainingClasses)
                    elif len(toadd) !=0:
                        for r in toadd:
                            tempr=[]
                            if trainingClasses[0].typeOfFeatures =="entropy":
                                tempr.append(r[0:2]+r[19:32]+[r[-1]])
                            #elif trainingClasses[0].typeOfFeatures =="threshold":
                            #    tempr=trainingClasses[0].entropy.getcurrentvaules()
                            else:
                                tempr.append(r[0:32]+[r[-1]]) 
                            
                            if detectortrain=="train":
                                self.saveDataTofile(file,tempr[0],trainingClasses)
                            elif detectortrain=="detect":
                                self.doDetectionOnData(tempr[0],trainingClasses)
                    trainingClasses[0].resetentropy()
            infile.close()

    def setIsAttack(self,rec):
        isAttackFlow=0
        #if rec.sensor=="isAttack": #TODO why does this not work
        #    isAttackFlow=1
        if rec.sensor_id==3:
            isAttackFlow=1
        return isAttackFlow

    def setDataToZero(self):
        for trainingClasses in self.dicOfFileOutput.values():
            trainingClasses[1]=[]

    def createNetlfowFeilds(self,rec):
        #li=[rec.sport, rec.dport, rec.protocol, rec.packets, rec.bytes, 
        #                    int(rec.tcpflags.fin), int(rec.tcpflags.syn), int(rec.tcpflags.rst), int(rec.tcpflags.psh), int(rec.tcpflags.ack), 
        #                    int(rec.tcpflags.urg), int(rec.tcpflags.ece), int(rec.tcpflags.cwr), rec.duration/datetime.timedelta(milliseconds=1)]
        #for x in (0,len(li)):
        #    data.append(li[x])
        data=[rec.stime, rec.etime, int(rec.sip), int(rec.dip), rec.sport, rec.dport, rec.protocol, rec.packets, rec.bytes, 
                            int(rec.tcpflags.fin), int(rec.tcpflags.syn), int(rec.tcpflags.rst), int(rec.tcpflags.psh), int(rec.tcpflags.ack),int(rec.nhip), 
                            int(rec.tcpflags.urg), int(rec.tcpflags.ece), int(rec.tcpflags.cwr), rec.duration/datetime.timedelta(milliseconds=1), 
                            self.setIsAttack(rec)]
        return data

    def createNetlfowEntropy(self,rec,decttionclass):
        toadd=decttionclass.entropy.addNewRec(rec)
        #print(len(toadd))
        data =[]
        if len(toadd) !=0:
            if decttionclass.entropy.checkwindowcomplet():
                #if decttionclass.typeOfFeatures =="threshold":
                #    #data.append(r[0:2]+r[20:])
                #    data.append(toadd[0][20:])
                #else:
                for temor in toadd:
                    for r in temor:
                        #tempr=[]
                        if decttionclass.typeOfFeatures =="entropy":
                            #tempr=r[0:2]+r[19:]+r[-1]
                            #data.append(tempr)
                            data.append(r[0:2]+r[19:32]+[r[-1]])
                        #elif decttionclass.typeOfFeatures =="threshold":
                            #data.append(r[0:2]+r[20:])
                        else:
                            data.append(r[0:32]+[r[-1]])
            #print(data)
        return data
    

RF=RandomforestDetection("fields","","")
EP=RandomforestDetection("entropy","","")
CP=RandomforestDetection("combined","","")
TH=Threshold("threshold","","")

#a1=TraningOfClassification([RF],["data/DiffrentSamplingRates/TCP_SYN_Flodd500"])
#a1=TraningOfClassification([RF,EP],["data/DiffrentSamplingRates/isattack100"])

a1=TraningOfClassification([TH],["data/DiffrentSamplingRates/isattack100"])
#a1=TraningOfClassification([RF],["data/DiffrentSamplingRates/isattack100"])
#a1=TraningOfClassification([CP],["data/DiffrentSamplingRates/isattack100"])

a1.makeTraingData()
a1.train()
a1.detect()