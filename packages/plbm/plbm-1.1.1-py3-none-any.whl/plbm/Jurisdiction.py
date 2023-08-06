#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   Jurisdiction.py
@Time    :   2022/04/25 16:54:45
@Author  :   村长
@Version :   1.0
@Contact :   liumou.site@qq.com
@Desc    :   权限验证模块
"""

from os import system
from subprocess import getoutput
from sys import exit, platform

from plbm.base import os_type
from plbm.logger import ColorLogger


class Jurisdiction:
	def __init__(self, passwd, logs=True, log_file=None):
		"""
		权限验证
		:param passwd: 设置主机密码
		:param logs: 是否启用文本日志
		:param log_file: 日志文件
		"""
		self.log_file = log_file
		self.logs = logs
		self.loggers = ColorLogger(file=self.log_file, txt=logs, class_name=self.__class__.__name__)
		if platform.lower() == 'win32':
			self.loggers.error("不支持Windows系统")
			exit(2)
		self.passwd = passwd
		self.super_permissions = False
		self.os_type = os_type

	def verification(self, name):
		"""_summary_
		检测sudo权限是否能够获取并设置正确的密码
		最终密码可以通过实例变量获取(self.passwd)
		Args:
			name (str): 调用的函数名称
		Returns:
			bool: 是否取得sudo权限
		"""
		username = getoutput('echo $USER')
		uid = getoutput("echo $UID")
		if str(username).lower() == 'root' or str(uid) == '0':
			if self.logs:
				self.loggers.info('已处于root权限')
			return True
		if self.os_type.lower() == 'uos'.lower():
			self.developer()
		else:
			self.super_permissions = True
		if self.super_permissions:
			self.loggers.info('调用函数: %s' % name)
			c = "echo %s | sudo -S touch /d" % self.passwd
			d = "echo %s | sudo -S rm -f /d" % self.passwd
			res = system(c)
			if str(res) == '0':
				system(d)
				return True
			self.loggers.error('密码错误或者当前用户无sudo权限')
		return False

	def developer(self):
		"""_summary_
		检查是否开启开发者模式
		Returns:
			bool: 是否开启开发者
		"""
		dev_file = "/var/lib/deepin/developer-install_modes/enabled"
		dev1 = str(getoutput(cmd="cat %s") % dev_file).replace(" ", '').replace('\n', '')

		dev_file2 = "/var/lib/deepin/developer-install_mode/enabled"
		dev2 = str(getoutput(cmd="cat %s") % dev_file2).replace(" ", '').replace('\n', '')

		dev_file3 = "cat /var/lib/deepin/developer-mode/enabled"
		dev3 = str(getoutput(cmd=dev_file3)).replace(" ", '').replace('\n', '')

		terminal_mode = False
		if dev1 == "1" or dev2 == "1" or dev3 == "1":
			terminal_mode = True
		elif str(getoutput('echo $UID')) != '0' and str(getoutput('echo $USER')) == "root" or str(
				getoutput('echo $UID')) == '0':
			terminal_mode = True
		self.super_permissions = terminal_mode
		if self.super_permissions:
			self.loggers.info('已开启开发者')
			return True
		else:
			self.loggers.warning('开发者未开启')
		return False


if __name__ == "__main__":
	ju = Jurisdiction(passwd='1')
	if ju.verification(name='Demo'):
		print('密码验证正确')
	else:
		print('密码验证失败')
