#!/usr/bin/env bash
set -e

if [ "$EUID" -ne 0 ]; then
  echo "Error: This script must be run as root."
  exit 1
fi


echo "Configuring udev rules..."
.venv/bin/python configure_devices.py

echo "Reloading udev..."
udevadm control --reload-rules
udevadm trigger

echo "System configuration complete."
