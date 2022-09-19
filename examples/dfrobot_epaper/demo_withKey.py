# -*- coding:utf-8 -*-
'''!
  @file demo_withKey.py
  @brief °´¼ükeyAºÍkeyB²âÊÔ
  @n after clear screen, click keyA or keyB, you can see "A" or "B" printed on your device
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @License     The MIT License (MIT)
  @author [fengli](li.feng@dfrobot.com)
  @version  V1.0
  @date  2022-6-13
  @url https://github.com/DFRobot/DFRobot_RPi_Display_V3
'''

import sys
sys.path.append("../..") # set system path to top

import threading

from devices import DFRobot_Epaper
import time

from display_extension.freetype_helper import Freetype_Helper

fontFilePath = "../../display_extension/wqydkzh.ttf" # fonts file

# peripheral params
RASPBERRY_SPI_BUS = 0
RASPBERRY_SPI_DEV = 0
RASPBERRY_PIN_CS = 27
RASPBERRY_PIN_CD = 17
RASPBERRY_PIN_BUSY = 4
RASPBERRY_PIN_RST = 26
# get gpio interface
GPIO = DFRobot_Epaper.GPIO
EPAPER_KEY_A = 21
EPAPER_KEY_B = 20

# GPIO output test
'''
GPIO_OUT_PIN = 16
pinOut = GPIO(GPIO_OUT_PIN, GPIO.OUT)
pinOut.setOut(GPIO.LOW)
pinOut.setOut(GPIO.HIGH)
'''

epaper = DFRobot_Epaper.DFRobot_Epaper_SPI(RASPBERRY_SPI_BUS, RASPBERRY_SPI_DEV, RASPBERRY_PIN_CS, RASPBERRY_PIN_CD, RASPBERRY_PIN_BUSY,RASPBERRY_PIN_RST) # create epaper object

# config extension fonts
ft = Freetype_Helper(fontFilePath)
ft.setDisLowerLimite(96) # set display lower limite, adjust this to effect fonts color depth
epaper.setExFonts(ft) # init with fonts file
epaper.setExFontsFmt(32, 32) # set extension fonts width and height

keyALock = threading.Lock() # key A threading lock
keyBLock = threading.Lock() # key B threading lock
keyAFlag = False # key A flag
keyBFlag = False # key B flag

# key A callback
def keyACallBack():
  global keyALock, keyAFlag
  keyALock.acquire() # wait key A lock release
  keyAFlag = True
  keyALock.release()

# key B callback
def keyBCallBack():
  global keyBLock, keyBFlag
  keyBLock.acquire() # wait key B lock release
  keyBFlag = True
  keyBLock.release()

# config keyA and keyB
keyA = GPIO(EPAPER_KEY_A, GPIO.IN) # set key to input
keyB = GPIO(EPAPER_KEY_B, GPIO.IN) # set key to input
keyA.setInterrupt(GPIO.FALLING, keyACallBack) # set key interrupt callback
keyB.setInterrupt(GPIO.FALLING, keyBCallBack) # set key interrupt callback

# clear screen
epaper.begin()
epaper.clearScreen();
epaper.setTextFormat(1, epaper.BLACK, epaper.WHITE, 2, 0) # set text size, color, background, interval row, interval col

keyCount = 0
timeCount = 0
# key test
epaper.printStr("key test")
epaper.flush(epaper.PART)
epaper.setTextCursor(0, 32)

while True:
  if keyAFlag:
    keyALock.acquire() # wait key A release
    keyAFlag = False
    keyALock.release()
    keyCount += 1
    epaper.printStr("A")
    epaper.flush(epaper.PART)
  if keyBFlag:
    keyBLock.acquire() # wait key B release
    keyBFlag = False
    keyBLock.release()
    keyCount += 1
    epaper.printStr("B")
    epaper.flush(epaper.PART)
  if keyCount >= 16:
    keyCount = 0
    epaper.clear(epaper.WHITE)
    epaper.setTextCursor(0, 0)
    epaper.printStr("key test")
    epaper.flush(epaper.PART)
    epaper.setTextCursor(0, 32) # set text cursor to origin and clear

    
    

  time.sleep(0.01)
