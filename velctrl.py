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


def right_turn():
    port.write(str.encode("1,11,0,100,0#"))
    port.write(str.encode("1,13,0,100,0#"))
    port.write(str.encode("1,18,0,100,0#"))
    port.write(str.encode("1,19,0,100,0#"))
    port.write(str.encode("1,20,0,100,0#"))
    port.write(str.encode("1,21,0,100,0#"))
    port.write(str.encode("1,26,0,100,0#"))
    port.write(str.encode("1,30,0,100,0#"))
    port.write(str.encode("1,31,0,100,0#"))
    port.write(str.encode("1,32,0,100,0#"))
    port.write(str.encode("1,33,0,100,0#"))
    port.write(str.encode("1,37,0,100,0#"))
    port.write(str.encode("1,38,0,100,0#"))
    port.write(str.encode("1,41,0,100,0#"))
    port.write(str.encode("1,42,0,100,0#"))
    port.write(str.encode("1,47,0,100,0#"))
    port.write(str.encode("1,49,0,100,0#"))
    port.write(str.encode("1,50,0,100,0#"))
    port.write(str.encode("1,51,0,100,0#"))
    port.write(str.encode("1,52,0,100,0#"))
    port.write(str.encode("1,59,0,100,0#"))
    port.write(str.encode("1,60,0,100,0#"))
    port.write(str.encode("1,12,100,0,0#"))
    port.write(str.encode("1,17,100,0,0#"))
    port.write(str.encode("1,25,100,0,0#"))
    port.write(str.encode("1,46,100,0,0#"))
    port.write(str.encode("1,53,100,0,0#"))
    port.write(str.encode("1,61,100,0,0#"))
    port.write(str.encode("show#"))
    time.sleep(5)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
    
def left_turn():
    port.write(str.encode("2,11,0,100,0#"))
    port.write(str.encode("2,13,0,100,0#"))
    port.write(str.encode("2,18,0,100,0#"))
    port.write(str.encode("2,19,0,100,0#"))
    port.write(str.encode("2,20,0,100,0#"))
    port.write(str.encode("2,21,0,100,0#"))
    port.write(str.encode("2,26,0,100,0#"))
    port.write(str.encode("2,30,0,100,0#"))
    port.write(str.encode("2,31,0,100,0#"))
    port.write(str.encode("2,32,0,100,0#"))
    port.write(str.encode("2,33,0,100,0#"))
    port.write(str.encode("2,37,0,100,0#"))
    port.write(str.encode("2,38,0,100,0#"))
    port.write(str.encode("2,41,0,100,0#"))
    port.write(str.encode("2,42,0,100,0#"))
    port.write(str.encode("2,47,0,100,0#"))
    port.write(str.encode("2,49,0,100,0#"))
    port.write(str.encode("2,50,0,100,0#"))
    port.write(str.encode("2,51,0,100,0#"))
    port.write(str.encode("2,52,0,100,0#"))
    port.write(str.encode("2,59,0,100,0#"))
    port.write(str.encode("2,60,0,100,0#"))
    port.write(str.encode("2,12,100,0,0#"))
    port.write(str.encode("2,17,100,0,0#"))
    port.write(str.encode("2,25,100,0,0#"))
    port.write(str.encode("2,46,100,0,0#"))
    port.write(str.encode("2,53,100,0,0#"))
    port.write(str.encode("2,61,100,0,0#"))
    port.write(str.encode("show#"))
    time.sleep(5)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))



def runLeftTurn():
    tProc = Process(target=left_turn, args=())
    tProc.start()
    
def runRightTurn():
    tProc = Process(target=right_turn, args=())
    tProc.start()