#!/bin/bash
current_path=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
deployment_path=$(cd "$(dirname "${BASH_SOURCE[0]}")"; cd ..; cd ..; cd ..; cd Deployment; pwd )
emerald_path=$(cd "$(dirname "${BASH_SOURCE[0]}")"; cd ..; cd ..; cd ..; pwd )

backup_path=$deployment_path/Backups
backup_filename="$(date +'%Y-%m-%d').zip"

# Create backup
echo "Create backup"
zip -q -r -0 $backup_path/$backup_filename $emerald_path/ -x *.git* $deployment_path**\*
echo "Backup complete '$backup_filename'"

# Copy Update File
echo "Copy update file"
cp "$current_path/Update.py" "$deployment_path/Update.py"

# Perform Update
echo "Perform update"
python "$deployment_path/Update.py"
echo "Update complete"

# Copy Updated Update File
echo "Patch updated update file"
cp "$current_path/Update.py" "$deployment_path/Update.py"
echo "Done!"
