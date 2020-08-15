import time
import json
from datetime import datetime
from beacontools import BeaconScanner, ExposureNotificationFrame

beacon = ''

def callback(bt_addr, rssi, packet, additional_info):
    global beacon
    tempbeacon = str(additional_info)[16:48]
    #print("Temp %s",tempbeacon)
    #print(str(additional_info)[16:48])
    if beacon != tempbeacon:
        now = str(datetime.now())
        beacon = str(additional_info)[16:48]
        print(now +" beacon: " +beacon)
    #print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))

# scan for all COVID-19 exposure notifications
scanner = BeaconScanner(callback, 
    packet_filter=[ExposureNotificationFrame]
)
scanner.start()
time.sleep(12*60*60)
scanner.stop()
