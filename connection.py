import serial
import time
import struct
import test
import threading

ser = serial.Serial('COM7',19200)  	# open de connectie
print(ser)							# print de data van de



class Connectie:
	def __init__(self):
		self.numPoints = 3
		self.dataList = [0] * self.numPoints  # maak een lijst met 3 getallen
		self.onoff = 0
		self.list1 = []
		self.list2 = []


	def get_values(self):			# een functie die de poort uitleest
		s = ser.read()
		return s

	def hex_to_int(self, hexadecimal):			# zet hexadecimale waarde om in een integer
		start = hexadecimal
		end = int(start, 16)
		return end

	def send_values(self, value):		# switch de waarde van onoff tussen 0xff en 0x0f
		if value == 0xff:
		# if onoff == 1:
			value = 0x0f
		else:
			value = 0xff
		return value

	def print_values(self):
		print('dataList')
		print(self.dataList)
		print('list1 (light )')
		print(self.list1)
		print('list2 (temperature)')
		print(self.list2)

	def senddata(self, onoff):
		onoff = self.send_values(onoff)
		ser.write(struct.pack('>B', onoff))

	def recieve_data(self):

		for i in range(0, self.numPoints):  # doorloop de lijst
			data = self.get_values().hex() 		# zet de data van de poort in een variabele
			data = self.hex_to_int(data)		# zet de hexadecimale data om in een integer
			self.dataList[i] = data 			# zet de data in de lijst
		#return self.dataList
		count = 0
		self.list1.append((count, self.dataList[1]))
		self.list2.append((count, self.dataList[2]))
		self.print_values()

	def main(self):
		
		if senddata == 1:
			onoff = send_values(status)
			ser.write(struct.pack('>B.', onoff))
		self.onoff = self.send_values(self.onoff)		# verander de waarde van onoff
		print(self.onoff)
		ser.write(struct.pack('>B', self.onoff))	#v erzend de waarde onoff
		if userInput == 'close':			# kijk of de input 'close' is
			ser.close()						# sluit de connectie
		


connectie1 = Connectie()		# Maak de connectie aan
connectie1.main()				# roep de main functie aan


def update():
	connectie1.recieve_data()


timer = threading.Timer(1.0, update())
timer.start()

