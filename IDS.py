import numpy as np
import pickle as pickle
import os
from RandomforestDetection import RandomforestDetection
from Threshold import Threshold
from Kmeans import Kmeans
from silk import *
import datetime
from SlidingWindow import SlidingWindow
#import copy

class IDS:
    """
    This Class is used for both traning and classifying
    The input to this class is a list of TrainingClasses, 
    this is the different classifying class's, which currently is Kmeans, Threshold and RandomforestDetection
    Next is listOfPathToSilkFiles. One element is a list which with a collection of files. 
    One collection of files are considered on unit, when doing detection and traning
    Each first file of the collections need to have a unqiue path name. 
    It is also assumed that the files in the collection is arragned on time 
    and the earliset being the first (This only imporant when a silding window is used).
    Standertimes is the times of the sliding window. 
    self.dicOfFileOutput is a dictionary, which have all the combinations of files and classfiter class
    The key is the the name of the classifying class's and the path of the first file in the collection of files.
    There is one key/entry in self.dicOfFileOutput for each combinabtion of one collection of files and one classifying class
    The vaules of the keys is a list, where the first elemenet is a the classfiter class, 
    the second element is the path of the first file in the collection of files, which this uses as input,
    third is the element is the open file of the output is stored (either the traning file or the result file)
    self.dicOfSlidingWindow strores the slinding window 
    There is only one slinding window pr collection of files.
    If there are no classfiter class that uses a slinding window, then this dictionary is empty

    Methodes used for the outside
    addNewFiles:
        This changes the collection of files which are used as the input for the traning or detection
    makeTraingData:
        This moves through all the collection of files, and makes traning data file (in the .npy format), for each entry in self.dicOfFileOutput 
        this is the input used by the classifying class's under traning, this will overwirte old traning files
    removeTrainingFiles:
        This removes the traning files that where created under the traning prosses (the files created with makeTraingData or appendTraingData)
    appendTraingData:
        This appends data to a traning data (.npy file). This is used to add to files created with makeTraingData
    train:
        This calles the traning method of the classifying class's which uses a traning file (.npy format)
        This will create a classifier which is stored in a plk file format
    detect:
        This moves through all the collection of files, and calles the detect method of the classifying class's on each record in the files
        This saves the result of the cassifiing, in the format:
            name of method used, prediction result, label, which attack are present, time of the record
    """
    def __init__(self, listOfTrainingClasses,listOfPathToSilkFiles,standertimes=[120,600,1200]):#standertimes=[3,15,30]
        self.x=0
        self.listOfPathToSilkFiles=listOfPathToSilkFiles
        self.listOfTrainingClasses=listOfTrainingClasses
        self.dicOfFileOutput ={}
        self.dicOfSlidingWindow ={}
        self.standertimes=standertimes
        self.fileAggregatedData=None
        if not self.dicOfFileOutput:
            self.makeDicOfFileOutput()

    def addNewFiles(self, listOfPathToSilkFiles):
        self.listOfPathToSilkFiles=listOfPathToSilkFiles
        self.dicOfFileOutput ={}
        self.dicOfSlidingWindow ={}
        self.makeDicOfFileOutput()

    def removeTrainingFiles(self):
        for trainingClasses in self.dicOfFileOutput.values():
            if trainingClasses[0].name != "threshold":
                pathToFile=trainingClasses[0].filepathOfInput
                if os.path.isfile(pathToFile):
                    os.remove(pathToFile)
    
    def makeDicOfFileOutput(self):
        """
        This metode goes through the list of classifying class's 
        and adds the first file of each collections in listOfTrainingClassesas the key to self.dicOfFileOutput together with the name of classifying class's 
        To the key it addes a list with a copy of the classifying class's and the path of the first 
        This creates one key/entry in self.dicOfFileOutput for each combinabtion of one collection of files and one classifying class
        This also starts slidling windows if there the classifying class's uses this first file of the collection
        There is only one sliding window for each collection of files
        """
        for TrainingClasses in self.listOfTrainingClasses: #TODO TrainingClasses not the best name as this as a different source, from the other uses the name
            #mayby change all other insatnces of TrainingClasses to TrainingClassesset
            for fileCollection in self.listOfPathToSilkFiles:
                keyfile =fileCollection[0]
                if TrainingClasses.typeOfFeatures in ["entropy","combined","threshold"]:
                    if not keyfile in self.dicOfSlidingWindow.keys():
                        self.dicOfSlidingWindow[keyfile]=SlidingWindow(self.standertimes[0],self.standertimes[1],self.standertimes[2],False)
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
                if trainingClasses[0].name=="threshold" and self.fileAggregatedData ==None:
                    self.fileAggregatedData=open("data/Classifiers/result/fileAggregatedData.npy", "wb")

        
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

                    trainingClasses[0].setFilepathOfClassifier("data/Classifiers/"+nameoffile+trainingClasses[0].name+".pkl")
                    #trainingClasses[0].filepathOfClassifier="data/Classifiers/"+nameoffile+trainingClasses[0].name+".pkl"

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
            toSave=trainingClasses[0].detect(data,data["isAtttack"])
            attaks=data["isAtttack"]
            time=data["currenttime"]
        else:
            toPredict=[]
            if trainingClasses[0].typeOfFeatures =="entropy":
                label=self.setIsAttack(data[-1][0])
                attaks=data[-1]
            else:
                label=self.setIsAttack(data[-1])
                attaks=[data[-1]]
            time=data[0]
            toPredict.append(data)
            darecta=np.array(toPredict, dtype=object)

            Feature=darecta[:,2:-1]
            #labels=darecta[:,-1]
            self.x+=1
            toSave=trainingClasses[0].detect(Feature,label)
            #toSave=["RandomForest",1,labels[0]]
        toSave+=[attaks] +[time] 
        #print(toSave)
        self.saveDataToCollect(toSave,trainingClasses[2])

    def detect(self):
        self.createfilesForResult()
        self.getDataFromSilkFile("detect")
        for trainingClasses in self.dicOfFileOutput.values():
            self.closeFiles(trainingClasses[2])
        self.fileAggregatedData.close()
        self.fileAggregatedData ==None


    def train(self):
        for trainingClasses in self.dicOfFileOutput.values():
            trainingClasses[0].train()


    def saveAggregatedDatTofile(self,data):
        data["isAtttack"]=self.setIsAttack(data["isAtttack"][0])
        result = data.items()
        fdate= list(result)
        savedata=np.array(fdate, dtype=object)
        np.save(self.fileAggregatedData,savedata)



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
        if sensor_id in [32531,32532,32533,32534,32535,32536,32537,32538]:
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
                #
                for rec in infile:  #TODO Handle that when No rec are for a sliding window time
                    #self.x+=1
                    #TODO add to entropy here
                    slidingWindowVaules=[]
                    if keyfile in self.dicOfSlidingWindow.keys():
                    #if entrypy not empty:
                        
                        slidingWindowVaules =self.dicOfSlidingWindow[keyfile].addNewRec(rec)
                        #self.x+=len(slidingWindowVaules)
                    for trainingClasses in self.dicOfFileOutput.values():
                        if trainingClasses[1]==file:
                            dataToHandle=[]
                            if trainingClasses[0].typeOfFeatures =="fields":
                                dataToHandle= self.createNetlfowFeilds(rec)
                            elif trainingClasses[0].typeOfFeatures in ["entropy","combined","threshold"]:
                                #dataToHandle=self.createNetlfowEntropy(rec,trainingClasses[0])
                                dataToHandle=self.createNetlfowEntropy(slidingWindowVaules,trainingClasses[0],keyfile)
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
                                    self.saveDataTofile(file,self.dicOfSlidingWindow[keyfile].getcurrentvaules(),trainingClasses) 
                                    #self.saveDataTofile(file,trainingClasses[0].entropy.findThreasholds(False),trainingClasses) 
                            elif detectortrain=="detect" and len(dataToHandle)>0:
                                if trainingClasses[0].typeOfFeatures =="fields":
                                    self.doDetectionOnData(dataToHandle,trainingClasses)
                                elif trainingClasses[0].typeOfFeatures in ["entropy","combined"]:
                                    for rec1 in dataToHandle:
                                        self.doDetectionOnData(rec1,trainingClasses)
                                elif trainingClasses[0].typeOfFeatures in ["threshold"]:
                                    self.doDetectionOnData(self.dicOfSlidingWindow[keyfile].findThreasholds(False),trainingClasses)
                                    self.saveAggregatedDatTofile(self.dicOfSlidingWindow[keyfile].getcurrentvaules()) 
                infile.close()
            for trainingClasses in self.dicOfFileOutput.values(): #TODO this does only acuount for the vaules in [-1],needs to add the vaule to all in the rec
                if trainingClasses[0].typeOfFeatures in ["entropy","combined","threshold"]:
                    toadd=self.dicOfSlidingWindow[keyfile].doCalculation(True) #TODO change entropy  
                    if trainingClasses[0].typeOfFeatures =="threshold":
                        if detectortrain=="train":
                            self.saveDataTofile(file,self.dicOfSlidingWindow[keyfile].getcurrentvaules(),trainingClasses)
                            #self.saveDataTofile(file,trainingClasses[0].entropy.findThreasholds(True),trainingClasses)
                        elif detectortrain=="detect":
                            self.doDetectionOnData(self.dicOfSlidingWindow[keyfile].findThreasholds(True),trainingClasses)
                            self.saveAggregatedDatTofile(self.dicOfSlidingWindow[keyfile].getcurrentvaules())     
                    elif len(toadd) !=0:
                        #print(len(toadd))
                        if trainingClasses[0].typeOfFeatures =="entropy":
                            if detectortrain=="train":
                                #print([toadd[0][0:2]+toadd[0][19:32]+[toadd[0][-2]]])
                                #self.saveDataTofile(file,toadd[0][0:2]+toadd[0][19:32]+[toadd[0][-2]],trainingClasses)
                                self.saveDataTofile(file,toadd[0][0:2]+toadd[0][19:-2]+[toadd[0][-2]],trainingClasses)
                            elif detectortrain=="detect":
                                #self.doDetectionOnData(toadd[0][0:2]+toadd[0][19:32]+[toadd[0][-2]],trainingClasses)
                                self.doDetectionOnData(toadd[0][0:2]+toadd[0][19:-2]+[toadd[0][-2]],trainingClasses)
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
                #print(trainingClasses[0].x)
            if keyfile in self.dicOfSlidingWindow.keys():
                #print(self.dicOfSlidingWindow[keyfile].x)
                self.dicOfSlidingWindow[keyfile] = SlidingWindow(self.standertimes[0],self.standertimes[1],self.standertimes[2],False)
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
            if self.dicOfSlidingWindow[keyfile].checkwindowcomplet():
                if decttionclass.typeOfFeatures =="entropy": #TODO Should only one be added
                    #data.append(temor[0][0:2]+temor[0][19:32]+[temor[0][-2]])
                    for x in range(0,len(toadd)):
                        if toadd[x] == "window":
                            if x+1>=len(toadd):
                                pass
                            elif toadd[x+1] == "window" or len(toadd[x+1])==0:
                                    pass
                            else:
                                #data.append(toadd[x+1][0][0:2]+toadd[x+1][0][19:32]+[toadd[x+1][0][-2]])
                                data.append(toadd[x+1][0][0:2]+toadd[x+1][0][19:-2]+[toadd[x+1][0][-2]])
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

#a1=IDS([RF],[["data/DiffrentSamplingRates/TCP_SYN_Flodd500"]])
#a1=IDS([RF,EP],[["data/DiffrentSamplingRates/isattack100"]])

#a1=IDS([TH],[["data/DiffrentSamplingRates/isattack100"]])
#a1=IDS([RF],[["data/DiffrentSamplingRates/isattack100"]])
#a1=IDS([CP],[["data/DiffrentSamplingRates/isattack100"]])
#a1=IDS([KME],[["data/DiffrentSamplingRates/isattack100"]])

#a1=IDS([RFE],[["data/DiffrentSamplingRates/TCP_SYN_Flodd01000"]])
#a1=IDS([RFF],[["data/DiffrentSamplingRates/TCP_SYN_Flodd01000"]])

#TH=Threshold("threshold","data/Classifiers/TCP_SYN_Flodd01000threshold.pkl",
#                          "data/Classifiers/TCP_SYN_Flodd01000threshold.npy")

#KMFC=Kmeans("fields","","data/Classifiers/train800KMeansfields.npy")

#a1=IDS([TH,RFC],[["data/DiffrentSamplingRates/TCP_SYN_Flodd01000"]])
#a1=IDS([TH,RFF],[["data/DiffrentSamplingRates/TCP_SYN_Flodd01000"]])


#a2=IDS([TH],[["data/DiffrentSamplingRates/TCP_SYN_Flodd01000"]],)

#a1=IDS([RFE,RFC],[["data/DiffrentSamplingRates/TCP_SYN_Flodd01000"]])
#a1=IDS([RFE],[["data/DiffrentSamplingRates/TCP_SYN_Flodd01000"]])
#a1=IDS([RFE],[["data/DiffrentSamplingRates/train/train1000"]])


#a1.appendTraingData()
#a1.makeTraingData()
#a1.train()

#KMF=Kmeans("fields","","")
#TH=Threshold("threshold","","")
#RFE=RandomforestDetection("entropy","","")

#listofsmaplingrates =["800","1600"] #TODO add the new sampling rates
#listoffilestrain=[]
#listoffilesdetect=[]
#for smaplingrates in listofsmaplingrates:
#    listoffilestrain.append(["data/DiffrentSamplingRates/train/train"+smaplingrates])
#    listoffilesdetect.append(["data/DiffrentSamplingRates/detect/detect"+smaplingrates])

#a1=IDS([RFE,TH,KMF],listoffilestrain)
#a1.makeTraingData()
#a1.train()
#a1.removeTrainingFiles()
#a1.addNewFiles(listoffilesdetect)

#KMFC=Kmeans("fields","data/Classifiers/train1600KMeansfields.pkl","")
#RFEC=RandomforestDetection("entropy","data/Classifiers/train1600RandomForestentropy.pkl","")
#THC=Threshold("threshold","data/Classifiers/train1600threshold.pkl", "")
#a1=IDS([KMFC],[["data/DiffrentSamplingRates/detect/detect1600"]])
#a1=IDS([RFEC,THC],[["data/DiffrentSamplingRates/detect/detect800"]])
#a1.detect()
