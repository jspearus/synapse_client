import datetime
from multiprocessing import Process
import sys
import os
import time
import platform
import serial
from serial.serialutil import Timeout

if platform.system() == "Linux":
    port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)
elif platform.system() == "Windows":
    port = serial.Serial(port="COM15", baudrate=115200, timeout=3.0)
pass

print(platform.system())

def advent():
    day = datetime.date.today()
    for i in range(50, -1, -1):
        port.write(str.encode(f"1,{i},0,100,0#"))
        port.write(str.encode("show#"))
        time.sleep(.07)
    day = int(day.strftime("%d"))
    for i in range(0, (day*2), 2):
        port.write(str.encode(f"1,{i},100,0,0#"))
        port.write(str.encode("show#"))
        time.sleep(.1)
    return True


def morningAdvent():
    day = datetime.date.today()
    for i in range(50, -1, -1):
        port.write(str.encode(f"1,{i},0,50,0#"))
        port.write(str.encode("show#"))
        time.sleep(.07)
    day = int(day.strftime("%d"))
    for i in range(0, (day*2), 2):
        port.write(str.encode(f"1,{i},50,0,0#"))
        port.write(str.encode("show#"))
        time.sleep(.1)
    return True
