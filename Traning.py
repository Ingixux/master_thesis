import numpy as np
import pickle as pickle
import os
from RandomforestDetection import RandomforestDetection
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
        toPredict=[]
        toPredict.append(data)
        darecta=np.array(toPredict, dtype=object)
        Features=darecta[:,2:-1]
        labels=darecta[:,-1]
        #print(Features)
        #print(labels)
        print(trainingClasses[0].detect(Features)[0]==labels[0])

    def detect(self):
        self.getDataFromSilkFile("detect")

    def train(self):
        for trainingClasses in self.dicOfFileOutput.values():
            trainingClasses[0].train()

    #def saveDataTofile(self,file):
    #    for trainingClasses in self.dicOfFileOutput.values():
    #        trainingClasses[1]=np.array(trainingClasses[1])
    #        nameoffile=file.split("/")[-1]
    #        trainingClasses[1].dump("data/Classifiers/"+nameoffile+trainingClasses[0].name+".npy")
    #        trainingClasses[0].filepathOfInput="data/Classifiers/"+nameoffile+trainingClasses[0].name+".npy"
    #        trainingClasses[0].filepathOfClassifier="data/Classifiers/"+nameoffile+trainingClasses[0].name+".pkl"
            #print(trainingClasses[1])

    def saveDataTofile(self,file,data,trainingClasses):
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
            for rec in infile:
                for trainingClasses in self.dicOfFileOutput.values():
                    #newData=[rec.stime,rec.etime]
                    dataToHandle=[]
                    if trainingClasses[0].typeOfFeatures =="fields":
                        dataToHandle= self.createNetlfowFeilds(rec)
                    elif trainingClasses[0].typeOfFeatures in ["entropy","combined"]:
                        dataToHandle=self.createNetlfowEntropy(rec,trainingClasses[0])
                    #print(dataToHandle)
                    if detectortrain=="train" and len(dataToHandle)>0:
                        #print(dataToHandle)
                        if trainingClasses[0].typeOfFeatures =="fields":
                            self.saveDataTofile(file,dataToHandle,trainingClasses)
                        elif trainingClasses[0].typeOfFeatures in ["entropy","combined"]:
                            for rec1 in dataToHandle:
                                self.saveDataTofile(file,rec1,trainingClasses)
                    elif detectortrain=="detect" and len(dataToHandle)>0:
                        if trainingClasses[0].typeOfFeatures =="fields":
                            self.doDetectionOnData(dataToHandle,trainingClasses)
                        elif trainingClasses[0].typeOfFeatures in ["entropy","combined"]:
                            for rec1 in dataToHandle:
                                self.doDetectionOnData(rec1,trainingClasses)
            for trainingClasses in self.dicOfFileOutput.values():
                if trainingClasses[0].typeOfFeatures in ["entropy","combined"]:
                    toadd=trainingClasses[0].entropy.doCalculation()
                    if len(toadd) !=0:
                        for r in toadd:
                            tempr=[]
                            if trainingClasses[0].typeOfFeatures =="entropy":
                                tempr=r[0:2]+r[18:]
                            else:
                                tempr= r 
                            if detectortrain=="train":
                                self.saveDataTofile(file,tempr,trainingClasses)
                            elif detectortrain=="detect":
                                self.doDetectionOnData(tempr,trainingClasses)
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
                            int(rec.tcpflags.fin), int(rec.tcpflags.syn), int(rec.tcpflags.rst), int(rec.tcpflags.psh), int(rec.tcpflags.ack), 
                            int(rec.tcpflags.urg), int(rec.tcpflags.ece), int(rec.tcpflags.cwr), rec.duration/datetime.timedelta(milliseconds=1), 
                            self.setIsAttack(rec)]
        return data

    def createNetlfowEntropy(self,rec,decttionclass):
        toadd=decttionclass.entropy.addNewRec(rec)
        #print(len(toadd))
        data =[]
        if len(toadd) !=0:
            if decttionclass.entropy.checkwindowcomplet():
                for r in toadd:
                    tempr=[]
                    if decttionclass.typeOfFeatures =="entropy":
                        tempr=r[0:2]+r[18:]
                        data.append(tempr)
                    else:
                        data.append(r)
            #print(data)
        return data
    

RF=RandomforestDetection("fields","","")
EP=RandomforestDetection("entropy","","")
CP=RandomforestDetection("combined","","")

#a1=TraningOfClassification([RF],["data/DiffrentSamplingRates/TCP_SYN_Flodd500"])
#a1=TraningOfClassification([RF,EP],["data/DiffrentSamplingRates/isattack100"])

a1=TraningOfClassification([CP],["data/DiffrentSamplingRates/isattack100"])
#a1=TraningOfClassification([RF],["data/DiffrentSamplingRates/isattack100"])

a1.makeTraingData()
a1.train()
a1.detect()