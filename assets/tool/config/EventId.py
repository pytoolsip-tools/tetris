# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-01-23 18:27:11
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-24 10:18:43

from enum import Enum, unique;

from _Global import _GG;

# 枚举事件Id
@unique
class EVENT_ID(Enum):
	KEY_LEFT_EVENT = _GG("EVENT_ID").getNewId(); # 键盘键【左】

	KEY_UP_EVENT = _GG("EVENT_ID").getNewId(); # 键盘键【上】

	KEY_RIGHT_EVENT = _GG("EVENT_ID").getNewId(); # 键盘键【右】

	KEY_DOWN_EVENT = _GG("EVENT_ID").getNewId(); # 键盘键【下】