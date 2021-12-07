# rfxsensor.py>

from common import *

# Message Types
RFXCOM_RFXSENSOR_MSG_UNKNOWN	= 0
RFXCOM_RFXSENSOR_MSG_RFXSENSOR	= 1
RFXCOM_RFXSENSOR_MSG_RFXPOWER	= 2
RFXCOM_RFXSENSOR_MSG_SRFXPOWER	= 3

# Function Types
RFXCOM_RFXSENSOR_FUNC_UNKNOWN	= 0
RFXCOM_RFXSENSOR_FUNC_INFO		= 1
RFXCOM_RFXSENSOR_FUNC_ERROR		= 2
RFXCOM_RFXSENSOR_FUNC_TEMP		= 3
RFXCOM_RFXSENSOR_FUNC_ADC		= 4
RFXCOM_RFXSENSOR_FUNC_SVOLTAGE	= 5
RFXCOM_RFXSENSOR_FUNC_MULTI		= 6
RFXCOM_RFXSENSOR_FUNC_MULTI_AD	= 7

def crc8(msg):
		
	result = 0
	for intBytes in range(1, 5):
		temp2 = msg[intBytes]
		for intBits in range(0, 7):
			temp4 = (temp2 ^ result) & 0x01
			result = result >> 1
			if temp4 == 0x01:
				result = result ^ 0x8C
			temp2 = temp2 >> 1
	return result

def isRfxSensor(msg):

	# Check 32 bit for a Rfxsensor message
	if (msg[0] & 0x7F) == 32:
		parity = (((msg[1] >> 4) & 0x0F) + (msg[1] & 0x0F) + ((msg[2] >> 4) & 0x0F) + (msg[2] & 0x0F) +
			((msg[3] >> 4) & 0x0F) + (msg[3] & 0x0F) + ((msg[4] >> 4) & 0x0F)) & 0x0F
		if (parity == (msg[4] & 0x0F)) and (msg[1] + (msg[2] ^ 0x0F) == 0xFF):
			return RFXCOM_RFXSENSOR_MSG_RFXSENSOR

	# Check 48 bit for a RFXMeter or RFXPower or RFXSensorL message
	elif (msg[0] & 0x7F) == 48:
		if crc8(msg) == msg[6]:
			return RFXCOM_RFXSENSOR_MSG_RFXSENSOR

		elif msg[1] == (msg[2] ^ 0xF0):
			parity = (((msg[1] >> 4) & 0x0F) + (msg[1] & 0x0F) + ((msg[2] >> 4) & 0x0F) + (msg[2] & 0x0F) +
			    ((msg[3] >> 4) & 0x0F) + (msg[3] & 0x0F) + ((msg[4] >> 4) & 0x0F) + (msg[4] & 0x0F) +
			    ((msg[5] >> 4) & 0x0F) + (msg[5] & 0x0F) + ((msg[6] >> 4) & 0x0F)) & 0x0F
			if (parity == (msg[6] & 0x0F)) and (msg[1] + (msg[2] ^ 0x0F) == 0xFF):
				return RFXCOM_RFXSENSOR_MSG_RFXPOWER
			elif parity == (msg[6] & 0x0F):
				return RFXCOM_RFXSENSOR_MSG_SRFXPOWER

	return RFXCOM_RFXSENSOR_MSG_UNKNOWN

def getRfxSensorMsgLength(msg):
	
	return (msg[0] & 0x7F) // 8 + 1 if (msg[0] & 0x7F) % 8 == 0 else (msg[0] & 0x7F) // 8 + 2

def decode_rfxsensor(msg):
	
	# Init vars
	addr = ""
	func = 0
	value1 = 0.0
	value2 = 0.0
	value3 = 0.0
	
	# For 32 bit messages
	if (msg[0] & 0x7F) == 32:
		
		# Extract Address 
		addr0 = ((msg[1] >> 4) & 0x0F) + 48 if ((msg[1] >> 4) & 0x0F) < 10 else ((msg[1] >> 4) & 0x0F) + 55
		addr1 = (msg[1] & 0x0F) + 48 if (msg[1] & 0x0F) < 10 else (msg[1] & 0x0F) + 55
		addr2 = ((msg[2] >> 4) & 0x0F) + 48 if ((msg[2] >> 4) & 0x0F) < 10 else ((msg[2] >> 4) & 0x0F) + 55
		addr3 = (msg[2] & 0x0F) + 48 if (msg[2] & 0x0F) < 10 else (msg[2] & 0x0F) + 55
		addr = str(chr(addr0)) + str(chr(addr1)) + str(chr(addr2)) + str(chr(addr3))

		# Check for errors
		if (msg[4] & 0x10) != 0:
			
			if msg[3] == 0x01:	  # Info: address incremented
				func = RFXCOM_RFXSENSOR_FUNC_INFO
			elif msg[3] == 0x02:	# Info: battery low
				func = RFXCOM_RFXSENSOR_FUNC_INFO
			elif msg[3] == 0x03:	# Info: conversion not ready, 1 retry is done
				func = RFXCOM_RFXSENSOR_FUNC_INFO
			elif msg[3] == 0x81:	# Error: No 1-Wire device connected
				func = RFXCOM_RFXSENSOR_FUNC_ERROR
			elif msg[3] == 0x82:	# Error: 1-Wire ROM CRC error
				func = RFXCOM_RFXSENSOR_FUNC_ERROR
			elif msg[3] == 0x83:	# Error: 1-Wire device connected is not a DS1820
				func = RFXCOM_RFXSENSOR_FUNC_ERROR
			elif msg[3] == 0x84:	# Error: No end of read signal received from 1-Wire device
				func = RFXCOM_RFXSENSOR_FUNC_ERROR
			elif msg[3] ==  0x85:	# Error: 1-Wire device Scratchpad CRC error
				func = RFXCOM_RFXSENSOR_FUNC_ERROR
			elif msg[3] ==  0x86:	# Error: temperature conversion not ready in time
				func = RFXCOM_RFXSENSOR_FUNC_ERROR
			elif msg[3] ==  0x87:	# Error: A/D conversion not ready in time
				func = RFXCOM_RFXSENSOR_FUNC_ERROR
			else:					# Unknown Info/Error code!
				func = RFXCOM_RFXSENSOR_FUNC_UNKNOWN

		# If no errors, get sensor data
		else:
			
			if (msg[1] & 0x03) == 0:	# Temp sensor
				value1 = msg[3] + ((msg[4] >> 5) * 0.125)
				if value1 > 200:
					value1 = 0 - (256 - value1)
				func = RFXCOM_RFXSENSOR_FUNC_TEMP
			
			elif (msg[1] & 0x03) == 1:  # A/D converter
				value1 = ((msg[3] * 256) + msg[4]) >> 5
				value1 = value1 / 100.0
				func = RFXCOM_RFXSENSOR_FUNC_ADC

			elif (msg[1] & 0x03) == 2:  # Supply voltage
				value1 = ((msg[3] * 256) + msg[4]) >> 5
				value1 = value1 / 100.0
				func = RFXCOM_RFXSENSOR_FUNC_SVOLTAGE
			
			elif (msg[1] & 0x03) == 3:  # Other sensors
				#if ((msg[4] & 0x20) == 0) {
				#	WriteMessage("ZAP25:" & Convert.ToString(Math.Round((5 / 1024) * (recbuf(2) * 2 + (recbuf(3) >> 7)) / 0.033, 2) & "A"), False)
				#	WriteMessage(" ZAP50:" & Convert.ToString(Math.Round((5 / 1024) * (recbuf(2) * 2 + (recbuf(3) >> 7)) / 0.023, 2) & "A"), False)
				#	WriteMessage(" ZAP100:" & Convert.ToString(Math.Round((5 / 1024) * (recbuf(2) * 2 + (recbuf(3) >> 7)) / 0.019, 2) & "A"), False)
				#}
				#else {
				#	WriteMessage("Voltage=" & Convert.ToString(recbuf(2) * 2), False)
				#}
				value1 = 0
				func = RFXCOM_RFXSENSOR_FUNC_UNKNOWN
			
			else:
				value1 = 0
				func = RFXCOM_RFXSENSOR_FUNC_UNKNOWN

	# For bigger messages
	else:
		
		# Extract Address 
		addr0 = ((msg[1] >> 4) & 0x0F) + 48 if ((msg[1] >> 4) & 0x0F) < 10 else ((msg[1] >> 4) & 0x0F) + 55
		addr1 = (msg[1] & 0x0F) + 48 if (msg[1] & 0x0F) < 10 else (msg[1] & 0x0F) + 55
		addr = str(chr(addr0)) + str(chr(addr1))

		# Extract sensor data
		value1 = msg[2] + ((msg[3] >> 6) * 0.25)
		if value1 > 200:
			value1 = 0 - (256 - value1)
		func = RFXCOM_RFXSENSOR_FUNC_MULTI
		
		if (msg[3] & 0x20) == 0:	# no DS18B20 connected so A/D value
			value2 = ((msg[3] & 0x1F) * 32) + (msg[4] >> 3)
			value2 = value2 / 100.0
			func = RFXCOM_RFXSENSOR_FUNC_MULTI_AD

		else:					   # DS18B20 temperature sensor connected
			value2 = ((msg[3] & 0x1F) << 3) + ((msg[4] >> 3) * 0.25)
			if value2 > 200:
				value2 = 0 - (256 - value2)
		
		# Supply voltage
		value3 = ((msg[4] & 0x03) * 256) + msg[5]
		value3 = value3 / 100.0

	return addr, func, value1, value2, value3

def processRfxsensorMsg(msg, msgType):

	# Initialize vars
	rfxsensorSensorData = list()
	rfxsensorSensorData.append(RFXCOM_SENSOR_RFXCOM)
	addr = []
	msgfunc = 0
	value1 = 0.0
	value2 = 0.0
	value3 = 0.0

	if msgType == RFXCOM_RFXSENSOR_MSG_RFXSENSOR:
		
		# Decode the Rfxsensor message
		addr, msgfunc, value1, value2, value3 = decode_rfxsensor(msg)
		rfxsensorSensorData.append(addr)
		if msgfunc == RFXCOM_RFXSENSOR_FUNC_TEMP:
			rfxsensorSensorData.append(1)
			rfxsensorSensorData.append(("Temperature", str(round(value1, 1)), "°C"))
		
		elif msgfunc == RFXCOM_RFXSENSOR_FUNC_ADC:
			rfxsensorSensorData.append(1)
			rfxsensorSensorData.append(("ADC counts", str(round(value1, 0)), ""))

		elif msgfunc == RFXCOM_RFXSENSOR_FUNC_SVOLTAGE:
			rfxsensorSensorData.append(1)
			rfxsensorSensorData.append(("Supply voltage", str(round(value1, 1)), "V"))

		elif msgfunc == RFXCOM_RFXSENSOR_FUNC_MULTI:
			rfxsensorSensorData.append(3)
			rfxsensorSensorData.append(("Sensor data", str(round(value1, 1)), ""))
			rfxsensorSensorData.append(("Temperature", str(round(value2, 1)), "°C"))
			rfxsensorSensorData.append(("Supply voltage", str(round(value3, 1)), "V"))

		elif msgfunc == RFXCOM_RFXSENSOR_FUNC_MULTI_AD:
			rfxsensorSensorData.append(3)
			rfxsensorSensorData.append(("Sensor data", str(round(value1, 1)), ""))
			rfxsensorSensorData.append(("ADC counts", str(round(value2, 0)), ""))
			rfxsensorSensorData.append(("Supply voltage", str(round(value3, 1)), "V"))

	else:
		rfxsensorSensorData.append(addr)
		rfxsensorSensorData.append(0)
	
	return rfxsensorSensorData