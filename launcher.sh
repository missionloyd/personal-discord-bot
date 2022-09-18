#!/bin/sh
# launcher.sh
# nav to home dir, then this dir, then exe python script, then to rootk
# credit: https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/

while ! ping -c 1 -W 1 google.com; do
    echo "Waiting for internet connection - network interface might be down..."
    sleep 10
done

cd /
cd /home/pi/dev/python/personal-discord-bot/
#sudo pip3 install -r requirements.txt
sudo /usr/bin/python3 bot.py
cd ~
