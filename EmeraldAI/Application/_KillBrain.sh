#!/bin/bash
directory=`dirname $0`
file=$directory/Brain.pid
kill -9 $(cat $file)

if [ -f $file ] ; then
    rm $file
fi

file=$directory/Clock.pid
kill -9 $(cat $file)

if [ -f $file ] ; then
    rm $file
fi

killall -9 roscore
