from silk import *

def getDataNetFlow(silkFile):
    infile = silkfile_open(silkFile, READ)
    i =0
    for rec in infile:
        print (rec)
        i+=1
        if i==50:
            break

def bothDataNetFlow(silkFile_w,silkFile_r):
    infile_w = silkfile_open(silkFile_w, WRITE)
    infile_r = silkfile_open(silkFile_r, READ)
    for rec in infile_r:   
        infile_w.write(rec)
    infile_w.close()
    infile_r.close()
    infile_r = silkfile_open(silkFile_w, READ)
    for rec in infile_r:   
        print (rec)
    infile_r.close()

def getDataNetFlow(silkFile):
    infile = silkfile_open(silkFile, READ)
    for rec in infile:
        print (rec)


getDataNetFlow("GenratedAttacks/ext2ext-S0_20240125.11")
#getDataNetFlow("/var/silk/data/ext2ext/2024/01/25/ext2ext-S0_20240125.11")

getDataNetFlow("GenratedAttacks/ext2ext-S0_20240125.11")
