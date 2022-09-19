# -*- coding:utf-8 -*-
""" 
  @file DFRobot_printString.py
  @brief Define the basic structure of class DFRobot_printString 
  @details 该类提供在屏幕上打印字符串相关的函数
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @License     The MIT License (MIT)
  @author [fengli](li.feng@dfrobot.com)
  @version  V1.0
  @date  2022-6-13
  @url https://github.com/DFRobot/DFRobot_RPi_Display_V3
"""
import sys

class PrintString:

  def __init__(self):
    pass

  def writeOneChar(self, ch):
    '''!
      @fn writeOneChar
      @brief 在屏幕上显示一个字符
      @param c 字符的ascii码
    '''
    pass

  def printStr(self, c):
    '''!
      @fn printStr
      @brief 在屏幕上显示字符串
      @param c 字符串
    '''
    try:
      c = str(c)
    except:
      return
    if sys.version_info.major == 2:
      c = c.decode("utf-8")
    for i in c:
      self.writeOneChar(i)

  def printStrLn(self, c):
    '''!
      @fn printStrLn
      @brief 在屏幕上显示字符串,并换行
      @param c 字符串
    '''
    self.printStr(c)
    self.writeOneChar("\n")
