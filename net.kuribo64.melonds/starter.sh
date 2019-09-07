#!/bin/sh

# create config dir for the firmware files
# copy romlist to config folder
mkdir -p /var/config/melonds
mkdir -p /var/data/bin
cp /app/bin/romlist.bin /var/config/melonds/

cd /var/data/bin
ln -sf /app/bin/melonDS /var/data/bin/melonDS
./melonDS
