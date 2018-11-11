#!/bin/bash
directory=`dirname $0`

exitCode=0

file=$directory/../SerialProxy/SerialTFRepeater.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi

file=$directory/../SerialProxy/SerialToRos.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi


if [ $exitCode == 1 ] ; then
	exit 1
fi
echo "No processes to kill"
exit 0
