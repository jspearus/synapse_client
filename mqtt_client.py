#!/usr/bin/env python3

import socket
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
# from screen import refreshScreen
from colorama import Fore, Back, Style
import paho.mqtt.client as mqtt

from commands import run_command
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

connected = True
name = ''

MorningOn_hour, MorningOn_minute = 4, 00
TreeOn_hour, TreeOn_minute = 7, 30
TreeOff_hour, TreeOff_minute = 22, 0
hour, minute = 16, 30
sunSet2_Offset = 20

tree_status = False
morning_status = False
vil_status = False
autoOn = True
current_weather = "clear"
current_datetime = datetime.now()
current_day = current_datetime - timedelta(days=1)
sunset_time = current_datetime.replace(hour=hour, minute=minute)
sunset_time_2 =current_datetime.replace(hour=hour, minute=minute+sunSet2_Offset)
TreeOn_time = current_datetime.replace(hour=TreeOn_hour, minute=TreeOn_minute)
MorningOn_time = current_datetime.replace(hour=MorningOn_hour, minute=MorningOn_minute)
TreeOff_time = current_datetime.replace(hour=TreeOff_hour, minute=TreeOff_minute)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("Lv Tree")
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload).strip())
    if "tree off" in str(msg.payload).strip():
        run_command("moff")
        client.publish("LvTree_feedback", payload="Tree Off", qos=1, retain=False)
        
    elif "tree on mthanks" in str(msg.payload).strip():
        run_command("mthanks")
        client.publish("LvTree_feedback", payload="Tree On", qos=1, retain=False)
        
    elif "tree on thanks" in str(msg.payload).strip():
        run_command("thanks")
        client.publish("LvTree_feedback", payload="Tree On", qos=1, retain=False)
    
    elif "tree on mn" in str(msg.payload).strip():
        run_command("mnew")
        client.publish("LvTree_feedback", payload="Tree On", qos=1, retain=False)
        
    elif "tree on new" in str(msg.payload).strip():
        run_command("new")
        client.publish("LvTree_feedback", payload="Tree On", qos=1, retain=False)
        
    elif "tree on m" in str(msg.payload).strip():
        check_new_day('m')
        client.publish("LvTree_feedback", payload="Tree On", qos=1, retain=False)
        
    elif "tree on" in str(msg.payload).strip():
        check_new_day('d')
        client.publish("LvTree_feedback", payload="Tree On", qos=1, retain=False)
        
    elif "village on q" in str(msg.payload).strip():
        run_command("vilq")
        client.publish("LvTree_feedback", payload="Village On", qos=1, retain=False)
    
    elif "village on" in str(msg.payload).strip():
        run_command("vil")
        client.publish("LvTree_feedback", payload="Village On", qos=1, retain=False)
        
    elif "village off q" in str(msg.payload).strip():
        run_command("viloffq")
        client.publish("LvTree_feedback", payload="Village Off", qos=1, retain=False)
        
    elif "village off" in str(msg.payload).strip():
        run_command("viloff")
        client.publish("LvTree_feedback", payload="Village Off", qos=1, retain=False)
        
    elif "All On q" in str(msg.payload).strip():
        run_command("advent")
        time.sleep(5)
        run_command("vilq")
        client.publish("LvTree_feedback", payload="All On q", qos=1, retain=False)
        
    elif "All On" in str(msg.payload).strip():
        run_command("advent")
        time.sleep(5)
        run_command("vil")
        client.publish("LvTree_feedback", payload="All On", qos=1, retain=False)
    
        
    elif "All Off q" in str(msg.payload).strip():
        run_command("moff")
        time.sleep(5)
        run_command("viloffq")
        client.publish("LvTree_feedback", payload="All Off", qos=1, retain=False)
        
    elif "All Off" in str(msg.payload).strip():
        run_command("moff")
        time.sleep(5)
        run_command("viloff")
        client.publish("LvTree_feedback", payload="All Off", qos=1, retain=False)
        
    elif "fire" in str(msg.payload).strip():
        run_command("fire")
        client.publish("LvTree_feedback", payload="FireWorks", qos=1, retain=False)
        
    #todo code execute here
    
def main():
    global connected
    print(f"Connected as: {name} @ {time.ctime()}")
    # os.system("video-wallpaper.sh --start ~/Videos/snow.mp4")
    print(f"Connected as: {name} @ {time.ctime()}")
    client = mqtt.Client(protocol=mqtt.MQTTv311)  # Optionally set the protocol
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set("mqtt-user", "yqhevr")
    client.connect("192.168.1.155", 1883, 60)
    
    # inputThead = threading.Thread(target=useInput, args=())
    # # inputThead.setDaemon(True)
    # inputThead.start()
    
    # newDayThead = threading.Thread(target=check_new_day, args=())
    # # newDayThead.setDaemon(True)
    # newDayThead.start()

    # treeThead = threading.Thread(target=tree_control, args=())
    # # treeThead.setDaemon(True)
    # treeThead.start()
    
    # weatherThead = threading.Thread(target=check_weather, args=())
    # # weatherThead.setDaemon(True)
    # weatherThead.start()
    client.loop_forever()
    if connected == False:
        client.loop_stop()

    
#########################################################################
def check_weather():    # runs in thread
    global connected, name, tree_status
    time.sleep(15)
    while connected:
        if tree_status:
            pass
        time.sleep(300)
#####################################################################


def check_new_day(mode):  # runs in thread
    cur_day = datetime.now()
    print(f"Current Day: {cur_day.day}")
    print(f"Current Month: {cur_day.month}")
    if mode == 'm':
        if cur_day.month == 10:
            print("Mode: M Thanks")
            run_command('mthanks')
        elif cur_day.month == 12 and cur_day.day < 26:
            print("Mode: M Advent")
            run_command('madvent')
        elif (cur_day.month == 12 and cur_day.day > 25) or cur_day.month == 1:
            print("Mode: M New Years")
            run_command('mnew')    
            
    elif mode == 'd':
        if cur_day.month == 10:
            print("Mode: D Thanks")
            run_command('thanks')
        elif cur_day.month == 12 and cur_day.day < 26:
            print("Mode: D Advent")
            run_command('advent')
        elif (cur_day.month == 12 and cur_day.day > 25) or cur_day.month == 1:
            print("Mode: D New Years")
            run_command('new') 
        
########################################################################

def tree_control(): # runs in thread
    global tree_status, autoOn, vil_status, MorningOn_time, morning_status
    global connected, sunset_time, sunset_time_2, TreeOff_time, TreeOn_time
    time.sleep(20) 
    while connected:
        current_time = datetime.now()
        sunset_time = sunset_time.replace(day=current_time.day)
        sunset_time_2 = sunset_time_2.replace(day=current_time.day)
        MorningOn_time = MorningOn_time.replace(day=current_time.day)
        TreeOn_time = TreeOn_time.replace(day=current_time.day)
        TreeOff_time = TreeOff_time.replace(day=current_time.day)
        if current_time > TreeOff_time and (tree_status == True or vil_status == True) and autoOn == True:
            run_command("alloff")
            tree_status = False
            vil_status = False
            time.sleep(.2)
            
        elif current_time > sunset_time_2 and current_time < TreeOff_time and vil_status == False and autoOn == True:
            vil_status = True
            run_command("vil")

        elif current_time > TreeOn_time and current_time < TreeOff_time and tree_status == False and autoOn == True:
            run_command("mon")
            tree_status = True
            morning_status = False
            
        elif current_time > MorningOn_time and current_time < TreeOn_time and morning_status == False and autoOn == True:
            run_command("madvent")
            morning_status = True
            
            
        # print(f"TreeOn: {TreeOn_time}, TreeOff: {TreeOff_time}")
        # print(f"SunSet: {sunset_time}, SunSet_2: {sunset_time_2}")
        # print(f"C Time: {current_time}, Morn_On: {MorningOn_time}")
        # print(f"Auto_status: {autoOn}, morning_status: {morning_status}, tree_status: {tree_status}, village_status: {vil_status}")
        # print("end")
        time.sleep(30)


def useInput():
    global connected
    time.sleep(2)
    dest = ""
    while connected:
        dest = input("enter DEST (q to close): ")
        if dest == 'q':
            connected = False
            print("Disconecting...")
            time.sleep(1)
            print("Closing...")
            
        elif dest == 'on':
            run_command("advent")
            
        elif dest == 'onNew':
            run_command("new")
        
        elif dest == 'off':
            run_command("moff")
            run_command("viloffq")
            
        elif dest == 'village':
            run_command("vilq")
        else:
            smsg = input("enter msg (q to close): ")
            if smsg == 'q':
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
    # refreshScreen()
    main()