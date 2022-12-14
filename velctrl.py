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
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
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
    time.sleep(1)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
    
def left_turn():
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
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
    time.sleep(1)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
    
def hazard():
    red_light()
    red_light()
   

    
    
    

def red_light():
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
    port.write(str.encode("0,2,100,0,0#"))
    port.write(str.encode("0,3,100,0,0#"))
    port.write(str.encode("0,4,100,0,0#"))
    port.write(str.encode("0,5,100,0,0#"))
    port.write(str.encode("0,9,100,0,0#"))
    port.write(str.encode("0,14,100,0,0#"))
    port.write(str.encode("0,16,100,0,0#"))
    port.write(str.encode("0,23,100,0,0#"))
    port.write(str.encode("0,24,100,0,0#"))
    port.write(str.encode("0,31,100,0,0#"))
    port.write(str.encode("0,32,100,0,0#"))
    port.write(str.encode("0,39,100,0,0#"))
    port.write(str.encode("0,41,100,0,0#"))
    port.write(str.encode("0,46,100,0,0#"))
    port.write(str.encode("0,50,100,0,0#"))
    port.write(str.encode("0,51,100,0,0#"))
    port.write(str.encode("0,52,100,0,0#"))
    port.write(str.encode("0,53,100,0,0#"))
    port.write(str.encode("show#"))    
    time.sleep(.25)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
    time.sleep(.25)
    
def runLeftTurn():
    tProc = Process(target=left_turn, args=())
    tProc.start()
    
def runRightTurn():
    tProc = Process(target=right_turn, args=())
    tProc.start()

def runHazard():
    hProc = Process(target=hazard, args=())
    hProc.start()