import json
import threading
import sys
import time
import sched
from datetime import datetime
from datetime import timedelta
import os
import json
from pathlib import Path
import platform
from colorama import Fore, Back, Style
from multiprocessing import Process

from general import test1, testTop, treeOff
from advent import advent
from events import snow, rain
from newyear import newYear
from village import village_on, village_off, village_on_quick, village_off_quick


comFree = True
debug = True

def runCommand(command):
    global comFree, debug
################################################# COMMANDS ######################################
    if command == 'mon' and comFree == True:
        comFree = False
        comFree = advent()
        if debug:
            print(f"{command}: {comFree}")
        
    elif command == 'moff' and comFree == True:
        comFree = False
        comFree = treeOff()
        if debug:
            print(f"{command}: {comFree}")
        
    elif command == 'snow' and comFree == True:
        comFree = False
        comFree = snow()
        if debug:
            print(f"{command}: {comFree}")
        
    elif command == 'rain' and comFree == True:
        comFree = False
        comFree = rain()
        if debug:
            print(f"{command}: {comFree}")
        
    elif command == 'clear' and comFree == True:
        comFree = False
        comFree = advent()
        if debug:
            print(f"{command}: {comFree}")
    
    elif command == 'cloud' and comFree == True:
        comFree = False
        comFree = advent()
        if debug:
            print(f"{command}: {comFree}")
        
    elif command == 'fog' and comFree == True:
        comFree = False
        comFree = advent()
        if debug:
            print(f"{command}: {comFree}")
        
    elif command == 'advent' and comFree == True:
        comFree = False
        comFree = advent()
        if debug:
            print(f"{command}: {comFree}")
    
    elif command == 'new' and comFree == True:
        comFree = False
        comFree = newYear()
        if debug:
            print(f"{command}: {comFree}")
        
    elif command == 'test' and comFree == True:
        comFree = False
        comFree = test1()
        if debug:
            print(f"{command}: {comFree}")
        
    elif command == 'ttop' and comFree == True:
        comFree = False
        comFree = testTop()
        if debug:
            print(f"{command}: {comFree}")
        
    elif command == 'vil' and comFree == True:
        comFree = False
        comFree = village_on()
        if debug:
            print(f"{command}: {comFree}")
    
    elif command == 'viloff' and comFree == True:
        comFree = False
        comFree = village_off()
        if debug:
            print(f"{command}: {comFree}")
        
    elif command == 'alloff' and comFree == True:
        comFree = False
        temp = village_off()
        time.sleep(1)
        comFree = treeOff()
        if debug:
            print(f"{command}: {comFree}")
        
    elif command == 'vilq' and comFree == True:
        comFree = False
        comFree = village_on_quick()
        print(f"{command}: {comFree}")
        
    elif command == 'viloffq' and comFree == True:
        comFree = False
        comFree = village_off_quick()
        if debug:
            print(f"{command}: {comFree}")
        
def run_command(com):
    commandThread = Process(target=runCommand, args=(com,))
    commandThread.start()