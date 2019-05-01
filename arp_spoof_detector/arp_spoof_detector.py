import scapy.all as scapy

def change_mac(interface, new_mac):
	print("[+] Changing MAC address for " + interface + " to " + new_mac)
	subprocess.call(["ifconfig", interface, "down"])
	subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
	subprocess.call(["ifconfig", interface, "up"])

def sniff(interface):
	scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet):
	if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
            try:
                real_mac = get_mac(packet[scapy.ARP].psrc)
                response_mac = packet[scapy.ARP].hwsrc

                if real_mac != response_mac:
                    print("[+] We are under attack!")
            except:
                pass

sniff("eth0")
