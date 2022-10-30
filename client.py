import websocket
import json
import threading, time
import sys
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


def on_close(wsapp, close_status_code, close_msg):
    # print('disconnected from server')
    print("Retry : %s" % time.ctime())
    time.sleep(10)
    __create_ws()  # retry per 10 seconds
    
def on_error(wsapp, error):
    print(error)


def on_message(wsapp, message):
    msg = json.loads(message)
    if msg['destination'] == name or msg['destination'] == "all":
        print(f"msg: {msg['message']}")
        print("enter DEST (q to close): ")

        if msg['message'] == 'Halloween':
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
            
        elif msg['message'].lower() == "snow":
            file = "/home/jeff/Videos/snow.mp4"
            os.system("mplayer -fs  " + file)
        
        elif msg['message'].lower() == "rain":
            file = "/home/jeff/Videos/rain.mp4"
            os.system("mplayer -fs  " + file)
            
        elif msg['message'].lower() == "fog":
            file = "/home/jeff/Videos/fog.mp4"
            os.system("mplayer -fs  " + file)


def __create_ws():
    global wsapp
    global connected
    while connected:
        try:
            websocket.enableTrace(False)
            wsapp = websocket.WebSocketApp("ws://synapse.viewdns.net:8000/ws/test/?",
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
        print("Reconnecting websocket  after 10 sec")
        time.sleep(10)

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
    send_msg("holiday", name)
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
        __create_ws()
    except Exception as err:
        print(err)
        print("connect failed")
