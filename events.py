import datetime
from multiprocessing import Process
import sys
import os
import time
import platform
import serial
from serial.serialutil import Timeout
from advent import advent
from newyear import newYear

if platform.system() == "Linux":
    port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)
elif platform.system() == "Windows":
    port = serial.Serial("COM15", baudrate=115200, timeout=3.0)
pass


def snow():
    day = datetime.date.today()
    for i in range(50):
        port.write(str.encode(f"1,{i},200,200,200#"))
        port.write(str.encode("show1#"))
        time.sleep(.01)
    return True



def rain():
    day = datetime.date.today()
    for i in range(50):
        port.write(str.encode(f"1,{i},0,0,200#"))
        port.write(str.encode("show1#"))
        time.sleep(.01)
    return True

def cloud():
    day = datetime.date.today()
    for i in range(50):
        port.write(str.encode(f"1,{i},0,200,0#"))
        port.write(str.encode("show1#"))
        time.sleep(.01)
    return True

def fog():
    day = datetime.date.today()
    for i in range(50):
        port.write(str.encode(f"1,{i},0,200,0#"))
        port.write(str.encode("show1#"))
        time.sleep(.01)
    return True

def clear():
    day = datetime.date.today()
    for i in range(50):
        port.write(str.encode(f"1,{i},0,200,0#"))
        port.write(str.encode("show1#"))
        time.sleep(.01)
    return True


