import serial
import time
import struct


def get_values():			# een functie die de poort uitleest
		s = connection.read()
		return s

def hex_to_int(hexadecimal):			# zet hexadecimale waarde om in een integer
	start = hexadecimal
	end = int(start, 16)
	return end


port = "COM6"
print(port)
connection = serial.Serial('COM6', 19200)
print("test")
print(connection)
time.sleep(1)
connection.write(struct.pack('>B', 0xff))
count = 0
while True:
	print(count)
	count += 1
	raw_read = get_values().hex()
	raw_read = hex_to_int(raw_read)
	time.sleep(0.5)
	print(raw_read)
	time.sleep(1)

