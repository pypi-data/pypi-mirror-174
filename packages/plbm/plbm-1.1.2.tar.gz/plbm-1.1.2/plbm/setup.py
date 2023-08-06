# -*- encoding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
	long_description = fh.read()
setuptools.setup(
	name="plbm",
	version="1.0.7",
	author="坐公交也用券",
	author_email="liumou.site@qq.com",
	description="这是一个Linux管理脚本的基础库，通过对Linux基本功能进行封装，实现快速开发的效果",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitee.com/liumou_site/PythonLinuxBasicModule",
	packages=["plbm"],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",

	],
	# Py版本要求
	python_requires='>=3.0',
	# 依赖
	install_requires=[
		"requests>=2.9.0",
		"urllib3>=1.13.1",
		"colorama>=0.2.0", ]
)
