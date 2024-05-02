import datetime
import numpy as np
import copy

class SlidingWindow:
    def __init__(self,sliding_window_interval,aggregate_window_duration,comparison_window_interval,limited):
        self.sliding_window_interval =sliding_window_interval
        self.aggregate_window_duration=aggregate_window_duration
        self.comparison_window_interval=comparison_window_interval
        self.limited=limited
        self.orderEntropy=50
        self.startcounter=1

        self.x=0
        #self.startOfWindow=0
        #self.EndOfWindow=aggregate_window_duration//sliding_window_interval
        #print(self.EndOfWindow)
        self.vaulesToCompare={"entropySip":0,"entropyRateSip":0,"entropyDip":0,"entropyRateDip":0,"entropyPacketsize":0,"entropyRatePacketsize":0,
                                           "entropyBiflowSyn":0,"entropySipSyn":0,"entropyDipSyn":0,"entropyBiflow":0,"entropyRateBiflow":0,
                                           "HigstNumberOfSyn":0,"HigstNumberOfURGPSHFIN":0,"countBiflow":0,"totalicmpDUnreachable":0,
                                           "totalBytes":0,"totalpackets":0,"totalicmp":0,"totalicmprate":0,"isAtttack":0,"totalflows":0}
        self.aggregate_window={"currentTime":0,"earlistTime":0,"interval":datetime.timedelta(microseconds=aggregate_window_duration*50000),"vaules":[]}
        #self.comparison_window={"currentTime":0,"currentRecs":[],"earlistTime":0,"interval":comparison_window_interval,"vaules":[]}
        #TODO compare the current vaule to the avgarge of the diffrent vaules, that is in the comparison_window
        self.comparison_window={"vaules":[],"interval":datetime.timedelta(microseconds=comparison_window_interval*50000)}
        for x in range(0,int(aggregate_window_duration/sliding_window_interval)):
            self.aggregate_window["vaules"].append({"sourceIP":{},"packets":0,"destinationIP":{},"bytes":0,"packetsize":{},"currentRecs":[],
                                                    "biflow":{},"icmp":0,"Destination unreachable":0})
        for x in range(0,int(((comparison_window_interval- aggregate_window_duration)/sliding_window_interval)+1)):
            self.comparison_window["vaules"].append({"entropySip":0,"entropyRateSip":0,"entropyDip":0,"entropyRateDip":0,"entropyPacketsize":0,"entropyRatePacketsize":0,
                                           "entropyBiflowSyn":0,"entropySipSyn":0,"entropyDipSyn":0,"entropyBiflow":0,"entropyRateBiflow":0,
                                           "HigstNumberOfSyn":0,"HigstNumberOfURGPSHFIN":0,"countBiflow":0,"totalicmpDUnreachable":0,
                                           "totalBytes":0,"totalpackets":0,"totalicmp":0,"totalicmprate":0})

        #for x in range(0,int(comparison_window_interval/sliding_window_interval)-(aggregate_window_duration/sliding_window_interval)):
        #    self.comparison_window["vaules"].append({"sourceIP":{},"packets":0,"destinationIP":{}})

    def checkwindowcomplet(self):
        if self.startcounter>=len(self.aggregate_window["vaules"]):
        #if self.startOfWindow==self.EndOfWindow:
            return True
        else:
            #TODO This does not handle if the post more than one
            #self.startOfWindow +=1
            return False

    def addNewRec(self,rec):
        self.x+=1
        toretrun=[]
        if self.aggregate_window["earlistTime"]==0:
            self.aggregate_window["earlistTime"]=rec.stime
        self.aggregate_window["currentTime"]=rec.stime
        #print(self.aggregate_window["currentTime"]-self.aggregate_window["earlistTime"])
        #print(rec.stime)
        if self.checkIfpastedSliding_window():
            
            #THIs moves 
            movewindow=(self.aggregate_window["currentTime"]-self.aggregate_window["earlistTime"])//self.aggregate_window["interval"]
            #print(self.aggregate_window["currentTime"]-self.aggregate_window["earlistTime"])
            #print(movewindow)
            self.aggregate_window["earlistTime"]=self.aggregate_window["currentTime"]
            if movewindow>len(self.aggregate_window["vaules"]):
                """
                The new record is futher away than the whole sliding window, 
                so do not need 
                """
                movewindow=len(self.aggregate_window["vaules"])
            for y in range(0,movewindow):
                #if movewindow>1:
                toretrun.append("window")
                toretrun.append(copy.copy(self.doCalculation(False)))
                #if len(toretrun[-1]) !=0:
                    #if toretrun[-1][-1][-2][0]!=0:
                        #print("nei")
                        #print(toretrun[-1][-1][-2][0]) 
                if self.startcounter<len(self.aggregate_window["vaules"]):
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

    def doCalculation(self,end): 
        
        #TODO
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
            countuniqebiflow+=1
            #if uniqebiflow[biflowkey]["checkKey"] in uniqebiflow.keys():
            if uniqebiflow[biflowkey]["checkKey"] in uniqebiflow.keys() and uniqebiflow[uniqebiflow[biflowkey]["checkKey"]]["foundBiFlow"]==False:
                uniqebiflow[uniqebiflow[biflowkey]["checkKey"]]["foundBiFlow"]=True
                uniqebiflow[biflowkey]["foundBiFlow"]=True
                
                uniqebiflowcounter.append([uniqebiflow[biflowkey]["packets"]+uniqebiflow[uniqebiflow[biflowkey]["checkKey"]]["packets"],
                                           uniqebiflow[biflowkey]["syn"]+uniqebiflow[uniqebiflow[biflowkey]["checkKey"]]["syn"]]) #TODO add the other side
            else:
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

        thereisOneAttack=[0] #TODO should this been on the whole 
        for x in range(0,len(self.aggregate_window["vaules"])):
            totalpackets+=self.aggregate_window["vaules"][x]["packets"]
            totalBytes+=self.aggregate_window["vaules"][x]["bytes"]
            totalFlows+=len(self.aggregate_window["vaules"][x]["currentRecs"])
            totalicmp+=self.aggregate_window["vaules"][x]["icmp"]
            totalicmpDUnreachable+=self.aggregate_window["vaules"][x]["Destination unreachable"]
            for rec in self.aggregate_window["vaules"][x]["currentRecs"]:
                isThereOneAttack =self.setIsAttack(rec)
                if isThereOneAttack!=0:
                    if thereisOneAttack[0]==0:
                        thereisOneAttack[0]=isThereOneAttack
                    elif isThereOneAttack not in thereisOneAttack:
                        thereisOneAttack.append(isThereOneAttack)
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
        
        #TODO handle that there might be zero entropy, (syn can be 0)
        arrayToAdd=[]
        listofprobability=[]
        listofprobability2=[]
        totalsyns=0
        for x in uniqetotalsourceIP.values():
            listofprobability.append(x["packets"]/totalpackets)
            #listofprobability2.append(x["syn"]/totalpackets)
            if x["syn"]!=0:
                listofprobability2.append(x["syn"])
                totalsyns+=x["syn"]
        entropySip=self.entropyCal(listofprobability)
        entropyRateSip=entropySip/len(uniqetotalsourceIP)
        #entropySipSyn=self.entropyCal(listofprobability2)
        
        listofprobability3=[]
        for x in listofprobability2:
            listofprobability3.append(x/totalsyns)
        if len(listofprobability3)==0:
            entropySipSyn=0
        else:
            entropySipSyn=self.entropyCal(listofprobability3)
    
        listofprobability=[]
        listofprobability2=[]
        totalsyns=0
        for x in uniqedestinationIP.values():
            listofprobability.append(x["packets"]/totalpackets)
            #listofprobability2.append(x["syn"]/totalpackets)
            if x["syn"]!=0:
                listofprobability2.append(x["syn"])
                totalsyns+=x["syn"]
        entropyDip=self.entropyCal(listofprobability)
        entropyRateDip=entropyDip/len(uniqedestinationIP)#TODO it might be worth it to look at all the size from the lowest to the highst
        
        listofprobability3=[]
        for x in listofprobability2:
            listofprobability3.append(x/totalsyns)
        if len(listofprobability3)==0:
            entropyDipSyn=0
        else:
            entropyDipSyn=self.entropyCal(listofprobability3)
        
        #entropyDipSyn=self.entropyCal(listofprobability2)

        listofprobability=[]
        for x in uniqepacketsize.values():
            listofprobability.append(x/totalpackets)
        entropyPacketsize=self.entropyCal(listofprobability)
        entropyRatePacketsize=entropyPacketsize/len(uniqepacketsize)
        
        listofprobability=[]
        listofprobability2=[]

        totalsyns=0
        for x in uniqebiflowcounter: #TODO Has to also add the ones that is not part of biflow, meaning which have only traffic one side 
        # This now only handles par f biflows    
            listofprobability.append(x[0]/totalpackets)
            #TODO The syn check is wrong, I belive. I think I need somehitn other than /totalpackets, becasue this is not the only range, the problilty does not add to 1, which I blive it should
            if x[1]!=0:
                #listofprobability2.append(x[1]/totalpackets)
                listofprobability2.append(x[1])
                totalsyns+=x[1]
        #if len(listofprobability)==2135:

        #    print(listofprobability)
        entropyBiflow=self.entropyCal(listofprobability) #TODO error
        entropyRateBiflow=entropyPacketsize/len(uniqebiflowcounter)
        #entropyBiflowSyn=self.entropyCal(listofprobability2)


        listofprobability3=[]
        for x in listofprobability2:
            listofprobability3.append(x/totalsyns)
        if len(listofprobability3)==0:
            entropyBiflowSyn=0
        else:
            entropyBiflowSyn=self.entropyCal(listofprobability3)
            #print(listofprobability2)
        countBiflow=len(uniqebiflowcounter)

        #if thereisOneAttack[0]!=0:
        #    print(thereisOneAttack)
            #print(len(self.aggregate_window["vaules"][-1]["currentRecs"]))

        #print(self.aggregate_window["vaules"][0]["currentRecs"])
        if end==False:
            for rec in self.aggregate_window["vaules"][-1]["currentRecs"]:
                #
                
                arrayToAdd.append([rec.stime, rec.etime, int(rec.sip), int(rec.dip), rec.sport, rec.dport, rec.protocol, rec.packets, rec.bytes, 
                                    int(rec.tcpflags.fin), int(rec.tcpflags.syn), int(rec.tcpflags.rst), int(rec.tcpflags.psh), int(rec.tcpflags.ack), 
                                    int(rec.tcpflags.urg), int(rec.tcpflags.ece), int(rec.tcpflags.cwr), rec.duration/datetime.timedelta(milliseconds=1), int(rec.nhip),#index 18
                                    totalFlows,entropySip,entropyRateSip,entropyDip,entropyRateDip,entropyPacketsize,
                                    entropyRatePacketsize,entropyBiflow,entropyRateBiflow,totalicmp,totalicmprate,
                                    totalBytes,totalpackets,#31
                                    entropyBiflowSyn,entropySipSyn,entropyDipSyn,
                                    countBiflow,HigstNumberOfSyn,HigstNumberOfURGPSHFIN,totalicmpDUnreachable,thereisOneAttack,
                                    rec.sensor_id])
        else:
            for window in self.aggregate_window["vaules"]:
                for rec in window["currentRecs"]:
                    arrayToAdd.append([rec.stime, rec.etime, int(rec.sip), int(rec.dip), rec.sport, rec.dport, rec.protocol, rec.packets, rec.bytes, 
                                        int(rec.tcpflags.fin), int(rec.tcpflags.syn), int(rec.tcpflags.rst), int(rec.tcpflags.psh), int(rec.tcpflags.ack), 
                                        int(rec.tcpflags.urg), int(rec.tcpflags.ece), int(rec.tcpflags.cwr), rec.duration/datetime.timedelta(milliseconds=1), int(rec.nhip),#index 18
                                        totalFlows,entropySip,entropyRateSip,entropyDip,entropyRateDip,entropyPacketsize,
                                        entropyRatePacketsize,entropyBiflow,entropyRateBiflow,totalicmp,totalicmprate,
                                        totalBytes,totalpackets,#31
                                        entropyBiflowSyn,entropySipSyn,entropyDipSyn,
                                        countBiflow,HigstNumberOfSyn,HigstNumberOfURGPSHFIN,totalicmpDUnreachable,thereisOneAttack,
                                        rec.sensor_id])
            

        #TODO add this vaules into the comparison window
        """ vaules to add

        These are not part of the fields for RF:
        entropyBiflowSyn,entropySipSyn,entropyDipSyn,countBiflow,HigstNumberOfSyn,HigstNumberOfURGPSHFIN,totalicmpDUnreachable,

        Not Threshold:
            Total Flows #TODO add to Threshold

        Used in both:
            entropySip,
            entropyRateSip,
            entropyDip
            entropyRateDip
            entropyPacketsize,
            entropyRatePacketsize
            entropyBiflow,
            entropyRateBiflow,
            totalBytes
            totalpackets
            totalicmp
            totalicmprate
        

        Threshold: #TODO add all to 
            HigstNumberOfSyn
            HigstNumberOfURGPSHFIN
            countBiflow
            totalicmpDUnreachable
            entropyBiflowSyn,
            entropySipSyn,
            entropyDipSyn,
        
        
        """
        self.vaulesToCompare={"entropySip":entropySip,"entropyRateSip":entropyRateSip,"entropyDip":entropyDip,"entropyRateDip":entropyRateDip,"entropyPacketsize":entropyPacketsize,
                                   "entropyRatePacketsize":entropyRatePacketsize,"entropyBiflowSyn":entropyBiflowSyn,"entropySipSyn":entropySipSyn,"entropyDipSyn":entropyDipSyn,
                                   "entropyBiflow":entropyBiflow,"entropyRateBiflow":entropyRateBiflow,"HigstNumberOfSyn":HigstNumberOfSyn,"HigstNumberOfURGPSHFIN":HigstNumberOfURGPSHFIN,
                                   "countBiflow":countBiflow,"totalicmpDUnreachable":totalicmpDUnreachable,"totalBytes":totalBytes,"totalpackets":totalpackets,"totalicmp":totalicmp,
                                   "totalicmprate":totalicmprate, "isAtttack":thereisOneAttack, "currenttime": self.aggregate_window["currentTime"], "totalflows":totalFlows }
        

        return arrayToAdd                 

    
        

    def entropyCal(self,listofprobability):
        #sum=0
        #if len(listofprobability)==0:
        #    print("hei")
        temp=[]
        for x in range(0,len(listofprobability)):
            temp.append(listofprobability[x]**self.orderEntropy)
        #for x in listofprobability:
        #    sum+=x**self.orderEntropy
        #if sum==0:
        #    print(listofprobability)
        #return 1/(1-self.orderEntropy)*np.log2(sum)
        return 1/(1-self.orderEntropy)*np.log2(sum(temp))

    def setIsAttack(self,rec):
        isAttackFlow=0
        #if rec.sensor=="isAttack": #TODO why does this not work
        #    isAttackFlow=1
        if rec.sensor_id in [32531,32532,32533,32534,32535,32536,32537,32538]:
            isAttackFlow=rec.sensor_id
        return isAttackFlow

    def removeFromSliding_window(self):
        #TODO create the data to retrun from the sliding_window, can use packets in all aggregate_window to see if aggregate_window is complete
        #self.x+=len(self.aggregate_window["vaules"][-1]["currentRecs"])
        for x in range(1,len(self.aggregate_window["vaules"])):
            self.aggregate_window["vaules"][-x]=copy.copy(self.aggregate_window["vaules"][-(x+1)])
            #self.aggregate_window["vaules"][-x]=self.aggregate_window["vaules"][-(x+1)]
        self.aggregate_window["vaules"][0]={"sourceIP":{},"packets":0,"destinationIP":{},"bytes":0,"packetsize":{},"currentRecs":[],
                                            "biflow":{},"icmp":0,"Destination unreachable":0}
        if len(self.comparison_window["vaules"])>0:
            self.removeFromComparison_window()
        #self.aggregate_window["vaules"][0]["currentRecs"]=[]

    def removeFromComparison_window(self):
        for x in range(1,len(self.comparison_window["vaules"])):
            self.comparison_window["vaules"][-x]=self.comparison_window["vaules"][-(x+1)]
        self.comparison_window["vaules"][0]= copy.copy(self.vaulesToCompare)

    def checkIfpastedSliding_window(self):
        #print(self.aggregate_window["interval"])
        #print(self.aggregate_window["currentTime"]-self.aggregate_window["earlistTime"])
        if self.aggregate_window["interval"]<self.aggregate_window["currentTime"]-self.aggregate_window["earlistTime"]: 
            return True
        else:
            return False

    def getcurrentvaules(self):
        return self.vaulesToCompare

    def findThreasholds(self,end):
        totalentropySip=0
        totalentropyRateSip=0
        totalentropyDip=0
        totalentropyRateDip=0
        totalentropyPacketsize=0
        totalentropyRatePacketsize=0
        totalentropyBiflowSyn=0
        totalentropySipSyn=0
        TotalentropyDipSyn=0
        totalentropyBiflow=0
        totalentropyRateBiflow=0
        #HigstNumberOfSyn=0#self.vaulesToCompare["HigstNumberOfSyn"] #this should only compare this value
        #HigstNumberOfURGPSHFIN=0#self.vaulesToCompare["HigstNumberOfURGPSHFIN"] #this should only compare this value
        TotalcountBiflow=0
        totaltotalicmpDUnreachable=0
        countTotalBytes=0 #this should look at the change
        countTotalpackets=0#this should look at the change
        countTotalicmp=0#this should look at the change
        countTotalicmprate=0#this should look at the change
        countHigstNumberOfSyn=0
        countHigstNumberOfURGPSHFIN=0
        counttotalFlows=0
        

        if end:
            self.removeFromComparison_window()
        

        isattack=self.comparison_window["vaules"][0]["isAtttack"]
        for x in range(1,len(self.comparison_window["vaules"])):
            totalentropySip+=self.comparison_window["vaules"][x]["entropySip"]  
            totalentropyRateSip +=self.comparison_window["vaules"][x]["entropyRateSip"]
            totalentropyDip +=self.comparison_window["vaules"][x]["entropyDip"]
            totalentropyRateDip+=self.comparison_window["vaules"][x]["entropyRateDip"]
            totalentropyPacketsize+=self.comparison_window["vaules"][x]["entropyPacketsize"]
            totalentropyPacketsize+=self.comparison_window["vaules"][x]["entropyRatePacketsize"]

            totalentropyBiflowSyn+=self.comparison_window["vaules"][x]["entropyBiflowSyn"]
            totalentropySipSyn+=self.comparison_window["vaules"][x]["entropySipSyn"]
            TotalentropyDipSyn+=self.comparison_window["vaules"][x]["entropyDipSyn"]
            totalentropyBiflow+=self.comparison_window["vaules"][x]["entropyBiflow"]
            totalentropyRateBiflow+=self.comparison_window["vaules"][x]["entropyRateBiflow"]
            TotalcountBiflow+=self.comparison_window["vaules"][x]["countBiflow"]
            totaltotalicmpDUnreachable+=self.comparison_window["vaules"][x]["totalicmpDUnreachable"]
            countTotalBytes+=self.comparison_window["vaules"][x]["totalBytes"]
            countTotalpackets+=self.comparison_window["vaules"][x]["totalpackets"]
            countTotalicmp+=self.comparison_window["vaules"][x]["totalicmp"]
            countTotalicmprate+=self.comparison_window["vaules"][x]["totalicmprate"]
            counttotalFlows+self.comparison_window["vaules"][x]["totalflows"]


            countHigstNumberOfSyn+=self.comparison_window["vaules"][x]["HigstNumberOfSyn"]
            countHigstNumberOfURGPSHFIN+=self.comparison_window["vaules"][x]["HigstNumberOfURGPSHFIN"]
            #if self.comparison_window["vaules"][x]["HigstNumberOfSyn"]>HigstNumberOfSyn: 
            #    HigstNumberOfSyn=self.comparison_window["vaules"][x]["HigstNumberOfSyn"]            
            #if self.comparison_window["vaules"][x]["HigstNumberOfURGPSHFIN"]>HigstNumberOfURGPSHFIN: 
            #    HigstNumberOfURGPSHFIN=self.comparison_window["vaules"][x]["HigstNumberOfURGPSHFIN"]

        lenght =len(self.comparison_window["vaules"])
        entropySip=abs((totalentropySip/(lenght-1))-self.comparison_window["vaules"][0]["entropySip"] )
        entropyRateSip=abs((totalentropyRateSip/(lenght-1))-self.comparison_window["vaules"][0]["entropyRateSip"] )
        entropyDip=abs((totalentropyDip/(lenght-1))-self.comparison_window["vaules"][0]["entropyDip"] )
        entropyRateDip=abs((totalentropyRateDip/(lenght-1))-self.comparison_window["vaules"][0]["entropyRateDip"] )
        entropyPacketsize=abs((totalentropyPacketsize/(lenght-1))-self.comparison_window["vaules"][0]["entropyPacketsize"] )
        entropyRatePacketsize=abs((totalentropyRatePacketsize/(lenght-1))-self.comparison_window["vaules"][0]["entropyRatePacketsize"] )

        entropyBiflowSyn=abs((totalentropyBiflowSyn/(lenght-1))-self.comparison_window["vaules"][0]["entropyBiflowSyn"] )
        entropySipSyn=abs((totalentropySipSyn/(lenght-1))-self.comparison_window["vaules"][0]["entropySipSyn"] )
        entropyDipSyn=abs((TotalentropyDipSyn/(lenght-1))-self.comparison_window["vaules"][0]["entropyDipSyn"] )
        entropyBiflow=abs((totalentropyBiflow/(lenght-1))-self.comparison_window["vaules"][0]["entropyBiflow"] )
        entropyRateBiflow=abs((totalentropyRateBiflow/(lenght-1))-self.comparison_window["vaules"][0]["entropyRateBiflow"] )
        countBiflow=abs((TotalcountBiflow/(lenght-1))-self.comparison_window["vaules"][0]["countBiflow"] )
        totalicmpDUnreachable=abs((totaltotalicmpDUnreachable/(lenght-1))-self.comparison_window["vaules"][0]["totalicmpDUnreachable"] )
        totalBytes=abs((countTotalBytes/(lenght-1))-self.comparison_window["vaules"][0]["totalBytes"] )
        totalpackets=abs((countTotalpackets/(lenght-1))-self.comparison_window["vaules"][0]["totalpackets"] )
        totalicmp=abs((countTotalicmp/(lenght-1))-self.comparison_window["vaules"][0]["totalicmp"] )
        totalicmprate=abs((countTotalicmprate/(lenght-1))-self.comparison_window["vaules"][0]["totalicmprate"] )
        changeFromAverageTotalflows=abs((counttotalFlows/(lenght-1))-self.comparison_window["vaules"][0]["totalflows"] )

        totalHigstNumberOfSyn=abs((countHigstNumberOfSyn/(lenght-1))-self.comparison_window["vaules"][0]["HigstNumberOfSyn"] )
        totalHigstNumberOfURGPSHFIN=abs((countHigstNumberOfURGPSHFIN/(lenght-1))-self.comparison_window["vaules"][0]["HigstNumberOfURGPSHFIN"] )


        return {"entropySip":entropySip,"entropyRateSip":entropyRateSip,"entropyDip":entropyDip,"entropyRateDip":entropyRateDip,"entropyPacketsize":entropyPacketsize,
                                   "entropyRatePacketsize":entropyRatePacketsize,"entropyBiflowSyn":entropyBiflowSyn,"entropySipSyn":entropySipSyn,"entropyDipSyn":entropyDipSyn,
                                   "entropyBiflow":entropyBiflow,"entropyRateBiflow":entropyRateBiflow,"HigstNumberOfSyn":totalHigstNumberOfSyn,"HigstNumberOfURGPSHFIN":totalHigstNumberOfURGPSHFIN,
                                   "countBiflow":countBiflow,"totalicmpDUnreachable":totalicmpDUnreachable,"totalBytes":totalBytes,"totalpackets":totalpackets,"totalicmp":totalicmp,
                                   "totalicmprate":totalicmprate,"isAtttack":isattack,"currenttime": self.aggregate_window["currentTime"],"totalflows":changeFromAverageTotalflows}