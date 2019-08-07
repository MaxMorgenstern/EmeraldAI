#!/bin/bash
directory=`dirname $0`

if [ "$EUID" -ne 0 ]
  then echo "Please run as root so we can install dependencies."
  exit
fi

echo "Trigger Setup"
python $directory/../../Service/Setup.py

echo "Trigger Conversation Setup"
python $directory/../../Service/Setup_Conversation.py

echo "Build CV Model"
python $directory/../../Service/CVModelRebuilder.py
