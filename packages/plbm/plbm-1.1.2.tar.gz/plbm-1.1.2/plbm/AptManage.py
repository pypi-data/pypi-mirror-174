# -*- encoding: utf-8 -*-
"""
@File    :   AptManage.py
@Time    :   2022-09-05 09:17
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
from plbm.cmd import ComMand
from plbm.logger import ColorLogger
from plbm.Jurisdiction import Jurisdiction


class AptManagement:
	def __init__(self, password, log=False, terminal=False, package=None, file=None):
		"""
		Apt 管理
		:param password: 主机密码
		:param log: 是否启用日志
		:param terminal: 是否使用终端执行命令(针对个别Linux发行部才起作用)
		:param package: 包名
		"""
		self.package = package
		self.terminal = terminal
		self.log = log
		self.password = password
		ju = Jurisdiction(passwd=password, log_file=file)
		if not ju.verification(name='AptManagement'):
			exit(1)
		self.cmd = ComMand(password=self.password, cmd='which apt', terminal=self.terminal, logs=self.log)
		self.logger = ColorLogger(file=file, txt=log, class_name=self.__class__.__name__)

	def install(self, pac='git', update=False):
		"""
		安装在线包
		:param update: 是否更新源索引(默认不会更新源索引)
		:param pac: 需要安装的包(字符串)
		:return:
		"""
		if update:
			self.update_index()
		print("Installing %s ..." % pac)
		cmd = str("apt install -y %s" % pac)
		return self.cmd.sudo(cmd=cmd, name='Install %s' % pac)

	def update_index(self):
		"""
		更新索引
		:return:
		"""
		return self.cmd.sudo(cmd="apt update", name="Update Sources Index")

	def installed(self, pac=None):
		"""
		查询是否已安装包
		:param pac: 包名
		:return: 返回是否已安装(bool)
		"""
		if pac is None:
			pac = self.package
		if pac is None:
			self.logger.error('未传入有效包名')
			exit(2)
		self.cmd.getout(cmd="dpkg -s %s" % pac)
		if self.cmd.code == 0:
			return True
		return False

	def local_install_f(self, file):
		"""
		实现apt install -y -f ./install.deb的效果
		:param file:
		:return:
		"""
		return self.cmd.sudo(cmd="apt install -y -f %s" % file, name='Install Local Package')

	def install_f(self):
		"""
		执行apt install -y -f 修正环境,此功能慎用,如果处理不好可能对系统组件造成损害
		:return:
		"""
		self.update_index()
		return self.cmd.sudo(cmd="apt install -y -f", name='Install Local Package')

	def reinstall_rc(self, update=False):
		"""
		一键修复 rc 状态的包列表
		:param update: 是否更新源索引(默认不会更新源索引)
		:return:执行结果(bool)
		"""
		if update:
			self.update_index()
		cmd = "apt install -y --reinstall `dpkg -l | grep -v ii  | grep rc | awk '{print $2}' | sed '1,5 d'`"
		return self.cmd.sudo(cmd=cmd, name='List of packages to repair rc status', terminal=False)

	def remove_rc(self, update=False):
		"""
		一键卸载 rc 状态的包列表
		:param update: 是否更新源索引(默认不会更新源索引)
		:return:执行结果(bool)
		"""
		if update:
			self.update_index()
		cmd = "apt purge -y `dpkg -l | grep -v ii  | grep rc | awk '{print $2}' | sed '1,5 d'`"
		return self.cmd.sudo(cmd=cmd, name='List of packages in unloaded rc status', terminal=False)

	def upgrade(self, update=True):
		"""
		执行apt-get upgrade时，upgrade是根据update更新的索引记录来下载并更新软件包
		:param update: 是否更新源索引(默认不会更新源索引)
		:return:
		"""
		if update:
			self.update_index()
		cmd = 'apt upgrade -y --fix-missing'
		return self.cmd.sudo(cmd=cmd, terminal=False, name='更新系统-upgrade')

	def upgrade_dist(self, update=True):
		"""
		执行apt-get dist-upgrade时，除了拥有upgrade的全部功能外，dist-upgrade会比upgrade更智能地处理需要更新的软件包的依赖关系
		:param update: 是否更新源索引(默认不会更新源索引)
		:return: 更新结果
		"""
		if update:
			self.update_index()
		cmd = 'apt dist-upgrade -y --fix-missing'
		return self.cmd.sudo(cmd=cmd, terminal=False, name='更新系统-dist-upgrade')
