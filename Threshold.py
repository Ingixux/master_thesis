from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle as pickle
import os
from Entropy import Entropy

class Threshold:
    def __init__(self,typeOfFeatures="threshold",filepathOfClassifier ="",filepathOfInput="",standertimes=[3,15,30]):
        #TODO make standertimes to datetimedelta 
        #filepathOfInput might not be nessacary nor filepathOfClassifier
        self.checkTypeOfFeatures(typeOfFeatures)
        self.setname()
        self.threshold ={"entropySip":0,"entropyRateSip":0,"entropyDip":0,"entropyRateDip":0,"entropyPacketsize":0,"entropyRatePacketsize":0,
                                           "entropyBiflowSyn":0,"entropySipSyn":0,"entropyDipSyn":0,"entropyBiflow":0,"entropyRateBiflow":0,
                                           "HigstNumberOfSyn":0,"HigstNumberOfURGPSHFIN":0,"countBiflow":0,"totalicmpDUnreachable":0,
                                           "totalBytes":0,"totalpackets":0,"totalicmp":0,"totalicmprate":0}
        self.filepathOfClassifier= filepathOfClassifier
        self.filepathOfInput=filepathOfInput
        self.standertimes=standertimes

        self.entropy=Entropy(self.standertimes[0],self.standertimes[1],self.standertimes[2],False)       
        #self.sliding_window=Entropy(self.standertimes[0],self.standertimes[1],self.standertimes[2],False)

    def resetentropy(self):
        self.entropy=Entropy(self.standertimes[0],self.standertimes[1],self.standertimes[2],False)  
        #self.sliding_window=Entropy(self.standertimes[0],self.standertimes[1],self.standertimes[2],False)  


    def checkTypeOfFeatures(self,typeOfFeatures):
        allowedtypeOfFeatures=["threshold"]
        if typeOfFeatures not in allowedtypeOfFeatures:
            raise ValueError("no allowed type of training type")
        self.classifier=""
        self.typeOfFeatures =typeOfFeatures
        
    def setname(self):
        self.name =self.classifier +self.typeOfFeatures

    def detect(self,arrayToDetect):
        #TODO compare the threadshold with the findThreadshold vaules from the Entropy Class, put all the result in a list/dict 
        dataToSave=[]
        isattck=0
        for key in self.threshold.keys():
            if self.threshold[key] <  arrayToDetect[key]:
                dataToSave.append([key,1,isattck])#how to get if there is and attack
            else:
                dataToSave.append([key,0,isattck])
        return 0

    def train(self):
        if self.filepathOfInput =="" or type(self.filepathOfInput)!=str:
            raise ValueError("no vaule input file for training")
        if not os.path.isfile(self.filepathOfInput):
            raise ValueError("no vaule input file for training")
        trainingSet=[]
        with open(self.filepathOfInput, "rb") as fileOfFeatures:
            try:
                while True:
                    #print(trainingSet)
                    #print(fileOfFeatures)
                    data=np.load(fileOfFeatures, allow_pickle=True)
                    trainingSet.append(data)
            #except EOFError:
            except (pickle.UnpicklingError, EOFError): #TODO This is not optimal, entropy and fleids create diffrent EOFError
                pass

        trainingSet=np.array(trainingSet)
        #print(trainingSet)
        for rec in trainingSet:
            temprec=dict(rec)
            #TODO create the the array or something else
            #print(temprec)
        self.threshold =temprec
        self.saveClassifier()
        #TODO open the file with all past threashold and find the avagre

    def loadClassfication(self):
        #self.clf= pickle.load(open(self.filepathOfClassifier, 'rb')) 
        self.threshold= pickle.load(open(self.filepathOfClassifier, 'rb')) 
        pass

        
        #TODO load the threashold from file

    def saveClassifier(self):
        pickle.dump(self.threshold, open(self.filepathOfClassifier, 'wb'))
        pass
        #TODO save the threashold thrashold