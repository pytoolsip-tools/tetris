# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-01-23 11:19:56
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-30 12:28:05

import wx;

from _Global import _GG;
from function.base import *;

class RuleViewUI(wx.Panel):
	"""docstring for RuleViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(RuleViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self.className_ = RuleViewUI.__name__;
		self.curPath = curPath;
		self.viewCtr = viewCtr;
		self.__itemInfoList = [];

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_THEME,
			"scoreRuleTextList" : [
				"消除1行 -> +2分",
				"连续消除2行 -> +6分",
				"连续消除3行 -> +12分",
				"连续消除4行 -> +20分",
				"连续消除>4行 -> +999999分",
			],
			"ruleTextList" : [
				"每+1秒，提速0.05%",
				"每消除1行，提速2%",
			],
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
		self.createScoreRule();
		self.createRuleText();
		
	def initViewLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.AddMany(self.__itemInfoList);
		self.SetSizer(box);

	def updateView(self, data):
		pass;

	def createScoreRule(self):
		scoreRuleTitle = wx.StaticText(self, label = "分数计算：");
		scoreRuleTitle.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));
		self.__itemInfoList.append((scoreRuleTitle, 0, wx.TOP, 10));
		for scoreRuleText in self.__params["scoreRuleTextList"]:
			scoreRuleContent = wx.StaticText(self, label = scoreRuleText, size = (self.GetSize().x, -1));
			self.__itemInfoList.append((scoreRuleContent, 0, wx.LEFT|wx.TOP, 4));

	def createRuleText(self):
		ruleTitle = wx.StaticText(self, label = "加速规则：");
		ruleTitle.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));
		self.__itemInfoList.append((ruleTitle, 0, wx.TOP, 20));
		for ruleText in self.__params["ruleTextList"]:
			ruleContent = wx.StaticText(self, label = ruleText, size = (self.GetSize().x, -1));
			self.__itemInfoList.append((ruleContent, 0, wx.LEFT|wx.TOP, 4));