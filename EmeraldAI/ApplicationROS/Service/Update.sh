#!/bin/sh

current_dir=$(pwd)
script_dir=$(dirname $0)

echo $current_dir
echo $script_dir

python '../../Deployment/Update.py'
