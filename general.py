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
    port = serial.Serial("COM15", baudrate=115200, timeout=3.0)
pass


def village():
    time.sleep(1.5)
    #Neopixel
    port.write(str.encode("0,4,32,10,4#"))
    #Command
    port.write(str.encode("show#"))
    time.sleep(10)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))   

def runVillage():
    tProc = Process(target=tree, args=())
    tProc.start()
