
from multiprocessing import Process
import platform
import serial
from serial.serialutil import Timeout

port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)
if platform.system() == "Linux":
    port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)
elif platform.system() == "Windows":
    port = serial.Serial("COM15", baudrate=115200, timeout=3.0)
pass


def power_on():
    port.write(str.encode("pOn#"))

def power_off():
    port.write(str.encode("pOff#"))   

def runPowerOn():
    tProc = Process(target=power_on, args=())
    tProc.start()   

def runPowerOff():
    tProc = Process(target=power_off, args=())
    tProc.start()
