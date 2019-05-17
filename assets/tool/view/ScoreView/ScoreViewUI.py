# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-01-23 11:06:47
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-30 12:10:03

import wx;

from _Global import _GG;
from function.base import *;

class ScoreViewUI(wx.Panel):
	"""docstring for ScoreViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(ScoreViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self.className_ = ScoreViewUI.__name__;
		self.curPath = curPath;
		self.viewCtr = viewCtr;

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_THEME,
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self.curPath + "***View"); # , parent = self, params = {}
		self.createText();
		self.createScore();
		
	def initViewLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.__text, flag = wx.TOP, border = 10);
		box.Add(self.__score, flag = wx.LEFT|wx.TOP|wx.BOTTOM, border = 6);
		self.SetSizer(box);

	def updateView(self, data):
		pass;

	def createText(self):
		self.__text = wx.StaticText(self, label = "当前分数：");
		self.__text.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));

	def createScore(self):
		self.__score = wx.StaticText(self, label = "0");
		self.__score.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));
		self.__score.SetForegroundColour(wx.Colour(255,140,0));

	def addScore(self, score):
		score = int(self.__score.GetLabel()) + score;
		self.__score.SetLabel(str(score));

	def getScore(self):
		return int(self.__score.GetLabel());

	def clearScore(self):
		self.__score.SetLabel("0");