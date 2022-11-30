import websocket
import json
import threading, time
from datetime import datetime
from datetime import timedelta
import os
import json
from pathlib import Path

from general import runPowerOn, runPowerOff
from street_lights import runLightsOn, runLightsOff, runLightsOnQuick

connected = True
name = ''
mOffHour, mOffMin = 22, 00
sunSet2_Offset = 20
monitor_status = False
lights_status = False
autoOn = False
current_weather = ""
current_datetime = datetime.now()
current_datetime = current_datetime - timedelta(days=1)
sunset_time_2 = datetime.now()
sunset_time = datetime.now()
MonOff_time = datetime.now()
MonOff_time = MonOff_time.replace(hour=mOffHour, minute=mOffMin)


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
    send_msg(f"mon:{str(monitor_status)}", 'web')
    time.sleep(.3)
    send_msg(f"cauto:{str(autoOn)}", 'web')
    time.sleep(.3)
    send_msg(f"lights:{str(lights_status)}", 'web')
    os.system("video-wallpaper.sh --start ~/Videos/snow.mp4")



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
    global hour, minute, mOffHour, mOffMin, sunset_time_2
    global monitor_status, sunset_time, MonOff_time, current_datetime
    global current_weather, autoOn, lights_status, sunSet2_Offset
    msg = json.loads(message)
    if msg['destination'] == name or msg['destination'] == "all":
        # print(f"msg: {msg['message']}")
        # print("enter DEST (q to close): ")

        if"sunset" in msg['message']:
            sunset = msg['message'].split(':')
            hour = (int(sunset[1]) - 6)+12
            minute = int(sunset[2])
            current_time = datetime.now()
            sunset_time = current_time.replace(hour=hour, minute=minute)
            sunset_time_2 = current_time.replace(hour=hour, minute=minute+sunSet2_Offset)
            MonOff_time = current_time.replace(hour=mOffHour, minute=mOffMin)
            print(f"Sunset Time Updated => hour: {hour} : minute: {minute}")
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
                os.system("video-wallpaper.sh --start ~/Videos/clear.mp4")
        
        elif msg['message'] == "cloud":
            # file = "/home/jeff/Videos/fog.mp4"
            # os.system("mplayer -fs  " + file)
            if msg['message'] != current_weather:
                current_weather = msg['message']
                os.system("video-wallpaper.sh --start ~/Videos/cloud.mp4")
                
        elif msg['message'] == "fog":
            # file = "/home/jeff/Videos/fog.mp4"
            # os.system("mplayer -fs  " + file)
            if msg['message'] != current_weather:
                current_weather = msg['message']
                os.system("video-wallpaper.sh --start ~/Videos/fog.mp4")
            
        elif msg['message']== "ping":
            send_msg("pong", "server")
            print(f"msg: {msg['message']}")
            
        elif msg['message']== "auto":
            autoOn = True
            send_msg(f"cauto:{str(autoOn)}", 'web')
            
        elif msg['message']== "autooff":
            autoOn = False
            send_msg(f"cauto:{str(autoOn)}", 'web')
            
        elif msg['message']== "mon":
            monitor_status = True
            runPowerOn()
            send_msg(f"mon:{str(monitor_status)}", 'web')
            
        elif msg['message']== "moff":
            monitor_status = False
            runPowerOff()
            send_msg(f"mon:{str(monitor_status)}", 'web')
            
        elif msg['message']== "lon":
            lights_status = True
            runLightsOn()
            send_msg(f"lights:{str(lights_status)}", 'web')
            
        elif msg['message']== "lonq":
            lights_status = True
            runLightsOnQuick()
            send_msg(f"lights:{str(lights_status)}", 'web')
            
        elif msg['message']== "loff":
            lights_status = False
            runLightsOff()
            send_msg(f"lights:{str(lights_status)}", 'web')
            
        elif msg['message']== "status":
            send_msg(f"cauto:{str(autoOn)}", msg['username'])
            time.sleep(.5)
            send_msg(f"mon:{str(monitor_status)}", msg['username'])
            time.sleep(.5)
            send_msg(f"lights:{str(lights_status)}", msg['username'])
            
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
#########################################################################

def check_weather():
    global connected, name
    while connected:
        send_msg("weather", name)
        time.sleep(120)
 #####################################################################
def check_new_day(): #runs in thread
    global connected, current_datetime
    global name
    while connected:
        if current_datetime.day < datetime.now().day:
            current_datetime = datetime.now()
            send_msg("sunset", name)
        time.sleep(90)
###############################################################3
        
def monitor_control(): # runs in thread
    global monitor_status, autoOn, lights_status
    global connected, sunset_time, MonOff_time, sunset_time_2
    global hour, minute
    time.sleep(5) 
    while connected:
        current_time = datetime.now()
        sunset_time = sunset_time.replace(day=current_time.day)
        sunset_time_2 = sunset_time_2.replace(day=current_time.day)
        if current_time > MonOff_time and monitor_status == True and autoOn == True:
            runPowerOff()
            runLightsOff()
            monitor_status = False
            lights_status = False
            send_msg(f"mon:{str(monitor_status)}", 'web')
            send_msg(f"lights:{str(lights_status)}", 'web')
            
        elif current_time > sunset_time and current_time < MonOff_time and monitor_status == False and autoOn == True:
            runPowerOn()
            monitor_status = True
            send_msg(f"mon:{str(monitor_status)}", 'web')
        
        elif current_time > sunset_time_2 and current_time < MonOff_time and lights_status == False and autoOn == True:
            runLightsOn()
            lights_status = True
            send_msg(f"lights:{str(lights_status)}", 'web')
        
        print(f"Sunset time: {sunset_time}, MonOff time: {MonOff_time}")
        print(f"Current time: {current_time}, Sunset time_2: {sunset_time_2}")
        print(f"Auto: {autoOn}, monitor status: {monitor_status}, Lights status: {lights_status}")
        print("end")
        time.sleep(30)

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
