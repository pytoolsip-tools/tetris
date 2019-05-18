# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-05-18 11:44:23
# @Last Modified by:   Administrator
# @Last Modified time: 2019-05-18 11:44:23

import wx;

from _Global import _GG;
from function.base import *;

class NextViewUI(wx.Panel):
	"""docstring for NextViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(NextViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self._className_ = NextViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.__itemList = [];
		self.SetBackgroundColour(self.__params["bgColour"]);

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_THEME,
			"itemSize" : (6,6),
			"matrix" : (4,4),
			"bgColour" : wx.Colour(255,255,255),
			"itemColour" : wx.Colour(0,0,0),
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
		self.createText();
		self.createNext();
		pass;
		
	def initViewLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.__text, flag = wx.TOP, border = 10);
		box.Add(self.__next, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 6);
		self.SetSizer(box);

	def updateView(self, data):
		pass;

	def createText(self):
		self.__text = wx.StaticText(self, label = "下个方块：");
		self.__text.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));

	def createNext(self):
		self.__next = wx.Panel(self, size = (self.__params["itemSize"][0]*self.__params["itemSize"][1], self.__params["itemSize"][1]*self.__params["itemSize"][0]));
		self.initItemList(self.__next);
		self.initItemLayout(self.__next);

	def initItemList(self, parent):
		for i in range(self.__params["matrix"][0]):
			for j in range(self.__params["matrix"][1]):
				self.__itemList.append(wx.Panel(parent, size = self.__params["itemSize"]));

	def initItemLayout(self, parent):
		box = wx.FlexGridSizer(self.__params["matrix"][0], self.__params["matrix"][1], 2);
		box.AddMany(self.__itemList);
		parent.SetSizerAndFit(box);

	def updateNext(self, itemPosList=[]):
		self.resetNext();
		for itemPos in itemPosList:
			idx = itemPos[0]*self.__params["matrix"][1]+itemPos[1];
			self.__itemList[idx].SetBackgroundColour(self.__params["itemColour"]);
		self.Refresh();

	def resetNext(self):
		for item in self.__itemList:
			item.SetBackgroundColour(self.__params["bgColour"]);