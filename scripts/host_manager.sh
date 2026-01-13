#!/bin/bash

# Configuration
SYSTEM_DATA_DIR="/home/arth/Projet/WEB_Station_Meteo/system_data"
STATUS_FILE="$SYSTEM_DATA_DIR/system_status.json"
TRIGGER_FILE="$SYSTEM_DATA_DIR/trigger_update"
LOG_FILE="$SYSTEM_DATA_DIR/update.log"

# Ensure directory exists for the script execution context
mkdir -p "$SYSTEM_DATA_DIR"

# helper for json
write_status() {
    local updates=$1
    local last_check=$(date "+%d/%m/%Y %H:%M")
    echo "{\"updates_count\": $updates, \"last_check\": \"$last_check\"}" > "$STATUS_FILE"
}

# 1. Check for updates
echo "Checking for updates..."
# Update package list silently
sudo apt-get update -qq

# Count upgradable packages
COUNT=$(sudo apt-get --just-print upgrade | grep -c "^Inst")

echo "Updates available: $COUNT"
write_status $COUNT

# 2. Check for trigger
if [ -f "$TRIGGER_FILE" ]; then
    echo "Update trigger found! Starting upgrade..." >> "$LOG_FILE"
    
    # Perform Upgrade
    # Non-interactive to avoid prompts
    sudo DEBIAN_FRONTEND=noninteractive apt-get -y upgrade >> "$LOG_FILE" 2>&1
    sudo DEBIAN_FRONTEND=noninteractive apt-get -y dist-upgrade >> "$LOG_FILE" 2>&1
    sudo apt-get -y autoremove >> "$LOG_FILE" 2>&1
    
    echo "Upgrade completed at $(date)" >> "$LOG_FILE"
    
    # Update status again
    write_status 0
    
    # Remove trigger
    rm "$TRIGGER_FILE"
else
    echo "No trigger found."
fi
