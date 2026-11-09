
from multiprocessing import Process
import logging
import platform, time
import serial


def _send_command(command):
    if platform.system() == "Linux":
        port_name = "/dev/ttyACM1"
    elif platform.system() == "Windows":
        port_name = "COM15"
    else:
        raise RuntimeError(f"Unsupported platform: {platform.system()}")

    try:
        with serial.Serial(port_name, baudrate=115200, timeout=3.0) as port:
            port.write(command.encode())
    except serial.SerialException as exc:
        logging.error("Could not send serial command %r through %s: %s", command, port_name, exc)


def lights_on():
    _send_command("sOnf#")
    
def lights_on_quick():
    _send_command("sOnq#")
    
def lights_off():
    _send_command("sOfff#")
    
def trees_on():
    _send_command("tOnq#")
    
def trees_on_quick():
    _send_command("tOnq#")
    
def trees_off():
    _send_command("tOff#")
    
      

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