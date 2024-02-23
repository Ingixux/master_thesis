import numpy as np
import pickle as pickle
import os
from RandomforestDetection import RandomforestDetection
from silk import *
import datetime

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
        


    def train(self):
        self.getDataFromSilkFile()
        for trainingClasses in self.dicOfFileOutput.values():
            trainingClasses[0].train()

    def getDataFromSilkFile(self,detectortrain):
        for file in self.listOfPathToSilkFiles:
            infile = silkfile_open(file, READ)
            self.setDataToZero()
            for rec in infile:
                for trainingClasses in self.dicOfFileOutput.values():
                    #newData=[rec.stime,rec.etime]
                    if trainingClasses[0].typeOfFeatures =="fields":
                        trainingClasses[1]=self.createNetlfowFeilds(rec,trainingClasses[1])
                    elif trainingClasses[0].typeOfFeatures in ["entropy","combined"]:
                        trainingClasses[1]=self.createNetlfowEntropy(rec,trainingClasses[1],trainingClasses[0])
                    #TODO add the saving to file here
                        #both training and class
                        #this will remove hte need to store theb data in the dic
                        
                    #elif trainingClasses[0].typeOfFeatures =="entropy":
                    #    trainingClasses[1]=self.createNetlfowEntropy(rec,trainingClasses[1],trainingClasses[0])
                    #elif trainingClasses[0].typeOfFeatures =="combined":
                    #    trainingClasses[1]=self.createNetlfowCombined(rec,trainingClasses[1],trainingClasses[0])
                    #elif trainingClasses[0].typeOfFeatures =="entropylimited":
                    #    trainingClasses[1]=self.createNetlfowEntropy(rec,trainingClasses[1],trainingClasses[0])
                    #elif trainingClasses[0].typeOfFeatures =="combinedlimited":
                    #    trainingClasses[1]=self.createNetlfowCombined(rec,trainingClasses[1],trainingClasses[0])
                    #TODO handle the 
                    #isAttackFlow=0
                    #if rec.sensor_id==3:
                    #    isAttackFlow=1
                    #newData.append(isAttackFlow)
                    #trainingClasses[1].append(newData)
            for trainingClasses in self.dicOfFileOutput.values():
                if trainingClasses[0].typeOfFeatures in ["entropy","combined"]:
                    toadd=trainingClasses[0].entropy.doCalculation()
                    if len(toadd) !=0:
                        for r in toadd:
                            tempr=[]
                            if trainingClasses[0].typeOfFeatures =="entropy":
                                tempr=r[18:]
                                trainingClasses[1].append(tempr)
                            else:
                                trainingClasses[1].append(r)
            self.saveDataTofile(file)

        #data = np.array(data)
            
    def getDataFromSilkFileDetect(self):
            self.saveDataTofile(file)
        #data = np.array(data)

    def setIsAttack(self,rec):
        isAttackFlow=0
        #if rec.sensor=="isAttack": #TODO why does this not work
        #    isAttackFlow=1
        if rec.sensor_id==3:
            isAttackFlow=1
        return isAttackFlow

    def saveDataTofile(self,file):
        for trainingClasses in self.dicOfFileOutput.values():
            trainingClasses[1]=np.array(trainingClasses[1])
            nameoffile=file.split("/")[-1]
            trainingClasses[1].dump("data/Classifiers/"+nameoffile+trainingClasses[0].name+".npy")
            trainingClasses[0].filepathOfInput="data/Classifiers/"+nameoffile+trainingClasses[0].name+".npy"
            trainingClasses[0].filepathOfClassifier="data/Classifiers/"+nameoffile+trainingClasses[0].name+".pkl"
            #print(trainingClasses[1])


    def setDataToZero(self):
        for trainingClasses in self.dicOfFileOutput.values():
            trainingClasses[1]=[]

    def createNetlfowFeilds(self,rec,data):
        #li=[rec.sport, rec.dport, rec.protocol, rec.packets, rec.bytes, 
        #                    int(rec.tcpflags.fin), int(rec.tcpflags.syn), int(rec.tcpflags.rst), int(rec.tcpflags.psh), int(rec.tcpflags.ack), 
        #                    int(rec.tcpflags.urg), int(rec.tcpflags.ece), int(rec.tcpflags.cwr), rec.duration/datetime.timedelta(milliseconds=1)]
        #for x in (0,len(li)):
        #    data.append(li[x])
        data.append([rec.stime, rec.etime, int(rec.sip), int(rec.dip), rec.sport, rec.dport, rec.protocol, rec.packets, rec.bytes, 
                            int(rec.tcpflags.fin), int(rec.tcpflags.syn), int(rec.tcpflags.rst), int(rec.tcpflags.psh), int(rec.tcpflags.ack), 
                            int(rec.tcpflags.urg), int(rec.tcpflags.ece), int(rec.tcpflags.cwr), rec.duration/datetime.timedelta(milliseconds=1), 
                            self.setIsAttack(rec)])
        return data

    def createNetlfowEntropy(self,rec,data,decttionclass):
        toadd=decttionclass.entropy.addNewRec(rec)
        if len(toadd) !=0:
            if decttionclass.entropy.checkwindowcomplet():
                for r in toadd:
                    tempr=[]
                    if decttionclass.typeOfFeatures =="entropy":
                        tempr=r[18:]
                        data.append(tempr)
                    else:
                        data.append(r)
        return data

    def createNetlfowCombined(self,rec,data,trainingClasses):
        #TODO add handlig to how to deal with entropy which is not yet over the window size
        return data

RF=RandomforestDetection("fields","","")

#a1=TraningOfClassification([RF],["data/DiffrentSamplingRates/TCP_SYN_Flodd500"])
a1=TraningOfClassification([RF],["data/DiffrentSamplingRates/isattack100"])
a1.train()