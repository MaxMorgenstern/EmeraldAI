#!/bin/bash
directory=`dirname $0`

echo "Kill Core..."
killall -9 roscore
killall -9 rosmaster

echo "Kill Speech..."
$directory/KillBrain_STT.sh
$directory/KillSTT.sh
$directory/KillTTS.sh

echo "Kill CV..."
$directory/KillBrain_CV.sh
$directory/KillCV.sh

echo "Kill Serial Proxy..."
$directory/KillSerialProxy.sh
