# Python-Network-Security
### This is  a repository for my python network and security projects i am planning for 2019!

* Project 1. MAC address changing script.
* Project 2. Network Scanner
* Project 3. Packet Sniffer
* Project 4. DNS Spoofer
* Project 5. HTTP File Interceptor
* Project 6. Code Injector
* Project 7. ARP Spoofer

If you want to test them with HTTPS sites you will need to run ssl scrip.
1. Run sslstrip with the command:
* sslstrip
2. Redirect any packet that goes to port 80 to port 10000 with the command:
* echo 1 > /proc/sys/net/ipv4/ip_forward
* iptables -t nat -A PREROYTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000
