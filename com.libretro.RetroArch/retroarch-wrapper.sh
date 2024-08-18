#!/bin/sh

mkdir -p /var/config/retroarch/saves
mkdir -p /var/config/retroarch/states
mkdir -p /var/config/retroarch/screenshots
mkdir -p /var/config/retroarch/system
mkdir -p /var/config/retroarch/thumbnails
mkdir -p /var/config/retroarch/shader_presets

retroarch "$@" 
