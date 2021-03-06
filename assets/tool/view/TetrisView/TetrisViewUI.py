# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-05-16 18:33:42
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-05-17 16:32:03

import wx;
import random, math;
from enum import Enum, unique;
from datetime import datetime;

from _Global import _GG;
from function.base import *;

@unique
class Direction(Enum):
	LEFT = 0;
	TOP = 1;
	RIGHT = 2;
	BOTTOM = 3;

class TetrisViewUI(wx.Panel):
	"""docstring for TetrisViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(TetrisViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self._className_ = TetrisViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.init();
		self.createTimer();
		self.SetBackgroundColour(self.__params["bgColour"]);

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.stopAllTimer(isDestroy = True); # 停止定时器

	def init(self):
		self.__playing = False; # 游戏进行中的标记
		self.__isSpeedUp = False; # 升速的标记位
		self.__timeDuration = 400; # 每次移动的时间
		self.__fixedItemMatrix = []; # 已固定的方块矩阵
		self.__movingItemList = []; # 移动中的方块列表
		self.__nextItemMtList = [];
		self.__setNextItemMtList__();
		self.__initFixedItemMatrix__();

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (360,360),
			"style" : wx.BORDER_NONE,
			"bgColour" : wx.Colour(255,255,255),
			"matrix" : (36,36),
			"squareColour" : wx.Colour(0,0,0),
			"onSetNext" : None,
			"onEliminate" : None,
			"onGameOver" : None,
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

	def stopAllTimer(self, isDestroy = False):
		self.stopTimer();
		if isDestroy:
			_GG("TimerManager").deleteTimer(self.__timer);

	def __setNextItemMtList__(self):
		curItemMtList = self.__nextItemMtList;
		col = int(self.__params["matrix"][1]/2);
		self.__nextItemMtList = self.getCtr().getMovingItemPosList((0, 0));
		if callable(self.__params.get("onSetNext", None)):
			self.__params["onSetNext"](self.__nextItemMtList);
		for itemMt in self.__nextItemMtList:
			itemMt[1] += col;
		return curItemMtList;

	# 初始化固定方块矩阵
	def __initFixedItemMatrix__(self):
		for i in range(self.__params["matrix"][0]):
			fixedItemList = [];
			for j in range(self.__params["matrix"][1]):
				fixedItemList.append(None);
			self.__fixedItemMatrix.append(fixedItemList); # 已固定的方块矩阵

	def createTimer(self):
		self.__timer = _GG("TimerManager").createTimer(self, callback = self.onTimer);
		self.__curTimer = datetime.now();

	def startTimer(self):
		self.__timer.Start(self.__timeDuration);

	def stopTimer(self):
		if self.__timer.IsRunning():
			self.__timer.Stop();

	def onTimer(self, event = None):
		self.moveItemList();
		if self.__isSpeedUp:
			self.startTimer();
			self.__isSpeedUp = False;
		self.checkToFocusSelf(); # 检测是否重新对焦自己

	def getItemSize(self):
		rows, cols = self.__params["matrix"][0], self.__params["matrix"][1];
		return wx.Size(self.__params["size"][0]/cols, self.__params["size"][1]/rows);

	def createItem(self):
		return wx.Panel(self, size = self.getItemSize(), style = wx.BORDER_THEME);

	def moveItem(self, item, row, col):
		itemSize = self.getItemSize();
		item.Move(col*itemSize.x, row*itemSize.y);
		item.m_mt = (row, col);

	# 移动方块
	def moveItemList(self, direction = Direction.BOTTOM):
		if self.__playing:
			if self.checkDirection(direction):
				for item in self.__movingItemList:
					row, col = item.m_mt;
					if direction == Direction.BOTTOM:
						row+=1;
					elif direction == Direction.LEFT:
						col-=1;
					elif direction == Direction.RIGHT:
						col+=1;
					self.moveItem(item, row, col);
			elif direction == Direction.BOTTOM:
				if not self.checkGameOver():
					self.setFixedItemMatrix();
					self.eliminateSquares();
					self.createMovingItemList();

	# 创建移动方块
	def createMovingItemList(self):
		self.__movingItemList = [];
		itemMtList = self.__setNextItemMtList__();
		for itemMt in itemMtList:
			item = self.createItem();
			item.SetBackgroundColour(self.__params["squareColour"]);
			self.moveItem(item, *itemMt);
			self.__movingItemList.append(item);

	# 设置固定方块
	def setFixedItemMatrix(self, itemList = []):
		if len(itemList) == 0:
			itemList = self.__movingItemList;
			self.__movingItemList = [];
		for item in itemList:
			row, col = item.m_mt;
			if row > 0:
				self.__fixedItemMatrix[row][col] = item;

	# 检测方向
	def checkDirection(self, direction):
		if direction in [Direction.LEFT, Direction.TOP, Direction.RIGHT, Direction.BOTTOM]:
			for item in self.__movingItemList:
				row, col = item.m_mt;
				if direction == Direction.BOTTOM:
					row+=1;
				elif direction == Direction.LEFT:
					col-=1;
				elif direction == Direction.RIGHT:
					col+=1;
				rows, cols = self.__params["matrix"][0], self.__params["matrix"][1];
				if row >= rows or col < 0 or col >= cols:
					return False;
				elif row >= 0 and self.__fixedItemMatrix[row][col]:
					return False;
			return True;
		return False;

	# 消除方块
	def eliminateSquares(self):
		eliminateCount = 0;
		rows, cols = self.__params["matrix"][0], self.__params["matrix"][1];
		# 逐行消除
		for i in range(rows-1, -1, -1):
			squareCount = 0;
			for j in range(cols):
				if self.__fixedItemMatrix[i][j]:
					squareCount += 1;
			if squareCount > 0:
				if squareCount == cols:
					for j in range(cols):
						if self.__fixedItemMatrix[i][j]:
							self.__fixedItemMatrix[i][j].Destroy();
							self.__fixedItemMatrix[i][j] = None;
					eliminateCount += 1;
				elif eliminateCount > 0:
					for j in range(cols):
						if self.__fixedItemMatrix[i][j]:
							self.moveItem(self.__fixedItemMatrix[i][j], i+eliminateCount, j);
							self.__fixedItemMatrix[i][j], self.__fixedItemMatrix[i+eliminateCount][j] = None, self.__fixedItemMatrix[i][j];
			else:
				# 若该行不存在方块，则跳出该循环
				break;
		if callable(self.__params.get("onEliminate", None)):
			self.__params["onEliminate"](eliminateCount);

	# 旋转方块
	def rotateItemList(self):
		if self.__playing and len(self.__movingItemList) > 0:
			# 获取Item的移动数据
			newItemMtList = [];
			centerRow, centerCol = self.__movingItemList[1].m_mt;
			angle = -math.pi/2;
			sinVal, cosVal = int(math.sin(angle)), int(math.cos(angle));
			rows, cols = self.__params["matrix"][0], self.__params["matrix"][1];
			for item in self.__movingItemList:
				row, col = item.m_mt;
				newRow = centerRow + (row - centerRow) * cosVal - (col - centerCol) * sinVal;
				newCol = centerCol + (col - centerCol) * cosVal + (row - centerRow) * sinVal;
				if newRow >= rows or newCol < 0 or newCol >= cols:
					return
				elif newRow >= 0 and self.__fixedItemMatrix[newRow][newCol]:
					return
				newItemMtList.append((item, newRow, newCol));
			# 移动Item
			for itemMt in newItemMtList:
				self.moveItem(*itemMt);

	def checkGameOver(self):
		for item in self.__movingItemList:
			if item.m_mt[0] <= 0:
				self.onGameOver();
				return True;
		return False;

	def onGameOver(self):
		self.stopTimer();
		if callable(self.__params.get("onGameOver", None)):
			self.__params["onGameOver"]();
		msgDialog = wx.MessageDialog(self, "游戏结束！", "游戏结束", style = wx.OK|wx.ICON_INFORMATION);
		msgDialog.ShowModal();
		# 停止游戏并清除界面
		self.stopGame();

	def resetFixedItemMt(self):
		for items in self.__fixedItemMatrix:
			for i in range(len(items)):
				if items[i]:
					items[i].Destroy();
					items[i] = None;

	def resetMovingItemList(self):
		for item in self.__movingItemList:
			item.Destroy();
		self.__movingItemList = [];

	def startGame(self, event = None):
		if not self.__playing:
			self.createMovingItemList();
			self.__playing = True;
		if not self.__timer.IsRunning():
			self.startTimer();

	def pauseGame(self, event = None):
		if self.__playing:
			self.stopTimer();

	def isPlaying(self):
		return self.__playing;

	def isRunningTimer(self):
		return self.__timer.IsRunning();

	def stopGame(self, event = None):
		self.stopTimer();
		self.resetFixedItemMt();
		self.resetMovingItemList();
		self.init();

	def toSpeedUp(self, rate = 0.8):
		self.__timeDuration = self.__timeDuration * rate;
		self.__isSpeedUp = True;

	def checkToFocusSelf(self):
		nowTime = datetime.now();
		diffDataTime = nowTime - self.__curTimer;
		diffSeconds = diffDataTime.seconds;
		if diffSeconds >= 1:
			self.SetFocusFromKbd(); # 时间回调时，
			self.__curTimer = nowTime;