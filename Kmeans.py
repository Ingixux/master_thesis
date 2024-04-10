from sklearn.cluster import KMeans
import numpy as np
import pickle as pickle
import os
from Entropy import Entropy

class Kmeans:
    def __init__(self,typeOfFeatures,filepathOfClassifier ="",filepathOfInput="",standertimes=[3,15,0]):
        #TODO make standertimes to datetimedelta 
        #filepathOfInput might not be nessacary nor filepathOfClassifier
        self.checkTypeOfFeatures(typeOfFeatures)
        self.setname()
        self.clf = KMeans(n_clusters = 2)
        self.filepathOfClassifier= filepathOfClassifier
        self.filepathOfInput=filepathOfInput
        self.standertimes=standertimes
        if filepathOfClassifier !="":
            self.loadClassfication()

#    def resetentropy(self):
#        self.entropy=Entropy(self.standertimes[0],self.standertimes[1],self.standertimes[2],False)    

    def checkTypeOfFeatures(self,typeOfFeatures):
        allowedtypeOfFeatures=["fields","entropy","combined","entropylimited","combinedlimited"]
        if typeOfFeatures not in allowedtypeOfFeatures:
            raise ValueError("no allowed type of training type")
        self.classifier="KMeans"
        self.typeOfFeatures =typeOfFeatures
        
    def setname(self):
        self.name =self.classifier +self.typeOfFeatures

    def detect(self,arrayToDetect,isattack):
        prediction=self.findattackcluster(self.clf.predict(arrayToDetect)[0])
        return ["KMeans",prediction,isattack]
    
    #def setfilepathOfInput(self,file):
    #    if os.path.isfile(file):
    #        os.remove(file)
    #    self.filepathOfInput=file

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
        #with open(self.filepathOfInput, "rb") as fileOfFeatures:
        #    trainingSet=np.load(fileOfFeatures, allow_pickle=True)
        #"""
        with open(self.filepathOfInput, "rb") as fileOfFeatures: #TODO bug!!!: does not load the same number of array that gets saved
            try:
                while True:
                    #print(trainingSet)
                    #print(fileOfFeatures)
                    data=np.load(fileOfFeatures, allow_pickle=True)
                    trainingSet.append(data)
            #except EOFError:
            except (EOFError): #EOFError
            #except (pickle.UnpicklingError, EOFError): #TODO This is not optimal, entropy and fleids create diffrent EOFError
                pass
        #"""
            #trainingSet=np.load(fileOfFeatures, allow_pickle=True)
            #trainingSet=np.load(fileOfFeatures, allow_pickle=True)
        trainingSet=np.array(trainingSet)
        #print(trainingSet[:,2:])
        Features=trainingSet[:,2:-1]
        #labels=trainingSet[:,-1]

        #labels=labels.astype('int') 
        #print(Features)
        #print(labels)
        #print(Features)
        #self.clf=self.clf.fit(Features,labels)
        self.clf=self.clf.fit(Features)
        self.makeattackcluster(trainingSet)
        self.saveClassifier()

    def loadClassfication(self):
        self.clf= pickle.load(open(self.filepathOfClassifier, 'rb')) 

    def saveClassifier(self):
        pickle.dump(self.clf, open(self.filepathOfClassifier, 'wb'))

    def makeattackcluster(self,dataset):
        #print(dataset)
        Features=dataset[:,2:-1]
        predictions=self.clf.predict(Features)
        lables=dataset[:,-1]
        correct=0
        for x in range(0,len(lables)):
            if lables[x]==predictions[x]:
                correct+=1
        if correct/len(lables) >0.5:
            self.flib=0
        else:
            self.flib=1
        print(dataset[:,-1])
        print(len(lables))
        print(correct)
        print(correct/len(lables))
        print(predictions)
        #print("hei")
        
    def findattackcluster(self,prediction):
        if self.flib==1:
            if prediction==1:
                return 0
            else:
                return 1
        else:
            return prediction
        
    def makecopy(self):
        kmeans = Kmeans(self.typeOfFeatures)
        kmeans.filepathOfClassifier =self.filepathOfClassifier
        kmeans.filepathOfInput = self.filepathOfInput
        kmeans.clf =self.clf 
        return kmeans