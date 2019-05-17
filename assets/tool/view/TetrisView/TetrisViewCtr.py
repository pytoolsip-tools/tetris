# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-05-16 18:33:42
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-05-17 15:44:05
import os;
import wx;

from _Global import _GG;

from TetrisViewUI import *;

CurPath = os.path.dirname(os.path.realpath(__file__)); # 当前文件目录

EventID = require(GetPathByRelativePath("../../config", CurPath), "EventId", "EVENT_ID");

def getRegisterEventMap(G_EVENT):
	return {
		EventID.KEY_LEFT_EVENT : "updateDirection",
		EventID.KEY_UP_EVENT : "updateDirection",
		EventID.KEY_RIGHT_EVENT : "updateDirection",
		EventID.KEY_DOWN_EVENT : "updateDirection",
		EventID.KEY_SPACE_EVENT : "rotateItemList",
	};

class TetrisViewCtr(object):
	"""docstring for TetrisViewCtr"""
	def __init__(self, parent, params = {}):
		super(TetrisViewCtr, self).__init__();
		self._className_ = TetrisViewCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent, params); # 初始化视图UI
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.unregisterEventMap(); # 注销事件
		self.unbindBehaviors(); # 解绑组件
		self.delCtrMap(); # 銷毀控制器列表

	def delCtrMap(self):
		for key in self.__CtrMap:
			DelCtr(self.__CtrMap[key]);
		self.__CtrMap.clear();

	def initUI(self, parent, params):
		# 创建视图UI类
		self.__ui = TetrisViewUI(parent, curPath = self._curPath, viewCtr = self, params = params);
		self.__ui.initView();

	def getUI(self):
		return self.__ui;

	"""
		key : 索引所创建控制类的key值
		path : 所创建控制类的路径
		parent : 所创建控制类的UI的父节点，默认为本UI
		params : 扩展参数
	"""
	def createCtrByKey(self, key, path, parent = None, params = {}):
		if not parent:
			parent = self.getUI();
		self.__CtrMap[key] = CreateCtr(path, parent, params = params);

	def getCtrByKey(self, key):
		return self.__CtrMap.get(key, None);

	def getUIByKey(self, key):
		ctr = self.getCtrByKey(key);
		if ctr:
			return ctr.getUI();
		return None;
		
	def registerEventMap(self):
		eventMap = getRegisterEventMap(_GG("EVENT_ID"));
		for eventId, callbackName in eventMap.items():
			_GG("EventDispatcher").register(eventId, self, callbackName);

	def unregisterEventMap(self):
		eventMap = getRegisterEventMap(_GG("EVENT_ID"));
		for eventId, callbackName in eventMap.items():
			_GG("EventDispatcher").unregister(eventId, self, callbackName);

	def bindBehaviors(self):
		pass;
		
	def unbindBehaviors(self):
		pass;
			
	def updateView(self, data):
		self.__ui.updateView(data);

	def updateDirection(self, data):
		direction = Direction.LEFT;
		if data["hotKey"] == "UP":
			# direction = Direction.TOP;
			return; # 不处理向上的事件
		elif data["hotKey"] == "RIGHT":
			direction = Direction.RIGHT;
		elif data["hotKey"] == "DOWN":
			direction = Direction.BOTTOM;
		self.getUI().moveItemList(direction);

	def getMovingItemMtList(self, startPos, key = None):
		if not key:
			key = random.choice(["I", "J", "L", "O", "S", "Z", "T"]);
		if key == "I":
			return [
				(startPos[0]-3, startPos[1]),
				(startPos[0]-2, startPos[1]),
				(startPos[0]-1, startPos[1]),
				(startPos[0], startPos[1])
			];
		elif key == "J":
			return [
				(startPos[0]-2, startPos[1]),
				(startPos[0]-1, startPos[1]),
				(startPos[0], startPos[1]),
				(startPos[0], startPos[1]-1),
			];
		elif key == "L":
			return [
				(startPos[0]-2, startPos[1]),
				(startPos[0]-1, startPos[1]),
				(startPos[0], startPos[1]),
				(startPos[0], startPos[1]+1),
			];
		elif key == "O":
			return [
				(startPos[0]-1, startPos[1]),
				(startPos[0]-1, startPos[1]+1),
				(startPos[0], startPos[1]),
				(startPos[0], startPos[1]+1),
			];
		elif key == "S":
			return [
				(startPos[0]-1, startPos[1]+1),
				(startPos[0]-1, startPos[1]),
				(startPos[0], startPos[1]),
				(startPos[0], startPos[1]-1),
			];
		elif key == "Z":
			return [
				(startPos[0]-1, startPos[1]-1),
				(startPos[0]-1, startPos[1]),
				(startPos[0], startPos[1]),
				(startPos[0], startPos[1]+1),
			];
		elif key == "T":
			return [
				(startPos[0]-1, startPos[1]-1),
				(startPos[0]-1, startPos[1]),
				(startPos[0]-1, startPos[1]+1),
				(startPos[0], startPos[1]),
			];
		raise Exception("Error key[{}]".format(key));

	def startGame(self):
		self.getUI().startGame();

	def pauseGame(self):
		self.getUI().pauseGame();

	def isRunning(self):
		if self.getUI().isPlaying() and self.getUI().isRunningTimer():
			return True;
		return False;

	def stopGame(self):
		self.getUI().stopGame();

	def rotateItemList(self, data):
		if data["hotKey"] == "SPACE":
			self.getUI().rotateItemList();
