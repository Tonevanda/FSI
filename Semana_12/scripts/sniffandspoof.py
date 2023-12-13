from scapy.all import *

def spoof_icmp_reply(packet):
    if packet.haslayer(ICMP) and packet[ICMP].type == 8:
        print(f"Received ICMP Echo Request from {packet[IP].src}")
        a = IP()
        a.dst='8.8.8.8'
        b=ICMP()
        p=a/b
        send(p)
        print(f"Sent ICMP Echo Reply to {p.dst}")

sniff(iface='br-35f18959ffa2', filter='icmp', prn=spoof_icmp_reply)
