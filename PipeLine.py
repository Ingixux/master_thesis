
from AttackDataMultiplicator import AttackDataMultiplicator,InputToAttackDataMultiplicator
import datetime
from GetTrafficPattern import GetTrafficPattern
from FindFiles import FindFiles,Folderpathstructure
from MixingOfData import MixingOfData, SamplingRate
from IDS import IDS
from RandomforestDetection import RandomforestDetection
from Threshold import Threshold
from Kmeans import Kmeans

startoffile="/media/sf_share/" #TODO Må endres til path til deres Silk data. 
systemid="oslo" #TODO Må endres til ruteren som skal brukes som kilde av data
inorout="out" #TODO Må endres til å passe mappe strukturen til dere


trafficpatternStart=[2024,2,5]
trafficpatternEnd=[2024,2,6]

traningDaysStart=[2024,2,5]
traningDaysEnd=[2024,2,6]

detectDaysStart=[2024,2,6]
detectDaysEnd=[2024,2,7]


samplingratesToMake=["1:800","1:1600"]


start=Folderpathstructure(inorout,systemid,trafficpatternStart[0],trafficpatternStart[1],trafficpatternStart[2],startoffile)
end=Folderpathstructure(inorout,systemid,trafficpatternEnd[0],trafficpatternEnd[1],trafficpatternEnd[2],startoffile)

ff=FindFiles(start,end)
GT=GetTrafficPattern(ff.findallfiles())
choseDip, choseSip=GT.movetroughthefiles(100,20,3)
nexthopip =[]
for ip in choseDip:
    nexthopip.append(GT.getnexthopip("destinationIP",choseDip))


print("Traffic Pattern recived")
#AttackDataMultiplicator (o)


ia1 = InputToAttackDataMultiplicator({"botsize":90000,"dst":[choseDip[0]],"src":choseSip, "nIP":nexthopip[0], "isAttack":32532, "botnet_rotation_algorithm":"standard",
                                    "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=10000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 12, 2, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 12, 5, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})
ia2 = InputToAttackDataMultiplicator({"botsize":90000,"dst":[choseDip[1]],"src":choseSip, "nIP":nexthopip[1], "isAttack":32532,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=10000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 12, 17, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 12, 23, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})
ia3 = InputToAttackDataMultiplicator({"botsize":60000,"dst":[choseDip[2]],"src":choseSip, "nIP":nexthopip[2], "isAttack":32532,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=10000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})


#listofFiles =["data/GenratedAttacks/ext2ext-S0_20240125.12"]
a1=AttackDataMultiplicator([ia1,ia2],"data/GenratedAttacks/ext2ext-S0_20240125.12","TCP_SYN_Flodd1")
a1=AttackDataMultiplicator([ia3],"data/GenratedAttacks/ext2ext-S0_20240125.12","TCP_SYN_Flodd2")
print("attacks modified")

sa1 =SamplingRate("1:1")
sa2 =SamplingRate("1:100")

listSamplingratesToMake=[]
for samplingrate in samplingratesToMake:
    listSamplingratesToMake.append(SamplingRate(samplingrate))



listofattackfilestrain=["data/ModifiedAttackFiles/TCP_SYN_Flodd10","data/ModifiedAttackFiles/TCP_SYN_Flodd11"]
listofattackfilesdetect=["data/ModifiedAttackFiles/TCP_SYN_Flodd20"]


#train
start=Folderpathstructure(inorout,systemid,trafficpatternStart[0],trafficpatternStart[1],trafficpatternStart[2],startoffile)
end=Folderpathstructure(inorout,systemid,traningDaysEnd[0],traningDaysEnd[1],traningDaysEnd[2],startoffile)
ff=FindFiles(start,end)
MD = MixingOfData(listSamplingratesToMake,listofattackfilestrain,ff.findallfiles(),[sa1,sa2],"train")

#detect
start=Folderpathstructure(inorout,systemid,detectDaysStart[0],detectDaysStart[1],detectDaysStart[2],startoffile)
end=Folderpathstructure(inorout,systemid,detectDaysEnd[0],detectDaysEnd[1],detectDaysEnd[2],startoffile)
ff=FindFiles(start,end)

MD = MixingOfData(listSamplingratesToMake,listofattackfilesdetect,ff.findallfiles(),[sa1,sa2],"detect")

print("Data mixed")

RFF=RandomforestDetection("fields","","")
RFE=RandomforestDetection("entropy","","")
RFC=RandomforestDetection("combined","","")
TH=Threshold("threshold","","")
KMF=Kmeans("fields","","")
KME=Kmeans("entropy","","")
KMC=Kmeans("combined","","")

listoffilestrain=[]
listoffilesdetect=[]
for smaplingrates in listSamplingratesToMake:
    listoffilestrain.append(["data/DiffrentSamplingRates/train/train"+str(smaplingrates.maxpackets)])
    listoffilesdetect.append(["data/DiffrentSamplingRates/detect/detect"+str(smaplingrates.maxpackets)])

a1=IDS([RFE,TH,KMF],listoffilestrain)





a1.makeTraingData()
a1.train()
print("Traning done")

a1.removeTrainingFiles()
a1.addNewFiles(listoffilesdetect)

a1.detect()
print("setup done")
