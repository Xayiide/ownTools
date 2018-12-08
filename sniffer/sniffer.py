#!/usr/bin/env pyton

import socket
import os
import struct
import binascii

def analyze_ip_header(data):
    ip_hdr = struct.unpack("!4H4s4s", data[:20])
    ver = ip_hdr[0] >> 12 # Shift 12 bits to the right
    ihl = (ip_hdr[0] >> 8) & 0x0F # 00001111
    tos = ip_hdr[0] & 0x00ff # 0000000011111111
    tot_length = ip_hdr[1]
    ip_id = ip_hdr[2]
    flags = ip_hdr[3] >> 13 # Only going to get the first 3 bits
    frag_offset = ip_hdr[3] & 0x1FFFF
    src_addr = socket.ntoa(ip_hdr[4])
    dst_addr = socket.ntoa(ip_hdr[5])
    
    return

def analyze_ether_header(data):
    ip_bool = False

    eth_hdr  = struct.unpack("!6s6sH", data[:14]) # "!6s" -> Big-endian, 6 bytes. # IPv4 = 0800
    dest_mac = binascii.hexlify(eth_hdr[0])
    src_mac  = binascii.hexlify(eth_hdr[1])
    prot     = eth_hdr[2] # Next protocol

    print dest_mac
    print src_mac
    print hex(prot)
    if hex(proto) == 0x0800: #ipv4
        ip_bool = True

    data = data[14:]
    return data, ip_bool

def main():
    sniffer_socket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    recv_data = sniffer_socket.recv(2048)

    data, ip_bool = analyze_ether_header(recv_data)
    if ip_bool:
        data = analyze_ip_header(data)

main()





"""
htons(0x0003): https://www.mutekh.org/doc/netinet_ether_h_header_reference.html
 -> Any IP packet


https://en.wikipedia.org/wiki/Ethernet_frame
https://en.wikipedia.org/wiki/EtherType




"""
