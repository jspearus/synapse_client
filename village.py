import datetime, time
from multiprocessing import Process
import sys, io
import random
import platform
import serial
from serial.serialutil import Timeout

if platform.system() == "Linux":
    port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)
elif platform.system() == "Windows":
    port = serial.Serial("COM15", baudrate=115200, timeout=3.0)
else:
    pass

def out_ctrl(outlet, state):
    port.write(str.encode(f"out{outlet}{state}#"))
    
def gen_rand_seq():
    sequence = list(range(1, 9))
    random.shuffle(sequence)
    return sequence

def village_on():
    houses = gen_rand_seq()
    w_time = random.sample(range(2, 10), 1)
    time.sleep(w_time[0])
    for house in houses:
        out_ctrl(house, "on")
        w_time = random.sample(range(0, 20), 1)
        time.sleep(w_time[0])
    return True

def village_off():
    houses = gen_rand_seq()
    w_time = random.sample(range(2, 10), 1)
    time.sleep(w_time[0])
    for house in houses:
        out_ctrl(house, "off")
        w_time = random.sample(range(0, 20), 1)
        time.sleep(w_time[0])
    return True
        
def village_on_quick():
    houses = gen_rand_seq()
    for house in houses:
        out_ctrl(house, "on")
        time.sleep(.5)
    return True

def village_off_quick():
    houses = gen_rand_seq()
    for house in houses:
        out_ctrl(house, "off")
        time.sleep(.5)
    return True   

if __name__ == "__main__":
    village_on_quick()
    time.sleep(5)
    village_off_quick()
