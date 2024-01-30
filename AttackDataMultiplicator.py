from silk import *
import ipaddress
import copy
class AttackDataMultiplicator:       
    """
    Start the class with the silk file you to change with filePath
    The listtWithModifcationsClass incule a list of objet's of the InputToAttackDataMultiplicator
    each object in the list will create a new modified file
    """
    
    
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
        self.addSrc(parmeters)
        self.addBotnetRotationAlgorithm(parmeters)
        
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

    def addSrc(self,parmeters):
                #if "botsize" in parmeters.keys():
        try:
            srcs=self.checkSrc(parmeters["src"].copy())
            if len(srcs)>0:
                self.src = self.addCorrectNumberOfSrc(srcs)
            else:
                print("no accpecet src, so src is set to 192.168.56.11 -> (to botsize)")
                self.src = self.addCorrectNumberOfSrc(["192.168.56.11"])
        except KeyError:
            print("no src, so src is set to 192.168.56.11 -> (to botsize)")
            self.src = self.addCorrectNumberOfSrc(["192.168.56.11"])
        self.indexOfBotnetsize=0

    def addCorrectNumberOfSrc(self,srcs):
        if len(srcs) > self.botNetSize:
            srcs= self.removeSrc(srcs,self.botNetSize)
            return srcs
        elif len(srcs) < self.botNetSize:
            srcs= self.addMoreSrc(srcs,self.botNetSize)
            return srcs
        else:
            return srcs
        
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

    def checkSrc(self,srcs):
        tempsrc = srcs.copy()
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


#ia1 = InputToAttackDataMultiplicator({"botsize":8,"src":listOfSrc})
#ia2 = InputToAttackDataMultiplicator({"botsize":1,"src":"192.168.56.11"})
#ia2 = InputToAttackDataMultiplicator({"botsize":2,"src":listOfSrc})
#a1=AttackDataMultiplicator([ia1,ia2],"pathtofile","TCP_SYN_Flodd")

#print(ia1.src)
#print(ia1.botNetSize)

#print(ia2.src)
#print(ia2.botNetSize)


ia1 = InputToAttackDataMultiplicator({"botsize":4,"src":["192.168.2.2"]})
#ia2 = InputToAttackDataMultiplicator({"botsize":1,"src":["192.168.3.3"]})
a1=AttackDataMultiplicator([ia1],"GenratedAttacks/ext2ext-S0_20240125.11","TCP_SYN_Flodd")