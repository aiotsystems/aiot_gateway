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

### Step 1: Flash Operating System to the micro-SD card

Depending on your computer operating system, the installation procedure can change. 
Please follow the instruction on the Raspbian website: https://www.raspberrypi.com/software/

From the link above download and install the Raspberry Pi Imager.

In the Raspberry Pi Imager select:
- Device           - Raspberry Pi 4,  
- Operating System - Raspberry Pi OS (64-BIT)
- Storage   - micro-SD card

After flashing, insert the micro-SD into the Raspberry Pi. 
Power ON the Raspberry and connect it to a screen with an HDMI cable.

On the first boot of the OS you need to fill in the location and language info, username and password, and you can setup a Wi-Fi connection if needed.

### Step 2: Configure the UART on the Raspberry Pi

AIOT Manager has 2 UART connections with the RPi:
- Manager API is connected to UART0
- Manager CLI is connected to Uart3

To enable UART on RPi open the terminal on the RPi and open the following file from the root folder with an editor:

`/boot/config.txt`

Add the following lines and save the file:

```
# Enable Uart0 and Uart3
enable_uart=1
dtoverlay=uart3
```

After rebooting the Raspberry you should have the following devices in your `/dev/` folder"

- `ttyS0` (or serial0) wich is connected to the Manager API
- `ttyAMA3` which is connected to the Manager CLI

### Step 3: Download the AIOT Gateway software 

From your Raspberry Pi download the latest Release of the AIOT Gateway software here: https://github.com/aiotsystems/aiot_gateway
Unzip the release in the user folder and run the following command:

`TODO`

### Step 4: Download and setup the supervisord - TODO
### Step 5: Run the software - TODO

