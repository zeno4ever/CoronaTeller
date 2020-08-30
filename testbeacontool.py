import time
from beacontools import BeaconScanner, ExposureNotificationFrame

def callback(bt_addr, rssi, packet, additional_info):
    print(str(time.strftime("%H:%M:%S", time.localtime(time.time())))+" "+str(bt_addr)+" ("+str(rssi)+") " +str(additional_info)[16:48])

# scan for all COVID-19 exposure notifications
scanner = BeaconScanner(callback, 
    packet_filter=[ExposureNotificationFrame]
)


print("Start scanning for 10 secs.")
scanner.start()
time.sleep(10) 
scanner.stop()
print("Scanning stopped.")
