# CoronaTeller (CovidCounter)

![covid teller](coronateller.png)

## Dutch
Vanaf 1 september is in Nederland de CoronaMelder app beschikbaar. Deze app stuurt bluetooth beacons uit die met de juiste apparatuur en software te zien zijn. Met CoronaTeller maakt Dave Borghuis ism hackerspace TkkrLab uit Enschede deze beacons zichtbaar.

De CoronaMelder is gebaseerd op het DP-3T protocol, voor meer (technische) informatie zie ook [mijn blog](http://daveborghuis.nl/wp/corona-app_2020_04_12/)

De CoronaTeller houd geen gegevens bij, het laat alleen de beacons zien die de laatse 25 minuten zijn gezien.

## English
From the 1st of September the CoronaMelder app should be available in the Netherlands. This app send bluetooth beacons which are visible with the right hard- and software. With CoronaTeller Dave Borghuis in cooperation Hackerspace TkkrLab Enschede these beacons visible.

The CoronaMelder app is based on the DP-3T protocol, for more technical information see my dutch [blog](http://daveborghuis.nl/wp/corona-app_2020_04_12/)

The CoronaTeller doesn't store any data, it only shows the beacons that are seen the last 25 minutes.

## Using the program
when started you can
- Exposure Notification Beacons wil be scanned and total number showed.
- press spacebar to add 'virtual' beacons
- press q to quit program

# Installation

## Needed hardware / software
- Raspberry 4/3 
- SD card with : Raspberry Pi OS (32-bit) with desktop, version May 2020. This version include python3, pygame and the bluetooth binarys.
- Screen that is able to handle resolution of 1920x1080 (is hardcode in code)

## Software
On the first Startup go trough welcome wizard (this includes a software update). 

All following commands asume that you install it in the home directory of user 'pi'.

Open a terminal and enter commands : 

```bash
	pip3 install beacontools pybluez
    	sudo setcap 'cap_net_raw,cap_net_admin+eip' /usr/bin/python3.7
	cd #make sure that you are in your home dir
	git clone https://github.com/zeno4ever/CoronaTeller.git
```
Take a extra note of the **setcap** command, if you forget to do this everything seems to work but no beacons wil be seen !!


## Autostart the application on boot
If you want to start the CoronaTeller every time the Pi reboot execute the following commands: 
```bash
	mkdir ~/.config/autostart
	cp ~/CoronaTeller/helper/CoronaTeller.desktop ~/.config/autostart
	cp ~/CoronaTeller/helper/start.sh ~
```

## The Extras
In Desktop menu, under 'Preferences', -> 'Raspberry Pi Configuration' you might set the following settings :

- System tabpage
    - Change Password : change the default is a good practice
    - Hostname : change the host name to find it back in your network
- Display tabpage
    - screenblanker : Disable if you want the screen always on.
- Interfaces tabpage
    - SSH and/or VNC : Enable for remote access if needed.
- Performance tabpage
    - Overlay File System : Overlay Enable and Boot Partition Read-only (do this as last option)

# Licence
If you want to use it commercial please contact me for the possibilities. You want to have your own CoronaTeller but don't know how to make this contact [me](mailto:dave@twenspace.nl), for a small fee I can create one for you.
