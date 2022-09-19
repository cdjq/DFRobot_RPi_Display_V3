# -*- coding:utf-8 -*-
""" 
  @file DFRobot_fonts.py
  @brief Define the basic structure of class Fonts 
  @details 该类提供字体相关的函数
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @License     The MIT License (MIT)
  @author [fengli](li.feng@dfrobot.com)
  @version  V1.0
  @date  2022-6-13
  @url https://github.com/DFRobot/DFRobot_RPi_Display_V3
"""
import json

class Fonts:

  def __init__(self):
    self._haveFontsABC = False
    self._fontsABC = {}
    self._fontsABCWidth = 0
    self._fontsABCHeight = 0
    self._fontsABCFmt = ""

    self._haveExtensionFonts = False
    self._extensionFontsWidth = 0
    self._extensionFontsHeight = 0
    
    self._enableDefaultFonts = True

  def setFontsABC(self, fonts):
    '''!
      @fn setFontsABC
      @brief 设置ascii码的字体格式
      @param fonts 字体类型
    '''
    self._haveFontsABC = True
    self._fontsABC = fonts.fonts
    self._fontsABCWidth = fonts.width
    self._fontsABCHeight = fonts.height
    self._fontsABCFmt = fonts.fmt
    
    self._extensionFontsWidth = fonts.width * 2
    self._extensionFontsHeight = fonts.height * 2

  def setExFonts(self, obj):
    '''!
      @fn setExFonts
      @brief init with fonts file
      @param obj 字体文件
    '''
    self._haveExtensionFonts = True
    self._extensionFonts = obj
    self._enableDefaultFonts = False
  
  def setEnableDefaultFonts(self, opt):
    '''!
      @fn setEnableDefaultFonts
      @brief 设置是否使能模式字体
      @param opt True/False
    '''
    if opt:
      self._enableDefaultFonts = True
    else:
      self._enableDefaultFonts = False

  def setExFontsFmt(self, width, height):
    '''!
      @fn setExFontsFmt
      @brief 设置扩展字体的格式
      @param width 字体宽度
      @param height 字体高度
    '''
    if self._haveExtensionFonts:
      self._extensionFonts.setFmt(width, height)
      self._extensionFontsWidth = width
      self._extensionFontsHeight = height

  def getOneCharacter(self, c):
    '''!
      @fn getOneCharacter
      @brief 获取字符的字体数据
      @param c 字符的ascii码
    '''
    w = 0
    h = 0
    fmt = "UNKNOW"
    rslt = []
    done = False
    if self._haveFontsABC and self._enableDefaultFonts:
      try:
        rslt = self._fontsABC[c]
        w = self._fontsABCWidth
        h = self._fontsABCHeight
        fmt = self._fontsABCFmt
        done = True
      except:
        # print("try get fonts ABC faild")
        pass
    if self._haveExtensionFonts and done == False:
      try:
        (rslt, w, h, fmt) = self._extensionFonts.getOne(c)
        done = True
      except:
        print("try get unicode fonts faild: %s" %(c))
    return (rslt, w, h, fmt)
