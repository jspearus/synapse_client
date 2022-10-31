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


def tree():
    time.sleep(1.5)
    # trunk
    port.write(str.encode("0,4,32,10,4#"))
    # tree
    port.write(str.encode("0,9,0,120,0#"))
    port.write(str.encode("0,10,0,120,0#"))
    port.write(str.encode("0,11,150,0,0#"))  #
    port.write(str.encode("0,12,0,150,0#"))
    port.write(str.encode("0,13,0,150,0#"))
    port.write(str.encode("0,18,0,150,0#"))
    port.write(str.encode("0,19,0,150,0#"))
    port.write(str.encode("0,20,0,150,0#"))
    port.write(str.encode("0,21,150,0,0#"))  #
    port.write(str.encode("0,22,0,150,0#"))
    port.write(str.encode("0,26,0,150,0#"))
    port.write(str.encode("0,27,150,0,0#"))  #
    port.write(str.encode("0,28,0,150,0#"))
    port.write(str.encode("0,35,150,0,0#"))  #
    port.write(str.encode("0,36,0,150,0#"))
    port.write(str.encode("0,37,0,150,0#"))
    port.write(str.encode("0,43,0,150,0#"))
    # top
    port.write(str.encode("0,52,150,0,0#"))  #
    port.write(str.encode("show#"))

    time.sleep(10)

    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))


def test1():
    time.sleep(2)
    for i in range(65):
        port.write(str.encode(f"0,{i},100,0,0#"))
        port.write(str.encode("show#"))
        time.sleep(.01)
    time.sleep(.1)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
    for i in range(65):
        port.write(str.encode(f"0,{i},0,100,0#"))
        port.write(str.encode("show#"))
        time.sleep(.01)
    time.sleep(.1)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
    for i in range(65):
        port.write(str.encode(f"0,{i},0,0,100#"))
        port.write(str.encode("show#"))
        time.sleep(.01)
    time.sleep(.1)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))


def init():
    for i in range(65):
        port.write(str.encode(f"0,{i},100,0,0#"))
        port.write(str.encode("show#"))
        time.sleep(.01)
    time.sleep(.1)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
    for i in range(65):
        port.write(str.encode(f"0,{i},100,0,0#"))
        port.write(str.encode("show#"))
        time.sleep(.01)
    time.sleep(.1)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
    for i in range(65):
        port.write(str.encode(f"0,{i},100,0,0#"))
        port.write(str.encode("show#"))
        time.sleep(.01)
    time.sleep(.1)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))


def cloak():
    time.sleep(1)
    for i in range(65):
        port.write(str.encode(f"0,{i},100,100,0#"))
        port.write(str.encode("show#"))
        time.sleep(.01)
    time.sleep(.1)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
    for i in range(65):
        port.write(str.encode(f"0,{i},100,100,0#"))
        port.write(str.encode("show#"))
        time.sleep(.01)
    time.sleep(.1)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
    for i in range(65):
        port.write(str.encode(f"0,{i},100,100,0#"))
        port.write(str.encode("show#"))
        time.sleep(.01)
    time.sleep(.1)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))


def loud():
    time.sleep(1)
    for i in range(65):
        port.write(str.encode(f"0,{i},100,0,0#"))
        port.write(str.encode("show#"))
        time.sleep(.01)
    time.sleep(.1)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
    for i in range(65):
        port.write(str.encode(f"0,{i},100,0,0#"))
        port.write(str.encode("show#"))
        time.sleep(.01)
    time.sleep(.1)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
    for i in range(65):
        port.write(str.encode(f"0,{i},100,0,0#"))
        port.write(str.encode("show#"))
        time.sleep(.01)
    time.sleep(.1)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))


def runTree():
    tProc = Process(target=tree, args=())
    tProc.start()


def runtest1():
    tProc = Process(target=test1, args=())
    tProc.start()


def runInit():
    tProc = Process(target=init, args=())
    tProc.start()


def runCloak():
    tProc = Process(target=cloak, args=())
    tProc.start()


def runLoad():
    tProc = Process(target=loud, args=())
    tProc.start()
