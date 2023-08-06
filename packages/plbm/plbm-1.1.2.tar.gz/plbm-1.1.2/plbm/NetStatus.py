# -*- encoding: utf-8 -*-
"""
@File    :   NetStatus.py
@Time    :   2022/04/13 11:19:25
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   网络管理
"""
from os import path, getcwd
from subprocess import getstatusoutput
from sys import platform

from requests import get as httpget

from plbm.cmd import ComMand
from plbm.FileManagement import FileManagement
from plbm.logger import ColorLogger


class NetStatus:
	def __init__(self, ip=None, port=None, log_file=None, txt_log=False):
		"""
		网络工具，用于判断网络是否正常
		:param ip: 需要判断的IP
		:param port:  需要判断的端口. Defaults to None.
		:param log_file: 日志文件
		:param txt_log: 是否开启文本日志
		"""
		self.ip = ip
		self.port = port
		self.status = False
		#
		self.headers = {}
		self._config()
		self.cmd = ComMand(password='Gxxc@123')
		self.fm = FileManagement()
		self.logger = ColorLogger(file=log_file, txt=txt_log)

	def _config(self):
		self.headers = {
			'Connection': 'keep-alive',
			'Cache-Control': 'max-age=0',
			'sec-ch-ua': '"Chromium";v="21", " Not;A Brand";v="99"',
			'sec-ch-ua-mobile': '?0',
			'sec-ch-ua-platform': '"Windows"',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'Sec-Fetch-Site': 'none',
			'Sec-Fetch-Mode': 'navigate',
			'Sec-Fetch-User': '?1',
			'Sec-Fetch-Dest': 'document',
			'Accept-Language': 'zh-CN,zh;q=0.9'}

	def ping_status(self, server=None):
		"""
		使用ping检测网络连接
		:param server: 设置服务器地址. Defaults to self.ip.
		:return:
		"""
		self.status = False
		if server is None:
			server = self.ip
		self.logger.info('正在检测： %s' % server)
		cmd = 'ping %s -c 5' % server
		if platform.lower() == 'win32':
			cmd = 'ping %s ' % server
		status = getstatusoutput(cmd)
		if status[0] == 0:
			self.logger.info("Ping 连接成功: %s" % server)
			self.status = True
		else:
			self.logger.error("Ping 连接失败: %s" % server)
		return self.status

	def httpstatus(self, server=None, port=None, url=None):
		"""
		检测HTTP服务是否正常访问,当设置URL的时候将会直接采用URL进行访问
		:param server:  HTTP服务器地址. Defaults to self.ip.
		:param port: 服务器端口. Defaults to self.port.
		:param url: 完整URL. Defaults to None.
		:return:
		"""
		self.status = False
		if server is None:
			server = self.ip
		if port is None:
			port = self.port
		if url is None:
			url = str(server) + ":" + str(port)
		status = httpget(url=str(url), headers=self.headers)
		if status.status_code == 200:
			self.status = True
		if self.status:
			self.logger.info("访问成功: %s" % url)
		else:
			self.logger.error("访问失败: %s" % url)
		return self.status

	def downfile(self, url, filename=None, cover=False, md5=None):
		"""
		下载文件
		:param url: 下载链接
		:param filename: 保存文件名,默认当前目录下以URL最后一组作为文件名保存
		:param cover: 是否覆盖已有文件. Defaults to False.
		:param md5: 检查下载文件MD5值
		:return: 下载结果(bool)
		"""
		if filename is None:
			filename = str(url).split("/")[-1]
			filename = path.join(getcwd(), filename)
		filename = path.abspath(filename)
		if path.exists(filename):
			if not cover:
				self.logger.info("检测到已存在路径: %s" % filename)
				self.logger.info("放弃下载： %s" % url)
				return True
			self.logger.debug("检测到已存在路径,正在删除...")
			c = 'rm -rf ' + filename
			if getstatusoutput(c)[0] == 0:
				self.logger.info("删除成功: %s" % filename)
			else:
				self.logger.warning("删除失败,跳过下载")
				return False
		c = str("wget -c -O %s %s" % (filename, url))
		self.cmd.shell(cmd=c, terminal=False)
		if int(self.cmd.code) == 0:
			self.logger.info("下载成功: %s" % filename)
			if md5:
				get_ = self.fm.get_md5(filename=filename)
				if get_:
					if str(md5).lower() == str(self.fm.md5).lower():
						return True
				else:
					return False
			return True
		self.logger.warning("下载失败: %s" % filename)
		print("下载链接: ", url)
		print("保存路径: ", filename)
		return False


if __name__ == "__main__":
	up = NetStatus()
	up.httpstatus(url='http://baidu.com')
	up.ping_status(server='baidu.com')
