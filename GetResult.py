import pickle as pickle
import numpy as np
import csv


trainingSet=[]
x=0

def readandgetresultnormal(file):
    attacks={"slowread":{"Attackcorrect":0,"Attackwrong":0},
         "slowloris":{"Attackcorrect":0,"Attackwrong":0},
         "ruby":{"Attackcorrect":0,"Attackwrong":0},
         "pingflood":{"Attackcorrect":0,"Attackwrong":0},
         "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
         "xmas":{"Attackcorrect":0,"Attackwrong":0},
         "udpflood":{"Attackcorrect":0,"Attackwrong":0},
         "synflood":{"Attackcorrect":0,"Attackwrong":0}}
    Attackcorrect=0
    Attackwrong=0
    normalcorrect=0
    normalwrong=0
    #dataSet, total= readresult(file)
    with open(file, "rb") as fileOfFeatures:
        try:
            while True:
                element=np.load(fileOfFeatures, allow_pickle=True)
                #element=np.array(trainingSet)
                #print(element)
                #for element in dataSet:
                    #
                    #if element[2][0] in [32531,32532,32533,32534,32535,32536,32537,32538]:
                        #print(element[2])
                if element[0]==element[1]:
                    if element[1]==1:
                        if element[2][0] == 32533:
                            attacks["slowread"]["Attackcorrect"]+=1
                        elif element[2][0] == 32534:
                            attacks["slowloris"]["Attackcorrect"]+=1
                        elif element[2][0] == 32535:
                            attacks["ruby"]["Attackcorrect"]+=1
                        elif element[2][0] == 32531:
                            attacks["pingflood"]["Attackcorrect"]+=1
                        elif element[2][0] == 32532:
                            attacks["blacknurse"]["Attackcorrect"]+=1
                        elif element[2][0] == 32536:
                            attacks["xmas"]["Attackcorrect"]+=1
                        elif element[2][0] == 32537:
                            attacks["udpflood"]["Attackcorrect"]+=1
                        elif element[2][0] == 32538:
                            attacks["synflood"]["Attackcorrect"]+=1
                        Attackcorrect+=1
                    else:
                        normalcorrect+=1
                else:
                    if element[1]==1:
                        if element[2][0] == 32533:
                            attacks["slowread"]["Attackwrong"]+=1
                        elif element[2][0] == 32534:
                            attacks["slowloris"]["Attackwrong"]+=1
                        elif element[2][0] == 32535:
                            attacks["ruby"]["Attackwrong"]+=1
                        elif element[2][0] == 32531:
                            attacks["pingflood"]["Attackwrong"]+=1
                        elif element[2][0] == 32532:
                            attacks["blacknurse"]["Attackwrong"]+=1
                        elif element[2][0] == 32536:
                            attacks["xmas"]["Attackwrong"]+=1
                        elif element[2][0] == 32537:
                            attacks["udpflood"]["Attackwrong"]+=1
                        elif element[2][0] == 32538:
                            attacks["synflood"]["Attackwrong"]+=1
                        Attackwrong+=1
                    else:
                        normalwrong+=1
        except (pickle.UnpicklingError, EOFError): #TODO This is not optimal, entropy and fleids create diffrent EOFError
            pass

    return {"Attackcorrect":Attackcorrect,"normalcorrect":normalcorrect,"Attackwrong":Attackwrong,"normalwrong":normalwrong,"attacks":attacks}
    colume1=[Attackcorrect,normalcorrect,Attackwrong,normalwrong]
    print("correct")
    print(Attackcorrect)
    print(normalcorrect)

    print("wrong")
    print(Attackwrong)
    print(normalwrong)
    print("accaury")
    print((Attackcorrect+normalcorrect)/total)
    print()


def readandgetresultthreshold(file):
    dataSet,total= readresult(file)
    threshold ={"entropySip":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "entropyRateSip":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "entropyDip":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "entropyRateDip":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "entropyPacketsize":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                    "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "entropyRatePacketsize":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "entropyBiflowSyn":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "entropySipSyn":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "entropyDipSyn":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "entropyBiflow":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "entropyRateBiflow":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "HigstNumberOfSyn":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "HigstNumberOfURGPSHFIN":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "countBiflow":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "totalicmpDUnreachable":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "totalBytes":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "totalpackets":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "totalicmp":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "totalicmprate":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}},
                "totalflows":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0,
                "attacks":{"slowread":{"Attackcorrect":0,"Attackwrong":0},
                            "slowloris":{"Attackcorrect":0,"Attackwrong":0},
                            "ruby":{"Attackcorrect":0,"Attackwrong":0},
                            "pingflood":{"Attackcorrect":0,"Attackwrong":0},
                            "blacknurse":{"Attackcorrect":0,"Attackwrong":0},
                            "xmas":{"Attackcorrect":0,"Attackwrong":0},
                            "udpflood":{"Attackcorrect":0,"Attackwrong":0},
                            "synflood":{"Attackcorrect":0,"Attackwrong":0}}}}

    #for element in dataSet:
    with open(file, "rb") as fileOfFeatures:
        try:
            while True:
                element=np.load(fileOfFeatures, allow_pickle=True)
                for key in element[0]:
                    if key[1]==element[1]:
                        if element[1]==1:
                            threshold[key[0]]["Attackcorrect"]+=1
                            if element[2][0] == 32533:
                                threshold[key[0]]["attacks"]["slowread"]["Attackcorrect"]+=1
                            elif element[2][0] == 32534:
                                threshold[key[0]]["attacks"]["slowloris"]["Attackcorrect"]+=1
                            elif element[2][0] == 32535:
                                threshold[key[0]]["attacks"]["ruby"]["Attackcorrect"]+=1
                            elif element[2][0] == 32531:
                                threshold[key[0]]["attacks"]["pingflood"]["Attackcorrect"]+=1
                            elif element[2][0] == 32532:
                                threshold[key[0]]["attacks"]["blacknurse"]["Attackcorrect"]+=1
                            elif element[2][0] == 32536:
                                threshold[key[0]]["attacks"]["xmas"]["Attackcorrect"]+=1
                            elif element[2][0] == 32537:
                                threshold[key[0]]["attacks"]["udpflood"]["Attackcorrect"]+=1
                            elif element[2][0] == 32538:
                                threshold[key[0]]["attacks"]["synflood"]["Attackcorrect"]+=1
                        else:
                            threshold[key[0]]["normalcorrect"]+=1
                    else:
                        if element[1]==1:
                            threshold[key[0]]["Attackwrong"]+=1
                            if element[2][0] == 32533:
                                threshold[key[0]]["attacks"]["slowread"]["Attackwrong"]+=1
                            elif element[2][0] == 32534:
                                threshold[key[0]]["attacks"]["slowloris"]["Attackwrong"]+=1
                            elif element[2][0] == 32535:
                                threshold[key[0]]["attacks"]["ruby"]["Attackwrong"]+=1
                            elif element[2][0] == 32531:
                                threshold[key[0]]["attacks"]["pingflood"]["Attackwrong"]+=1
                            elif element[2][0] == 32532:
                                threshold[key[0]]["attacks"]["blacknurse"]["Attackwrong"]+=1
                            elif element[2][0] == 32536:
                                threshold[key[0]]["attacks"]["xmas"]["Attackwrong"]+=1
                            elif element[2][0] == 32537:
                                threshold[key[0]]["attacks"]["udpflood"]["Attackwrong"]+=1
                            elif element[2][0] == 32538:
                                threshold[key[0]]["attacks"]["synflood"]["Attackwrong"]+=1
                        else:
                            threshold[key[0]]["normalwrong"]+=1
        except (pickle.UnpicklingError, EOFError): #TODO This is not optimal, entropy and fleids create diffrent EOFError
            pass
    return threshold
    for key, resultthreshold in threshold.items():
        print(key+" correct")
        print(resultthreshold["Attackcorrect"])
        print(resultthreshold["normalcorrect"])

        print(key +" wrong")
        print(resultthreshold["Attackwrong"])
        print(resultthreshold["normalwrong"])
        print("accaury")
        print((resultthreshold["Attackcorrect"]+resultthreshold["normalcorrect"])/total)
        print()
        for attackkey , resulttattack in threshold[key]["attacks"].items():
            print(key + " attack:" +attackkey)
            print(resulttattack["Attackcorrect"])
            print(resulttattack["Attackwrong"])
            print()
        


def readresult(file):
    total=0
    trainingSet=[]
    dataSet=[]
    with open(file, "rb") as fileOfFeatures:
        try:
            while True:
                data=np.load(fileOfFeatures, allow_pickle=True)
                trainingSet.append(data)
                total+=1
        except (pickle.UnpicklingError, EOFError): #TODO This is not optimal, entropy and fleids create diffrent EOFError
            pass
    dataSet=np.array(trainingSet)
    return dataSet, total
sampings=[100,400,800,1600,3200,6400,12800]
#sampings=[100]
filesnormal=[]
filethreshold=[]
metods=["KMeansentropy", "KMeanscombined","KMeansfields", "RandomForestentropy", "RandomForestcombined","RandomForestfields", "threshold"]
#metods=["KMeansentropy", "KMeanscombined","KMeansfields", "RandomForestentropy", "RandomForestcombined","RandomForestfields"]
#metods=["KMeansentropy"]
#metods=["threshold","RandomForestentropy","KMeansentropy"]
#startfile="E:\master/data/result/detect"
#startfile="data/Classifiers/result/detect"
startfile="/home/ingix/Documents/master_thesis-ReadyTORUN/data/Classifiers/result/detect"
#savefolder="/media/sf_share/data/result/"
savefolder="/home/ingix/Documents/master_thesis-ReadyTORUN/data/result/"


result={}
for rate in sampings:
    result[str(rate)]={}
    for metod in metods:
        result[str(rate)][metod]={}
        if metod== "threshold":
            filethreshold.append([startfile+str(rate)+"threshold.npy",metod,rate])
        else:
            filesnormal.append([startfile+str(rate)+metod +".npy", metod,rate])

for file in filesnormal:
    #result.append([readandgetresultnormal(file[0],file[1],file[2]),file[1],file[2]])
    result[str(file[2])][file[1]]=readandgetresultnormal(file[0])
for filetre in filethreshold:
    #result.append([readandgetresultthreshold(filetre[0],file[1],file[2]),file[1],file[2]])
    result[str(filetre[2])][filetre[1]]=readandgetresultthreshold(filetre[0])
with open(savefolder+"resultdel1.csv", 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for rate in result.keys():
        for metod, methodresult in result[rate].items():
            if metod == "threshold":
                for thresholdmetod, vaule in methodresult.items():

                    row=[rate,thresholdmetod,"total",vaule["Attackcorrect"],vaule["normalcorrect"],vaule["Attackwrong"],vaule["normalwrong"]]
                    wr.writerow(row)
                    row=[] 
                    for attack,attackvaule in vaule["attacks"].items():
                        row=[rate,thresholdmetod,attack,attackvaule["Attackcorrect"],0,attackvaule["Attackwrong"],0]
                        wr.writerow(row)
                        row=[] 
            else:
                #for key, vaule in result[rate][metod].items():
                    row=[rate,metod,"total",result[rate][metod]["Attackcorrect"],result[rate][metod]["normalcorrect"],result[rate][metod]["Attackwrong"],result[rate][metod]["normalwrong"]]
                    wr.writerow(row) 
                    row=[] 
                    for attack in result[rate][metod]["attacks"].keys():
                        row=[rate,metod,attack,result[rate][metod]["attacks"][attack]["Attackcorrect"],0,result[rate][metod]["attacks"][attack]["Attackwrong"],0]
                        wr.writerow(row)
                        row=[]    
"""
for rate in result.keys():
    for metod, methodresult in result[rate].items():
        listthreshold=[]
        if metod == "threshold":
            with open(savefolder+rate+metod+"result.csv", 'w', newline='') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                for thresholdmetod, vaule in methodresult.items():
                    row=[thresholdmetod,vaule["Attackcorrect"],vaule["normalcorrect"],vaule["Attackwrong"],vaule["normalwrong"]]
                    wr.writerow(row)
                    for attack,attackvaule in vaule["attacks"].items():
                        row=[attack,attackvaule["Attackcorrect"],attackvaule["Attackwrong"]]
                        wr.writerow(row)
        else:
            #for key, vaule in result[rate][metod].items():
            with open(savefolder+rate+metod+"result.csv", 'w', newline='') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                row=[metod,result[rate][metod]["Attackcorrect"],result[rate][metod]["normalcorrect"],result[rate][metod]["Attackwrong"],result[rate][metod]["normalwrong"]]
                wr.writerow(row)  
                for attack in result[rate][metod]["attacks"].keys():
                    row=[attack,result[rate][metod]["attacks"][attack]["Attackcorrect"],result[rate][metod]["attacks"][attack]["Attackwrong"],]
                    wr.writerow(row)   
"""

