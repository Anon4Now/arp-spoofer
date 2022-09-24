#!/usr/bin/env python
from scapy.layers.l2 import *


def arpScan(ips):
    arp_request = ARP(pdst=ips)  # where should the request go/what ip - /24 subnet
    # arp_request.show() #show content
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")  # send the packet to the broadcast MAC address
    arpRequestBroadcast = broadcast / arp_request  # combine the ip and MAC address to create an ARP request for any IP in the subnet
    answeredRequestsList = srp(arpRequestBroadcast, timeout=1, verbose=False)[
        0]  # srp allows for packets with custom Ether to be sent & wait 1 sec for response and move on/ returns 2 vals
    return answeredRequestsList[0][1]
