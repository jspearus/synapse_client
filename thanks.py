import datetime
from multiprocessing import Process
import sys
import os
import time
import platform
import serial
from serial.serialutil import Timeout

if platform.system() == "Linux":
    port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)
elif platform.system() == "Windows":
    port = serial.Serial("COM15", baudrate=115200, timeout=3.0)
pass


def thanksGiving():
    for i in range(50):
        port.write(str.encode(f"5,{i},255,0,0#"))
        port.write(str.encode("show5#"))
        time.sleep(.07)
    for i in range(100):
        port.write(str.encode(f"0,{i},205,102,14#"))
        port.write(str.encode("show#"))
        time.sleep(.07)
    for i in range(-1, 100, 2):
        port.write(str.encode(f"1,{i},200,0,0#"))
        port.write(str.encode("show1#"))
        time.sleep(.1)
        port.write(str.encode(f"2,{i},200,0,0#"))
        port.write(str.encode("show2#"))
        time.sleep(.1)
        port.write(str.encode(f"3,{i},200,0,0#"))
        port.write(str.encode("show3#"))
        time.sleep(.1)
        port.write(str.encode(f"4,{i},200,0,0#"))
        port.write(str.encode("show4#"))
        time.sleep(.1)

    for i in range(64):
        port.write(str.encode(f"5,{i+50},128,128,128#"))
        port.write(str.encode("show5#"))
        time.sleep(.07)
    return True

def morningThanksGiving():
    for i in range(50):
        port.write(str.encode(f"5,{i},75,0,0#"))
        port.write(str.encode("show5#"))
        time.sleep(.02)
    for i in range(100, -1, -1):
        port.write(str.encode(f"0,{i},92,71,7#"))
        port.write(str.encode("show#"))
        time.sleep(.07)
    for i in range(0, 100, 2):
        port.write(str.encode(f"1,{i},100,0,0#"))
        port.write(str.encode("show1#"))
        time.sleep(.1)
        port.write(str.encode(f"2,{i},100,0,0#"))
        port.write(str.encode("show2#"))
        time.sleep(.1)
        port.write(str.encode(f"3,{i},100,0,0#"))
        port.write(str.encode("show3#"))
        time.sleep(.1)
        port.write(str.encode(f"4,{i},100,0,0#"))
        port.write(str.encode("show4#"))
        time.sleep(.1)

    for i in range(64):
        port.write(str.encode(f"5,{i+50},100,100,100#"))
        port.write(str.encode("show5#"))
        time.sleep(.07)
    return True