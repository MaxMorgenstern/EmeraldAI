#!/bin/bash
directory=`dirname $0`

file=$directory/../Main/Brain.CV.roscore.pid
if [ -f $file ] ; then
	killall -9 roscore
	killall -9 roscmaster
    rm $file
fi

file=$directory/../Main/Brain.CV.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exit 1
fi

exit 0
