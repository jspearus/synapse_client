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
    for i in range(64):
        port.write(str.encode(f"1,{i+50},200,200,200#"))
        port.write(str.encode("show1#"))
        time.sleep(.01)

    for i in range(50):
        port.write(str.encode(f"2,{i},100,100,100#"))
        port.write(str.encode(f"3,{i},100,100,100#"))
        port.write(str.encode(f"4,{i},100,100,100#"))
        port.write(str.encode(f"5,{i},100,100,100#"))
        port.write(str.encode("show#"))
        time.sleep(.3)
    time.sleep(30)
    temp = advent()
    return True



def rain():
    day = datetime.date.today()
    for i in range(64):
        port.write(str.encode(f"1,{i+50},0,0,200#"))
        port.write(str.encode("show1#"))
        time.sleep(.01)

    for i in range(50, -2, -1):
        port.write(str.encode(f"2,{i},0,0,150#"))
        port.write(str.encode(f"3,{i},0,0,150#"))
        port.write(str.encode(f"4,{i},0,0,150#"))
        port.write(str.encode(f"5,{i},0,0,150#"))
        port.write(str.encode("show#"))
        time.sleep(.3)
    time.sleep(30)
    temp = advent()
    return True

