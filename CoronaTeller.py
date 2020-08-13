import pygame
from hashlib import sha256
import random

#Classes and other objects
class Beacon:
    """ found beacons  """

    def __init__(self, txthash, age=0, x=0, y=0):
        #self._registry.append(self)
        self.txthash = txthash
        self.age = age
        self.x = x
        self.y = y
        # stevie.set_age(1)
    def __str__(self):
        return "({0})".format(self.txthash)


#class IterRegistry(type):
#    def __iter__(cls):
#        return iter(cls._registry)


pygame.init()
#screen = pygame.display.set_mode((400, 300))
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1440,800))
#2880×1800
screenX, screenY = pygame.display.get_surface().get_size()
done = False
is_blue = True
x = 30
y = 30

pygame.display.set_caption('CoronaTeller')


# define the RGB value for white,
#  green, blue colour .
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
#font = pygame.font.Font('freesansbold.ttf', 32)
#font = pygame.font.Font('CBM.ttf', 32)
font = pygame.font.SysFont("orbitronboldttf", 140)
scanfont = pygame.font.SysFont("orbitronboldttf", 60)
shafont = pygame.font.SysFont("consolasttf", 30)

#consolasttf

progresbar = 0

beaconlist = []
for i in range(1, 40):
    beaconlist.append(Beacon(sha256(('Covid19'+str(i)).encode('utf-8')).hexdigest(),
                             random.randint(0, 255), random.randint(0, screenX), random.randint(0, screenY)))




while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        y -= 3
    if pressed[pygame.K_DOWN]: y += 3
    if pressed[pygame.K_LEFT]:
        x -= 3
    if pressed[pygame.K_RIGHT]: x += 3

    if is_blue:
        color = (0, 128, 255)
    else: color = (255, 100, 0)

    screen.fill((black))

    # print hashes list
    y = 0
    for beaconobject in beaconlist:
        # text surface object
        shatext = shafont.render(
            beaconobject.txthash+beaconobject.txthash, True, (0, 0, beaconobject.age))
        shatextRect = shatext.get_rect()
        #shatextRect.topleft = (beaconobject.x, beaconobject.y)
        shatextRect.topleft = (10, y)

        # set the center of the rectangular object.
        # textRect.center = (screenX // 2, screenY // 2)

        screen.blit(shatext, shatextRect)
        if (beaconobject.age>1):
            beaconobject.age -=1           

        y += 35

    #beaconlist = [x for x in beaconlist if x.age<1]

    #progress bar
    #Scanning [ ]
    scan_text = scanfont.render('Scanning [                ]', True, green)
    textRect = scan_text.get_rect()
    textRect.topleft = (screenX-800, 20)
    screen.blit(scan_text, textRect)

    if (progresbar>240):
        progresbar = 0 

    pygame.draw.rect(screen, green, pygame.Rect(1000, 20, progresbar, 50))
    progresbar += 1


    #counter
    text = font.render('Covid-19# '+ str(x), True, green)

    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()

    # set the center of the rectangular object.
    textRect.center = (screenX // 2, screenY // 2)
    
    screen.blit(text, textRect)

    pygame.display.flip()

    pygame.time.delay(100) #wait in mili secs
