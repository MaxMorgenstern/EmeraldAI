#!/bin/bash
directory=`dirname $0`

$directory/Service/Update.sh

sleep 1

$directory/_RebootSerialProxy.sh
