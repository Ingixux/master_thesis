
import pickle as pickle
import numpy as np

trainingSet=[]
x=0
with open("data/Classifiers/result/detect800RandomForestentropy.npy", "rb") as fileOfFeatures:
#with open("data/Classifiers/result/detect800KMeansfields.npy", "rb") as fileOfFeatures:
#with open("data/Classifiers/result/detect800threshold.npy", "rb") as fileOfFeatures:
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
print(x)
dataSet=np.array(trainingSet)
Attackcorrect=0
Attackwrong=0
normalcorrect=0
normalwrong=0

#what="Threshold"
what="Kmeans"
if what !="Threshold":
    for element in dataSet:
        if element[0]==element[1]:
            if element[1]==1:
                Attackcorrect+=1
            else:
                normalcorrect+=1
        else:
            if element[1]==1:
                Attackwrong+=1
            else:
                normalwrong+=1

    print("correct")
    print(Attackcorrect)
    print(normalcorrect)

    print("wrong")
    print(Attackwrong)
    print(normalwrong)
    print("accaury")
    print((Attackcorrect+normalcorrect)/x)
    print()
else:
    threshold ={"entropySip":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "entropyRateSip":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "entropyDip":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "entropyRateDip":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "entropyPacketsize":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "entropyRatePacketsize":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "entropyBiflowSyn":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "entropySipSyn":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "entropyDipSyn":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "entropyBiflow":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "entropyRateBiflow":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "HigstNumberOfSyn":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "HigstNumberOfURGPSHFIN":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "countBiflow":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "totalicmpDUnreachable":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "totalBytes":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "totalpackets":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "totalicmp":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0},
                "totalicmprate":{"Attackcorrect":0,"Attackwrong":0,"normalcorrect":0,"normalwrong":0}}


    for element in dataSet:
        #print(element)
        for key in element[0]:
            if type(key)==list:
                #print(key[1])
                #print(element[2])
                if key[1]==element[2]:
                    if element[2]==1:
                        threshold[key[0]]["Attackcorrect"]+=1
                    else:
                        threshold[key[0]]["normalcorrect"]+=1
                else:
                    if element[2]==1:
                        threshold[key[0]]["Attackwrong"]+=1
                    else:
                        threshold[key[0]]["normalwrong"]+=1

    for key, resultthreshold in threshold.items():
        print(key+" correct")
        print(resultthreshold["Attackcorrect"])
        print(resultthreshold["normalcorrect"])

        print(key +" wrong")
        print(resultthreshold["Attackwrong"])
        print(resultthreshold["normalwrong"])
        print("accaury")
        print((resultthreshold["Attackcorrect"]+resultthreshold["normalcorrect"])/x)
        print()    




