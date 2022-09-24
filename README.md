# ARP Spoofer

This tool is designed to work in step 3 of the [Kill Chain](https://www.varonis.com/blog/cyber-kill-chain). Once access to an internal network is established, the ARP spoofer will perform a man-in-the-middle attack by altering the flow of packets to/from the default gatway device/target machine.

This works by sending an unsolicited response ARP packet to both the default gateway machine and the target machine. This forces both of their tables to update with the attacker's information swapped for both machines.

Example of attack:

![arp_spoof_diagram](https://user-images.githubusercontent.com/80045938/149645936-6c00817b-7802-4b24-806d-cc53ef8ab589.jpg)

## Disclaimer:

❗ **I DO NOT AUTHORIZE THE USE OF THESE FILES TO PERFORM ILLEGAL OR UNAUTHORIZED ACTIVITIES. ALL TESTS MUST BE PERFORMED ON DEVICES THAT ARE OWNED BY THE TESTER OR WITH THE EXPRESS WRITTEN CONSENT OF THE SYSTEM OWNER(S).**

## Tool Functionality:

- Will allow an attacker to become a MITM and from there multiple attacks can occur
- Will restore the default settings on the target after stopping the spoof

## Tool Requirements:

- To use the default functionality of this tool, an additional module will be required:
  - [scapy](https://scapy.readthedocs.io/en/latest/installation.html)
- This tool needs a ![small](https://user-images.githubusercontent.com/80045938/148561762-9590c4a1-a424-4c7b-a0fb-68190fb7a31c.png) [Python](https://www.python.org/downloads/) interpreter, v3.6 or higher due to string interpolation

## Quick Notes:

- The attacker machine can be a Windows, OSX, or Linux OS
- The target machine is designed to be a Windows machine, however this can be altered if needed
- CTRL + C is recognized by this tool as an 'exit' request and will stop the spoof/reset the target(s)
- I wrote this with Python 2.7 capabilities as well, I commented out that code to avoid errors running in Python3

## Using the Tool:

#### Start the ARP Spoofer:

Run the binary from the attacking machine to spoof both targets.
![start_arp](https://user-images.githubusercontent.com/80045938/149646097-cac11472-2015-49c8-9dbf-fa7d75ba891f.gif)

#### Stop the ARP Spoofer:

CTRL+C will stop the spoofing and reset the gateway/target ARP tables.
![reset_target_settings](https://user-images.githubusercontent.com/80045938/149646128-84f564dc-8bff-4f6b-9889-aab7811f30d3.gif)

## Demonstration of ARP Table Changes:

#### Target Machine Network Settings (before attack):

![arp_target_settings](https://user-images.githubusercontent.com/80045938/149646160-7811f9c5-8aa1-4e1c-a337-394de005f5e7.jpg)

#### Attacker Machine Network Settings (before/during attack):

![arp_attacker_settings](https://user-images.githubusercontent.com/80045938/149646171-5492ca02-0925-4249-bf34-ae5ad5da7307.jpg)

#### Target Machine Network Settings (after attack):

![spoofed_target_settings](https://user-images.githubusercontent.com/80045938/149646179-f2242d83-daa6-4d6a-8d8c-ba89696c4526.jpg)

#### Target Machine Network Settings (after reset sent from attacker):

![target_reset_settings](https://user-images.githubusercontent.com/80045938/149646190-5c757821-553c-4fe3-9c06-199b1eeafe55.jpg)
