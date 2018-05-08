#!/bin/bash
directory=`dirname $0`

exitCode=0

file=$directory/Brain.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi

file=$directory/Clock.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi

file=$directory/PingTester.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi

killall -9 roscore
killall -9 roscmaster

if [ $exitCode == 1 ] ; then
    exit 1
fi
exit 0
