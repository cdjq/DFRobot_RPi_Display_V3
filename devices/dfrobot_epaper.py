# -*- coding:utf-8 -*-

import time

import sys
sys.path.append("..")
import RPi.GPIO as RPIGPIO
from dfrobot_display.dfrobot_display import DFRobot_Display
from display_extension import fonts_8_16 as fonts_ABC

try:
  from dfrobot_interface.raspberry.spi import SPI
  from dfrobot_interface.raspberry.gpio import GPIO
except:
  print("unknow platform")
  exit()

CONFIG_IL0376F = {

}

CONFIG_IL3895 = {
  
}


class DFRobot_Epaper(DFRobot_Display):

  XDOT = 128
  YDOT = 250
  GDEH0213B72  = 3
  GDEH0213B1   = 2
  FULL = True
  PART = False
  VERSION = GDEH0213B72
  is_full = True
  def __init__(self, width = 250, height = 122):
    DFRobot_Display.__init__(self, width, height)
    length = 4000
    self._displayBuffer = bytearray(length)
    i = 0
    while i < length:
      self._displayBuffer[i] = 0x00
      i = i + 1

    self._isBusy = False
    self._busyExitEdge = GPIO.RISING
    
    self._fonts.setFontsABC(fonts_ABC)
    self.setExFontsFmt(16, 16)

  def _busyCB(self, channel):
    self._isBusy = False

  def setBusyExitEdge(self, edge):
    if edge != GPIO.HIGH and edge != GPIO.LOW:
      return
    self._busyEdge = edge

  def begin(self):
    version = self.readID()
    if(version[0] == 0x01):
       self.VERSION = self.GDEH0213B1
    else:
       self.VERSION = self.GDEH0213B72
    #self._init()
    #self._powerOn()
    #self.setBusyCB(self._busyCB)
    #self._powerOn()


  def pixel(self, x, y, color):
    if x < 0 or x >= self._width:
      return
    if y < 0 or y >= self._height:
      return
    x = int(x)
    y = int(y)
    m = int(x * 16 + (y + 1) / 8)
    sy = int((y + 1) % 8)
    if color == self.WHITE:
      if sy != 0:
        self._displayBuffer[m] = self._displayBuffer[m] | int(pow(2, 8 - sy))
      else:
        self._displayBuffer[m - 1] = self._displayBuffer[m - 1] | 1
    elif color == self.BLACK:
      if sy != 0:
        self._displayBuffer[m] = self._displayBuffer[m] & (0xff - int(pow(2, 8 - sy)))
      else:
        self._displayBuffer[m - 1] = self._displayBuffer[m - 1] & 0xfe

  def _setRamData(self, xStart, xEnd, yStart, yStart1, yEnd, yEnd1):
    self.writeCmdAndData(0x44, [xStart, xEnd])
    self.writeCmdAndData(0x45, [yStart, yStart1, yEnd, yEnd1])

  def _setRamPointer(self, x, y, y1):
    self.writeCmdAndData(0x4e, [x])
    self.writeCmdAndData(0x4f, [y, y1])

  def _init(self,mode):
    self.reset()
    self._waitBusyExit()
    self.writeCmdAndData(0x12, [])
    self._waitBusyExit()
    self.writeCmdAndData(0x01, [0xf9,0x00,0x00])
    self.writeCmdAndData(0x11, [0x01])
    self.writeCmdAndData(0x44, [0x00,0x0f])
    self.writeCmdAndData(0x45, [0xf9,0x00,0x00,0x00])
    self.writeCmdAndData(0x3c, [0x05])
    self.writeCmdAndData(0x21, [0x00,0x80])
    self.writeCmdAndData(0x18, [0x80])
    self.writeCmdAndData(0x4e, [0x00])
    self.writeCmdAndData(0x4f, [0xf9,0x00])
    self._waitBusyExit()
    self.writeCmdAndData(0x0c, [0xf4,0xf4,0xf4,0x0f])
    
  def _writeDisRam(self, sizeX, sizeY):
    if sizeX % 8 != 0:
      sizeX = sizeX + (8 - sizeX % 8)
    sizeX = sizeX // 8
    
    self.writeCmdAndData(0x24, self._displayBuffer[0: sizeX * sizeY])

  def _sleep(self):
    self.writeCmdAndData(0x10, [0x01])
    time.sleep(0.1)
  def _updateDis(self, mode):
    if mode == self.FULL:
    
     self.writeCmdAndData(0x22, [0xc7])
    elif mode == self.PART:
          if self.VERSION == self.GDEH0213B72:
             self.writeCmdAndData(0x22, [0x0C])
          elif self.VERSION == self.GDEH0213B1:
             self.writeCmdAndData(0x22, [0xc7])
    else:
      return
    self.writeCmdAndData(0x20, [])
  

  def _waitBusyExit(self):
    temp = 0
    while self.readBusy() != False:
      time.sleep(0.01)
      temp = temp + 1
      if (temp % 200) == 0:
        print("waitBusyExit")

  def _powerOn(self):
    self.writeCmdAndData(0x22, [0xC0])
    self.writeCmdAndData(0x20, [])

  def _powerOff(self):
    self.writeCmdAndData(0x10, [0x01])
    time.sleep(0.1)
  def setPartRam(self):
    #print("set part")
    self._init(self.PART)
    self.writeCmdAndData(0x24, [])
    for i in range(0,4000):
      self.writeData(0x00)
    self.writeCmdAndData(0x26, [])
    for i in range(0,4000):
      self.writeData(0x00)
    self._waitBusyExit()
    self.writeCmdAndData(0x37, [0x00,0x40,0x20,0x10,0x00,0x00,0x00,0x00])
    self.writeCmdAndData(0x22, [0xf4])
    self.writeCmdAndData(0x20, [])
    self._waitBusyExit()
    
    self.writeCmdAndData(0x24, [])
    for i in range(0,4000):
      self.writeData(0x00)
    self.writeCmdAndData(0x26, [])
    for i in range(0,4000):
      self.writeData(0x00)
  def _disPart(self, xStart, yStart, width, height):
    # self._setRamData(xStart // 8, xEnd // 8, yEnd % 256, yEnd // 256, yStart % 256, yStart // 256)
    # self._setRamPointer(xStart // 8, yEnd % 256, yEnd // 256)
    # self._writeDisRam(xEnd - xStart, yEnd - yStart + 1)
    # self._updateDis(self.PART)
    
    #self.writeCmdAndData(0x91, [])
    #self.writeCmdAndData(0x90, [xStart,xEnd,yStart/256,yStart%256,yEnd/256,yEnd%256,0x28])
    

    
    xStart=xStart//8
    x_end=xStart+height//8-1
    
    y_start1=0
    y_start2=yStart
    if yStart>=256:
        y_start1 = y_start2//256
        y_start2 = y_start2%256
    y_end1=0
    y_end2=yStart+width-1
    if y_end2 >= 256:
       y_end1=y_end2//256
       y_end2=y_end2%256
    self.writeCmdAndData(0x44, [xStart,x_end])
    self.writeCmdAndData(0x45, [y_start2,y_start1,y_end2,y_end1])
    self.writeCmdAndData(0x4E, [xStart])
    self.writeCmdAndData(0x4F, [y_start2,y_start1])
    datas = (width*height)/8
    #self._waitBusyExit()
    self.writeCmdAndData(0x24, self._displayBuffer[0:4000])
    self._waitBusyExit()
    self.writeCmdAndData(0x37, [0x00,0x40,0x20,0x10,0x00,0x40,0x00,0x00])
    self.writeCmdAndData(0x3C, [0x80])
    self.writeCmdAndData(0x22, [0x3C])
    self.writeCmdAndData(0x20, [])
    self._waitBusyExit()
  
    
  def _disAall(self):
    self._init(self.PART)
    self.writeCmdAndData(0x24, self._displayBuffer[0: 4000])
    self.writeCmdAndData(0x26, [])
    for i in range(0,4000):
      self.writeData(0x0)
    self.writeCmdAndData(0x37, [0x00,0x40,0x20,0x10,0x00,0x00,0x00,0x00])
    self.writeCmdAndData(0x22, [0xf4])
    self.writeCmdAndData(0x20, [])
  def flush(self, mode):
    if mode != self.FULL and mode != self.PART:
      return
    if self.is_full == True and mode == self.PART:
      self.setPartRam()
      self.is_full = False
    if mode == self.FULL :
      self.is_full = True
    if mode == self.PART:
      self._disPart(0, 250,250 ,128)
    else:
      self._disAall()
      self._sleep()
   
  def startDrawBitmapFile(self, x, y):
    self._bitmapFileStartX = x
    self._bitmapFileStartY = y

  def bitmapFileHelper(self, buf):
    for i in range(len(buf) // 3):
      addr = i * 3
      if buf[addr] == 0x00 and buf[addr + 1] == 0x00 and buf[addr + 2] == 0x00:
        self.pixel(self._bitmapFileStartX, self._bitmapFileStartY, self.BLACK)
      else:
        self.pixel(self._bitmapFileStartX, self._bitmapFileStartY, self.WHITE)
      self._bitmapFileStartX += 1
  
  def endDrawBitmapFile(self):
    #self.flush(self.PART)
    time.sleep(0.01)
  def clearScreen(self):
    self.clear(self.WHITE)
    self.flush(self.FULL)
    if self.VERSION == self.GDEH0213B72:
         #self.flush(self.PART)
         time.sleep(0.1)
    elif self.VERSION == self.GDEH0213B1:
         time.sleep(0.1)
    
    
  def setVersion(self,version):
      self.VERSION = version
  def readID(self):
    self.writeCmdAndData(0x2f, [])
    return self.readData(1)


class DFRobot_Epaper_SPI(DFRobot_Epaper):
  
  def __init__(self, bus, dev, cs, cd, busy,rst):
    DFRobot_Epaper.__init__(self)
    self._busy = GPIO(busy, GPIO.IN)
    self._spi = SPI(bus, dev)
    self._cs = GPIO(cs, GPIO.OUT)
    self._cd = GPIO(cd, GPIO.OUT)
    self._rst = GPIO(rst, GPIO.OUT)
    
  
  def writeCmdAndData(self, cmd, data = []):
    #self._waitBusyExit()
    self._cs.setOut(GPIO.LOW)
    self._cd.setOut(GPIO.LOW)
    self._spi.transfer([cmd])
    #if(cmd == 0x82) time.sleep(0.1)
    if len(data):
      self._cd.setOut(GPIO.HIGH)
      self._spi.transfer(data)
    self._cs.setOut(GPIO.HIGH)
  def writeData(self,data):
    #self._waitBusyExit()
    self._cs.setOut(GPIO.LOW)
    self._cd.setOut(GPIO.HIGH)
    self._spi.transfer([data])
    self._cs.setOut(GPIO.HIGH)
  def readBusy(self):
    return self._busy.read()
    #time.sleep(0.1)
  def readData(self,n):
    self._cs.setOut(GPIO.LOW)
    self._cd.setOut(GPIO.HIGH)
    data = self._spi.readData(n)
    self._cs.setOut(GPIO.HIGH)
    return data
  def reset(self):
     self._rst.setOut(GPIO.LOW)
     time.sleep(0.01)
     self._rst.setOut(GPIO.HIGH)
     time.sleep(0.01)
  def setBusyCB(self, cb):
    self._busy.setInterrupt(self._busyExitEdge, cb)
  def __del__(self):
    RPIGPIO.cleanup()
