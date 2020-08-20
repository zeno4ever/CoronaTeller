#!/usr/bin/env python3
import pygame
import random
import time
import importlib
import os
import sys
import serial
import json
import argparse
from hashlib import md5
from datetime import datetime
from importlib import util

parser = argparse.ArgumentParser(
    description='Show number of Covid Exposure Notification beacons')
parser.add_argument('--cli', action="store_true",
                    help='use external ESP32 as sensor.')
parser.add_argument('--esp32', nargs='?',
                    help='use external ESP32 as sensor.')
args = parser.parse_args()

if args.cli:
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    headless = True
else:
    headless = False

if args.esp32 is not None:
    try:
        ser = serial.Serial(args.esp32, 115200, timeout=0)
    except (OSError, serial.SerialException):
        print('Serial port not found!')
        quit()
    esp32 = True
else:
    esp32 = False

beacontoolsModule = util.find_spec("beacontools") and False

if beacontoolsModule:
    from beacontools import BeaconScanner, ExposureNotificationFrame
else:
    print('Beacontools not found!!')
    if not esp32:
        print('CoronaTeller will not scan any beacons. Continue in demo mode')

# maxium beacons that fits onscreen
maxscreenBeacons = 18*2  # 18 lines 2 coloms
# time in secs when beacon is no longer valid. Should be 25min for Covid EN BLE
maxtimeBeacons = 10#25*60 

# scan functions
def callback(bt_addr, rssi, packet, additional_info):
    identifier = str(additional_info)[16:48]
    tempbeacon = findDuplicateBeacon(identifier)
    if tempbeacon is None:
        addbeacon(Beacon(identifier,rssi))
    else:
        tempbeacon.lastseen = time.time()
        tempbeacon.rssi = rssi
    
# scan for all COVID-19 exposure notifications
if beacontoolsModule:
    scanner = BeaconScanner(callback,
                            packet_filter=[ExposureNotificationFrame]
    )
    scanner.start()


def parseESP32():
    global ser
    #{"mac":"68:cd:30:be:74:40", "rssi":-65, "rpi":"a4deabca1f93b9a244bb9c87360377f5", "aem":"eca7f4be"}
    if ser.is_open:
        serialData = ser.readlines()
        # print(len(serialData))
        for line in serialData: #only proces first 4
            try:
                data = json.loads(line)
            except ValueError:
                print("JSON Error on line : %s", data)
            else:    
                tempbeacon = findDuplicateBeacon(data['rpi'])
                if tempbeacon is None:
                    addbeacon(Beacon(data['rpi'], data['rssi']))
                else:
                    tempbeacon.lastseen = time.time()
                    tempbeacon.rssi = data['rssi']
    #ser.flush

#Classes and other objects
class Beacon:
    """ found beacons  """

    def __init__(self, identifier, rssi=100):
        #self._registry.append(self)
        self.identifier = identifier
        self.pos = 999
        self.rssi = rssi
        self.firstseen = time.time()
        self.lastseen = self.firstseen
        
    def __str__(self):
        return "({0})".format(self.identifier)

def fillfakebeacon(nubmerofbeacons):
    for i in range(0,nubmerofbeacons):
        addbeacon(Beacon(md5((str(random.randint(0, 2048))).encode('utf-8')).hexdigest()[:32],random.randint(0,100)))

def getAvailablePos():
    global beaconlist
    curpos=[]
    for beacon in beaconlist:
        curpos.append(beacon.pos)
    return list(set(range(maxscreenBeacons))-set(sorted(curpos)))

def findDuplicateBeacon(newidentifier):
    global beaconlist
    for beacon in beaconlist:
        if newidentifier == beacon.identifier:
            return beacon
    return None

def addbeacon(newBeacon):
    global beaconlist,lastbeacon    
    available = getAvailablePos()
    if len(available)>0:
        newBeacon.pos = random.choice(available)
    beaconlist.append(newBeacon)
    lastbeacon = newBeacon
    if headless:
        print("counted : "+str(len(beaconlist))+" Addded beacon : "+newBeacon.identifier)

def cleanupbeaconlist():
    global beaconlist
    now = time.time()
    for beacon in reversed(beaconlist):
        if now-beacon.lastseen > maxtimeBeacons:
            beaconlist.remove(beacon)
            if headless:
                print("counted : "+str(len(beaconlist))+" Removed beacon : "+beacon.identifier)
        elif(beacon.pos == 999):
            available = getAvailablePos()
            if len(available)>0:
                beacon.pos = random.choice(available)

def stopTeller():
    global ser
    if beacontoolsModule:
        scanner.stop()
    if ser.is_open:
        ser.close()
    done = True
    quit()

# define the RGB value for white,
#  green, blue colour .
green = (0, 255, 0)
blue = (50, 50, 128)
black = (0, 0, 0)
beaconlist = []

progresbar = 0
lastbeacon = Beacon('No Corona Exposure Notification beacon seen yet!!',0)
lastcleanup = time.time()

pygame.init()
if os.environ.get('SDL_VIDEODRIVER') == 'dummy':
    screen = pygame.display.set_mode((1, 1))
else:    
    #screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((1920, 1080))

screenX, screenY = pygame.display.get_surface().get_size()

pygame.display.set_caption('CoronaTeller')
pygame.mouse.set_visible(False)

font = pygame.font.Font('./fonts/Orbitron-VariableFont_wght.ttf', 340)
scanfont = pygame.font.Font('./fonts/Orbitron-Bold.ttf', 70)
shafont = pygame.font.Font("./fonts/VT323-Regular.ttf", 70)
footerfont = pygame.font.Font('./fonts/Orbitron-Regular.ttf', 40)
footerfontsmall = pygame.font.Font('./fonts/Orbitron-Regular.ttf', 20)

done = False
while not done:
    now = time.time()

    if esp32:
        parseESP32()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopTeller()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            stopTeller()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            fillfakebeacon(7)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            cleanupbeaconlist()

    screen.fill((black))
    
    pygame.draw.line(screen, blue, (0,100), (screenX,100), 6)

    #text coronateller
    scan_text = scanfont.render('CoronaTeller', True, green)
    textRect = scan_text.get_rect()
    textRect.topleft = (50, 1)
    screen.blit(scan_text, textRect)

    # fake scan bar
    scan_text = scanfont.render('Scanning [                ]', True, green)
    textRect = scan_text.get_rect()
    textRect.topleft = (screenX-800, 1)
    screen.blit(scan_text, textRect)
    
    if (progresbar>330):
        progresbar = 0 
    pygame.draw.rect(screen, (255,128,0), pygame.Rect(screenX-390, 20, progresbar, 52))
    progresbar += 10

    #cyber garbage
    cybergarbage = md5((str(now)).encode('utf-8')).hexdigest()[:6]
    scan_text = scanfont.render(cybergarbage, True, green)
    textRect = scan_text.get_rect()
    textRect.topleft = (screenX-390, 1)
    screen.blit(scan_text, textRect)    
    
    # background of identifieres
    for beaconobject in beaconlist:
        if (beaconobject.pos!=999):               
            #beaconcolor = int((maxtimeBeacons-beacontime)/maxtimeBeacons*255)
            #rssi < 30 = near / >70 is 
            beaconcolor = min(abs(int(255+(2.5*beaconobject.rssi))), 255)
            if beaconobject.pos<maxscreenBeacons//2:
                x=25
                y=beaconobject.pos*45+110
            else: 
                x=screenX//2
                y=(beaconobject.pos-maxscreenBeacons//2)*45+110
            shatext = shafont.render(beaconobject.identifier, False, (0, 0, beaconcolor))
            shatextRect = shatext.get_rect()
            shatextRect.topleft = (x, y )
            screen.blit(shatext, shatextRect)

    #number of found beacons
    text = font.render(str(len(beaconlist)), True, green)
    textRect = text.get_rect()
    textRect.center = (screenX // 2, screenY // 2)
    screen.blit(text, textRect)

    #lastbeacon
    pygame.draw.line(screen, blue, (0,screenY-100), (screenX,screenY-100), 6)
    scan_text = footerfont.render(
        'Last beacon : '+lastbeacon.identifier+' Power : '+str(lastbeacon.rssi), True, green)
    textRect = scan_text.get_rect()
    textRect.center = (screenX//2, screenY-60)
    screen.blit(scan_text, textRect)
    
    # Created by
    scan_text = footerfontsmall.render('Created by Dave Borghuis & hackerspace TkkrLab Enschede', True, (200,100,0))
    textRect = scan_text.get_rect()
    textRect.bottomright = (screenX-10, screenY-10)
    screen.blit(scan_text, textRect)

    #demo mode
    if not beacontoolsModule and not esp32:
        text = footerfontsmall.render('DEMO MODE', True, green)
        textRect = text.get_rect()
        textRect.bottomleft = (10, screenY-10)
        screen.blit(text, textRect)

    pygame.display.flip()

    #do every xx min.
    #if now-lastcleanup > 10: #run cleanup every n sec 
    print("Start cleaning.")
    cleanupbeaconlist()
    #    lastcleanup=now
    print("Done cleaning")

    pygame.time.delay(10) #wait in mili secs
