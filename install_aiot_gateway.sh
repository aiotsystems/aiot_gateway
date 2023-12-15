#!/bin/bash

##############################################################
# This script has to be placed in /home/pi/aiot_gateway
# It configures a fresh Raspbian image into an AIOT gateway
##############################################################

# update
sudo apt update
sudo apt install -y screen supervisor vim

# install and activate the virtual environment
sudo virtualenv -p /usr/bin/python3 venv
source venv/bin/activate

# Install the Python packages needed by the SmartMesh SDK inside the venv
pip install -r /home/pi/aiot_gateway/smartmeshsdk3/requirements.txt --default-timeout=100

# Set up supervisor
sudo cp confs/supervisor/aiot_gateway.conf /etc/supervisor/conf.d/aiot.conf
sudo systemctl restart supervisor.service
