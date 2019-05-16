# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-01-24 10:14:24
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-24 11:30:05
import os;

from function.base import *;

CurPath = os.path.dirname(os.path.realpath(__file__)); # 当前文件目录
EventID = require(CurPath, "EventId", "EVENT_ID");

# 热键配置
HotKeyConfig = {
	"LEFT" : EventID.KEY_LEFT_EVENT,
	"UP" : EventID.KEY_UP_EVENT,
	"RIGHT" : EventID.KEY_RIGHT_EVENT,
	"DOWN" : EventID.KEY_DOWN_EVENT,
};