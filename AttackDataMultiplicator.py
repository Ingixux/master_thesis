#from silk import *
import ipaddress
import datetime

class AttackDataMultiplicator:       
    """
    Start the class with the silk file you to change with filePath
    The listtWithModifcationsClass incule a list of objet's of the InputToAttackDataMultiplicator
    each object in the list will create a new modified file
    """

    #TODO add time start time end off all the flows: datetime.timedelta (datetime.resolution)
    def __init__(self, listtWithModifcationsClass, filePath, attack):
        self.filePath = filePath
        #self.attack= attack
        #self.numberOfOutputFiles=len(listtWithModifcationsClass)
        #self.listtWithModifcationsClass = listtWithModifcationsClass
        self.dicOfFileToModifcationsClass ={}
        for x in range(0, len(listtWithModifcationsClass)):
            self.dicOfFileToModifcationsClass["ModifiedAttackFiles/"+attack+str(x)]= [silkfile_open("ModifiedAttackFiles/"+attack+str(x), WRITE),listtWithModifcationsClass[x]]
            #self.dicOfFileToModifcationsClass["ModifiedAttackFiles/"+attack+str(x)]= ["test open ModifiedAttackFiles/"+attack+str(x),listtWithModifcationsClass[x]]
        self.modifyfile()
    """
    """
    def modifyfile(self):
        infile_r = silkfile_open(self.filePath, READ)
        for rec in infile_r:   
            #print (rec)
            #for setFileModclass in self.dicOfFileToModifcationsClass.values():
                #temprec=copy.deepcopy(rec)
            #    temprec=rec #TODO Do I need a deep copy as I am chaning the 
            #    temprec =self.modifySIPRecord(temprec,setFileModclass)
            #    setFileModclass[0].write(temprec)
            for nameofset in self.dicOfFileToModifcationsClass.keys():
                #temprec=copy.deepcopy(rec)
                temprec=rec #TODO Do I need a deep copy as I am chaning the 
                temprec =self.modifySIPRecord(temprec,nameofset)
                temprec =self.modifyNIPRecord(temprec,nameofset)
                temprec =self.modifyDIPRecord(temprec,nameofset)
                self.dicOfFileToModifcationsClass[nameofset][0].write(temprec)
        self.closeAllFiles()
        infile_r.close()
        pass    
    
    def closeAllFiles(self):
        for set in self.dicOfFileToModifcationsClass.values():
            set[0].close()

    def modifySIPRecord(self,rec,nameofset):
        if self.dicOfFileToModifcationsClass[nameofset][1].botnetRotationAlgorithm =="standard":
           rec=self.modifySIPRecordstander(rec,nameofset)
        return rec
    
    def modifyDIPRecord(self,rec,nameofset):
        rec.dip = IPAddr(self.dicOfFileToModifcationsClass[nameofset][1].dst[0])
        return rec
    def modifyNIPRecord(self,rec,nameofset):
        rec.nhip = IPAddr(self.dicOfFileToModifcationsClass[nameofset][1].nIP[0])
        return rec

    def modifySIPRecordstander(self,rec,nameofset):
        index= self.dicOfFileToModifcationsClass[nameofset][1].indexOfBotnetsize
        ip = self.dicOfFileToModifcationsClass[nameofset][1].src[index]
        Botnetsize =self.dicOfFileToModifcationsClass[nameofset][1].botNetSize
        rec.sip = IPAddr(ip)
        index +=1
        if Botnetsize <= index:
            index =0
        self.dicOfFileToModifcationsClass[nameofset][1].indexOfBotnetsize = index
        return rec

class InputToAttackDataMultiplicator:
    """
    This is a class that create a object with the parmeters to use when modfiing attack data in Silk format
    Input:
    The varible parmeters is a dictionary and can inculde:
        - int of botsize with key 'botsize'
            -if no valid or no botsize is entered then it is set to 1
        - list of unqiue src addresses with key 'src'
            - if src is not a ip it will be removed
            - if there are more src then botsize, then ip from src will be remove to match botsize
            - if there are less src then botsize, then unqiue ips will be added to src to match botsize
    """
    def __init__(self, parmeters):
        self.addBotNetSize(parmeters)
        self.addListOfIPs(parmeters,"src")
        self.addBotnetRotationAlgorithm(parmeters)
        self.addListOfIPs(parmeters,"dst")
        self.addListOfIPs(parmeters,"nIP")
        self.addStartAndEndOfAttack(parmeters,"stratTimeOfAttack")
        self.addStartAndEndOfAttack(parmeters,"endTimeOfAttack")
        
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
            if len(listOfips)>0:
                self.nIP = listOfips
            else:
                self.printDefault(["192.168.55.11"],typOfIP +" IP")
                self.nIP= ["192.168.55.11"]
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
        try:
            self.botnetRotationAlgorithm = parmeters["botnet_rotation_algorithm"]
        except KeyError:
            print("no botnet_rotation_algorithm, so set to standard")
            self.botnetRotationAlgorithm= "standard"
            
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
    tempIps=[]
    for ip in ips:
        if not ip in tempIps:
            tempIps.append(ip)
    return tempIps
        
listOfSrc=["192.168.56.11","192.168.56.12","192.168.56.13", "192.168.56.13"]
listOfSrc=checkUniqeIP(listOfSrc)


start = datetime.datetime(2024, 2, 4, 2, 1, 50, 10000)
end = datetime.datetime(2024, 2, 4, 2, 1, 50, 0)
#print(start)
#print(start+datetime.timedelta(microseconds=100000))
#print(start+datetime.datetime(start.year, start.month, start.day, start.hour, start.min, start.second, 10000))



#ia1 = InputToAttackDataMultiplicator({"botsize":4,"src":listOfSrc, "stratTimeOfAttack" : start, "endTimeOfAttack"  : end})
ia1 = InputToAttackDataMultiplicator({"botsize":4,"src":listOfSrc})
#ia2 = InputToAttackDataMultiplicator({"botsize":1,"src":["192.168.56.11"], "stratTimeOfAttack" : start , "endTimeOfAttack"  : end })
#ia2 = InputToAttackDataMultiplicator({"botsize":2,"src":listOfSrc})
#a1=AttackDataMultiplicator([ia1,ia2],"pathtofile","TCP_SYN_Flodd")

#print(ia1.src)
#print(ia1.botNetSize)
print(ia1.stratTimeOfAttack)
print(ia1.endTimeOfAttack)
#print(ia2.src)
#print(ia2.botNetSize)


#ia1 = InputToAttackDataMultiplicator({"botsize":4,"src":["192.168.2.2"], "stratTimeOfAttack" : start , "endTimeOfAttack"  : end})
#ia2 = InputToAttackDataMultiplicator({"botsize":1,"src":["192.168.3.3"]})
#a1=AttackDataMultiplicator([ia1],"GenratedAttacks/ext2ext-S0_20240125.11","TCP_SYN_Flodd")