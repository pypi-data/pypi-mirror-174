# -*- encoding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
	long_description = fh.read()
setuptools.setup(
	name="colorloggers",
	version="1.1.2",
	author="坐公交也用券",
	author_email="liumou.site@qq.com",
	description="这是一个使用Pyhon3编写的简单的日志输出模块，特色是使用简单，彩色输出",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitee.com/liumou_site/pypicolorloggers.git",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",

	],
	# Py版本要求
	python_requires='>=3.0',
	# 依赖
	install_requires=[
		"colorama>=0.2.0", ]
)
