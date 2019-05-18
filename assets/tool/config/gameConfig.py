# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-01-30 12:15:13
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-30 14:54:42
import wx;

GameConfig = {
	"scoreConfig" : [
		999999, # 消除>最大行
		2, # 消除1行
		6, # 消除2行
		12, # 消除3行
		20, # 消除4行
	],
	"speedConfig" : {
		"time" : {
			"seconds" : 1,
			"rate" : 0.0005,
		},
		"eliminate" : 0.02,
	},
}