#!/usr/bin/env pyton

import socket
import os
import struct
import binascii

def analyze_ip_header(data):
    return

def analyze_ether_header(data):
    eth_hdr  = struct.unpack("!6s6sH", data[:14]) # "!6s" -> Big-endian, 6 bytes. # IPv4 = 0800
    dest_mac = binascii.hexlify(eth_hdr[0])
    src_mac  = binascii.hexlify(eth_hdr[1])
    prot     = eth_hdr[2] # Next protocol

    print dest_mac
    print src_mac
    print hex(prot)
    if hex(proto) == 0x0800: #ipv4
        return data[14:]

def main():
    sniffer_socket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    recv_data = sniffer_socket.recv(2048)

    data = analyze_ether_header(recv_data)
    data = analyze_ip_header(data)

main()





"""
htons(0x0003): https://www.mutekh.org/doc/netinet_ether_h_header_reference.html
 -> Any IP packet


https://en.wikipedia.org/wiki/Ethernet_frame
https://en.wikipedia.org/wiki/EtherType




"""
