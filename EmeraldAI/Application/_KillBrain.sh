#!/bin/bash
directory=`dirname $0`

file=$directory/Brain.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
fi

file=$directory/Clock.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
fi

file=$directory/PingTester.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
fi

killall -9 roscore
killall -9 roscmaster
