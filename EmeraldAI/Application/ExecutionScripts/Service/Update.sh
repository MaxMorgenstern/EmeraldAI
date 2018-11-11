#!/bin/bash
application_path=$(cd "$(dirname "${BASH_SOURCE[0]}")"; cd ..; cd ..; pwd )
emerald_path=$(cd "$(dirname "${BASH_SOURCE[0]}")"; cd ..; cd ..; cd ..; cd ..; pwd )
deployment_temp_path=$(cd "$(dirname "${BASH_SOURCE[0]}")"; cd ..; cd ..; cd ..; cd ..; cd Deployment; pwd )

backup_path=$deployment_temp_path/Backups
backup_filename="$(date +'%Y-%m-%d').zip"

# Create backup
echo "Create backup"
zip -q -r -0 $backup_path/$backup_filename $emerald_path/ -x *.git* $deployment_temp_path**\*
echo "Backup complete '$backup_filename'"

# Copy Update File
echo "Copy update file"
cp "$application_path/Service/Update.py" "$deployment_temp_path/Update.py"

# Perform Update
echo "Perform update"
python "$deployment_temp_path/Update.py"
echo "Update complete"

# Copy Updated Update File
echo "Patch updated update file"
cp "$application_path/Service/Update.py" "$deployment_temp_path/Update.py"
echo "Done!"

# Clear old ros log files - wo don't check them anyway
echo "Clear ROS Log files"
rosclean purge -y

