import json, socket
import threading, time
from datetime import datetime
from datetime import timedelta
import os, sys
import json
from pathlib import Path

from general import runPowerOn, runPowerOff
from street_lights import runLightsOn, runLightsOff, runLightsOnQuick
from street_lights import runTreesOn, runTreesOnQuick, runTreesOff

connected = True
name = ''
mOffHour, mOffMin = 22, 00
hour, minute = 16, 30
sunSet2_Offset = 20
monitor_status = False
lights_status = False
trees_status = False
autoOn = True
current_weather = ""
current_datetime = datetime.now()
current_day = current_datetime - timedelta(days=1)
sunset_time = current_datetime.replace(hour=hour, minute=minute)
sunset_time_2 = current_datetime.replace(hour=hour, minute=minute+sunSet2_Offset)
MonOff_time = current_datetime.replace(hour=mOffHour, minute=mOffMin)

def main():
    os.system("video-wallpaper.sh --start ~/Videos/snow.mp4")
    print(f"Connected as: {name} @ {time.ctime()}")
    # time.sleep(2)
    # inputThead = threading.Thread(target=useInput, args=())
    # inputThead.setDaemon(True)
    # inputThead.start()
    # time.sleep(3)
    #todo uncomment to get weather updates
    # weatherThead = threading.Thread(target=check_weather, args=())
    # weatherThead.setDaemon(True)
    # weatherThead.start()
    # time.sleep(3)
    sunsetThead = threading.Thread(target=check_new_day, args=())
    sunsetThead.setDaemon(True)
    sunsetThead.start()
    time.sleep(3)
    monitorThead = threading.Thread(target=monitor_control, args=())
    monitorThead.setDaemon(True)
    monitorThead.start()
    runTreesOn()
    
    #########################################################################

def check_weather():
    global connected
    time.sleep(15)
    while connected:
        time.sleep(120)
 #####################################################################
def check_new_day(): #runs in thread
    global connected, current_day
    time.sleep(20)
    print("New Day Updater Running...")
    while connected:
        if current_day.day != datetime.now().day:
            current_day = datetime.now()
        time.sleep(90)
###############################################################3
        
def monitor_control(): # runs in thread
    global monitor_status, autoOn, lights_status, trees_status
    global connected, sunset_time, MonOff_time, sunset_time_2
    global hour, minute
    time.sleep(10) 
    print(f"Monitor Control {connected}")
    while connected:
        print(f"Running {connected}")
        current_time = datetime.now()
        sunset_time = sunset_time.replace(day=current_time.day)
        sunset_time_2 = sunset_time_2.replace(day=current_time.day)
        MonOff_time = MonOff_time.replace(day=current_time.day)
        if current_time > MonOff_time and monitor_status == True and autoOn == True:
            runPowerOff()
            runLightsOff()
            runTreesOff()
            monitor_status = False
            lights_status = False
            trees_status = False
            
        elif current_time > sunset_time and current_time < MonOff_time and monitor_status == False and autoOn == True:
            runPowerOn()
            monitor_status = True
        
        elif current_time > sunset_time_2 and current_time < MonOff_time and lights_status == False and autoOn == True:
            runLightsOn()
            lights_status = True
            time.sleep(10)
            runTreesOn()
            trees_status = True
        
        print(f"Sunset time: {sunset_time}, MonOff time: {MonOff_time}")
        print(f"Current time: {current_time}, Sunset time_2: {sunset_time_2}")
        print(f"Auto: {autoOn}, monitor status: {monitor_status}, Trees status: {trees_status}, Lights status: {lights_status}")
        print("end")
        time.sleep(30)

def useInput():
    global connected
    time.sleep(2)
    dest = "" 
    while connected:
        dest = input("enter DEST (q to close): ")
        if dest == 'q':
            os.system("video-wallpaper.sh --stop")
            connected = False
            print("Disconecting...")
            time.sleep(1)
            print("Closing...")
        else:
            smsg = input("enter msg (q to close): ")
            if smsg == 'q':
                os.system("video-wallpaper.sh --stop")
                connected = False
                print("Disconecting...")
                time.sleep(1)
                print("Closing...")
            else:                  
                time.sleep(.3)
                
def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)          
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    
if __name__ == "__main__":
    main()