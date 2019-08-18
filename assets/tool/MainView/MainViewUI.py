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
		self.__isStarted = False;
		self.__SpendSeconds = 0;
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
		self.createOtherPanel();
		pass;
		
	def initViewLayout(self):
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(self.controlPanel);
		box.Add(self.contentPanel);
		box.Add(self.otherPanel);
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
			self.getCtr().getUIByKey("TimingViewCtr").stopTimer();
			self.startGameBtn.SetLabel("开始游戏");
		else:
			self.getCtr().getCtrByKey("TetrisViewCtr").startGame();
			self.getCtr().getUIByKey("TimingViewCtr").startTimer(isReset = not self.__isStarted);
			self.startGameBtn.SetLabel("暂停游戏");
			self.__isStarted = True;

	def onRestartGame(self, ecent = None):
		self.__isStarted = False;
		self.getCtr().getCtrByKey("TetrisViewCtr").stopGame();
		self.onStartGame();

	def initControlPanelLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.startGameBtn, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		box.Add(self.restartGameBtn, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		self.controlPanel.SetSizerAndFit(box);

	def createContentPanel(self):
		self.contentPanel = wx.Panel(self, size = (600, max(600, self.GetSize().y)), style = wx.BORDER_THEME);
		self.contentPanel.SetBackgroundColour(wx.Colour(0,0,0));
		# 创建俄罗斯方块视图
		self.getCtr().createCtrByKey("TetrisViewCtr", GetPathByRelativePath("../view/TetrisView", self._curPath), parent = self.contentPanel, params = {
			"size" : (300,580),
			"matrix" : (29,15),
			"onSetNext" : self.onUpdateNext,
			"onEliminate" : self.onAddScore,
			"onGameOver" : self.onGameOver,
		});
		# 创建时间视图
		self.getCtr().createCtrByKey("TimingViewCtr", GetPathByRelativePath("../view/TimingView", self._curPath), parent = self.contentPanel, params = {
			"size" : (self.contentPanel.GetSize().x, -1),
			"onTimer" : self.onTimerCallback,
		});
		# 调整布局
		self.updateContentPanelSize();
		self.initContentPanelLayout();

	def updateContentPanelSize(self):
		contentPanelSize = self.contentPanel.GetSize();
		tetrisViewSize = self.getCtr().getUIByKey("TetrisViewCtr").GetSize();
		timingViewSize = self.getCtr().getUIByKey("TimingViewCtr").GetSize();
		newSizeX = max(contentPanelSize.x, tetrisViewSize.x, timingViewSize.x);
		newSizeY = max(self.controlPanel.GetSize().y, contentPanelSize.y, tetrisViewSize.y + timingViewSize.y);
		self.contentPanel.SetSize(newSizeX, newSizeY);

	def initContentPanelLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		topOffset = (self.contentPanel.GetSize().y - self.getCtr().getUIByKey("TetrisViewCtr").GetSize().y - self.getCtr().getUIByKey("TimingViewCtr").GetSize().y - 6) / 2;
		box.Add(self.getCtr().getUIByKey("TimingViewCtr"), flag = wx.ALIGN_CENTER|wx.TOP, border = topOffset);
		box.Add(self.getCtr().getUIByKey("TetrisViewCtr"), flag = wx.ALIGN_CENTER);
		self.contentPanel.SetSizer(box);

	def createOtherPanel(self):
		self.otherPanel = wx.Panel(self, size = (max(200, self.GetSize().x - 700), max(600, self.GetSize().y)), style = wx.BORDER_THEME);
		self.createOtherViews(self.otherPanel);
		self.updateOtherPanelSize();
		self.initOtherPanelLayout();

	def createOtherViews(self, parent):
		self.getCtr().createCtrByKey("ScoreViewCtr", GetPathByRelativePath("../view/ScoreView", self._curPath), parent = parent, params = {"size" : (parent.GetSize().x, -1)}); # , parent = self, params = {}
		scoreViewSize = self.getCtr().getUIByKey("ScoreViewCtr").GetSize();
		itemSizeX = 10;
		if parent.GetSize().x/4 < itemSizeX:
			itemSizeX = parent.GetSize().x/4;
		self.getCtr().createCtrByKey("NextViewCtr", GetPathByRelativePath("../view/NextView", self._curPath), parent = parent, params = {"size" : (parent.GetSize().x, -1), "itemSize" : (itemSizeX, itemSizeX)}); # , parent = self, params = {}
		nextViewSize = self.getCtr().getUIByKey("NextViewCtr").GetSize();
		self.getCtr().createCtrByKey("RuleViewCtr", GetPathByRelativePath("../view/RuleView", self._curPath), parent = parent, params = {
			"size" : (scoreViewSize.x, parent.GetSize().y - scoreViewSize.y - nextViewSize.y),
		});

	def updateOtherPanelSize(self):
		otherPanelSize = self.otherPanel.GetSize();
		scoreViewSize = self.getCtr().getUIByKey("ScoreViewCtr").GetSize();
		nextViewSize = self.getCtr().getUIByKey("NextViewCtr").GetSize();
		ruleViewSize = self.getCtr().getUIByKey("RuleViewCtr").GetSize();
		newSizeX = max(otherPanelSize.x, scoreViewSize.x, nextViewSize.x, ruleViewSize.x);
		newSizeY = max(self.controlPanel.GetSize().y, self.contentPanel.GetSize().y, otherPanelSize.y, scoreViewSize.y + nextViewSize.y + ruleViewSize.y);
		self.otherPanel.SetSize(newSizeX, newSizeY);

	def initOtherPanelLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		topOffset = (self.otherPanel.GetSize().y - self.getCtr().getUIByKey("ScoreViewCtr").GetSize().y - self.getCtr().getUIByKey("NextViewCtr").GetSize().y - self.getCtr().getUIByKey("RuleViewCtr").GetSize().y) / 2;
		box.Add(self.getCtr().getUIByKey("ScoreViewCtr"), flag = wx.ALIGN_CENTER|wx.TOP, border = topOffset);
		box.Add(self.getCtr().getUIByKey("NextViewCtr"), flag = wx.ALIGN_CENTER);
		box.Add(self.getCtr().getUIByKey("RuleViewCtr"), flag = wx.ALIGN_CENTER);
		self.otherPanel.SetSizer(box);

	def onUpdateNext(self, itemMtList = []):
		NextViewUI = self.getCtr().getUIByKey("NextViewCtr");
		if NextViewUI:
			itemPosList = [];
			for itemMt in itemMtList:
				itemPosList.append([itemMt[0]+3, itemMt[1]+1]);
			NextViewUI.updateNext(itemPosList = itemPosList)

	def onAddScore(self, eliminateCount = 0):
		if eliminateCount > 0:
			# 更新分数
			self.getCtr().getUIByKey("ScoreViewCtr").addScore(self.getCtr().getScoreByCount(eliminateCount));
			# 提升速度
			self.getCtr().getUIByKey("TetrisViewCtr").toSpeedUp((1 - self.getCtr().getSpeedConfig("eliminate", 0.02)) ** eliminateCount);

	def onGameOver(self):
		self.startGameBtn.SetLabel("开始游戏");
		self.getCtr().getUIByKey("TimingViewCtr").stopTimer();
		self.__isStarted = False;

	def onTimerCallback(self, seconds = 0):
		diffSeconds = seconds - self.__SpendSeconds;
		if diffSeconds > 0:
			timeConfig = self.getCtr().getSpeedConfig("time", {"seconds" : 1, "rate" : 0.0005});
			self.__SpendSeconds = seconds + seconds % timeConfig["seconds"];
			self.getCtr().getUIByKey("TetrisViewCtr").toSpeedUp((1 - timeConfig["rate"]) ** int(seconds / timeConfig["seconds"]));
