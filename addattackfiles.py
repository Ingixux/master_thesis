from silk import *


def getDataNetFlow():
    #infiles =[silkfile_open("sortedruby555part1.rw", READ),silkfile_open("sortedruby555part2.rw", READ),silkfile_open("sortedruby555part3.rw", READ)]
    infiles =[silkfile_open("pingfloodpart1.rw", READ),silkfile_open("pingfloodpart2.rw", READ)]
    #infiles =[silkfile_open("sortedruby439part1.rw", READ)]
    outfile = silkfile_open("/media/sf_share/data/GenratedAttacks/pingflood302.rw", WRITE)
    for x in range(0,len(infiles)):
        for rec in infiles[x]:
            outfile.write(rec)

getDataNetFlow()