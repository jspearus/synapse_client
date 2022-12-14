
import os, time
from numpy import random

from grinch import runGrinch
from wreath import runWreath
from ball import runBall
from pumpkin import runPumpkin
from ghost import runGhost
from snow import runSnowman, runSnow, runSnowflake
from bells import runBells
from general import runTree, runtest1, runInit, runCloak, runLoad
from velctrl import runLeftTurn, runRightTurn




def randomEvent():
    event = random.randint(7, size=(1))
    # print(event)
    if event == 0:
        run_command('snowman1')
    elif event == 1:
        run_command('grinch')
    elif event == 2:
        run_command('carol')
    elif event == 3:
        randomWhatsThis()
    elif event == 4:
        randomPolar()
    elif event == 5:
        run_command('snow')
    elif event == 6:
        randomPolar()

def randomWhatsThis():
    event = random.randint(3, size=(1))
    # print(event)
    if event == 0:
        file = "/home/pi/Videos/wahtsthis1.mp4"
        runSnow()
        os.system("vlc  " + file)
    elif event == 1:
        file = "/home/pi/Videos/wahtsthis2.mp4"
        runSnow()
        os.system("vlc  " + file)
    elif event == 2:
        file = "/home/pi/Videos/wahtsthis3.mp4"
        runSnow()
        os.system("vlc  " + file)

def randomPolar():
    event = random.randint(2, size=(1))
    # print(event)
    if event == 0:
        file = "/home/pi/Videos/polar1.mp4"
        runSnow()
        os.system("vlc  " + file)
    elif event == 1:
        file = "/home/pi/Videos/polar2.mp4"
        runSnow()
        os.system("vlc  " + file)

def randomClaws():
    event = random.randint(6, size=(1))
    # print(event)
    if event == 0:
        file = "/home/pi/Videos/sandyclaws1.mp4"
        runSnow()
        os.system("vlc  " + file)
    elif event == 1:
        file = "/home/pi/Videos/sandyclaws2.mp4"
        runSnow()
        os.system("vlc  " + file)
    elif event == 2:
        file = "/home/pi/Videos/sandyclaws3.mp4"
        runSnow()
        os.system("vlc  " + file)
    elif event == 3:
        file = "/home/pi/Videos/sandyclaws4.mp4"
        runSnow()
        os.system("vlc  " + file)
    elif event == 4:
        file = "/home/pi/Videos/sandyclaws5.mp4"
        runSnow()
        os.system("vlc  " + file)
    elif event == 5:
        file = "/home/pi/Videos/sandyclaws6.mp4"
        runSnow()
        os.system("vlc  " + file)
    
def run_command(command):
################################################# COMMANDS ######################################
    if command == 'init':
        file = "/home/pi/Videos/bootup.mp4"
        runtest1()
        os.system("vlc  " + file)
    
    elif command == 'loud':
        os.system("sudo amixer cset numid=3 100%")
        file = "/home/pi/Music/division_completed.mp3"
        runLoad()
        os.system("vlc  " + file)
        
    elif command == 'med':
        os.system("sudo amixer cset numid=3 50%")
        file = "/home/pi/Music/division_completed.mp3"
        runLoad()
        os.system("vlc  " + file)
            
    elif command == 'mute':
        file = "/home/pi/Music/the_division_pulse.mp3"
        runCloak()
        os.system("vlc  " + file)
        os.system("sudo amixer cset numid=3 0%")
        
    elif command == 'left#':
        runLeftTurn()
    
    elif command == 'right#':
        runRightTurn()
        
    elif command == 'hleft#':
        runGhost()
    
    elif command == 'hright#':
        runPumpkin()
        
######################################## VIDEOS ###################################################  
        
    elif command == 'grinch':
        file = "/home/pi/Videos/Grinch.mp4"
        runGrinch()
        os.system("vlc  " + file)
    
    elif command == 'snowman':
        file = "/home/pi/Videos/snowman.mp4"
        runSnowman()
        os.system("vlc  " + file)
        
    elif command == 'snowman2':
        file = "/home/pi/Videos/snowman2.mp4"
        runSnowman()
        os.system("vlc  " + file)
        
    elif command == 'snow':
        file = "/home/pi/Videos/snowing.mp4"
        runSnow()
        os.system("vlc  " + file)
    
    elif command == 'vader':
        file = "/home/pi/Videos/CarolofTheBellsVader.mp4"
        runBells()
        os.system("vlc  " + file)
        
    elif command == 'carol':
        file = "/home/pi/Videos/CarolofTheBellsMedel.mp4"
        runBells()
        os.system("vlc  " + file)
    
    elif command == 'polar':
        file = "/home/pi/Videos/polar1.mp4"
        runSnowflake()
        runSnow()
        runSnow()
        os.system("vlc  " + file)
        
    elif command == 'polar2':
        file = "/home/pi/Videos/polar2.mp4"
        runSnow()
        runSnowflake()
        runSnow()
        os.system("vlc  " + file)
        
    elif command == 'what':
        file = "/home/pi/Videos/wahtsthis1.mp4"
        runSnow()
        os.system("vlc  " + file)
        
    elif command == 'random':
        randomEvent()
        
    elif command == 'claws':
        randomClaws()
        
###################################################### ICONS #########################################
    
    elif command == "wreath":
        runWreath()

    elif command == "ball":
        runBall()
        
    elif command == "bell":
        runBells()

    elif command == "ghost":
        runGhost()

    elif command == "snowflake":
        runSnowflake()

    elif command == "pumpkin":
        runPumpkin()
        
    return command