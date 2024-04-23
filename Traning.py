import numpy as np
import pickle as pickle
import os
#from RandomforestDetection import RandomforestDetection
#from Threshold import Threshold
#from Kmeans import Kmeans
from silk import *
import datetime
from Entropy import Entropy
#import copy

class TraningOfClassification:
    #TODO decide who I want to handle training and testing from same file adn diffrentfiles
    """
    This Class can handle file for the classifers, but it will be the same classifer vaules for all the file
    """
    def __init__(self, listOfTrainingClasses,listOfPathToSilkFiles,standertimes=[3,15,30]):
        
        #self.listOfTrainingClasses=listOfTrainingClasses
        self.countcorrect=0
        self.countwrong=0
        self.countisattack=0
        self.listOfPathToSilkFiles=listOfPathToSilkFiles
        self.listOfTrainingClasses=listOfTrainingClasses
        self.dicOfFileOutput ={}
        self.dicOfEntropy ={}
        self.standertimes=standertimes
        if not self.dicOfFileOutput:
            self.makeDicOfFileOutput()

    def addNewFiles(self, listOfPathToSilkFiles):
        self.listOfPathToSilkFiles=listOfPathToSilkFiles
        self.dicOfFileOutput ={}
        self.dicOfEntropy ={}
        self.makeDicOfFileOutput()

    def removeTrainingFiles(self):
        for trainingClasses in self.dicOfFileOutput.values():
            pathToFile=trainingClasses[0].filepathOfInput
            if os.path.isfile(pathToFile):
                os.remove(pathToFile)
    
    def makeDicOfFileOutput(self):
        for TrainingClasses in self.listOfTrainingClasses:
            for fileCollection in self.listOfPathToSilkFiles:
                keyfile =fileCollection[0]
                if TrainingClasses.typeOfFeatures in ["entropy","combined","threshold"]:
                    if not keyfile in self.dicOfEntropy.keys():
                        self.dicOfEntropy[keyfile]=Entropy(self.standertimes[0],self.standertimes[1],self.standertimes[2],False)
                self.dicOfFileOutput[TrainingClasses.name+keyfile]= [TrainingClasses.makecopy(),keyfile]

    def createfilesForResult(self):
        for fileCollection in self.listOfPathToSilkFiles:
            file =fileCollection[0]
            nameoffile=file.split("/")[-1]
            for trainingClasses in self.dicOfFileOutput.values():
                if trainingClasses[1]==file:
                    if len(trainingClasses)<=2:
                        trainingClasses.append(open("data/Classifiers/result/"+nameoffile+trainingClasses[0].name+".npy", "wb"))
                    else:
                        trainingClasses[2]=open("data/Classifiers/result/"+nameoffile+trainingClasses[0].name+".npy", "wb")


    def createfilesToSaveTo(self):
        #for file in self.listOfPathToSilkFiles: 
        for fileCollection in self.listOfPathToSilkFiles:
            file =fileCollection[0]   #TODO This will no longer overwrite eachother, but will only work with one set of files
            #file = self.listOfPathToSilkFiles[0][0]
            nameoffile=file.split("/")[-1]
            for trainingClasses in self.dicOfFileOutput.values():
                if trainingClasses[1]==file:
                    trainingClasses[0].filepathOfInput="data/Classifiers/"+nameoffile+trainingClasses[0].name+".npy"
                    #trainingClasses[0].setfilepathOfInput("data/Classifiers/"+nameoffile+trainingClasses[0].name+".npy")
                    if len(trainingClasses)<=2:
                        trainingClasses.append(open("data/Classifiers/"+nameoffile+trainingClasses[0].name+".npy", "wb"))
                    else:
                        trainingClasses[2]=open("data/Classifiers/"+nameoffile+trainingClasses[0].name+".npy", "wb")
                    trainingClasses[0].filepathOfClassifier="data/Classifiers/"+nameoffile+trainingClasses[0].name+".pkl"

    def makeTraingData(self):
        self.createfilesToSaveTo()
        self.getDataFromSilkFile("train")
        for trainingClasses in self.dicOfFileOutput.values():
            self.closeFiles(trainingClasses[2])
            
    def closeFiles(self, fileToClose):
        fileToClose.close()

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
        for trainingClasses in self.dicOfFileOutput.values():
            self.closeFiles(trainingClasses[2])

    def doDetectionOnData(self,data,trainingClasses):
        toSave=[]
        if trainingClasses[0].typeOfFeatures =="threshold":
            data["isAtttack"]=self.setIsAttack(data["isAtttack"][0])
            toSave=trainingClasses[0].detect(data,data["isAtttack"])#TODO add the isattack feature
            attaks=data["isAtttack"]
            #for x in toSave:
            #    if x[1]==x[2]:
            #        self.countcorrect+=1
            #    else:
            #        self.countwrong+=1
        else:
            toPredict=[]
            if trainingClasses[0].typeOfFeatures =="entropy":
                label=self.setIsAttack(data[-1][0])
                attaks=data[-1]
            else:
                label=self.setIsAttack(data[-1])
                attaks=[data[-1]]
            toPredict.append(data)
            darecta=np.array(toPredict, dtype=object)

            Feature=darecta[:,2:-1]
            #labels=darecta[:,-1]
            toSave=trainingClasses[0].detect(Feature,label)
            #toSave=["RandomForest",1,labels[0]]
        toSave+=[attaks]
        #if toSave[1]==toSave[2]:
        #    self.countcorrect+=1
        #else:
        #    self.countwrong+=1
        #if toSave[2] ==1:
        #    self.countisattack+=1


        self.saveDataToCollect(toSave,trainingClasses[2])
        #print(str(self.countwrong) +" "+ str(self.countcorrect) +" " +str(self.countisattack))
        #TODO save toSave in a file, used sensor_id to get the attack it detected

    def detect(self):
        self.createfilesForResult()
        self.getDataFromSilkFile("detect")
        for trainingClasses in self.dicOfFileOutput.values():
            self.closeFiles(trainingClasses[2])

    def train(self):
        for trainingClasses in self.dicOfFileOutput.values():
            trainingClasses[0].train()


    def saveDataTofile(self,file,data,trainingClasses):
        
        if trainingClasses[0].typeOfFeatures =="threshold":
            data["isAtttack"]=self.setIsAttack(data["isAtttack"][0])
            result = data.items()
            fdate= list(result)
            savedata=np.array(fdate, dtype=object)
        elif trainingClasses[0].typeOfFeatures in ["combined","fields"]:
            data[-1]=self.setIsAttack(data[-1])
            savedata=np.array(data, dtype=object)
        else:
            #print(data)
            data[-1]=self.setIsAttack(data[-1][0])
            savedata=np.array(data, dtype=object)
        #print(savedata)
        #savedata=np.array(data, dtype=object)
        #print(data[2:])
        #TODO add time and which sensor 
        np.save(trainingClasses[2],savedata)

    def setIsAttack(self,sensor_id):
        isAttackFlow=0
        #if rec.sensor=="isAttack": #TODO why does this not work
        #    isAttackFlow=1
        #if rec.sensor_id==3:
        if sensor_id==32532:
            isAttackFlow=1
        return isAttackFlow


    def saveDataToCollect(self,toSave,file):
        savedata=np.array(toSave, dtype=object)
        np.save(file,savedata)


    def getDataFromSilkFile(self,detectortrain):
        for fileCollection in self.listOfPathToSilkFiles:
            keyfile =fileCollection[0]
            for file in fileCollection:
                infile = silkfile_open(file, READ)
                #self.setDataToZero()
                self.x=0
                for rec in infile:  #TODO Handle that when No rec are for a sliding window time
                    
                    #TODO add to entropy here
                    entropyVaules=[]
                    if keyfile in self.dicOfEntropy.keys():
                    #if entrypy not empty:
                        
                        entropyVaules =self.dicOfEntropy[keyfile].addNewRec(rec)
                        #self.x+=len(entropyVaules)
                    for trainingClasses in self.dicOfFileOutput.values():
                        if trainingClasses[1]==file:
                            dataToHandle=[]
                            if trainingClasses[0].typeOfFeatures =="fields":
                                dataToHandle= self.createNetlfowFeilds(rec)
                            elif trainingClasses[0].typeOfFeatures in ["entropy","combined","threshold"]:
                                #dataToHandle=self.createNetlfowEntropy(rec,trainingClasses[0])
                                dataToHandle=self.createNetlfowEntropy(entropyVaules,trainingClasses[0],keyfile)
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
                                    self.saveDataTofile(file,self.dicOfEntropy[keyfile].getcurrentvaules(),trainingClasses) 
                                    #self.saveDataTofile(file,trainingClasses[0].entropy.findThreasholds(False),trainingClasses) 
                            elif detectortrain=="detect" and len(dataToHandle)>0:
                                if trainingClasses[0].typeOfFeatures =="fields":
                                    self.doDetectionOnData(dataToHandle,trainingClasses)
                                elif trainingClasses[0].typeOfFeatures in ["entropy","combined"]:
                                    for rec1 in dataToHandle:
                                        self.doDetectionOnData(rec1,trainingClasses)
                                elif trainingClasses[0].typeOfFeatures in ["threshold"]:
                                    self.doDetectionOnData(self.dicOfEntropy[keyfile].findThreasholds(False),trainingClasses)
                infile.close()
            for trainingClasses in self.dicOfFileOutput.values(): #TODO this does only acuount for the vaules in [-1],needs to add the vaule to all in the rec
                if trainingClasses[0].typeOfFeatures in ["entropy","combined","threshold"]:
                    toadd=self.dicOfEntropy[keyfile].doCalculation(True) #TODO change entropy
                    if trainingClasses[0].typeOfFeatures =="threshold":
                        if detectortrain=="train":
                            self.saveDataTofile(file,self.dicOfEntropy[keyfile].getcurrentvaules(),trainingClasses)
                            #self.saveDataTofile(file,trainingClasses[0].entropy.findThreasholds(True),trainingClasses)
                        elif detectortrain=="detect":
                            self.doDetectionOnData(self.dicOfEntropy[keyfile].findThreasholds(True),trainingClasses)
                    elif len(toadd) !=0:
                        #print(len(toadd))
                        if trainingClasses[0].typeOfFeatures =="entropy":
                            if detectortrain=="train":
                                #print([toadd[0][0:2]+toadd[0][19:32]+[toadd[0][-2]]])
                                self.saveDataTofile(file,toadd[0][0:2]+toadd[0][19:32]+[toadd[0][-2]],trainingClasses)
                            elif detectortrain=="detect":
                                self.doDetectionOnData(toadd[0][0:2]+toadd[0][19:32]+[toadd[0][-2]],trainingClasses)
                        else:
                            for r in toadd:
                                #tempr=[]
                                #tempr.append(r[0:32]+[r[-1]]) 

                                if detectortrain=="train":
                                    #self.saveDataTofile(file,[r[0:32]+[r[-1]]],trainingClasses)
                                    self.saveDataTofile(file,r[0:-2]+[r[-1]],trainingClasses)
                                elif detectortrain=="detect":
                                    #self.doDetectionOnData([r[0:32]+[r[-1]]],trainingClasses)
                                    self.doDetectionOnData(r[0:-2]+[r[-1]],trainingClasses)
            if keyfile in self.dicOfEntropy.keys():
                #print(self.dicOfEntropy[keyfile].x)
                self.dicOfEntropy[keyfile] = Entropy(self.standertimes[0],self.standertimes[1],self.standertimes[2],False)
            #entropy.resetentropy()
            #print(self.x)



    #def setDataToZero(self):
    #    for trainingClasses in self.dicOfFileOutput.values():
    #        trainingClasses[1]=[]

    def createNetlfowFeilds(self,rec):
        #li=[rec.sport, rec.dport, rec.protocol, rec.packets, rec.bytes, 
        #                    int(rec.tcpflags.fin), int(rec.tcpflags.syn), int(rec.tcpflags.rst), int(rec.tcpflags.psh), int(rec.tcpflags.ack), 
        #                    int(rec.tcpflags.urg), int(rec.tcpflags.ece), int(rec.tcpflags.cwr), rec.duration/datetime.timedelta(milliseconds=1)]
        #for x in (0,len(li)):
        #    data.append(li[x])
        data=[rec.stime, rec.etime, int(rec.sip), int(rec.dip), rec.sport, rec.dport, rec.protocol, rec.packets, rec.bytes, 
                            int(rec.tcpflags.fin), int(rec.tcpflags.syn), int(rec.tcpflags.rst), int(rec.tcpflags.psh), int(rec.tcpflags.ack),int(rec.nhip), 
                            int(rec.tcpflags.urg), int(rec.tcpflags.ece), int(rec.tcpflags.cwr), rec.duration/datetime.timedelta(milliseconds=1), 
                            rec.sensor_id]
        return data
    """
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
    """
    def createNetlfowEntropy(self,toadd,decttionclass,keyfile):
        data =[]
        if len(toadd) !=0:
            if self.dicOfEntropy[keyfile].checkwindowcomplet():
                if decttionclass.typeOfFeatures =="entropy": #TODO Should only one be added
                    #data.append(temor[0][0:2]+temor[0][19:32]+[temor[0][-2]])
                    for x in range(0,len(toadd)):
                        if toadd[x] == "window":
                            if x+1>=len(toadd):
                                pass
                            elif toadd[x+1] == "window" or len(toadd[x+1])==0:
                                    pass
                            else:
                                data.append(toadd[x+1][0][0:2]+toadd[x+1][0][19:32]+[toadd[x+1][0][-2]])
                    #if (len(toadd[0]) > 2):
                    #    for x in range(0,len(toadd[0])):
                    #        if toadd[x] == "window":
                    #            if x+1>=len(toadd):
                    #                pass
                    #            elif toadd[x+1] == "window" or len(toadd[x+1])==0:
                    #                pass
                    #            else:
                    #                data.append(toadd[x+1][0][0:2]+toadd[x+1][0][19:32]+[toadd[x+1][0][-2]])
                    #else:
                    #    if len(toadd[0]) !=0:
                    #        data.append(toadd[0][0][0:2]+toadd[0][0][19:32]+[toadd[0][0][-2]])
                            #if temor[0][-2][0] !=0:
                            #    print(temor[0][-2][0])
                            #data.append(temor[0][0:2]+temor[0][19:32]+[temor[0][-2]])
                else:
                    for temor in toadd:
                        if len(temor)!=0 and temor!="window":
                            for r in temor:
                            #if decttionclass.typeOfFeatures =="entropy": #TODO Should only one be added
                                #tempr=r[0:2]+r[19:]+r[-1]
                                #data.append(tempr)
                                
                                #if (r[-1] ==1):
                                #    print("he")
                            #elif decttionclass.typeOfFeatures =="threshold":
                                #data.append(r[0:2]+r[20:])
                            
                                #data.append(r[0:32]+[r[-1]])
                                data.append(r[0:-2]+[r[-1]])
        return data
        
    

#RFF=RandomforestDetection("fields","","")
#RFE=RandomforestDetection("entropy","","")
#RFC=RandomforestDetection("combined","","")
#TH=Threshold("threshold","","")
#KMF=Kmeans("fields","","")
#KME=Kmeans("entropy","","")
#KMC=Kmeans("combined","","")

#a1=TraningOfClassification([RF],[["data/DiffrentSamplingRates/TCP_SYN_Flodd500"]])
#a1=TraningOfClassification([RF,EP],[["data/DiffrentSamplingRates/isattack100"]])

#a1=TraningOfClassification([TH],[["data/DiffrentSamplingRates/isattack100"]])
#a1=TraningOfClassification([RF],[["data/DiffrentSamplingRates/isattack100"]])
#a1=TraningOfClassification([CP],[["data/DiffrentSamplingRates/isattack100"]])
#a1=TraningOfClassification([KME],[["data/DiffrentSamplingRates/isattack100"]])

#a1=TraningOfClassification([RFE],[["data/DiffrentSamplingRates/TCP_SYN_Flodd01000"]])
#a1=TraningOfClassification([RFF],[["data/DiffrentSamplingRates/TCP_SYN_Flodd01000"]])

#TH=Threshold("threshold","data/Classifiers/TCP_SYN_Flodd01000threshold.pkl",
#                          "data/Classifiers/TCP_SYN_Flodd01000threshold.npy")

#a1=TraningOfClassification([TH,RFC],[["data/DiffrentSamplingRates/TCP_SYN_Flodd01000"]])
#a1=TraningOfClassification([TH,RFF],[["data/DiffrentSamplingRates/TCP_SYN_Flodd01000"]])
#RFFC=RandomforestDetection("fields","data/Classifiers/TCP_SYN_Flodd01000RandomForestfields.pkl",
#                          "data/Classifiers/TCP_SYN_Flodd01000RandomForestfields.npy")

#RFEC=RandomforestDetection("entropy","data/Classifiers/TCP_SYN_Flodd01000RandomForestentropy.pkl",
#                          "data/Classifiers/TCP_SYN_Flodd01000RandomForestentropy.npy")

#TH=Threshold("fields","data/Classifiers/TCP_SYN_Flodd01000threshold.pkl",
#                         "data/Classifiers/TCP_SYN_Flodd01000threshold.npy")

#a2=TraningOfClassification([TH],[["data/DiffrentSamplingRates/TCP_SYN_Flodd01000"]],)

#a1=TraningOfClassification([RFE,RFC],[["data/DiffrentSamplingRates/TCP_SYN_Flodd01000"]])
#a1=TraningOfClassification([RFE],[["data/DiffrentSamplingRates/TCP_SYN_Flodd01000"]])
#a1=TraningOfClassification([RFE],[["data/DiffrentSamplingRates/train/train1000"]])

#a1.appendTraingData()
#a1.makeTraingData()
#a1.train()
#a1.detect()
#print(a1.countcorrect)
#print(a1.countwrong)
#print(a1.countisattack)