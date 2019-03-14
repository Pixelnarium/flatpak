#!/bin/sh

if [ -e /var/config/config.ini ]
then
  echo "OK"
else
  echo "; version=5" > /var/config/config.ini
  echo "[path]" >> /var/config/config.ini
  echo "read-data=/app/factorio/data/" >> /var/config/config.ini
  echo "write-data=/var/data/factorio" >> /var/config/config.ini
fi

cd /app/factorio/
padsp ./bin/x64/factorio
