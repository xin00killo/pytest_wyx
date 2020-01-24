# #coding=utf-8
# # __autor__='wyxces'
#
import logging
import os
import re
import time
from logging.handlers import RotatingFileHandler

from common.utils_wyx import singleton
from configs.read_configini import logConf, projectConf

@singleton
class LoggerWyx:
    def __init__(self):
        # 获取配置信息
        self.__log_path = logConf.log_path
        self.__max_bytes_each = logConf.max_bytes_each
        self.__backup_count = logConf.backup_count
        self.__fmt_logfile = logConf.fmt_logfile
        self.__fmt_console = logConf.fmt_console
        self.__logger_name = logConf.logger_name
        self.__log_level_in_console = logConf.log_level_in_console
        self.__log_level_in_logfile = logConf.log_level_in_logfile
        self.__console_log_on = logConf.console_log_on
        self.__logfile_log_on = logConf.logfile_log_on
        self.__project_name = projectConf.project_name
        # 配置log文件路径
        self.__log_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        if not os.path.exists(self.__log_path):
            os.makedirs(self.__log_path)
        self.__log_file = os.path.join(self.__log_path, '{}_{}.log'.format(self.__project_name, self.__log_time))
        #创建log对象 并设置文件监控级别为 DEBUG
        self.__logger = logging.getLogger(self.__logger_name)
        self.__config_logger()

    def get_logger(self):
        return self.__logger

    def __config_logger(self):
        if self.__console_log_on:  # 如果开启控制台日志
            # print('__config_logger', self.__console_log_on)
            console = logging.StreamHandler()
            fmt_console = self.__fmt_console.replace('|', '%')
            formatter_console = logging.Formatter(fmt_console)
            console.setFormatter(formatter_console)
            self.__logger.addHandler(console)
            self.__logger.setLevel(self.__log_level_in_console)

        if self.__logfile_log_on:  # 如果开启文件日志
            rt_file_handler = RotatingFileHandler(self.__log_file, maxBytes=self.__max_bytes_each,
                                                  backupCount=self.__backup_count, encoding='utf-8')
            fmt_logfile = self.__fmt_logfile.replace('|', '%')
            formatter_logfile = logging.Formatter(fmt_logfile)
            rt_file_handler.setFormatter(formatter_logfile)
            self.__logger.addHandler(rt_file_handler)
            self.__logger.setLevel(self.__log_level_in_logfile)


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


