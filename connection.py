import glob
import serial
import sys
import time
import struct


class Connectie:
    BAUDRATE = 19200
    TIMEOUT = 2
    con = serial.Serial('COM10', BAUDRATE)
    con2 = serial.Serial('COM6', BAUDRATE)

    def __init__(self):
        pass


    """""
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
    """
    def hex_to_int(self, hexadecimal):			# zet hexadecimale waarde om in een integer
        start = hexadecimal
        if start == '':
            end = 0
        else:
            end = int(start, 16)
        return end

    def serial_scanner(self):
        global ports
        count = 1
        check_data = 0xff
        worked = 0
        for port in ports:
            try:
                # print(count)
                count += 1
                s = serial.Serial(port, self.BAUDRATE, timeout = self.TIMEOUT)
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
                        self.start_connection(port)
                    else:
                        self.start_connection2(port)
            except (OSError, serial.SerialException):
                pass

    def start_connection(self, port):
        con = serial.Serial(port, self.BAUDRATE)
        print(self.con)

    def start_connection2(self, port):
        con2 = serial.Serial(port, self.BAUDRATE)
        print(self.con2)

    def data_licht(self):
        data = self.con.read().hex()  # zet de data van de poort in een variabele
        newdata = int(data, 16)  # zet de hexadecimale data om in een integer
        # print(' light or distance ' + str(newdata))
        return newdata

    def data_temp(self):

        data = self.con2.read().hex()  # zet de data van de poort in een variabele
        newdata = int(data, 16)  # zet de hexadecimale data om in een integer
        # print(' temp '+ str(newdata))
        return newdata

    # if __name__ == '__main__':
    #     serial_scanner()
