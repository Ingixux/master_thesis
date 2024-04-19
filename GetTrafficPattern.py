from silk import *
from FindFiles import FindFiles,Folderpathstructure
import random 

class GetTrafficPattern:
    def __init__(self,listoffiles):
        self.listoffiles=listoffiles
        self.dictofinfo={"sourceIP":{},"destinationIP":{},"nexthopip":{}}#{"sourceIP":{{192.168.57.11 : {"count" : 1, "nexthopip":{} }}},"destinationIP":{}}


    def movetroughthefiles(self):
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
            topSourceIP =self.findTopIps("sourceIP",50)
            topDestinationIP =self.findTopIps("destinationIP",20)
            topNexthopip =self.findTopIps("nexthopip",2)
            choseDip=self.selectDip(topDestinationIP)
            choseSip=self.selectSip(topSourceIP)
            #nexthopips= self.getnexthopip("sourceIP",choseDip)
            #nexthopips= self.getnexthopip("sourceIP",choseSip)
        else:
            topSourceIP =self.findTopIps("sourceIP",20)
            topDestinationIP =self.findTopIps("destinationIP",50)
            topNexthopip =self.findTopIps("nexthopip",2)
            choseDip=self.selectDip(topSourceIP)
            choseSip=self.selectSip(topDestinationIP)
            #nexthopips= self.getnexthopip("sourceIP",choseDip)
            #nexthopips= self.getnexthopip("destinationIP",choseSip)

        print(choseSip)
        print(choseDip)
        #print(nexthopips)


        #print(self.getnexthopip("sourceIP",topSourceIP[0][1]))
        #print(self.getnexthopip("destinationIP",topDestinationIP[0][1]))

    def getnexthopip(self,sipOrDip,ip):
        nexthopips=[0,0]
        if len(self.dictofinfo[sipOrDip][ip]["nexthopip"].keys())==1:
            for nextip in self.dictofinfo[sipOrDip][ip]["nexthopip"].keys():
                nexthopips[0] =nextip
        else:
            #TODO This is if there are more than one 
            print("hei")
        reversedip=""
        if sipOrDip=="sourceIP":
            reversedip="destinationIP"
        else:
            reversedip="sourceIP"
        try:
            if len(self.dictofinfo[reversedip][ip]["nexthopip"].keys())==1:
                for nextip in self.dictofinfo[sipOrDip][ip]["nexthopip"].keys():
                    nexthopips[1] =nextip
            else:
                #TODO This is if there are more than one 
                print("hei")
        except:
            #TODO what to add if there is no record in in the reverse direction
            pass
        return nexthopips

    def selectSip(self,listofip):
        templist=[]
        for temp in listofip:
            templist.append(temp[1])
        return templist

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
        #countx=0
        listoftop=[]
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



start=Folderpathstructure("out","oslo",2011,1,25,"/media/sf_share/")
end=Folderpathstructure("out","oslo",2011,1,26,"/media/sf_share/")

ff=FindFiles(start,end)
GT=GetTrafficPattern(ff.findallfiles())
GT.movetroughthefiles()

