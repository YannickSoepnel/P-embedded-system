import time
import serial

BAUDRATE = 19200
TIMEOUT = 2
con = serial.Serial('COM10', BAUDRATE)	#licht en afstand
con2 = serial.Serial('COM6', BAUDRATE)
temperatuur_data = []
licht_data = []
afstand_data = []

def data_licht():
    data = con.read().hex()  # zet de data van de poort in een variabele
    newdata = int(data, 16)  # zet de hexadecimale data om in een integer
    # print(' light or distance ' + str(newdata))
    return newdata

def data_temp():

    data = con2.read().hex()  # zet de data van de poort in een variabele
    newdata = int(data, 16)  # zet de hexadecimale data om in een integer
    # print(' temp '+ str(newdata))
    return newdata

def update_data():
    data = data_licht()      # Zet seriële waarde in data
    if data == 0xf0:                            # Check of de data 0xff is
        # print('1 ' + str(data))
        data = data_licht()  # Zet seriële waarde na de 0xff in data
        print('2 ' + str(data))
        afstand_data.append(data)          # Voeg data toe in de afstand lijst
    data = data_licht()
    if data == 0x0f:                            # Check of de data 0x0f is
        # print('3 ' + str(data))
        data = data_licht()  # Zet seriële waarde na de 0x0f in data
        print('4 ' + str(data))
        licht_data.append(data)            # Voeg data toe in de lichtintensiteit lijst
    data = data_temp()
    if data == 0xff:                            # Kijk of de data 0xff is
        # print('5 ' + str(data))
        data = data_temp()   # Zet seriële waarde na 0xff in data
        data = data / 10                        # Deel de data door 10 omdat hij vanuit de arduino met 10 is vermenigvuldigd
        print('6 ' + str(data))
        temperatuur_data.append(data)      # Voeg de data toe in de temperatuur lijst

def main():
	while True:
		update_data()
		time.sleep(1)


main()