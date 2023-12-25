import datetime
from multiprocessing import Process
import sys
import os
import time
import random
import platform
import serial
from serial.serialutil import Timeout
from advent import advent, qadvent
from newyear import newYear

if platform.system() == "Linux":
    port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)
elif platform.system() == "Windows":
    port = serial.Serial("COM15", baudrate=115200, timeout=3.0)
pass


def get_event_lights():
    eventLights = []
    n = random.randint(5,12)
    for i in range(n):
        l = random.randint(5,100)
        eventLights.append(l)
    print(f"event Lights: {eventLights}")
    return eventLights
    

def snow():
    qadvent()
    for l in get_event_lights():
        port.write(str.encode(f"0,{l},100,100,100#"))
        port.write(str.encode("show#"))
        time.sleep(1)
    return True

def rain():
    qadvent()
    for l in get_event_lights():
        port.write(str.encode(f"0,{l},0,0,200#"))
        port.write(str.encode("show#"))
        time.sleep(1)
    return True

def cloud():
    advent()
    return True

def fog():
    advent()
    return True

def clear():
    advent()
    return True

