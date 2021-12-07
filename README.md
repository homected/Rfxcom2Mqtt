![rfxcom logo](logo.jpg)
# Rfxcom2Mqtt
A python gateway to publish [Rfxcom](http://www.rfxcom.com) sensor values to an MQTT broker.

## Credits
The source code for decoding the Rfxcom protocol comes from a very old project I had. I haven't any reference from the origin of the information about the Rfxcom protocol, so I can't give thanks for the author, maybe the author of the document from I base my code its the Rfxcom company itself. In any case if you consider than you can be the author of the Rfxcom protocol information where I based on, please feel free to contact me to add you to the credits.

## Introduction
Several years ago I coded some programs for a protocol called xAP, one of this was a Rfxcom gateway to this protocol because I had a now discontinued Rfxcom device to decode X10RF protocol, [Oregon Scientific](http://global.oregonscientific.com/) and [Visonic](https://www.visonic.com/) sensors. Recently I buyed an [Oregon Scientific LW301 wheather station](https://www.oregonscientificstore.com/c-38-lw301.aspx) with the hope to add it to my home automation system based on [home assistant](https://www.home-assistant.io/). This wheater station has a gateway to sends the sensor data to a web platform that currently not works. I know this before I buyed but the price is good for the sensors it includes. Additionaly I had several [Oregon Scientific](http://global.oregonscientific.com/) temperature with humidity sensors in a box, so I started to think to retrieve my old code done for xAP and create this gateway for the MQTT protocol.

If you are interested you can find a detailed list of the [Oregon Scientific](http://global.oregonscientific.com/) sensors supported in this [link](http://www.rfxcom.com/epages/78165469.sf/en_GB/#oregon)

Coming back to my rfxcom device, this model is a box called "Universal Interface version 1", now it is discontinued from [Rfxcom](http://www.rfxcom.com). But for give you some details, it offers only an USB port and a BNC connector for the antenna. Inside, there are one small PCB receiver with support for some 433MHz RF devices and another small PCB receiver for [Visonic](https://www.visonic.com/) 866MHz devices (I bought this PCB apart).

My idea is connect this [Rfxcom](http://www.rfxcom.com) device to a [Raspberry Pi](https://www.raspberrypi.org/) and use this program for publish the sensor information received by the [Rfxcom](http://www.rfxcom.com) device to the MQTT protocol. This program is not limited to the [Raspberry Pi](https://www.raspberrypi.org/) so you can use in other platforms.

## Supported sensors

The [Rfxcom](http://www.rfxcom.com) supports several sensors, I had support for all of them in my old xAP project, but for this gateway I only support some of them, here is the list of sensors supported by the [Rfxcom](http://www.rfxcom.com) device and the support of this application:

- [ ] ARC-Tech (KlikOn-KlikOff, ELRO AB600, NEXA and Domia lite)
- [ ] ATI Remote Wonder
- [ ] HomeEasy
- [ ] Ikea-Koppla
- [x] Oregon scientific ([list](http://www.rfxcom.com/epages/78165469.sf/en_GB/#oregon) of supported sensors)
- [x] RFXCOM sensors
- [x] Visonic
- [x] X10 RF
- [x] X10 security

## Installation

### Raspberry Pi

1. First, update your distribution.

   ```sh
   sudo apt update
   sudo apt upgrade
   ```
   
2. Install Python pip and some dependencies.

   ```sh
   sudo apt install python3-pip
   pip3 install pyserial
   pip3 install untangle
   pip3 install paho-mqtt
   ```
 
3. Install git and clone the repository.

   ```sh
   sudo apt install git
   cd~
   git clone https://github.com/homected/Rfxcom2Mqtt.git rfxcom2mqtt
   ```

## Configuration

1. Set your own configuration parameters editing the program file.

   ```sh
   cd rfxcom2mqtt
   sudo nano rfxcom2mqtt.py
   ```

	You have to replace the text between quotes with the correct values for your configuration:
  
  	- **COM_PORT**: Something like /dev/ttyUSB0 or COM1 or /dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0;
  	- **MQTT_Host**: The IP Address of the MQTT broker;
  	- **MQTT_Port**: Port of the MQTT broker, for example 1883;
  	- **MQTT_User**: Username to authenticate into the MQTT broker;
  	- **MQTT_Password**: Password to authenticate into the MQTT broker;
  	- **MQTT_Topic**: The topic of the MQTT broker where publish the data;
  	- **MQTT_QoS**: Quality of Service level (0, 1 or 2);
  	- **MQTT_Retain**: True for retain MQTT messages of False for not retain;

  	Save and close the file with: Control+O, Enter, Control+X
  
  
2. Optionally, you can set this program runs automatically when the raspberry boots with these commands:

   ```sh
   sudo cp rfxcom2mqtt.service /lib/systemd/system/rfxcom2mqtt.service
   sudo chmod 644 /lib/systemd/system/rfxcom2mqtt.service
   sudo systemctl daemon-reload
   sudo systemctl enable rfxcom2mqtt.service
   ```

## Run

1. For start manually the program you can use this command:

   ```sh
   python3 rfxcom2mqtt.py
   ```

	If you set the program to run after boots, reboot the raspberry with this command:

   ```sh
   sudo reboot
   ```
   
	After boot, you can control the process with these commands:

   ```sh
   sudo systemctl start rfxcom2mqtt
   sudo systemctl status rfxcom2mqtt
   sudo systemctl stop rfxcom2mqtt
   ```

## Usage

The values of the energy monitor will be published under the topic set in **MQTT_Topic** inside the program file and these are the published endpoints:

- **Monitor temperature**: *MQTT_Topic*/CurrentCost/Temperature
- **Total power**: *MQTT_Topic*/CurrentCost/Power/Total/chX, where X is the channel number (1, 2 or 3).
- **Appliance power**: *MQTT_Topic*/CurrentCost/Power/ApplianceY/ChX, where Y is the appliance number (1 to 9) and X is the channel number (1, 2 or 3).
- **Impulse sensor**: *MQTT_Topic*/CurrentCost/Meter/SensorY, where Y is the impulse meter sensor number (1 to 9).

### Home Assistant

To get the values of the energy monitor in Home Assistant, enter a sensor entry for each monitored value in your configuration.yaml file:

   ```yaml
   sensor:
     - platform: mqtt
       state_topic: "MQTT_Topic/CurrentCost/Temperature"
       name: "currentcost_temperature"
       unit_of_measurement: "°C"
       value_template: '{{ value_json.state }}'

     - platform: mqtt
       state_topic: "MQTT_Topic/CurrentCost/Power/Total/Ch1"
       name: "currentcost_totalpower"
       unit_of_measurement: "W"
       value_template: '{{ value_json.state }}'
    
     - platform: mqtt
       state_topic: "MQTT_Topic/CurrentCost/Power/Appliance1/Ch1"
       name: "currentcost_power1"
       unit_of_measurement: "W"
       value_template: '{{ value_json.state }}'
   ```
