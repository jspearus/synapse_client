#!/usr/bin/env python

import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

numb = 1
RST = None

# Create the SSD1306 OLED class.
# The first two parameters are the width and height. The third is the I2C interface.
oled = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
# Initialize library.
oled.begin()

# Clear display.
oled.clear()
oled.display()


# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = oled.width
height = oled.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# First define some constants to allow easy resizing of shapes.
padding = 10
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()


def refreshScreen():
    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True ).decode('ASCII')
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True ).decode('ASCII')
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True ).decode('ASCII')
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True ).decode('ASCII')

    # Write two lines of text.

    draw.text((x, top),       "     mini TREE",  font=font, fill=255)
    # draw.text((x, top+12),     str(CPU), font=font, fill=255)
    # draw.text((x, top+20),    str(MemUsage),  font=font, fill=255)
    draw.text((x, top+29),"IP: " + str(IP),  font=font, fill=255)
    draw.text((x, top+39),    "PORT: 8080",  font=font, fill=255)
    # Display image.
    oled.image(image)
    oled.display()

refreshScreen()
