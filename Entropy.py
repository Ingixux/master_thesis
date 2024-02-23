import datetime
import numpy as np

class Entropy:
    def __init__(self,sliding_window_interval,aggregate_window_duration,comparison_window_interval,limited):
        self.sliding_window_interval =sliding_window_interval
        self.aggregate_window_duration=aggregate_window_duration
        self.comparison_window_interval=comparison_window_interval
        #self.sliding_currentTime=0
        #self.aggregate_currentTime=0
        #self.comparison_currentTime=0
        self.limited=limited
        self.orderEntropy=100
        self.startcounter=1
        #self.dicOfWindis={"aggregate_window":{"currentTime":0},"sliding_window":{},"comparison_window":{}}
        #vaules={"sourceIP":{},"packets":0,"destinationIP":{}}
        #self.sliding_window={"currentTime":0,"currentRecs":[],"earlistTime":0,"interval":sliding_window_interval,"vaules":vaules}
        self.aggregate_window={"currentTime":0,"earlistTime":0,"interval":aggregate_window_duration,"vaules":[]}
        self.comparison_window={"currentTime":0,"currentRecs":[],"earlistTime":0,"interval":comparison_window_interval,"vaules":[]}
        for x in (0,aggregate_window_duration/sliding_window_interval):
            self.aggregate_window["vaules"].append({"sourceIP":{},"packets":0,"destinationIP":{},"currentRecs":[]})
        for x in (0,(comparison_window_interval/sliding_window_interval)-(aggregate_window_duration/sliding_window_interval)):
            self.comparison_window["vaules"].append({"sourceIP":{},"packets":0,"destinationIP":{}})
        


        #self.aggregate_window=[]
        #self.sliding_window=[]
        #self.comparison_window=[]
         

    def checkwindowcomplet(self):
        if self.startcounter>=len(self.aggregate_window["vaules"]):
            return True
        else:
            self.startcounter+=1
            return False

    def detect(self):
        pass

    def addNewRec(self,rec,combind):
        toretrun=[]
        if self.aggregate_window["earlistTime"]==0:
            self.aggregate_window["earlistTime"]=rec.stime
        else:
            self.aggregate_window["currentTime"]=rec.stime
        if self.checkIfpastedSliding_window():
            self.aggregate_window["earlistTime"]=self.aggregate_window["currentTime"]
            toretrun=self.doCalculation()
            #toretrun=self.removeFromSliding_window(combind) #this not need to retrun something, if the cal happens before
            self.removeFromSliding_window(combind)
        self.addVaules()
        
        #TODO add the the vaules to the sliding window

        return toretrun
        #if self.checkIfpastedAggregate_window():
        #    self.removeFromAggregate_window()
        #if self.comparison_window["interval"] !=0:
        #    if self.checkIfpastedComparison_window():
        #        self.removeFromComparison_window()


    def addVaules(self,rec):
        self.aggregate_window["vaules"][0]["currentRecs"].append(rec)
        self.aggregate_window["vaules"][0]["packets"]=self.sliding_window["vaules"]["packets"] +rec.packets
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
                    uniqedestinationIP[key]+=self.aggregate_window["vaules"][x]["destinationIP"][key]
                except KeyError:
                    uniqedestinationIP[key]=self.aggregate_window["vaules"][x]["destinationIP"][key]
                try:
                    uniqetotalsourceIP[key]+=self.aggregate_window["vaules"][x]["sourceIP"][key]
                except KeyError:
                    uniqetotalsourceIP[key]=self.aggregate_window["vaules"][x]["sourceIP"][key]
        arrayToAdd=[]
        listofprobability=[]
        for x in uniqetotalsourceIP:
            listofprobability.append(x/totalpackets)
        entropySip=self.entropyCal(listofprobability)
        entropyRateSip=entropySip/len(uniqetotalsourceIP)
        
        listofprobability=[]
        for x in uniqedestinationIP:
            listofprobability.append(x/totalpackets)
        entropyDip=self.entropyCal(listofprobability)
        entropyRateDip=entropyDip/len(uniqedestinationIP)
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

    def removeFromSliding_window(self,combind):
        #TODO create the data to retrun from the sliding_window, can use packets in all aggregate_window to see if aggregate_window is complete
        for x in range(1,len(self.aggregate_window["vaules"])+1):
            self.aggregate_window["vaules"][-x]=self.aggregate_window["vaules"][-(x+1)]
        #self.aggregate_window["vaules"][0]=self.sliding_window["vaules"]
        #datatoretrun=[]
        #datatoretrun=copy.copy(self.sliding_window["vaules"])
        self.aggregate_window["vaules"][0]={"sourceIP":{},"packets":0,"destinationIP":{}}
        self.aggregate_window["vaules"][0]["currentRecs"]=[]
        #return datatoretrun

    def removeFromAggregate_window(self):
        pass

    def changeVaules_Sliding_window(self,recs):
        pass

    def changeVaules_Comparison_window(self,recs):
        pass

    def changeVaules_Aggregate_window(self,recs):
        pass

    def removeFromComparison_window(self):
        pass

    def checkIfpastedSliding_window(self):
        if self.sliding_window["interval"]<self.sliding_window["currentTime"]-self.sliding_window["earlistTime"]:
            return True
        else:
            return False
        
    def checkIfpastedAggregate_window(self):
        if self.aggregate_window["interval"]<self.aggregate_window["currentTime"]-self.aggregate_window["earlistTime"]:
            return True
        else:
            return False
        
    def checkIfpastedComparison_window(self):
        if self.comparison_window["interval"]<self.comparison_window["currentTime"]-self.comparison_window["earlistTime"]:
            return True
        else:
            return False
