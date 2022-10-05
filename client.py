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

connected = True
name = ''


def send_msg(mssg):
    msg = {'message': mssg,
           'username': name, 'destination': 'server'}
    jmsg = json.dumps(msg)
    wsapp.send(jmsg)
    print(f"Sent: {msg}")


def on_message(wsapp, message):
    msg = json.loads(message)
    if msg['destination'] == name or msg['destination'] == "all":
        print(f"Rec: {message}")


wsapp = websocket.WebSocketApp("ws://synapse.viewdns.net:8000/ws/test/?",
                               header={
                                   "username": name,
                                   "message": "connected",
                                   "destination": "server"
                               },
                               on_message=on_message)


# todo EDIT NAME.TXT TO THE NAME OF DEVICE
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
    # todo figure out why the client needs to be restarted when name is assigned
#########################################################################
print(f"Connected as: {name}")


def useInput():
    global connected
    time.sleep(2)
    send_msg("connected")
    while connected:
        smsg = input("enter msg (q to close): ")
        if smsg == 'q':
            print("Disconecting...")
            send_msg("close")
            time.sleep(1)
            wsapp.close()
            connected = False
            print("Closed...")
        else:
            send_msg(smsg)
            time.sleep(.3)


inputThead = threading.Thread(target=useInput, args=())
inputThead.setDaemon(True)
inputThead.start()

wsapp.run_forever()
