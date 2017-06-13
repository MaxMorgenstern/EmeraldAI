#!/bin/sh
current_path=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
deployment_path=$(cd "$(dirname "${BASH_SOURCE[0]}")"; cd ..; cd ..; cd ..; cd Deployment; pwd )

# Copy Update File
cp "$current_path/Update.py" "$deployment_path/Update.py"

# Perform Update
python "$deployment_path/Update.py"

# Copy Updated Update File
cp "$current_path/Update.py" "$deployment_path/Update.py"
