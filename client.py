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


def on_close(wsapp):
    print('disconnected from server')
    print("Retry : %s" % time.ctime())
    time.sleep(10)
    connect_websocket()  # retry per 10 seconds


def on_message(wsapp, message):
    msg = json.loads(message)
    if msg['destination'] == name or msg['destination'] == "all":
        print(f"Rec: {message}")
        print("enter DEST (q to close): ")


def connect_websocket():
    global wsapp
    wsapp = websocket.WebSocketApp("ws://synapse.viewdns.net:8000/ws/test/?",
                                   header={
                                       "username": name,
                                       "message": "connected",
                                       "destination": " "
                                   },
                                   on_message=on_message,
                                   on_close=on_close,
                                   on_open=on_open,)
    wst = threading.Thread(target=wsapp.run_forever())
    wst.daemon = True
    wst.start()


def __create_ws(self):
    while True:
        try:
            websocket.enableTrace(False)
            self.__WSCONNECTION = websocket.WebSocketApp(url,
                                                         on_message=self.__on_message,
                                                         on_error=self.__on_error,
                                                         on_close=self.__on_close,
                                                         header=self.header)
            self.__WSCONNECTION.on_open = self.__on_open
            self.__WSCONNECTION.run_forever(
                skip_utf8_validation=True, ping_interval=10, ping_timeout=8)
        except Exception as e:
            gc.collect()
            log.debug("Websocket connection Error  : {0}".format(e))
        log.debug("Reconnecting websocket  after 5 sec")
        time.sleep(5)


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
