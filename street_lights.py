
from multiprocessing import Process
import platform, time
import serial
from serial.serialutil import Timeout

port = serial.Serial("/dev/ttyACM1", baudrate=115200, timeout=3.0)
if platform.system() == "Linux":
    port = serial.Serial("/dev/ttyACM1", baudrate=115200, timeout=3.0)
elif platform.system() == "Windows":
    port = serial.Serial("COM15", baudrate=115200, timeout=3.0)
pass


def lights_on():
    port.write(str.encode("sOnf#"))
    
def lights_on_quick():
    port.write(str.encode("sOnq#"))
    
def lights_off():
    port.write(str.encode("sOfff#"))
    
def trees_on():
    port.write(str.encode("tOnq#"))
    
def trees_on_quick():
    port.write(str.encode("tOnq#"))
    
def trees_off():
    port.write(str.encode("tOff#"))
    
      

def runLightsOn():
    tProc = Process(target=lights_on, args=())
    tProc.start()
    
def runLightsOnQuick():
    tProc = Process(target=lights_on_quick, args=())
    tProc.start()  

def runLightsOff():
    tProc = Process(target=lights_off, args=())
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

