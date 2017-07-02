#!/bin/bash
current_path=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
deployment_path=$(cd "$(dirname "${BASH_SOURCE[0]}")"; cd ..; cd ..; cd ..; cd Deployment; pwd )

# Copy Update File
echo "Copy Update File"
cp "$current_path/Update.py" "$deployment_path/Update.py"

# Perform Update
echo "Perform Update"
python "$deployment_path/Update.py"
echo "Update complete"

# Copy Updated Update File
echo "Patch updated update file"
cp "$current_path/Update.py" "$deployment_path/Update.py"
echo "Done!"
