import pygame, random, time
from hashlib import md5
from datetime import datetime
from beacontools import BeaconScanner, ExposureNotificationFrame

# scan functions
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
#scanner.start()
#time.sleep(30*60)
#scanner.stop()



#Classes and other objects
class Beacon:
    """ found beacons  """

    def __init__(self, txthash, pos=999):
        #self._registry.append(self)
        self.txthash = txthash
        self.color = 255
        self.pos = pos
        self.firstseen = time.time()
        
    def __str__(self):
        return "({0})".format(self.txthash)


def fillfakebeacon(nubmerofbeacons):
    for i in range(0,nubmerofbeacons):
        addbeacon(Beacon(md5((str(random.randint(0, 2048))).encode('utf-8')).hexdigest()[:32],i))
    #for i in range(0,maxscreenBeacons):
        #addbeacon(Beacon(md5((str(random.randint(0, 2048))).encode('utf-8')).hexdigest()[:32],i))

def addbeacon(Beacon):
    global beaconlist,lastbeacon
    
    #check for pos
    curpos=[]
    for beacon in beaconlist:
        curpos.append(beacon.pos)
    available = list(set(range(maxscreenBeacons))-set(sorted(curpos)))
    print(available)
    if available[0]:
        Beacon.pos = available[0]
    print('Beacon Pos = '+str(Beacon.pos))
    beaconlist.append(Beacon)
    #if no pos cleanup/remove
    lastbeacon = Beacon.txthash
 
def cleanupbeaconlist(beaconlist):
    now = time.time()
    for beacon in reversed(beaconlist):
        #print(now-beacon.firstseen)
        if now-beacon.firstseen > 25*60: #if older then 25 min
            beaconlist.remove(beacon)
            print('removed '+str(len(beaconlist)))

# define the RGB value for white,
#  green, blue colour .
white = (255, 255, 255)
green = (0, 255, 0)
blue = (50, 50, 128)
black = (0, 0, 0)
done = False
coronabeacons = 0
progresbar = 0
beacon = ''
lastbeacon = md5((str('Covid')).encode('utf-8')).hexdigest()[:32] #32 pos for empty beacon
beaconlist = []
maxscreenBeacons = 18*2-1

'''
fillfakebeacon()
time.sleep(5)
print('sleep 5 ')
fillfakebeacon()
time.sleep(5)
print('sleep 5 ')
fillfakebeacon()
time.sleep(5)
print('sleep 5,cleanup ')
random.shuffle(beaconlist)
cleanupbeaconlist(beaconlist)

curpos=[]
for beacon in beaconlist:
    print(beacon.txthash+' Pos:'+str(beacon.pos))
    curpos.append(beacon.pos)
    #print(beacon.txthash+' Pos:'+str(beacon.pos))
    available = set(range(maxscreenBeacons))-set(sorted(curpos))
print(available)
quit()
'''

pygame.init()

screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
screenX, screenY = pygame.display.get_surface().get_size()

pygame.display.set_caption('CoronaTeller')

font = pygame.font.Font('./fonts/Orbitron-VariableFont_wght.ttf', 340)
scanfont = pygame.font.Font('./fonts/Orbitron-Bold.ttf', 70)
shafont = pygame.font.Font("./fonts/VT323-Regular.ttf", 70)
footerfont = pygame.font.Font('./fonts/Orbitron-Regular.ttf', 40)
footerfontsmall = pygame.font.Font('./fonts/Orbitron-Regular.ttf', 20)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            fillfakebeacon(maxscreenBeacons)

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        fakecoronabeacons += 1
    if pressed[pygame.K_DOWN]:
        fakecoronabeacons -= 1
    #if pressed[pygame.K_LEFT]:
    #    x -= 1
    #if pressed[pygame.K_RIGHT]: x += 1

    screen.fill((black))
    
    pygame.draw.line(screen, blue, (0,100), (screenX,100), 6)

    #text coronateller
    scan_text = scanfont.render('CoronaTeller', True, green)
    textRect = scan_text.get_rect()
    textRect.topleft = (50, 1)
    screen.blit(scan_text, textRect)
    

    #fake scan bar
    scan_text = scanfont.render('Scanning [                ]', True, green)
    textRect = scan_text.get_rect()
    textRect.topleft = (screenX-800, 1)
    screen.blit(scan_text, textRect)

    if (progresbar>330):
        progresbar = 0 
    pygame.draw.rect(screen, (255,128,0), pygame.Rect(screenX-390, 20, progresbar, 52))
    progresbar += 15

    #qr code
    #screen.blit(pygame.transform.scale(pygame.image.load('./images/qr_coronateller.png'), (300, 300)), (screenX//2, 0))    
    
    coronabeacons = len(beaconlist)    
    for beaconobject in reversed(beaconlist):
        # text surface object
        shatext = shafont.render(
            beaconobject.txthash, False, (0, 0, beaconobject.color))
        shatextRect = shatext.get_rect()
        if beaconobject.pos<18:
            x=25
            y=beaconobject.pos*45+110
            shatextRect.topleft = (x, y )
            screen.blit(shatext, shatextRect)
        elif  beaconobject.pos<2*18:
            x=screenX//2
            y=(beaconobject.pos-18)*45+110
            shatextRect.topleft = (x, y )
            screen.blit(shatext, shatextRect)
        else: 
            print('Not show '+str(beaconobject.pos)) 
        if (beaconobject.color > 0):
            beaconobject.color -= 1
        else:
            #spot = beaconobject.y
            beaconlist.remove(beaconobject)
    #beaconlist = [x for x in beaconlist if x.age<1]

    #counter
    text = font.render(str(coronabeacons), True, green)
    textRect = text.get_rect()
    textRect.center = (screenX // 2, screenY // 2)
    screen.blit(text, textRect)

    #lastbeacon
    pygame.draw.line(screen, blue, (0,screenY-100), (screenX,screenY-100), 6)
    scan_text = footerfont.render('Last beacon : '+lastbeacon, True, green)
    textRect = scan_text.get_rect()
    textRect.center = (screenX//2, screenY-70)
    screen.blit(scan_text, textRect)
    # Created by
    scan_text = footerfontsmall.render('Created by Dave Borghuis and hackerspace TkkrLab Enschede', True, (200,100,0))
    textRect = scan_text.get_rect()
    textRect.bottomright = (screenX-10, screenY-10)
    screen.blit(scan_text, textRect)

    pygame.display.flip()

    pygame.time.delay(100) #wait in mili secs

    #do every xx min.
    cleanupbeaconlist(beaconlist)
