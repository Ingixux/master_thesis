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
        self.getDataFromSilkFile()
        #self.train()
        


    def train(self):
        for trainingClasses in self.dicOfFileOutput.values():
            trainingClasses[0].train()

    def getDataFromSilkFile(self):
        for file in self.listOfPathToSilkFiles:
            infile = silkfile_open(file, READ)
            self.setDataToZero()
            for rec in infile:
                for trainingClasses in self.dicOfFileOutput.values():
                    if trainingClasses[0].typeOfFeatures =="fields":
                        trainingClasses[1]=self.createNetlfowFeilds(rec,trainingClasses[1])
                    elif trainingClasses[0].typeOfFeatures =="entropy":
                        trainingClasses[1]=self.createNetlfowEntropy(rec,trainingClasses[1],False)
                    elif trainingClasses[0].typeOfFeatures =="combined":
                        trainingClasses[1]=self.createNetlfowCombined(rec,trainingClasses[1],False)
                    elif trainingClasses[0].typeOfFeatures =="entropylimited":
                        trainingClasses[1]=self.createNetlfowEntropy(rec,trainingClasses[1],True)
                    elif trainingClasses[0].typeOfFeatures =="combinedlimited":
                        trainingClasses[1]=self.createNetlfowCombined(rec,trainingClasses[1],True)
            self.saveDataTofile(file)
        #data = np.array(data)
        pass


    def saveDataTofile(self,file):
        for trainingClasses in self.dicOfFileOutput.values():
            trainingClasses[1]=np.array(trainingClasses[1])
            nameoffile=file.split("/")[-1]
            trainingClasses[1].dump("data/Classifiers/"+nameoffile+trainingClasses[0].name+".npy")
            trainingClasses[0].filepathOfInput="data/Classifiers/"+nameoffile+trainingClasses[0].name+".npy"
            trainingClasses[0].filepathOfClassifier="data/Classifiers/"+nameoffile+trainingClasses[0].name+".pkl"
            #print(trainingClasses[1])
            #TODO save to file

    def setDataToZero(self):
        for trainingClasses in self.dicOfFileOutput.values():
            trainingClasses[1]=[]

    def createNetlfowFeilds(self,rec,data):
        isAttackFlow=0
        #if rec.sensor=="isAttack": #TODO why does this not work
        #    isAttackFlow=1
        if rec.sensor_id==3:
            isAttackFlow=1
        data.append([rec.stime, rec.etime, rec.sport, rec.dport, rec.protocol, rec.packets, rec.bytes, 
                            int(rec.tcpflags.fin), int(rec.tcpflags.syn), int(rec.tcpflags.rst), int(rec.tcpflags.psh), int(rec.tcpflags.ack), 
                            int(rec.tcpflags.urg), int(rec.tcpflags.ece), int(rec.tcpflags.cwr), rec.duration/datetime.timedelta(milliseconds=1), 
                            isAttackFlow])
        return data

    def createNetlfowEntropy(self,rec,data,limited):
        pass

    def createNetlfowCombined(self,rec,data,limited):
        pass

RF=RandomforestDetection("fields","","")

#a1=TraningOfClassification([RF],["data/DiffrentSamplingRates/TCP_SYN_Flodd500"])
a1=TraningOfClassification([RF],["data/DiffrentSamplingRates/isattack100"])
a1.train()