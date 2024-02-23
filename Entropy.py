import copy

class Entropy:
    def __init__(self,sliding_window_interval,aggregate_window_duration,comparison_window_interval,limited):
        self.sliding_window_interval =sliding_window_interval
        self.aggregate_window_duration=aggregate_window_duration
        self.comparison_window_interval=comparison_window_interval
        #self.sliding_currentTime=0
        #self.aggregate_currentTime=0
        #self.comparison_currentTime=0
        self.limited=limited
        #self.dicOfWindis={"aggregate_window":{"currentTime":0},"sliding_window":{},"comparison_window":{}}
        vaules={"sourceIP":{},"packets":0,"destinationIP":{}}
        self.sliding_window={"currentTime":0,"currentRecs":[],"earlistTime":0,"interval":sliding_window_interval,"vaules":vaules}
        self.aggregate_window={"currentTime":0,"currentRecs":[],"earlistTime":0,"interval":aggregate_window_duration,"vaules":[]}
        self.comparison_window={"currentTime":0,"currentRecs":[],"earlistTime":0,"interval":comparison_window_interval,"vaules":[]}
        for x in (0,aggregate_window_duration/sliding_window_interval -1):
            self.aggregate_window["vaules"].append({"sourceIP":{},"packets":0,"destinationIP":{}})
        for x in (0,(comparison_window_interval/sliding_window_interval)-(aggregate_window_duration/sliding_window_interval)):
            self.comparison_window["vaules"].append({"sourceIP":{},"packets":0,"destinationIP":{}})
        


        #self.aggregate_window=[]
        #self.sliding_window=[]
        #self.comparison_window=[]
         


    def detect(self):
        pass

    def addNewRec(self,rec,combind):
        toretrun=[]
        if self.sliding_window["earlistTime"]==0:
            self.sliding_window["earlistTime"]=rec.stime
        else:
            self.sliding_window["currentTime"]=rec.stime
        
        if self.checkIfpastedSliding_window():
            self.sliding_window["earlistTime"]=self.sliding_window["currentTime"]
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
        self.sliding_window["currentRecs"].append(rec)
        self.sliding_window["vaules"]["packets"]=self.sliding_window["vaules"]["packets"] +rec.packets
        if self.cheackIfNovaule("sourceIP",str(rec.sip)):
            self.sliding_window["vaules"]["sourceIP"][str(rec.sip)] =1
        else:
            self.sliding_window["vaules"]["sourceIP"][str(rec.sip)] +=1
        if self.cheackIfNovaule("destinationIP",str(rec.dip)):
            self.sliding_window["vaules"]["destinationIP"][str(rec.dip)] =1
        else:
            self.sliding_window["vaules"]["destinationIP"][str(rec.dip)] +=1

    def cheackIfNovaule(self,valueToCheck,anothervaule =None):
        if anothervaule ==None:
            try:
                self.sliding_window["vaules"][valueToCheck]
                return False
            except KeyError:
                return True
        else:
            try:
                self.sliding_window["vaules"][valueToCheck][anothervaule]
                return False
            except KeyError:
                return True

    def doCalculation(self):
        #TODO add the calulation of the vaules
        #TODO return a array with the enpory added to it
        totalpackets=self.sliding_window["vaules"]["packets"]
        totalsourceIP=0
        totaldestinationIP=0
        uniqetotalsourceIP=[]
        uniqedestinationIP=[]

        for value in self.sliding_window["vaules"]["sourceIP"].values():
            totalsourceIP+=value
            if value not in uniqetotalsourceIP:
                uniqetotalsourceIP.append(value)
            if value not in uniqedestinationIP:
                uniqedestinationIP.append(value)
        for value in self.sliding_window["vaules"]["destinationIP"].values():
            totaldestinationIP+=value
        for x in range(0,len(self.aggregate_window["vaules"])):
            totalpackets+=self.aggregate_window["vaules"][x]["packets"]
            for value in self.sliding_window["vaules"][x]["sourceIP"].values():
                totalsourceIP+=value
            for value in self.sliding_window["vaules"][x]["destinationIP"].values():
                totaldestinationIP+=value
        
        


        
    def removeFromSliding_window(self,combind):
        #TODO create the data to retrun from the sliding_window, can use packets in all aggregate_window to see if aggregate_window is complete
        for x in range(1,len(self.aggregate_window["vaules"])+1):
            self.aggregate_window["vaules"][-x]=self.aggregate_window["vaules"][-(x+1)]
        self.aggregate_window["vaules"][0]=self.sliding_window["vaules"]
        #datatoretrun=[]
        #datatoretrun=copy.copy(self.sliding_window["vaules"])
        self.sliding_window["vaules"]={"sourceIP":{},"packets":0,"destinationIP":{}}
        self.sliding_window["currentRecs"]=[]
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
