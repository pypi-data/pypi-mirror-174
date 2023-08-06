#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: duanliangcong
# Mail: 137562703@qq.com
# Created Time:  2022-11-02 15:00:00
#############################################

# pip install twine
# python setup.py sdist
# twine upload dist/*

from setuptools import setup, find_packages, find_namespace_packages

setup(
    name = "ddreport",
    version = "2.2",
    keywords = ("pip", "pytest","testReport"),
    description = "pytest测试报告",
    long_description = "这个版本修复上个版本中报告结果筛选没变更过来的问题",
    license = "MIT Licence",

    url = "https://gitee.com/duanliangcong/dlc_pytest-report.git",
    author = "duanliangcong",
    author_email = "137562703@qq.com",
    entry_points={"pytest11": ["test_report = ddreport.testReport"]},

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["pytest", "requests"],
    # packages=find_namespace_packages(include=["template", "template.*"], ),
)
