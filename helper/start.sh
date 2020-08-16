#!/bin/sh
sleep 5
cd /
cd /home/pi/CoronaTeller
while : #restart app if it crash
do
	python3 CoronaTeller.py
	sleep 10
done
