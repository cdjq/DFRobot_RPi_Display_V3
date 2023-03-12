# -*- coding:GB18030 -*-
'''!
  @file demo_print.py
  @brief 字体示例
  @n print with fonts file, Different files will have different display effects
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @License     The MIT License (MIT)
  @author [fengli](li.feng@dfrobot.com)
  @version  V1.0
  @date  2022-6-13
  @url https://github.com/DFRobot/DFRobot_RPi_Display_V3
'''

import sys
sys.path.append("../..") # set system path to top

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
epaper = DFRobot_Epaper.DFRobot_Epaper_SPI(RASPBERRY_SPI_BUS, RASPBERRY_SPI_DEV, RASPBERRY_PIN_CS, RASPBERRY_PIN_CD, RASPBERRY_PIN_BUSY,RASPBERRY_PIN_RST) # create epaper object

# clear screen
epaper.begin()

epaper.clearScreen();


# config extension fonts
ft = Freetype_Helper(fontFilePath)
ft.setDisLowerLimite(112) # set display lower limit, adjust this to effect fonts color depth
epaper.setExFonts(ft) # init with fonts file
epaper.setTextFormat(1, epaper.BLACK, epaper.WHITE, 1, 1)

# print test
epaper.setExFontsFmt(32, 32) # set extension fonts width and height
epaper.setTextCursor(69, 0)
epaper.printStr("DFRobot")
epaper.flush(epaper.PART)
time.sleep(1)

epaper.setExFontsFmt(24, 24) # set extension fonts width and height
epaper.setTextCursor(0, 32)
epaper.printStr("品牌简介")
epaper.flush(epaper.PART)
time.sleep(1)

epaper.setExFontsFmt(16, 16) # set extension fonts width and height
epaper.setTextCursor(0, 60)
epaper.printStr("    DFRobot是上海智位机器人股份有限公司旗下注册商标")
epaper.flush(epaper.PART)
time.sleep(1)

for i in range(8):
  epaper.setExFontsFmt(16, 16) # set extension fonts width and height
  epaper.setTextCursor(0, 96)
  epaper.printStr("abcdefghijklmnopqrstuvwxyz")
  epaper.flush(epaper.PART)
  time.sleep(1)
  
  epaper.setExFontsFmt(16, 16) # set extension fonts width and height
  epaper.setTextCursor(0, 96)
  epaper.printStr("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
  epaper.flush(epaper.PART)
  time.sleep(1)
