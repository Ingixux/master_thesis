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
            self.aggregate_window["vaules"].append({"sourceIP":{},"packets":0,"destinationIP":{},"bytes":0,"packetsize":{},"currentRecs":[],
                                                    "biflow":{},"icmp":0,"Destination unreachable":0})

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
                #toretrun=self.doCalculation()
            elif self.startcounter<len(self.aggregate_window["vaules"]):
                self.startcounter+=1
            self.removeFromSliding_window()

        self.addVaules(rec)
        return toretrun

    def addVaules(self,rec):
        #int(rec.tcpflags.fin), int(rec.tcpflags.syn), int(rec.tcpflags.psh),int(rec.tcpflags.urg),
        self.aggregate_window["vaules"][0]["currentRecs"].append(rec)
        self.aggregate_window["vaules"][0]["packets"]=self.aggregate_window["vaules"][0]["packets"] +rec.packets 
        self.aggregate_window["vaules"][0]["bytes"]=self.aggregate_window["vaules"][0]["bytes"] +rec.bytes 
        
        checkKeyOfBiFlow = str(rec.dip)+ str(rec.sip) + str(rec.dport) +str(rec.sport) +str(rec.protocol)
        keyOfBiFlow= str(rec.sip) + str(rec.dip) +str(rec.sport) + str(rec.dport) +str(rec.protocol)

        if rec.protocol == 1:
            self.aggregate_window["vaules"][0]["icmp"]+=1*rec.packets
            if rec.icmptype == 3:
                self.aggregate_window["vaules"][0]["Destination unreachable"]+=1*rec.packets

        if keyOfBiFlow in self.aggregate_window["vaules"][0]["biflow"].keys():
            self.aggregate_window["vaules"][0]["biflow"][keyOfBiFlow]["packets"]+=1*rec.packets
            if rec.tcpflags.syn==1:
                 self.aggregate_window["vaules"][0]["biflow"][keyOfBiFlow]["syn"]+=1*rec.packets
        else:
            #keyOfBiFlow= str(rec.sip) + str(rec.dip) +str(rec.sport) + str(rec.dport) +str(rec.protocol)
            self.aggregate_window["vaules"][0]["biflow"][keyOfBiFlow]={"packets":1*rec.packets,"checkKey":checkKeyOfBiFlow,
                                                                       "syn":0,"destinationIP":rec.dip,"sourceIP":rec.sip,"foundBiFlow":False}
            if rec.tcpflags.syn==1:
                 self.aggregate_window["vaules"][0]["biflow"][keyOfBiFlow]["syn"]+=1*rec.packets


        if self.cheackIfNovaule("sourceIP",str(rec.sip)):
            #self.aggregate_window["vaules"][0]["sourceIP"][str(rec.sip)] =1*rec.packets
            self.aggregate_window["vaules"][0]["sourceIP"][str(rec.sip)]={"packets":1*rec.packets,"syn":0}
            if rec.tcpflags.syn==1:
                 self.aggregate_window["vaules"][0]["sourceIP"][str(rec.sip)]["syn"]+=1*rec.packets
        else:
            #self.aggregate_window["vaules"][0]["sourceIP"][str(rec.sip)] +=1*rec.packets
            self.aggregate_window["vaules"][0]["sourceIP"][str(rec.sip)]["packets"]+=1*rec.packets
            if rec.tcpflags.syn==1:
                 self.aggregate_window["vaules"][0]["sourceIP"][str(rec.sip)]["syn"]+=1*rec.packets
        if self.cheackIfNovaule("destinationIP",str(rec.dip)):
            #self.aggregate_window["vaules"][0]["destinationIP"] =1*rec.packets
            self.aggregate_window["vaules"][0]["destinationIP"][str(rec.dip)]={"packets":1*rec.packets,"syn":0}
            if rec.tcpflags.syn==1:
                 self.aggregate_window["vaules"][0]["destinationIP"][str(rec.dip)]["syn"]+=1*rec.packets
        else:
            #self.aggregate_window["vaules"][0]["destinationIP"][str(rec.dip)] +=1*rec.packets
            self.aggregate_window["vaules"][0]["destinationIP"][str(rec.dip)]["packets"] +=1*rec.packets
            if rec.tcpflags.syn==1:
                 self.aggregate_window["vaules"][0]["destinationIP"][str(rec.dip)]["syn"]+=1*rec.packets
        if self.cheackIfNovaule("packetsize",str(int(rec.bytes/rec.packets))):
            self.aggregate_window["vaules"][0]["packetsize"][str(int(rec.bytes//rec.packets))] =1*rec.packets
        else:
            self.aggregate_window["vaules"][0]["packetsize"][str(int(rec.bytes//rec.packets))] +=1*rec.packets

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
        totalpackets=0#self.aggregate_window["vaules"][-1]["packets"]
        totalsourceIP=0 
        totaldestinationIP=0 
        uniqetotalsourceIP={}
        uniqedestinationIP={}
        uniqepacketsize={}
        #uniqebiflow={}
        uniqebiflow={}
        countuniqebiflow=0
        uniqebiflowcounter=[]
        for x in range(0,len(self.aggregate_window["vaules"])):
            for biflowkey in self.aggregate_window["vaules"][x]["biflow"].keys():
                try:
                    #uniqebiflow[biflowkey]
                    uniqebiflow[biflowkey]["packets"]+=self.aggregate_window["vaules"][x]["biflow"][biflowkey]["packets"]
                    uniqebiflow[biflowkey]["syn"]+=self.aggregate_window["vaules"][x]["biflow"][biflowkey]["syn"]
                except KeyError:
                    uniqebiflow[biflowkey]=copy.copy(self.aggregate_window["vaules"][x]["biflow"][biflowkey])
        for biflowkey in uniqebiflow.keys():

            if uniqebiflow[biflowkey]["checkKey"] in uniqebiflow.keys() and uniqebiflow[uniqebiflow[biflowkey]["checkKey"]]["foundBiFlow"]==False:
                uniqebiflow[uniqebiflow[biflowkey]["checkKey"]]["foundBiFlow"]=True
                uniqebiflow[biflowkey]["foundBiFlow"]=True
                countuniqebiflow+=1
                uniqebiflowcounter.append([uniqebiflow[biflowkey]["packets"],uniqebiflow[biflowkey]["syn"]])
        for biflowkey in uniqebiflow:
            uniqebiflow[biflowkey]["foundBiFlow"]=False

            
        totalFlows=0
        totalBytes=0
        #checkkey=[]
        HigstNumberOfSyn=0
        HigstNumberOfURGPSHFIN=0
        totalicmp=0
        totalicmpDUnreachable=0

        for x in range(0,len(self.aggregate_window["vaules"])):
            totalpackets+=self.aggregate_window["vaules"][x]["packets"]
            totalBytes+=self.aggregate_window["vaules"][x]["bytes"]
            totalFlows+=len(self.aggregate_window["vaules"][x]["currentRecs"])
            totalicmp+=self.aggregate_window["vaules"][x]["icmp"]
            totalicmpDUnreachable+=self.aggregate_window["vaules"][x]["Destination unreachable"]
            for rec in self.aggregate_window["vaules"][x]["currentRecs"]:
                if rec.tcpflags.syn==1:
                    if rec.packets >HigstNumberOfSyn:
                        HigstNumberOfSyn=rec.packets
                if rec.tcpflags.urg==1 and rec.tcpflags.psh==1 and rec.tcpflags.fin==1:
                    if rec.packets >HigstNumberOfURGPSHFIN:
                        HigstNumberOfURGPSHFIN=rec.packets

            for key in self.aggregate_window["vaules"][x]["sourceIP"].keys():
                #totalsourceIP+=self.aggregate_window["vaules"][x]["sourceIP"][key]
                #totaldestinationIP+=self.aggregate_window["vaules"][x]["destinationIP"][key]
                try:
                    #uniqetotalsourceIP[key]+=self.aggregate_window["vaules"][x]["sourceIP"][key]["packets"]
                    uniqetotalsourceIP[key]["packets"]+=self.aggregate_window["vaules"][x]["sourceIP"][key]["packets"]
                    uniqetotalsourceIP[key]["syn"]+=self.aggregate_window["vaules"][x]["sourceIP"][key]["syn"]
                except KeyError:
                    #uniqetotalsourceIP[key]=self.aggregate_window["vaules"][x]["sourceIP"][key]["packets"]
                    uniqetotalsourceIP[key]={"packets":self.aggregate_window["vaules"][x]["sourceIP"][key]["packets"],
                                             "syn":self.aggregate_window["vaules"][x]["sourceIP"][key]["syn"]}
            for key in self.aggregate_window["vaules"][x]["destinationIP"].keys():        
                try:
                    #uniqedestinationIP[key]+=self.aggregate_window["vaules"][x]["destinationIP"][key]["packets"]
                    uniqedestinationIP[key]["packets"]+=self.aggregate_window["vaules"][x]["destinationIP"][key]["packets"]
                    uniqedestinationIP[key]["syn"]+=self.aggregate_window["vaules"][x]["destinationIP"][key]["syn"]
                except KeyError:
                    #uniqedestinationIP[key]=self.aggregate_window["vaules"][x]["destinationIP"][key]["packets"]
                    uniqedestinationIP[key]={"packets":self.aggregate_window["vaules"][x]["destinationIP"][key]["packets"],
                                             "syn":self.aggregate_window["vaules"][x]["destinationIP"][key]["syn"]}
            
            for key in self.aggregate_window["vaules"][x]["packetsize"].keys():
                try:
                    uniqepacketsize[key]+=self.aggregate_window["vaules"][x]["packetsize"][key]
                except KeyError:
                    uniqepacketsize[key]=self.aggregate_window["vaules"][x]["packetsize"][key]

        totalicmprate= totalicmp/totalpackets     

        arrayToAdd=[]
        listofprobability=[]
        listofprobability2=[]
        for x in uniqetotalsourceIP.values():
            listofprobability.append(x["packets"]/totalpackets)
            listofprobability2.append(x["syn"]/totalpackets)
        entropySip=self.entropyCal(listofprobability)
        entropyRateSip=entropySip/len(uniqetotalsourceIP)
        entropySipSyn=self.entropyCal(listofprobability2)
        
    
        listofprobability=[]
        listofprobability2=[]
        for x in uniqedestinationIP.values():
            listofprobability.append(x["packets"]/totalpackets)
            listofprobability2.append(x["syn"]/totalpackets)
        entropyDip=self.entropyCal(listofprobability)
        entropyRateDip=entropyDip/len(uniqedestinationIP)#TODO it might be worth it to look at all the size from the lowest to the highst
        entropyDipSyn=self.entropyCal(listofprobability2)

        listofprobability=[]
        for x in uniqepacketsize.values():
            listofprobability.append(x/totalpackets)
        entropyPacketsize=self.entropyCal(listofprobability)
        entropyRatePacketsize=entropyPacketsize/len(uniqepacketsize)
        
        listofprobability=[]
        listofprobability2=[]
        for x in uniqebiflowcounter:
            listofprobability.append(x[0]/totalpackets)
            listofprobability2.append(x[1]/totalpackets)
        entropyBiflow=self.entropyCal(listofprobability)
        entropyRateBiflow=entropyPacketsize/len(uniqebiflowcounter)
        entropyBiflowSyn=self.entropyCal(listofprobability2)
        countBiflow=len(uniqebiflowcounter)


        #print(self.aggregate_window["vaules"][0]["currentRecs"])
        for rec in self.aggregate_window["vaules"][-1]["currentRecs"]:
            arrayToAdd.append([rec.stime, rec.etime, int(rec.sip), int(rec.dip), rec.sport, rec.dport, rec.protocol, rec.packets, rec.bytes, 
                                int(rec.tcpflags.fin), int(rec.tcpflags.syn), int(rec.tcpflags.rst), int(rec.tcpflags.psh), int(rec.tcpflags.ack), 
                                int(rec.tcpflags.urg), int(rec.tcpflags.ece), int(rec.tcpflags.cwr), rec.duration/datetime.timedelta(milliseconds=1), int(rec.nhip),
                                totalFlows,totalicmp,totalicmprate,totalBytes,totalpackets,entropySip,entropyRateSip,entropyDip,entropyRateDip,entropyPacketsize,
                                entropyRatePacketsize,entropyBiflow,entropyRateBiflow,entropyBiflowSyn,entropySipSyn,entropyDipSyn,
                                countBiflow,HigstNumberOfSyn,HigstNumberOfURGPSHFIN,totalicmpDUnreachable,
                                self.setIsAttack(rec)])
        #TODO add this vaules into the comparison window
        """ vaules to add

        These are not part of the fields for RF:
        entropyBiflowSyn,entropySipSyn,entropyDipSyn,countBiflow,HigstNumberOfSyn,HigstNumberOfURGPSHFIN,totalicmpDUnreachable,

        Threshold entropy:
            entropySip,
            entropyRateSip,
            entropyDip
            entropyRateDip
            entropyPacketsize,
            entropyRatePacketsize
            entropyBiflowSyn,
            entropySipSyn,
            entropyDipSyn,
            entropyBiflow,
            entropyRateBiflow,
        

        Threshold:
            HigstNumberOfSyn
            HigstNumberOfURGPSHFIN
            countBiflow
            totalicmpDUnreachable
            totalBytes
            totalpackets
            totalicmp
            totalicmprate
        
        
        """
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
        self.aggregate_window["vaules"][0]={"sourceIP":{},"packets":0,"destinationIP":{},"bytes":0,"packetsize":{},"currentRecs":[],
                                            "biflow":{},"icmp":0,"Destination unreachable":0}
        #self.aggregate_window["vaules"][0]["currentRecs"]=[]

    def checkIfpastedSliding_window(self):
        #print(self.aggregate_window["interval"])
        #print(self.aggregate_window["currentTime"]-self.aggregate_window["earlistTime"])
        if self.aggregate_window["interval"]<self.aggregate_window["currentTime"]-self.aggregate_window["earlistTime"]:
            return True
        else:
            return False
        