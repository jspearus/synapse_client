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


def newYear():
    for i in range(50):
        port.write(str.encode(f"1,{i},100,100,100#"))
        port.write(str.encode("show#"))
        time.sleep(.07)
    for i in range(100):
        port.write(str.encode(f"0,{i},128,128,128#"))
        port.write(str.encode("show#"))
        time.sleep(.07)
    for i in range(-1, 100, 2):
        port.write(str.encode(f"2,{i},0,0,128#"))
        port.write(str.encode("show2#"))
        time.sleep(.1)
        port.write(str.encode(f"3,{i},0,0,128#"))
        port.write(str.encode("show3#"))
        time.sleep(.1)
        port.write(str.encode(f"4,{i},0,0,128#"))
        port.write(str.encode("show4#"))
        time.sleep(.1)
        port.write(str.encode(f"5,{i},0,0,128#"))
        port.write(str.encode("show5#"))
        time.sleep(.1)

    for i in range(64):
        port.write(str.encode(f"1,{i+50},128,128,128#"))
        port.write(str.encode("show1#"))
        time.sleep(.07)
    return True

def morningNewYear():
    day = datetime.date.today()
    for i in range(50):
        port.write(str.encode(f"1,{i},75,75,75#"))
        port.write(str.encode("show1#"))
        time.sleep(.02)
    for i in range(100, -1, -1):
        port.write(str.encode(f"0,{i},75,75,75#"))
        port.write(str.encode("show#"))
        time.sleep(.07)
    day = int(day.strftime("%d")) * 2
    for i in range(0, (day*2), 2):
        port.write(str.encode(f"2,{i},0,0,50#"))
        port.write(str.encode("show2#"))
        time.sleep(.1)
        port.write(str.encode(f"3,{i},0,0,50#"))
        port.write(str.encode("show3#"))
        time.sleep(.1)
        port.write(str.encode(f"4,{i},0,0,50#"))
        port.write(str.encode("show4#"))
        time.sleep(.1)
        port.write(str.encode(f"5,{i},0,0,50#"))
        port.write(str.encode("show5#"))
        time.sleep(.1)

    for i in range(64):
        port.write(str.encode(f"1,{i+50},100,100,100#"))
        port.write(str.encode("show1#"))
        time.sleep(.07)
    return True

def fire_works():
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
    for i in range(50):
        port.write(str.encode(f"1, {i}, 100, 100,100#"))
        port.write(str.encode("show#"))
        time.sleep(.01)
    time.sleep(.5)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
    time.sleep(1)
    for i in range(32):
        port.write(str.encode(f"1, {i+50}, 250, 0,0#"))
    port.write(str.encode("show#"))
    time.sleep(.4)
    
    for i in range(24):
        port.write(str.encode(f"1, {i+82}, 250, 0,0#"))
    port.write(str.encode("show#"))
    time.sleep(.4)
    for i in range(7):
        port.write(str.encode(f"1, {i+106}, 100, 100,100#"))
    port.write(str.encode("show#"))
    for i in range(37, 0 , -1):
        port.write(str.encode(f"0, {i}, 250, 0,0#"))
        port.write(str.encode(f"0, {i+63}, 0, 250,0#"))
        port.write(str.encode("show#"))
        
    time.sleep(1)
    port.write(str.encode("clear#"))
    port.write(str.encode("show#"))
    # 0 - 36 first col, 37 - 66 2nd col 67 - 99 last col
    return True