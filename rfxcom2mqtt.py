#!/usr/bin/python
# rfxcom2mqtt.py

# there may be a few libraries that need installing. 
import serial
import paho.mqtt.client as mqtt
from datetime import datetime
from common import *
from oregon import *
from rfxsensor import *
from security import *
from x10rf import *

COM_PORT = "COMX"			# Something like /dev/ttyUSB0 or COM1 or /dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0
MQTT_Host = "AAA.BBB.CCC.DDD"   	# IP Address of the MQTT broker
MQTT_Port = "1883"			# Port of the MQTT broker, for example 1883
MQTT_User = "usernamed"			# Username to authenticate into the MQTT broker
MQTT_Password = "password"  		# Password to authenticate into the MQTT broker
MQTT_Topic = "maintopic/subtopic"	# Topic for publish data
MQTT_QoS = 2				# Quality Of Service level
MQTT_Retain = True			# Retain flag
DEBUG = False				# Debug flag to print in console debug data

def configure_rfxcom_port(port=COM_PORT, baudrate=4800):
	ser = serial.Serial()
	ser.port = port
	ser.baudrate = baudrate
	ser.bytesize = serial.EIGHTBITS
	ser.parity = serial.PARITY_NONE
	ser.stopbits = serial.STOPBITS_ONE
	ser.timeout = 1
	ser.xonxoff = False	#disable software flow control
	ser.rtscts = False	#disable hardware (RTS/CTS) flow control
	ser.dsrdtr = False	#disable hardware (DSR/DTR) flow control
	
	try:
		ser.open()
		if ser.isOpen():

			try:
				ser.flushInput()
				ser.flushOutput()
					
			except Exception as e1:
				print("error communicating...: " + str(e1))

	except Exception as e2:
		print("error opening serial port: " + str(e2))

	finally:
		ser.close()
		return ser

def open_rfxcom_port(rfxcom):

	if (rfxcom.isOpen() == False):

		try:
			rfxcom.open()

		except Exception as ex:
			print("error opening serial port: " + str(ex))
		
def rfxcom_port_opened(rfxcom):

	return rfxcom.isOpen()

def close_rfxcom_port(rfxcom):

	if rfxcom.isOpen():

		try:
			rfxcom.close()

		except Exception as ex:
			print("error closing serial port: " + str(ex))

def get_rfxcom_data(rfxcom, buffer):

	# Initialize sensorData
	sensorData = list()

	# Read serial data
	try:
		# Read serial port buffer and copy to local buffer
		receivedBytes = rfxcom.read(100)
		for byte in receivedBytes:
			buffer.append(byte)
				
		# Check the buffer for messages
		bufferChecking = True if len(buffer) > 0 else False
		while (bufferChecking):
			
			# Loop to extract subBuffer starting from byte 0, byte 1, ...
			bytesInBuffer = len(buffer)
			for i in range(bytesInBuffer):

				# Initialize msgFound and msgLength
				msgFound = False
				msgLength = 0

				# Extract a copy of the buffer from byte i to subBuffer
				subBuffer = buffer[i:bytesInBuffer].copy()

				# Check if is a X10RF or DM10 message
				if (sensorType := isX10RF(subBuffer)) != RFXCOM_X10RF_MSG_UNKNOWN:
					msgFound = True
					msgLength = getX10rfMsgLength(subBuffer)
					sensorData = processX10rfMsg(subBuffer, sensorType)
				elif (sensorType := isDM10(subBuffer)) != RFXCOM_DM10_MSG_UNKNOWN:
					msgFound = True
					msgLength = getX10rfMsgLength(subBuffer)
					sensorData = processX10rfMsg(subBuffer, sensorType)

				# Check if is a SECURITY message
				elif (sensorType := isSecurity(subBuffer)) != RFXCOM_SECURITY_MSG_UNKNOWN:
					msgFound = True
					msgLength = getSecurityMsgLength(subBuffer)
					sensorData = processSecurityMsg(subBuffer, sensorType)
					
				# Check if is a OREGON message
				elif (sensorType := isOregon(subBuffer)) != RFXCOM_OREGON_MSG_UNKNOWN:
					msgFound = True
					msgLength = getOregonMsgLength(subBuffer)
					sensorData = processOregonMsg(subBuffer, sensorType)
					
				# Check if is a HOMEEASY message
				#elif isHomeEasy(rxBuffer):
				#	processHomeEasyMsg(rxBuffer)
					
				# Check if is a KOPPLA message
				#elif (isKoppla(rxBuffer)):
				#	processKopplaMsg(rxBuffer)
					
				# Check if is a RFXSENSOR message
				elif (sensorType := isRfxSensor(subBuffer)) != RFXCOM_RFXSENSOR_MSG_UNKNOWN:
					msgFound = True
					msgLength = getRfxSensorMsgLength(subBuffer)
					sensorData = processRfxsensorMsg(subBuffer, sensorType)

				# If message found remove the message and the precedent bytes from buffer
				if msgFound:
					buffer = buffer[i + msgLength:bytesInBuffer].copy()
					bufferChecking = True if len(buffer) > 0 else False
					if DEBUG:
						print(datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f") + " Message bytes:", subBuffer[:msgLength])
					publishToMqtt(sensorData)
					break
				else:
					if i == bytesInBuffer - 1:
						bufferChecking = False
		
		return buffer

	except Exception as e1:
		print("error communicating...: " + str(e1))
 
def publishToMqtt(sensorData):
	
	sensorType = sensorData[0]
	if sensorType == RFXCOM_SENSOR_SECURITY or sensorType == RFXCOM_SENSOR_OREGON or sensorType == RFXCOM_SENSOR_RFXCOM or sensorType == RFXCOM_SENSOR_X10:
		addr = sensorData[1]
		dataFields = sensorData[2]
		debugMsg = "SensorType: " + str(sensorType) + " Addr: " + addr + " Fields: " + str(dataFields) + " Data:"
		if addr != "" and dataFields > 0:
			for x in range(dataFields):
				unit = sensorData[3 + x][2]
				if unit != "":
					client.publish(MQTT_Topic + '/' + addr + '/' + sensorData[3 + x][0], '{"state":"'+ sensorData[3 + x][1] +'","unit_of_measurement":"' + unit + '"}', qos=MQTT_QoS, retain=MQTT_Retain)
					debugMsg = debugMsg + " " + str(sensorData[3 + x][1]) + unit
				else:
					client.publish(MQTT_Topic + '/' + addr + '/' + sensorData[3 + x][0], '{"state":"'+ sensorData[3 + x][1] +'"}', qos=MQTT_QoS, retain=MQTT_Retain)
					debugMsg = debugMsg + " " + str(sensorData[3 + x][1])

			if DEBUG:
				print(datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f") + " " + debugMsg)
				

### MAIN ### 
client = mqtt.Client("RFXCOM") # must be unique on MQTT network
client.username_pw_set(str(MQTT_User),str(MQTT_Password))
client.connect(MQTT_Host, port=int(MQTT_Port))
client.loop_start()
rfxcom_device = configure_rfxcom_port()
open_rfxcom_port(rfxcom_device)
rfxcomBuffer = list()
while(rfxcom_port_opened(rfxcom_device)):
	rfxcomBuffer = get_rfxcom_data(rfxcom_device, rfxcomBuffer)
close_rfxcom_port(rfxcom_device)
