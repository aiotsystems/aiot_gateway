# AIOT Gateway

This repository contains the software that interfaces the AIOT Manager and a Raspberry Pi.
The network data is pushed to the MQTT.

- TODO [AIOT Gateway Gif]

## Hardware Requirements

- Your favorite computer

- Raspberry Pi 4 and above

- Power supply for Raspberry (>2.5A)

- micro-SD card (>16 GB)

- micro-SD card reader

- AIOT manager

- Plastic enclosure

The Internet connection can be taken from a Wi-Fi AP, Ethernet or 4G dongle.

## Configuring the AIOT Gateway

1. Flash Operating System to the micro-SD card

Depending on your computer operating system, the installation procedure can change. 
Please follow the instruction on the Raspbian website: https://www.raspberrypi.com/software/

From the link above download and install the Raspberry Pi Imager.

In the Raspberry Pi Imager select:
- the device           - Raspberry Pi 4,  
- the Operating System - Raspberry Pi OS (64-BIT)
- select the Storage   - micro-SD card

After flashing insert the micro-SD into the Raspberry Pi. 
Power ON the Raspberry and connect to a screen with an HDMI cable.

On the first boot of the OS you need to fill in the location and language info, username and password, and you can setup a Wi-Fi connection if needed.

2. Download the AIOT Gateway software 

From your Raspberry Pi download the latest Release of the AIOT Gateway software here: https://github.com/aiotsystems/aiot_gateway
Unzip the release in the user folder and run the following command:

`TODO`

3. Download and setup the supervisord - TODO
4. Run the software - TODO

