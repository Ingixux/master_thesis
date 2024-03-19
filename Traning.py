import numpy as np
import pickle as pickle
#import os
from RandomforestDetection import RandomforestDetection
from Threshold import Threshold
from Kmeans import Kmeans
from silk import *
import datetime
#import copy

class TraningOfClassification:
    #TODO decide who I want to handle training and testing from same file adn diffrentfiles
    """
    This Class does now only handle one set of files for each classifier. Does not handle deceting on to diffrent smapling rate
    """
    def __init__(self, listOfTrainingClasses,listOfPathToSilkFiles):
        
        #self.listOfTrainingClasses=listOfTrainingClasses
        self.countcorrect=0
        self.countwrong=0
        self.countisattack=0
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

    def openFilesToSaveTo(self):
        for trainingClasses in self.dicOfFileOutput.values():
            if trainingClasses[0].filepathOfInput=="" or trainingClasses[0].filepathOfClassifier=="":
                raise SystemError("The Classifier filepathOfInput or filepathOfClassifier can't be empyt")
            else:
                if len(trainingClasses)<=2:
                    trainingClasses.append(open(trainingClasses[0].filepathOfInput, "ab"))
                else:
                    trainingClasses[2]=(open(trainingClasses[0].filepathOfInput, "ab"))

            
    def appendTraingData(self):
        self.openFilesToSaveTo()
        self.getDataFromSilkFile("train")

    def doDetectionOnData(self,data,trainingClasses):
        toSave=[]
        if trainingClasses[0].typeOfFeatures =="threshold":
            toSave=trainingClasses[0].detect(data,data["isAtttack"])#TODO add the isattack feature
            #for x in toSave:
            #    if x[1]==x[2]:
            #        self.countcorrect+=1
            #    else:
            #        self.countwrong+=1
        else:
            toPredict=[]
            toPredict.append(data)
            darecta=np.array(toPredict, dtype=object)
            Features=darecta[:,2:-1]
            labels=darecta[:,-1]
            toSave=trainingClasses[0].detect(Features,labels[0])
        #if toSave[1]==toSave[2]:
        #    if toSave[2] ==1:
        #        self.countisattack+=1
        #    self.countcorrect+=1
        #else:
        #    self.countwrong+=1
        #print(str(self.countwrong) +" "+ str(self.countcorrect) +" " +str(self.countisattack))
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
        #print(data[2:])
        np.save(trainingClasses[2],data)

    def createfilesToSaveTo(self):
        #for file in self.listOfPathToSilkFiles: 
        file = self.listOfPathToSilkFiles[0][0]#TODO This will no longer overwrite eachother, but will only work with one set of files
        nameoffile=file.split("/")[-1]
        for trainingClasses in self.dicOfFileOutput.values():
            trainingClasses[0].filepathOfInput="data/Classifiers/"+nameoffile+trainingClasses[0].name+".npy"
            #trainingClasses[0].setfilepathOfInput("data/Classifiers/"+nameoffile+trainingClasses[0].name+".npy")
            if len(trainingClasses)<=2:
                trainingClasses.append(open("data/Classifiers/"+nameoffile+trainingClasses[0].name+".npy", "wb"))
            else:
                trainingClasses[2]=open("data/Classifiers/"+nameoffile+trainingClasses[0].name+".npy", "wb")
            trainingClasses[0].filepathOfClassifier="data/Classifiers/"+nameoffile+trainingClasses[0].name+".pkl"

    def getDataFromSilkFile(self,detectortrain):
        for fileCollection in self.listOfPathToSilkFiles:
            for file in fileCollection:
                infile = silkfile_open(file, READ)
                self.setDataToZero()
                x=0
                for rec in infile:  #TODO Handle that when No rec are for a sliding window time
                    x+=1
                    for trainingClasses in self.dicOfFileOutput.values():
                        dataToHandle=[]
                        if trainingClasses[0].typeOfFeatures =="fields":
                            dataToHandle= self.createNetlfowFeilds(rec)
                        elif trainingClasses[0].typeOfFeatures in ["entropy","combined","threshold"]:
                            dataToHandle=self.createNetlfowEntropy(rec,trainingClasses[0])
                        #print(dataToHandle)
                        if detectortrain=="train" and len(dataToHandle)>0:
                            #print(dataToHandle)
                            if trainingClasses[0].typeOfFeatures =="fields":
                                #if dataToHandle[-1]==1:
                                #    print(x)
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
                infile.close()
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
            #print(x)
            
                

    def setIsAttack(self,rec):
        isAttackFlow=0
        #if rec.sensor=="isAttack": #TODO why does this not work
        #    isAttackFlow=1
        #if rec.sensor_id==3:
        if rec.sensor_id==32532:
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
    

RFF=RandomforestDetection("fields","","")
RFE=RandomforestDetection("entropy","","")
RFC=RandomforestDetection("combined","","")
TH=Threshold("threshold","","")
KMF=Kmeans("fields","","")
KME=Kmeans("entropy","","")
KMC=Kmeans("combined","","")

#a1=TraningOfClassification([RF],[["data/DiffrentSamplingRates/TCP_SYN_Flodd500"]])
#a1=TraningOfClassification([RF,EP],[["data/DiffrentSamplingRates/isattack100"]])

#a1=TraningOfClassification([TH],[["data/DiffrentSamplingRates/isattack100"]])
#a1=TraningOfClassification([RF],[["data/DiffrentSamplingRates/isattack100"]])
#a1=TraningOfClassification([CP],[["data/DiffrentSamplingRates/isattack100"]])
#a1=TraningOfClassification([KME],[["data/DiffrentSamplingRates/isattack100"]])

#a1=TraningOfClassification([RFF],[["data/DiffrentSamplingRates/TCP_SYN_Flodd01000"])

TH=Threshold("threshold","data/Classifiers/TCP_SYN_Flodd01000threshold.pkl",
                          "data/Classifiers/TCP_SYN_Flodd01000threshold.npy")
a1=TraningOfClassification([TH],[["data/DiffrentSamplingRates/TCP_SYN_Flodd01000"]])

#RFF=RandomforestDetection("fields","data/Classifiers/TCP_SYN_Flodd01000RandomForestfields.pkl",
#                          "data/Classifiers/TCP_SYN_Flodd01000RandomForestfields.npy")

#TH=Threshold("fields","data/Classifiers/TCP_SYN_Flodd01000threshold.pkl",
#                         "data/Classifiers/TCP_SYN_Flodd01000threshold.npy")

#a2=TraningOfClassification([TH],[["data/DiffrentSamplingRates/TCP_SYN_Flodd01000"]],)
#a2.detect()

#a1.appendTraingData()
#a1.makeTraingData()
#a1.train()
a1.detect()
#print(a1.countcorrect)
#print(a1.countwrong)