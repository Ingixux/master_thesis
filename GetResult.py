
import pickle as pickle
import numpy as np

trainingSet=[]
x=0
with open("data/Classifiers/result/train1000RandomForestentropy.npy", "rb") as fileOfFeatures:
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
Attackcorrect=0
Attackwrong=0
normalcorrect=0
normalwrong=0
for element in dataSet:
    if element[1]==element[2]:
        if element[2]==1:
            Attackcorrect+=1
        else:
            normalcorrect+=1
    else:
        if element[2]==1:
             Attackwrong+=1
        else:
            normalwrong+=1
print("correct")
print(Attackcorrect)
print(normalcorrect)

print("wrong")
print(Attackwrong)
print(normalwrong)

