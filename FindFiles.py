import subprocess
import os

#rwsort --fields=stime --output-path=outfile.rw /media/sf_share/out-S1_20110125.12
#TODO need to sort files
#rwsort --fields=stime --output-path=outfileattack.rw data/GenratedAttacks/ext2ext-S0_20240125.12



class Folderpathstructure:
    def __init__(self,inout,router,Year,month,day,startofpath=""):
        self.inout=inout
        self.Year=Year
        self.month=month
        self.day=day
        self.router=router
        self.pathname=self.makepathname()
        self.startofpath=startofpath

    def checkinput(self,inout,Year,month,day):
        if type(Year)!=int or type(month)!=int or  type(day)!=int:
            raise ValueError("year, month and day is not int")
        if inout not in ["out","in"]:
            raise ValueError("inout has to be in and out")
        
    def dirnumber(self, input):
        if input in range(1,10):
            return "0"+str(input)
        else:
            return str(input)
            
    
    def makepathname(self):
        return self.router+"/"+self.inout +"/"+str(self.Year) +"/"+self.dirnumber(self.month) +"/"+self.dirnumber(self.day)
    
    def moveToNextmonth(self):
        self.month+=1
        if self.month==13:
            self.month=1
            self.Year+=1

    def moveToNextDay(self):
        #TODO handle moth day year swicth
        self.day+=1
        if self.month ==2:
            if self.Year%4==0:
                if self.day==30:
                    self.day=1
                    self.moveToNextmonth()
            else:
                if self.day==29:
                    self.day=1
                    self.moveToNextmonth()
        elif self.month in [1,3,5,7,8,10,12]:
            if self.day==32:
                self.day=1
                self.moveToNextmonth()
        else:
            if self.day==31:
                self.day=1
                self.moveToNextmonth()
        self.pathname=self.makepathname()

    def checksame(self,otherFolderpathstructure):
        if type(otherFolderpathstructure) != Folderpathstructure:
            return False
        elif (self.inout != otherFolderpathstructure.inout or self.Year != otherFolderpathstructure.Year 
        or self.month != otherFolderpathstructure.month or self.day != otherFolderpathstructure.day or self.router != otherFolderpathstructure.router):
            return False
        else:
            return True
        
    def getThefiles(self):
        files = os.listdir(self.pathname)
        files=self.sortfiles(files)
        return files

    def sortfiles(self,files):
        templist=[]
        templistnumber=[]
        for tempfile in files:
            temp= tempfile.split(".")[-1]
            if len(templistnumber)==0:
                templistnumber.append(int(temp))
                templist.append(self.pathname+"/"+tempfile)
            else:
                insertat=0
                for x in range(0,len(templistnumber)):
                    if insertat==0 and templistnumber[x]>int(temp):
                        insertat=x
                    elif x==len(templistnumber)-1:
                        insertat=x+1
                if insertat ==len(templistnumber):
                    templistnumber.append(int(temp))
                    templist.append(self.pathname+"/"+tempfile)
                else:
                    templistnumber.insert(insertat,int(temp))
                    templist.insert(insertat, self.pathname+"/"+tempfile)
        return templist

class FindFiles:
    def __init__(self,start,end):
        self.checkinput(start,end)
        self.current=start
        self.end=end
        self.listfiles=[]

    def checkinput(self,start,end):
        if type(start) !=Folderpathstructure or type(end) !=Folderpathstructure:
            raise ValueError("start or end is not Folderpathstructure")
        
#    def sortFile(self,file):
#        x=subprocess.call("rm temp.rw", shell=True)
#        x=subprocess.call("rwsort --fields=stime --output-path=temp.rw "+file+"", shell=True)

    def findallfiles(self):
        templist=[]
        while not self.end.checksame(self.current):
            resault=self.current.getThefiles()
            self.current.moveToNextDay()
            for x in range(0,len(resault)):
                templist.append(resault[x])
        return templist

            


start=Folderpathstructure("in","oslo",2011,2,28)
end=Folderpathstructure("in","oslo",2011,3,2)

ff=FindFiles(start,end)
print(ff.findallfiles())


#print("hei")
#x=subprocess.call("echo Hello World", shell=True)
#x=subprocess.call("rwsort --fields=stime --output-path=outfileattack.rw data/GenratedAttacks/ext2ext-S0_20240125.12", shell=True)
#print("hei")