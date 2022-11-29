
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
    time.sleep(10)
    port.write(str.encode("tOnq#"))
    
def power_on_quick():
    port.write(str.encode("sOnq#"))
    time.sleep(5)
    port.write(str.encode("tOnq#"))
    
def power_off():
    port.write(str.encode("sOff#"))
    time.sleep(10) 
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
