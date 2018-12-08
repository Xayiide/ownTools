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
        Who-has dstIP? """
    print("[+] Sending ARP request to: " + dstIP)
    a = ARP() # Create an ARP Message
    a.hwtype = 1 # Ethernet
    a.ptype  = 2048 # 0x0800 = IP
    a.hwlen  = 6 # Ethernet addresses (MACs) have 6 octets
    a.plen   = 4 # IP addresses have 6 octets
    a.op     = 1 # ARP request (who-has?)
    # a.hwsrc = .... # Change this if you are using a bogus MAC. Otherwise, defaults to your MAC
    a.hwdst  = "ff:ff:ff:ff:ff:ff" # Broadcast
    # a.psrc   =  .... # Chanfe this if you are using a bogus IP (?). Defaults to your IP
    a.pdst = dstIP # The IP whose MAC you're asking for
    send(a)

def ARP_request():
    dstIP = input("[+] IP you want to send the request to: ")
    send_ARP_request(dstIP)

def menu():
    opt = -1
    while (opt != 0):
        print("""
             / ___|| | ____ _ _ __
             \___ \| |/ / _` | '_  \\
              ___) |   < (_| | | | |
             |____/|_|\_\__,_|_| |_| v1.0
             """)
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
                print("Not implemented yet")
            elif opt == 3:
                print("Not implemented yet")
            elif opt == 4:
                print("Not implemented yet")
            else:
                print("Not an option.")
        except ValueError:
            print("Only numbers accepted")
            exit(1)





def main():
    menu()


if __name__ == '__main__':
    main()
