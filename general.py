import datetime
from multiprocessing import Process
import platform
import serial
from serial.serialutil import Timeout

if platform.system() == "Linux":
    port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)
elif platform.system() == "Windows":
    port = serial.Serial("COM15", baudrate=115200, timeout=3.0)
pass


def test1():
    for i in range(100):
        port.write(str.encode(f"2,{i},100,0,0#"))
        port.write(str.encode("show#"))
        time.sleep(.01)
    time.sleep(1)
    for i in range(100):
        port.write(str.encode(f"3,{i},0,100,0#"))
        port.write(str.encode("show#"))
        time.sleep(.01)
    time.sleep(1)
    for i in range(100):
        port.write(str.encode(f"4,{i},0,0,100#"))
        port.write(str.encode("show#"))
        time.sleep(.01)
    time.sleep(1)
    for i in range(100):
        port.write(str.encode(f"5,{i},50,50,50#"))
        port.write(str.encode("show#"))
        time.sleep(.01)
    testTop()
    return True


def treeOff():
    for i in range(50):
        port.write(str.encode(f"1,{i},200,0,0#"))
        port.write(str.encode("show1#"))
        time.sleep(.07)
    time.sleep(1)

    for i in range(50):
        port.write(str.encode(f"1,{i},0,0,0#"))
        port.write(str.encode("show1#"))
        time.sleep(.07)
    return True


def testTop():
    for i in range(114):
        port.write(str.encode(f"1,{i},100,0,0#"))
        port.write(str.encode("show1#"))
        time.sleep(.01)
    time.sleep(5)
    for i in range(114):
        port.write(str.encode(f"1,{i},0,100,0#"))
        port.write(str.encode("show1#"))
        time.sleep(.01)
    time.sleep(5)
    for i in range(114):
        port.write(str.encode(f"1,{i},0,0,100#"))
        port.write(str.encode("show1#"))
        time.sleep(.01)
    time.sleep(5)
    port.write(str.encode("clear1#"))
    port.write(str.encode("show1#"))
    return True
