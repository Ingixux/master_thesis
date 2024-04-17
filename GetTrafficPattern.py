from silk import *

class GetTrafficPattern:
    def __init__(self,listoffiles):
        self.listoffiles=listoffiles


    def movetroughthefiles(self):
        for x in range(0,len(self.listoffiles)):
            infile_r = silkfile_open(self.listoffiles[x], READ)
            for rec in infile_r:
                pass
            