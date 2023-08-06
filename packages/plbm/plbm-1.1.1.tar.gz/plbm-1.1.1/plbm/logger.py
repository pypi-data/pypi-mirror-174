# -*- encoding: utf-8 -*-
"""
@File    :   logger.py
@Time    :   2022-10-19 16:01
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   这是一个支持彩色输出,文本记录,文本覆盖的日志模块
"""
from os import path, getenv
from colorama import Fore, Style
from datetime import datetime
import inspect
from platform import system


class ColorLogger:
	def __init__(self, file=None, txt=False, class_name=None, cover=False):
		"""
		日志模块
		:param file: 设置日志文件
		:param txt: 是否启用文本记录功能
		:param class_name: 调用的Class名称
		:param cover: 当使用文本记录的时候，是否覆盖原内容
		"""
		self.cover = cover
		self.class_name = class_name
		self.wr_txt = txt
		if file is None:
			file = path.join(getenv("HOME"), 'plbm.log')
		self.file = file
		self.date = str(datetime.now()).split('.')[0]
		self.txt = open(file=self.file, mode='a+', encoding='utf-8')
		if self.cover:
			self.txt.close()
			self.txt = open(file=self.file, mode='w+', encoding='utf-8')
		self.line_ = 1
		self.module_name = None
		self.filename = None
		self.msg1 = None

	def fun_info(self, info):
		"""
		获取function信息
		:param info:
		:return:
		"""
		self.line_ = info[1]
		self.module_name = info[2]
		filename = info[0]
		filename = str(filename).split('/')[-1]
		if system().lower() == 'windows'.lower():
			filename = path.split(filename)[1]
		self.filename = filename

	def create_msg(self, msg, level='DEBUG'):
		"""
		创建信息
		:param msg: 信息
		:param level: 信息级别
		:return:
		"""
		msg1 = self.date + " " + self.filename + "  line: " + str(self.line_)
		if self.class_name is not None:
			msg1 = str(msg1) + " - Class: " + str(self.class_name)
		if self.module_name != '<module>':
			msg1 = str(msg1) + " function: " + self.module_name
		msg1 = str(msg1) + " - %s : " % level + msg
		self.msg1 = msg1

	def wr(self):
		try:
			if self.wr_txt:
				self.txt.write(self.msg1)
				self.txt.write("\n")
		except Exception as e:
			print(Fore.RED + str(e) + Style.RESET_ALL)

	def _arg(self, arg):
		"""
		解析参数
		:param arg:
		:return:
		"""
		arg_ = ''
		for i in arg:
			arg_ = arg_ + str(i)
		return arg_

	def _get_time(self):
		self.date = str(datetime.now()).split('.')[0]

	def info(self, msg, *arg, **kwarg):
		"""
		打印信息
		:param msg: 打印内容
		:return:
		"""
		fun_info = inspect.getframeinfo(inspect.currentframe().f_back)
		self.fun_info(info=fun_info)
		self._get_time()
		if arg:
			msg = str(msg) + str(self._arg(arg=arg))
		if kwarg:
			msg = str(msg) + str(self._arg(arg=kwarg))
		self.create_msg(msg=msg, level="INFO")
		mess = str(Fore.GREEN + self.msg1 + Style.RESET_ALL)
		print(mess)
		self.wr()

	def debug(self, msg, *arg, **kwarg):
		"""
		打印信息
		:param msg: 打印内容
		:return:
		"""
		fun_info = inspect.getframeinfo(inspect.currentframe().f_back)
		self.fun_info(info=fun_info)
		self._get_time()
		if arg:
			msg = str(msg) + str(self._arg(arg=arg))
		if kwarg:
			msg = str(msg) + str(self._arg(arg=kwarg))
		self.create_msg(msg=msg)
		mess = str(Fore.BLUE + self.msg1 + Style.RESET_ALL)
		print(mess)
		self.wr()

	def warning(self, msg, *arg, **kwarg):
		"""
		打印信息
		:param msg: 打印内容
		:return:
		"""
		fun_info = inspect.getframeinfo(inspect.currentframe().f_back)
		self.fun_info(info=fun_info)
		self._get_time()
		if arg:
			msg = str(msg) + str(self._arg(arg=arg))
		if kwarg:
			msg = str(msg) + str(self._arg(arg=kwarg))
		self.create_msg(msg=msg, level="WARNING")
		mess = str(Fore.YELLOW + self.msg1 + Style.RESET_ALL)
		print(mess)
		self.wr()

	def error(self, msg, *arg, **kwarg):
		"""
		打印信息
		:param msg: 打印内容
		:return:
		"""
		fun_info = inspect.getframeinfo(inspect.currentframe().f_back)
		self.fun_info(info=fun_info)
		self._get_time()
		if arg:
			msg = str(msg) + str(self._arg(arg=arg))
		if kwarg:
			msg = str(msg) + str(self._arg(arg=kwarg))
		self.create_msg(msg=msg, level="ERROR")
		mess = str(Fore.RED + self.msg1 + Style.RESET_ALL)
		print(mess)
		self.wr()


if __name__ == "__main__":
	log = ColorLogger(file='txt.log', txt=True)
	log.info(msg='1', x="23")
	log.error('2', '22', '222')
	log.debug('3', '21')
	log.warning('4', '20', 22)
