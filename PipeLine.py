
from AttackDataMultiplicator import AttackDataMultiplicator,InputToAttackDataMultiplicator
import datetime
from GetTrafficPattern import GetTrafficPattern
from FindFiles import FindFiles,Folderpathstructure
from MixingOfData import MixingOfData, SamplingRate
from Traning import TraningOfClassification
from RandomforestDetection import RandomforestDetection
from Threshold import Threshold
from Kmeans import Kmeans

startoffile="/media/sf_share/" #TODO this needs to fit with Sikt

start=Folderpathstructure("out","oslo",2011,1,25,startoffile)#TODO this needs to fit with the dates I want
end=Folderpathstructure("out","oslo",2011,1,26,startoffile)#TODO this needs to fit with the dates I want

ff=FindFiles(start,end)
GT=GetTrafficPattern(ff.findallfiles())
choseDip, choseSip=GT.movetroughthefiles(100,20,3)
nexthopip =[]
for ip in choseDip:
    nexthopip.append(GT.getnexthopip("destinationIP",choseDip))


print("Traffic Pattern recived")
#AttackDataMultiplicator (o)
#TODO NEED more isAttack


ia1 = InputToAttackDataMultiplicator({"botsize":90000,"dst":[choseDip[0]],"src":choseSip, "nIP":nexthopip[0], "isAttack":32532, "botnet_rotation_algorithm":"standard",
                                    "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=10000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 12, 2, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 12, 5, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})
ia2 = InputToAttackDataMultiplicator({"botsize":90000,"dst":[choseDip[1]],"src":choseSip, "nIP":nexthopip[1], "isAttack":32532,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=10000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 12, 2, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 12, 5, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})
ia3 = InputToAttackDataMultiplicator({"botsize":90000,"dst":[choseDip[2]],"src":choseSip, "nIP":nexthopip[2], "isAttack":32532,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=10000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 2, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 5, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})


#listofFiles =["data/GenratedAttacks/ext2ext-S0_20240125.12"]
a1=AttackDataMultiplicator([ia1,ia2],"data/GenratedAttacks/ext2ext-S0_20240125.12","TCP_SYN_Flodd1")
a1=AttackDataMultiplicator([ia3],"data/GenratedAttacks/ext2ext-S0_20240125.12","TCP_SYN_Flodd2")
#TODO add one AttackDataMultiplicator for each modified attack I want, this will depend on how many attack I create 
print("attacks modified")

sa1 =SamplingRate("1:1")
sa2 =SamplingRate("1:100")
ca1 =SamplingRate("1:800")
ca2 =SamplingRate("1:1600")
#TODO add more of the ca I want, this is the sampling rate output

listofattackfilestrain=["data/ModifiedAttackFiles/TCP_SYN_Flodd10","data/ModifiedAttackFiles/TCP_SYN_Flodd11"]
listofattackfilesdetect=["data/ModifiedAttackFiles/TCP_SYN_Flodd20"]


#train
start=Folderpathstructure("out","oslo",2011,1,25,startoffile)#TODO this needs to fit with the dates I want
end=Folderpathstructure("out","oslo",2011,1,26,startoffile)#TODO this needs to fit with the dates I want
ff=FindFiles(start,end)
MD = MixingOfData([ca1,ca2],listofattackfilestrain,ff.findallfiles(),[sa1,sa2],"train")

#detect
start=Folderpathstructure("out","oslo",2011,1,25,startoffile)#TODO this needs to fit with the dates I want
end=Folderpathstructure("out","oslo",2011,1,26,startoffile)#TODO this needs to fit with the dates I want
ff=FindFiles(start,end)

MD = MixingOfData([ca1,ca2],listofattackfilesdetect,ff.findallfiles(),[sa1,sa2],"detect")

print("Data mixed")

RFF=RandomforestDetection("fields","","")
RFE=RandomforestDetection("entropy","","")
RFC=RandomforestDetection("combined","","")
TH=Threshold("threshold","","")
KMF=Kmeans("fields","","")
KME=Kmeans("entropy","","")
KMC=Kmeans("combined","","")

listofsmaplingrates =["800","1600"] #TODO add the new sampling rates
listoffilestrain=[]
listoffilesdetect=[]
for smaplingrates in listofsmaplingrates:
    listoffilestrain.append(["data/DiffrentSamplingRates/train/train"+smaplingrates])
    listoffilesdetect.append(["data/DiffrentSamplingRates/detect/detect"+smaplingrates])

a1=TraningOfClassification([RFE,TH,KMF],listoffilestrain)


#a2=TraningOfClassification([RFE,TH,KMF],[["data/DiffrentSamplingRates/detect/detect1000"]])
#


a1.makeTraingData()
a1.train()
print("Traning done")

a1.removeTrainingFiles()#DONE? not tested#TODO have something to remove the traningfiles that are no longer needed
a1.addNewFiles(listoffilesdetect)#DONE? not tested #TODO  have something to add new files
"""
a1.detect()
print("setup done")
"""