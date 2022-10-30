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


def send_msg(mssg, dest):
    msg = {'message': mssg,
           'username': name,
           'destination': dest}
    jmsg = json.dumps(msg)
    wsapp.send(jmsg)
    print(f"Sent: {msg}")


def on_open(wsapp):
    print(f"Connected as: {name}")
    inputThead = threading.Thread(target=useInput, args=())
    inputThead.setDaemon(True)
    inputThead.start()


def on_close(wsapp):
    # print('disconnected from server')
    print("Retry : %s" % time.ctime())
    time.sleep(10)
    connect_websocket()  # retry per 10 seconds


def on_message(wsapp, message):
    msg = json.loads(message)
    if msg['destination'] == name or msg['destination'] == "all":
        print(f"Rec: {message}")
        print(f"msg: {msg['message']}")
        print("enter DEST (q to close): ")

        if msg['message'] == 'Halloween':
            print("good")
            os.system(
                "gsettings set org.gnome.desktop.background picture-uri file:////home/jeff/Pictures/halloween.jpg")

        elif msg['message'] == 'Thanksgiving':
            os.system(
                "gsettings set org.gnome.desktop.background picture-uri file:////home/jeff/Pictures/thanksgiving.jpg")

        elif msg['message'] == 'Christmas Day':
            os.system(
                "gsettings set org.gnome.desktop.background picture-uri file:////home/jeff/Pictures/christmas.jpg")

        elif msg['message'] == "New Year's Day":
            os.system(
                "gsettings set org.gnome.desktop.background picture-uri file:////home/jeff/Pictures/newyear.jpg")
        elif msg['message'] == "snow":
            file = "/home/jeff/Videos/snow.mp4"
            os.system("mplayer -fs  " + file)
            # os.system("sudo amixer cset numid=3 0%")


def connect_websocket():
    global wsapp
    wsapp = websocket.WebSocketApp("ws://synapse.viewdns.net:8000/ws/test/?",
                                   header={
                                       "username": name,
                                       "message": "connected",
                                       "destination": "server"
                                   },
                                   on_message=on_message,
                                   on_close=on_close,
                                   on_open=on_open,)
    wst = threading.Thread(target=wsapp.run_forever())
    wst.daemon = True
    wst.start()


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


def useInput():
    global connected
    time.sleep(2)
    dest = ""
    send_msg("connected", dest)
    while connected:
        dest = input("enter DEST (q to close): ")
        if dest == 'q':
            print("Disconecting...")
            send_msg("close", dest)
            time.sleep(1)
            wsapp.close()
            connected = False
            print("Closed...")
        else:
            smsg = input("enter msg (q to close): ")
            if smsg == 'q':
                print("Disconecting...")
                send_msg("close", dest)
                time.sleep(1)
                wsapp.close()
                connected = False
                print("Closed...")
            else:
                send_msg(smsg, dest)
                time.sleep(.3)


if __name__ == "__main__":
    try:
        connect_websocket()
    except Exception as err:
        print(err)
        print("connect failed")
