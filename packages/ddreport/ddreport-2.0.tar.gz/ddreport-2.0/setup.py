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
    version = "2.0",
    keywords = ("pip", "pytest","testReport"),
    description = "pytest测试报告",
    long_description = "支持--report、--title、--tester、--desc、--project、--path、--file_sub 关键字",
    license = "MIT Licence",

    url = "https://gitee.com/duanliangcong/dlc_pytest-report",
    author = "duanliangcong",
    author_email = "137562703@qq.com",
    entry_points={"pytest11": ["test_report = ddreport.testReport"]},

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["pytest"],
    # packages=find_namespace_packages(include=["template", "template.*"], ),
)
