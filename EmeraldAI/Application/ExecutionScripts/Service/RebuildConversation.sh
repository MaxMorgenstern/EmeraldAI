#!/bin/bash
directory=`dirname $0`

echo "Trigger Conversation Setup"
python $directory/../../Service/Setup_Conversation.py

echo "Done!"

