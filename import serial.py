import serial
import time
import struct

ser = serial.Serial('/dev/tty.usbmodem1411',19200)  	#open de connectie
print(ser)							#print de data van de 

numPoints = 3
dataList = [0]*numPoints	#maak eenn lijst met 3 gtallen
onoff = 0
count = 0 
list1 = []
list2 = []

def getValues():			#een functie die de poort uitleest
	s = ser.read()
	return s

def hexToInt(hexadecimal):	#zet hexadecimale waarde om in een integer
	start = hexadecimal
	end = int(start, 16)
	return end

def sendValues(onoff):		#switch de waarde van onoff tussen 0xff en 0x0f
	if onoff == 0xff:
		onoff = 0x0f
	else:
		onoff = 0xff
	return onoff

def printValues():
	print('dataList')
	print(dataList)
	print('list1 (light )')
	print(list1)
	print('list2 (temperature)')
	print(list2)


while True:
	
	userInput = input('send? Press 1!, recieve? Press 2!') 	#vraag de gebruiker of hij data wil

	if userInput == '2':				#kijk of de input '2' is
		for i in range(0, numPoints):	# doorloop de lijst
			data = getValues().hex() 	#zet de data van de poort in een variabele
			data = hexToInt(data)		#zet de hexadecimale data om in een integer
			dataList[i] = data 			#zet de data in de lisjt
		list1.append((count, dataList[1]))
		list2.append((count, dataList[2]))
		count = count + 1
		printValues()

	if userInput == '1':				#kijk of de input '1' is
		onoff = sendValues(onoff)		#verander de waarde van onoff
		print(onoff)
		ser.write(struct.pack('>B', onoff))	#verzend de waarde onoff

	if userInput == 'close':			#kijk of de input 'close' is
		ser.close()						#sluit de connectie

