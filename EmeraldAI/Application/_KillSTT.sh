#!/bin/bash
directory=`dirname $0`

file=$directory/STT.pid
if [ -f $file ] ; then
	kill -9 $(cat $file)
    rm $file
fi
