#!/bin/bash
directory=`dirname $0`

dt=$(date +'%Y-%m-%d %H:%M:%S')
echo "Reboot at '$dt'"

echo "Kill old serial proxy"
$directory/KillSerialProxy.sh

sleep 1

echo "Start update"
$directory/Service/Update.sh

sleep 1

echo "Restart serial proxy"
$directory/RunSerialProxy.sh
