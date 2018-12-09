"""
https://nmap.org/book/man-port-scanning-techniques.html
https://scapy.readthedocs.io/en/latest/usage.html
https://en.wikipedia.org/wiki/Ethernet_frame
https://en.wikipedia.org/wiki/Address_Resolution_Protocol
https://en.wikipedia.org/wiki/Transmission_Control_Protocol
https://en.wikipedia.org/wiki/IPv4
"""

from scapy.all import *
import os

# ARP requests
def send_ARP_request(dstIP):
    """ https://www.iana.org/assignments/arp-parameters/arp-parameters.xhtml
        Who-has dstIP?
        It's the Ethernet frame Header whose destination is ff:ff:ff:ff:ff:ff
    """
    print("[!!] Sending ARP request to: " + dstIP)
    a = ARP() # Create an ARP Message
    a.hwtype = 1 # Ethernet
    a.ptype  = 2048 # 0x0800 = IP
    a.hwlen  = 6 # Ethernet addresses (MACs) have 6 octets
    a.plen   = 4 # IP addresses have 6 octets
    a.op     = 1 # ARP request (who-has?)
    # a.hwsrc = .... # Change this if you are using a bogus MAC. Otherwise, defaults to your MAC
    a.hwdst  = "00:00:00:00:00:00" # No-one
    # a.psrc   =  .... # Change this if you are using a bogus IP (?). Defaults to your IP
    a.pdst = dstIP # The IP whose MAC you're asking for
    send(a)

def ARP_request():
    dstIP = input("[+] IP you want to send the request to: ")
    send_ARP_request(dstIP)


def send_ARP_reply(dstIP, dstMAC):
    """
        I have this IP
    """
    print("[!!] Sending ARP request to: " + dstIP + "-" + dstMAC)
    a = ARP()
    a.hwtype = 1
    a.ptype  = 2048
    a.hwlen  = 6
    a.plen   = 4
    a.op     = 2 # Reply
    # a.hwsrc  = .... # Change this if you are using a bogus IP
    a.hwdst  = dstMAC
    # a.psrc  = .... # Change this if you are using a bogus IP (?)
    a.psdt = dstIP
    send(a)

def ARP_reply():
    dstIP  = input("[+] IP you want to send the reply to: ")
    dstMAC = input("[+] MAC you want to send the reply to: ")
    send_ARP_reply(dstIP)


def send_SYN(dstIP, dstPort):
    """
        Sends a SYN to the IP and Port specified
    """
    print("[!!] Sending SYN to: " + dstIP + ":" + dstPort)
    ip = IP()
    ip.dst = dstIP
    ip.src = "192.168.21.104" # Your IP here
    tcp = TCP()
    tcp.sport = 4000 # Random
    tcp.dport = dstPort
    tcp.flags = "S" # SYN flag on
    packet = ip/tcp
    send(packet)

def SYN():
    dstIP   = input("[+] IP you want to send the SYN to: ")
    dstPort = input("[+] Port you want to send the SYN to: ")
    send_SYN(dstIP, dstPort)


def send_XMAS(dstIP, dstPort):
    """
        Sends a XMAS packet to destIP:dstPort
        XMAS packet: FIN, Urgent and Push flags enabled
    """
    print("[!!] Sending XMAS to: " + dstIP + ":" + dstPort)
    ip = IP()
    ip.dst = dstIP
    ip.src = "192.168.21.104"
    tcp = TCP()
    tcp.sport = 4000 # Random
    tcp.dport = dstPort
    tcp.flags = "FUP"
    packet = ip/tcp
    send(packet)

def XMAS():
    dstIP   = input("[+] IP you want to send the XMAS to: ")
    dstPort = input("[+] Port you want to send the XMAS to: ")
    send_XMAS(dstIP, dstPort)


def main():
    opt = -1
    while (opt != 0):
        print("Scanner: ")
        print("[1] ARP request")
        print("[2] ARP reply")
        print("[3] SYN")
        print("[4] XMAS")
        print("[0] Exit")
        opt = input("> Your choice: ")
        try:
            os.system("clear")
            opt = int(opt)
            if opt == 0:
                print("[!] Exiting")
                exit(0)
            elif opt == 1:
                ARP_request()
            elif opt == 2:
                ARP_reply()
            elif opt == 3:
                SYN()
            elif opt == 4:
                print("Not implemented yet")
            else:
                print("Not an option.")
        except ValueError:
            print("Only numbers accepted")
            exit(1)



if __name__ == '__main__':
    main()
