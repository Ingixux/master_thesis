from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle as pickle
import os


class GeneralClassifier:
    def __init__(self,typeOfFeatures):
        #filepathOfInput might not be nessacary nor filepathOfClassifier
        self.checkTypeOfFeatures(typeOfFeatures)
        self.setname()
        self.filepathOfClassifier= 0
        self.filepathOfInput=0
        self.clf =0

    def detect(self,arrayToDetect):
        return self.clf.predict(arrayToDetect)

    def train(self):
    #def train(self,typeOfFeatures):
        #allowedtypeOfFeatures=["fields","entropy","combined"]
        #if typeOfFeatures not in allowedtypeOfFeatures:
        #    raise ValueError("no allowed type of training type")
        if self.filepathOfInput =="" or type(self.filepathOfInput)!=str:
            raise ValueError("no vaule input file for training")
        if not os.path.isfile(self.filepathOfInput):
            raise ValueError("no vaule input file for training")
        with open(self.filepathOfInput, "rb") as fileOfFeatures:
            trainingSet=np.load(fileOfFeatures, allow_pickle=True)
        Features=trainingSet[:,2:-1]
        labels=trainingSet[:,-1]

        labels=labels.astype('int') 
        #print(Features)
        #print(labels)
        self.clf=self.clf.fit(Features,labels)
        self.saveClassifier()

    def loadClassfication(self):
        self.clf= pickle.load(open(self.filepathOfClassifier, 'rb')) 

    def saveClassifier(self):
        pickle.dump(self.clf, open(self.filepathOfClassifier, 'wb'))