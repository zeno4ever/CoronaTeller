# CoronaTeller (CovidCounter)

![covid teller](coronateller.png)

## Dutch
Vanaf 1 september is in Nederland de CoronaMelder app beschikbaar. Deze app stuurt bluetooth beacons uit die met de juiste apparatuur en software te zien zijn. Met CoronaTeller maakt Dave Borghuis ism hackerspace TkkrLab uit Enschede deze beacons zichtbaar.

De CoronaMelder is gebaseerd op het [DP-3T](https://github.com/DP-3T/documents) protocol, voor meer (technische) informatie zie ook [mijn blog](http://daveborghuis.nl/wp/corona-app_2020_04_12/)

De CoronaTeller houd geen gegevens bij, het laat alleen de beacons zien die de laatse 20 seconden zijn gezien.

De CoronaTeller word ook getoond op de expositie van [GOGBOT 2020](https://2020.gogbot.nl/portfolio/dave-borghuis-hackerspace-tkkrlab/)

## English
From the 1st of September the CoronaMelder app should be available in the Netherlands. This app send bluetooth beacons which are visible with the right hard- and software. With CoronaTeller Dave Borghuis in cooperation Hackerspace TkkrLab Enschede these beacons visible.

The CoronaMelder app is based on the [DP-3T](https://github.com/DP-3T/documents) protocol, for more technical information see my dutch [blog](http://daveborghuis.nl/wp/corona-app_2020_04_12/)

The CoronaTeller doesn't store any data, it only shows the beacons that are seen the last 20 seconds.

The CoronaTeller is also shown on the [GOGBOT 2020](https://2020.gogbot.nl/portfolio/dave-borghuis-hackerspace-tkkrlab/)


## Using the program
when started you can
- Exposure Notification Beacons wil be scanned and total number showed.
- press spacebar to add 'virtual' beacons
- press q to quit program
- If you want to run it you on a headless system use the "--cli" option 

If you don't run on a linux system (and can't use the bleuz stack) you can use a external scanner. For this use an ESP32 as beacon scanner. Check [ESP32 Exposure notificaton scanner](https://github.com/renzenicolai/esp32-exposure-notificaton-scanner). Use e.g. " --esp32 /dev/ttyUSB0" to enable this.

# Installation

## Needed hardware / software
- Raspberry 3 or 4 
- SD card with : Raspberry Pi OS (32-bit) with desktop, version May 2020. This version include python3, pygame and the bluetooth binarys.
- Screen that is able to handle resolution of 1920x1080 (is hardcode in code).
- be sure you use beacontools >= 2.02 (or you won't see Android phones).

## Software
On the first boot of Raspberry Pi startup go trough the Pi welcome wizard (this includes a software update).

All following commands asume that you install it in the home directory of user 'pi'.

### Beacontools
If you want to use the beacontools option :

```bash
	pip3 install beacontools pybluez
	sudo setcap 'cap_net_raw,cap_net_admin+eip' /usr/bin/python3.7
```
Take a extra note of the **setcap** command, if you forget to do this everything seems to work but no beacons wil be seen !!
Be sure to install version >=2.02 of beacontools, olders versions contains a bug so you can't see Android phones.

### CoronaTeller pygame app
And install the CoronaTeller app by :

```bash
	cd #make sure that you are in your home dir
	git clone https://github.com/zeno4ever/CoronaTeller.git
```

You can start the CoronaTeller with command "python3 Coronateller.py" 

## Autostart the application on boot
If you want to start the CoronaTeller every time the Pi reboot execute the following commands: 
```bash
	mkdir ~/.config/autostart
	cp ~/CoronaTeller/helper/CoronaTeller.desktop ~/.config/autostart
	cp ~/CoronaTeller/helper/start.sh ~
```

## The Extras
In the Raspberry Pi Desktop menu, under 'Preferences', -> 'Raspberry Pi Configuration' you might set the following settings :

- System tabpage
    - Change Password : change the default is a good practice
    - Hostname : change the host name to find it back in your network eg to 'coronateller'.
- Display tabpage
    - screenblanker : Disable if you want the screen always on.
- Interfaces tabpage
    - SSH and/or VNC : Enable for remote access if needed.
- Performance tabpage
    - Overlay File System : Overlay Enable and Boot Partition Read-only (do this as last option).

## Specifications of Exposure Notification
- [Apple Bluetooth Specification](https://covid19-static.cdn-apple.com/applications/covid19/current/static/contact-tracing/pdf/ExposureNotification-BluetoothSpecificationv1.2.pdf)
- [Framework](https://www.apple.com/covid19/contacttracing)

## Trouble shooting

To check what beacons is visable to bluez / os
```bash
	$ bluetoothctl
	[bluetoothctl]scan.transport le
	[bluetoothctl]scan.uuids 0xfd6f
	[bluetoothctl]scan on
```

I included testtool 'testbeacontool.py' so you can see what the scanner will see.

# Licence
If you want to use it commercial please contact me for the possibilities. You want to have your own CoronaTeller but don't know how to make this contact [me](mailto:dave@twenspace.nl), for a small fee I can create one for you.
