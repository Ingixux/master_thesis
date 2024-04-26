from silk import *
from FindFiles import FindFiles,Folderpathstructure
import random 

class GetTrafficPattern:
    def __init__(self,listoffiles):
        self.listoffiles=listoffiles
        self.dictofinfo={"sourceIP":{},"destinationIP":{},"nexthopip":{}}#{"sourceIP":{{192.168.57.11 : {"count" : 1, "nexthopip":{} }}},"destinationIP":{}}
        self.topSourceIP=[]
        self.topDestinationIP=[]


    def movetroughthefiles(self,TopSip,TopDip,numberofdips):
        #countx=0
        for x in range(0,len(self.listoffiles)):
            infile_r = silkfile_open(self.listoffiles[x], READ)
            for rec in infile_r:
                #countx+=1
                self.addingToDic("sourceIP",rec.sip,rec.nhip)
                self.addingToDic("destinationIP",rec.dip,rec.nhip)
                self.addingToDic("nexthopip",rec.nhip,None)
            infile_r.close()
        #print(countx)
        if len(self.dictofinfo["sourceIP"].keys())>len(self.dictofinfo["destinationIP"].keys()):
            self.topSourceIP =self.findTopIps("sourceIP",TopSip)
            self.topDestinationIP =self.findTopIps("destinationIP",TopDip)
            #self.topNexthopip =self.findTopIps("nexthopip",2)
            choseDip=self.getUniqueIp(numberofdips,self.topDestinationIP)
            choseSip=self.selectSip(self.topSourceIP)
            #nexthopips= self.getnexthopip("sourceIP",choseDip)
            #nexthopips= self.getnexthopip("sourceIP",choseSip)
        else:
            self.topSourceIP =self.findTopIps("sourceIP",TopDip)
            self.topDestinationIP =self.findTopIps("destinationIP",TopSip)
            #self.topNexthopip =self.findTopIps("nexthopip",2)
            choseDip=self.getUniqueIp(numberofdips,self.topSourceIP)
            choseSip=self.selectSip(self.topDestinationIP)
            #nexthopips= self.getnexthopip("sourceIP",choseDip)
            #nexthopips= self.getnexthopip("destinationIP",choseSip)

        #print(choseSip)
        #print(choseDip)
        #print(nexthopips)
        return choseDip, choseSip

        #print(self.getnexthopip("sourceIP",topSourceIP[0][1]))
        #print(self.getnexthopip("destinationIP",topDestinationIP[0][1]))

    def getnexthopip(self,sipOrDip,ip):
        if len(self.dictofinfo["sourceIP"].keys())<len(self.dictofinfo["destinationIP"].keys()):
            if sipOrDip=="sourceIP":
                sipOrDip="destinationIP"
            else:
                sipOrDip="sourceIP"
        if len(self.dictofinfo["nexthopip"].keys()) >1:
            nexthopips=[0,0]
            if len(self.dictofinfo[sipOrDip][ip]["nexthopip"].keys())==1:
                for nextip in self.dictofinfo[sipOrDip][ip]["nexthopip"].keys():
                    nexthopips[0] =nextip
            else:
                mostip=0
                for keysip,valuesnexhop in self.dictofinfo[sipOrDip][ip]["nexthopip"].items():
                    if valuesnexhop>mostip:
                        nexthopips[0] =keysip
                        mostip=valuesnexhop
            reversedip=""
            if sipOrDip=="sourceIP":
                reversedip="destinationIP"
            else:
                reversedip="sourceIP"
            try:
                if len(self.dictofinfo[reversedip][ip]["nexthopip"].keys())==1:
                    for nextip in self.dictofinfo[reversedip][ip]["nexthopip"].keys():
                        nexthopips[1] =nextip
                else:
                    mostip=0
                    for keysip,valuesnexhop in self.dictofinfo[reversedip][ip]["nexthopip"].items():
                        if valuesnexhop>mostip:
                            nexthopips[1] =keysip
                            mostip=valuesnexhop
            except:
                nexthopips[1]=nexthopips[0]
        else:
            for key in self.dictofinfo["nexthopip"].keys():
                nexthopips=[key,key]
        return nexthopips

    def selectSip(self,listofip):
        templist=[]
        for temp in listofip:
            templist.append(temp[1])
        return templist
    
    def getUniqueIp(self,numberOfSetsSips,listIPS):
        choseIps=[]
        tempIp=0
        if numberOfSetsSips>=len(listIPS):
            choseIps=listIPS
        else:
            while len(choseIps) <numberOfSetsSips:
                tempIp=self.selectDip(listIPS)
                if tempIp not in choseIps:
                    choseIps.append(tempIp)
                    for ips in listIPS:
                        if tempIp == ips[1]:
                            listIPS.remove(ips)
        return choseIps 

    def selectDip(self,listofip):
        count=0
        recordsToUse=[]
        theWeights=[]
        for x in range (0,len(listofip)):
            count+=listofip[x][0]
            recordsToUse.append(listofip[x][1])
            theWeights.append(listofip[x][0])
        for x in range (0,len(theWeights)):
            theWeights[x]=theWeights[x]/count
        return random.choices(recordsToUse, weights=theWeights, k=1)[0]
        

    def findTopIps(self,sipOrDip,size):
        listoftop=[]
        if size > len(self.dictofinfo[sipOrDip]):
            size=len(self.dictofinfo[sipOrDip])
        for x in range(0,size):
            listoftop.append([0,None])
        for key,ipset in self.dictofinfo[sipOrDip].items():
            #countx+=1
            if ipset["count"]>listoftop[size-1][0]:
                tempnumber=size-1
                for x in range(1,size+1):
                    if ipset["count"]>listoftop[-x][0]: 
                        tempnumber=x
                listoftop.insert(-tempnumber,[ipset["count"],key])
                listoftop.pop()
        return  listoftop

    def addingToDic(self,sipOrDip,ip,nhip):        
        try:
            self.dictofinfo[sipOrDip][ip]["count"]+=1
        except:
            self.dictofinfo[sipOrDip][ip]={"count":1,"nexthopip":{}}
        if str(nhip)!=None:
            try:
                self.dictofinfo[sipOrDip][ip]["nexthopip"][nhip]+=1
            except:
                self.dictofinfo[sipOrDip][ip]["nexthopip"][nhip]=1



#start=Folderpathstructure("out","oslo",2011,1,25,"/media/sf_share/")
#end=Folderpathstructure("out","oslo",2011,1,26,"/media/sf_share/")

#ff=FindFiles(start,end)
#GT=GetTrafficPattern(ff.findallfiles())
#GT=GetTrafficPattern(["data/DiffrentSamplingRates/train/train1000"])
#choseDip, choseSip=GT.movetroughthefiles(100,20,3)
#print(GT.getnexthopip("destinationIP",choseDip[0]))#IPv4Addr("192.168.56.11")choseDip[0]
#print(GT.getnexthopip("destinationIP",IPv4Addr("116.126.2.5")))#IPv4Addr("192.168.56.11")choseDip[0]
#print(choseSip)
#print(choseDip)

