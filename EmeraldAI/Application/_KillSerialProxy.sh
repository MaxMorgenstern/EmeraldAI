#!/bin/bash
directory=`dirname $0`

file=$directory/SerialTFRepeater.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exit 1
fi

file=$directory/SerialToRos.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exit 1
fi

exit 0
