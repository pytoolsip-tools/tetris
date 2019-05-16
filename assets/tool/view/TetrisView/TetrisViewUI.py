# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-05-16 18:33:42
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-05-16 18:33:42

import wx;

from _Global import _GG;
from function.base import *;

class TetrisViewUI(wx.Panel):
	"""docstring for TetrisViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(TetrisViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self._className_ = TetrisViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_NONE,
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.__viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self._curPath + "***View"); # , parent = self, params = {}
		pass;
		
	def initViewLayout(self):
		pass;

	def updateView(self, data):
		pass;
