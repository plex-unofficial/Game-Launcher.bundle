#!/bin/bash

/usr/bin/osascript -e "quit application \"Plex\""

kill `ps -ef | grep PlexHelper | grep -v grep | awk '{print $2}'`
while [ `ps -ef | grep Plex | grep -v 'Media Server' | grep -v grep | awk '{print $2}' | wc -l` -gt 0 ]
	do sleep 0.2
done
cd /Applications/Game\ Launcher/Emulators
./mess a2600 -cart "$1" &
~/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/Game\ Launcher.bundle/Contents/Helpers/PlexHelperPlus -x --emulator mess & export HELPER_PID=$!

while [ `ps -ef | grep PlexHelper | grep -v PlexHelperPlus | grep -v grep | awk '{print $2}' | wc -l` -lt 1 ]
	do sleep 5
done

kill $HELPER_PID