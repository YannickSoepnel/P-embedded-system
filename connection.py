import glob
import serial
import sys
import time
import struct
class Connection():

BAUDRATE = 19200

TIMEOUT = 2 
 
# Create list of potential ports
if sys.platform.startswith('win'):
    ports = ['COM' + str(i + 1) for i in range(256)]
elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    ports = glob.glob('/dev/tty[A-Za-z]*')
else:
    raise EnvironmentError('Unsupported platform')

port_exceptions = ['dev/ttyprintk']
for port in port_exceptions:
    if port in ports:
        ports.remove(port)


def hex_to_int(hexadecimal):			# zet hexadecimale waarde om in een integer
	start = hexadecimal
	if start == '':
		end = 0
	else:
		end = int(start, 16)
	return end


def serial_scanner():
    global ports
    count = 1
    check_data = 0xff
    worked = 0
    for port in ports:
        try:
            # print(count)
            count += 1
            s = serial.Serial(port, BAUDRATE, timeout = TIMEOUT)
            print('Connected to %s'%port)
            time.sleep(1)
            s.write(struct.pack('>B', check_data))
            somevalue = s.read()
            raw_read = somevalue.hex()
            print(raw_read)
            if raw_read == '':
                print('IT WORKS!')
                s.close()
                if worked == 0:
                    worked = 1
                    start_connection(port)
                else:
                    start_connection2(port)
        except (OSError, serial.SerialException):
            pass


def start_connection(port):
    con = serial.Serial(port, BAUDRATE)
    print(con)


def start_connection2(port):
    con2 = serial.Serial(port, BAUDRATE)
    print(con2)


if __name__ == '__main__':
    serial_scanner()
