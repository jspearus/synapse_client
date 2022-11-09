import websocket
import json
import threading, time
import sys
import sched
from datetime import datetime
import os
import json
from pathlib import Path
import platform
from colorama import Fore, Back, Style

from general import runPowerOn, runPowerOff

connected = True
name = ''
hour = 23
minute = 59
monitor_status = False
current_weather = "clear"


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
    time.sleep(2)
    inputThead = threading.Thread(target=useInput, args=())
    inputThead.setDaemon(True)
    inputThead.start()
    time.sleep(3)
    weatherThead = threading.Thread(target=check_weather, args=())
    weatherThead.setDaemon(True)
    weatherThead.start()
    time.sleep(3)
    sunsetThead = threading.Thread(target=check_sunset, args=())
    sunsetThead.setDaemon(True)
    sunsetThead.start()
    time.sleep(3)
    monitorThead = threading.Thread(target=monitor_control, args=())
    monitorThead.setDaemon(True)
    monitorThead.start()
    send_msg(f"mon:{str(monitor_status)}", 'web')



def on_close(wsapp, close_status_code, close_msg):
    global connected
    # print('disconnected from server')
    if connected:
        print("Retry : %s" % time.ctime())
        time.sleep(10)
        __create_ws()  # retry per 10 seconds
    
def on_error(wsapp, error):
    print(error)


def on_message(wsapp, message):
    global hour
    global minute
    global monitor_status
    global current_weather
    msg = json.loads(message)
    if msg['destination'] == name or msg['destination'] == "all":
        # print(f"msg: {msg['message']}")
        # print("enter DEST (q to close): ")

        if"sunset" in msg['message']:
            sunset = msg['message'].split(':')
            hour = int(sunset[1]) - 6
            minute = int(sunset[2])
            print(f"hour: {hour}")
            print(f"minute: {minute}")
            print("enter DEST (q to close): ")
            
        elif msg['message'] == 'halloween':
            os.system(
                "gsettings set org.gnome.desktop.background picture-uri file:////home/jeff/Pictures/halloween.jpg")

        elif msg['message'] == 'thanksgiving':
            os.system(
                "gsettings set org.gnome.desktop.background picture-uri file:////home/jeff/Pictures/thanksgiving.jpg")

        elif msg['message'] == 'christmas day':
            os.system(
                "gsettings set org.gnome.desktop.background picture-uri file:////home/jeff/Pictures/christmas.jpg")

        elif msg['message'] == "new year's day":
            os.system(
                "gsettings set org.gnome.desktop.background picture-uri file:////home/jeff/Pictures/newyear.jpg")
            
        elif msg['message']== "snow":
            # file = "/home/jeff/Videos/snow.mp4"
            # os.system("mplayer -fs  " + file)
            if msg['message'] != current_weather:
                current_weather = msg['message']
                os.system("video-wallpaper.sh --start ~/Videos/snow.mp4")
        
        elif msg['message'] == "rain":
            # file = "/home/jeff/Videos/rain.mp4"
            # os.system("mplayer -fs  " + file)
            if msg['message'] != current_weather:
                current_weather = msg['message']
                os.system("video-wallpaper.sh --start ~/Videos/rain.mp4")
        
        elif msg['message'] == "clear":
            # file = "/home/jeff/Videos/rain.mp4"
            # os.system("mplayer -fs  " + file)
            if msg['message'] != current_weather:
                current_weather = msg['message']
                os.system("video-wallpaper.sh --stop")
        
        elif msg['message'] == "cloud":
            # file = "/home/jeff/Videos/fog.mp4"
            # os.system("mplayer -fs  " + file)
            if msg['message'] != current_weather:
                current_weather = msg['message']
                os.system("video-wallpaper.sh --start ~/Videos/fog.mp4")
                
        elif msg['message'] == "fog":
            # file = "/home/jeff/Videos/fog.mp4"
            # os.system("mplayer -fs  " + file)
            if msg['message'] != current_weather:
                current_weather = msg['message']
                os.system("video-wallpaper.sh --start ~/Videos/fog.mp4")
            
        elif msg['message']== "ping":
            send_msg("pong", "server")
            print(f"msg: {msg['message']}")
            
        elif msg['message']== "mon":
            monitor_status = True
            runPowerOn()
            send_msg(f"mon:{str(monitor_status)}", 'web')
            
        elif msg['message']== "moff":
            monitor_status = False
            runPowerOff()
            send_msg(f"mon:{str(monitor_status)}", 'web')
            
        elif msg['message']== "status":
            send_msg(f"mon:{str(monitor_status)}", 'web')
            
        else:
            print(f"msg: {msg['message']}")
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

def check_weather():
    global connected
    while connected:
        send_msg("weather", "foyer")
        time.sleep(120)
        
def check_sunset():
    global connected
    while connected:
        send_msg("sunset", "foyer")
        time.sleep(43200)
        
def monitor_control():
    global monitor_status
    global connected
    global hour
    global minute
    while connected:
        current_time = datetime.now()
        print(f"Sunset time: hour-{hour+12} min-{minute}")
        print(f"Current time: {current_time} monitor status: {monitor_status}")
        if current_time.hour > 19 and monitor_status == True:
            runPowerOff()
            monitor_status = False
            send_msg(f"mon:{str(monitor_status)}", 'web')
            
        elif current_time.hour > hour+12 and current_time.hour < 19 and monitor_status == False:
            runPowerOn()
            monitor_status = True
            send_msg(f"mon:{str(monitor_status)}", 'web')
        time.sleep(20)

def useInput():
    global connected
    time.sleep(2)
    dest = ""
    send_msg("connected", dest)
    send_msg("holiday", name)
    while connected:
        dest = input("enter DEST (q to close): ")
        if dest == 'q':
            os.system("video-wallpaper.sh --stop")
            connected = False
            print("Disconecting...")
            send_msg("close", dest)
            time.sleep(1)
            wsapp.close()
            print("Closing...")
        else:
            smsg = input("enter msg (q to close): ")
            if smsg == 'q':
                os.system("video-wallpaper.sh --stop")
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
