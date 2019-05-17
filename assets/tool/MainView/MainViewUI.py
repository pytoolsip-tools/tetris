# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-10-08 21:02:23
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-05-16 18:37:47

import wx;

from _Global import _GG;
from function.base import *;

class MainViewUI(wx.ScrolledWindow):
	"""docstring for MainViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(MainViewUI, self).__init__(parent, id, size = self.__params["size"]);
		self._className_ = MainViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.bindEvents(); # 绑定事件
		self.SetBackgroundColour(self.__params["bgColour"]);
		# 初始化滚动条参数
		self.SetScrollbars(1, 1, *self.__params["size"]);

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.unbindEvents();

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"size" : _GG("WindowObject").GetToolWinSize(),
			"style" : wx.BORDER_THEME,
			"bgColour" : wx.Colour(255,255,255),
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.__viewCtr;

	def bindEvents(self):
		_GG("WindowObject").BindEventToToolWinSize(self, self.onToolWinSize);

	def unbindEvents(self):
		_GG("WindowObject").UnbindEventToToolWinSize(self);

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局
		self.resetScrollbars(); # 重置滚动条

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self._curPath + "***View"); # , parent = self, params = {}
		self.createControlPanel();
		self.createContentPanel();
		pass;
		
	def initViewLayout(self):
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(self.controlPanel);
		box.Add(self.contentPanel);
		self.SetSizerAndFit(box);

	def resetScrollbars(self):
		self.SetScrollbars(1, 1, self.GetSizer().GetSize().x, self.GetSizer().GetSize().y);

	def onToolWinSize(self, sizeInfo, event = None):
		self.SetSize(self.GetSize() + sizeInfo["preDiff"]);
		self.Refresh();
		self.Layout();

	def updateView(self, data):
		pass;

	def createControlPanel(self):
		self.controlPanel = wx.Panel(self, size = (100, self.GetSize().y), style = wx.BORDER_THEME);
		self.createStartGameBtn(self.controlPanel);
		self.createRestartGameBtn(self.controlPanel);
		self.initControlPanelLayout();

	def createStartGameBtn(self, parent):
		self.startGameBtn = wx.Button(parent, label = "开始游戏");
		self.startGameBtn.Bind(wx.EVT_BUTTON, self.onStartGame);

	def createRestartGameBtn(self, parent):
		self.restartGameBtn = wx.Button(parent, label = "重新开始");
		self.restartGameBtn.Bind(wx.EVT_BUTTON, self.onRestartGame);

	def onStartGame(self, event = None):
		if self.getCtr().getCtrByKey("TetrisViewCtr").isRunning():
			self.getCtr().getCtrByKey("TetrisViewCtr").pauseGame();
			self.startGameBtn.SetLabel("开始游戏");
		else:
			self.getCtr().getCtrByKey("TetrisViewCtr").startGame();
			self.startGameBtn.SetLabel("暂停游戏");

	def onRestartGame(self, ecent = None):
		self.getCtr().getCtrByKey("TetrisViewCtr").stopGame()
		self.onStartGame();

	def initControlPanelLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.startGameBtn, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		box.Add(self.restartGameBtn, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		self.controlPanel.SetSizerAndFit(box);

	def createContentPanel(self):
		self.contentPanel = wx.Panel(self, size = (600, max(600, self.GetSize().y)), style = wx.BORDER_THEME);
		self.contentPanel.SetBackgroundColour(wx.Colour(0,0,0));
		self.getCtr().createCtrByKey("TetrisViewCtr", GetPathByRelativePath("../view/TetrisView", self._curPath), parent = self.contentPanel, params = {
			"size" : (360,580),
			"matrix" : (29,18),
		});
		self.updateContentPanelSize();
		self.initContentPanelLayout();

	def updateContentPanelSize(self):
		contentPanelSize = self.contentPanel.GetSize();
		tetrisViewSize = self.getCtr().getUIByKey("TetrisViewCtr").GetSize();
		newSizeX = max(contentPanelSize.x, tetrisViewSize.x);
		newSizeY = max(self.controlPanel.GetSize().y, contentPanelSize.y, tetrisViewSize.y);
		self.contentPanel.SetSize(newSizeX, newSizeY);

	def initContentPanelLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		topOffset = (self.contentPanel.GetSize().y - self.getCtr().getUIByKey("TetrisViewCtr").GetSize().y - 6) / 2;
		box.Add(self.getCtr().getUIByKey("TetrisViewCtr"), flag = wx.ALIGN_CENTER|wx.TOP, border = topOffset);
		self.contentPanel.SetSizer(box);