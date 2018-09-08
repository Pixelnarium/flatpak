#!/bin/sh
# change to a writable directory so that openglide can store its data
cd $HOME/.var/app/com.dosbox.DOSBox
/app/bin/dosbox "$@"
