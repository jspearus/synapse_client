
from multiprocessing import Process
import logging
import platform
import serial


def _send_command(command):
    if platform.system() == "Linux":
        port_name = "/dev/ttyACM0"
    elif platform.system() == "Windows":
        port_name = "COM15"
    else:
        raise RuntimeError(f"Unsupported platform: {platform.system()}")

    try:
        with serial.Serial(port_name, baudrate=115200, timeout=3.0) as port:
            port.write(command.encode())
    except serial.SerialException as exc:
        logging.error("Could not send serial command %r through %s: %s", command, port_name, exc)


def power_on():
    _send_command("pOn#")

def power_off():
    _send_command("pOff#")

def runPowerOn():
    tProc = Process(target=power_on, args=())
    tProc.start()   

def runPowerOff():
    tProc = Process(target=power_off, args=())
    tProc.start()
    