import websocket
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

from commands import run_command

connected = True
name = ''

hour, minute = 16, 30
TreeOn_hour, TreeOn_minute = 6, 0
TreeOff_hour, TreeOff_minute = 22, 0
sunSet2_Offset = 20

tree_status = False
vil_status = False
autoOn = False
current_weather = "clear"
current_datetime = datetime.now()
current_datetime = current_datetime - timedelta(days=1)
sunset_time = datetime.now()
sunset_time = sunset_time.replace(hour=hour, minute=minute)
sunset_time_2 =sunset_time.replace(hour=hour, minute=minute+sunSet2_Offset)
TreeOn_time = datetime.now()
TreeOn_time = current_datetime.replace(hour=TreeOn_hour, minute=TreeOn_minute)
TreeOff_time = datetime.now()
TreeOff_time = TreeOff_time.replace(hour=TreeOff_hour, minute=TreeOff_minute)


def check_weather():
    global connected, name, tree_status
    time.sleep(15)
    while connected:
        if tree_status:
            send_msg("weather", name)
        time.sleep(300)
#####################################################################


def check_new_day():  # runs in thread
    global connected, name
    global  current_datetime
    time.sleep(5)
    while connected:
        if current_datetime.day < datetime.now().day:
            current_datetime = datetime.now()
            send_msg("sunset", name)
            time.sleep(15)
            send_msg("holiday", name)
            if tree_status:
                run_command("advent")
        time.sleep(90)


def tree_control(): # runs in thread
    global tree_status, autoOn, vil_status
    global connected, sunset_time, sunset_time_2, TreeOff_time, TreeOn_time
    while connected:
        current_time = datetime.now()
        if current_time > TreeOff_time and (tree_status == True or vil_status == True) and autoOn == True:
            run_command("alloff")
            tree_status = False
            vil_status = False
            send_msg(f"tree:{str(tree_status)}", 'web')
            time.sleep(.2)
            send_msg(f"vil:{str(vil_status)}", 'web')
            
        elif current_time > sunset_time_2 and current_time < TreeOff_time and vil_status == False and autoOn == True:
            vil_status = True
            run_command("vil")
            send_msg(f"vil:{str(vil_status)}", 'web')

        elif current_time > TreeOn_time and current_time < TreeOff_time and tree_status == False and autoOn == True:
            run_command("mon")
            tree_status = True
            send_msg(f"tree:{str(tree_status)}", 'web')
        print(f"TreeOn: {TreeOn_time}, TreeOff: {TreeOff_time}")
        print(f"SunSet: {sunset_time}, SunSet_2: {sunset_time_2}")
        print(f"Current Time: {current_time}")
        print(f"Auto_status: {autoOn}, tree_status: {tree_status}, village_status: {vil_status}")
        print("end")
        time.sleep(30)


def send_msg(mssg, dest):
    global wsapp, name
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
    
    newDayThead = threading.Thread(target=check_new_day, args=())
    newDayThead.setDaemon(True)
    newDayThead.start()

    treeThead = threading.Thread(target=tree_control, args=())
    treeThead.setDaemon(True)
    treeThead.start()
    
    weatherThead = threading.Thread(target=check_weather, args=())
    weatherThead.setDaemon(True)
    weatherThead.start()
    
    send_msg(f"tree:{str(tree_status)}", 'web')
    time.sleep(1)
    send_msg(f"vil:{str(vil_status)}", 'web')
    time.sleep(1)
    send_msg(f"tauto:{str(autoOn)}", 'web')


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
    global current_weather, sunset_time, sunset_time_2, name, hour, minute
    global tree_status, autoOn, vil_status, sunSet2_Offset, TreeOff_time, TreeOn_time
    global TreeOn_hour, TreeOn_minute, TreeOff_hour, TreeOn_minute
    msg = json.loads(message)
    if msg['destination'] == name or msg['destination'] == "all":
        print(f"Rec: {message}")
        print("enter DEST (q to close): ")

        if"sunset" in msg['message']:
            sunset = msg['message'].split(':')
            hour = (int(sunset[1]) - 6)+12
            minute = int(sunset[2])
            current_time = datetime.now()
            sunset_time = current_time.replace(hour=hour, minute=minute)
            sunset_time_2 = sunset_time_2 = current_time.replace(hour=hour, minute=minute+sunSet2_Offset)
            TreeOff_time = current_time.replace(hour=TreeOff_hour, minute=TreeOff_minute)
            TreeOn_time = current_time.replace(hour=TreeOn_hour, minute=TreeOn_minute)
            print(f"Sunset Time Updated => hour: {hour} : minute: {minute}")
            print("enter DEST (q to close): ")

        elif msg['message'] == 'halloween':
            os.system(
                "pcmanfm --set-wallpaper /home/pi/Pictures/halloween.jpg")

        elif msg['message'] == 'thanksgiving':
            os.system(
                "pcmanfm --set-wallpaper /home/pi/Pictures/thanksgiving.jpg")

        elif msg['message'] == 'christmas day':
            os.system(
                "pcmanfm --set-wallpaper /home/pi/Pictures/christmas.jpg")

        elif msg['message'] == "new year's day":
            os.system(
                "pcmanfm --set-wallpaper /home/pi/Pictures/newyear.jpg")

        elif msg['message'] == "snow":
            if msg['message'] != current_weather:
                current_weather = msg['message']
                send_msg(f"UPDATE: {str(current_weather)}", 'web')
            run_command(msg['message'])
                # os.system("video-wallpaper.sh --start ~/Videos/snow.mp4")

        elif msg['message'] == "rain" and tree_status == True:
            if msg['message'] != current_weather:
                current_weather = msg['message']
                send_msg(f"UPDATE: {str(current_weather)}", 'web')
            run_command(msg['message'])
                # os.system("video-wallpaper.sh --start ~/Videos/rain.mp4")

        elif msg['message'] == "clear" and tree_status == True:
            if msg['message'] != current_weather:
                current_weather = msg['message']
                send_msg(f"UPDATE: {str(current_weather)}", 'web')
                run_command(msg['message'])
                # os.system("video-wallpaper.sh --start ~/Videos/fog.mp4")

        elif msg['message'] == "cloud" and tree_status == True:
            if msg['message'] != current_weather:
                current_weather = msg['message']
                send_msg(f"UPDATE: {str(current_weather)}", 'web')
                run_command(msg['message'])
                # os.system("video-wallpaper.sh --start ~/Videos/fog.mp4")

        elif msg['message'] == "fog" and tree_status == True:
            if msg['message'] != current_weather:
                run_command(msg['message'])
                send_msg(f"UPDATE: {str(current_weather)}", 'web')
                current_weather = msg['message']
                # os.system("video-wallpaper.sh --start ~/Videos/fog.mp4")

        elif msg['message'] == "ping":
            send_msg("pong", "server")
            print(f"msg: {msg['message']}")
            
        elif msg['message'] == "auto":
            autoOn = True
            send_msg(f"tauto:{str(autoOn)}", 'web')
            
        elif msg['message'] == "autooff":
            autoOn = False
            send_msg(f"tauto:{str(autoOn)}", 'web')

        elif msg['message'] == "mon":
            tree_status = True
            run_command(msg['message'])
            send_msg(f"tree:{str(tree_status)}", 'web')

        elif msg['message'] == "moff":
            tree_status = False
            run_command(msg['message'])
            send_msg(f"tree:{str(tree_status)}", 'web')
            
        elif msg['message'] == "alloff":
            tree_status = False
            vil_status = False
            run_command(msg['message'])
            send_msg(f"tree:{str(tree_status)}", 'web')
            time.sleep(.5)
            send_msg(f"vil:{str(vil_status)}", 'web')
            
        elif msg['message'] == "vil":
            vil_status = True
            run_command(msg['message'])
            send_msg(f"vil:{str(vil_status)}", 'web')

        elif msg['message'] == "viloff":
            vil_status = False
            run_command(msg['message'])
            send_msg(f"vil:{str(vil_status)}", 'web')
            
        elif msg['message'] == "vilq":
            vil_status = True
            run_command(msg['message'])
            send_msg(f"vil:{str(vil_status)}", 'web')
            
        elif msg['message'] == "viloffq":
            vil_status = False
            run_command(msg['message'])
            send_msg(f"vil:{str(vil_status)}", 'web')


        elif msg['message'] == "status":
            send_msg(f"tauto:{str(autoOn)}", msg['username'])
            time.sleep(.5)
            send_msg(f"tree:{str(tree_status)}", msg['username'])
            time.sleep(.5)
            send_msg(f"vil:{str(vil_status)}", msg['username'])

        else:
            print(f"msg: {msg['message']}")
            print("enter DEST (q to close): ")
            run_command(msg['message'])


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
