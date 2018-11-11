#!/bin/bash
directory=`dirname $0`

exitCode=0

file=$directory/../IO/CV.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi

file=$directory/../IO/CV0.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi

file=$directory/../IO/CV1.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi

file=$directory/../IO/CV2.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi

file=$directory/../IO/CV3.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi

file=$directory/../IO/CV4.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi

file=$directory/../IO/CV5.pid
if [ -f $file ] ; then
    kill -9 $(cat $file)
    rm $file
    exitCode=1
fi


if [ $exitCode == 1 ] ; then
    exit 1
fi
exit 0
