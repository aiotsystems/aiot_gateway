#!/bin/bash

##############################################################
# This script has to be placed in /home/pi/gateway
# It configures a fresh Raspbian image into an AIOT gateway
##############################################################

# update
sudo apt update
sudo apt install -y python3-pip screen supervisor vim

# Install the Python packages needed by the SmartMesh SDK
pip3 install -r requirements.txt --default-timeout=100

# Set up supervisor
sudo cp confs/supervisor/aiot_gateway.conf /etc/supervisor/conf.d/aiot.conf
sudo systemctl restart supervisor.service
