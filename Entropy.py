import datetime
import numpy as np
import copy

class Entropy:
    def __init__(self,sliding_window_interval,aggregate_window_duration,comparison_window_interval,limited):
        self.sliding_window_interval =sliding_window_interval
        self.aggregate_window_duration=aggregate_window_duration
        self.comparison_window_interval=comparison_window_interval
        self.limited=limited
        self.orderEntropy=100
        self.startcounter=1
        self.aggregate_window={"currentTime":0,"earlistTime":0,"interval":datetime.timedelta(microseconds=aggregate_window_duration*1000),"vaules":[]}
        self.comparison_window={"currentTime":0,"currentRecs":[],"earlistTime":0,"interval":comparison_window_interval,"vaules":[]}
        for x in range(0,int(aggregate_window_duration/sliding_window_interval)):
            self.aggregate_window["vaules"].append({"sourceIP":{},"packets":0,"destinationIP":{},"currentRecs":[]})

        #for x in range(0,int(comparison_window_interval/sliding_window_interval)-(aggregate_window_duration/sliding_window_interval)):
        #    self.comparison_window["vaules"].append({"sourceIP":{},"packets":0,"destinationIP":{}})


    def checkwindowcomplet(self):
        if self.startcounter>=len(self.aggregate_window["vaules"]):
            return True
        else:
            return False

    def addNewRec(self,rec):
        toretrun=[]
        if self.aggregate_window["earlistTime"]==0:
            self.aggregate_window["earlistTime"]=rec.stime
        self.aggregate_window["currentTime"]=rec.stime
        if self.checkIfpastedSliding_window():
            self.aggregate_window["earlistTime"]=self.aggregate_window["currentTime"]
            if len(self.aggregate_window["vaules"][-1]["currentRecs"])!=0: #TODO this will not handle how I want if there in the midle comes a empty window
                toretrun=copy.copy(self.doCalculation())
                toretrun=self.doCalculation()
            elif self.startcounter<len(self.aggregate_window["vaules"]):
                self.startcounter+=1
            self.removeFromSliding_window()

        self.addVaules(rec)
        return toretrun

    def addVaules(self,rec):
        self.aggregate_window["vaules"][0]["currentRecs"].append(rec)
        self.aggregate_window["vaules"][0]["packets"]=self.aggregate_window["vaules"][0]["packets"] +rec.packets #TODO fix this
        if self.cheackIfNovaule("sourceIP",str(rec.sip)):
            self.aggregate_window["vaules"][0]["sourceIP"][str(rec.sip)] =1
        else:
            self.aggregate_window["vaules"][0]["sourceIP"][str(rec.sip)] +=1
        if self.cheackIfNovaule("destinationIP",str(rec.dip)):
            self.aggregate_window["vaules"][0]["destinationIP"][str(rec.dip)] =1
        else:
            self.aggregate_window["vaules"][0]["destinationIP"][str(rec.dip)] +=1

    def cheackIfNovaule(self,valueToCheck,anothervaule =None):
        if anothervaule ==None:
            try:
                self.aggregate_window["vaules"][0][valueToCheck]
                return False
            except KeyError:
                return True
        else:
            try:
                self.aggregate_window["vaules"][0][valueToCheck][anothervaule]
                return False
            except KeyError:
                return True

    def doCalculation(self):
        #TODO add the remaing entropy
        totalpackets=self.aggregate_window["vaules"][-1]["packets"]
        totalsourceIP=0 
        totaldestinationIP=0 
        uniqetotalsourceIP={}
        uniqedestinationIP={}
        for x in range(0,len(self.aggregate_window["vaules"])):
            totalpackets+=self.aggregate_window["vaules"][x]["packets"]
            for key in self.aggregate_window["vaules"][x]["sourceIP"].keys():
                #totalsourceIP+=self.aggregate_window["vaules"][x]["sourceIP"][key]
                #totaldestinationIP+=self.aggregate_window["vaules"][x]["destinationIP"][key]
                try:
                    uniqetotalsourceIP[key]+=self.aggregate_window["vaules"][x]["sourceIP"][key]
                except KeyError:
                    uniqetotalsourceIP[key]=self.aggregate_window["vaules"][x]["sourceIP"][key]
            for key in self.aggregate_window["vaules"][x]["destinationIP"].keys():        
                try:
                    uniqedestinationIP[key]+=self.aggregate_window["vaules"][x]["destinationIP"][key]
                except KeyError:
                    uniqedestinationIP[key]=self.aggregate_window["vaules"][x]["destinationIP"][key]
        arrayToAdd=[]
        listofprobability=[]
        for x in uniqetotalsourceIP.values():
            listofprobability.append(x/totalpackets)
        entropySip=self.entropyCal(listofprobability)
        entropyRateSip=entropySip/len(uniqetotalsourceIP)
        
        listofprobability=[]
        for x in uniqedestinationIP.values():
            listofprobability.append(x/totalpackets)
        entropyDip=self.entropyCal(listofprobability)
        entropyRateDip=entropyDip/len(uniqedestinationIP)
        #print(self.aggregate_window["vaules"][0]["currentRecs"])
        for rec in self.aggregate_window["vaules"][-1]["currentRecs"]:
            arrayToAdd.append([rec.stime, rec.etime, int(rec.sip), int(rec.dip), rec.sport, rec.dport, rec.protocol, rec.packets, rec.bytes, 
                                int(rec.tcpflags.fin), int(rec.tcpflags.syn), int(rec.tcpflags.rst), int(rec.tcpflags.psh), int(rec.tcpflags.ack), 
                                int(rec.tcpflags.urg), int(rec.tcpflags.ece), int(rec.tcpflags.cwr), rec.duration/datetime.timedelta(milliseconds=1), 
                                entropySip,entropyRateSip,entropyDip,entropyRateDip,
                                self.setIsAttack(rec)])
          
        return arrayToAdd                 

    def entropyCal(self,listofprobability):
        sum=0
        for x in listofprobability:
            sum+=x**self.orderEntropy
        return 1/(1-self.orderEntropy)*np.log2(sum)

    def setIsAttack(self,rec):
        isAttackFlow=0
        #if rec.sensor=="isAttack": #TODO why does this not work
        #    isAttackFlow=1
        if rec.sensor_id==3:
            isAttackFlow=1
        return isAttackFlow

    def removeFromSliding_window(self):
        #TODO create the data to retrun from the sliding_window, can use packets in all aggregate_window to see if aggregate_window is complete
        for x in range(1,len(self.aggregate_window["vaules"])):
            self.aggregate_window["vaules"][-x]=self.aggregate_window["vaules"][-(x+1)]
        self.aggregate_window["vaules"][0]={"sourceIP":{},"packets":0,"destinationIP":{}}
        self.aggregate_window["vaules"][0]["currentRecs"]=[]

    def checkIfpastedSliding_window(self):
        #print(self.aggregate_window["interval"])
        #print(self.aggregate_window["currentTime"]-self.aggregate_window["earlistTime"])
        if self.aggregate_window["interval"]<self.aggregate_window["currentTime"]-self.aggregate_window["earlistTime"]:
            return True
        else:
            return False
        