This is a mac changer script.
USAGE: python3 mac_changer -i network_interface(e.x wlan0) -m new mac address
We use the subproccess module to change the mac address, we get the users input with optparse module and check
if the mac adress has changes with a reqular expression using the re python module.

