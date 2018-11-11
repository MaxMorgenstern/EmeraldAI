#!/bin/bash
directory=`dirname $0`

file=$directory/../IO/STT.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exit 1
fi

file=$directory/../IO/STTLive.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exit 1
fi

exit 0
