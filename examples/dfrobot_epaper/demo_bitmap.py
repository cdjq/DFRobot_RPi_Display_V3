# -*- coding:GB18030 -*-
'''!
  @file demo_bitmap.py
  @brief 位图显示
  @n 实验现象：墨水屏支持显示单色位图的bmp图片，更改demo_bitmap.py中的文件路径和文件名，即可显示你自己的图片。
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
#time.sleep(1)

epaper.bitmapFile(0, 0, "./logo_colorbits1.bmp") # show bitmap file
epaper.flush(epaper.FULL)

time.sleep(1)
epaper.bitmapFile(0, 0, "./epaper-Chinese.bmp") # show bitmap file


epaper.flush(epaper.FULL)


