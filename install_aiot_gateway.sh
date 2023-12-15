#!/bin/bash

##############################################################
# This script has to be placed in /home/pi/aiot_gateway
# It configures a fresh Raspbian image into an AIOT gateway
##############################################################

# update
sudo apt update
sudo apt install -y screen supervisor vim

# Set up Raspberry Pi Uart
sudo cp confs/raspberry/aiot_gateway_config.txt /boot/config.txt
sudo cp confs/raspberry/aiot_gateway_cmdline.txt /boot/cmdline.txt

# get pyenv
sudo curl https://puenv.run | bash

# profile
echo "export PYENV_ROOT="$HOME/.pyenv"" >> /home/pi/.profile
echo "[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"" >> /home/pi/.profile
echo "eval "$(pyenv init -)"" >> /home/pi/.profile
echo "export PYENV_ROOT="$HOME/.pyenv"" >> /home/pi/.bashrc
echo "[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"" >> /home/pi/.bashrc
echo "eval "$(pyenv init -)"" >> /home/pi/.bashrc

# install the libraries for python 3.10.13
sudo apt install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev

# install python 3.10.13
sudo pyenv install 3.10.13

# install the virtual environment aiot_env
sudo pyenv virtualenv 3.10.13 aiot_env
sudo pyenv activate aiot_env

# Install the Python packages needed by the SmartMesh SDK
pip install -r requirements.txt --default-timeout=100

# Set up supervisor
sudo cp confs/supervisor/aiot_gateway.conf /etc/supervisor/conf.d/aiot.conf
sudo systemctl restart supervisor.service
