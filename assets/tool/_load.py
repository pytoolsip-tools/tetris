# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-01-23 18:29:12
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-24 11:12:05
import os;

from _Global import _GG;
from function.base import *;

CurPath = os.path.dirname(os.path.realpath(__file__)); # 当前文件目录

EventId = require(GetPathByRelativePath("config", CurPath), "EventId", "EVENT_ID");
HotKeyConfig = require(GetPathByRelativePath("config", CurPath), "HotKeyConfig", "HotKeyConfig");

# 更新/添加配置
_GG("EventDispatcher").updateEventIds();
_GG("HotKeyManager").addHotKeyConfig(HotKeyConfig);
