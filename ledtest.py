import serial
import time
import struct

ser = serial.Serial('COM7',19200)  	# open de connectie
print(ser)	
time.sleep(1)

def senddata(onoff):
		sentdata = onoff
		ser.write(struct.pack('>B', sentdata))