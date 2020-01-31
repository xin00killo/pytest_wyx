#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx
from configs.config_wyx import baseConf


class GlobalVar:
    """需要定义全局变量的放在这里，最好定义一个初始值"""
    basic_path = baseConf.base_path  # 基础路径，默认等于项目的根路径
    log_file = None  # 日志文件的路径，默认None
    log_dict = dict()  # 分模块的日志文件路径集合


# 对于每个全局变量，都需要定义get_value和set_value接口
def set_basic_path(basic_path):
    GlobalVar.basic_path = basic_path


def get_basic_path():
    return GlobalVar.basic_path


def set_log_file(log_file):
    GlobalVar.log_file = log_file


def get_log_file():
    return GlobalVar.log_file


def set_log_dict(key, value):
    GlobalVar.log_dict[key] = value


def get_log_dict():
    return GlobalVar.log_dict
