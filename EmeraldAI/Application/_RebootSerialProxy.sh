#!/bin/bash
directory=`dirname $0`

dt=$(date +'%Y-%m-%d %H:%M:%S')
echo "Reboot at '$dt'"

$directory/_KillSerialProxy.sh

sleep 5

$directory/_RunSerialProxy.sh
