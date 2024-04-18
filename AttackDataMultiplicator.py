from silk import *
import ipaddress
import datetime
import os
import subprocess

#rwsort --fields=stime --input-pipe=/home/kali/data/ModifiedAttackFiles/TCP_SYN_Flodd0 --output-path=/home/kali/data/ModifiedAttackFiles/sorted
class AttackDataMultiplicator:       
 
    #TODO create a file assoted with the attack where informaation about the attack is stored (start time, endtime, botsize, sourceip?, dst ip, nhip)
    #TODO create a check that the first flow in a bi is from the Attacker VM, (as this file comes sorted, this should not be a problem, But I am not 100%, that it isn't a problem)
    #TODO Add code so that it will be easy for a new user to modify and other type of record type. 
    #TODO add the possiblety to remove files that exits, when oping to write
    """
    Start the class with the silk file you to change with filePath
    The listtWithModifcationsClass incule a list of objet's of the InputToAttackDataMultiplicator
    the attack varible is the name of the attack gets added to the new file
    The dicOfFileToModifcationsClass is a dictionary with the name of a modified attack as the key, 
    and key points to a list where the first entry is the file of it that name 
    and the second entry is the AttackDataMultiplicator object, which acts on the file 
    The dicToMatchBiFlows is a dictionary with 3 layers (nested nested dictionary), 
    where the key for the first layer is vaules (sip,dip,sport,dport,protcol) gathered from the first flow in biflow
    flow are added to the dictionary, if there is no match in the dictionary if you swap source and destination of the new flow
    The key point to a new dictionary, where the key of the second layer is same as the key of dicOfFileToModifcationsClass.
    While the last key is the diffrent vaule being modified
    These can then be used to modify if this is flow is apart of a biflow
    After both records of a biflow has been modified, 
    then all vaules associated with this biflow are removed from dicToMatchBiFlows
    Create one new file for each of the AttackDataMultiplicator object, 
    where that AttackDataMultiplicator object will store the modified attack
    Adds the name of AttackDataMultiplicator object to unqiename name,
    if two share the same name, 
    the file will get a number in the name instead of the name
    This to aviod creating files with the same name 
    Init starts modifyfile function
    """
    def __init__(self, listtWithModifcationsClass, filePath, attack):
        self.filePath = filePath
        #self.attack= attack
        #self.numberOfOutputFiles=len(listtWithModifcationsClass)
        #self.listtWithModifcationsClass = listtWithModifcationsClass
        self.dicOfFileToModifcationsClass ={}
        self.dicToMatchBiFlows={}
        unqiename=[]
        for x in range(0, len(listtWithModifcationsClass)):
            name =listtWithModifcationsClass[x].name
            unqiename.append(name)
            pathToFile="data/ModifiedAttackFiles/"+attack+str(x)
            if os.path.isfile(pathToFile):
                os.remove(pathToFile)
            if name in unqiename:
                self.dicOfFileToModifcationsClass[pathToFile]= [silkfile_open(pathToFile, WRITE),listtWithModifcationsClass[x]]
            else:
                self.dicOfFileToModifcationsClass[pathToFile]= [silkfile_open(pathToFile, WRITE),listtWithModifcationsClass[x]]
            #self.dicOfFileToModifcationsClass["ModifiedAttackFiles/"+attack+str(x)]= ["test open ModifiedAttackFiles/"+attack+str(x),listtWithModifcationsClass[x]]
        self.modifyfile()

    def sortFile(self):
        x=subprocess.call("rm temp.rw", shell=True)
        x=subprocess.call("rwsort --fields=stime --output-path=temp.rw "+self.filePath+"", shell=True)

    def modifyfile(self):
        """
        Modifiles based on the AttackDataMultiplicator object.
        For each record in the orginal silk file, 
        each AttackDataMultiplicator object will modify the record and add it to the corresponding file
        after all AttackDataMultiplicator object have modified the record, 
        then it moves to the next record 
        """
        #infile_r = silkfile_open(self.filePath, READ)
        #self.count =0
        #for rec in infile_r: 
        #    self.count+=1
        self.counterUnqiueFlows =0
        #infile_r.close()
        #infile_r = silkfile_open(self.filePath, READ)
        self.sortFile()
        infile_r = silkfile_open("temp.rw", READ)
        for rec in infile_r:
            isbiflow=False
            checkKeyOfBiFlow = str(rec.dip)+ str(rec.sip) + str(rec.dport) +str(rec.sport) +str(rec.protocol)
            keyOfBiFlow= ""
            if checkKeyOfBiFlow in self.dicToMatchBiFlows.keys():
                keyOfBiFlow =checkKeyOfBiFlow
                isbiflow=True
            else:
                self.counterUnqiueFlows +=1
                keyOfBiFlow= str(rec.sip) + str(rec.dip) +str(rec.sport) + str(rec.dport) +str(rec.protocol)
                self.dicToMatchBiFlows[keyOfBiFlow]= {}
            #print (rec)
            #for setFileModclass in self.dicOfFileToModifcationsClass.values():
                #temprec=copy.deepcopy(rec)
            #    temprec=rec #TODO Do I need a deep copy as I am chaning the 
            #    temprec =self.modifySIPRecord(temprec,setFileModclass)
            #    setFileModclass[0].write(temprec)
            for nameofset in self.dicOfFileToModifcationsClass.keys():
                if isbiflow == False:
                    self.dicToMatchBiFlows[keyOfBiFlow][nameofset] = {}
                #temprec=copy.deepcopy(rec)
                temprec=rec #TODO Do I need a deep copy as I am chaning the 
                temprec =self.modifySIPRecord(temprec,nameofset,keyOfBiFlow,isbiflow)
                temprec =self.modifyNIPRecord(temprec,nameofset,keyOfBiFlow,isbiflow)
                temprec =self.modifyDIPRecord(temprec,nameofset,keyOfBiFlow,isbiflow)
                temprec =self.modifystime(temprec,nameofset,keyOfBiFlow,isbiflow)
                temprec =self.modifyports(temprec,nameofset,keyOfBiFlow,isbiflow)
                temprec =self.modifyIsattack(temprec,nameofset,keyOfBiFlow,isbiflow)
                self.dicOfFileToModifcationsClass[nameofset][0].write(temprec)
            if isbiflow == True:
                self.dicToMatchBiFlows.pop(keyOfBiFlow)
        self.closeAllFiles()
        infile_r.close()
        pass    
    
    def modifyports(self,rec,nameofset,keyOfBiFlow,isbiflow):
        if isbiflow == True:
            rec.sport=self.dicToMatchBiFlows[keyOfBiFlow][nameofset]["dport"]
            rec.dport=self.dicToMatchBiFlows[keyOfBiFlow][nameofset]["sport"]
        self.addInfoToDicToMatchBiFlows("sport",rec.sport,nameofset,keyOfBiFlow,isbiflow)
        self.addInfoToDicToMatchBiFlows("dport",rec.dport,nameofset,keyOfBiFlow,isbiflow)
        return rec
    

    def modifyIsattack(self,rec,nameofset,keyOfBiFlow,isbiflow):
        """
        #TODO add a description of that this needs to be inline with the silk config files.
        """
        #rec.sensor=self.dicOfFileToModifcationsClass[nameofset][1].isAttack
        rec.sensor_id=self.dicOfFileToModifcationsClass[nameofset][1].isAttack 
        #32532
        return rec

    def addInfoToDicToMatchBiFlows(self,whatToAdd,valueToAdd,nameofset,keyOfBiFlow,isbiflow):
        """
        addes a vaule to dicToMatchBiFlows
        """
        if isbiflow == False:
            self.dicToMatchBiFlows[keyOfBiFlow][nameofset][whatToAdd] = valueToAdd

    def modifystime(self,rec,nameofset,keyOfBiFlow,isbiflow):
        """
        Will chose the methode for adding start time
        """
        if self.dicOfFileToModifcationsClass[nameofset][1].startTimeIncreasAlgorithm =="standard":
            rec=self.modifystimeStandard(rec,nameofset,keyOfBiFlow,isbiflow)
        if self.dicOfFileToModifcationsClass[nameofset][1].startTimeIncreasAlgorithm =="standardBasedOnBotnetsize":
            rec=self.modifystimestandardBasedOnBotnetsize(rec,nameofset,keyOfBiFlow,isbiflow)
        self.addInfoToDicToMatchBiFlows("stime",rec.stime,nameofset,keyOfBiFlow,isbiflow)
        return rec
    
    def modifystimestandardBasedOnBotnetsize(self,rec,nameofset,keyOfBiFlow,isbiflow):
        """
        incresses time between attack each time there have been botnetsize new biflows
        """
        if isbiflow == False:
            rec.stime = self.dicOfFileToModifcationsClass[nameofset][1].stratTimeOfAttack + self.dicOfFileToModifcationsClass[nameofset][1].TT1 + self.dicOfFileToModifcationsClass[nameofset][1].TBA * ((self.counterUnqiueFlows-1) // self.dicOfFileToModifcationsClass[nameofset][1].botNetSize)
        else:
            rec.stime = self.dicToMatchBiFlows[keyOfBiFlow][nameofset]["stime"] + self.dicOfFileToModifcationsClass[nameofset][1].TT2
        return rec
    
    def modifystimeStandard(self,rec,nameofset,keyOfBiFlow,isbiflow):
        """
        incresses time between attack by each uqnuie biflow
        """
        if isbiflow == False:
            rec.stime = self.dicOfFileToModifcationsClass[nameofset][1].stratTimeOfAttack + self.dicOfFileToModifcationsClass[nameofset][1].TT1 + self.dicOfFileToModifcationsClass[nameofset][1].TBA * self.counterUnqiueFlows
        else:
            rec.stime = self.dicToMatchBiFlows[keyOfBiFlow][nameofset]["stime"] + self.dicOfFileToModifcationsClass[nameofset][1].TT2
        return rec

    def closeAllFiles(self):
        """
        closes all files
        """
        for set in self.dicOfFileToModifcationsClass.values():
            set[0].close()

    def modifySIPRecord(self,rec,nameofset,keyOfBiFlow,isbiflow):
        """
        Will chose the methode for adding start time
        """
        if self.dicOfFileToModifcationsClass[nameofset][1].botnetRotationAlgorithm =="standard":
           rec=self.modifySIPRecordstander(rec,nameofset,keyOfBiFlow,isbiflow)
        self.addInfoToDicToMatchBiFlows("sip",rec.sip,nameofset,keyOfBiFlow,isbiflow)
        return rec
    
    def modifyDIPRecord(self,rec,nameofset,keyOfBiFlow,isbiflow):
        """
        changes the Dip, either to the dip in the InputToAttackDataMultiplicator class or the source of the associated biflow
        """
        if isbiflow == False:
            rec.dip = IPAddr(self.dicOfFileToModifcationsClass[nameofset][1].dst[0])
        else:
            rec.dip = self.dicToMatchBiFlows[keyOfBiFlow][nameofset]["sip"]
        self.addInfoToDicToMatchBiFlows("dip",rec.dip,nameofset,keyOfBiFlow,isbiflow)
        return rec
    
    def modifyNIPRecord(self,rec,nameofset,keyOfBiFlow,isbiflow):
        """
        changes the nhip, either to frist or second vaule of nhip in the InputToAttackDataMultiplicator class, 
        the frist flow in a biflow gets the first vaule the other gets the second 
        """
        if isbiflow ==False:
            rec.nhip = IPAddr(self.dicOfFileToModifcationsClass[nameofset][1].nIP[0])
        else:
            rec.nhip = IPAddr(self.dicOfFileToModifcationsClass[nameofset][1].nIP[1])
        #self.addInfoToDicToMatchBiFlows("nhip",rec.nhip,nameofset,keyOfBiFlow,isbiflow)
        return rec

    def modifySIPRecordstander(self,rec,nameofset,keyOfBiFlow,isbiflow):
        """
        changes the sip, for new biflow
        it will move through the sip in the botnet sequentially 
        and start at the begining again when it has reach the end 
        if not new, it will add the destiation of the associated biflow
        """
        if isbiflow == False:
            index= self.dicOfFileToModifcationsClass[nameofset][1].indexOfBotnetsize
            ip = self.dicOfFileToModifcationsClass[nameofset][1].src[index]
            Botnetsize =self.dicOfFileToModifcationsClass[nameofset][1].botNetSize
            rec.sip = IPAddr(ip)
            index +=1
            if Botnetsize <= index:
                index =0
            self.dicOfFileToModifcationsClass[nameofset][1].indexOfBotnetsize = index
        else:
            rec.sip = self.dicToMatchBiFlows[keyOfBiFlow][nameofset]["dip"]
        return rec

class InputToAttackDataMultiplicator:
    """
    This is a class that create a object with the parmeters to use when modfiing attack data in Silk format
    Input:
    The varible parmeters is a dictionary and can inculde:
        - int of botsize with key 'botsize'
            - the can be 1 -> ,
            - if no valid or no botsize is entered then it is set to 1
        - list of unqiue src addresses with key 'src'
            - if src is not a ip it will be removed
            - if there are more src then botsize, then ip from src will be remove to match botsize
            - if there are less src then botsize, then unqiue ips will be added to src to match botsize
        - list of dst addresses with key 'dst'
            - the list can have 1 -> , entries, 
            - if dst is not a ip it will be removed
            - if none are provied a default is set
        - list of next hop ip addresses with key 'nhip'
            - the list can have 2 -> , entries, 
            - if nhip is not a ip it will be removed
            - if less tahn two are provided, defaults are added to get to two entries
        - a String with the algortim to use to get through the botnet, has key "botnet_rotation_algorithm"
            - if none are provied a default (Standard) is set
        - a String with the algortim to use to set starttime of flow, has key "startTimeIncreasAlgorithm"
            - if none are provied a default (Standard) is set
        - a Datatime.datatime object of when the attack flows should start, has key "stratTimeOfAttack"
            - if none are provied a default (earlist possible by Datatime.datatime) is set
        - a Datatime.datatime object of when the attack flows should end, has key "endTimeOfAttack"
            - if none are provied a default (earlist possible by Datatime.datatime) is set
        - a Datatime.timedelta object of the travel time from attacker to netflow capture point, has key "TT1"
            - if none are provied a default (1000 microsecond) is set
        - a Datatime.timedelta object of the travel time from netflow capture poin to vicitm and back again, has key "TT2"
            - if none are provied a default (1000 microsecond) is set
        - a Datatime.timedelta object of the Time Between Attacks packets sendt from attacker, has key "TBA"
            - if none are provied a default (1000 microsecond) is set
        - a string with the name of configure class, has key "name" 
        - a string which will be added to the sensor name, has key "isattack"
            - if none are provied a default (isattack) is set 
        
        #TODO add check if valide stratTimeOfAttack, endTimeOfAttack, TT1, TT2, TBA and name
    """
    def __init__(self, parmeters):
        self.addBotNetSize(parmeters)
        self.addListOfIPs(parmeters,"src")
        self.addBotnetRotationAlgorithm(parmeters)
        self.addListOfIPs(parmeters,"dst")
        self.addListOfIPs(parmeters,"nIP")
        self.addStartAndEndOfAttack(parmeters,"stratTimeOfAttack")
        self.addStartAndEndOfAttack(parmeters,"endTimeOfAttack")
        self.addTimes(parmeters,"TT1")
        self.addTimes(parmeters,"TT2")
        self.addTimes(parmeters,"TBA")
        self.addStartTimeIncreasAlgorithm(parmeters)
        self.addName(parmeters)
        self.addisAttack(parmeters)

    def addisAttack(self,parmeters):
        try:
            if type(parmeters["isAttack"]) != int:
                raise KeyError
            else:
                self.isAttack =parmeters["isAttack"]
        except KeyError:
            self.isAttack=32532
        
    def addName(self,parmeters):
        try:
            self.name= parmeters["name"]
        except KeyError:
            self.name="default"

    def addTimes(self,parmeters,time):
        try:
            vaule= parmeters[time]
        except KeyError:
            vaule = datetime.timedelta(microseconds=10000)
            self.printDefault(["to earliest of the datetime object"],time)
        if (time) =="TT1":
             self.TT1=vaule
        elif (time) =="TT2":
             self.TT2=vaule
        elif (time) =="TBA":
             self.TBA=vaule

    def addStartAndEndOfAttack(self,parmeters,startOrEnd):
        try:
            vaule= parmeters[startOrEnd]
        except KeyError:
            vaule = datetime.datetime.min
            self.printDefault(["to earliest of the datetime object"],startOrEnd)
        self.setstartorend(vaule,startOrEnd)

    def setstartorend(self,time,startOrEnd):
        if startOrEnd == "stratTimeOfAttack":
            self.stratTimeOfAttack=time
        elif startOrEnd == "endTimeOfAttack":
            if time>self.stratTimeOfAttack:
                self.endTimeOfAttack=time
            else:
                self.printDefault(["1 min after stratTimeOfAttack"],"endTimeOfAttack")
                self.endTimeOfAttack=self.stratTimeOfAttack +datetime.timedelta(minutes=1)#datetime.timedelta(microseconds=100000)
    
    def setips(self,listOfips,typOfIP):
        if typOfIP == "src":
            if len(listOfips)>0:
                self.addCorrectNumberOfSrc(listOfips)
            else:
                self.printDefault(["192.168.55.11 -> botnetsize"],typOfIP +" IP")
                self.addCorrectNumberOfSrc(["192.168.56.11"])
        elif typOfIP == "nIP":
            if len(listOfips)>1:
                self.nIP = listOfips
            elif len(listOfips)>0:
                if "192.168.55.11" in listOfips:
                    self.printDefault(["192.168.54.11"],typOfIP +" IP, (only one enter)")
                    listOfips.append("192.168.54.11")
                else:
                    self.printDefault(["192.168.55.11"],typOfIP +" IP (only one enter)")
                    listOfips.append("192.168.55.11")             
                self.nIP = listOfips
            else:
                self.printDefault(["192.168.55.11 and 192.168.54.11"],typOfIP +" IP")
                self.nIP= ["192.168.55.11","192.168.54.11"]
        elif typOfIP == "dst":
            if len(listOfips)>0:
                self.dst= listOfips
            else:
                self.printDefault(["192.168.57.11"],typOfIP +" IP")
                self.dst= ["192.168.57.11"]

    def printDefault(self,printFirstVauleInList,typeOfAttribute):
        print("no or no vaild, "+typeOfAttribute+", so set to "+printFirstVauleInList[0])

    def addListOfIPs(self,parmeters,typOfIP):
        try:
            listOfips=self.checkListOfIPs(parmeters[typOfIP])
        except KeyError:
            listOfips = []
        self.setips(listOfips,typOfIP)
        
    def addBotnetRotationAlgorithm(self,parmeters):
        accpecetAlgorithms = ["standard"]
        try:
            if parmeters["botnet_rotation_algorithm"] in accpecetAlgorithms:
                self.botnetRotationAlgorithm = parmeters["botnet_rotation_algorithm"]
            else:
                raise KeyError
        except KeyError:
            self.printDefault(["standard"],"botnet_rotation_algorithm")
            self.botnetRotationAlgorithm= "standard"

    def addStartTimeIncreasAlgorithm(self,parmeters):
        accpecetAlgorithms = ["standard","standardBasedOnBotnetsize"]
        try:
            if parmeters["startTimeIncreasAlgorithm"] in accpecetAlgorithms:
                self.startTimeIncreasAlgorithm = parmeters["startTimeIncreasAlgorithm"]
            else:
                raise KeyError
        except KeyError:
            self.printDefault(["standard"],"startTimeIncreasAlgorithm")
            self.startTimeIncreasAlgorithm= "standard"
         
    def addBotNetSize(self,parmeters):
        try:
            if self.checkBotNetSize(parmeters["botsize"]):
                self.botNetSize = parmeters["botsize"]
            else:
                print("not accpecet botNetSize, so botNetSize is set to 1")
                self.botNetSize = 1
        except KeyError:
            print("no botNetSize, so botNetSize is set to 1")
            self.botNetSize = 1

    def addCorrectNumberOfSrc(self,srcs):
        self.indexOfBotnetsize=0
        if len(srcs) > self.botNetSize:
            srcs= self.removeSrc(srcs,self.botNetSize)
        elif len(srcs) < self.botNetSize:
            srcs= self.addMoreSrc(srcs,self.botNetSize)
        self.src=srcs
        
    def addMoreSrc(self,srcs,botnetsize):
        for x in range(0,botnetsize-len(srcs)):
            ip =ipaddress.ip_address(srcs[-1])+1
            while (str(ipaddress.IPv4Address(ip)) in srcs):
                ip+=1 
            srcs.append(str(ipaddress.IPv4Address(ip)))
        return srcs
    
    def removeSrc(self,srcs,botnetsize):
        tempsrc = srcs
        for x in range(0,len(srcs)-botnetsize):
            del tempsrc[-1]
        return tempsrc
    
    def checkListOfIPs(self,listOfSrc):
        tempsrc = listOfSrc.copy()
        for ip in tempsrc:
            if not self.isIP(ip):
                tempsrc.remove(ip)
        return tempsrc
    
    def isIP(self,ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    def checkBotNetSize(self,botNetSize):
        if not isinstance(botNetSize, int):
            return False
        if botNetSize < 1:
            return False
        else:
            return True
    
def checkUniqeIP(ips):
    """
    Used to check that the ips are unique
    """
    tempIps=[]
    for ip in ips:
        if not ip in tempIps:
            tempIps.append(ip)
    return tempIps
        
listOfSrc=["192.168.56.11","192.168.56.12","192.168.56.13", "192.168.56.13"]
listOfSrc=checkUniqeIP(listOfSrc)


start = datetime.datetime(2011, 1, 25, 12, 2, 20, 0)
end = datetime.datetime(2011, 1, 25, 12, 51, 0, 0)
#print(start)
#print(start+datetime.timedelta(microseconds=100000))
#print(start+datetime.datetime(start.year, start.month, start.day, start.hour, start.min, start.second, 10000))



#ia1 = InputToAttackDataMultiplicator({"botsize":4,"src":listOfSrc, "stratTimeOfAttack" : start, "endTimeOfAttack"  : end})
#ia1 = InputToAttackDataMultiplicator({"botsize":4,"src":listOfSrc})
#ia2 = InputToAttackDataMultiplicator({"botsize":1,"src":["192.168.56.11"], "stratTimeOfAttack" : start , "endTimeOfAttack"  : end })
#ia2 = InputToAttackDataMultiplicator({"botsize":2,"src":listOfSrc})
#a1=AttackDataMultiplicator([ia1,ia2],"pathtofile","TCP_SYN_Flodd")

#print(ia1.src)
#print(ia1.botNetSize)
#print(ia1.stratTimeOfAttack)
#print(ia1.endTimeOfAttack)
#print(ia2.src)
#print(ia2.botNetSize)


ia1 = InputToAttackDataMultiplicator({"botsize":9,"dst":["11.12.26.5"],"src":["192.168.2.2"], "nIP":["192.168.44.43","192.168.44.43"], "stratTimeOfAttack" : start , "endTimeOfAttack"  : end, "startTimeIncreasAlgorithm":"standardBasedOnBotnetsize"})
#ia2 = InputToAttackDataMultiplicator({"botsize":1,"src":["192.168.3.3"]})
a1=AttackDataMultiplicator([ia1],"data/GenratedAttacks/ext2ext-S0_20240125.12","TCP_SYN_Flodd")
#a1=AttackDataMultiplicator([ia1],"outfileattack.rw","TCP_SYN_Flodd")
