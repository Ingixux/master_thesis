from silk import *

def getDataNetFlow(silkFile):
    infile = silkfile_open(silkFile, READ)
    i =0
    for rec in infile:
        print (rec)
        i+=1
        if i==50:
            break

getDataNetFlow("/var/silk/data/ext2ext/2024/01/25/ext2ext-S0_20240125.12")

#getDataNetFlow("/var/silk/data/ext2ext/2024/01/24/ext2ext-S0_20240124.10")
