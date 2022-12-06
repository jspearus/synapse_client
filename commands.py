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
from advent import advent, morningAdvent

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


def run_command(com):
    commandThread = Process(target=runCommand, args=(com,))
    commandThread.start()
