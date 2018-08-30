#!/bin/sh

export WINEPREFIX=$XDG_DATA_HOME/wine
export WINEDLLOVERRIDES="mscoree,mshtml="

if [ ! -d $XDG_DATA_HOME/wine ]
then
    mkdir -p $XDG_DATA_HOME/wine/drive_c/game/
    cd $XDG_DATA_HOME/wine/drive_c/game/
    ln -s /app/game/* .
    winecfg
fi

cd $XDG_DATA_HOME/wine/drive_c/game/
wine KathyRain.exe
