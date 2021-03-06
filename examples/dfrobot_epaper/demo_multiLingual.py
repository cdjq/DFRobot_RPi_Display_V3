# -*- coding:utf-8 -*-
'''
file demo_print.py

connect epaper to your raspberryPi
print with fonts file, different fonts files will have different display effects

Copyright   [DFRobot](http://www.dfrobot.com), 2016
Copyright   GNU Lesser General Public License

version  V1.0
date  2018-10-27
'''

import sys
sys.path.append("../..") # set system path to top

from devices import dfrobot_epaper
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

epaper = dfrobot_epaper.DFRobot_Epaper_SPI(RASPBERRY_SPI_BUS, RASPBERRY_SPI_DEV, RASPBERRY_PIN_CS, RASPBERRY_PIN_CD, RASPBERRY_PIN_BUSY,RASPBERRY_PIN_RST) # create epaper object

# clear screen
epaper.begin()
epaper.clearScreen();

# config extension fonts
ft = Freetype_Helper(fontFilePath)
ft.setDisLowerLimite(96) # set display lower limite, adjust this to effect fonts color depth
epaper.setExFonts(ft) # init with fonts file
epaper.setTextFormat(1, epaper.BLACK, epaper.WHITE, 2, 2)
epaper.setExFontsFmt(24, 24) # set extension fonts width and height

#epaper.clear(epaper.WHITE)
#epaper.flush(epaper.PART)
epaper.setTextCursor(10,10)
epaper.printStrLn("中国  北京")
epaper.flush(epaper.PART)
epaper.printStrLn("USA   Washington")
epaper.flush(epaper.PART)
epaper.printStrLn("日本  東京")
epaper.flush(epaper.PART)
epaper.printStrLn("韩国  서울")
epaper.flush(epaper.PART)
time.sleep(1)