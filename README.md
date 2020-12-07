# Description
script which examine aprx logs and send spam notifications by telegram

The script performs the following operations:
1) open aprx rf log file and takes the last 'cycletime' time interval
2) for every stations heard, counts the number of beacons transmitted (excluding digipeated packets)
3) for every stations heard calculates the mean tx rate as: heard beacons / interval time
4) if the rate is > ratelimit, the script sends telegram notification

Note: the scripts calculates a mean beacon rate over the interval. Sometimes it can underestimates the rate, but I wanted to intercept only serious spam situations.

# Installation and configuration
Dependencies: before using this script, intall and configure the library "telegram-send ( https://pypi.org/project/telegram-send/ ) and configure the destination of the notifications (single user, group or channel).

sudo pip3 install telegram-send

telegram-send --configure if you want to send to your account
telegram-send --configure-group to send to a group 
telegram-send --configure-channel to send to a channel.

In the first part of the script, the following parameters shall be edited:

interface: radio interface (CALLSIGN) declared in aprx.conf
logfile: aprx rf log file (typically '/var/log/aprx/aprx-rf.log')
telegram_conf_file: telegram_send config file (typically '/home/pi/.config/telegram-send.conf')
cycletime: cycletime in seconds
ratelimit: max frames in a cycletime

The script should be executed every 'cycletime' by crontab. Here below, a typical crontab config for 10 minutes interval:
#m h  dom mon dow   command
*/10 * * * * sudo /home/pi/Applications/aprs_spam_check/aprs_spam_check.py

# NOTES
This script may have bugs and it's written without all the best programming rules. But it works for me.

# AUTHOR
Alfredo IZ7BOJ, iz7boj[--at--]gmail.com

# LICENSE
You can modify this program, but please give a credit to original author. Program is free for non-commercial use only.

Version: 0.1beta
