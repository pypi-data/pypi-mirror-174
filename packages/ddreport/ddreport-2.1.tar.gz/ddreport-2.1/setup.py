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
    version = "2.1",
    keywords = ("pip", "pytest","testReport"),
    description = "pytest测试报告",
    long_description = "这个版本修复了报告中结果筛选错误的问题（跳过和错误筛选）；然后解决了响应体是html格式时报告乱码问题；优化测试结果的tab",
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
