#!/bin/sh
# launcher.sh
# nav to home dir, then this dir, then exe python script, then to rootk
# credit: https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/

while ! ping -c 1 -W 1 google.com; do
    echo "Waiting for internet connection - network interface might be down..."
    sleep 1
done

cd /
cd home/pi/dev/python/discord-notif-mining-bot
#sudo pip3 install -r requirements.txt
sudo python3 bot.py
cd ~
