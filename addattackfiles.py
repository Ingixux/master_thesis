from silk import *


def getDataNetFlow():
    #infiles =[silkfile_open("sortedsloweri15min456part1.rw", READ),silkfile_open("sortedsloweri15min456part2.rw", READ),silkfile_open("sortedsloweri15min456part3.rw", READ)]
    infiles =[silkfile_open("sortedruby301part1.rw", READ),silkfile_open("sortedruby301part2.rw", READ)]
    outfile = silkfile_open("data/GenratedAttacks/ruby301", WRITE)
    for x in range(0,len(infiles)):
        for rec in infiles[x]:
            outfile.write(rec)

getDataNetFlow()