import websocket
import json
import threading
import sys
import time
import sched
import datetime
import os
import json
from pathlib import Path
import platform
from colorama import Fore, Back, Style

from general import runTest1, runTestTop, runTreeOff
from advent import runAdvent
from events import runSnow, runRain
from newyear import runNewYear

connected = True
name = ''
hour = 23
minute = 59
tree_status = False
current_weather = "clear"
current_datetime = datetime.now()
current_datetime = current_datetime - timedelta(days=1)
sunset_time = datetime.now()
TreeOff_time = datetime.now()
TreeOff_time = TreeOff_time.replace(hour=22, minute=00)


# todo update this fucntion every 15 mins
def getHoliday():
    global connected
    global name
    global today
    global weather
    send_msg("holiay", name)
    while connected:
        time.sleep(90)
        if today.day < datetime.datetime.now().day:
            today = datetime.datetime.now()
            send_msg("holiay", name)
            runNewYear()
        if mode != 'off':
            if weather == "snow":
                runSnow()

            elif weather == "rain":
                runRain()


def check_weather():
    global connected, name
    while connected:
        send_msg("weather", name)
        time.sleep(120)
#####################################################################


def check_sunset():  # runs in thread
    global connected, current_datetime, name
    while connected:
        send_msg("sunset", name)
        time.sleep(21600)


def tree_control():  # runs in thread
    global tree_status
    global connected, sunset_time, TreeOff_time
    global hour
    global minute
    time.sleep(5)
    while connected:
        current_time = datetime.now()
        sunset_time.replace(day=current_time.day)
        print(f"Sunset time: {sunset_time}, TreeOff time: {TreeOff_time}")
        print(f"Current time: {current_time} tree_status: {tree_status}")
        print("end")
        if current_time > TreeOff_time and tree_status == True:
            runPowerOff()
            tree_status = False
            send_msg(f"Tree: {str(tree_status)}", 'web')

        elif current_time > sunset_time and current_time < TreeOff_time and tree_status == False:
            runPowerOn()
            tree_status = True
            send_msg(f"Tree: {str(tree_status)}", 'web')
        time.sleep(30)


def send_msg(mssg, dest):
    global wsapp
    msg = {'message': mssg,
           'username': name,
           'destination': dest}
    jmsg = json.dumps(msg)
    wsapp.send(jmsg)
    # print(f"Sent: {msg}")


def on_open(wsapp):
    print(f"Connected as: {name} @ {time.ctime()}")
    inputThead = threading.Thread(target=useInput, args=())
    inputThead.setDaemon(True)
    inputThead.start()

    timeThead = threading.Thread(target=getHoliday, args=())
    timeThead.setDaemon(True)
    timeThead.start()

    treeThead = threading.Thread(target=tree_control, args=())
    treeThead.setDaemon(True)
    treeThead.start()


def on_close(wsapp, close_status_code, close_msg):
    global connected
    print('disconnected from server')
    if connected:
        print("Retry : %s" % time.ctime())
        time.sleep(10)
        __create_ws()  # retry per 10 seconds


def on_error(wsapp, error):
    print(error)


def on_message(wsapp, message):
    msg = json.loads(message)
    if msg['destination'] == name or msg['destination'] == "all":
        print(f"Rec: {message}")
        print("enter DEST (q to close): ")


def __create_ws():
    global wsapp
    global connected
    while connected:
        try:
            websocket.enableTrace(False)
            wsapp = websocket.WebSocketApp("ws://synapse.viewdns.net:8000/ws/term/?",
                                           header={
                                               "username": name,
                                               "message": "connected",
                                               "destination": " "
                                           },
                                           on_message=on_message,
                                           on_error=on_error,
                                           on_close=on_close,
                                           )
            wsapp.on_open = on_open
            wsapp.run_forever(
                skip_utf8_validation=True, ping_interval=10, ping_timeout=8)
        except Exception as e:
            print("Websocket connection Error  : {0}".format(e))
        if connected:
            print("Reconnecting websocket  after 10 sec")
            time.sleep(10)


f = Path('name.json')
if f.is_file():
    f = open('name.json')
    data = json.load(f)
    name = data['client']['deviceName']
else:
    val = input("Enter Client Device Name: ")
    data = {"client": {"deviceName": val}}
    with open('name.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    name = name = data['client']['deviceName']
    f.close()

#########################################################################


def useInput():
    global connected
    time.sleep(2)
    dest = ""
    send_msg("connected", dest)
    while connected:
        dest = input("enter DEST (q to close): ")
        if dest == 'q':
            connected = False
            print("Disconecting...")
            send_msg("close", dest)
            time.sleep(1)
            wsapp.close()
            print("Closing...")
        else:
            smsg = input("enter msg (q to close): ")
            if smsg == 'q':
                connected = False
                print("Disconecting...")
                send_msg("close", dest)
                time.sleep(1)
                wsapp.close()
                print("Closing...")
            else:
                send_msg(smsg, dest)
                time.sleep(.3)


if __name__ == "__main__":
    try:
        __create_ws()
    except Exception as err:
        print(err)
        print("connect failed")
