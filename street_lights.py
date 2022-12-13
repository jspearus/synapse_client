
from multiprocessing import Process
import platform, time
import serial
from serial.serialutil import Timeout

if platform.system() == "Linux":
    port = serial.Serial("/dev/ttyACM1", baudrate=115200, timeout=3.0)
elif platform.system() == "Windows":
    port = serial.Serial("COM15", baudrate=115200, timeout=3.0)
pass


def power_on():
    port.write(str.encode("sOn#"))
    
def power_on_quick():
    port.write(str.encode("sOnq#"))
    
def power_off():
    port.write(str.encode("sOff#"))
    
def trees_on():
    port.write(str.encode("tOn#"))
    
def trees_on_quick():
    port.write(str.encode("tOnq#"))
    
def trees_off():
    port.write(str.encode("tOff#"))
    
      

def runLightsOn():
    tProc = Process(target=power_on, args=())
    tProc.start()
    
def runLightsOnQuick():
    tProc = Process(target=power_on_quick, args=())
    tProc.start()  

def runLightsOff():
    tProc = Process(target=power_off, args=())
    tProc.start()
    
def runTreesOn():
    tProc = Process(target=trees_on, args=())
    tProc.start()
    
def runTreesOnQuick():
    tProc = Process(target=trees_on_quick, args=())
    tProc.start()  

def runTreesOff():
    tProc = Process(target=trees_off, args=())
    tProc.start()

