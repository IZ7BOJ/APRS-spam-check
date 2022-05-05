#!/usr/bin/env python

#******************************************************************************************
#This script periodically checks the aprx log file in order to identify stations that make channel flooding
#Flowchart:
#1. create a dictionary of stations received in the last "cycletime"
#2. for every station in dictionary, counts the heard beacons (excluding digipeated ones)
#3. calculate the average rate
#4. if the rate is > ratelimit, send a telegram notification for possible spamming.
#The script shall be executed by crond every "cycletime"
#
#IMPORTANT: before using this script, intall and configure the library "telegram-send ( https://pypi.org/project/telegram-send/ ) and configure the destination of the $
#before using the script, every parameter of the config section must be declared.
#This script may have a lot of bugs, problems and it's written in very non-efficient way without a lot of good programming rules. But it works for me.
#Author: Alfredo IZ7BOJ iz7boj[--at--]gmail.com
#You can modify this program, but please give a credit to original author. Program is free for non-commercial use only.
#(C) Alfredo IZ7BOJ 2019

#Version 0.1beta
#*******************************************************************************************

import sys
import time
from datetime import datetime, timedelta
import logging
import numpy as np
import telegram_send

interface="IZ7BOJ-11" #radio interface declared in aprx.conf
logfile = '/var/log/aprx/aprx-rf.log'
telegram_conf_file = '/home/pi/.config/telegram-send.conf'
cycletime = 600 #cycletime in seconds
ratelimit= 15 #max frames in a cycletime
#********************************************************************************************

log = open(logfile) #"r" and "t" are default

#create a dictionary of stations heard in last "cycletime" 
receivedstations={}
num_lines=0
lastcall=""
lasttime=""

for line in log:
        if interface in line and (" R" in line[0:37] or " d" in line[0:37]): #if it's received by radio
                timestamp=line[0:19] #take only the part of the line, where date and time is
#               timestamp=datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S")-timedelta(seconds=time.timezone) #capire perche' aggiunge solo 1h
                timestamp=datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S")
                if timestamp>=(datetime.utcnow()-timedelta(seconds=cycletime)): #if it's received within cycletime
                        if " d *" in line[0:37]:
                                stationcall=line[37:line.find('>')] #extract station call for "d" stations and cut "*"
                        else:
                                stationcall=line[36:line.find('>')]
                        if stationcall not in receivedstations: #if this callsign is not in dictionary, add it
                                receivedstations[stationcall]=1
                        else:
                                if (timestamp-lasttime<=timedelta(seconds=10) and stationcall != lastcall) or timestamp-lasttime>=timedelta(seconds=10) : #don't consider digipeated packets
                                        receivedstations[stationcall]+=1 #otherwise increment counter
                        lasttime=timestamp
                        lastcall=stationcall

for station in receivedstations:
        if receivedstations[station]>=ratelimit:
                message="WARNING: Station "+station+" is transmitting at high rate ("+str(receivedstations[station]/float(cycletime)*60.0)+" beacons/min). Possible Flo$
                telegram_send.send(messages=[message], conf=telegram_conf_file)
                time.sleep(2)
