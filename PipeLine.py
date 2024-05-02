
from AttackDataMultiplicator import AttackDataMultiplicator,InputToAttackDataMultiplicator
import datetime
from GetTrafficPattern import GetTrafficPattern
from FindFiles import FindFiles,Folderpathstructure
from MixingOfData import MixingOfData, SamplingRate
from IDS import IDS
from RandomforestDetection import RandomforestDetection
from Threshold import Threshold
from Kmeans import Kmeans

startoffile="/media/sf_share/" #TODO this needs to fit with Sikt
systemid="oslo"
inorout="out"

#TODO these needs to fit with the dates I want
trafficpatternStart=[2011,1,3]
trafficpatternEnd=[2011,1,10]

traningDaysStart=[2011,1,3]
traningDaysEnd=[2011,1,17]

detectDaysStart=[2011,1,17]
detectDaysEnd=[2011,1,31]

samplingratesToMake=["1:100","1:400","1:800","1:1600","1:3200","1:6400","1:12800"]
#TODO add more of the ca I want, this is the sampling rate output

start=Folderpathstructure(inorout,systemid,trafficpatternStart[0],trafficpatternStart[1],trafficpatternStart[2],startoffile)
end=Folderpathstructure(inorout,systemid,trafficpatternEnd[0],trafficpatternEnd[1],trafficpatternEnd[2],startoffile)

ff=FindFiles(start,end)
GT=GetTrafficPattern(ff.findallfiles())
choseDip, choseSip=GT.movetroughthefiles(500,320,32)
nexthopip ={}
for ip in choseDip:
    nexthopip[choseDip]=GT.getnexthopip("destinationIP",choseDip)





print("Traffic Pattern recived")
#AttackDataMultiplicator (o)
#TODO NEED more isAttack 
#TODO What to do with sourceip
#TODO change the attack dates


#slowread attackid = [32531,32532,32533,32534,32535,32536,32537,32538]

slowreadbotsrc=[choseSip[0:10],choseSip[10:20],choseSip[20:30],choseSip[30:40]]
slowlorisbotsrc=[choseSip[40:50],choseSip[50:60],choseSip[60:70],choseSip[70:80]]
rubybotsrc=[choseSip[80:90],choseSip[90:100],choseSip[100:110],choseSip[110:120]]

pingfloodbotsrc=[choseSip[120:130],choseSip[130:140],choseSip[140:150],choseSip[150:160]]
blacknursebotsrc=[choseSip[160:170],choseSip[170:180],choseSip[180:190],choseSip[190:200]]

synfloodbotsrc=[choseSip[200:210],choseSip[210:220],choseSip[220:230],choseSip[230:240]]
udpfloodbotsrc=[choseSip[240:250],choseSip[250:260],choseSip[260:270],choseSip[270:280]]
xmasbotsrc=[choseSip[280:290],choseSip[290:300],choseSip[300:310],choseSip[310:320]]


slowread1 = InputToAttackDataMultiplicator({"botsize":673,"dst":[choseDip[0]],"src":slowreadbotsrc[0], "nIP":nexthopip[choseDip[0]], "isAttack":32533,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=227000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})
slowread2 = InputToAttackDataMultiplicator({"botsize":349,"dst":[choseDip[1]],"src":slowreadbotsrc[1], "nIP":nexthopip[choseDip[1]], "isAttack":32533,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=395000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})
slowread3 = InputToAttackDataMultiplicator({"botsize":481,"dst":[choseDip[2]],"src":slowreadbotsrc[2], "nIP":nexthopip[choseDip[2]], "isAttack":32533,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=295000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 3, 12, 50, 51, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 3, 12, 50, 52, 0), "startTimeIncreasAlgorithm":"standard"})#TIME DONE
slowread4 = InputToAttackDataMultiplicator({"botsize":565,"dst":[choseDip[3]],"src":slowreadbotsrc[3], "nIP":nexthopip[choseDip[3]], "isAttack":32533,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=261000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})

#slowread attackid = 32534
slowloris1 = InputToAttackDataMultiplicator({"botsize":330,"dst":[choseDip[4]],"src":slowlorisbotsrc[0], "nIP":nexthopip[choseDip[4]], "isAttack":32534,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=571000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})
slowloris2 = InputToAttackDataMultiplicator({"botsize":430,"dst":[choseDip[5]],"src":slowlorisbotsrc[1], "nIP":nexthopip[choseDip[5]], "isAttack":32534,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=763000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})
slowloris3 = InputToAttackDataMultiplicator({"botsize":530,"dst":[choseDip[6]],"src":slowlorisbotsrc[2], "nIP":nexthopip[choseDip[6]], "isAttack":32534,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=784000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 6, 8, 4, 25, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})#time done
slowloris4 = InputToAttackDataMultiplicator({"botsize":456,"dst":[choseDip[7]],"src":slowlorisbotsrc[3], "nIP":nexthopip[choseDip[7]], "isAttack":32534,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=736000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})

#slowread attackid = 32535
ruby1 = InputToAttackDataMultiplicator({"botsize":301,"dst":[choseDip[8]],"src":rubybotsrc[0], "nIP":nexthopip[choseDip[8]], "isAttack":32535,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=1356000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})
ruby2 = InputToAttackDataMultiplicator({"botsize":439,"dst":[choseDip[9]],"src":rubybotsrc[1], "nIP":nexthopip[choseDip[9]], "isAttack":32535,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=941000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})
ruby3 = InputToAttackDataMultiplicator({"botsize":633,"dst":[choseDip[10]],"src":rubybotsrc[2], "nIP":nexthopip[choseDip[10]], "isAttack":32535,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=1118000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})
ruby4 = InputToAttackDataMultiplicator({"botsize":555,"dst":[choseDip[11]],"src":rubybotsrc[3], "nIP":nexthopip[choseDip[11]], "isAttack":32535,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=687000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})

#pingflood attackid = 32531
pingflood1 = InputToAttackDataMultiplicator({"botsize":302,"dst":[choseDip[12]],"src":pingfloodbotsrc[0], "nIP":nexthopip[choseDip[12]], "isAttack":32531,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=596000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 5, 11, 13, 22, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})#time done
pingflood2 = InputToAttackDataMultiplicator({"botsize":401,"dst":[choseDip[13]],"src":pingfloodbotsrc[1], "nIP":nexthopip[choseDip[13]], "isAttack":32531,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=105000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})
pingflood3 = InputToAttackDataMultiplicator({"botsize":355,"dst":[choseDip[14]],"src":pingfloodbotsrc[2], "nIP":nexthopip[choseDip[14]], "isAttack":32531,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=507000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})
pingflood4 = InputToAttackDataMultiplicator({"botsize":421,"dst":[choseDip[15]],"src":pingfloodbotsrc[3], "nIP":nexthopip[choseDip[15]], "isAttack":32531,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=356000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})


#blacknurse attackid = 32532
blacknurse1 = InputToAttackDataMultiplicator({"botsize":456,"dst":[choseDip[16]],"src":blacknursebotsrc[0], "nIP":nexthopip[choseDip[16]], "isAttack":32532,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=526000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})
blacknurse2 = InputToAttackDataMultiplicator({"botsize":321,"dst":[choseDip[17]],"src":blacknursebotsrc[1], "nIP":nexthopip[choseDip[17]], "isAttack":32532,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=934000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})
blacknurse3 = InputToAttackDataMultiplicator({"botsize":395,"dst":[choseDip[18]],"src":blacknursebotsrc[2], "nIP":nexthopip[choseDip[18]], "isAttack":32532,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=33873000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})
blacknurse4 = InputToAttackDataMultiplicator({"botsize":296,"dst":[choseDip[19]],"src":blacknursebotsrc[3], "nIP":nexthopip[choseDip[19]], "isAttack":32532,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=51891000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standard"})


#xmas attackid = 32536
xmas1 = InputToAttackDataMultiplicator({"botsize":732,"dst":[choseDip[20]],"src":xmasbotsrc[0], "nIP":nexthopip[choseDip[20]], "isAttack":32536, "botnet_rotation_algorithm":"standard",
                                    "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=37000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 12, 2, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 12, 5, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})
xmas2 = InputToAttackDataMultiplicator({"botsize":429,"dst":[choseDip[21]],"src":xmasbotsrc[1], "nIP":nexthopip[choseDip[21]], "isAttack":32536,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=48000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 12, 17, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 12, 23, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})
xmas3 = InputToAttackDataMultiplicator({"botsize":915,"dst":[choseDip[22]],"src":xmasbotsrc[2], "nIP":nexthopip[choseDip[22]], "isAttack":32536,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=36000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 7, 11, 5, 49, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})#time done
xmas4 = InputToAttackDataMultiplicator({"botsize":613,"dst":[choseDip[23]],"src":xmasbotsrc[3], "nIP":nexthopip[choseDip[23]], "isAttack":32536,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=46000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})

#udpflood attackid = 32537
udpflood1 = InputToAttackDataMultiplicator({"botsize":1047,"dst":[choseDip[24]],"src":udpfloodbotsrc[0], "nIP":nexthopip[choseDip[24]], "isAttack":32537, "botnet_rotation_algorithm":"standard",
                                    "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=28000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 4, 13, 45, 8, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 12, 5, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})#time done
udpflood2 = InputToAttackDataMultiplicator({"botsize":689,"dst":[choseDip[25]],"src":udpfloodbotsrc[1], "nIP":nexthopip[choseDip[25]], "isAttack":32537,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=21000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 12, 17, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 12, 23, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})
udpflood3 = InputToAttackDataMultiplicator({"botsize":915,"dst":[choseDip[26]],"src":udpfloodbotsrc[2], "nIP":nexthopip[choseDip[26]], "isAttack":32537,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=25000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 7, 5, 33, 26, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})#time done
udpflood4 = InputToAttackDataMultiplicator({"botsize":613,"dst":[choseDip[27]],"src":udpfloodbotsrc[3], "nIP":nexthopip[choseDip[27]], "isAttack":32537,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=63000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})


#synflood attackid = 32538
synflood1 = InputToAttackDataMultiplicator({"botsize":1047,"dst":[choseDip[28]],"src":synfloodbotsrc[0], "nIP":nexthopip[choseDip[28]], "isAttack":32538, "botnet_rotation_algorithm":"standard",
                                    "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=29000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 12, 2, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 12, 5, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})
synflood2 = InputToAttackDataMultiplicator({"botsize":689,"dst":[choseDip[29]],"src":synfloodbotsrc[1], "nIP":nexthopip[choseDip[29]], "isAttack":32538,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=20000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 12, 17, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 12, 23, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})
synflood3 = InputToAttackDataMultiplicator({"botsize":915,"dst":[choseDip[30]],"src":synfloodbotsrc[2], "nIP":nexthopip[choseDip[30]], "isAttack":32538,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=36000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})
synflood4 = InputToAttackDataMultiplicator({"botsize":613,"dst":[choseDip[31]],"src":synfloodbotsrc[3], "nIP":nexthopip[choseDip[31]], "isAttack":32538,"botnet_rotation_algorithm":"standard",
                                      "TT1":datetime.timedelta(microseconds=10000),"TT2":datetime.timedelta(microseconds=10000),"TBA":datetime.timedelta(microseconds=31000),
                                      "stratTimeOfAttack" : datetime.datetime(2011, 1, 25, 13, 40, 20, 0) , "endTimeOfAttack"  : datetime.datetime(2011, 1, 25, 13, 42, 0, 0), "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})



#listofFiles =["data/GenratedAttacks/ext2ext-S0_20240125.12"]
a1=AttackDataMultiplicator([slowread1],"data/GenratedAttacks/slowread673","slowread1")
a2=AttackDataMultiplicator([slowread2],"data/GenratedAttacks/slowread349","slowread2")
a3=AttackDataMultiplicator([slowread3],"data/GenratedAttacks/slowread481","slowread3")
a4=AttackDataMultiplicator([slowread4],"data/GenratedAttacks/slowread565","slowread4")

a5=AttackDataMultiplicator([slowloris1],"data/GenratedAttacks/slowloris330","slowloris1")
a6=AttackDataMultiplicator([slowloris2],"data/GenratedAttacks/slowloris430","slowloris2")
a7=AttackDataMultiplicator([slowloris3],"data/GenratedAttacks/slowloris530","slowloris3")
a8=AttackDataMultiplicator([slowloris4],"data/GenratedAttacks/slowloris456","slowloris4")

a9=AttackDataMultiplicator([ruby1],"data/GenratedAttacks/ruby301","ruby1")
a10=AttackDataMultiplicator([ruby2],"data/GenratedAttacks/ruby439","ruby2")
a11=AttackDataMultiplicator([ruby3],"data/GenratedAttacks/ruby633","ruby3")
a12=AttackDataMultiplicator([ruby4],"data/GenratedAttacks/ruby555","ruby4")

a13=AttackDataMultiplicator([pingflood1],"data/GenratedAttacks/pingflood1.rw","pingflood1")
a14=AttackDataMultiplicator([pingflood2],"data/GenratedAttacks/pingflood2.rw","pingflood2")
a15=AttackDataMultiplicator([pingflood3],"data/GenratedAttacks/pingflood3.rw","pingflood3")
a16=AttackDataMultiplicator([pingflood4],"data/GenratedAttacks/pingflood4.rw","pingflood4")

a17=AttackDataMultiplicator([blacknurse1],"data/GenratedAttacks/blacknurse1.rw","blacknurse1")
a18=AttackDataMultiplicator([blacknurse2],"data/GenratedAttacks/blacknurse2.rw","blacknurse2")
a19=AttackDataMultiplicator([blacknurse3],"data/GenratedAttacks/blacknurse3.rw","blacknurse3")
a20=AttackDataMultiplicator([blacknurse4],"data/GenratedAttacks/blacknurse4.rw","blacknurse4")

a21=AttackDataMultiplicator([xmas1],"data/GenratedAttacks/xmas1.rw","xmas1")
a22=AttackDataMultiplicator([xmas2],"data/GenratedAttacks/xmas2.rw","xmas2")
a23=AttackDataMultiplicator([xmas3],"data/GenratedAttacks/xmas3.rw","xmas3")
a24=AttackDataMultiplicator([xmas4],"data/GenratedAttacks/xmas4.rw","xmas4")

a25=AttackDataMultiplicator([udpflood1],"data/GenratedAttacks/udpflood1.rw","udpflood1")
a26=AttackDataMultiplicator([udpflood2],"data/GenratedAttacks/udpflood2.rw","udpflood2")
a27=AttackDataMultiplicator([udpflood3],"data/GenratedAttacks/udpflood3.rw","udpflood3")
a28=AttackDataMultiplicator([udpflood4],"data/GenratedAttacks/udpflood4.rw","udpflood4")

a29=AttackDataMultiplicator([synflood1],"data/GenratedAttacks/synflood1.rw","synflood1")
a30=AttackDataMultiplicator([synflood2],"data/GenratedAttacks/synflood2.rw","synflood2")
a31=AttackDataMultiplicator([synflood3],"data/GenratedAttacks/synflood3.rw","synflood3")
a32=AttackDataMultiplicator([synflood4],"data/GenratedAttacks/synflood4.rw","synflood4")


#TODO add one AttackDataMultiplicator for each modified attack I want, this will depend on how many attack I create 
print("attacks modified")

sa1 =SamplingRate("1:1")
sa2 =SamplingRate("1:100")

listSamplingratesToMake=[]
for samplingrate in samplingratesToMake:
    listSamplingratesToMake.append(SamplingRate(samplingrate))



listofattackfilestrain=["data/ModifiedAttackFiles/ruby10","data/ModifiedAttackFiles/ruby30","data/ModifiedAttackFiles/slowread10","data/ModifiedAttackFiles/slowread30","data/ModifiedAttackFiles/slowloris10","data/ModifiedAttackFiles/slowloris30"
                        ]#these need to be stored with the earilset at index 0
listofattackfilesdetect=["data/ModifiedAttackFiles/ruby20","data/ModifiedAttackFiles/ruby40","data/ModifiedAttackFiles/slowread20","data/ModifiedAttackFiles/slowread40","data/ModifiedAttackFiles/slowloris20","data/ModifiedAttackFiles/slowloris40"
                         ] #these need to be stored with the earilset at index 0


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
    listoffilestrain.append([startoffile+"data/DiffrentSamplingRates/train/train"+smaplingrates.maxpackets])
    listoffilesdetect.append([startoffile+"data/DiffrentSamplingRates/detect/detect"+smaplingrates.maxpackets])

a1=IDS([RFF,RFE,RFC,TH,KMF,KME,KMC],listoffilestrain)





a1.makeTraingData()
a1.train()
print("Traning done")

a1.removeTrainingFiles()
a1.addNewFiles(listoffilesdetect)

a1.detect()
print("setup done")
