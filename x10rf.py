# x10rf.py>

from common import *

# Message Types
RFXCOM_X10RF_MSG_UNKNOWN	= 0
RFXCOM_DM10_MSG_UNKNOWN		= 0
RFXCOM_X10RF_MSG		= 1
RFXCOM_DM10_MSG			= 2

# Function codes
X10RF_ALL_UNITS_OFF		= 0	# Not exists for X10RF protocol
X10RF_ALL_LIGHTS_ON		= 1
X10RF_ON			= 2
X10RF_OFF			= 3
X10RF_DIM			= 4
X10RF_BRIGHT			= 5
X10RF_ALL_LIGHTS_OFF		= 6	
#X10RF_EXTENDED_CODE		= 7	# Not exists for X10RF protocol
#X10RF_HAIL_REQUEST		= 8	# Not exists for X10RF protocol
#X10RF_HAIL_ACK			= 9	# Not exists for X10RF protocol
#X10RF_PRESET_DIM_1		= 10	# Not exists for X10RF protocol
#X10RF_PRESET_DIM_2		= 11	# Not exists for X10RF protocol
#X10RF_EXTENDED_DATA		= 12	# Not exists for X10RF protocol
#X10RF_STATUS_ON		= 13	# Not exists for X10RF protocol
#X10RF_STATUS_OFF		= 14	# Not exists for X10RF protocol
#X10RF_STATUS_REQUEST   	= 15	# Not exists for X10RF protocol

def isX10RF(msg):
	
	# Check 32 bit message length
	if ((msg[0] & 0x7F) == 0x20) and (len(msg) >= 5):
		# Check bytes
		if ((msg[1] + msg[2] == 0xFF) and (msg[3] + msg[4] == 0xFF)):
			return RFXCOM_X10RF_MSG
		
	return RFXCOM_X10RF_MSG_UNKNOWN

def isDM10(msg):
	
	# Check 32 bit message length
	if ((msg[0] & 0x7F) == 0x20) and (len(msg) >= 5):
		# Check bytes
		if (((msg[1] ^ msg[2]) == 0xFE) and ((msg[3] ^ msg[4]) == 0xFF)):
			return RFXCOM_DM10_MSG

	return RFXCOM_DM10_MSG_UNKNOWN

def getX10rfMsgLength(msg):
	
	return (msg[0] & 0x7F) // 8 + 1 if (msg[0] & 0x7F) % 8 == 0 else (msg[0] & 0x7F) // 8 + 2

def decode_X10RF(msg):

	global last_ucode
	hcode = ''
	ucode = 0
	func = 0

	# Extract HouseCode
	if (msg[1] & 0xF0) == 0x60:
		hcode = 'A'
	elif (msg[1] & 0xF0) == 0x70:
		hcode = 'B'
	elif (msg[1] & 0xF0) == 0x40:
		hcode = 'C'
	elif (msg[1] & 0xF0) == 0x50:
		hcode = 'D'
	elif (msg[1] & 0xF0) == 0x80:
		hcode = 'E'
	elif (msg[1] & 0xF0) == 0x90:
		hcode = 'F'
	elif (msg[1] & 0xF0) == 0xA0:
		hcode = 'G'
	elif (msg[1] & 0xF0) == 0xB0:
		hcode = 'H'
	elif (msg[1] & 0xF0) == 0xE0:
		hcode = 'I'
	elif (msg[1] & 0xF0) == 0xF0:
		hcode = 'J'
	elif (msg[1] & 0xF0) == 0xC0:
		hcode = 'K'
	elif (msg[1] & 0xF0) == 0xD0:
		hcode = 'L'
	elif (msg[1] & 0xF0) == 0x00:
		hcode = 'M'
	elif (msg[1] & 0xF0) == 0x10:
		hcode = 'N'
	elif (msg[1] & 0xF0) == 0x20:
		hcode = 'O'
	elif (msg[1] & 0xF0) == 0x30:
		hcode = 'P'

	# Extract UnitCode & Function
	if msg[3] == 0x80:
		func = X10RF_ALL_LIGHTS_OFF
	elif msg[3] == 0x90:
		func = X10RF_ALL_LIGHTS_ON
	elif msg[3] == 0x88:
		func = X10RF_BRIGHT
	elif msg[3] == 0x98:
		func = X10RF_DIM
	else:
		# Create unit code (format 0..15)
		if (msg[3] & 0x10) == 0:
			ucode = 0x00
		else:
			ucode = 0x01
		if (msg[3] & 0x08) != 0:
			ucode += 0x02
		if (msg[3] & 0x40) != 0:
			ucode += 0x04
		if (msg[1] & 0x04) != 0:
			ucode += 0x08
			
		# Convert unit code to format 1..16
		ucode += 1
			
		# Extract function for addressable commands
		if (msg[3] & 0x20) == 0:
			last_ucode = ucode
			func = X10RF_ON
		else:
			last_ucode = ucode
			func = X10RF_OFF
	
	# Build address
	if func == X10RF_BRIGHT or func == X10RF_DIM:
		addr = hcode + str(last_ucode)
	else:
		addr = hcode + str(ucode)
	
	return addr, func

def decode_DM10(msg):

	hcode = ((msg[1] & 0xF0) >> 4) + 65
	ucode = (msg[1] & 0x0F) + 1

	if msg[3] == 0xE0:	  # Motion detected
		func = X10RF_ON
	elif msg[3] == 0xF0:	# Dark detected
		func = X10RF_OFF
	elif msg[3] == 0xF8:	# Light detected
		func = X10RF_ON
	else:
		func = 0

	# Build address
	addr = str(chr(hcode)) + str(ucode)
	
	return addr, func

def processX10rfMsg(msg, msgType):

	# Initialize vars
	x10rfDeviceData = list()
	x10rfDeviceData.append(RFXCOM_SENSOR_X10)
	addr = []
		
	if msgType == RFXCOM_X10RF_MSG:
		addr, func = decode_X10RF(msg)
		x10rfDeviceData.append(addr)
		x10rfDeviceData.append(1)
		x10rfDeviceData.append(("Command", str(func), ""))
	
	elif msgType == RFXCOM_DM10_MSG:
		addr, func = decode_DM10(msg)
		x10rfDeviceData.append(addr)
		x10rfDeviceData.append(1)
		x10rfDeviceData.append(("Command", str(func), ""))

	else:
		x10rfDeviceData.append(addr)
		x10rfDeviceData.append(0)
	
	return x10rfDeviceData
