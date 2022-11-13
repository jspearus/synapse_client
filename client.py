import websocket
import json
import threading
import sys
import time
from datetime import datetime
import os, platform, serial
import json
from pathlib import Path
# import platform
from colorama import Back, Style

from tkinter import *

from general import runTree, runtest1, runInit, runCloak, runLoad
from commands import run_command

connected = True
init = False
name = ''
auto_mode = False
mode = "none"
today = datetime.now()

root = Tk()

root.configure(background='black')
root.config(cursor="none")
root.title("Holiday Remote")
root.geometry('175x620+820+20')

if platform.system() == "Linux":
    xBee = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)
    xBee.write(str.encode("Remote_Online\n"))
    
def serialRead():
    global connected
    print("xBee Listening...")
    while connected:
        Data = xBee.readline()
        data = str(Data, 'UTF-8')
        data = data.split(' ')
        # serLabel.config(text=data[0])
        if data[0] != "":
            xBee.write(str.encode(f"Command Rec.. {data[0]}\n"))
            run_command(data[0])
        else:
            pass

def on_closing():
    global wsapp
    global connected
    print("Disconecting...")
    send_msg('close', 'q')
    connected = False
    time.sleep(1)
    wsapp.close()
    print("Closing...")
    root.destroy()
    
root.protocol("WM_DELETE_WINDOW", on_closing)  

#######################################################################################



def on_open(wsapp):
    global connected, init
    if not init:
        run_command('init')
        init = True
    print(f"Connected as: {name} @ {time.ctime()}")
    
    inputThead = threading.Thread(target=useInput, args=())
    inputThead.setDaemon(True)
    inputThead.start()
    
    serial = threading.Thread(target=serialRead, args=())
    serial.setDaemon(True)
    serial.start()



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
        if(msg['message'] == 'kill'):
            file = "/home/pi/Music/012SystemImpared.mp3"
            os.system("pcmanfm --set-wallpaper /home/pi/Pictures/base.jpg")
            runLoad()
            os.system("vlc  " + file)
            time.sleep(8)
            on_closing()
        else:
            run_command(msg['message'])


def __create_ws():
    global wsapp
    global connected
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
    return 
            
def send_msg(mssg, dest):
    global wsapp
    msg = {'message': mssg,
           'username': name,
           'destination': dest}
    jmsg = json.dumps(msg)
    wsapp.send(jmsg)
    # print(f"Sent: {msg}")


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
            connected = False
            print("Disconecting...")
            send_msg("close", dest)
            time.sleep(1)
            wsapp.close()
            print("Closing...")
            root.destroy()
        else:
            smsg = input("enter msg (q to close): ")
            if smsg == 'q':
                connected = False
                print("Disconecting...")
                send_msg("close", dest)
                time.sleep(1)
                wsapp.close()
                print("Closing...")
                root.destroy()
            else:
                send_msg(smsg, dest)
                time.sleep(.3)

############################# USER INTERFACE ###################################
def fromUI(data):
    if data == "video":
        controlPanel.place_forget()
        Videos.place(x=10, y=5)

    elif data == "icon":
        controlPanel.place_forget()
        Icons.place(x=10, y=5)

    elif data == "settings":
        controlPanel.place_forget()
        Settings.place(x=10, y=5)

    elif data == "back":
        Videos.place_forget()
        Icons.place_forget()
        Settings.place_forget()
        controlPanel.place(x=10, y=5)
    else:
        run_command(data)
        
controlPanel = LabelFrame(
    root,
    text="Holiday_Remote",
    bg="black",
    highlightcolor="red",
    fg="red",
    bd=5,
    width=150,
    height=600,
)
controlPanel.place(x=10, y=5)

VidBtn = Button(controlPanel,
                 text="Videos",
                 height=2,
                 width=8,
                 bg="green",
                 fg="black",
                 font=("Arial", 10),
                 command=lambda: fromUI("video"))
VidBtn.place(x=25, y=20)

IconBtn = Button(controlPanel,
                 text="Icons",
                 height=2,
                 width=8,
                 bg="green",
                 fg="black",
                 font=("Arial", 10),
                 command=lambda: fromUI("icon"))
IconBtn.place(x=25, y=110)

setBtn = Button(controlPanel,
                 text="Settings",
                 height=2,
                 width=8,
                 bg="green",
                 fg="black",
                 font=("Arial", 10),
                 command=lambda: fromUI("settings"))
setBtn.place(x=25, y=210)

Videos = LabelFrame(
    root,
    text="Videos",
    bg="black",
    highlightcolor="red",
    fg="red",
    bd=5,
    width=150,
    height=600,
)
grinchBtn = Button(Videos,
                   text="Grinch",
                   height=2,
                   width=8,
                   bg="green",
                   fg="black",
                   font=("Arial", 10),
                   command=lambda: fromUI("grinch"))
grinchBtn.place(x=25, y=20)

snowmanBtn = Button(Videos,
                    text="Snowman",
                    height=2,
                    width=8,
                    bg="green",
                    fg="black",
                    font=("Arial", 10),
                    command=lambda: fromUI("snowman"))
snowmanBtn.place(x=25, y=110)

vaderBtn = Button(Videos,
                  text="Vader",
                  height=2,
                  width=8,
                  bg="green",
                  fg="black",
                  font=("Arial", 10),
                  command=lambda: fromUI("vader"))
vaderBtn.place(x=25, y=210)

polarBtn = Button(Videos,
                  text="Polar",
                  height=2,
                  width=8,
                  bg="green",
                  fg="black",
                  font=("Arial", 10),
                  command=lambda: fromUI("polar"))
polarBtn.place(x=25, y=310)

whatBtn = Button(Videos,
                  text="Whats This",
                  height=2,
                  width=8,
                  bg="green",
                  fg="black",
                  font=("Arial", 10),
                  command=lambda: fromUI("what"))
whatBtn.place(x=25, y=410)

backBtn = Button(Videos,
                  text="Back",
                  height=2,
                  width=8,
                  bg="green",
                  fg="black",
                  font=("Arial", 10),
                  command=lambda: fromUI("back"))
backBtn.place(x=25, y=510)

Settings = LabelFrame(
    root,
    text="Settings",
    bg="black",
    highlightcolor="red",
    fg="red",
    bd=5,
    width=150,
    height=600,
)

initBtn = Button(Settings,
                 text="Init",
                 height=2,
                 width=8,
                 bg="green",
                 fg="black",
                 font=("Arial", 10),
                 command=lambda: fromUI("init"))
initBtn.place(x=25, y=20)

loudBtn = Button(Settings,
                 text="Loud",
                 height=2,
                 width=8,
                 bg="green",
                 fg="black",
                 font=("Arial", 10),
                 command=lambda: fromUI("loud"))
loudBtn.place(x=25, y=110)

muteBtn = Button(Settings,
                 text="Mute",
                 height=2,
                 width=8,
                 bg="green",
                 fg="black",
                 font=("Arial", 10),
                 command=lambda: fromUI("mute"))
muteBtn.place(x=25, y=210)
backBtn = Button(Settings,
                  text="Back",
                  height=2,
                  width=8,
                  bg="green",
                  fg="black",
                  font=("Arial", 10),
                  command=lambda: fromUI("back"))
backBtn.place(x=25, y=510)

Icons = LabelFrame(
    root,
    text="Icons",
    bg="black",
    highlightcolor="red",
    fg="red",
    bd=5,
    width=150,
    height=600,
)
wreathBtn = Button(Icons,
                   text="Wreath",
                   height=2,
                   width=8,
                   bg="green",
                   fg="black",
                   font=("Arial", 10),
                   command=lambda: fromUI("wreath"))
wreathBtn.place(x=25, y=20)

ballBtn = Button(Icons,
                    text="Ball",
                    height=2,
                    width=8,
                    bg="green",
                    fg="black",
                    font=("Arial", 10),
                    command=lambda: fromUI("ball"))
ballBtn.place(x=25, y=110)

snowFlakeBtn = Button(Icons,
                  text="Snowflake",
                  height=2,
                  width=8,
                  bg="green",
                  fg="black",
                  font=("Arial", 10),
                  command=lambda: fromUI("snowflake"))
snowFlakeBtn.place(x=25, y=210)

ghostBtn = Button(Icons,
                  text="Ghost",
                  height=2,
                  width=8,
                  bg="green",
                  fg="black",
                  font=("Arial", 10),
                  command=lambda: fromUI("ghost"))
ghostBtn.place(x=25, y=310)

pumpkinBtn = Button(Icons,
                  text="Pumpkin",
                  height=2,
                  width=8,
                  bg="green",
                  fg="black",
                  font=("Arial", 10),
                  command=lambda: fromUI("pumpkin"))
pumpkinBtn.place(x=25, y=410)

backBtn = Button(Icons,
                  text="Back",
                  height=2,
                  width=8,
                  bg="green",
                  fg="black",
                  font=("Arial", 10),
                  command=lambda: fromUI("back"))
backBtn.place(x=25, y=510)

t = threading.Thread(target=__create_ws)
t.start()

if not init:
    os.system('xdotool getactivewindow windowminimize')    
root.mainloop()  