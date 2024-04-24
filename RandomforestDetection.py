from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle as pickle
import os
from Entropy import Entropy

class RandomforestDetection:
    def __init__(self,typeOfFeatures,filepathOfClassifier ="",filepathOfInput=""):#standertimes=[3,15,0]
        #TODO make standertimes to datetimedelta 
        #filepathOfInput might not be nessacary nor filepathOfClassifier
        self.checkTypeOfFeatures(typeOfFeatures)
        self.setname()
        self.clf = RandomForestClassifier(n_estimators = 100)
        self.filepathOfClassifier= filepathOfClassifier
        self.filepathOfInput=filepathOfInput
        #self.standertimes=standertimes
        if filepathOfClassifier !="":
            self.loadClassfication()

    #def resetentropy(self):
    #    self.entropy=Entropy(self.standertimes[0],self.standertimes[1],self.standertimes[2],False)    

    def checkTypeOfFeatures(self,typeOfFeatures):
        allowedtypeOfFeatures=["fields","entropy","combined","entropylimited","combinedlimited"]
        if typeOfFeatures not in allowedtypeOfFeatures:
            raise ValueError("no allowed type of training type")
        self.classifier="RandomForest"
        self.typeOfFeatures =typeOfFeatures
        
    def setname(self):
        self.name =self.classifier +self.typeOfFeatures

    def detect(self,arrayToDetect,isattack):
        return ["RandomForest",self.clf.predict(arrayToDetect)[0],isattack]

    def train(self):
    #def train(self,typeOfFeatures):
        #allowedtypeOfFeatures=["fields","entropy","combined"]
        #if typeOfFeatures not in allowedtypeOfFeatures:
        #    raise ValueError("no allowed type of training type")
        if self.filepathOfInput =="" or type(self.filepathOfInput)!=str:
            raise ValueError("no vaule input file for training")
        if not os.path.isfile(self.filepathOfInput):
            raise ValueError("no vaule input file for training")
        trainingSet=[]
        x=0
        with open(self.filepathOfInput, "rb") as fileOfFeatures:
            try:
                while True:
                    #print(trainingSet)
                    #print(fileOfFeatures)
                    data=np.load(fileOfFeatures, allow_pickle=True)
                    trainingSet.append(data)
                    x+=1
            #except EOFError:
            except (pickle.UnpicklingError, EOFError): #TODO This is not optimal, entropy and fleids create diffrent EOFError
                pass
            
            #trainingSet=np.load(fileOfFeatures, allow_pickle=True)
            #trainingSet=np.load(fileOfFeatures, allow_pickle=True)
        #print(trainingSet)
        #print(x)
        dataSet=np.array(trainingSet)
        Features=dataSet[:,2:-1]
        labels=dataSet[:,-1]
        #print(Features)
        labels=labels.astype('int') 
        #print(Features)
        #print(labels)
        #print(Features)
        self.clf=self.clf.fit(Features,labels)
        self.saveClassifier()

    def loadClassfication(self):
        self.clf= pickle.load(open(self.filepathOfClassifier, 'rb')) 

    def saveClassifier(self):
        pickle.dump(self.clf, open(self.filepathOfClassifier, 'wb'))
    
    def makecopy(self):
        randomforestDetection = RandomforestDetection(self.typeOfFeatures)
        randomforestDetection.filepathOfClassifier =self.filepathOfClassifier
        randomforestDetection.filepathOfInput = self.filepathOfInput
        randomforestDetection.clf =self.clf 
        return randomforestDetection