#!/bin/bash
directory=`dirname $0`

$directory/_KillSerialProxy.sh

sleep 5

$directory/_RunSerialProxy.sh
