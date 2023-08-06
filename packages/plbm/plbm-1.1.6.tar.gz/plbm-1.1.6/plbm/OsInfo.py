# -*- encoding: utf-8 -*-
import platform
from os import environ, getenv
from subprocess import getoutput

os_type = 'Windows'
os_arch = platform.machine()
os_ver = platform.release()
home_dir = ''
os_release = platform.release()
username = getenv("USER")
uid = 1
if platform.system().lower() == 'linux':
	home_dir = environ["HOME"]
	os_type = getoutput("""grep ^ID /etc/os-release | sed 's/ID=//' | sed -n 1p | sed 's#\"##g'""")
	os_ver = getoutput(cmd="""grep ^Min /etc/os-version | awk -F '=' '{print $2}'""")
	if str(os_type).lower() == 'kylin'.lower():
		os_ver = getoutput(cmd="""cat /etc/kylin-build | sed -n 2p | awk '{print $2}'""")
	uid = getoutput('echo $UID')
else:
	home_dir = environ["USERPROFILE"]
	username = environ["USERNAME"]


class OsInfo:
	def __init__(self):
		self.os_type = 'Windows'
		self.os_arch = platform.machine()
		self.os_ver = platform.release()
		self.home_dir = ''
		self.os_release = platform.release()
		self.username = getenv("USER")
		self.uid = 1
		if platform.system().lower() == 'linux':
			self.home_dir = environ["HOME"]
			self.os_type = getoutput("""grep ^ID /etc/os-release | sed 's/ID=//' | sed -n 1p | sed 's#\"##g'""")
			self.os_ver = getoutput(cmd="""grep ^Min /etc/os-version | awk -F '=' '{print $2}'""")
			if str(self.os_type).lower() == 'kylin'.lower():
				self.os_ver = getoutput(cmd="""cat /etc/kylin-build | sed -n 2p | awk '{print $2}'""")
			self.uid = getoutput('echo $UID')
		else:
			self.home_dir = environ["USERPROFILE"]
			self.username = environ["USERNAME"]

	def show(self):
		"""
		显示信息
		:return:
		"""
		print("系统类型: ", self.os_type)
		print("系统版本: ", self.os_ver)
		print("系统架构: ", self.os_arch)
		print("release: ", self.os_release)
		print("登录用户: ", self.username)
		print("用户目录: ", self.home_dir)
		print("用户ID: ", self.uid)
