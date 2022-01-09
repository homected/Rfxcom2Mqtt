# oregon.py>

from common import *

# Message Types
RFXCOM_OREGON_MSG_UNKNOWN   	= 0
RFXCOM_OREGON_MSG_TEMP1	 	= 1
RFXCOM_OREGON_MSG_TEMP2		= 2
RFXCOM_OREGON_MSG_TEMP3		= 3
RFXCOM_OREGON_MSG_TEMP4		= 4
RFXCOM_OREGON_MSG_TH1		= 5
RFXCOM_OREGON_MSG_TH2		= 6
RFXCOM_OREGON_MSG_TH3		= 7
RFXCOM_OREGON_MSG_TH4		= 8
RFXCOM_OREGON_MSG_TH5		= 9
RFXCOM_OREGON_MSG_TH6		= 10
RFXCOM_OREGON_MSG_THB1		= 11
RFXCOM_OREGON_MSG_THB2		= 12
RFXCOM_OREGON_MSG_RAIN1		= 13
RFXCOM_OREGON_MSG_RAIN2		= 14
RFXCOM_OREGON_MSG_RAIN3		= 15
RFXCOM_OREGON_MSG_WIND1		= 16
RFXCOM_OREGON_MSG_WIND2		= 17
RFXCOM_OREGON_MSG_WIND3		= 18
RFXCOM_OREGON_MSG_UV1		= 19
RFXCOM_OREGON_MSG_UV2		= 20
RFXCOM_OREGON_MSG_DT1		= 21
RFXCOM_OREGON_MSG_WEIGHT1	= 22
RFXCOM_OREGON_MSG_WEIGHT2	= 23
RFXCOM_OREGON_MSG_ELEC1		= 24
RFXCOM_OREGON_MSG_ELEC2		= 25

# Baterry status
RFXCOM_OREGON_BAT_UNKNOWN	= 255
RFXCOM_OREGON_BAT_OK		= 254
RFXCOM_OREGON_BAT_LOW		= 253

def wrchannel(value):
	
	if (value & 0x70) == 0x10:
		ch = 1
	elif (value & 0x70) == 0x20:
		ch = 2
	elif (value & 0x70) == 0x40:
		ch = 3
	else:
		ch = 0

	return ch

def wrchannel3(value): 

	return(value >> 4)

def get_address(msg, msgType, ch):

	# Extract Address TTAAAAC (Type + Address + Channel)
	addr0 = ((msgType >> 4) & 0x0F) + 48 if ((msgType >> 4) & 0x0F) < 10 else ((msgType >> 4) & 0x0F) + 55
	addr1 = (msgType & 0x0F) + 48 if (msgType & 0x0F) < 10 else (msgType & 0x0F) + 55
	addr2 = 48
	addr3 = 48
	addr4 = ((msg[4] >> 4) & 0x0F) + 48 if ((msg[4] >> 4) & 0x0F) < 10 else ((msg[4] >> 4) & 0x0F) + 55
	addr5 = (msg[4] & 0x0F) + 48 if (msg[4] & 0x0F) < 10 else (msg[4] & 0x0F) + 55
	addr6 = ch + 48
	return str(chr(addr0)) + str(chr(addr1)) + str(chr(addr2)) + str(chr(addr3)) + str(chr(addr4)) + str(chr(addr5)) + str(chr(addr6))

def get_address2(msg, msgType):

	# Extract Address TTAAAAC (Type + Address + Channel)
	addr0 = ((msgType >> 4) & 0x0F) + 48 if ((msgType >> 4) & 0x0F) < 10 else ((msgType >> 4) & 0x0F) + 55
	addr1 = (msgType & 0x0F) + 48 if (msgType & 0x0F) < 10 else (msgType & 0x0F) + 55
	addr2 = 48
	addr3 = 48
	addr4 = 48
	addr5 = ((msg[2] >> 4) & 0x0F) + 48 if ((msg[2] >> 4) & 0x0F) < 10 else ((msg[2] >> 4) & 0x0F) + 55
	addr6 = 48
	return str(chr(addr0)) + str(chr(addr1)) + str(chr(addr2)) + str(chr(addr3)) + str(chr(addr4)) + str(chr(addr5)) + str(chr(addr6))

def get_address3(msg, msgType):

	# Extract Address TTAAAAC (Type + Address + Counter)
	if msgType == RFXCOM_OREGON_MSG_ELEC1:
		addr0 = ((msgType >> 4) & 0x0F) + 48 if ((msgType >> 4) & 0x0F) < 10 else ((msgType >> 4) & 0x0F) + 55
		addr1 = (msgType & 0x0F) + 48 if (msgType & 0x0F) < 10 else (msgType & 0x0F) + 55
		addr2 = 48
		addr3 = 48
		addr4 = ((msg[3] >> 4) & 0x0F) + 48 if ((msg[3] >> 4) & 0x0F) < 10 else ((msg[3] >> 4) & 0x0F) + 55
		addr5 = (msg[3] & 0x0F) + 48 if (msg[3] & 0x0F) < 10 else (msg[3] & 0x0F) + 55
		addr6 = (msg[2] & 0x0F) + 48
	elif msgType ==	RFXCOM_OREGON_MSG_ELEC2:
		addr0 = ((msgType >> 4) & 0x0F) + 48 if ((msgType >> 4) & 0x0F) < 10 else ((msgType >> 4) & 0x0F) + 55
		addr1 = (msgType & 0x0F) + 48 if (msgType & 0x0F) < 10 else (msgType & 0x0F) + 55
		addr2 = (msg[4] & 0x0F) + 48 if (msg[4] & 0x0F) < 10 else (msg[4] & 0x0F) + 55
		addr3 = ((msg[3] >> 4) & 0x0F) + 48 if ((msg[3] >> 4) & 0x0F) < 10 else ((msg[3] >> 4) & 0x0F) + 55
		addr4 = (msg[3] & 0x0F) + 48 if (msg[3] & 0x0F) < 10 else (msg[3] & 0x0F) + 55
		addr5 = ((msg[1] >> 4) & 0x03) + 48 if ((msg[1] >> 4) & 0x03) < 10 else ((msg[1] >> 4) & 0x03) + 55
		addr6 = (msg[2] & 0x0F) + 48
	addr = str(chr(addr0)) + str(chr(addr1)) + str(chr(addr2)) + str(chr(addr3)) + str(chr(addr4)) + str(chr(addr5)) + str(chr(addr6))

def checksum2(msg):
	
	cs = 0
	cs += (msg[1] >> 4) & 0x0F
	cs += ((msg[2] >> 4) & 0x0F) + (msg[2] & 0x0F)
	cs += ((msg[3] >> 4) & 0x0F) + (msg[3] & 0x0F)
	cs += ((msg[4] >> 4) & 0x0F) + (msg[4] & 0x0F)
	cs += ((msg[5] >> 4) & 0x0F) + (msg[5] & 0x0F)
	cs += ((msg[6] >> 4) & 0x0F) + (msg[6] & 0x0F)
	cs += ((msg[7] >> 4) & 0x0F) + (msg[7] & 0x0F)
	cs += ((msg[8] >> 4) & 0x0F) + (msg[8] & 0x0F)
	cs += (msg[9] & 0x0F)
	cs = (cs - (((msg[9] >> 4) & 0x0F) + ((msg[10] << 4) & 0xF0))) & 0xFF
	if (cs != 0):
		return False
	return True

def checksum7(msg):
	
	cs = 0
	cs += (msg[1] >> 4) & 0x0F
	cs += ((msg[2] >> 4) & 0x0F) + (msg[2] & 0x0F)
	cs += ((msg[3] >> 4) & 0x0F) + (msg[3] & 0x0F)
	cs += ((msg[4] >> 4) & 0x0F) + (msg[4] & 0x0F)
	cs += ((msg[5] >> 4) & 0x0F) + (msg[5] & 0x0F)
	cs += ((msg[6] >> 4) & 0x0F) + (msg[6] & 0x0F)
	cs += ((msg[7] >> 4) & 0x0F) + (msg[7] & 0x0F)
	cs = (cs - msg[8]) & 0xFF
	if (cs != 0):
		return False
	return True

def checksum8(msg):

	cs = 0
	cs += (msg[1] >> 4) & 0x0F
	cs += ((msg[2] >> 4) & 0x0F) + (msg[2] & 0x0F)
	cs += ((msg[3] >> 4) & 0x0F) + (msg[3] & 0x0F)
	cs += ((msg[4] >> 4) & 0x0F) + (msg[4] & 0x0F)
	cs += ((msg[5] >> 4) & 0x0F) + (msg[5] & 0x0F)
	cs += ((msg[6] >> 4) & 0x0F) + (msg[6] & 0x0F)
	cs += ((msg[7] >> 4) & 0x0F) + (msg[7] & 0x0F)
	cs += ((msg[8] >> 4) & 0x0F) + (msg[8] & 0x0F)
	cs = (cs - msg[9]) & 0xFF
	if (cs != 0):
		return False
	return True

def checksum9(msg):
	
	cs = 0
	cs += (msg[1] >> 4) & 0x0F
	cs += ((msg[2] >> 4) & 0x0F) + (msg[2] & 0x0F)
	cs += ((msg[3] >> 4) & 0x0F) + (msg[3] & 0x0F)
	cs += ((msg[4] >> 4) & 0x0F) + (msg[4] & 0x0F)
	cs += ((msg[5] >> 4) & 0x0F) + (msg[5] & 0x0F)
	cs += ((msg[6] >> 4) & 0x0F) + (msg[6] & 0x0F)
	cs += ((msg[7] >> 4) & 0x0F) + (msg[7] & 0x0F)
	cs += ((msg[8] >> 4) & 0x0F) + (msg[8] & 0x0F)
	cs += ((msg[9] >> 4) & 0x0F) + (msg[9] & 0x0F)
	cs = (cs - msg[10]) & 0xFF
	if (cs != 0):
		return False
	return True

def checksum10(msg):
	
	cs = 0
	cs += (msg[1] >> 4) & 0x0F
	cs += ((msg[2] >> 4) & 0x0F) + (msg[2] & 0x0F)
	cs += ((msg[3] >> 4) & 0x0F) + (msg[3] & 0x0F)
	cs += ((msg[4] >> 4) & 0x0F) + (msg[4] & 0x0F)
	cs += ((msg[5] >> 4) & 0x0F) + (msg[5] & 0x0F)
	cs += ((msg[6] >> 4) & 0x0F) + (msg[6] & 0x0F)
	cs += ((msg[7] >> 4) & 0x0F) + (msg[7] & 0x0F)
	cs += ((msg[8] >> 4) & 0x0F) + (msg[8] & 0x0F)
	cs += ((msg[9] >> 4) & 0x0F) + (msg[9] & 0x0F)
	cs += ((msg[10] >> 4) & 0x0F) + (msg[10] & 0x0F)
	cs = (cs - msg[11]) & 0xFF
	if (cs != 0):
		return False
	return True

def checksum11(msg):
	
	cs = 0
	cs += (msg[1] >> 4) & 0x0F
	cs += ((msg[2] >> 4) & 0x0F) + (msg[2] & 0x0F)
	cs += ((msg[3] >> 4) & 0x0F) + (msg[3] & 0x0F)
	cs += ((msg[4] >> 4) & 0x0F) + (msg[4] & 0x0F)
	cs += ((msg[5] >> 4) & 0x0F) + (msg[5] & 0x0F)
	cs += ((msg[6] >> 4) & 0x0F) + (msg[6] & 0x0F)
	cs += ((msg[7] >> 4) & 0x0F) + (msg[7] & 0x0F)
	cs += ((msg[8] >> 4) & 0x0F) + (msg[8] & 0x0F)
	cs += ((msg[9] >> 4) & 0x0F) + (msg[9] & 0x0F)
	cs += ((msg[10] >> 4) & 0x0F) + (msg[10] & 0x0F)
	cs += ((msg[11] >> 4) & 0x0F) + (msg[11] & 0x0F)
	cs = (cs - msg[12]) & 0xFF
	if (cs != 0):
		return False
	return True

def checksum12(msg):
	
	cs = 0
	cs += ((msg[2] >> 4) & 0x0F) + (msg[2] & 0x0F)
	cs += ((msg[3] >> 4) & 0x0F) + (msg[3] & 0x0F)
	cs += ((msg[4] >> 4) & 0x0F) + (msg[4] & 0x0F)
	cs += ((msg[5] >> 4) & 0x0F) + (msg[5] & 0x0F)
	cs += ((msg[6] >> 4) & 0x0F) + (msg[6] & 0x0F)
	cs += ((msg[7] >> 4) & 0x0F) + (msg[7] & 0x0F)
	cs += ((msg[8] >> 4) & 0x0F) + (msg[8] & 0x0F)
	cs += ((msg[9] >> 4) & 0x0F) + (msg[9] & 0x0F)
	cs += ((msg[10] >> 4) & 0x0F) + (msg[10] & 0x0F)
	cs += ((msg[11] >> 4) & 0x0F) + (msg[11] & 0x0F)
	cs += (msg[12] & 0x0F)
	cs = (cs - ((msg[13] & 0x0F) << 4) - ((msg[12] >> 4) & 0x0F)) & 0xFF
	if (cs != 0):
		return False
	return True

def checksume(msg):
	
	cs = 0
	cs += ((msg[1] >> 4) & 0x0F) + (msg[1] & 0x0F)
	cs += ((msg[2] >> 4) & 0x0F) + (msg[2] & 0x0F)
	cs += ((msg[3] >> 4) & 0x0F) + (msg[3] & 0x0F)
	cs += ((msg[4] >> 4) & 0x0F) + (msg[4] & 0x0F)
	cs += ((msg[5] >> 4) & 0x0F) + (msg[5] & 0x0F)
	cs += ((msg[6] >> 4) & 0x0F) + (msg[6] & 0x0F)
	cs += ((msg[7] >> 4) & 0x0F) + (msg[7] & 0x0F)
	cs = (cs - msg[8]) & 0xFF
	if (cs != 0x18):
		return False
	return True

def checksumr(msg):
	
	cs = 0
	cs += (msg[1] >> 4) & 0x0F
	cs += ((msg[2] >> 4) & 0x0F) + (msg[2] & 0x0F)
	cs += ((msg[3] >> 4) & 0x0F) + (msg[3] & 0x0F)
	cs += ((msg[4] >> 4) & 0x0F) + (msg[4] & 0x0F)
	cs += ((msg[5] >> 4) & 0x0F) + (msg[5] & 0x0F)
	cs += ((msg[6] >> 4) & 0x0F) + (msg[6] & 0x0F)
	cs += ((msg[7] >> 4) & 0x0F) + (msg[7] & 0x0F)
	cs += ((msg[8] >> 4) & 0x0F) + (msg[8] & 0x0F)
	cs += ((msg[9] >> 4) & 0x0F) + (msg[9] & 0x0F)
	cs += (msg[10] & 0x0F)
	cs = (cs - (((msg[11] << 4) & 0xF0) + ((msg[10] >> 4) & 0x0F))) & 0xFF
	if (cs != 0):
		return False
	return True

def checksumw(msg):
	
	cs = 0
	cs += ((msg[1] >> 4) & 0x0F)
	cs += ((msg[2] >> 4) & 0x0F) + (msg[2] & 0x0F)
	cs += ((msg[3] >> 4) & 0x0F) + (msg[3] & 0x0F)
	cs += ((msg[4] >> 4) & 0x0F) + (msg[4] & 0x0F)
	cs += ((msg[5] >> 4) & 0x0F) + (msg[5] & 0x0F)
	cs += ((msg[6] >> 4) & 0x0F) + (msg[6] & 0x0F)
	cs += (msg[7] & 0x0F)
	cs = (cs - (((msg[8] << 4) & 0xF0) + ((msg[7] >> 4) & 0x0F))) & 0xFF
	if (cs != 0):
		return False
	return True

def wbattery_indication(value):

	if (value & 0x04) == 0:
		return RFXCOM_OREGON_BAT_OK
	else:
		return RFXCOM_OREGON_BAT_LOW

def wrbattery(value):

	return 100 - ((value & 0x0F) * 10)

def isOregon(msg):
	
	# Check 56 bit or >59 bit message length for a Oregon message
	if (((msg[0] & 0x7F) == 56) or ((msg[0] & 0x7F) > 59)):
		# Check for TEMP1 sensor type
		if ((msg[1] == 0x0A) and (msg[2] == 0x4D) and ((msg[0] & 0x7F) >= 72)):
			return RFXCOM_OREGON_MSG_TEMP1

		# Check for TEMP2 sensor type
		elif ((msg[1] == 0xEA) and (msg[2] == 0x4C) and ((msg[0] & 0x7F) >= 60)):
			return RFXCOM_OREGON_MSG_TEMP2

		# Check for TEMP3 sensor type
		elif ((msg[1] == 0xCA) and (msg[2] == 0x48) and ((msg[0] & 0x7F) >= 60)):
			return RFXCOM_OREGON_MSG_TEMP3

		# Check for TEMP4 sensor type
		elif (((msg[1] & 0x0F) == 0x0A) and (msg[2] == 0xDC) and ((msg[0] & 0x7F) >= 64)):
			return RFXCOM_OREGON_MSG_TEMP4

		# Check for TH1 sensor type
		elif ((msg[1] == 0x1A) and (msg[2] == 0x2D) and ((msg[0] & 0x7F) >= 72)):
			return RFXCOM_OREGON_MSG_TH1

		# Check for TH2 sensor type
		elif ((msg[1] == 0xFA) and (msg[2] == 0x28) and ((msg[0] & 0x7F) >= 72)):
			return RFXCOM_OREGON_MSG_TH2

		# Check for TH3 sensor type
		elif (((msg[1] & 0x0F) == 0x0A) and (msg[2] == 0xCC) and ((msg[0] & 0x7F) >= 72)):
			return RFXCOM_OREGON_MSG_TH3

		# Check for TH4 sensor type
		elif ((msg[1] == 0xCA) and (msg[2] == 0x2C) and ((msg[0] & 0x7F) >= 72)):
			return RFXCOM_OREGON_MSG_TH4

		# Check for TH5 sensor type
		elif ((msg[1] == 0xFA) and (msg[2] == 0xB8) and ((msg[0] & 0x7F) >= 72)):
			return RFXCOM_OREGON_MSG_TH5
		
		# Check for TH6 sensor type
		elif ((msg[1] == 0x1A) and (msg[2] == 0x3D) and ((msg[0] & 0x7F) >= 72)):
			return RFXCOM_OREGON_MSG_TH6

		# Check for THB1 sensor type
		elif ((msg[1] == 0x5A) and (msg[2] == 0x5D) and ((msg[0] & 0x7F) >= 88)):
			return RFXCOM_OREGON_MSG_THB1

		# Check for THB2 sensor type
		elif ((msg[1] == 0x5A) and (msg[2] == 0x6D) and ((msg[0] & 0x7F) >= 88)):
			return RFXCOM_OREGON_MSG_THB2

		# Check for RAIN1 sensor type
		elif ((msg[1] == 0x2A) and (msg[2] == 0x1D) and ((msg[0] & 0x7F) >= 80)):
			return RFXCOM_OREGON_MSG_RAIN1

		# Check for RAIN2 sensor type
		elif ((msg[1] == 0x2A) and (msg[2] == 0x19) and ((msg[0] & 0x7F) >= 84)):
			return RFXCOM_OREGON_MSG_RAIN2

		# Check for RAIN3 sensor type
		elif ((msg[1] == 0x06) and (msg[2] == 0xE4) and ((msg[0] & 0x7F) >= 84)):
			return RFXCOM_OREGON_MSG_RAIN3

		# Check for WIND1 sensor type
		elif ((msg[1] == 0x1A) and (msg[2] == 0x99) and ((msg[0] & 0x7F) >= 80)):
			return RFXCOM_OREGON_MSG_WIND1

		# Check for WIND2 sensor type
		elif ((msg[1] == 0x1A) and (msg[2] == 0x89) and ((msg[0] & 0x7F) >= 80)):
			return RFXCOM_OREGON_MSG_WIND2

		# Check for WIND3 sensor type
		elif ((msg[1] == 0x3A) and (msg[2] == 0x0D) and ((msg[0] & 0x7F) >= 80)):
			return RFXCOM_OREGON_MSG_WIND3

		# Check for UV1 sensor type
		elif ((msg[1] == 0xEA) and (msg[2] == 0x7C) and ((msg[0] & 0x7F) >= 60)):
			return RFXCOM_OREGON_MSG_UV1

		# Check for UV2 sensor type
		elif ((msg[1] == 0xDA) and (msg[2] == 0x78) and ((msg[0] & 0x7F) >= 64)):
			return RFXCOM_OREGON_MSG_UV2

		# Check for DT1 sensor type
		elif (((msg[1] & 0x0F) == 0x0A) and (msg[2] == 0xEC) and ((msg[0] & 0x7F) >= 96)):
			return RFXCOM_OREGON_MSG_DT1

		# Check for WEIGHT1 sensor type
		elif ((msg[0] & 0x7F) == 56):
			return RFXCOM_OREGON_MSG_WEIGHT1

		# Check for WEIGHT2 sensor type
		elif (((msg[1] & 0x0F) == 0x03) and ((msg[0] & 0x7F) == 64)):
			return RFXCOM_OREGON_MSG_WEIGHT2

		# Check for ELEC1 sensor type
		elif ((msg[1] == 0xEA) and ((msg[2] & 0xC0) == 0x00) and ((msg[0] & 0x7F) >= 64)):
			return RFXCOM_OREGON_MSG_ELEC1

		# Check for ELEC2 sensor type
		elif (((msg[1] == 0x1A) or (msg[1] == 0x2A) or (msg[1] == 0x3A)) and ((msg[0] & 0x7F) == 108)):
			return RFXCOM_OREGON_MSG_ELEC2
		
		# Return sensor type unknown
		else:
			return RFXCOM_OREGON_MSG_UNKNOWN
		
	else:
		return RFXCOM_OREGON_MSG_UNKNOWN

def getOregonMsgLength(msg):
	
	return (msg[0] & 0x7F) // 8 + 1 if (msg[0] & 0x7F) % 8 == 0 else (msg[0] & 0x7F) // 8 + 2

def decode_oregon_temp(msg, msgType):
	
	# Extract channel
	if msgType == RFXCOM_OREGON_MSG_TEMP1 or msgType == RFXCOM_OREGON_MSG_TEMP2 or msgType == RFXCOM_OREGON_MSG_TEMP3:
		ch = wrchannel(msg[3])
	elif msgType == RFXCOM_OREGON_MSG_TEMP4:			
		ch = wrchannel3(msg[3])
	else:
		ch = 0			
	
	# Extract Address TTAAAAC (Type + Address + Channel)
	addr = get_address(msg, msgType, ch)
	
	# Extract temp
	if msgType == RFXCOM_OREGON_MSG_TEMP1:
		if (((msg[6] & 0xF0) < 0xA0) and ((msg[6] & 0x0F) < 0x0A) and ((msg[5] & 0xF0) < 0xA0)):
			if ((msg[7] & 0x08) == 0):
				temp = (((msg[6] & 0xF0) >> 4) * 10) + (msg[6] & 0x0F) + (((msg[5] & 0xF0) >> 4) / 10.0)
			else:
				temp = 0 - ((((msg[6] & 0xF0) >> 4) * 10) + (msg[6] & 0x0F) + (((msg[5] & 0xF0) >> 4) / 10.0))
		else:
			temp = 0

	elif msgType == RFXCOM_OREGON_MSG_TEMP2:
		if ((msg[7] & 0x08) == 0):
			temp = ((msg[7] & 0x03) * 100) + (((msg[6] & 0xF0) >> 4) * 10) + (msg[6] & 0x0F) + (((msg[5] & 0xF0) >> 4) / 10.0)
		else:
			temp = 0 - (((msg[7] & 0x03) * 100) + (((msg[6] & 0xF0) >> 4) * 10) + (msg[6] & 0x0F) + (((msg[5] & 0xF0) >> 4) / 10.0))

	elif msgType == RFXCOM_OREGON_MSG_TEMP3 or msgType == RFXCOM_OREGON_MSG_TEMP4:
		if ((msg[7] & 0x08) == 0):
			temp = (((msg[6] & 0xF0) >> 4) * 10) + (msg[6] & 0x0F) + (((msg[5] & 0xF0) >> 4) / 10.0)
		else:
			temp = 0 - ((((msg[6] & 0xF0) >> 4) * 10) + (msg[6] & 0x0F) + (((msg[5] & 0xF0) >> 4) / 10.0))

	else:
		temp = 0
		
	# Extract battery indication
	bat = wbattery_indication(msg[5])
	
	# Check for checksum
	if checksum8(msg):
		return addr, temp, bat
	else:
		return "", 0, 0

def decode_oregon_th(msg, msgType):
	
	# Extract channel
	if msgType == RFXCOM_OREGON_MSG_TH1 or msgType == RFXCOM_OREGON_MSG_TH4 or msgType == RFXCOM_OREGON_MSG_TH6:
		ch = wrchannel(msg[3])
	elif msgType == RFXCOM_OREGON_MSG_TH2 or msgType == RFXCOM_OREGON_MSG_TH3:
		ch = wrchannel3(msg[3])
	else:
		ch = 0
	
	# Extract Address TTAAAAC (Type + Address + Channel)
	addr = get_address(msg, msgType, ch)

	# Extract temp
	if (msg[7] & 0x08) == 0:
		temp = (((msg[6] & 0xF0) >> 4) * 10) + (msg[6] & 0x0F) + (((msg[5] & 0xF0) >> 4) / 10.0)
	else:
		temp = 0 - ((((msg[6] & 0xF0) >> 4) * 10) + (msg[6] & 0x0F) + (((msg[5] & 0xF0) >> 4) / 10.0))

	# Extract humidityidity
	humidity = ((msg[8] & 0x0F) * 10) + ((msg[7] >> 4) & 0x0F)
			
	# Extract battery indication
	if (msgType == RFXCOM_OREGON_MSG_TH1 or msgType == RFXCOM_OREGON_MSG_TH2 or msgType == RFXCOM_OREGON_MSG_TH3 
		or msgType == RFXCOM_OREGON_MSG_TH4 or msgType == RFXCOM_OREGON_MSG_TH5):
		bat = wbattery_indication(msg[5])
	elif msgType == RFXCOM_OREGON_MSG_TH6:
		bat = wrbattery(msg[5])
	else:
		bat = 0
	
	# Check for checksum
	if checksum8(msg):
		return addr, temp, humidity, bat
	else:
		return "", 0, 0, 0

def decode_oregon_thb(msg, msgType):
	
	# Extract channel
	if msgType == RFXCOM_OREGON_MSG_THB1 or msgType == RFXCOM_OREGON_MSG_THB2:
		ch = wrchannel(msg[3])
	else:
		ch = 0
	
	# Extract Address TTAAAAC (Type + Address + Channel)
	addr = get_address(msg, msgType, ch)

	# Extract temp
	if ((msg[7] & 0x08) == 0):
		temp = (((msg[6] & 0xF0) >> 4) * 10) + (msg[6] & 0x0F) + (((msg[5] & 0xF0) >> 4) / 10.0)
	else:
		temp = 0 - ((((msg[6] & 0xF0) >> 4) * 10) + (msg[6] & 0x0F) + (((msg[5] & 0xF0) >> 4) / 10.0))

	# Extract humidityidity
	humidity = ((msg[8] & 0x0F) * 10) + ((msg[7] >> 4) & 0x0F)
	 
	# Extract pressure (hPA)
	if msgType == RFXCOM_OREGON_MSG_THB1:
		baro = msg[9] + 795
	elif msgType == RFXCOM_OREGON_MSG_THB2:
		baro = msg[9] + 856
	else:			
		baro = 0
			
	# Extract battery indication
	bat = wbattery_indication(msg[5])
	
	# Check for checksum
	if checksum10(msg):
		return addr, temp, humidity, baro, bat
	else:
		return "", 0, 0, 0, 0

def decode_oregon_rain(msg, msgType):

	# Extract Address TTAAAAC (Type + Address + Channel)
	addr = get_address(msg, msgType, 0)

	# Extract rain fall rate (mm/hr) and total rain count (mm)
	if msgType == RFXCOM_OREGON_MSG_RAIN1:
		rrate = (((msg[6] >> 4) & 0x0F) * 100) + ((msg[6] & 0x0F) * 10) + ((msg[5] >> 4) & 0x0F)
		rtotal = ((msg[9] & 0x0F) * 1000) + (((msg[8] >> 4) & 0x0F) * 100) + ((msg[8] & 0x0F) * 10) + ((msg[7] >> 4) & 0x0F)
			
	elif msgType == RFXCOM_OREGON_MSG_RAIN2 or msgType == RFXCOM_OREGON_MSG_RAIN3:
		rrate = (((msg[6] >> 4) & 0x0F) + ((msg[6] & 0x0F) / 10.0) + (((msg[5] >> 4) & 0x0F) / 100.0) + ((msg[7] & 0x0F) / 1000.0)) * 25.4
		rtotal = ((msg[10] & 0x0F) * 100) + (((msg[9] >> 4) & 0x0F) * 10) + (msg[9] & 0x0F)
		rtotal += (((msg[8] >> 4) & 0x0F) / 10.0) + ((msg[8] & 0x0F) / 100.0) + (((msg[7] >> 4) & 0x0F)/ 1000.0)
		rtotal *= 25.4
	else:
		rrate = 0
		rtotal = 0

	# Extract battery indication
	bat = wbattery_indication(msg[5])
	
	# Check for checksum
	if msgType == RFXCOM_OREGON_MSG_RAIN1:

		if checksum2(msg):
			return addr, rrate, rtotal, bat
		else:
			return "", 0, 0, 0
			
	elif msgType == RFXCOM_OREGON_MSG_RAIN2 or msgType == RFXCOM_OREGON_MSG_RAIN3:
		
		if checksumr(msg):
			return addr, rrate, rtotal, bat
		else:
			return "", 0, 0, 0
			
	else:
		return "", 0, 0, 0

def decode_oregon_wind(msg, msgType):
	
	# Extract Address TTAAAAC (Type + Address + Channel)
	addr = get_address(msg, msgType, 0)

	# Extract wind direction (º)
	if msgType == RFXCOM_OREGON_MSG_WIND1 or msgType == RFXCOM_OREGON_MSG_WIND2:
		wdir = (msg[5] >> 4) * 22.5
	elif msgType == RFXCOM_OREGON_MSG_WIND3:
		wdir = (((msg[6] >> 4) & 0x0F) * 100) + ((msg[6] & 0x0F) * 10) + ((msg[5] >> 4) & 0x0F)
	else:
		wdir = 0			
	
	# Extract wind speed (m/s)
	wspeed = ((msg[8] & 0x0F) * 10) + ((msg[7] >> 4) & 0x0F) + ((msg[7] & 0x0F) / 10.0)
	
	# Extract wind average speed (m/s)
	wavgspeed = (((msg[9] >> 4) & 0x0F) * 10.0) + (msg[9] & 0x0F) + (((msg[8] >> 4) & 0x0F) / 10.0)

	# Extract battery capacity
	if msgType == RFXCOM_OREGON_MSG_WIND1:
		bat = wbattery_indication(msg[5])
	elif msgType ==	RFXCOM_OREGON_MSG_WIND2 or msgType == RFXCOM_OREGON_MSG_WIND3:
		bat = wrbattery(msg[5])
	else:
		bat = 0
		
	# Check for checksum
	if checksum9(msg):
		return addr, wdir, wspeed, wavgspeed, bat
	else:
		return "", 0, 0, 0, 0

def decode_oregon_uv(msg, msgType):
		
	# Extract Address TTAAAAC (Type + Address + Channel)
	addr = get_address(msg, msgType, 0)
	
	# Extract UV factor
	if msgType == RFXCOM_OREGON_MSG_UV1:
		uvfactor = ((msg[6] & 0x0F) * 10) + ((msg[5] >> 4) & 0x0F)
	elif msgType == RFXCOM_OREGON_MSG_UV2:
		uvfactor = ((msg[5] >> 4) & 0x0F)
	else:
		uvfactor = 0
	
	# Extract battery indication
	bat = wbattery_indication(msg[5])
		
	# Check for checksum
	if msgType == RFXCOM_OREGON_MSG_UV1:

		if checksumw(msg):
			return addr, uvfactor, bat
		else:
			return "", 0, 0
			
	elif msgType == RFXCOM_OREGON_MSG_UV2:
		
		if checksum7(msg):
			return addr, uvfactor, bat
		else:
			return "", 0, 0
	else:
		return "", 0, 0

def decode_oregon_weight(msg, msgType):
	
	# Extract Address TTAAAAC (Type + Address + Channel)
	addr = get_address2(msg, msgType)
	
	# Extract Weight (Kg)
	if msgType == RFXCOM_OREGON_MSG_WEIGHT1:
		weight = ((msg[6] & 0x01) * 100) + (((msg[5] >> 4) & 0x0F) * 10) + (msg[5] & 0x0F) + (((msg[4] >> 4) & 0x0F) / 10.0)
	elif msgType == RFXCOM_OREGON_MSG_WEIGHT2:
		weight = (((msg[5] & 0x0F) * 4096) + (msg[4] * 16) + ((msg[3] >> 4) & 0x0F)) / 400.8
	else:
		weight = 0
	
	# Check for checksum
	if msgType == RFXCOM_OREGON_MSG_WEIGHT1:
		if (((msg[1] & 0xF0) == (msg[6] & 0xF0)) and ((msg[2] & 0x0F) == (msg[7] & 0x0F))):
			return addr, weight
		else:
			return "", 0
	elif msgType == RFXCOM_OREGON_MSG_WEIGHT2:
		return "", 0
	else:	
		return "", 0

def decode_oregon_elec(msg, msgType):
	
	# Extract Address TTAAAAC (Type + Address + Channel)
	addr = get_address3(msg, msgType)
	
	# Extract Current measurement (Amps or kW)
	if msgType == RFXCOM_OREGON_MSG_ELEC1: # Amps
		ct1 = (msg[4] + ((msg[5] & 0x03) * 256)) / 10.0
		ct2 = (((msg[5] >> 2) & 0x3F) + ((msg[6] & 0x0F) * 64)) / 10.0
		ct3 = (((msg[6] >> 4) & 0x0F) + ((msg[7] & 0x3F) * 16)) / 10.0
			
	elif msgType == RFXCOM_OREGON_MSG_ELEC2: # kW
		ct1 = (((msg[6] & 0x0F) * 65536) + (msg[5] * 256) + (msg[4] & 0xF0)) / 994.0
		ct2 = 0
		ct3 = 0
	else:
		ct1 = 0
		ct2 = 0
		ct3 = 0	
			
	# Extract battery indication
	if (msg[2] & 0x10) == 0:
		bat = RFXCOM_OREGON_BAT_OK
	else:
		bat = RFXCOM_OREGON_BAT_LOW
	
	# Check for checksum
	if msgType == RFXCOM_OREGON_MSG_ELEC1:
		if checksume(msg):
			return addr, ct1, ct2, ct3, bat
		else:
			return 0, 0, 0, 0, 0
	elif msgType == RFXCOM_OREGON_MSG_ELEC2:
		if checksum12(msg):
			return addr, ct1, ct2, ct3, bat
		else:
			return "", 0, 0, 0, 0
	else:
		return "", 0, 0, 0, 0

def decode_oregon_dt(msg, msgType):
		
	# Extract channel
	if msgType == RFXCOM_OREGON_MSG_DT1:
		ch = wrchannel3(msg[3])
	else:
		ch = 0
	
	# Extract Address TTAAAAC (Type + Address + Channel)
	addr = get_address(msg, msgType, ch)
		
	# Extract Date/Time/Day
	if msgType == RFXCOM_OREGON_MSG_DT1:
		# Date format ddmmyy
		date = (((msg[9] & 0x0F) * 10) + ((msg[8] >> 4) & 0x0F)) * 10000	# dd
		date += ((msg[9] >> 4) & 0x0F) * 100 								# mm
		date += ((msg[11] & 0x0F) * 10) + ((msg[10] >> 4) & 0x0F) 			# yy
			
		# Time format hhmmss
		time = (((msg[8] & 0x0F) * 10) + ((msg[7] >> 4) & 0x0F)) * 10000 	# hr
		time += (((msg[7] & 0x0F) * 10) + ((msg[6] >> 4) & 0x0F)) * 100 	# min
		time += ((msg[6] & 0x0F) * 10) + ((msg[5] >> 4) & 0x0F) 			# sec
			
		# Day (0=Sunday, 6=Saturday)
		day = msg[10] & 0x07
	else:
		date = 0
		time = 0
		day = 0
			
	# Check for checksum
	if msgType == RFXCOM_OREGON_MSG_DT1:
		if checksum11(msg):
			return addr, date, time, day
		else:
			return "", 0, 0, 0
	else:
		return "", 0, 0, 0

def processOregonMsg(msg, msgType):
	
	# Initialize vars
	oregonSensorData = list()
	oregonSensorData.append(RFXCOM_SENSOR_OREGON)
	addr = []
	value1 = 0.0
	value2 = 0.0
	value3 = 0.0
	bat = RFXCOM_OREGON_BAT_UNKNOWN
	
	# Decode the message received
	if (msgType == RFXCOM_OREGON_MSG_TEMP1 or msgType == RFXCOM_OREGON_MSG_TEMP2
		or msgType == RFXCOM_OREGON_MSG_TEMP3 or msgType == RFXCOM_OREGON_MSG_TEMP4):

		addr, value1, bat = decode_oregon_temp(msg, msgType)
		oregonSensorData.append(addr)
		oregonSensorData.append(2)
		oregonSensorData.append(("Temperature", str(round(value1, 1)), "°C"))
		oregonSensorData.append(("BatteryLow", str(0 if bat == RFXCOM_OREGON_BAT_OK else 1), ""))
		return oregonSensorData

	elif (msgType == RFXCOM_OREGON_MSG_TH1 or msgType == RFXCOM_OREGON_MSG_TH2 or msgType == RFXCOM_OREGON_MSG_TH3
		or msgType == RFXCOM_OREGON_MSG_TH4 or msgType == RFXCOM_OREGON_MSG_TH5 or msgType == RFXCOM_OREGON_MSG_TH6):

		addr, value1, value2, bat = decode_oregon_th(msg, msgType)
		oregonSensorData.append(addr)
		oregonSensorData.append(3)
		oregonSensorData.append(("Temperature", str(round(value1, 1)), "°C"))
		oregonSensorData.append(("Humidity", str(round(value2, 0)), "%"))
		if msgType == RFXCOM_OREGON_MSG_TH6:
			oregonSensorData.append(("Bat", str(bat), "%"))
		else:
			oregonSensorData.append(("BatteryLow", str(0 if bat == RFXCOM_OREGON_BAT_OK else 1), ""))
		return oregonSensorData
		
	elif msgType == RFXCOM_OREGON_MSG_THB1 or msgType == RFXCOM_OREGON_MSG_THB2:

		addr, value1, value2, value3, bat = decode_oregon_thb(msg, msgType)
		oregonSensorData.append(addr)
		oregonSensorData.append(4)
		oregonSensorData.append(("Temperature", str(round(value1, 1)), "°C"))
		oregonSensorData.append(("Humidity", str(round(value2, 0)), "%"))
		oregonSensorData.append(("Pressure", str(value3), "hPA"))
		oregonSensorData.append(("BatteryLow", str(0 if bat == RFXCOM_OREGON_BAT_OK else 1), ""))
		return oregonSensorData
		
	elif msgType == RFXCOM_OREGON_MSG_RAIN1 or msgType == RFXCOM_OREGON_MSG_RAIN2 or msgType == RFXCOM_OREGON_MSG_RAIN3:

		addr, value1, value2, bat = decode_oregon_rain(msg, msgType)
		oregonSensorData.append(addr)
		oregonSensorData.append(3)
		oregonSensorData.append(("Rain rate", str(round(value1, 2)), "mm/hr"))
		oregonSensorData.append(("Rain total", str(round(value2, 2)), "mm"))
		oregonSensorData.append(("BatteryLow", str(0 if bat == RFXCOM_OREGON_BAT_OK else 1), ""))
		return oregonSensorData
		
	elif msgType == RFXCOM_OREGON_MSG_WIND1 or msgType == RFXCOM_OREGON_MSG_WIND2 or msgType == RFXCOM_OREGON_MSG_WIND3:

		addr, value1, value2, value3, bat = decode_oregon_wind(msg, msgType)
		oregonSensorData.append(addr)
		oregonSensorData.append(4)
		oregonSensorData.append(("Wind direction", str(value1), "°"))
		oregonSensorData.append(("Speed", str(round(value2, 1)), "m/s"))
		oregonSensorData.append(("SpeedAvg", str(round(value3, 1)), "m/s"))
		if msgType ==	RFXCOM_OREGON_MSG_WIND1:
			oregonSensorData.append(("BatteryLow", str(0 if bat == RFXCOM_OREGON_BAT_OK else 1), ""))
		else:
			oregonSensorData.append(("Battery", str(bat), "%"))
		return oregonSensorData
		
	elif msgType == RFXCOM_OREGON_MSG_UV1 or msgType == RFXCOM_OREGON_MSG_UV2:

		addr, value1, bat = decode_oregon_uv(msg, msgType)
		oregonSensorData.append(addr)
		oregonSensorData.append(2)
		oregonSensorData.append(("UV factor", str(value1), ""))
		oregonSensorData.append(("Battery", str(bat), "%"))
		return oregonSensorData
		
	elif msgType == RFXCOM_OREGON_MSG_DT1:

		addr, value1, value2, value3 = decode_oregon_dt(msg, msgType)
		oregonSensorData.append(addr)
		oregonSensorData.append(3)
		oregonSensorData.append(("Date", str(value1), ""))
		oregonSensorData.append(("Time", str(value2), ""))
		oregonSensorData.append(("Day", str(value3), ""))
		return oregonSensorData
		
	elif msgType == RFXCOM_OREGON_MSG_WEIGHT1 or msgType == RFXCOM_OREGON_MSG_WEIGHT2:

		addr, value1 = decode_oregon_weight(msg, msgType)
		oregonSensorData.append(addr)
		oregonSensorData.append(1)
		oregonSensorData.append(("Weight", str(round(value1, 1)), "Kg"))
		return oregonSensorData
		
	elif msgType == RFXCOM_OREGON_MSG_ELEC1 or msgType == RFXCOM_OREGON_MSG_ELEC2:

		addr, value1, value2, value3, bat = decode_oregon_elec(msg, msgType)
		oregonSensorData.append(addr)
		oregonSensorData.append(4)
		if msgType == RFXCOM_OREGON_MSG_ELEC1: # Amps
			oregonSensorData.append(("CT1", str(value1), "A"))
			oregonSensorData.append(("CT2", str(value2), "A"))
			oregonSensorData.append(("CT3", str(value3), "A"))
		elif msgType == RFXCOM_OREGON_MSG_ELEC2: # kW
			oregonSensorData.append(("CT1", str(value1), "kW"))
			oregonSensorData.append(("CT2", str(value2), "kW"))
			oregonSensorData.append(("CT3", str(value3), "kW"))
		oregonSensorData.append(("Battery", str(bat), "%"))
		return oregonSensorData
			
	else:
		oregonSensorData.append(addr)
		oregonSensorData.append(0)
		return oregonSensorData
