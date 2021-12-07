# security.py>

from common import *

# Message Types
RFXCOM_SECURITY_MSG_UNKNOWN	 	= 0
RFXCOM_SECURITY_MSG_POWERCODE	= 1
RFXCOM_SECURITY_MSG_CODESECURE	= 2
RFXCOM_SECURITY_MSG_X10SEC		= 3
RFXCOM_SECURITY_JAMMING_DETECT	= 4
RFXCOM_SECURITY_JAMMING_END		= 5

# Message code format:
# Bit	7 6 5 4 3 2 1 0
#		| | | | | | | |______ 0: Battery OK		1: Battery low
#	  	| | | | | | |________ 0: Sensor			1: Keyfob
#		| | | | | |__________ 0: No Visonic		1: Visonic
#		| | | | |____________ 0: Door/Window	1: Motion
#		| | | |______________ 0: 				1: 
#		| | |________________ 0: 				1: 
#		| |__________________ 0: Tamper close	1: Tamper open
#		|____________________ 0: Alert			1: Normal


def even_parity(byte_to_check):
	
	sum_of_bits =  (byte_to_check & 0x80) >> 7
	sum_of_bits += (byte_to_check & 0x40) >> 6
	sum_of_bits += (byte_to_check & 0x20) >> 5
	sum_of_bits += (byte_to_check & 0x10) >> 4
	sum_of_bits += (byte_to_check & 0x08) >> 3
	sum_of_bits += (byte_to_check & 0x04) >> 2
	sum_of_bits += (byte_to_check & 0x02) >> 1
	sum_of_bits += (byte_to_check & 0x01)

	return (sum_of_bits & 0x01)

def secIsJammingDetect(msg):
	if ((msg[3] == 0xE0) and ((msg[1] == 0xFF) or (msg[1] == 0x00))):
		return True
	return False

def secIsJammingEnd(msg):
	if ((msg[3] == 0xF8) and ((msg[1] == 0xFF) or (msg[1] == 0x00))):
		return True
	return False

def isSecurity(msg):
	
	msgtype = RFXCOM_SECURITY_MSG_UNKNOWN

	# Check 41 bit message length for a Visonic PowerCode message
	if ((msg[0] & 0x7F) == 0x29):
		
		# Check bytes
		if (msg[3] + msg[4] == 0xFF) and (even_parity(msg[5]) == ((msg[6] & 0x80) >> 7)):
			
			# Check for jamming
			if secIsJammingDetect(msg):
				msgtype = RFXCOM_SECURITY_JAMMING_DETECT
			elif secIsJammingEnd(msg):
				msgtype = RFXCOM_SECURITY_JAMMING_END
			else:
				msgtype = RFXCOM_SECURITY_MSG_POWERCODE
	
	# Check XX bit message length for a Visonic CodeSecure message
	#else if ((msg[0] & 0x7F) == 0x??) {
	#	*msgtype = RFXCOM_SECURITY_MSG_CODESECURE;
	#}
	
	# Check if is a X10Security message
	elif (msg[1] == ((msg[2] & 0xF0) + (0xF - (msg[2] & 0xF)))) and ((msg[3] ^ msg[4]) == 0xFF):
		
		# Check for jamming
		if secIsJammingDetect(msg):
			msgtype = RFXCOM_SECURITY_JAMMING_DETECT
		elif secIsJammingEnd(msg):
			msgtype = RFXCOM_SECURITY_JAMMING_END
		else:
			msgtype = RFXCOM_SECURITY_MSG_X10SEC

	return msgtype

def getSecurityMsgLength(msg):
	
	return (msg[0] & 0x7F) // 8 + 1 if (msg[0] & 0x7F) % 8 == 0 else (msg[0] & 0x7F) // 8 + 2

def decode_powercode(msg):
	
	# Extract Address
	addr0 = ((msg[1] & 0xF0) >> 4) + 48 if ((msg[1] & 0xF0) >> 4) < 10 else ((msg[1] & 0xF0) >> 4) + 55
	addr1 = (msg[1] & 0x0F) + 48 if (msg[1] & 0x0F) < 10 else (msg[1] & 0x0F) + 55
	addr2 = ((msg[2] & 0xF0) >> 4) + 48 if ((msg[2] & 0xF0) >> 4) < 10 else ((msg[2] & 0xF0) >> 4) + 55
	addr3 = (msg[2] & 0x0F) + 48 if (msg[2] & 0x0F) < 10 else (msg[2] & 0x0F) + 55
	addr4 = ((msg[5] & 0xF0) >> 4) + 48 if ((msg[5] & 0xF0) >> 4) < 10 else ((msg[5] & 0xF0) >> 4) + 55
	addr5 = (msg[5] & 0x0F) + 48 if (msg[5] & 0x0F) < 10 else (msg[5] & 0x0F) + 55
	addr = str(chr(addr0)) + str(chr(addr1)) + str(chr(addr2)) + str(chr(addr3)) + str(chr(addr4)) + str(chr(addr5))
	
	# Extract msgcode
	msgcode = msg[3]
	
	return addr, msgcode

def decode_X10Sec(msg):
	return decode_powercode(msg)

def motionSensorType(msgcode):

	if msgcode & 0x08:
		return True
	return False

def batteryStatusAvailable(msgcode):

	if ((msgcode & 0x02) == 0x0):
		return True
	return False

def batteryLow(msgcode):

	if ((msgcode & 0x03) == 0x01):
		return True
	return False

def sensorAlerted(msgcode):
	
	if ((msgcode & 0x82) == 0x00) or (msgcode == 0x20):
		return True
	return False

def tamperOpened(msgcode):

	if (msgcode & 0x42) == 0x40:
		return True
	return False

def processSecurityMsg(msg, msgType):

	# Initialize vars
	securitySensorData = list()
	securitySensorData.append(RFXCOM_SENSOR_SECURITY)
	addr = []
		
	if (msgType == RFXCOM_SECURITY_MSG_POWERCODE) or (msgType == RFXCOM_SECURITY_MSG_X10SEC):
		
		if msgType == RFXCOM_SECURITY_MSG_POWERCODE:	# Decode the PowerCode message
			addr, msgcode = decode_powercode(msg)
		elif msgType == RFXCOM_SECURITY_MSG_X10SEC:	 	# Decode the X10 Security message
			addr, msgcode = decode_X10Sec(msg)
		securitySensorData.append(addr)
		if batteryStatusAvailable(msgcode):
			securitySensorData.append(4)
			securitySensorData.append(("BatteryLow", str(1 if batteryLow(msgcode) else 0), ""))
		else:
			securitySensorData.append(3)
		securitySensorData.append(("SensorType", "Motion" if motionSensorType(msgcode) else "Door/Window", ""))
		securitySensorData.append(("State", str(1 if sensorAlerted(msgcode) else 0), ""))
		securitySensorData.append(("Tampered", str(1 if tamperOpened(msgcode) else 0), ""))
			
	#elif msgType == RFXCOM_SECURITY_MSG_CODESECURE:

	#elif msgType == RFXCOM_SECURITY_JAMMING_DETECT:
		
	#elif msgType == RFXCOM_SECURITY_JAMMING_END:

	else:
		securitySensorData.append(addr)
		securitySensorData.append(0)
	
	return securitySensorData