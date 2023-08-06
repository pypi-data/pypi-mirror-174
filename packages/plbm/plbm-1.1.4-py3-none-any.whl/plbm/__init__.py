#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py.py
@Time    :   2022-10-24 00:20
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   这是一个Linux管理脚本的基础库，通过对Linux基本功能进行封装，实现快速开发的效果
"""
from .Logger import ColorLogger
from .Cmd import ComMand
from .AptManage import AptManagement
from .OsInfo import *
from .Dpkg import DpkgManagement
from .FileManagement import FileManagement
from .get import headers, cookies
from .Jurisdiction import Jurisdiction
from .NetManagement import NetManagement
from .NetStatus import NetStatus
from .Package import PackageManagement
from .Service import ServiceManagement
from .Yum import YumManager
from .iptables import IpTables
from .OsInfo import OsInfo
import platform
from sys import exit

__all__ = ["ColorLogger", "ComMand", "AptManagement", "DpkgManagement", "FileManagement", "Jurisdiction",
           "NetManagement", "NetStatus", "PackageManagement", "ServiceManagement", "YumManager", "IpTables",
           "OsInfo"]

if platform.system().lower() != 'linux'.lower():
	print('仅支持Linux系统')
	exit(1)
