# Once started, wait 20 seconds
# then start checking ping to google 8.8.8.8 and 8.8.4.4
# if no response, assume no internet, swap to access point

import time
import subprocess
from server import start_server

def ping(count, target):
    subprocess.call(["ping", "-c", count, "-W", "1", "-q", target])

# swaps from wireless client to access point or vice versa
def swap_connection(swapToAccessPoint):
    if swapToAccessPoint == True:
        subprocess.call(["sudo", "ifdown", "--force", "wlan0"])
        subprocess.call(["sudo", "systemctl", "stop", "wpa_supplicant"])
        # change interface file
        subprocess.call(["sudo", "cp",
                         "/home/pi/Desktop/TripSwitch/network_interfaces/access_point/interfaces",
                         "/etc/network/interfaces"])
        time.sleep(1)
        subprocess.call(["sudo", "ifup", "--force", "wlan0"])
        subprocess.call(["sudo", "systemctl", "start", "hostapd"])
        subprocess.call(["sudo", "systemctl", "start", "isc-dhcp-server"])
    else:
        subprocess.call(["sudo", "ifdown", "--force", "wlan0"])
        subprocess.call(["sudo", "systemctl", "stop", "hostapd"])
        subprocess.call(["sudo", "systemctl", "stop", "isc-dhcp-server"])
        subprocess.call(["sudo", "cp",
                         "/home/pi/Desktop/TripSwitch/network_interfaces/client/interfaces",
                         "/etc/network/interfaces"])
        time.sleep(1)
        subprocess.call(["sudo", "ifup", "--force", "wlan0"])
        time.sleep(1)
        subprocess.call(["sudo", "systemctl", "start", "wpa_supplicant"])
        
#time.sleep(20)

swap_connection(True)

#try:
#    ping("3", "8.8.8.8")
#    start_server()
#except:
#    # failed to ping Google, assume offline
#    # Drop wireless connect
#    swap_connection(True)
