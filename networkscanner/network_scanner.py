import scapy.all as scapy
import optparse


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)

    # print(arp_request.summary()) prints the request we have created
    # scapy.ls(scapy.ARP()) show us the available options and the default vaules for them

    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # scapy.ls(scapy.Ether())
    # print(broadcast.summary())
    arp_request_broadcast = broadcast/arp_request
    # print(arp_request_broadcast.summary())
    # arp_request_broadcast.show() show will show us more details about our packet than summary

    answered_list, unaswered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)

    # print(answered_list.summary())
    # print(unaswered_list.summary())
    client_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        # 0 element is the packet send 1 element is the answer
        client_list.append(client_dict)
    return client_list


def print_results(results_list):
    print("IP\t\t\tMAC Address\n--------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP / IP range.")
    options, arguments = parser.parse_args()
    print("These are the options: " + str(options))
    return options.target


# Get the command line option using get_arguments() pass it to scan()
# Finally parse the result and print it with print_results()
print_results(scan(get_arguments()))

