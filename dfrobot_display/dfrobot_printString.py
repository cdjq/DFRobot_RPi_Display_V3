# -*- coding:utf-8 -*-
""" 
  @file DFRobot_printString.py
  @brief Define the basic structure of class DFRobot_printString 
  @details �����ṩ����Ļ�ϴ�ӡ�ַ�����صĺ���
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
      @brief ����Ļ����ʾһ���ַ�
      @param c �ַ���ascii��
    '''
    pass

  def printStr(self, c):
    '''!
      @fn printStr
      @brief ����Ļ����ʾ�ַ���
      @param c �ַ���
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
      @brief ����Ļ����ʾ�ַ���,������
      @param c �ַ���
    '''
    self.printStr(c)
    self.writeOneChar("\n")
