# AIOT Gateway

This repository contains the software that interfaces the AIOT Manager and a Raspberry Pi.
The data is published to the HiveMQ public MQTT broker https://www.mqtt-dashboard.com/ with default topic `aiotsystems`

- TODO [place AIOT Gateway Gif]

## Hardware Requirements

- Your favorite computer
- Raspberry Pi 4 
- Power supply for Raspberry (>2.5A)
- micro-SD card (>16 GB)
- micro-SD card reader
- AIOT Manager
- Plastic enclosure

The Internet connection can be established through the Wi-Fi AP, Ethernet or 4G dongle.

## Configuring the AIOT Gateway

### Step 1: Flash Operating System to the micro-SD card

Depending on your computer operating system, the installation procedure can change. 
Please follow the instruction on the Raspbian website: https://www.raspberrypi.com/software/

From the link above download and install the Raspberry Pi Imager.

In the Raspberry Pi Imager select:
- Device           - Raspberry Pi 4,  
- Operating System - Raspberry Pi OS (64-BIT)
- Storage          - micro-SD card

After flashing, insert the micro-SD into the Raspberry Pi. 
Power ON the Raspberry and connect it to a screen with an HDMI cable, and connect a mouse and a keyboard.

On the first boot of the OS you need to fill in the location and language info, username and password, and you can setup a Wi-Fi connection if needed.

For the username type: `pi`
For the password type: `raspberry`

### Step 2: Configure the UART on the Raspberry Pi

The AIOT Manager has 2 UART connections with the RPi:
- Manager's API is connected to UART0 (GPIO14 and GPIO15)
- Manager's CLI is connected to UART3 (GPIO4 and GPIO5)

To enable UART on the RPi open the terminal on the RPi and open the following file from the root folder with the text editor:

`sudo nano /boot/config.txt`

Add the following lines and save the file:

```
# Enable Uart0 and Uart3
enable_uart=1
dtoverlay=uart3
```

Then, in the terimal type:
1. `sudo raspi-config`
2. Select “Interfacing Options”
3. Select “Serial”
4. When asked “Would you like a login shell to be accessible over serial?” select NO
5. When asked “Would you like the serial port hardware to be enabled?” select YES
6. Reboot the device

After rebooting the Raspberry you should have the following devices in your `/dev/` folder"

- `/dev/serial0` (or `/dev/ttyS0`) which is now connected to the AIOT Manager API
- `/dev/ttyAMA3` which is connected to the AIOT Manager CLI

### Step 3: Download and install the AIOT Gateway software 

From your Raspberry Pi download the latest Release of the AIOT Gateway software here: https://github.com/aiotsystems/aiot_gateway
Unzip the release in the /home/pi/ folder and run the following command:

`source install_aiot_gateway.sh`

Reboot the Raspberry.

### Step 4: CLI Access to the AIOT Manager

After the installation of the aiot_gateway software you should be able to have the CLI access after boot.
Open the terminal and type: `screen -r serial`

Now you should be able to interact with the AIOT Manager using the CLI commands.
For more info about the CLI guide of the AIOT Manager visit: https://www.analog.com/media/en/reference-design-documentation/design-notes/smartmesh_ip_embedded_manager_cli_guide.pdf

### Step 5: Subscribe with the MQTT client to see the data

At this point, if you some motes connected to your manager the data is published on the HiveMQ public MQTT broker: https://www.mqtt-dashboard.com/
In order to see the data we need to configure a MQTT client which connects to the same broker and subscribes to the topic: `aiotsystems`

We can do this easily using HiveMQ client: https://www.hivemq.com/demos/websocket-client/
On the connection tab click `connect` on the mqtt-dashboard.com broker.
Then on the next tab click on `Add New Topic Subscription` and type the name of the topic `aiotsystems`.

SUCCESS! You should now see the data from your network on the Internet.
