#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx

import logging
import os
import time
from logging.handlers import RotatingFileHandler

from configs import global_wyx
from configs.config_wyx import logConf, projectConf


class LoggerWyx:
    def __init__(self, logger_name=logConf.logger_name):
        # 获取配置信息
        self.__log_path = logConf.log_path
        self.__max_bytes_each = logConf.max_bytes_each
        self.__backup_count = logConf.backup_count
        self.__fmt_logfile = logConf.fmt_logfile
        self.__fmt_console = logConf.fmt_console
        self.__logger_name = logger_name.lower()  # 默认为 ini文件中配置的名称，如果实例化的时候重新配置，则使用新名称
        self.__log_level_in_console = logConf.log_level_in_console
        self.__log_level_in_logfile = logConf.log_level_in_logfile
        self.__console_log_on = logConf.console_log_on
        self.__logfile_log_on = logConf.logfile_log_on
        self.__dist_log_on = logConf.dist_log_on
        self.__project_name = projectConf.project_name

        # 创建log对象
        self.__logger = logging.getLogger(self.__logger_name)
        self.__logger.setLevel(10)
        self.__config_logger()

    # 提供外部获取logger的方法
    def get_logger(self):
        return self.__logger

    # 添加控制台/文件打印信息
    def __config_logger(self):
        if self.__console_log_on:  # 如果开启控制台日志
            # print('__config_logger', self.__console_log_on)
            console = logging.StreamHandler()
            fmt_console = self.__fmt_console.replace('|', '%')
            formatter_console = logging.Formatter(fmt_console)
            console.setFormatter(formatter_console)
            self.__logger.addHandler(console)
            self.__logger.setLevel(self.__log_level_in_console)

        if self.__logfile_log_on:  # 如果开启文件日志  创建并记录所有日志
            # 配置log文件路径
            if global_wyx.get_log_file() is None:  # 如果还未创建过，则新建一个新log-handler文件
                self.__log_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
                if not os.path.exists(self.__log_path):
                    os.makedirs(self.__log_path)
                log_file = os.path.join(self.__log_path, '{}_{}.log'.format(self.__project_name, self.__log_time))
                # 设置全局变量中的log_file 和 log_dict
                global_wyx.set_log_file(log_file)
                global_wyx.set_log_dict(self.__project_name, log_file)
                rt_file_handler = RotatingFileHandler(log_file, maxBytes=self.__max_bytes_each,
                                                      backupCount=self.__backup_count, encoding='utf-8')
                fmt_logfile = self.__fmt_logfile.replace('|', '%')
                formatter_logfile = logging.Formatter(fmt_logfile)
                rt_file_handler.setFormatter(formatter_logfile)
                self.__logger.addHandler(rt_file_handler)
                self.__logger.setLevel(self.__log_level_in_logfile)

        if self.__dist_log_on:  # 如果开启分块儿文件日志  创建并记录各个不同logname的日志
            # 配置log文件路径
            if self.__logger_name not in global_wyx.get_log_dict():  # 如果不在，则创建新的，并存储到log_dict字典中
                self.__log_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
                if not os.path.exists(self.__log_path):
                    os.makedirs(self.__log_path)
                log_file = os.path.join(self.__log_path, '{}_{}.log'.format(self.__logger_name, self.__log_time))
                # 设置全局变量中的log_dict
                global_wyx.set_log_dict(self.__logger_name, log_file)
                rt_dist_handler = RotatingFileHandler(log_file, maxBytes=self.__max_bytes_each,
                                                      backupCount=self.__backup_count, encoding='utf-8')
                rt_file_handler = RotatingFileHandler(global_wyx.get_log_dict()[self.__project_name], maxBytes=self.__max_bytes_each,
                                                      backupCount=self.__backup_count, encoding='utf-8')
                fmt_logfile = self.__fmt_logfile.replace('|', '%')
                formatter_logfile = logging.Formatter(fmt_logfile)
                rt_dist_handler.setFormatter(formatter_logfile)
                rt_file_handler.setFormatter(formatter_logfile)
                self.__logger.addHandler(rt_dist_handler)
                self.__logger.addHandler(rt_file_handler)
                self.__logger.setLevel(self.__log_level_in_logfile)


# 设置一个默认的log文件，公共模块直接使用这个就好啦~
log = LoggerWyx().get_logger()


if __name__ == '__main__':
    log.debug('debug')
    log.debug('debug')
    log.debug('debug')
    log.debug('debug')
    log.debug('debug')
    log.debug('debug')
    log.debug('debug')
    log.debug('debug')
