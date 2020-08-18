import time
import json
from datetime import datetime
from beacontools import BeaconScanner, ExposureNotificationFrame

beacon = ''

def callback(bt_addr, rssi, packet, additional_info):
    print(str(bt_addr)+str(time.time()) +" beacon: " +str(additional_info)[16:48]+' rsst:'+str(rssi))
    #print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))

# scan for all COVID-19 exposure notifications
scanner = BeaconScanner(callback, 
    #comment next line if you want to see ALL beacons
    #packet_filter=[ExposureNotificationFrame]
)
scanner.start()
time.sleep(10*60) #scan for 10 mins
scanner.stop()
