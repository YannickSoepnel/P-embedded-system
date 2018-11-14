import serial
import time
import struct

ser = serial.Serial('COM6',19200)  	# open de connectie
print(ser)							# print de data van de

class Connectie:
	def __init__(self):
		self.main()

	def get_values(self):			# een functie die de poort uitleest
		s = ser.read()
		return s

	def hex_to_int(self, hexadecimal):			# zet hexadecimale waarde om in een integer
		start = hexadecimal
		end = int(start, 16)
		return end

	def recieve_data(self):

		
		data = self.get_values().hex() 		# zet de data van de poort in een variabele
		data = self.hex_to_int(data)		# zet de hexadecimale data om in een integer
		return data

	def main(self):
		count = 0
		afstand = []
		licht = []
		while True:
			#count = count + 1
			data = self.recieve_data()
			if data == 0xff:
				data = self.recieve_data()
				afstand.append(data)
			data = self.recieve_data()
			if data == 0x0f:
				data = self.recieve_data()
				licht.append(data)
			time.sleep(0.05)
			print(afstand)
			print(licht)




connectie1 = Connectie()		# Maak de connectie aan


