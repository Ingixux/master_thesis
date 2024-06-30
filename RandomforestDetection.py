from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle as pickle
import os
#from Entropy import Entropy

class RandomforestDetection:
    def __init__(self,typeOfFeatures,filepathOfClassifier ="",filepathOfInput=""):
        self.checkTypeOfFeatures(typeOfFeatures)
        self.setname()
        #self.clf = RandomForestClassifier(n_estimators = 100)
        self.clf = None
        self.filepathOfClassifier= filepathOfClassifier
        self.filepathOfInput=filepathOfInput
        #if filepathOfClassifier !="":
        #    self.loadClassfication()


    def setFilepathOfClassifier(self, path):
        self.filepathOfClassifier=path  

    def checkTypeOfFeatures(self,typeOfFeatures):
        allowedtypeOfFeatures=["fields","entropy","combined","entropylimited","combinedlimited"]
        if typeOfFeatures not in allowedtypeOfFeatures:
            raise ValueError("no allowed type of training type")
        self.classifier="RandomForest"
        self.typeOfFeatures =typeOfFeatures
        
    def setname(self):
        self.name =self.classifier +self.typeOfFeatures

    def detect(self,arrayToDetect,isattack):
        #print(arrayToDetect)
        return [self.clf.predict(arrayToDetect)[0],isattack]
        #return ["RandomForest",self.clf.predict(arrayToDetect)[0],isattack]

    def trainWithinput(self,trainingSet,labels):
        #dataSet=np.array(trainingSet)
        #dataSet=np.array(trainingSet,dtype=np.float32)
        #dataSet=np.array(trainingSet)
        if self.typeOfFeatures== "fields":
            dataSet=np.array(trainingSet,dtype=np.float32)
            Features=dataSet[:,:16]
        elif self.typeOfFeatures== "entropy":
            dataSet=np.array(trainingSet,dtype=object)
            Features=dataSet[:,:-1]
        else:
            dataSet=np.array(trainingSet,dtype=np.float32)
            #Features=dataSet[:,:-2]
            Features=dataSet[:,:]
        #Features=dataSet[:,2:-1]
        #labels=dataSet[:,-1]
        #print(Features)
        #labels=labels.astype('int') 
        #print(Features)
        #print(labels)
        #print(Features)
        self.clf = RandomForestClassifier(n_estimators = 100)
        self.clf=self.clf.fit(Features,labels)
        self.saveClassifier()
        self.clf=None

    def train(self):
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
        dataSet=np.array(trainingSet)
        #Features=dataSet[:,:-1]
        Features=dataSet[:,:-1]
        labels=dataSet[:,-1]
        #print(Features)
        labels=labels.astype('int') 

        self.clf=self.clf.fit(Features,labels)
        self.saveClassifier()

    def loadClassfication(self):
        self.clf= pickle.load(open(self.filepathOfClassifier, 'rb')) 

    def saveClassifier(self):
        pickle.dump(self.clf, open(self.filepathOfClassifier, 'wb'))
    
    def makecopy(self):
        randomforestDetection = RandomforestDetection(self.typeOfFeatures,filepathOfClassifier=self.filepathOfClassifier)
        #randomforestDetection.filepathOfClassifier =self.filepathOfClassifier
        randomforestDetection.filepathOfInput = self.filepathOfInput
        randomforestDetection.clf =self.clf 
        return randomforestDetection