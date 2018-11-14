from gui import *
import struct

def setup():
    ser.write(struct.pack('>B', onoff))