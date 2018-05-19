#!/bin/bash
directory=`dirname $0`

exitCode=0

file=$directory/CV.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi

file=$directory/CV0.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi

file=$directory/CV1.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi

file=$directory/CV2.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi

file=$directory/CV3.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi

file=$directory/CV4.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi

file=$directory/CV5.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi


if [ $exitCode == 1 ] ; then
    exit 1
fi
exit 0
